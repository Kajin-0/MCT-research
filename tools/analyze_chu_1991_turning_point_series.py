#!/usr/bin/env python3
"""Analyze the Chu 1991 turning-point edge series without refitting models."""
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

Model = Callable[[float, float], float]
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
    if len(data["source"]["input_asset_sha256"]) != 64:
        raise ValueError("Chu source lacks SHA-256 binding")
    if len(data["temperature_series"]["rows"]) != 7:
        raise ValueError("Chu x=0.276 temperature inventory is incomplete")
    if len(data["composition_series_300K"]["rows"]) != 8:
        raise ValueError("Chu 300 K composition inventory is incomplete")
    return data


def metrics(residuals_ev: np.ndarray) -> dict[str, float]:
    residuals = np.asarray(residuals_ev, dtype=float)
    return {
        "count": int(residuals.size),
        "mae_meV": float(1000.0 * np.mean(np.abs(residuals))),
        "rmse_meV": float(1000.0 * math.sqrt(float(np.mean(residuals**2)))),
        "bias_meV": float(1000.0 * np.mean(residuals)),
        "max_abs_meV": float(1000.0 * np.max(np.abs(residuals))),
    }


def analyze(path: str | Path) -> dict[str, object]:
    data = load_series(path)
    series = data["temperature_series"]
    rows = series["rows"]
    temperatures = np.asarray([row["temperature_K"] for row in rows], dtype=float)
    observed = np.asarray([row["edge_eV"] for row in rows], dtype=float)
    reference_temperature = float(series["reference_temperature_K"])
    reference_indices = np.flatnonzero(temperatures == reference_temperature)
    if reference_indices.size != 1:
        raise ValueError("Chu reference temperature must occur exactly once")
    reference_index = int(reference_indices[0])

    composition = float(series["composition_x"])
    composition_sigma = float(series["composition_sigma_conservative"])
    if composition_sigma != 0.005:
        raise ValueError("Chu conservative composition uncertainty changed")
    composition_grid = np.linspace(
        composition - composition_sigma,
        composition + composition_sigma,
        401,
    )

    temperature_comparisons: dict[str, dict[str, object]] = {}
    for name, model in MODELS.items():
        predicted = np.asarray(
            [model(composition, temperature) for temperature in temperatures],
            dtype=float,
        )
        absolute = predicted - observed
        anchored = (predicted - predicted[reference_index]) - (
            observed - observed[reference_index]
        )

        envelope_mae: list[float] = []
        envelope_300_error: list[float] = []
        for trial_x in composition_grid:
            trial = np.asarray(
                [model(float(trial_x), temperature) for temperature in temperatures],
                dtype=float,
            )
            trial_anchored = (trial - trial[reference_index]) - (
                observed - observed[reference_index]
            )
            envelope_mae.append(1000.0 * float(np.mean(np.abs(trial_anchored))))
            envelope_300_error.append(1000.0 * float(trial_anchored[-1]))

        temperature_comparisons[name] = {
            "absolute": metrics(absolute),
            "anchored_increment": metrics(anchored),
            "predicted_6_to_300_increment_meV": float(
                1000.0 * (predicted[-1] - predicted[reference_index])
            ),
            "observed_6_to_300_increment_meV": float(
                1000.0 * (observed[-1] - observed[reference_index])
            ),
            "composition_envelope": {
                "x_interval": [
                    float(composition_grid[0]),
                    float(composition_grid[-1]),
                ],
                "anchored_mae_meV_min": float(min(envelope_mae)),
                "anchored_mae_meV_max": float(max(envelope_mae)),
                "error_6_to_300_meV_min": float(min(envelope_300_error)),
                "error_6_to_300_meV_max": float(max(envelope_300_error)),
            },
        }

    composition_rows = data["composition_series_300K"]["rows"]
    composition_comparisons: dict[str, dict[str, float]] = {}
    for name, model in MODELS.items():
        residuals = np.asarray(
            [
                model(float(row["composition_x"]), 300.0) - float(row["edge_eV"])
                for row in composition_rows
            ],
            dtype=float,
        )
        composition_comparisons[name] = metrics(residuals)

    anchored_rank = sorted(
        temperature_comparisons,
        key=lambda name: temperature_comparisons[name]["anchored_increment"]["mae_meV"],
    )
    composition_rank = sorted(
        composition_comparisons,
        key=lambda name: composition_comparisons[name]["mae_meV"],
    )
    pade_mae = float(
        temperature_comparisons["provisional_hansen_pade"]["anchored_increment"]["mae_meV"]
    )
    hansen_mae = float(
        temperature_comparisons["hansen_1982"]["anchored_increment"]["mae_meV"]
    )
    pade_min = float(
        temperature_comparisons["provisional_hansen_pade"]["composition_envelope"][
            "anchored_mae_meV_min"
        ]
    )
    hansen_max = float(
        temperature_comparisons["hansen_1982"]["composition_envelope"][
            "anchored_mae_meV_max"
        ]
    )

    return {
        "schema_version": "1.0",
        "analysis": "Chu 1991 turning-point edge transfer screen",
        "measurement_class": data["measurement_class"],
        "value_status": data["value_status"],
        "temperature_series": {
            "specimen_id": series["specimen_id"],
            "composition_x": composition,
            "composition_sigma_conservative": composition_sigma,
            "reference_temperature_K": reference_temperature,
            "row_count": len(rows),
            "model_comparisons": temperature_comparisons,
            "anchored_mae_rank": anchored_rank,
        },
        "composition_series_300K": {
            "row_count": len(composition_rows),
            "model_comparisons": composition_comparisons,
            "absolute_mae_rank": composition_rank,
        },
        "decision": {
            "observed_6_to_300_increment_meV": float(
                1000.0 * (observed[-1] - observed[reference_index])
            ),
            "pade_minus_hansen_anchored_mae_meV": pade_mae - hansen_mae,
            "pade_min_envelope_minus_hansen_max_envelope_meV": pade_min - hansen_max,
            "provisional_pade_preferred_for_chu_turning_point_transfer": False,
            "provisional_pade_cross_source_support_weakened": True,
            "hansen_over_pade_material_law_selection_authorized": False,
            "chu_absolute_ranking_independent": False,
            "strict_cross_method_material_law_ranking_authorized": False,
            "new_universal_gap_refit_authorized": False,
            "reason": (
                "The same-specimen turning-point increments remove most absolute "
                "composition-offset sensitivity and show poorer transfer for the "
                "provisional Pade law than Hansen across the declared composition "
                "interval. The source is nevertheless an absorption turning-point "
                "operator, not an independent magneto-optical latent-gap series; "
                "method offsets and printed-label precision block a universal law "
                "selection."
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
