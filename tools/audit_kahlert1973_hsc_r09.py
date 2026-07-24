from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/kahlert1973_hsc_r09_source_metadata.csv"
SAMPLE = ROOT / "data/hansen/kahlert1973_sample_population.csv"
PARAMETERS = ROOT / "data/hansen/kahlert1973_model_parameters.csv"
RELATION = ROOT / "data/hansen/kahlert1973_temperature_relation.csv"
PAIRINGS = ROOT / "data/hansen/kahlert1973_hansen_ingestion_candidates.csv"


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
    metadata = _csv(META)[0]
    sample = _csv(SAMPLE)[0]
    parameters = {row["parameter_id"]: row for row in _csv(PARAMETERS)}
    relation = _csv(RELATION)[0]
    candidates = {row["candidate_id"]: row for row in _csv(PAIRINGS)}

    x = float(metadata["nominal_composition_x"])
    eg0 = float(relation["Eg0_eV"])
    alpha = float(relation["alpha_per_K"])
    exact_slope = eg0 * alpha
    rounded_slope = float(relation["source_reported_rounded_slope_eV_per_K"])

    key_temperatures = [0.0, 4.2, 50.0, 77.0, 80.0, 130.0]
    source_model = {
        str(t).rstrip("0").rstrip("."): eg0 * (1.0 + alpha * t)
        for t in key_temperatures
    }
    hansen_model = {
        str(t).rstrip("0").rstrip("."): hansen_gap_ev(x, t)
        for t in key_temperatures
    }

    source_80 = source_model["80"]
    rounded_80 = eg0 + rounded_slope * 80.0
    hansen_slope = 5.35e-4 * (1.0 - 2.0 * x)

    result = {
        "schema_version": "1.0",
        "source_id": metadata["source_id"],
        "source_pdf_sha256": metadata["source_pdf_sha256"],
        "source_scope": {
            "article_pages": [int(metadata["first_page"]), int(metadata["last_page"])],
            "named_specimen_count": 0,
            "physical_specimen_count_reported": False,
            "source_level_sample_population_rows": 1,
            "figure_digitization_performed": False,
            "pointwise_covariance_reported": False,
            "copyrighted_source_committed": False,
        },
        "measurement_identity": {
            "primary_measurement_class": metadata["primary_measurement_class"],
            "primary_gap_observable": metadata["primary_gap_observable"],
            "direct_observations": [
                "longitudinal_resistivity_vs_magnetic_field",
                "shubnikov_de_haas_extremum_positions",
                "magnetophonon_resonance_extremum_positions_vs_temperature",
            ],
            "gap_relation_is_model_conditioned": True,
            "direct_optical_edge": False,
        },
        "sample_population": {
            "vendor": sample["vendor"],
            "composition_x": float(sample["nominal_composition_x"]),
            "composition_uncertainty_status": sample["composition_uncertainty_status"],
            "mobility_4p2k_cm2_v_s": float(sample["mobility_4p2k_cm2_v_s"]),
            "carrier_concentration_4p2k_cm3": float(sample["carrier_concentration_4p2k_cm3"]),
            "specimen_count_status": sample["physical_specimen_count_status"],
        },
        "source_reported_parameters": {
            "band_edge_effective_mass_ratio": float(parameters["KAH73_MSTAR0"]["value"]),
            "band_edge_effective_mass_half_width": float(parameters["KAH73_MSTAR0"]["half_width"]),
            "effective_g_factor": float(parameters["KAH73_GSTAR0"]["value"]),
            "effective_g_factor_half_width": float(parameters["KAH73_GSTAR0"]["half_width"]),
            "sdh_gap_input_ev": float(parameters["KAH73_EG_SDH_INPUT"]["value"]),
            "spin_orbit_splitting_ev": float(parameters["KAH73_DELTA"]["value"]),
            "fermi_energy_ev": float(parameters["KAH73_EF"]["value"]),
            "accepted_hgte_like_lo_phonon_ev": float(parameters["KAH73_HGTE_LO"]["value"]),
            "rejected_cdte_like_lo_phonon_ev": float(parameters["KAH73_CDTE_LO"]["value"]),
        },
        "temperature_relation": {
            "relation": relation["relation"],
            "mass_relation": relation["mass_relation"],
            "temperature_range_k": [
                float(relation["temperature_min_k"]),
                float(relation["temperature_max_k"]),
            ],
            "Eg0_ev": eg0,
            "alpha_per_k": alpha,
            "exact_slope_from_printed_factors_ev_per_k": exact_slope,
            "source_reported_rounded_slope_ev_per_k": rounded_slope,
            "rounding_difference_ev_per_k": exact_slope - rounded_slope,
            "source_model_gap_ev": source_model,
            "rounded_slope_gap_80k_ev": rounded_80,
            "fit_covariance_reported": False,
        },
        "hansen_descriptive_comparison": {
            "independent_validation": False,
            "hansen_slope_ev_per_k": hansen_slope,
            "source_exact_to_hansen_slope_ratio": exact_slope / hansen_slope,
            "hansen_gap_ev": hansen_model,
            "residual_hansen_minus_source_relation_80k_ev": hansen_model["80"] - source_80,
            "residual_hansen_minus_rounded_relation_80k_ev": hansen_model["80"] - rounded_80,
            "external_direct_comparison_slope_ev_per_k": float(parameters["KAH73_DIRECT_COMPARISON"]["value"]),
            "external_direct_comparison_is_source_measurement": False,
        },
        "hansen_ingestion": {
            "candidate_ids": sorted(candidates),
            "candidate_count": len(candidates),
            "source_relation_available": True,
            "per_marker_source_labels_available": False,
            "exact_ingestion_mapping_resolved": False,
            "reason": "Kahlert and Bauer print a complete temperature relation, but Hansen does not expose source-labeled HSC_R09 markers or state whether the relation, a rounded 80 K conversion, or selected figure points were ingested.",
        },
        "decision": {
            "primary_source_recovered": True,
            "measurement_class_corrected": True,
            "temperature_relation_reconstructed": True,
            "hansen_exact_ingestion_mapping_resolved": False,
            "direct_hansen_validation_authorized": False,
            "controlling_decision": "primary_source_recovered_temperature_relation_reconstructed_hansen_marker_mapping_unresolved",
        },
    }
    return _stable(result)


def render_reference() -> str:
    return json.dumps(build_audit(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    print(render_reference(), end="")


if __name__ == "__main__":
    main()
