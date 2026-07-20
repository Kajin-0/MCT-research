#!/usr/bin/env python3
"""Test composition-shape transfer on the Chu 1991 300 K edge series."""
from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable
from pathlib import Path

import numpy as np

from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import (
    chu_1983_gap_ev,
    schmit_stelzer_1969_gap_ev,
    seiler_1990_gap_ev,
    weiler_1977_gap_ev,
    wiley_dexter_1969_gap_ev,
)

Model = Callable[[float | np.ndarray, float], float | np.ndarray]
MODELS: dict[str, Model] = {
    "schmit_stelzer_1969": schmit_stelzer_1969_gap_ev,
    "wiley_dexter_1969": wiley_dexter_1969_gap_ev,
    "weiler_1977": weiler_1977_gap_ev,
    "hansen_1982": hansen_gap_ev,
    "seiler_1990": seiler_1990_gap_ev,
    "laurenti_reconstructed": laurenti_gap_ev,
    "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    "chu_1983": chu_1983_gap_ev,
}


def load_series(path: str | Path) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported Chu turning-point schema")
    if data.get("measurement_class") != "absorption_turning_point_edge":
        raise ValueError("Chu measurement class changed")
    if data.get("value_status") != "printed_figure_labels":
        raise ValueError("Chu values must remain printed figure labels")
    if data["source"]["doi"] != "10.1016/0020-0891(91)90110-2":
        raise ValueError("Chu 1991 DOI changed")
    rows = data["composition_series_300K"]["rows"]
    if len(rows) != 8:
        raise ValueError("Chu 300 K composition inventory is incomplete")
    if float(data["composition_series_300K"]["temperature_K"]) != 300.0:
        raise ValueError("Chu composition series temperature changed")
    return data


def metrics(residuals_ev: np.ndarray) -> dict[str, float | int]:
    residuals = np.asarray(residuals_ev, dtype=float)
    return {
        "count": int(residuals.size),
        "mae_meV": float(1000.0 * np.mean(np.abs(residuals))),
        "rmse_meV": float(1000.0 * math.sqrt(float(np.mean(residuals**2)))),
        "bias_meV": float(1000.0 * np.mean(residuals)),
        "max_abs_meV": float(1000.0 * np.max(np.abs(residuals))),
    }


def leave_one_out_offset_errors(
    predicted_ev: np.ndarray,
    observed_ev: np.ndarray,
) -> np.ndarray:
    """Estimate one observation-class offset on n-1 rows and predict the holdout."""

    errors = np.empty_like(predicted_ev)
    for index in range(predicted_ev.size):
        training_offset = float(
            np.mean(np.delete(observed_ev - predicted_ev, index))
        )
        errors[index] = predicted_ev[index] + training_offset - observed_ev[index]
    return errors


def analyze(path: str | Path) -> dict[str, object]:
    data = load_series(path)
    series = data["composition_series_300K"]
    temperature = float(series["temperature_K"])
    rows = series["rows"]
    compositions = np.asarray([row["composition_x"] for row in rows], dtype=float)
    observed = np.asarray([row["edge_eV"] for row in rows], dtype=float)

    shared_shift_grid = np.linspace(-0.005, 0.005, 401)
    comparisons: dict[str, dict[str, object]] = {}
    for name, model in MODELS.items():
        predicted = np.asarray(model(compositions, temperature), dtype=float)
        raw_residuals = predicted - observed

        fitted_offset = float(np.mean(observed - predicted))
        offset_corrected_residuals = predicted + fitted_offset - observed
        loo_errors = leave_one_out_offset_errors(predicted, observed)
        adjacent_increment_errors = np.diff(predicted) - np.diff(observed)

        shifted_loo_mae: list[float] = []
        shifted_loo_rmse: list[float] = []
        for shift in shared_shift_grid:
            shifted = np.asarray(model(compositions + shift, temperature), dtype=float)
            errors = leave_one_out_offset_errors(shifted, observed)
            shifted_metrics = metrics(errors)
            shifted_loo_mae.append(float(shifted_metrics["mae_meV"]))
            shifted_loo_rmse.append(float(shifted_metrics["rmse_meV"]))

        comparisons[name] = {
            "raw_absolute": metrics(raw_residuals),
            "fitted_observation_offset_meV": 1000.0 * fitted_offset,
            "offset_corrected_in_sample": metrics(offset_corrected_residuals),
            "leave_one_specimen_out_offset_transfer": metrics(loo_errors),
            "adjacent_composition_increment": metrics(adjacent_increment_errors),
            "shared_composition_shift_envelope": {
                "shift_interval": [
                    float(shared_shift_grid[0]),
                    float(shared_shift_grid[-1]),
                ],
                "loo_mae_meV_min": float(min(shifted_loo_mae)),
                "loo_mae_meV_max": float(max(shifted_loo_mae)),
                "loo_rmse_meV_min": float(min(shifted_loo_rmse)),
                "loo_rmse_meV_max": float(max(shifted_loo_rmse)),
            },
        }

    raw_rank = sorted(
        comparisons,
        key=lambda name: comparisons[name]["raw_absolute"]["mae_meV"],
    )
    loo_rank = sorted(
        comparisons,
        key=lambda name: comparisons[name][
            "leave_one_specimen_out_offset_transfer"
        ]["mae_meV"],
    )
    independent_names = [name for name in MODELS if name != "chu_1983"]
    independent_raw_rank = sorted(
        independent_names,
        key=lambda name: comparisons[name]["raw_absolute"]["mae_meV"],
    )
    independent_loo_rank = sorted(
        independent_names,
        key=lambda name: comparisons[name][
            "leave_one_specimen_out_offset_transfer"
        ]["mae_meV"],
    )

    seiler_loo = float(
        comparisons["seiler_1990"]["leave_one_specimen_out_offset_transfer"][
            "mae_meV"
        ]
    )
    hansen_loo = float(
        comparisons["hansen_1982"]["leave_one_specimen_out_offset_transfer"][
            "mae_meV"
        ]
    )
    pade_min = float(
        comparisons["provisional_hansen_pade"][
            "shared_composition_shift_envelope"
        ]["loo_mae_meV_min"]
    )
    hansen_max = float(
        comparisons["hansen_1982"]["shared_composition_shift_envelope"][
            "loo_mae_meV_max"
        ]
    )

    return {
        "schema_version": "1.0",
        "analysis": "Chu 1991 300 K composition-shape transfer",
        "measurement_class": data["measurement_class"],
        "value_status": data["value_status"],
        "temperature_K": temperature,
        "row_count": len(rows),
        "model_comparisons": comparisons,
        "raw_absolute_mae_rank": raw_rank,
        "leave_one_out_offset_mae_rank": loo_rank,
        "independent_raw_absolute_mae_rank": independent_raw_rank,
        "independent_leave_one_out_offset_mae_rank": independent_loo_rank,
        "decision": {
            "raw_independent_winner": independent_raw_rank[0],
            "offset_transfer_independent_winner": independent_loo_rank[0],
            "ranking_changes_after_observation_offset": (
                independent_raw_rank[0] != independent_loo_rank[0]
            ),
            "seiler_minus_hansen_loo_mae_meV": seiler_loo - hansen_loo,
            "pade_min_minus_hansen_max_shared_shift_meV": pade_min - hansen_max,
            "chu_1983_independent_validation_authorized": False,
            "seiler_over_hansen_material_law_selection_authorized": False,
            "universal_observation_offset_authorized": False,
            "new_universal_gap_refit_authorized": False,
            "reason": (
                "The raw turning-point residual ranking is reversed when a single "
                "source-class offset is estimated on seven specimens and transferred "
                "to the eighth. Hansen and Seiler then reproduce composition shape "
                "more accurately than the provisional Pade and Laurenti forms, and "
                "the Hansen-Pade separation survives a shared +/-0.005 composition "
                "shift. The fitted offset is source-specific, not a universal "
                "correction; printed-label precision, specimen composition error, "
                "carrier state, and the circular Chu source lineage block material-"
                "law selection."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.series_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
