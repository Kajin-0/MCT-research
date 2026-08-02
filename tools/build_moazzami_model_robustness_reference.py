"""Build compact immutable records for the Moazzami model-robustness audit."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from tools.run_moazzami2005_model_robustness import build as build_detailed


def _compatible_candidate_ids(specimen: dict[str, Any]) -> list[str]:
    return [
        item["candidate_id"]
        for item in specimen["nominal_model_adequacy_diagnostics"]
        if not item["boundary_limited"]
        and item["normalized_rms_using_vertical_line_halfwidth"] <= 1.0
        and item["fraction_within_two_vertical_halfwidths"] >= 0.95
    ]


def _maximum_all_reconstruction_shift_mev(specimen: dict[str, Any]) -> float:
    nominal = {
        item["candidate_id"]: float(item["edge_ev"])
        for item in specimen["nominal_candidates"]
    }
    return float(
        max(
            1000.0 * abs(float(edge) - nominal[candidate_id])
            for record in specimen["reconstruction_sensitivity"]
            for candidate_id, edge in record["model_edges_ev"].items()
        )
    )


def build(root: Path) -> dict[str, Any]:
    detailed = build_detailed(root)
    specimens: list[dict[str, Any]] = []
    for specimen in detailed["specimens"]:
        nominal_edges = {
            item["candidate_id"]: float(item["edge_ev"])
            for item in specimen["nominal_candidates"]
        }
        compatible = _compatible_candidate_ids(specimen)
        compatible_edges = [nominal_edges[candidate_id] for candidate_id in compatible]
        grid_spans = [
            float(item["nonboundary_model_span_mev"])
            for item in specimen["fit_domain_and_weighting_sensitivity"]
        ]
        specimens.append(
            {
                "specimen_id": specimen["specimen_id"],
                "nominal_fit_point_count": specimen["nominal_fit_point_count"],
                "nominal_model_edges_ev": nominal_edges,
                "boundary_limited_candidate_ids": [
                    item["candidate_id"]
                    for item in specimen["nominal_candidates"]
                    if item["boundary_limited"]
                ],
                "maximum_fixed_membership_reconstruction_shift_mev": float(
                    max(
                        specimen[
                            "maximum_reconstruction_shift_mev_by_candidate"
                        ].values()
                    )
                ),
                "maximum_all_admissible_reconstruction_shift_mev": (
                    _maximum_all_reconstruction_shift_mev(specimen)
                ),
                "maximum_fit_domain_or_weighting_shift_mev": float(
                    max(
                        specimen[
                            "maximum_fit_domain_or_weighting_shift_mev_by_candidate"
                        ].values()
                    )
                ),
                "minimum_nonboundary_span_across_grid_mev": float(min(grid_spans)),
                "maximum_nonboundary_span_across_grid_mev": float(max(grid_spans)),
                "admissible_fit_domain_weighting_record_count": len(
                    specimen["fit_domain_and_weighting_sensitivity"]
                ),
                "excluded_reconstruction_scenario_count": len(
                    specimen["excluded_reconstruction_scenarios"]
                ),
                "excluded_fit_domain_scenario_count": len(
                    specimen["excluded_fit_domain_scenarios"]
                ),
                "line_envelope_compatibility_rule": {
                    "boundary_limited": False,
                    "maximum_normalized_rms": 1.0,
                    "minimum_fraction_within_two_halfwidths": 0.95,
                    "semantics": (
                        "deterministic descriptive screen; not likelihood, confidence "
                        "level, physical model selection, or experimental uncertainty"
                    ),
                },
                "line_envelope_compatible_candidate_ids": compatible,
                "line_envelope_compatible_nominal_span_mev": float(
                    1000.0 * np.ptp(np.asarray(compatible_edges, dtype=float))
                ),
                "nominal_model_adequacy_diagnostics": specimen[
                    "nominal_model_adequacy_diagnostics"
                ],
            }
        )
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 compact fitted-model robustness reference",
        "methods": detailed["methods"],
        "specimens": specimens,
        "decision": {
            "fixed_absorption_coordinates_excluded_from_fitted_model_span": True,
            "fit_domain_and_weighting_are_material_sensitivity_axes": True,
            "line_envelope_screen_is_secondary_and_nonprobabilistic": True,
            "unique_physical_gap_identified": False,
            "universal_hgcdte_claim_authorized": False,
        },
        "claim_boundary": detailed["claim_boundary"],
    }


def write_csv(path: Path, result: dict[str, Any]) -> None:
    fields = [
        "specimen_id",
        "nominal_fit_point_count",
        "maximum_fixed_membership_reconstruction_shift_mev",
        "maximum_all_admissible_reconstruction_shift_mev",
        "maximum_fit_domain_or_weighting_shift_mev",
        "minimum_nonboundary_span_across_grid_mev",
        "maximum_nonboundary_span_across_grid_mev",
        "line_envelope_compatible_nominal_span_mev",
        "line_envelope_compatible_candidate_ids",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for specimen in result["specimens"]:
            row = {key: specimen[key] for key in fields}
            row["line_envelope_compatible_candidate_ids"] = ";".join(
                specimen["line_envelope_compatible_candidate_ids"]
            )
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    arguments = parser.parse_args()
    result = build(arguments.repository_root.resolve())
    arguments.output_json.parent.mkdir(parents=True, exist_ok=True)
    arguments.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(arguments.output_csv, result)


if __name__ == "__main__":
    main()
