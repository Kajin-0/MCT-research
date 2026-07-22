from __future__ import annotations

import csv
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "experimental" / "groves1967_source_metadata.csv"
PARAMETERS = ROOT / "data" / "experimental" / "groves1967_band_parameter_ledger.csv"
README = ROOT / "data" / "experimental" / "groves1967_README.md"
HANSEN_GRAPH = ROOT / "data" / "hansen" / "hansen_1982_source_graph.csv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _parameter_rows() -> dict[str, dict[str, str]]:
    return {row["record_id"]: row for row in _rows(PARAMETERS)}


def test_primary_source_identity_and_binary_boundary_are_explicit() -> None:
    rows = _rows(METADATA)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "GROVES1967"
    assert row["authors"] == "S. H. Groves; R. N. Brown; C. R. Pidgeon"
    assert row["title"] == "Interband Magnetoreflection and Band Structure of HgTe"
    assert row["venue"] == "Physical Review"
    assert row["volume"] == "161"
    assert row["issue"] == "3"
    assert row["pages"] == "779-792"
    assert row["doi"] == "10.1103/PhysRev.161.779"
    assert row["source_file_library_name"] == "groves1967.pdf"
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


def test_signed_interaction_gap_and_zero_thermal_gap_remain_distinct() -> None:
    row = _rows(METADATA)[0]
    assert row["measurement_class"] == "interband_magnetoreflection"
    assert row["signed_observable"] == "signed_Gamma6_minus_Gamma8_interaction_gap"
    assert row["sign_convention"] == (
        "E_g=E(Gamma6)-E(Gamma8); negative means inverted ordering"
    )
    assert row["thermal_gap_distinction"] == (
        "zero_thermal_energy_gap_at_Gamma8_degeneracy_is_distinct_from_negative_interaction_gap"
    )
    abstract = _parameter_rows()["GROVES1967_ABSTRACT_FIT"]
    assert float(abstract["signed_gap_ev"]) == pytest.approx(-0.283)
    assert abstract["signed_value_status"] == "explicit_signed_negative_inverted"


def test_published_rounded_fit_is_transcribed_exactly() -> None:
    row = _parameter_rows()["GROVES1967_ABSTRACT_FIT"]
    assert row["record_type"] == "published_rounded_fit"
    assert float(row["signed_gap_ev"]) == pytest.approx(-0.283)
    assert float(row["signed_gap_uncertainty_ev"]) == pytest.approx(0.001)
    assert float(row["Ep_ev"]) == pytest.approx(18.0)
    assert float(row["Ep_uncertainty_ev"]) == pytest.approx(1.0)
    assert int(row["fit_parameter_count"]) == 2
    assert row["uncertainty_semantics"] == (
        "higher_band_parameter_sensitivity_not_pointwise_measurement_sigma"
    )


def test_representative_detailed_parameter_set_is_conditional_not_universal() -> None:
    row = _parameter_rows()["GROVES1967_DETAILED_SET1"]
    expected = {
        "signed_gap_ev": -0.2833,
        "Ep_ev": 18.13,
        "Delta_ev": 1.0,
        "H1": -5.0,
        "G": -1.0,
        "L_prime": -2.0,
        "A_prime": 0.0,
        "M": -5.0,
        "L_minus_M_minus_N": 7.0,
    }
    for key, value in expected.items():
        assert float(row[key]) == pytest.approx(value)
    assert row["parameter_status"] == "representative_declared_model_parameter_set"
    assert "not an independently measured modern eight-band parameter vector" in row["notes"]
    metadata = _rows(METADATA)[0]
    assert metadata["modern_parameter_translation_status"] == (
        "requires_explicit_convention_and_parameter_translation_before_modern_8band_use"
    )


def test_temperature_ledger_separates_main_fit_proof_update_and_detector() -> None:
    rows = _parameter_rows()
    main = rows["GROVES1967_ABSTRACT_FIT"]
    assert float(main["temperature_k"]) == pytest.approx(30.0)
    assert main["temperature_status"] == (
        "source_note_estimate_not_directly_logged_setpoint"
    )

    proof = rows["GROVES1967_PROOF_UPDATE"]
    assert float(proof["temperature_k"]) == pytest.approx(1.5)
    assert proof["signed_gap_ev"] == ""
    assert float(proof["gap_magnitude_ev"]) == pytest.approx(0.30)
    assert proof["signed_value_status"] == (
        "inverted_sign_inherited_from_source_interpretation_but_only_magnitude_printed"
    )

    metadata = _rows(METADATA)[0]
    assert float(metadata["later_detector_temperature_k"]) == pytest.approx(4.2)
    assert metadata["detector_temperature_is_sample_temperature"] == "false"
    assert {float(row["temperature_k"]) for row in rows.values()} == {30.0, 1.5}


def test_specimen_and_measurement_protocol_are_preserved() -> None:
    row = _rows(METADATA)[0]
    assert row["sample_growth_method"] == "slow_Bridgman"
    assert row["growth_environment"] == "Hg_rich"
    assert float(row["growth_rate_cm_per_day"]) == pytest.approx(0.25)
    assert row["sample_purity"] == "high_purity"
    assert row["sample_crystallinity"] == "polycrystalline"
    assert row["orientation_status"] == "reflected_light_samples_several_orientations"
    assert row["near_77k_result"] == "magnetoreflection_oscillations_not_resolved_near_77K"
    assert row["surface_preparation"] == (
        "5_to_10_percent_bromine_in_methanol_then_methanol_rinse"
    )
    assert row["measurement_scan_mode"] == "fixed_photon_energy_with_magnetic_field_sweeps"
    assert row["resonance_field_processing"] == (
        "average_increasing_and_decreasing_field_resonance_positions"
    )
    assert row["fit_transition_family"] == "Gamma6_to_Gamma8"
    assert row["secondary_transition_family"] == "Gamma8_to_Gamma8"


def test_model_dependence_uncertainty_and_lineage_are_not_overstated() -> None:
    row = _rows(METADATA)[0]
    assert row["theory_model"] == (
        "coupled_Gamma6_Gamma7_Gamma8_Kane_Luttinger_magnetic_field_model"
    )
    assert row["fit_method"] == (
        "two_parameter_least_squares_conditional_on_higher_band_parameters"
    )
    assert row["pointwise_covariance_status"] == "not_reported"
    assert row["source_parameter_uncertainty_semantics"] == (
        "published parameter errors reflect higher_band_parameter uncertainty; not pointwise Gaussian measurement covariance"
    )
    assert row["relationship_to_hansen"] == (
        "not_in_reconstructed_Hansen_22_fitted_alloy_graph_endpoint_sign_source"
    )
    graph_text = HANSEN_GRAPH.read_text(encoding="utf-8").lower()
    assert "s. h. groves, r. n. brown" not in graph_text


def test_no_figure_pseudodata_or_claim_expansion_is_present() -> None:
    metadata = _rows(METADATA)[0]
    assert metadata["figure4_point_ledger_status"] == "not_digitized_in_this_tranche"
    assert metadata["figure5_point_ledger_status"] == "not_digitized_in_this_tranche"
    assert not (
        ROOT / "data" / "experimental" / "groves1967_figure4_digitized.csv"
    ).exists()
    assert not (
        ROOT / "data" / "experimental" / "groves1967_figure5_digitized.csv"
    ).exists()
    assert {int(row["figure_point_count"]) for row in _rows(PARAMETERS)} == {0}

    text = README.read_text(encoding="utf-8")
    required = (
        "This negative interaction gap is not the same object as the thermal-energy gap",
        "This is not relabeled as 4.2 K or 5.5 K",
        "The detector operating temperature is not the sample temperature",
        "contains no calibrated marker coordinates",
        "does not identify a temperature law",
        "It cannot by itself support",
    )
    assert all(token in text for token in required)
