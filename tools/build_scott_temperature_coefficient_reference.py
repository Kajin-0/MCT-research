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
_SPECIMEN_METRIC_KEYS = (
    "composition_x",
    "slope_ev_per_k",
    "n_points",
    "rmse_ev",
    "maximum_absolute_residual_ev",
    "maximum_normalized_box_residual",
    "fraction_within_first_order_box",
    "squared_hinge_violation",
)


def _metric_headline(metrics: Mapping[str, object]) -> dict[str, object]:
    return {key: metrics[key] for key in _METRIC_KEYS if key in metrics}


def _specimen_metrics(metrics: Mapping[str, object]) -> dict[str, object]:
    return {
        label: {
            key: specimen[key]
            for key in _SPECIMEN_METRIC_KEYS
            if key in specimen
        }
        for label, specimen in metrics["by_specimen"].items()
    }


def _compact_subset(name: str, analysis: Mapping[str, object]) -> dict[str, object]:
    s0 = analysis["S0_independent_specimen_slopes"]
    s1 = analysis["S1_shared_linear_composition_slope"]
    sh = analysis["SH_hansen_fixed_slope"]
    compact: dict[str, object] = {
        "n_points": analysis["n_points"],
        "n_specimens": analysis["n_specimens"],
        "compositions_x": [
            specimen["composition_x"] for specimen in analysis["specimens"]
        ],
        "S0_independent_specimen_slopes": {
            "metrics": _metric_headline(s0["metrics"]),
        },
        "S1_shared_linear_composition_slope": {
            **{key: value for key, value in s1.items() if key != "metrics"},
            "metrics": _metric_headline(s1["metrics"]),
        },
        "SH_hansen_fixed_slope": {
            **{key: value for key, value in sh.items() if key != "metrics"},
            "metrics": _metric_headline(sh["metrics"]),
        },
        "hansen_slope_delta_pattern": {
            "longest_same_sign_run": analysis["hansen_slope_delta_pattern"][
                "longest_same_sign_run"
            ],
            "monotone_residual_sign_pattern": analysis[
                "hansen_slope_delta_pattern"
            ]["monotone_residual_sign_pattern"],
        },
    }
    if name == "core_unflagged_within_range":
        compact["S0_independent_specimen_slopes"]["by_specimen"] = (
            _specimen_metrics(s0["metrics"])
        )
        compact["S1_shared_linear_composition_slope"]["by_specimen"] = (
            _specimen_metrics(s1["metrics"])
        )
        compact["SH_hansen_fixed_slope"]["by_specimen"] = (
            _specimen_metrics(sh["metrics"])
        )
    return compact


def _compact_lopo(result: Mapping[str, object]) -> dict[str, object]:
    return {
        "model": result["model"],
        "all_held_out_specimens_box_feasible": result[
            "all_held_out_specimens_box_feasible"
        ],
        "maximum_held_out_normalized_box_residual": result[
            "maximum_held_out_normalized_box_residual"
        ],
        "by_held_out_specimen": {
            label: {
                "composition_x": held_out["composition_x"],
                "training_b0_ev_per_k": held_out["training_b0_ev_per_k"],
                "training_b1_ev_per_k_per_x": held_out[
                    "training_b1_ev_per_k_per_x"
                ],
                "predicted_slope_ev_per_k": held_out[
                    "predicted_slope_ev_per_k"
                ],
                "metrics": _metric_headline(held_out["metrics"]),
            }
            for label, held_out in result["by_held_out_specimen"].items()
        },
    }


def compact_reference(reference: Mapping[str, object]) -> dict[str, object]:
    full = reference["subset_analyses"]["full_9_specimens"]
    independent = full["S0_independent_specimen_slopes"]
    specimen_rows = {
        specimen["specimen_group"]: specimen for specimen in full["specimens"]
    }
    return {
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
                "metrics": _metric_headline(
                    independent["metrics"]["by_specimen"][label]
                ),
            }
            for label, slope in independent["slopes_ev_per_k"].items()
        },
        "subset_analyses": {
            name: _compact_subset(name, analysis)
            for name, analysis in reference["subset_analyses"].items()
        },
        "leave_one_specimen_out": {
            subset: {
                model: _compact_lopo(result)
                for model, result in model_results.items()
            }
            for subset, model_results in reference[
                "leave_one_specimen_out"
            ].items()
        },
        "linearized_box_sensitivity": reference[
            "linearized_box_sensitivity"
        ],
    }


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
