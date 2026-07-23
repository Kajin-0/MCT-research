from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping

from mct_research.scott_temperature_coefficients import (
    build_reference,
    load_scott_points,
    quantize_for_json,
    source_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/experimental/scott1969_figure2_digitized.csv"
DEFAULT_OUTPUT = (
    ROOT / "data/validation/scott1969_temperature_coefficient_test.json"
)

_METRIC_KEYS = (
    "box_feasible",
    "n_points",
    "rmse_ev",
    "maximum_absolute_residual_ev",
    "maximum_normalized_box_residual",
    "fraction_within_first_order_box",
    "squared_hinge_violation",
)


def _metric_headline(metrics: Mapping[str, object]) -> dict[str, object]:
    return {key: metrics[key] for key in _METRIC_KEYS if key in metrics}


def _stable_model_fields(model: Mapping[str, object]) -> dict[str, object]:
    fields = {key: value for key, value in model.items() if key != "metrics"}
    if "condition_number" in fields:
        fields["condition_number"] = round(float(fields["condition_number"]), 10)
    return fields


def compact_reference(reference: Mapping[str, object]) -> dict[str, object]:
    full = reference["subset_analyses"]["full_9_specimens"]
    independent = full["S0_independent_specimen_slopes"]
    specimen_rows = {
        specimen["specimen_group"]: specimen for specimen in full["specimens"]
    }
    compact: dict[str, object] = {
        "schema_version": reference["schema_version"],
        "program": reference["program"],
        "issue": reference["issue"],
        "source": reference["source"],
        "observation_boundary": reference["observation_boundary"],
        "constants": reference["constants"],
        "decision": reference["decision"],
        "independent_specimen_slopes": {
            label: {
                "composition_x": independent["metrics"]["by_specimen"][label][
                    "composition_x"
                ],
                "quality_flag": specimen_rows[label]["quality_flag"],
                "slope_ev_per_k": slope,
                "maximum_normalized_box_residual": independent["metrics"][
                    "by_specimen"
                ][label]["maximum_normalized_box_residual"],
            }
            for label, slope in independent["slopes_ev_per_k"].items()
        },
        "subset_analyses": {},
        "leave_one_specimen_out": {},
        "linearized_box_sensitivity": reference[
            "linearized_box_sensitivity"
        ],
    }

    for name, analysis in reference["subset_analyses"].items():
        s0 = analysis["S0_independent_specimen_slopes"]
        s1 = analysis["S1_shared_linear_composition_slope"]
        sh = analysis["SH_hansen_fixed_slope"]
        subset: dict[str, object] = {
            "n_points": analysis["n_points"],
            "n_specimens": analysis["n_specimens"],
            "compositions_x": [
                specimen["composition_x"] for specimen in analysis["specimens"]
            ],
            "S0_metrics": _metric_headline(s0["metrics"]),
            "S1": {
                **_stable_model_fields(s1),
                "metrics": _metric_headline(s1["metrics"]),
            },
            "SH": {
                **_stable_model_fields(sh),
                "metrics": _metric_headline(sh["metrics"]),
            },
            "hansen_longest_same_sign_run": analysis[
                "hansen_slope_delta_pattern"
            ]["longest_same_sign_run"],
            "hansen_monotone_residual_sign_pattern": analysis[
                "hansen_slope_delta_pattern"
            ]["monotone_residual_sign_pattern"],
        }
        if name == "core_unflagged_within_range":
            subset["core_by_specimen"] = {
                model: {
                    label: {
                        "composition_x": metrics["composition_x"],
                        "slope_ev_per_k": metrics["slope_ev_per_k"],
                        "maximum_normalized_box_residual": metrics[
                            "maximum_normalized_box_residual"
                        ],
                        "fraction_within_first_order_box": metrics[
                            "fraction_within_first_order_box"
                        ],
                        "rmse_ev": metrics["rmse_ev"],
                    }
                    for label, metrics in model_record["metrics"][
                        "by_specimen"
                    ].items()
                }
                for model, model_record in (("S1", s1), ("SH", sh))
            }
        compact["subset_analyses"][name] = subset

    for subset_name, models in reference["leave_one_specimen_out"].items():
        compact_models: dict[str, object] = {}
        for model, result in models.items():
            record: dict[str, object] = {
                "all_held_out_specimens_box_feasible": result[
                    "all_held_out_specimens_box_feasible"
                ],
                "maximum_held_out_normalized_box_residual": result[
                    "maximum_held_out_normalized_box_residual"
                ],
            }
            if subset_name == "core_unflagged_within_range":
                record["by_held_out_specimen"] = {
                    label: {
                        "composition_x": held_out["composition_x"],
                        "predicted_slope_ev_per_k": held_out[
                            "predicted_slope_ev_per_k"
                        ],
                        "maximum_normalized_box_residual": held_out[
                            "metrics"
                        ]["maximum_normalized_box_residual"],
                        "box_feasible": held_out["metrics"]["box_feasible"],
                    }
                    for label, held_out in result[
                        "by_held_out_specimen"
                    ].items()
                }
            compact_models[model] = record
        compact["leave_one_specimen_out"][subset_name] = compact_models

    return compact


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build the deterministic Scott 1969 fixed-alpha temperature-"
            "coefficient reference."
        )
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    points = load_scott_points(args.source)
    full_reference = build_reference(
        points,
        source_csv_sha256=source_sha256(args.source),
    )
    quantized = quantize_for_json(compact_reference(full_reference))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(quantized, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
