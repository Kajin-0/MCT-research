#!/usr/bin/env python3
"""Audit exact two-coordinate source-pixel reversal cores in Moazzami spectra.

A raw source-pixel monotonicity reversal is defined before fitting from two
adjacent digitized coordinates whose source-image y center increases with
photon energy.  The exact two-coordinate pair is removed without interpolation,
smoothing, or replacement.  The deletion is then combined with the four
coherent coordinate perturbation corners already used by the manuscript.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np

from tools.analyze_moazzami2005_real_spectra import build_contract
from tools.audit_moazzami2005_local_feature_sensitivity import (
    BOUNDARY_TOLERANCE_EV,
    STABILITY_GATE_MEV,
    _fit_model_edges,
    _load_points,
)


def audit_specimen(csv_path: str | Path, calibration_path: str | Path) -> dict[str, Any]:
    points = _load_points(csv_path)
    contract, _ = build_contract(csv_path, calibration_path)
    low, high = (
        float(value)
        for value in contract["analysis_assumptions"]["fit_absorption_window_cm1"]
    )
    base_mask = (points["absorption"] >= low) & (points["absorption"] <= high)
    fit_indices = np.flatnonzero(base_mask)
    base_edges = _fit_model_edges(points, contract, base_mask)
    upper_bound = float(contract["analysis_assumptions"]["edge_search_bounds_ev"][1])
    boundary_ids = sorted(
        key
        for key, value in base_edges.items()
        if abs(value - upper_bound) <= BOUNDARY_TOLERANCE_EV
    )
    identified_ids = sorted(set(base_edges) - set(boundary_ids))

    pairs: list[dict[str, Any]] = []
    for left, right in zip(fit_indices[:-1], fit_indices[1:], strict=True):
        if int(right) != int(left) + 1:
            continue
        delta_y = float(
            points["source_pixel_y_center"][right]
            - points["source_pixel_y_center"][left]
        )
        if delta_y <= 0.0:
            continue
        removed = np.asarray([int(left), int(right)], dtype=int)
        keep = base_mask.copy()
        keep[removed] = False
        nominal_edges = _fit_model_edges(points, contract, keep)
        nominal_shifts = {
            key: 1000.0 * abs(nominal_edges[key] - base_edges[key])
            for key in base_edges
        }
        corner_rows = []
        joint_max = {key: nominal_shifts[key] for key in base_edges}
        for energy_sign, absorption_sign in itertools.product((-1, 1), repeat=2):
            edges = _fit_model_edges(
                points,
                contract,
                keep,
                energy_sign=energy_sign,
                absorption_sign=absorption_sign,
            )
            shifts = {
                key: 1000.0 * abs(edges[key] - base_edges[key]) for key in base_edges
            }
            for key in joint_max:
                joint_max[key] = max(joint_max[key], shifts[key])
            corner_rows.append(
                {
                    "energy_sign": energy_sign,
                    "absorption_sign": absorption_sign,
                    "edge_ev": edges,
                    "absolute_shift_from_nominal_base_mev": shifts,
                }
            )
        identified_nominal_max = max(nominal_shifts[key] for key in identified_ids)
        identified_joint_max = max(joint_max[key] for key in identified_ids)
        identified_span = 1000.0 * (
            max(nominal_edges[key] for key in identified_ids)
            - min(nominal_edges[key] for key in identified_ids)
        )
        pairs.append(
            {
                "removed_indices": [int(left), int(right)],
                "removed_energy_ev": [
                    float(points["energy"][left]),
                    float(points["energy"][right]),
                ],
                "source_pixel_y_center": [
                    float(points["source_pixel_y_center"][left]),
                    float(points["source_pixel_y_center"][right]),
                ],
                "pixel_y_reversal": delta_y,
                "nominal_edge_ev": nominal_edges,
                "nominal_absolute_shift_mev": nominal_shifts,
                "joint_max_absolute_shift_mev": joint_max,
                "identified_nominal_max_shift_mev": identified_nominal_max,
                "identified_joint_max_shift_mev": identified_joint_max,
                "identified_operator_span_after_pair_deletion_mev": identified_span,
                "coordinate_corners": corner_rows,
                "decision": {
                    "nominal_pair_deletion_below_1mev": (
                        identified_nominal_max < STABILITY_GATE_MEV
                    ),
                    "pair_deletion_plus_coordinate_corners_below_1mev": (
                        identified_joint_max < STABILITY_GATE_MEV
                    ),
                    "physical_origin_identified": False,
                    "spectrum_correction_authorized": False,
                },
            }
        )

    return {
        "specimen_id": contract["specimen_id"],
        "base_edge_ev": base_edges,
        "boundary_limited_candidate_ids": boundary_ids,
        "identified_candidate_ids": identified_ids,
        "pair_count": len(pairs),
        "pixel_reversal_pairs": pairs,
        "decision": {
            "all_nominal_pair_deletions_below_1mev": all(
                row["decision"]["nominal_pair_deletion_below_1mev"] for row in pairs
            ),
            "all_pair_deletion_plus_coordinate_corners_below_1mev": all(
                row["decision"]["pair_deletion_plus_coordinate_corners_below_1mev"]
                for row in pairs
            ),
            "points_smoothed_replaced_or_interpolated": False,
            "physical_origin_identified": False,
            "spectrum_correction_authorized": False,
        },
        "claim_boundary": (
            "The exact source-pixel reversal pair is an objectively defined influence "
            "case. Deleting it does not identify its physical origin and does not "
            "authorize alteration of the committed reconstructed spectrum."
        ),
    }


def analyze(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    stems = [
        "moazzami2005_figure6a_irse",
        "moazzami2005_figure6b_irse",
    ]
    specimens = [
        audit_specimen(
            root / "data/manuscript" / f"{stem}_digitized.csv",
            root / "data/manuscript" / f"{stem}_calibration.json",
        )
        for stem in stems
    ]
    return {
        "schema_version": "1.0",
        "analysis": "exact two-coordinate source-pixel reversal core audit",
        "method": {
            "feature_definition": (
                "adjacent fit-population coordinates with increasing source-image "
                "pixel-y center as photon energy increases"
            ),
            "deletion": "exact two-coordinate pair",
            "coordinate_perturbations": "four coherent corners",
            "smoothing_interpolation_or_replacement": "forbidden",
            "probability_semantics": "none; deterministic influence audit",
        },
        "specimens": specimens,
        "decision": {
            "all_nominal_pair_deletions_below_1mev": all(
                item["decision"]["all_nominal_pair_deletions_below_1mev"]
                for item in specimens
            ),
            "all_pair_deletion_plus_coordinate_corners_below_1mev": all(
                item["decision"][
                    "all_pair_deletion_plus_coordinate_corners_below_1mev"
                ]
                for item in specimens
            ),
            "physical_origin_identified": False,
            "spectrum_correction_authorized": False,
        },
        "claim_boundary": (
            "This result quantifies the influence of objectively defined source-pixel "
            "reversal cores. It is not evidence of a microscopic absorption feature "
            "or a corrected spectrum."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.repository_root)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
