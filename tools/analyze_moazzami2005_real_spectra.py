#!/usr/bin/env python3
"""Analyze the two digitized Moazzami 2005 Figure 6 IRSE spectra."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable

from mct_research.absorption_edge_uncertainty import analyze_absorption_edge_contract
from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_csv_matches_contract(csv_path: str | Path, contract: dict[str, Any]) -> int:
    with Path(csv_path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    energies = contract["spectrum"]["energy_ev"]
    absorptions = contract["spectrum"]["absorption_cm1"]
    if len(rows) != len(energies) or len(rows) != len(absorptions):
        raise ValueError("digitized CSV and contract spectrum lengths differ")
    previous = None
    for row, energy, absorption in zip(rows, energies, absorptions, strict=True):
        csv_energy = float(row["energy_ev"])
        csv_absorption = float(row["absorption_cm1"])
        if abs(csv_energy - float(energy)) > 5e-10:
            raise ValueError("digitized CSV energy differs from contract")
        if abs(csv_absorption - float(absorption)) > 5e-5:
            raise ValueError("digitized CSV absorption differs from contract")
        if previous is not None and csv_energy <= previous:
            raise ValueError("digitized energy must be strictly increasing")
        previous = csv_energy
        if float(row["energy_sigma_ev"]) > 0.005:
            raise ValueError("digitization energy uncertainty exceeds 5 meV stop rule")
    return len(rows)


def candidate_rankings(result: dict[str, Any], composition_x: float, temperature_k: float) -> tuple[dict[str, float], list[dict[str, Any]]]:
    models: dict[str, Callable[[float, float], float]] = {
        "hansen": hansen_gap_ev,
        "laurenti": laurenti_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    }
    predictions_mev = {
        name: 1000.0 * float(model(composition_x, temperature_k))
        for name, model in models.items()
    }
    rankings: list[dict[str, Any]] = []
    candidates = result["model_candidates"] + result["threshold_candidates"]
    for candidate in candidates:
        edge_mev = 1000.0 * float(candidate["edge_ev"])
        residuals = {
            name: abs(edge_mev - prediction)
            for name, prediction in predictions_mev.items()
        }
        rankings.append(
            {
                "candidate_id": candidate["candidate_id"],
                "edge_mev": edge_mev,
                "winner": min(residuals, key=residuals.get),
                **{f"{name}_abs_resid_mev": value for name, value in residuals.items()},
            }
        )
    return predictions_mev, rankings


def analyze_specimen(contract_path: str | Path, csv_path: str | Path, reference_path: str | Path) -> dict[str, Any]:
    contract = load_json(contract_path)
    point_count = verify_csv_matches_contract(csv_path, contract)
    result = analyze_absorption_edge_contract(contract)
    reference = load_json(reference_path)
    if result != reference:
        raise ValueError(f"recomputed contract result differs from {reference_path}")
    metadata = contract["metadata"]
    predictions, rankings = candidate_rankings(
        result,
        float(metadata["composition_x"]),
        float(metadata["temperature_k"]),
    )
    model_winners = {
        row["winner"]
        for row in rankings
        if row["candidate_id"].startswith("fractional_power")
        or row["candidate_id"] == "chu_1994_kane_region"
    }
    threshold_winners = {
        row["winner"]
        for row in rankings
        if row["candidate_id"].startswith("threshold")
    }
    boundary_limited = [
        candidate["candidate_id"]
        for candidate in result["model_candidates"]
        if abs(
            float(candidate["edge_ev"])
            - float(contract["analysis_assumptions"]["edge_search_bounds_ev"][1])
        ) <= 1e-9
    ]
    return {
        "specimen_id": result["specimen_id"],
        "measurement_id": result["measurement_id"],
        "digitized_point_count": point_count,
        "composition_x": float(metadata["composition_x"]),
        "temperature_k": float(metadata["temperature_k"]),
        "model_predictions_mev": predictions,
        "combined_envelope": result["combined_envelope"],
        "model_family_envelope": result["model_family_envelope"],
        "threshold_envelope": result["threshold_envelope"],
        "ranking_by_candidate": rankings,
        "model_candidate_winners": sorted(model_winners),
        "threshold_candidate_winners": sorted(threshold_winners),
        "boundary_limited_model_candidates": boundary_limited,
    }


def analyze(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    stems = [
        "moazzami2005_figure6a_irse",
        "moazzami2005_figure6b_irse",
    ]
    results = [
        analyze_specimen(
            root / "data/manuscript" / f"{stem}_contract_input.json",
            root / "data/manuscript" / f"{stem}_digitized.csv",
            root / "validation" / f"{stem}_contract_result.json",
        )
        for stem in stems
    ]
    fractional_winners = {
        winner for specimen in results for winner in specimen["model_candidate_winners"]
    }
    threshold_winners = {
        winner for specimen in results for winner in specimen["threshold_candidate_winners"]
    }
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 real-spectrum observation-model ranking sensitivity",
        "specimens": results,
        "decision": {
            "real_spectrum_count": len(results),
            "contract_gate_passed": len(results) >= 2,
            "fractional_power_model_span_mev_range": [
                min(item["model_family_envelope"]["full_span_mev"] for item in results),
                max(item["model_family_envelope"]["full_span_mev"] for item in results),
            ],
            "material_model_winner_changes_across_declared_observation_candidates": len(fractional_winners | threshold_winners) > 1,
            "fractional_power_candidates_alone_change_material_model_winner": len(fractional_winners) > 1,
            "fixed_threshold_candidates_change_material_model_winner": len(threshold_winners) > 1,
            "universal_correction_authorized": False,
            "single_edge_selection_authorized": False,
        },
        "claim_boundary": (
            "The ranking change is caused by declared observation definitions applied "
            "to digitized primary-figure curves. Fixed-threshold crossings are "
            "operational edge definitions, not direct estimates of the latent band gap."
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
