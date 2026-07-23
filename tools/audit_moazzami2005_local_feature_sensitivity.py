#!/usr/bin/env python3
"""Audit localized reconstruction influence in the Moazzami 2005 spectra.

The audit does not smooth, replace, or reinterpret any measured coordinate.  It
quantifies how fitted edge candidates change when every possible contiguous
one-, three-, and five-sample window is removed from the declared fit
population.  A second, joint audit combines the pre-existing coherent
coordinate perturbations with windows that contain raw source-pixel
monotonicity reversals.  Boundary-limited fits remain reported but are excluded
from stability certification because censoring at a search bound can mimic
robustness.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from mct_research.absorption_edge_uncertainty import (
    fit_chu_1994_kane_edge,
    fit_fractional_power_edge,
)
from mct_research.gap_models import hansen_gap_ev
from mct_research.historical_gap_models import seiler_1990_gap_ev
from tools.analyze_moazzami2005_real_spectra import build_contract

WINDOW_SIZES = (1, 3, 5)
STABILITY_GATE_MEV = 1.0
BOUNDARY_TOLERANCE_EV = 1.0e-9


def _load_points(path: str | Path) -> dict[str, np.ndarray]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return {
        "energy": np.asarray([float(row["energy_ev"]) for row in rows]),
        "absorption": np.asarray([float(row["absorption_cm1"]) for row in rows]),
        "energy_sigma": np.asarray([float(row["energy_sigma_ev"]) for row in rows]),
        "log_sigma": np.asarray(
            [float(row["log10_absorption_sigma"]) for row in rows]
        ),
        "source_pixel_y_center": np.asarray(
            [float(row["source_pixel_y_center"]) for row in rows]
        ),
    }


def _fit_model_edges(
    points: dict[str, np.ndarray],
    contract: dict[str, Any],
    keep_mask: np.ndarray,
    *,
    energy_sign: int = 0,
    absorption_sign: int = 0,
) -> dict[str, float]:
    if energy_sign not in {-1, 0, 1} or absorption_sign not in {-1, 0, 1}:
        raise ValueError("coordinate signs must be -1, 0, or 1")
    shift = energy_sign * float(np.max(points["energy_sigma"]))
    energy = points["energy"] + shift
    absorption = points["absorption"] * np.power(
        10.0, absorption_sign * points["log_sigma"]
    )
    assumptions = contract["analysis_assumptions"]
    bounds = tuple(float(value) + shift for value in assumptions["edge_search_bounds_ev"])
    fit_energy = energy[keep_mask]
    fit_absorption = absorption[keep_mask]
    if fit_energy.size < 20:
        raise ValueError("robustness fit must retain at least 20 points")

    edges: dict[str, float] = {}
    for exponent in assumptions["fractional_power_exponents"]:
        fixed = None if exponent == "free" else float(exponent)
        identifier = (
            "fractional_power_free"
            if fixed is None
            else f"fractional_power_p_{fixed:g}"
        )
        edges[identifier] = float(
            fit_fractional_power_edge(
                fit_energy,
                fit_absorption,
                edge_bounds_ev=bounds,
                exponent=fixed,
            )["edge_ev"]
        )
    if assumptions.get("include_chu_1994_kane_region", False):
        edges["chu_1994_kane_region"] = float(
            fit_chu_1994_kane_edge(
                fit_energy,
                fit_absorption,
                edge_bounds_ev=bounds,
                composition_x=float(contract["metadata"]["composition_x"]),
                temperature_k=float(contract["metadata"]["temperature_k"]),
            )["edge_ev"]
        )
    return edges


def _rank(edge_ev: float, composition_x: float, temperature_k: float) -> str:
    predictions = {
        "hansen": hansen_gap_ev(composition_x, temperature_k),
        "published_seiler": seiler_1990_gap_ev(composition_x, temperature_k),
    }
    return min(predictions, key=lambda key: abs(edge_ev - predictions[key]))


def _window_indices(fit_indices: np.ndarray, width: int) -> Iterable[np.ndarray]:
    for start in range(0, fit_indices.size - width + 1):
        yield fit_indices[start : start + width]


def _feature_windows(
    fit_indices: np.ndarray,
    violating_pairs: list[tuple[int, int]],
) -> list[np.ndarray]:
    position = {int(index): offset for offset, index in enumerate(fit_indices)}
    windows: set[tuple[int, ...]] = set()
    for left, right in violating_pairs:
        left_position = position[left]
        right_position = position[right]
        windows.add((left,))
        windows.add((right,))
        for width in (3, 5):
            midpoint = (left_position + right_position) // 2
            start = max(0, min(midpoint - width // 2, fit_indices.size - width))
            selected = tuple(int(value) for value in fit_indices[start : start + width])
            if left not in selected or right not in selected:
                raise RuntimeError("feature window failed to contain violating pair")
            windows.add(selected)
    return [np.asarray(values, dtype=int) for values in sorted(windows)]


def _scenario_record(
    points: dict[str, np.ndarray],
    contract: dict[str, Any],
    base_mask: np.ndarray,
    base_edges: dict[str, float],
    removed: np.ndarray,
) -> dict[str, Any]:
    keep = base_mask.copy()
    keep[removed] = False
    edges = _fit_model_edges(points, contract, keep)
    shifts = {
        key: 1000.0 * abs(edges[key] - base_edges[key]) for key in base_edges
    }
    composition = float(contract["metadata"]["composition_x"])
    temperature = float(contract["metadata"]["temperature_k"])
    return {
        "removed_indices": [int(value) for value in removed],
        "removed_energy_ev": [float(points["energy"][value]) for value in removed],
        "retained_point_count": int(np.count_nonzero(keep)),
        "edge_ev": edges,
        "absolute_shift_mev": shifts,
        "nominal_hansen_seiler_winner": {
            key: _rank(value, composition, temperature) for key, value in edges.items()
        },
    }


def audit_specimen(csv_path: str | Path, calibration_path: str | Path) -> dict[str, Any]:
    points = _load_points(csv_path)
    contract, point_count = build_contract(csv_path, calibration_path)
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

    violations: list[dict[str, Any]] = []
    violating_pairs: list[tuple[int, int]] = []
    for left, right in zip(fit_indices[:-1], fit_indices[1:], strict=True):
        if int(right) != int(left) + 1:
            continue
        delta_y = float(
            points["source_pixel_y_center"][right]
            - points["source_pixel_y_center"][left]
        )
        if delta_y > 0.0:
            violating_pairs.append((int(left), int(right)))
            violations.append(
                {
                    "left_index": int(left),
                    "right_index": int(right),
                    "left_energy_ev": float(points["energy"][left]),
                    "right_energy_ev": float(points["energy"][right]),
                    "left_pixel_y_center": float(
                        points["source_pixel_y_center"][left]
                    ),
                    "right_pixel_y_center": float(
                        points["source_pixel_y_center"][right]
                    ),
                    "pixel_y_reversal": delta_y,
                }
            )

    scenarios: list[dict[str, Any]] = []
    global_max_by_width: dict[str, dict[str, float]] = {}
    candidate_ids = sorted(base_edges)
    identified_spans = [
        1000.0
        * (max(base_edges[key] for key in identified_ids) - min(base_edges[key] for key in identified_ids))
    ]
    full_spans = [1000.0 * (max(base_edges.values()) - min(base_edges.values()))]
    all_identified_winners = {
        key: {
            _rank(
                base_edges[key],
                float(contract["metadata"]["composition_x"]),
                float(contract["metadata"]["temperature_k"]),
            )
        }
        for key in identified_ids
    }

    for width in WINDOW_SIZES:
        maxima = {key: 0.0 for key in candidate_ids}
        for removed in _window_indices(fit_indices, width):
            record = _scenario_record(points, contract, base_mask, base_edges, removed)
            record["window_width_samples"] = width
            scenarios.append(record)
            for key in candidate_ids:
                maxima[key] = max(maxima[key], record["absolute_shift_mev"][key])
            full_spans.append(
                1000.0
                * (max(record["edge_ev"].values()) - min(record["edge_ev"].values()))
            )
            identified_spans.append(
                1000.0
                * (
                    max(record["edge_ev"][key] for key in identified_ids)
                    - min(record["edge_ev"][key] for key in identified_ids)
                )
            )
            for key in identified_ids:
                all_identified_winners[key].add(
                    record["nominal_hansen_seiler_winner"][key]
                )
        global_max_by_width[str(width)] = maxima

    feature_records: list[dict[str, Any]] = []
    feature_joint_max = {key: 0.0 for key in candidate_ids}
    corners = list(itertools.product((-1, 1), repeat=2))
    for removed in _feature_windows(fit_indices, violating_pairs):
        keep = base_mask.copy()
        keep[removed] = False
        nominal = _scenario_record(points, contract, base_mask, base_edges, removed)
        corner_rows = []
        for energy_sign, absorption_sign in corners:
            edges = _fit_model_edges(
                points,
                contract,
                keep,
                energy_sign=energy_sign,
                absorption_sign=absorption_sign,
            )
            shifts = {
                key: 1000.0 * abs(edges[key] - base_edges[key]) for key in candidate_ids
            }
            for key in candidate_ids:
                feature_joint_max[key] = max(feature_joint_max[key], shifts[key])
            corner_rows.append(
                {
                    "energy_sign": energy_sign,
                    "absorption_sign": absorption_sign,
                    "edge_ev": edges,
                    "absolute_shift_from_nominal_base_mev": shifts,
                }
            )
        feature_records.append(
            {
                "removed_indices": nominal["removed_indices"],
                "removed_energy_ev": nominal["removed_energy_ev"],
                "window_width_samples": len(removed),
                "nominal_absolute_shift_mev": nominal["absolute_shift_mev"],
                "coordinate_corners": corner_rows,
            }
        )

    global_max = {
        key: max(global_max_by_width[str(width)][key] for width in WINDOW_SIZES)
        for key in candidate_ids
    }
    composition = float(contract["metadata"]["composition_x"])
    temperature = float(contract["metadata"]["temperature_k"])
    hansen_seiler_separation = 1000.0 * abs(
        hansen_gap_ev(composition, temperature)
        - seiler_1990_gap_ev(composition, temperature)
    )
    identified_global_max = max(global_max[key] for key in identified_ids)
    identified_feature_joint_max = max(feature_joint_max[key] for key in identified_ids)
    minimum_identified_span = min(identified_spans)

    return {
        "specimen_id": contract["specimen_id"],
        "source_csv": str(csv_path),
        "digitized_point_count": point_count,
        "fit_point_count": int(fit_indices.size),
        "fit_absorption_window_cm1": [low, high],
        "window_sizes_samples": list(WINDOW_SIZES),
        "base_edge_ev": base_edges,
        "boundary_limited_candidate_ids": boundary_ids,
        "identified_candidate_ids": identified_ids,
        "raw_source_pixel_monotonicity_reversals": violations,
        "all_window_scenarios": scenarios,
        "global_max_absolute_shift_mev_by_window_width": global_max_by_width,
        "global_max_absolute_shift_mev": global_max,
        "feature_joint_coordinate_records": feature_records,
        "feature_joint_max_absolute_shift_mev": feature_joint_max,
        "minimum_full_candidate_span_mev_across_nominal_deletions": min(full_spans),
        "minimum_identified_candidate_span_mev_across_nominal_deletions": minimum_identified_span,
        "maximum_identified_candidate_span_mev_across_nominal_deletions": max(identified_spans),
        "hansen_seiler_prediction_separation_mev": hansen_seiler_separation,
        "minimum_identified_span_to_hansen_seiler_ratio": (
            minimum_identified_span / hansen_seiler_separation
        ),
        "identified_candidate_nominal_winners_across_deletions": {
            key: sorted(values) for key, values in all_identified_winners.items()
        },
        "decision": {
            "points_smoothed_or_replaced": False,
            "interpolation_used": False,
            "physical_origin_of_local_feature_identified": False,
            "all_contiguous_windows_audited": True,
            "coordinate_corners_combined_with_source_pixel_reversal_windows": True,
            "boundary_limited_candidates_used_for_stability_certification": False,
            "maximum_identified_shift_from_any_nominal_local_deletion_mev": identified_global_max,
            "maximum_identified_shift_from_feature_deletion_plus_coordinate_corner_mev": identified_feature_joint_max,
            "nominal_local_deletion_stability_gate_mev": STABILITY_GATE_MEV,
            "nominal_local_deletion_gate_passed": identified_global_max < STABILITY_GATE_MEV,
            "feature_plus_coordinate_gate_passed": (
                identified_feature_joint_max < STABILITY_GATE_MEV
            ),
            "observation_model_span_remains_larger_than_hansen_seiler_separation": (
                minimum_identified_span > hansen_seiler_separation
            ),
        },
        "claim_boundary": (
            "The audit quantifies influence of localized reconstructed coordinates. "
            "It does not determine whether a source-pixel reversal is physical, "
            "instrumental, printed, or digitization-induced, and it does not authorize "
            "smoothing, point replacement, or a corrected spectrum."
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
        "analysis": "systematic localized-coordinate influence audit",
        "method": {
            "primary": (
                "leave every possible contiguous 1-, 3-, and 5-sample window out "
                "of the fixed declared fit population"
            ),
            "secondary": (
                "combine four coherent digitization-coordinate corners with all "
                "windows containing raw source-pixel monotonicity reversals"
            ),
            "point_replacement": "forbidden",
            "smoothing": "forbidden",
            "probability_semantics": "none; deterministic sensitivity envelope",
        },
        "specimens": specimens,
        "decision": {
            "specimen_count": len(specimens),
            "all_nominal_local_deletion_gates_passed": all(
                item["decision"]["nominal_local_deletion_gate_passed"]
                for item in specimens
            ),
            "all_feature_plus_coordinate_gates_passed": all(
                item["decision"]["feature_plus_coordinate_gate_passed"]
                for item in specimens
            ),
            "observation_model_dominance_survives_all_nominal_local_deletions": all(
                item["decision"][
                    "observation_model_span_remains_larger_than_hansen_seiler_separation"
                ]
                for item in specimens
            ),
            "physical_origin_identified": False,
            "spectrum_correction_authorized": False,
        },
        "claim_boundary": (
            "A local visual irregularity is treated as a reconstruction-influence "
            "question. The result is a deterministic robustness audit, not evidence "
            "for a microscopic absorption feature and not a corrected data product."
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
