from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/groves1971_hsc_r11_source_metadata.csv"
SAMPLE = ROOT / "data/hansen/groves1971_sample_record.csv"
STATES = ROOT / "data/hansen/groves1971_measurement_states.csv"
TRANSITIONS = ROOT / "data/hansen/groves1971_transition_summary.csv"
PARAMETERS = ROOT / "data/hansen/groves1971_model_parameters.csv"
ASSUMPTIONS = ROOT / "data/hansen/groves1971_model_assumptions.csv"
CANDIDATES = ROOT / "data/hansen/groves1971_hansen_ingestion_candidates.csv"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _number(value: str) -> float | None:
    return None if value == "" else float(value)


def _stable(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: _stable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_stable(item) for item in value]
    return value


def build_audit() -> dict[str, Any]:
    metadata = _csv(META)[0]
    sample = _csv(SAMPLE)[0]
    states = {row["state_id"]: row for row in _csv(STATES)}
    transitions = _csv(TRANSITIONS)
    parameters = {row["parameter_id"]: row for row in _csv(PARAMETERS)}
    assumptions = _csv(ASSUMPTIONS)
    candidates = _csv(CANDIDATES)

    body_states = [states["GR71_LOW_BODY"], states["GR71_HIGH_BODY"]]
    abstract_states = [states["GR71_ABSTRACT_4K"], states["GR71_ABSTRACT_77K"]]

    result = {
        "schema_version": "1.0",
        "source_id": metadata["source_id"],
        "source_pdf_sha256": metadata["source_pdf_sha256"],
        "source_scope": {
            "article_pages": [int(metadata["first_page"]), int(metadata["last_page"])],
            "pdf_page_count": int(metadata["source_pdf_page_count"]),
            "physical_specimen_count": int(sample["physical_specimen_count"]),
            "figure_digitization_performed": metadata["figure_digitization_performed"] == "true",
            "pointwise_covariance_reported": metadata["pointwise_covariance"] != "not_reported",
            "copyrighted_source_committed": metadata["source_binary_committed"] == "true",
        },
        "measurement_identity": {
            "primary_measurement_class": metadata["primary_measurement_class"],
            "primary_gap_observable": metadata["primary_gap_observable"],
            "direct_observations": [
                "circularly_polarized_reflectivity_vs_magnetic_field",
                "magnetoreflection_resonance_peak_fields",
                "transition_peak_energies_vs_magnetic_field",
            ],
            "gap_is_direct_zero_field_extrapolation": False,
            "gap_is_model_conditioned": True,
            "direct_optical_absorption_edge": False,
        },
        "sample": {
            "sample_id": sample["sample_id"],
            "dimensions_mm": sample["dimensions_mm"],
            "composition_x": float(sample["nominal_composition_x"]),
            "composition_half_width": float(sample["composition_half_width"]),
            "composition_method": sample["composition_method"],
            "carrier_type": sample["carrier_type"],
            "carrier_concentration_4k_cm3": float(sample["carrier_concentration_4k_cm3"]),
            "hall_mobility_4k_cm2_v_s": float(sample["hall_mobility_4k_cm2_v_s"]),
            "reflecting_surface": sample["reflecting_surface"],
            "magnetic_field_orientation": sample["magnetic_field_orientation"],
            "homogeneity_statement": sample["homogeneity_statement"],
        },
        "temperature_provenance": {
            "body_measurement_states": [
                {
                    "state_id": row["state_id"],
                    "temperature_range_k": [float(row["temperature_min_k"]), float(row["temperature_max_k"])],
                    "representative_temperature_k": float(row["representative_temperature_k"]),
                    "representative_temperature_basis": row["representative_temperature_basis"],
                    "data_visibility": row["data_visibility"],
                    "gamma6_minus_gamma8_gap_ev": _number(row["gamma6_minus_gamma8_gap_eV"]),
                    "gap_value_status": row["gap_value_status"],
                }
                for row in body_states
            ],
            "abstract_summary_states": [
                {
                    "state_id": row["state_id"],
                    "temperature_label_k": float(row["abstract_temperature_label_k"]),
                    "sign_statement": row["abstract_sign_statement"],
                    "numeric_gap_reported": row["gamma6_minus_gamma8_gap_eV"] != "",
                }
                for row in abstract_states
            ],
            "body_and_abstract_temperature_labels_identical": False,
            "exact_4k_and_77k_numeric_gaps_reported": False,
        },
        "transition_evidence": {
            "low_state": {
                "field_range_kOe": [
                    float(transitions[0]["field_min_kOe"]),
                    float(transitions[0]["field_max_kOe"]),
                ],
                "photon_energy_observed_max_ev": float(transitions[0]["photon_energy_observed_max_eV"]),
                "photon_energy_plotted_max_ev": float(transitions[0]["photon_energy_plotted_max_eV"]),
                "transition_count_status": transitions[0]["transition_count_status"],
                "reflectivity_change_max_fraction": float(transitions[0]["reflectivity_change_max_fraction"]),
                "polarizations": transitions[0]["polarizations"].split(";"),
                "experimental_peak_method": transitions[0]["experimental_peak_method"],
            },
            "high_state_data_shown": False,
            "theoretical_curves_digitized_as_data": False,
            "unresolved_weak_transition_ids": ["2"],
        },
        "source_reported_parameters": {
            "low_state_gap_ev": float(parameters["GR71_GAP_LOW"]["value"]),
            "high_state_gap_ev": float(parameters["GR71_GAP_HIGH"]["value"]),
            "Kane_Ep_ev": float(parameters["GR71_EP"]["value"]),
            "Gamma8_valence_mass_signed_m0": float(parameters["GR71_MV_SIGNED"]["value"]),
            "Gamma8_valence_mass_fit_sensitivity_half_width_m0": float(parameters["GR71_MV_SIGNED"]["half_width"]),
            "abstract_valence_mass_magnitude_m0": float(parameters["GR71_MV_ABSTRACT"]["value"]),
            "spin_orbit_splitting_approx_ev": float(parameters["GR71_SPIN_ORBIT"]["value"]),
            "mass_interval_is_statistical_uncertainty": False,
            "gap_covariance_reported": False,
        },
        "model_assumptions": [row["assumption"] for row in assumptions],
        "hansen_ingestion": {
            "candidate_ids": [row["candidate_id"] for row in candidates],
            "candidate_count": len(candidates),
            "numeric_body_candidate_count": sum(row["gap_eV"] != "" for row in candidates),
            "qualitative_abstract_candidate_count": sum(row["gap_eV"] == "" for row in candidates),
            "per_marker_source_labels_available": False,
            "exact_ingestion_mapping_resolved": False,
            "reason": "Groves prints approximate body-state gaps over 20-30 K and 90-100 K while the abstract uses qualitative 4 K and 77 K labels; Hansen does not expose source-labeled HSC_R11 markers or state which representation was ingested.",
        },
        "decision": {
            "primary_source_recovered": True,
            "measurement_class_resolved": True,
            "single_specimen_provenance_resolved": True,
            "model_parameters_reconstructed": True,
            "body_abstract_temperature_distinction_preserved": True,
            "hansen_exact_ingestion_mapping_resolved": False,
            "direct_hansen_validation_authorized": False,
            "controlling_decision": "primary_source_recovered_interband_magnetoreflection_parameters_reconstructed_temperature_labels_and_hansen_marker_mapping_unresolved",
        },
    }
    return _stable(result)


def render_reference() -> str:
    return json.dumps(build_audit(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    print(render_reference(), end="")


if __name__ == "__main__":
    main()
