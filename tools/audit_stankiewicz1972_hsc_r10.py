from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/stankiewicz1972_hsc_r10_source_metadata.csv"
SAMPLES = ROOT / "data/hansen/stankiewicz1972_sample_records.csv"
TABLE1 = ROOT / "data/hansen/stankiewicz1972_table1_parameters.csv"
ASSUMPTIONS = ROOT / "data/hansen/stankiewicz1972_model_assumptions.csv"
EQ4 = ROOT / "data/hansen/stankiewicz1972_equation4_relation.csv"
CANDIDATES = ROOT / "data/hansen/stankiewicz1972_hansen_ingestion_candidates.csv"


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


def source_eq4_gap_ev(x: float, temperature_k: float) -> float:
    return -0.303 + 1.91 * x + 5.25e-4 * (1.0 - 2.0 * x) * temperature_k


def build_audit() -> dict[str, Any]:
    metadata = _csv(META)[0]
    samples = _csv(SAMPLES)
    table = _csv(TABLE1)
    assumptions = {row["parameter_id"]: row for row in _csv(ASSUMPTIONS)}
    relation = _csv(EQ4)[0]
    candidates = _csv(CANDIDATES)

    specimen_records: list[dict[str, Any]] = []
    descriptive_comparisons: list[dict[str, Any]] = []
    for row in table:
        x = float(row["composition_x"])
        gap77 = float(row["gap_77k_eV"])
        gap280 = float(row["gap_280k_eV"])
        endpoint_slope = (gap280 - gap77) / (280.0 - 77.0)
        fitted_slope = float(row["temperature_coefficient_eV_per_K"])
        specimen_records.append(
            {
                "record_id": row["record_id"],
                "composition_x": x,
                "composition_half_width_x": float(row["composition_half_width_x"]),
                "gap_77k_ev": gap77,
                "gap_77k_half_width_ev": float(row["gap_77k_half_width_eV"]),
                "gap_280k_ev": gap280,
                "gap_280k_half_width_ev": float(row["gap_280k_half_width_eV"]),
                "pressure_coefficient_ev_per_atm": float(row["pressure_coefficient_eV_per_atm"]),
                "pressure_coefficient_half_width_ev_per_atm": float(row["pressure_coefficient_half_width_eV_per_atm"]),
                "temperature_coefficient_ev_per_k": fitted_slope,
                "temperature_coefficient_half_width_ev_per_k": float(row["temperature_coefficient_half_width_eV_per_K"]),
                "endpoint_implied_slope_ev_per_k": endpoint_slope,
                "endpoint_minus_fitted_slope_ev_per_k": endpoint_slope - fitted_slope,
            }
        )
        descriptive_comparisons.append(
            {
                "composition_x": x,
                "hansen_gap_77k_ev": hansen_gap_ev(x, 77.0),
                "source_table_gap_77k_ev": gap77,
                "hansen_minus_source_77k_ev": hansen_gap_ev(x, 77.0) - gap77,
                "hansen_gap_280k_ev": hansen_gap_ev(x, 280.0),
                "source_table_gap_280k_ev": gap280,
                "hansen_minus_source_280k_ev": hansen_gap_ev(x, 280.0) - gap280,
                "source_eq4_gap_77k_ev": source_eq4_gap_ev(x, 77.0),
                "source_eq4_gap_280k_ev": source_eq4_gap_ev(x, 280.0),
            }
        )

    result = {
        "schema_version": "1.0",
        "source_id": metadata["source_id"],
        "source_pdf_sha256": metadata["source_pdf_sha256"],
        "source_scope": {
            "article_pages": [int(metadata["first_page"]), int(metadata["last_page"])],
            "physical_specimen_count": 4,
            "composition_defined_specimen_records": len(samples),
            "table1_specimen_rows": len(table),
            "table1_gap_value_count": 2 * len(table),
            "figure_digitization_performed": False,
            "pointwise_covariance_reported": False,
            "copyrighted_source_committed": False,
        },
        "measurement_identity": {
            "primary_measurement_class": metadata["primary_measurement_class"],
            "primary_gap_observable": metadata["primary_gap_observable"],
            "direct_observations": [
                "hall_coefficient_vs_temperature",
                "hall_coefficient_vs_hydrostatic_pressure_at_fixed_temperature",
            ],
            "magnetic_field_oe": float(metadata["magnetic_field_oe"]),
            "temperature_range_k": [float(metadata["temperature_min_k"]), float(metadata["temperature_max_k"])],
            "pressure_max_atm": float(metadata["pressure_max_atm"]),
            "gap_values_are_model_conditioned": True,
            "direct_optical_edge": False,
        },
        "sample_provenance": {
            "compositions_x": [float(row["composition_x"]) for row in samples],
            "composition_half_width_x": 0.005,
            "preparation_method": samples[0]["preparation_method"],
            "composition_method": samples[0]["composition_method"],
            "homogeneity_checks": samples[0]["homogeneity_checks"],
            "source_native_specimen_identifiers_reported": False,
            "intrinsic_assumption": True,
            "source_reports_hole_influence": True,
        },
        "source_model_assumptions": {
            "kane_matrix_element_ep_ev": float(assumptions["SG72_EP"]["value"]),
            "hole_effective_mass_ratio": float(assumptions["SG72_MH"]["value"]),
            "overlap_energy_ev": float(assumptions["SG72_DELTA_E"]["value"]),
            "inverted_band_extension": assumptions["SG72_INVERTED_EXTENSION"]["value"],
            "hole_statistics": assumptions["SG72_HOLE_STATISTICS"]["value"],
            "fixed_quantities_pressure_independent": True,
            "fixed_quantities_temperature_independent": True,
            "model_error_beyond_measurement_error_acknowledged": True,
        },
        "table1": specimen_records,
        "source_equation4": {
            "relation": relation["relation_text"],
            "domain_x": [float(relation["domain_x_min"]), float(relation["domain_x_max"])],
            "intercept_ev": float(relation["intercept_eV"]),
            "linear_x_coefficient_ev": float(relation["linear_x_coefficient_eV"]),
            "temperature_prefactor_ev_per_k": float(relation["temperature_prefactor_eV_per_K"]),
            "source_caveat": relation["source_caveat"],
        },
        "hansen_descriptive_comparison": {
            "independent_validation": False,
            "same_x_temperature_comparisons": descriptive_comparisons,
        },
        "hansen_ingestion": {
            "candidate_count": len(candidates),
            "tabulated_gap_candidate_count": sum(row["candidate_basis"] == "Table_1_model_fit_output" for row in candidates),
            "equation_family_candidate_present": any(row["candidate_basis"] == "Equation_4_scalar_relation" for row in candidates),
            "per_marker_source_labels_available": False,
            "exact_ingestion_mapping_resolved": False,
            "reason": "Stankiewicz and Giriat provide eight exact Table 1 gap values and Equation 4, but Hansen does not expose source-labeled HSC_R10 markers or identify whether table values, relation-generated values, figure markers, or another transcription were ingested.",
        },
        "decision": {
            "primary_source_recovered": True,
            "measurement_class_corrected": True,
            "table1_parameters_reconstructed": True,
            "equation4_reconstructed": True,
            "hansen_exact_ingestion_mapping_resolved": False,
            "direct_hansen_validation_authorized": False,
            "controlling_decision": "primary_source_recovered_table1_and_equation4_reconstructed_hansen_marker_mapping_unresolved",
        },
    }
    return _stable(result)


def render_reference() -> str:
    return json.dumps(build_audit(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    print(render_reference(), end="")


if __name__ == "__main__":
    main()
