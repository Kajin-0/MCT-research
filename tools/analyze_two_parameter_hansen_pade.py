#!/usr/bin/env python3
"""Benchmark a zero-anchored two-parameter HgCdTe thermal gap law.

Candidate full equation, with energy in eV and temperature in kelvin::

    Eg(x,T) = -0.302 + 1.93 x - 0.81 x^2 + 0.832 x^3
              + alpha (1 - 2 x) T^3 / (T^2 + tau^2)

``alpha`` is expressed in eV/K by the public equation and in meV/K inside the
fitting helpers.  The benchmark uses leakage-safe specimen holdouts for thermal
shape, a no-offset absolute prediction for independently composed Seiler sample
3, and a separate low-temperature check on independently composed samples 3-5.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from tools.analyze_hansen_pade_crossover import (
    _fit_free_slope_tau,
    analyze as analyze_one_parameter,
    hansen_static_gap_ev,
    pade_thermal_shape_mev,
    published_seiler_gap_ev,
)
from tools.analyze_seiler1990_heldout_shape import _hansen_shape, _load, _metrics


def two_parameter_gap_ev(
    composition_x: float | np.ndarray,
    temperature_k: float | np.ndarray,
    alpha_mev_per_k: float,
    tau_k: float,
) -> float | np.ndarray:
    x = np.asarray(composition_x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    x, temperature = np.broadcast_arrays(x, temperature)
    thermal_mev = pade_thermal_shape_mev(
        temperature,
        0.0,
        tau_k,
        slope_mev_per_k=alpha_mev_per_k,
    )
    # pade_thermal_shape_mev with x=0 supplies alpha*T^3/(T^2+tau^2).
    thermal_ev = 1.0e-3 * (1.0 - 2.0 * x) * thermal_mev
    values = np.asarray(hansen_static_gap_ev(x), dtype=float) + thermal_ev
    scalar = np.asarray(composition_x).ndim == 0 and np.asarray(temperature_k).ndim == 0
    return float(values) if scalar else values


def _absolute_metrics(observed_mev: np.ndarray, predicted_ev: np.ndarray) -> dict[str, float]:
    return _metrics(observed_mev - 1000.0 * np.asarray(predicted_ev, dtype=float))


def _load_independent_low_temperature(path: str | Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["present_work"].strip().lower() != "true":
                continue
            sample = row["sample_number"].strip()
            if sample not in {"3", "4", "5"}:
                continue
            sigma_text = row["composition_sigma_x"].strip()
            gap_sigma_text = row["gap_sigma_mev"].strip()
            rows.append(
                {
                    "sample_number": float(sample),
                    "composition_x": float(row["composition_x"]),
                    "composition_sigma_x": float(sigma_text),
                    "gap_mev": float(row["gap_mev"]),
                    "gap_sigma_mev": float(gap_sigma_text),
                    "temperature_min_k": 2.0,
                    "temperature_max_k": 10.0,
                    "temperature_midpoint_k": 6.0,
                }
            )
    if len(rows) != 3:
        raise ValueError("expected independently composed Seiler samples 3, 4 and 5")
    return rows


def _low_temperature_check(
    rows: list[dict[str, float]],
    *,
    alpha_mev_per_k: float,
    tau_k: float,
) -> dict[str, Any]:
    model_residuals: dict[str, list[float]] = {
        "hansen_linear": [],
        "published_seiler": [],
        "two_parameter_pade": [],
    }
    records: list[dict[str, Any]] = []
    for row in rows:
        x = row["composition_x"]
        temperature = row["temperature_midpoint_k"]
        observed = row["gap_mev"]
        predictions = {
            "hansen_linear": float(hansen_static_gap_ev(x))
            + 1.0e-3 * float(_hansen_shape(np.asarray([temperature]), x)[0]),
            "published_seiler": float(published_seiler_gap_ev(x, temperature)),
            "two_parameter_pade": float(
                two_parameter_gap_ev(x, temperature, alpha_mev_per_k, tau_k)
            ),
        }
        envelopes: dict[str, dict[str, float]] = {}
        for model in predictions:
            absolute_residuals: list[float] = []
            for composition in np.linspace(
                x - row["composition_sigma_x"],
                x + row["composition_sigma_x"],
                81,
            ):
                for trial_temperature in np.linspace(
                    row["temperature_min_k"], row["temperature_max_k"], 81
                ):
                    if model == "hansen_linear":
                        prediction = float(hansen_static_gap_ev(composition)) + 1.0e-3 * float(
                            _hansen_shape(np.asarray([trial_temperature]), composition)[0]
                        )
                    elif model == "published_seiler":
                        prediction = float(
                            published_seiler_gap_ev(composition, trial_temperature)
                        )
                    else:
                        prediction = float(
                            two_parameter_gap_ev(
                                composition,
                                trial_temperature,
                                alpha_mev_per_k,
                                tau_k,
                            )
                        )
                    absolute_residuals.append(abs(observed - 1000.0 * prediction))
            envelopes[model] = {
                "minimum_absolute_residual_mev": float(min(absolute_residuals)),
                "maximum_absolute_residual_mev": float(max(absolute_residuals)),
            }
            model_residuals[model].append(observed - 1000.0 * predictions[model])
        records.append(
            {
                **row,
                "nominal_predictions_ev_at_6k": predictions,
                "composition_temperature_envelopes": envelopes,
            }
        )
    return {
        "temperature_interpretation": "reported 2-10 K range evaluated at 6 K with a full 2-10 K envelope",
        "nominal_metrics": {
            model: _metrics(np.asarray(residuals, dtype=float))
            for model, residuals in model_residuals.items()
        },
        "records": records,
    }


def analyze(
    figure7_path: str | Path,
    low_temperature_path: str | Path,
) -> dict[str, Any]:
    one_parameter = analyze_one_parameter(figure7_path)
    samples = _load(figure7_path)
    sample_ids = tuple(sorted(samples))
    all_fit = _fit_free_slope_tau(samples, sample_ids)
    absolute_fit = _fit_free_slope_tau(samples, (1, 2))

    free_rows = [
        row for row in one_parameter["folds"] if row["model"] == "free_slope_pade"
    ]
    alpha_values = np.asarray(
        [float(row["slope_mev_per_k"]) for row in free_rows], dtype=float
    )
    tau_values = np.asarray([float(row["tau_k"]) for row in free_rows], dtype=float)

    independent = samples[3]
    temperatures = independent["temperature_k"]
    observed = independent["gap_mev"]
    nominal_x = float(independent["composition_x"])
    sigma_x = 0.0015
    predictions = {
        "hansen_linear": np.asarray(hansen_static_gap_ev(nominal_x))
        + 1.0e-3 * _hansen_shape(temperatures, nominal_x),
        "published_seiler": published_seiler_gap_ev(nominal_x, temperatures),
        "two_parameter_pade": two_parameter_gap_ev(
            nominal_x,
            temperatures,
            absolute_fit["slope_mev_per_k"],
            absolute_fit["tau_k"],
        ),
    }
    absolute_metrics = {
        model: _absolute_metrics(observed, prediction)
        for model, prediction in predictions.items()
    }
    uncertainty_scan: dict[str, dict[str, float]] = {}
    for model in predictions:
        rmses: list[float] = []
        for composition in np.linspace(nominal_x - sigma_x, nominal_x + sigma_x, 301):
            if model == "hansen_linear":
                prediction = np.asarray(hansen_static_gap_ev(composition)) + 1.0e-3 * _hansen_shape(
                    temperatures, composition
                )
            elif model == "published_seiler":
                prediction = np.asarray(
                    published_seiler_gap_ev(composition, temperatures)
                )
            else:
                prediction = np.asarray(
                    two_parameter_gap_ev(
                        composition,
                        temperatures,
                        absolute_fit["slope_mev_per_k"],
                        absolute_fit["tau_k"],
                    )
                )
            rmses.append(_absolute_metrics(observed, prediction)["rmse_mev"])
        uncertainty_scan[model] = {
            "minimum_rmse_mev_within_x_uncertainty": float(min(rmses)),
            "maximum_rmse_mev_within_x_uncertainty": float(max(rmses)),
        }

    low_temperature = _low_temperature_check(
        _load_independent_low_temperature(low_temperature_path),
        alpha_mev_per_k=absolute_fit["slope_mev_per_k"],
        tau_k=absolute_fit["tau_k"],
    )

    shape_metrics = one_parameter["pooled_heldout_shape_metrics"]
    candidate_rmse = shape_metrics["free_slope_pade"]["rmse_mev"]
    trained_seiler_rmse = shape_metrics["trained_seiler"]["rmse_mev"]
    published_seiler_rmse = shape_metrics["published_seiler"]["rmse_mev"]
    low_metrics = low_temperature["nominal_metrics"]
    promotion_checks = {
        "shape_rmse_within_10_percent_of_trained_seiler": candidate_rmse
        <= 1.10 * trained_seiler_rmse,
        "shape_rmse_beats_published_seiler": candidate_rmse < published_seiler_rmse,
        "alpha_stable_within_5_percent": float(alpha_values.max() / alpha_values.min())
        <= 1.05,
        "tau_stable_within_factor_two": float(tau_values.max() / tau_values.min())
        <= 2.0,
        "absolute_sample3_beats_hansen": absolute_metrics["two_parameter_pade"][
            "rmse_mev"
        ]
        < absolute_metrics["hansen_linear"]["rmse_mev"],
        "absolute_sample3_beats_published_seiler": absolute_metrics[
            "two_parameter_pade"
        ]["rmse_mev"]
        < absolute_metrics["published_seiler"]["rmse_mev"],
        "low_temperature_nominal_rmse_not_worse_than_hansen_by_more_than_0p5mev": low_metrics[
            "two_parameter_pade"
        ]["rmse_mev"]
        <= low_metrics["hansen_linear"]["rmse_mev"] + 0.5,
    }

    return {
        "schema_version": "1.0",
        "analysis": "two-parameter zero-anchored Hansen-Pade benchmark",
        "candidate_equation": (
            "Eg_eV(x,T)=-0.302+1.93*x-0.81*x^2+0.832*x^3+"
            "alpha_eV_per_K*(1-2*x)*T^3/(T^2+tau_K^2)"
        ),
        "all_specimen_shape_fit": {
            "alpha_mev_per_k": all_fit["slope_mev_per_k"],
            "alpha_ev_per_k": 1.0e-3 * all_fit["slope_mev_per_k"],
            "tau_k": all_fit["tau_k"],
            "profiled_training_sse_mev2": all_fit["training_sse_mev2"],
        },
        "pooled_heldout_shape_metrics": shape_metrics,
        "fold_parameter_stability": {
            "alpha_mev_per_k": alpha_values.tolist(),
            "alpha_mean_mev_per_k": float(alpha_values.mean()),
            "alpha_sample_standard_deviation_mev_per_k": float(
                alpha_values.std(ddof=1)
            ),
            "alpha_max_to_min_ratio": float(alpha_values.max() / alpha_values.min()),
            "tau_k": tau_values.tolist(),
            "tau_mean_k": float(tau_values.mean()),
            "tau_sample_standard_deviation_k": float(tau_values.std(ddof=1)),
            "tau_max_to_min_ratio": float(tau_values.max() / tau_values.min()),
        },
        "independent_composition_absolute_test": {
            "heldout_sample": 3,
            "training_samples": [1, 2],
            "composition_x": nominal_x,
            "composition_sigma_x": sigma_x,
            "alpha_mev_per_k": absolute_fit["slope_mev_per_k"],
            "tau_k": absolute_fit["tau_k"],
            "metrics": absolute_metrics,
            "composition_uncertainty_scan": uncertainty_scan,
        },
        "independent_low_temperature_composition_check": low_temperature,
        "promotion_checks": promotion_checks,
        "decision": {
            "all_promotion_checks_pass": all(promotion_checks.values()),
            "leading_analytical_candidate": all(promotion_checks.values()),
            "production_equation_authorized": False,
            "next_required_work": (
                "If promoted, implement the equation as an explicitly provisional model, "
                "test additional historical composition/temperature datasets, propagate "
                "composition uncertainty, and complete a prior-art search before novelty claims."
            ),
        },
        "claim_boundary": [
            "Only three Seiler Figure 7 temperature-series specimens are available.",
            "The shape test profiles one additive offset per held-out specimen.",
            "Samples 1 and 2 train thermal shape but do not independently validate composition.",
            "Sample 3 supplies the only strict absolute temperature-series test with independent x.",
            "The 2-10 K samples 3-5 test the static-plus-negligible-thermal limit but do not identify alpha or tau.",
            "Alpha and tau are effective coefficients, not identified microscopic phonon parameters.",
            "No novelty claim follows without a dedicated prior-art review and broader external validation."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--figure7-csv",
        default="data/experimental/seiler1990_figure7_digitized.csv",
    )
    parser.add_argument(
        "--low-temperature-csv",
        default="data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv",
    )
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.figure7_csv, args.low_temperature_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
