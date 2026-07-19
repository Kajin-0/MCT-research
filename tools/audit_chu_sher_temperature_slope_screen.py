#!/usr/bin/env python3
"""Audit the secondary Chu-Sher HgCdTe temperature-coefficient screen.

The source reports one temperature coefficient per composition but does not
recover the primary fit interval or uncertainty. Linear-in-temperature models
have an unambiguous coefficient. Nonlinear models are therefore evaluated
under three declared observation operators rather than assigned one preferred
slope silently.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Callable

import numpy as np

from mct_research.gap_models import (
    HANSEN_PADE_ALPHA_EV_PER_K,
    HANSEN_PADE_TAU_K,
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import chu_1983_gap_ev


def _as_array(value: object) -> np.ndarray:
    return np.asarray(value, dtype=float)


def _model_values(
    model: Callable[[object, object], object],
    composition: np.ndarray,
    temperature_k: float,
) -> np.ndarray:
    return _as_array(model(composition, temperature_k))


def _secant_slope(
    model: Callable[[object, object], object],
    composition: np.ndarray,
    lower_k: float,
    upper_k: float,
) -> np.ndarray:
    return (
        _model_values(model, composition, upper_k)
        - _model_values(model, composition, lower_k)
    ) / (upper_k - lower_k)


def _hansen_local_slope(composition: np.ndarray, _: float) -> np.ndarray:
    return 5.35e-4 * (1.0 - 2.0 * composition)


def _chu_local_slope(composition: np.ndarray, _: float) -> np.ndarray:
    return (6.0 - 14.0 * composition + 3.0 * composition**2) * 1.0e-4


def _pade_local_slope(composition: np.ndarray, temperature_k: float) -> np.ndarray:
    temperature = float(temperature_k)
    tau2 = HANSEN_PADE_TAU_K**2
    derivative = (
        temperature**2 * (temperature**2 + 3.0 * tau2)
        / (temperature**2 + tau2) ** 2
    )
    return HANSEN_PADE_ALPHA_EV_PER_K * (1.0 - 2.0 * composition) * derivative


def _laurenti_local_slope(composition: np.ndarray, temperature_k: float) -> np.ndarray:
    temperature = float(temperature_k)
    one_minus_x = 1.0 - composition
    amplitude = (
        6.3 * one_minus_x
        - 3.25 * composition
        - 5.92 * composition * one_minus_x
    )
    scale = 11.0 * one_minus_x + 78.7 * composition
    derivative = temperature * (temperature + 2.0 * scale) / (temperature + scale) ** 2
    return 1.0e-4 * amplitude * derivative


def _metrics(observed: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    residual = observed - predicted
    residual_units = residual / 1.0e-4
    return {
        "mean_signed_residual_1e4_ev_per_k": float(np.mean(residual_units)),
        "mae_1e4_ev_per_k": float(np.mean(np.abs(residual_units))),
        "rmse_1e4_ev_per_k": float(np.sqrt(np.mean(residual_units**2))),
        "maximum_absolute_residual_1e4_ev_per_k": float(
            np.max(np.abs(residual_units))
        ),
    }


def _load(path: str | Path) -> tuple[np.ndarray, np.ndarray, list[dict[str, str]]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("temperature-slope screen is empty")
    composition = np.asarray([float(row["composition_x"]) for row in rows])
    coefficient = np.asarray(
        [float(row["temperature_coefficient_1e4_ev_per_k"]) * 1.0e-4 for row in rows]
    )
    if np.any(np.diff(composition) <= 0.0):
        raise ValueError("composition values must be strictly increasing")
    if not np.all(np.isfinite(coefficient)):
        raise ValueError("temperature coefficients must be finite")
    boundaries = {row["claim_boundary"] for row in rows}
    if boundaries != {
        "secondary_transcription_for_external_temperature_slope_screen_not_fit_authority"
    }:
        raise ValueError("every row must preserve the screen-only claim boundary")
    return composition, coefficient, rows


def analyze(path: str | Path) -> dict[str, object]:
    composition, observed, rows = _load(path)
    models: dict[str, Callable[[object, object], object]] = {
        "hansen": hansen_gap_ev,
        "chu_1983": chu_1983_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
        "laurenti": laurenti_gap_ev,
    }
    local_derivatives = {
        "hansen": _hansen_local_slope,
        "chu_1983": _chu_local_slope,
        "provisional_hansen_pade": _pade_local_slope,
        "laurenti": _laurenti_local_slope,
    }
    operators = {
        "local_derivative_at_300_k": {
            name: derivative(composition, 300.0)
            for name, derivative in local_derivatives.items()
        },
        "secant_80_to_300_k": {
            name: _secant_slope(model, composition, 80.0, 300.0)
            for name, model in models.items()
        },
        "secant_4p2_to_300_k": {
            name: _secant_slope(model, composition, 4.2, 300.0)
            for name, model in models.items()
        },
    }

    operator_results: dict[str, object] = {}
    rankings: dict[str, list[str]] = {}
    for operator_name, predictions in operators.items():
        model_results = {
            name: {
                "predicted_temperature_coefficients_1e4_ev_per_k": (
                    prediction / 1.0e-4
                ).tolist(),
                "metrics": _metrics(observed, prediction),
            }
            for name, prediction in predictions.items()
        }
        ranking = sorted(
            model_results,
            key=lambda name: model_results[name]["metrics"]["rmse_1e4_ev_per_k"],
        )
        rankings[operator_name] = ranking
        operator_results[operator_name] = {
            "ranking_lowest_rmse_first": ranking,
            "models": model_results,
        }

    linear_operator_invariance = {}
    for name in ("hansen", "chu_1983"):
        values = np.stack(
            [operators[operator_name][name] for operator_name in operators]
        )
        linear_operator_invariance[name] = float(
            np.max(np.abs(values - values[0])) / 1.0e-4
        )

    pade_ranks = [
        ranking.index("provisional_hansen_pade") + 1
        for ranking in rankings.values()
    ]
    winner_changes = len({ranking[0] for ranking in rankings.values()}) > 1
    result = {
        "schema_version": "1.0",
        "analysis": "secondary Chu-Sher Table 3.7 HgCdTe temperature-slope screen",
        "source_record_count": len(rows),
        "composition_range": [float(composition.min()), float(composition.max())],
        "observed_temperature_coefficients_1e4_ev_per_k": (
            observed / 1.0e-4
        ).tolist(),
        "operator_results": operator_results,
        "cross_operator_diagnostics": {
            "linear_model_maximum_operator_difference_1e4_ev_per_k": (
                linear_operator_invariance
            ),
            "winner_changes_with_nonlinear_slope_operator": winner_changes,
            "winners_by_operator": {
                name: ranking[0] for name, ranking in rankings.items()
            },
            "provisional_hansen_pade_rank_by_operator": dict(
                zip(rankings, pade_ranks, strict=True)
            ),
            "provisional_alpha_relative_to_hansen_slope_amplitude": float(
                HANSEN_PADE_ALPHA_EV_PER_K / 5.35e-4 - 1.0
            ),
        },
        "decision": {
            "primary_fit_authority": False,
            "coefficient_refit_authorized": False,
            "global_model_ranking_authorized": False,
            "screen_identifies_operator_dependence": winner_changes,
            "provisional_model_is_last_under_all_declared_operators": all(
                rank == 4 for rank in pade_ranks
            ),
            "interpretation": (
                "The source is a secondary transcription with no recovered primary fit "
                "interval or uncertainties. Laurenti is closest under the 4.2-300 K "
                "secant, while the source-family Chu relation is closest under the "
                "80-300 K secant and local 300 K derivative. The provisional Hansen-Pade "
                "law is systematically steeper and ranks last under all three declared "
                "operators. This is a cross-source screen and cannot select or refit a "
                "universal material law."
            ),
        },
        "claim_boundary": (
            "Secondary screen only. The table's primary source attribution, composition "
            "metrology, fit interval, and uncertainties are not recovered."
        ),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.input_csv)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
