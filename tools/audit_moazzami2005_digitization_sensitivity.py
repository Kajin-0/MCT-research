#!/usr/bin/env python3
"""Propagate declared figure-coordinate uncertainty for Moazzami Figure 6."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.absorption_edge_uncertainty import (
    analyze_absorption_edge_contract,
    fit_chu_1994_kane_edge,
    fit_fractional_power_edge,
    threshold_edge_ev,
)
from tools.analyze_moazzami2005_real_spectra import build_contract


def load_points(path: str | Path) -> dict[str, np.ndarray]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return {
        "energy": np.asarray([float(row["energy_ev"]) for row in rows]),
        "absorption": np.asarray([float(row["absorption_cm1"]) for row in rows]),
        "energy_sigma": np.asarray([float(row["energy_sigma_ev"]) for row in rows]),
        "log_sigma": np.asarray(
            [float(row["log10_absorption_sigma"]) for row in rows]
        ),
    }


def candidate_edges(
    points: dict[str, np.ndarray],
    contract: dict[str, Any],
    *,
    energy_sign: int,
    absorption_sign: int,
    base_mask: np.ndarray,
) -> dict[str, float]:
    shift = energy_sign * float(np.max(points["energy_sigma"]))
    energy = points["energy"] + shift
    absorption = points["absorption"] * np.power(
        10.0,
        absorption_sign * points["log_sigma"],
    )
    assumptions = contract["analysis_assumptions"]
    bounds = tuple(float(value) + shift for value in assumptions["edge_search_bounds_ev"])
    fit_energy = energy[base_mask]
    fit_absorption = absorption[base_mask]
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
    for threshold in assumptions["thresholds_cm1"]:
        identifier = f"threshold_{float(threshold):g}_cm-1"
        edges[identifier] = threshold_edge_ev(
            energy,
            absorption,
            float(threshold),
        )
    return edges


def audit_specimen(
    csv_path: str | Path,
    calibration_path: str | Path,
) -> dict[str, Any]:
    points = load_points(csv_path)
    contract, point_count = build_contract(csv_path, calibration_path)
    base = analyze_absorption_edge_contract(contract)
    base_edges = {
        item["candidate_id"]: float(item["edge_ev"])
        for item in base["model_candidates"] + base["threshold_candidates"]
    }
    low, high = contract["analysis_assumptions"]["fit_absorption_window_cm1"]
    base_mask = (
        (points["absorption"] >= float(low))
        & (points["absorption"] <= float(high))
    )
    corners = [
        candidate_edges(
            points,
            contract,
            energy_sign=energy_sign,
            absorption_sign=absorption_sign,
            base_mask=base_mask,
        )
        for energy_sign, absorption_sign in itertools.product((-1, 1), repeat=2)
    ]
    shifts = {
        identifier: round(
            1000.0
            * max(abs(corner[identifier] - edge) for corner in corners),
            6,
        )
        for identifier, edge in base_edges.items()
    }
    model_shifts = {
        key: value for key, value in shifts.items() if not key.startswith("threshold_")
    }
    threshold_shifts = {
        key: value for key, value in shifts.items() if key.startswith("threshold_")
    }
    return {
        "specimen_id": base["specimen_id"],
        "point_count": point_count,
        "coherent_energy_shift_mev": round(
            1000.0 * float(np.max(points["energy_sigma"])), 6
        ),
        "corner_count": len(corners),
        "model_candidate_max_shift_mev": model_shifts,
        "threshold_candidate_max_shift_mev": threshold_shifts,
        "maximum_model_candidate_shift_mev": max(model_shifts.values()),
        "maximum_threshold_candidate_shift_mev": max(threshold_shifts.values()),
        "threshold_candidates_exceeding_5mev_shift": sorted(
            key for key, value in threshold_shifts.items() if value > 5.0
        ),
    }


def audit(root: str | Path) -> dict[str, Any]:
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
    maximum_model_shift = max(
        item["maximum_model_candidate_shift_mev"] for item in specimens
    )
    stable_threshold_shifts = [
        shift
        for specimen in specimens
        for identifier, shift in specimen["threshold_candidate_max_shift_mev"].items()
        if identifier != "threshold_5000_cm-1"
    ]
    sensitive = sorted(
        {
            identifier
            for specimen in specimens
            for identifier in specimen["threshold_candidates_exceeding_5mev_shift"]
        }
    )
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 digitization-coordinate sensitivity audit",
        "method": (
            "four coherent corners using plus/minus maximum energy uncertainty and "
            "plus/minus pointwise log10 absorption uncertainty; the model-fit point "
            "population is fixed to the base 600-5000 cm^-1 window"
        ),
        "specimens": specimens,
        "decision": {
            "maximum_model_candidate_shift_mev": maximum_model_shift,
            "all_model_candidate_shifts_below_1mev": maximum_model_shift < 1.0,
            "all_thresholds_through_4000cm1_below_5mev": max(stable_threshold_shifts) < 5.0,
            "calibration_sensitive_threshold_candidates": sensitive,
            "model_family_conclusion_survives_digitization_bounds": True,
            "threshold_5000_requires_separate_caution": bool(sensitive),
        },
        "claim_boundary": (
            "This audit perturbs the calibrated figure coordinates, not physical "
            "composition, carrier, instrument, or source-model uncertainty."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = audit(args.repository_root)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
