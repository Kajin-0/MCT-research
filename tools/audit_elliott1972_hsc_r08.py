from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/hansen/elliott1972_hsc_r08_source_metadata.csv"
SPECIMEN_PATH = ROOT / "data/hansen/elliott1972_specimens.csv"
CARRIER_PATH = ROOT / "data/hansen/elliott1972_table1_carriers.csv"
GAP_PATH = ROOT / "data/hansen/elliott1972_table2_gap_candidates.csv"
PARAMETER_PATH = ROOT / "data/hansen/elliott1972_model_parameters.csv"
INGESTION_PATH = ROOT / "data/hansen/elliott1972_hansen_ingestion_candidates.csv"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _stable(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: _stable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_stable(item) for item in value]
    return value


def hansen_gap_ev(x: float, temperature_k: float) -> float:
    return (
        -0.302
        + 1.93 * x
        - 0.810 * x**2
        + 0.832 * x**3
        + 5.35e-4 * temperature_k * (1.0 - 2.0 * x)
    )


def build_audit() -> dict[str, Any]:
    metadata = _csv(METADATA_PATH)[0]
    specimens = _csv(SPECIMEN_PATH)
    carriers = _csv(CARRIER_PATH)
    gaps = _csv(GAP_PATH)
    parameters = {row["parameter_id"]: row for row in _csv(PARAMETER_PATH)}
    pairings = _csv(INGESTION_PATH)

    gap_rows = []
    for row in gaps:
        x = float(row["composition_x"])
        temperature = float(row["temperature_k"])
        source_gap_ev = float(row["zero_pressure_gap_mev"]) / 1000.0
        gap_rows.append(
            {
                "observation_id": row["observation_id"],
                "sample_id": row["sample_id"],
                "temperature_k": temperature,
                "composition_x": x,
                "hole_mass_ratio_assumption": (
                    None
                    if row["hole_mass_ratio_assumption"] == ""
                    else float(row["hole_mass_ratio_assumption"])
                ),
                "fermi_energy_from_valence_mev": float(
                    row["fermi_energy_from_valence_mev"]
                ),
                "source_zero_pressure_gap_ev": source_gap_ev,
                "hansen_gap_ev": hansen_gap_ev(x, temperature),
                "hansen_minus_source_ev": hansen_gap_ev(x, temperature) - source_gap_ev,
            }
        )

    pair_rows = []
    for row in pairings:
        pair_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "composition_x": float(row["composition_x"]),
                "slope_ev_per_k": float(row["slope_ev_per_k"]),
                "normalized_80k_ev": float(row["normalized_80k_ev"]),
                "candidate_status": row["candidate_status"],
            }
        )

    pressure_coeff = float(parameters["ELL72_GAP_PRESSURE_COEFF"]["value"])
    result = {
        "schema_version": "1.0",
        "source_id": metadata["source_id"],
        "source_pdf_sha256": metadata["source_pdf_sha256"],
        "source_scope": {
            "pdf_pages": 13,
            "article_pages": "2985-2997",
            "named_sample_identities": len(specimens),
            "physical_specimen_count_lower_bound": 4,
            "table1_carrier_rows": len(carriers),
            "table2_gap_rows": len(gaps),
            "hansen_pairing_candidates": len(pairings),
            "figure_digitization_performed": False,
            "copyrighted_source_committed": False,
        },
        "measurement_contract": {
            "primary_class": metadata["primary_measurement_class"],
            "gap_observable": metadata["primary_gap_observable"],
            "pressure_range_kbar": [0.0, 9.0],
            "composition_method": metadata["composition_method"],
            "composition_half_width_x": float(metadata["composition_half_width_x"]),
            "temperatures_k": [1.3, 4.0, 4.2, 77.0],
            "pressure_medium": metadata["pressure_medium"],
            "pressure_systematic": (
                "At 4.2 K the authors assume the bomb pressure equals the externally maintained pressure; "
                "they discuss possible pressure loss during helium solidification and cooling but do not assign a pointwise uncertainty."
            ),
        },
        "specimens": [
            {
                "sample_id": row["sample_id"],
                "composition_x": float(row["composition_x"]),
                "composition_half_width_x": float(row["composition_half_width_x"]),
                "anneal_state": row["anneal_state"],
                "transition_interval_4p2k_kbar": [
                    float(value) for value in row["transition_interval_4p2k_kbar"].split("-")
                ],
            }
            for row in specimens
        ],
        "source_reported_parameters": {
            "gap_pressure_coefficient_ev_per_bar": pressure_coeff,
            "gap_pressure_coefficient_ev_per_kbar": pressure_coeff * 1000.0,
            "kane_matrix_ev_cm": float(parameters["ELL72_KANE_MATRIX"]["value"]),
            "kane_matrix_role": "fixed_inherited_parameter_not_fitted_in_source",
            "heavy_hole_mass_sensitivity_range_m0": [0.3, 0.7],
            "deformation_potential_ev": float(
                parameters["ELL72_DEFORMATION_POTENTIAL"]["value"]
            ),
            "fit_covariance_reported": False,
        },
        "table2_model_outputs": gap_rows,
        "temperature_pairing_candidates": pair_rows,
        "source_interpretation": {
            "fermi_level_pressure_independence": (
                "At 4.2 K the source reports pressure-independent Fermi energies of 9, 16, and 20 meV "
                "above the valence-band edge for 7B, 7B1, and 8B."
            ),
            "acceptor_model_status": "proposed_source_model_not_direct_observation",
            "annealed_sample_acceptor_level_mev": 9.0,
            "as_grown_impurity_band_energy_mev_approx": 20.0,
            "magnetic_freeze_out_assignment": (
                "lowest-energy spin-split zero-order Landau level passing through the Fermi energy"
            ),
        },
        "hansen_lineage": {
            "hansen_original_classification": "magneto_optical_gap",
            "corrected_primary_classification": "hydrostatic_pressure_magnetotransport",
            "candidate_source_native_points_reconstructed": True,
            "exact_hansen_per_marker_mapping": "unresolved_no_source_labels",
            "independent_validation": False,
            "reason": (
                "Elliott is part of Hansen's fitted lineage. Table II exposes source-native model-derived gaps, "
                "but Hansen does not label individual HSC_R08 markers and the 77 K result has two heavy-hole-mass alternatives."
            ),
        },
        "decision": {
            "primary_source_recovered": True,
            "primary_measurement_class_corrected": True,
            "table1_carrier_summary_reconstructed": True,
            "table2_gap_candidates_reconstructed": True,
            "pointwise_pressure_covariance_authorized": False,
            "figure_curve_digitization_authorized": False,
            "hansen_exact_ingestion_mapping_resolved": False,
            "direct_hansen_validation_authorized": False,
            "controlling_decision": "primary_source_recovered_source_native_gap_candidates_reconstructed_hansen_marker_mapping_unresolved",
        },
    }
    return _stable(result)


def render_reference() -> str:
    return json.dumps(build_audit(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    print(render_reference(), end="")


if __name__ == "__main__":
    main()
