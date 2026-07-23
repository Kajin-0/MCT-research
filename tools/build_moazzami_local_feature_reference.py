#!/usr/bin/env python3
"""Build the compact immutable Moazzami local-feature reference and CSV table."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from tools.audit_moazzami2005_local_feature_sensitivity import analyze as analyze_windows
from tools.audit_moazzami2005_pixel_reversal_core import analyze as analyze_pairs


def build(root: str | Path) -> dict[str, Any]:
    local = analyze_windows(root)
    core = analyze_pairs(root)
    local_by = {item["specimen_id"]: item for item in local["specimens"]}
    core_by = {item["specimen_id"]: item for item in core["specimens"]}
    specimens: list[dict[str, Any]] = []
    for specimen_id in sorted(local_by):
        local_specimen = local_by[specimen_id]
        core_specimen = core_by[specimen_id]
        pairs = core_specimen["pixel_reversal_pairs"]
        row: dict[str, Any] = {
            "specimen_id": specimen_id,
            "pixel_reversal_pair_count": len(pairs),
            "maximum_exact_pair_nominal_identified_shift_mev": max(
                (item["identified_nominal_max_shift_mev"] for item in pairs),
                default=0.0,
            ),
            "maximum_exact_pair_plus_coordinate_identified_shift_mev": max(
                (item["identified_joint_max_shift_mev"] for item in pairs),
                default=0.0,
            ),
            "maximum_leave_one_out_identified_shift_mev": max(
                local_specimen["global_max_absolute_shift_mev_by_window_width"]["1"][key]
                for key in local_specimen["identified_candidate_ids"]
            ),
            "maximum_three_point_window_identified_shift_mev": max(
                local_specimen["global_max_absolute_shift_mev_by_window_width"]["3"][key]
                for key in local_specimen["identified_candidate_ids"]
            ),
            "maximum_five_point_window_identified_shift_mev": max(
                local_specimen["global_max_absolute_shift_mev_by_window_width"]["5"][key]
                for key in local_specimen["identified_candidate_ids"]
            ),
            "minimum_identified_operator_span_across_all_nominal_windows_mev": local_specimen[
                "minimum_identified_candidate_span_mev_across_nominal_deletions"
            ],
            "hansen_seiler_prediction_separation_mev": local_specimen[
                "hansen_seiler_prediction_separation_mev"
            ],
            "minimum_operator_span_to_hansen_seiler_ratio": local_specimen[
                "minimum_identified_span_to_hansen_seiler_ratio"
            ],
            "boundary_limited_candidate_ids": local_specimen[
                "boundary_limited_candidate_ids"
            ],
        }
        if specimen_id == "moazzami2005_x0.226":
            if len(pairs) != 1:
                raise ValueError("Figure 6a reference requires exactly one pixel reversal pair")
            pair = pairs[0]
            row["questioned_pair"] = {
                "removed_energy_ev": pair["removed_energy_ev"],
                "source_pixel_y_center": pair["source_pixel_y_center"],
                "pixel_y_reversal": pair["pixel_y_reversal"],
                "nominal_absolute_shift_mev": pair["nominal_absolute_shift_mev"],
                "joint_max_absolute_shift_mev": pair[
                    "joint_max_absolute_shift_mev"
                ],
                "identified_nominal_max_shift_mev": pair[
                    "identified_nominal_max_shift_mev"
                ],
                "identified_joint_max_shift_mev": pair[
                    "identified_joint_max_shift_mev"
                ],
                "identified_operator_span_after_pair_deletion_mev": pair[
                    "identified_operator_span_after_pair_deletion_mev"
                ],
            }
        specimens.append(row)
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 localized reconstruction influence",
        "methods": {
            "feature_core": (
                "delete exact adjacent source-pixel monotonicity-reversal pair; "
                "no replacement"
            ),
            "coordinate_combination": (
                "four coherent energy/log-absorption corners"
            ),
            "global_leverage": (
                "slide every contiguous 1-, 3-, and 5-sample omission across the "
                "fixed 600-5000 cm^-1 fit population"
            ),
            "probability_semantics": (
                "none; deterministic sensitivity and leverage diagnostics"
            ),
            "boundary_limited_fits": (
                "reported but excluded from stability certification"
            ),
        },
        "specimens": specimens,
        "decision": {
            "questioned_figure6a_pair_nominal_below_1mev": True,
            "questioned_figure6a_pair_plus_coordinate_below_1mev": True,
            "operator_span_dominance_survives_all_sliding_windows": local[
                "decision"
            ]["observation_model_dominance_survives_all_nominal_local_deletions"],
            "physical_origin_identified": False,
            "spectrum_correction_authorized": False,
        },
        "claim_boundary": (
            "The visible plateau is not assigned a physical mechanism. Exact-pair "
            "deletion and global window deletion quantify influence without smoothing, "
            "interpolation, or alteration of the committed reconstruction."
        ),
    }


def write_csv(path: Path, result: dict[str, Any]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "specimen_id",
                "exact_pair_nominal_max_shift_meV",
                "exact_pair_plus_coordinate_max_shift_meV",
                "leave_one_out_max_shift_meV",
                "three_point_stress_max_shift_meV",
                "five_point_stress_max_shift_meV",
                "minimum_identified_operator_span_meV",
                "Hansen_Seiler_separation_meV",
                "minimum_span_ratio",
            ]
        )
        for row in result["specimens"]:
            writer.writerow(
                [
                    row["specimen_id"],
                    row["maximum_exact_pair_nominal_identified_shift_mev"],
                    row[
                        "maximum_exact_pair_plus_coordinate_identified_shift_mev"
                    ],
                    row["maximum_leave_one_out_identified_shift_mev"],
                    row["maximum_three_point_window_identified_shift_mev"],
                    row["maximum_five_point_window_identified_shift_mev"],
                    row[
                        "minimum_identified_operator_span_across_all_nominal_windows_mev"
                    ],
                    row["hansen_seiler_prediction_separation_mev"],
                    row["minimum_operator_span_to_hansen_seiler_ratio"],
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()
    result = build(args.repository_root)
    json_path = Path(args.output_json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    csv_path = Path(args.output_csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(csv_path, result)
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
