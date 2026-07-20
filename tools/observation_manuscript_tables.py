"""Build manuscript CSV tables from the validated real-spectrum analyses."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from tools.analyze_moazzami2005_manuscript_comparators import MODEL_ORDER


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_tables(
    output: Path,
    base: dict[str, Any],
    comparison: dict[str, Any],
    sensitivity: dict[str, Any],
) -> list[str]:
    sensitivity_by_id = {item["specimen_id"]: item for item in sensitivity["specimens"]}
    provenance: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    material: list[dict[str, Any]] = []
    for spectrum, comparator in zip(base["specimens"], comparison["specimens"], strict=True):
        contract = spectrum["contract_result"]
        metadata = contract["metadata"]
        provenance.append(
            {
                "specimen_id": spectrum["specimen_id"],
                "source": contract["source"]["reference"],
                "composition_x": spectrum["composition_x"],
                "composition_sigma_x": metadata["composition_sigma_x"],
                "temperature_k": spectrum["temperature_k"],
                "thickness_um": metadata["thickness_um"],
                "carrier_type": metadata["carrier_type"],
                "carrier_density_status": metadata["carrier_density_status"],
                "digitized_point_count": spectrum["digitized_point_count"],
                "input_sha256": spectrum["input_sha256"],
            }
        )
        audit = sensitivity_by_id[spectrum["specimen_id"]]
        shifts = {
            **audit["model_candidate_max_shift_mev"],
            **audit["threshold_candidate_max_shift_mev"],
        }
        for row in comparator["candidates"]:
            edges.append(
                {
                    "specimen_id": spectrum["specimen_id"],
                    "candidate_id": row["candidate_id"],
                    "observation_class": row["observation_class"],
                    "edge_mev": row["edge_mev"],
                    "boundary_limited": row["boundary_limited"],
                    "digitization_coordinate_shift_mev": shifts[row["candidate_id"]],
                    "nominal_winner": row["nominal_winner"],
                    "nominal_runner_up": row["nominal_runner_up"],
                    "nominal_winner_margin_mev": row["nominal_winner_margin_mev"],
                }
            )
        for model in MODEL_ORDER:
            prediction = comparator["model_predictions_mev"][model]
            envelope = spectrum["model_family_envelope"]
            material.append(
                {
                    "specimen_id": spectrum["specimen_id"],
                    "model_id": model,
                    "prediction_mev": prediction,
                    "fitted_model_residual_min_mev": 1000.0 * envelope["minimum_edge_ev"] - prediction,
                    "fitted_model_residual_max_mev": 1000.0 * envelope["maximum_edge_ev"] - prediction,
                    "strict_ranking_authorized": False,
                }
            )
    candidates = [
        {"candidate_id": "fractional_power_free", "definition": "alpha=A(E-Eg)^p/E; p fitted", "source_domain": "declared fit window"},
        {"candidate_id": "fractional_power_fixed", "definition": "alpha=A(E-Eg)^p/E; p fixed", "source_domain": "p=0.5, 0.7, source-panel p, 1.0"},
        {"candidate_id": "chu_1994_kane_region", "definition": "alpha=alpha_g exp(sqrt(beta(x,T)(E-Eg)))", "source_domain": "0.170<=x<=0.443; 77<=T<=300 K"},
        {"candidate_id": "fixed_absorption_threshold", "definition": "first interpolated alpha crossing", "source_domain": "400-5000 cm-1; 5000 flagged where coordinate-sensitive"},
    ]
    claims = [
        {"claim": "fractional-model edge sensitivity is approximately 6-7 meV", "status": "authorized", "boundary": "two digitized 300 K IRSE spectra from one source study"},
        {"claim": "published Seiler is nominally closest for fitted-model edges", "status": "descriptive only", "boundary": "0.18-0.25 meV advantage over Hansen; composition uncertainty missing"},
        {"claim": "fixed-threshold definition can change the nominal comparator", "status": "authorized through 4000 cm-1", "boundary": "threshold is operational and is not the latent material gap"},
        {"claim": "one corrected or production edge exists", "status": "not authorized", "boundary": "complete candidate ensemble must be reported"},
    ]
    files = {
        "table1_specimen_provenance.csv": provenance,
        "table2_candidate_definitions.csv": candidates,
        "table3_edge_ensemble.csv": edges,
        "table4_material_model_comparison.csv": material,
        "table5_claim_boundaries.csv": claims,
    }
    for name, rows in files.items():
        write_csv(output / name, rows)
    return sorted(files)
