#!/usr/bin/env python3
"""Audit the carrier-coupled near-critical HgCdTe constraint from Orlita 2014."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable

import numpy as np

from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import chu_1983_gap_ev


def load_constraint(path: str | Path) -> dict[str, Any]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 1:
        raise ValueError("expected one Orlita constraint record")
    row = rows[0]
    return {
        "sample": row["sample"],
        "temperature_k": float(row["temperature_k"]),
        "composition_nominal": float(row["composition_nominal"]),
        "composition_precision_status": row["composition_precision_status"],
        "gap_ev": float(row["gap_ev"]),
        "gap_status": row["gap_status"],
        "fermi_energy_mev": [
            float(row["fermi_energy_mev_low"]),
            float(row["fermi_energy_mev_high"]),
        ],
        "carrier_density_cm3": [
            float(row["carrier_density_cm3_low"]),
            float(row["carrier_density_cm3_high"]),
        ],
        "composition_profile_thickness_um": float(
            row["composition_profile_thickness_um"]
        ),
        "composition_method": row["composition_method"],
        "source_doi": row["source_doi"],
    }


def composition_for_gap(
    model: Callable[[float, float], float],
    temperature_k: float,
    target_gap_ev: float,
    *,
    lower: float = 0.14,
    upper: float = 0.20,
) -> float:
    left = float(lower)
    right = float(upper)
    f_left = float(model(left, temperature_k)) - target_gap_ev
    f_right = float(model(right, temperature_k)) - target_gap_ev
    if np.signbit(f_left) == np.signbit(f_right):
        raise ValueError("target gap is not bracketed")
    for _ in range(256):
        midpoint = 0.5 * (left + right)
        value = float(model(midpoint, temperature_k)) - target_gap_ev
        if abs(value) < 1e-14 or right - left < 1e-13:
            return midpoint
        if np.signbit(value) == np.signbit(f_left):
            left = midpoint
            f_left = value
        else:
            right = midpoint
    raise RuntimeError("composition root did not converge")


def analyze(path: str | Path) -> dict[str, Any]:
    record = load_constraint(path)
    temperature = record["temperature_k"]
    nominal_x = record["composition_nominal"]
    target_gap = record["gap_ev"]
    models: dict[str, Callable[[float, float], float]] = {
        "hansen": hansen_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
        "laurenti": laurenti_gap_ev,
        "chu_1983": chu_1983_gap_ev,
    }

    nominal: dict[str, Any] = {}
    inferred: dict[str, Any] = {}
    for name, model in models.items():
        predicted = float(model(nominal_x, temperature))
        residual_mev = 1000.0 * (target_gap - predicted)
        nominal[name] = {
            "predicted_gap_mev": 1000.0 * predicted,
            "observed_minus_predicted_mev": residual_mev,
            "absolute_residual_mev": abs(residual_mev),
        }
        required_x = composition_for_gap(model, temperature, target_gap)
        inferred[name] = {
            "composition_for_4mev_gap": required_x,
            "offset_from_nominal_x": required_x - nominal_x,
        }

    nominal_winner = min(
        nominal, key=lambda name: nominal[name]["absolute_residual_mev"]
    )
    return {
        "source_record": record,
        "nominal_composition_model_screen": nominal,
        "composition_required_for_reported_gap": inferred,
        "nominal_winner": nominal_winner,
        "decision": {
            "primary_constraint_admitted": True,
            "exact_homogeneous_composition_gap_point": False,
            "carrier_state_is_part_of_observation_operator": True,
            "near_critical_source_family_leading_comparator": nominal_winner,
            "global_model_promotion_authorized": False,
            "coefficient_refit_authorized": False,
            "next_required_evidence": (
                "independent homogeneous composition metrology and a gap extraction "
                "that propagates carrier-density uncertainty"
            ),
        },
        "claim_boundary": (
            "The source reports a graded x approximately 0.17 plateau, a 4 meV "
            "gap that improves low-field modeling, and an optically inferred carrier "
            "state. It constrains the near-critical source family but is not an exact "
            "composition-gap calibration point."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.input_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
