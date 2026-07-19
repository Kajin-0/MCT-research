#!/usr/bin/env python3
"""Analyze digitized Moazzami 2005 Figure 6 IRSE spectra."""
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


def load_digitized_csv(path: str | Path) -> tuple[list[float], list[float], int]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) < 20:
        raise ValueError("digitized spectrum requires at least 20 points")
    energies: list[float] = []
    absorption: list[float] = []
    previous = None
    for row in rows:
        energy = float(row["energy_ev"])
        value = float(row["absorption_cm1"])
        if previous is not None and energy <= previous:
            raise ValueError("digitized energy must be strictly increasing")
        previous = energy
        if float(row["energy_sigma_ev"]) > 0.005:
            raise ValueError("digitization energy uncertainty exceeds 5 meV stop rule")
        energies.append(energy)
        absorption.append(value)
    return energies, absorption, len(rows)


def build_contract(
    csv_path: str | Path,
    calibration_path: str | Path,
) -> tuple[dict[str, Any], int]:
    calibration = load_json(calibration_path)
    energies, absorption, count = load_digitized_csv(csv_path)
    specimen = calibration["specimen"]
    panel = calibration["source_reference"]["figure"]
    composition = float(specimen["composition_x"])
    contract = {
        "schema_version": "1.0",
        "specimen_id": f"moazzami2005_x{composition:.3f}",
        "measurement_id": f"figure{panel}_irse_digitized",
        "source": {
            "kind": "digitized_primary_figure",
            "reference": (
                "Moazzami et al., J. Electron. Mater. 34, 773-778 (2005), "
                f"DOI 10.1007/s11664-005-0019-3, Figure {panel}"
            ),
            "calibration_record": str(calibration_path),
        },
        "metadata": {
            "modality": "infrared spectroscopic ellipsometry, digitized solid IRSE curve",
            "temperature_k": float(specimen["temperature_k"]),
            "thickness_um": float(specimen["thickness_um"]),
            "composition_x": composition,
            "composition_sigma_x": None,
            "composition_method": (
                "figure-reported composition; growth/metrology details deferred "
                "to cited prior work"
            ),
            "carrier_type": "unknown",
            "carrier_density_cm3": None,
            "carrier_density_status": "not reported in the 2005 article",
            "tail_model": "no tail correction applied; full digitized curve exported",
        },
        "analysis_assumptions": calibration["contract_analysis_assumptions"],
        "spectrum": {
            "energy_ev": energies,
            "absorption_cm1": absorption,
        },
    }
    return contract, count


def candidate_rankings(
    result: dict[str, Any],
    composition_x: float,
    temperature_k: float,
) -> tuple[dict[str, float], list[dict[str, Any]]]:
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
    for candidate in result["model_candidates"] + result["threshold_candidates"]:
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
                **{
                    f"{name}_abs_resid_mev": value
                    for name, value in residuals.items()
                },
            }
        )
    return predictions_mev, rankings


def analyze_specimen(
    csv_path: str | Path,
    calibration_path: str | Path,
) -> dict[str, Any]:
    contract, point_count = build_contract(csv_path, calibration_path)
    result = analyze_absorption_edge_contract(contract)
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
    upper_bound = float(
        contract["analysis_assumptions"]["edge_search_bounds_ev"][1]
    )
    boundary_limited = [
        candidate["candidate_id"]
        for candidate in result["model_candidates"]
        if abs(float(candidate["edge_ev"]) - upper_bound) <= 1e-9
    ]
    return {
        "specimen_id": result["specimen_id"],
        "measurement_id": result["measurement_id"],
        "digitized_point_count": point_count,
        "input_sha256": result["input_sha256"],
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
        "contract_result": result,
    }


def analyze(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    specs = [
        (
            root / "data/manuscript/moazzami2005_figure6a_irse_digitized.csv",
            root / "data/manuscript/moazzami2005_figure6a_irse_calibration.json",
        ),
        (
            root / "data/manuscript/moazzami2005_figure6b_irse_digitized.csv",
            root / "data/manuscript/moazzami2005_figure6b_irse_calibration.json",
        ),
    ]
    results = [analyze_specimen(*spec) for spec in specs]
    fractional_winners = {
        winner
        for specimen in results
        for winner in specimen["model_candidate_winners"]
    }
    threshold_winners = {
        winner
        for specimen in results
        for winner in specimen["threshold_candidate_winners"]
    }
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 real-spectrum observation-model ranking sensitivity",
        "specimens": results,
        "decision": {
            "real_spectrum_count": len(results),
            "contract_gate_passed": len(results) >= 2,
            "fractional_power_model_span_mev_range": [
                min(
                    specimen["model_family_envelope"]["full_span_mev"]
                    for specimen in results
                ),
                max(
                    specimen["model_family_envelope"]["full_span_mev"]
                    for specimen in results
                ),
            ],
            "material_model_winner_changes_across_declared_observation_candidates": (
                len(fractional_winners | threshold_winners) > 1
            ),
            "fractional_power_candidates_alone_change_material_model_winner": (
                len(fractional_winners) > 1
            ),
            "fixed_threshold_candidates_change_material_model_winner": (
                len(threshold_winners) > 1
            ),
            "universal_correction_authorized": False,
            "single_edge_selection_authorized": False,
        },
        "claim_boundary": (
            "The ranking change is caused by declared observation definitions applied "
            "to digitized primary-figure curves. Fixed-threshold crossings are "
            "operational edge definitions, not direct estimates of the latent band gap."
        ),
    }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": result["schema_version"],
        "decision": result["decision"],
        "specimens": [
            {
                key: specimen[key]
                for key in (
                    "specimen_id",
                    "measurement_id",
                    "digitized_point_count",
                    "composition_x",
                    "temperature_k",
                    "model_predictions_mev",
                    "combined_envelope",
                    "model_family_envelope",
                    "threshold_envelope",
                    "model_candidate_winners",
                    "threshold_candidate_winners",
                    "boundary_limited_model_candidates",
                )
            }
            for specimen in result["specimens"]
        ],
        "claim_boundary": result["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--compact-output-json")
    args = parser.parse_args()
    result = analyze(args.repository_root)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.compact_output_json:
        compact_path = Path(args.compact_output_json)
        compact_path.parent.mkdir(parents=True, exist_ok=True)
        compact_path.write_text(
            json.dumps(compact(result), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
