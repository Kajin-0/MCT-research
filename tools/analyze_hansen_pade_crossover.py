#!/usr/bin/env python3
"""Test a one-scale zero-anchored replacement for Hansen's linear thermal term.

Candidate full equation, with energy in eV and temperature in kelvin::

    Eg(x,T) = -0.302 + 1.93 x - 0.81 x^2 + 0.832 x^3
              + 5.35e-4 (1 - 2 x) T^3 / (T^2 + tau^2)

The thermal kernel preserves Hansen's high-temperature slope, is exactly zero at
T=0, and introduces one global crossover temperature.  This script first tests
thermal shape with one profiled offset per held-out specimen, then performs a
stricter absolute-gap test on Seiler sample 3, whose composition is independently
reported.  The crossover is trained without using sample 3.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np

from tools.analyze_seiler1990_heldout_shape import (
    PUBLISHED_A_K3,
    PUBLISHED_B_K2,
    _fit_seiler_family,
    _hansen_shape,
    _load,
    _metrics,
    _offset_residuals,
    _seiler_shape,
)

HANSEN_SLOPE_MEV_PER_K = 0.535
TAU_MIN_K = 0.25
TAU_MAX_K = 300.0


def hansen_static_gap_ev(composition_x: float | np.ndarray) -> float | np.ndarray:
    x = np.asarray(composition_x, dtype=float)
    value = -0.302 + 1.93 * x - 0.81 * x**2 + 0.832 * x**3
    return float(value) if value.ndim == 0 else value


def pade_thermal_shape_mev(
    temperature_k: np.ndarray,
    composition_x: float,
    tau_k: float,
    slope_mev_per_k: float = HANSEN_SLOPE_MEV_PER_K,
) -> np.ndarray:
    temperature = np.asarray(temperature_k, dtype=float)
    tau = float(tau_k)
    slope = float(slope_mev_per_k)
    if tau <= 0.0 or not np.isfinite(tau):
        raise ValueError("tau_k must be finite and positive")
    if not np.isfinite(slope):
        raise ValueError("slope must be finite")
    return slope * (1.0 - 2.0 * float(composition_x)) * temperature**3 / (
        temperature**2 + tau**2
    )


def hansen_pade_gap_ev(
    composition_x: float | np.ndarray,
    temperature_k: float | np.ndarray,
    tau_k: float,
) -> float | np.ndarray:
    x = np.asarray(composition_x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    x, temperature = np.broadcast_arrays(x, temperature)
    thermal_ev = (
        5.35e-4
        * (1.0 - 2.0 * x)
        * temperature**3
        / (temperature**2 + float(tau_k) ** 2)
    )
    value = np.asarray(hansen_static_gap_ev(x), dtype=float) + thermal_ev
    scalar = np.asarray(composition_x).ndim == 0 and np.asarray(temperature_k).ndim == 0
    return float(value) if scalar else value


def published_seiler_gap_ev(
    composition_x: float | np.ndarray, temperature_k: float | np.ndarray
) -> float | np.ndarray:
    x = np.asarray(composition_x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    x, temperature = np.broadcast_arrays(x, temperature)
    thermal_ev = (
        5.35e-4
        * (1.0 - 2.0 * x)
        * (PUBLISHED_A_K3 + temperature**3)
        / (PUBLISHED_B_K2 + temperature**2)
    )
    value = np.asarray(hansen_static_gap_ev(x), dtype=float) + thermal_ev
    scalar = np.asarray(composition_x).ndim == 0 and np.asarray(temperature_k).ndim == 0
    return float(value) if scalar else value


def _profiled_sse(
    samples: dict[int, dict[str, Any]],
    train_ids: tuple[int, ...],
    shape: Callable[[np.ndarray, float], np.ndarray],
) -> float:
    residuals: list[float] = []
    for sample in train_ids:
        record = samples[sample]
        _, values = _offset_residuals(
            record["gap_mev"],
            shape(record["temperature_k"], record["composition_x"]),
        )
        residuals.extend(values.tolist())
    vector = np.asarray(residuals, dtype=float)
    return float(vector @ vector)


def _fit_fixed_slope_tau(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...]
) -> dict[str, float]:
    def objective(log_tau: float) -> float:
        tau = float(np.exp(log_tau))
        return _profiled_sse(
            samples,
            train_ids,
            lambda temperature, composition: pade_thermal_shape_mev(
                temperature, composition, tau
            ),
        )

    log_min = math.log(TAU_MIN_K)
    log_max = math.log(TAU_MAX_K)
    grid = np.linspace(log_min, log_max, 3001)
    values = np.asarray([objective(float(point)) for point in grid])
    best = int(np.argmin(values))
    lower = float(grid[max(0, best - 2)])
    upper = float(grid[min(grid.size - 1, best + 2)])
    ratio = (1.0 + math.sqrt(5.0)) / 2.0
    left = upper - (upper - lower) / ratio
    right = lower + (upper - lower) / ratio
    left_value = objective(left)
    right_value = objective(right)
    for _ in range(180):
        if left_value < right_value:
            upper, right, right_value = right, left, left_value
            left = upper - (upper - lower) / ratio
            left_value = objective(left)
        else:
            lower, left, left_value = left, right, right_value
            right = lower + (upper - lower) / ratio
            right_value = objective(right)
    log_tau = 0.5 * (lower + upper)
    return {"tau_k": float(np.exp(log_tau)), "training_sse_mev2": objective(log_tau)}


def _solve_free_slope_at_tau(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...], tau_k: float
) -> tuple[float, float]:
    rows: list[list[float]] = []
    target: list[float] = []
    for sample in train_ids:
        record = samples[sample]
        basis = (
            (1.0 - 2.0 * record["composition_x"])
            * record["temperature_k"] ** 3
            / (record["temperature_k"] ** 2 + tau_k**2)
        )
        for coefficient, gap in zip(basis, record["gap_mev"], strict=True):
            rows.append(
                [float(coefficient)]
                + [1.0 if candidate == sample else 0.0 for candidate in train_ids]
            )
            target.append(float(gap))
    design = np.asarray(rows, dtype=float)
    response = np.asarray(target, dtype=float)
    coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
    residuals = response - design @ coefficients
    return float(residuals @ residuals), float(coefficients[0])


def _fit_free_slope_tau(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...]
) -> dict[str, float]:
    def objective(log_tau: float) -> float:
        return _solve_free_slope_at_tau(samples, train_ids, float(np.exp(log_tau)))[0]

    grid = np.linspace(math.log(TAU_MIN_K), math.log(TAU_MAX_K), 3001)
    values = np.asarray([objective(float(point)) for point in grid])
    best = int(np.argmin(values))
    lower = float(grid[max(0, best - 2)])
    upper = float(grid[min(grid.size - 1, best + 2)])
    ratio = (1.0 + math.sqrt(5.0)) / 2.0
    left = upper - (upper - lower) / ratio
    right = lower + (upper - lower) / ratio
    left_value = objective(left)
    right_value = objective(right)
    for _ in range(180):
        if left_value < right_value:
            upper, right, right_value = right, left, left_value
            left = upper - (upper - lower) / ratio
            left_value = objective(left)
        else:
            lower, left, left_value = left, right, right_value
            right = lower + (upper - lower) / ratio
            right_value = objective(right)
    tau = float(np.exp(0.5 * (lower + upper)))
    sse, slope = _solve_free_slope_at_tau(samples, train_ids, tau)
    return {"tau_k": tau, "slope_mev_per_k": slope, "training_sse_mev2": sse}


def _absolute_metrics(
    observed_mev: np.ndarray, predicted_ev: np.ndarray
) -> dict[str, float]:
    return _metrics(observed_mev - 1000.0 * np.asarray(predicted_ev, dtype=float))


def analyze(path: str | Path) -> dict[str, Any]:
    samples = _load(path)
    pooled: dict[str, list[float]] = {
        "hansen_linear": [],
        "published_seiler": [],
        "trained_seiler": [],
        "fixed_slope_pade": [],
        "free_slope_pade": [],
    }
    folds: list[dict[str, Any]] = []

    for heldout in sorted(samples):
        train_ids = tuple(sample for sample in sorted(samples) if sample != heldout)
        fixed_fit = _fit_fixed_slope_tau(samples, train_ids)
        free_fit = _fit_free_slope_tau(samples, train_ids)
        seiler_fit = _fit_seiler_family(samples, train_ids)
        record = samples[heldout]
        shapes = {
            "hansen_linear": _hansen_shape(
                record["temperature_k"], record["composition_x"]
            ),
            "published_seiler": _seiler_shape(
                record["temperature_k"],
                record["composition_x"],
                PUBLISHED_A_K3,
                PUBLISHED_B_K2,
            ),
            "trained_seiler": _seiler_shape(
                record["temperature_k"],
                record["composition_x"],
                seiler_fit["a_k3"],
                seiler_fit["b_k2"],
            ),
            "fixed_slope_pade": pade_thermal_shape_mev(
                record["temperature_k"], record["composition_x"], fixed_fit["tau_k"]
            ),
            "free_slope_pade": pade_thermal_shape_mev(
                record["temperature_k"],
                record["composition_x"],
                free_fit["tau_k"],
                free_fit["slope_mev_per_k"],
            ),
        }
        for model, shape in shapes.items():
            offset, residuals = _offset_residuals(record["gap_mev"], shape)
            pooled[model].extend(residuals.tolist())
            folds.append(
                {
                    "heldout_sample": heldout,
                    "training_samples": list(train_ids),
                    "model": model,
                    "heldout_offset_mev": offset,
                    **_metrics(residuals),
                    "tau_k": fixed_fit["tau_k"]
                    if model == "fixed_slope_pade"
                    else free_fit["tau_k"]
                    if model == "free_slope_pade"
                    else None,
                    "slope_mev_per_k": free_fit["slope_mev_per_k"]
                    if model == "free_slope_pade"
                    else None,
                    "seiler_a_k3": seiler_fit["a_k3"]
                    if model == "trained_seiler"
                    else None,
                    "seiler_b_k2": seiler_fit["b_k2"]
                    if model == "trained_seiler"
                    else None,
                }
            )

    pooled_metrics = {
        model: _metrics(np.asarray(residuals, dtype=float))
        for model, residuals in pooled.items()
    }
    fixed_rows = [row for row in folds if row["model"] == "fixed_slope_pade"]
    free_rows = [row for row in folds if row["model"] == "free_slope_pade"]

    # Strict absolute test: train only on samples 1 and 2, then predict independent-x sample 3.
    absolute_fit = _fit_fixed_slope_tau(samples, (1, 2))
    independent = samples[3]
    temperature = independent["temperature_k"]
    observed = independent["gap_mev"]
    nominal_x = float(independent["composition_x"])
    sigma_x = 0.0015
    absolute_predictions = {
        "hansen_linear": np.asarray(hansen_static_gap_ev(nominal_x))
        + 1.0e-3 * _hansen_shape(temperature, nominal_x),
        "published_seiler": published_seiler_gap_ev(nominal_x, temperature),
        "fixed_slope_pade": hansen_pade_gap_ev(
            nominal_x, temperature, absolute_fit["tau_k"]
        ),
    }
    absolute = {
        model: _absolute_metrics(observed, prediction)
        for model, prediction in absolute_predictions.items()
    }
    uncertainty_scan: dict[str, dict[str, float]] = {}
    for model in absolute_predictions:
        rmses: list[float] = []
        for composition in np.linspace(nominal_x - sigma_x, nominal_x + sigma_x, 301):
            if model == "hansen_linear":
                prediction = np.asarray(hansen_static_gap_ev(composition)) + 1.0e-3 * _hansen_shape(
                    temperature, composition
                )
            elif model == "published_seiler":
                prediction = np.asarray(published_seiler_gap_ev(composition, temperature))
            else:
                prediction = np.asarray(
                    hansen_pade_gap_ev(composition, temperature, absolute_fit["tau_k"])
                )
            rmses.append(_absolute_metrics(observed, prediction)["rmse_mev"])
        uncertainty_scan[model] = {
            "minimum_rmse_mev_within_x_uncertainty": float(min(rmses)),
            "maximum_rmse_mev_within_x_uncertainty": float(max(rmses)),
        }

    fixed_rmse = pooled_metrics["fixed_slope_pade"]["rmse_mev"]
    trained_seiler_rmse = pooled_metrics["trained_seiler"]["rmse_mev"]
    hansen_rmse = pooled_metrics["hansen_linear"]["rmse_mev"]
    fixed_tau = np.asarray([float(row["tau_k"]) for row in fixed_rows])
    free_tau = np.asarray([float(row["tau_k"]) for row in free_rows])
    free_slope = np.asarray([float(row["slope_mev_per_k"]) for row in free_rows])
    promotion_checks = {
        "shape_rmse_improves_over_hansen_by_20_percent": fixed_rmse <= 0.8 * hansen_rmse,
        "shape_rmse_within_20_percent_of_two_parameter_seiler": fixed_rmse
        <= 1.2 * trained_seiler_rmse,
        "crossover_stable_within_factor_two": float(fixed_tau.max() / fixed_tau.min()) <= 2.0,
        "absolute_sample3_beats_hansen": absolute["fixed_slope_pade"]["rmse_mev"]
        < absolute["hansen_linear"]["rmse_mev"],
        "absolute_sample3_not_worse_than_published_seiler_by_more_than_1mev": absolute[
            "fixed_slope_pade"
        ]["rmse_mev"]
        <= absolute["published_seiler"]["rmse_mev"] + 1.0,
    }

    return {
        "schema_version": "1.0",
        "analysis": "Hansen-Pade one-crossover equation benchmark",
        "candidate_equation": (
            "Eg_eV(x,T)=-0.302+1.93*x-0.81*x^2+0.832*x^3+"
            "5.35e-4*(1-2*x)*T^3/(T^2+tau^2)"
        ),
        "candidate_properties": {
            "thermal_increment_at_zero_temperature": 0.0,
            "zero_temperature_first_derivative": 0.0,
            "high_temperature_slope_ev_per_k": "5.35e-4*(1-2*x)",
            "nonlinear_parameter_count": 1,
        },
        "pooled_heldout_shape_metrics": pooled_metrics,
        "folds": folds,
        "parameter_stability": {
            "fixed_slope_tau_k": fixed_tau.tolist(),
            "fixed_slope_tau_max_to_min_ratio": float(fixed_tau.max() / fixed_tau.min()),
            "free_slope_tau_k": free_tau.tolist(),
            "free_slope_tau_max_to_min_ratio": float(free_tau.max() / free_tau.min()),
            "free_slope_mev_per_k": free_slope.tolist(),
            "free_slope_max_to_min_ratio": float(
                np.max(np.abs(free_slope)) / np.min(np.abs(free_slope))
            ),
        },
        "independent_composition_absolute_test": {
            "heldout_sample": 3,
            "training_samples_for_tau": [1, 2],
            "composition_x": nominal_x,
            "composition_sigma_x": sigma_x,
            "tau_k": absolute_fit["tau_k"],
            "metrics": absolute,
            "composition_uncertainty_scan": uncertainty_scan,
        },
        "promotion_checks": promotion_checks,
        "decision": {
            "all_promotion_checks_pass": all(promotion_checks.values()),
            "candidate_promoted_to_repository_model": False,
            "interpretation": (
                "Promote only if the one-parameter crossover transfers nearly as well as "
                "the two-parameter Seiler family and improves the independent-composition "
                "absolute prediction. Otherwise retain it as a rejected reduction."
            ),
        },
        "claim_boundary": [
            "The three-specimen shape test profiles one additive offset per specimen.",
            "Samples 1 and 2 do not have independent compositions; they train only the temperature kernel.",
            "The strict absolute test uses sample 3, whose x=0.259+/-0.0015 is independently reported.",
            "The candidate has not been checked against all historical datasets or prior art.",
            "A fitted tau is an effective crossover scale, not an identified phonon temperature.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/seiler1990_figure7_digitized.csv",
    )
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.input_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
