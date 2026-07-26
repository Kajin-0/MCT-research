import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTION_PATH = (
    ROOT
    / "configs"
    / "transport_noise"
    / "finkman1983_primary_transcription.json"
)
MATERIAL_GATE_PATH = (
    ROOT
    / "configs"
    / "transport_noise"
    / "kane_material_validation_gate.json"
)


def load_transcription() -> dict:
    return json.loads(TRANSCRIPTION_PATH.read_text(encoding="utf-8"))


def load_material_gate() -> dict:
    return json.loads(MATERIAL_GATE_PATH.read_text(encoding="utf-8"))


def test_source_identity_and_partial_exactness_status() -> None:
    data = load_transcription()
    assert data["source_id"] == "FINKMAN_1983"
    assert data["doi"] == "10.1063/1.332241"
    assert data["primary_full_text_recovered"] is True
    assert data["status"] == (
        "partial_symbol_exact_transcription_material_use_blocked"
    )


def test_experimental_domain_is_preserved() -> None:
    domain = load_transcription()["experimental_domain"]
    assert domain["composition"] == "0.205 < x < 0.310"
    assert domain["n_type_net_donor_range_cm3"] == {
        "lower_exclusive": 4.0e14,
        "upper_exclusive": 6.0e15,
    }
    assert domain["maximum_temperature_k"] == 345
    assert domain["near_intrinsic_onset"][0]["temperature_k"] == "160 and higher"
    assert domain["near_intrinsic_onset"][1]["temperature_k"] == (
        "approximately 200 and higher"
    )


def test_sample_error_statements_remain_separate() -> None:
    metadata = load_transcription()["sample_and_error_metadata"]
    assert metadata["sample_homogeneity_x"] == "+/- 0.002"
    assert metadata["maximum_thickness_error_relative"] == 0.03
    assert metadata["stored_sample_repeatability_relative"] == 0.01


def test_hall_relation_is_recovered_but_equation_set_is_not_overclaimed() -> None:
    method = load_transcription()["hall_and_neutrality_method"]
    assert method["high_temperature_carrier_relation"] == (
        "n = -1/(q R_H) under the one-carrier approximation"
    )
    assert method["intrinsic_density_equation_1_status"].endswith(
        "requires visual confirmation"
    )
    for key in (
        "electron_concentration_equation_2_status",
        "dispersion_equation_3_status",
        "effective_mass_equation_5_status",
        "heavy_hole_equation_6_status",
    ):
        assert "visual confirmation" in method[key] or "not symbol-exact" in method[key]


def test_fitted_parameters_are_pinned() -> None:
    results = load_transcription()["reported_fit_results"]
    assert results["momentum_matrix_element_ev_cm"] == {
        "value": 8.0e-8,
        "reported_plus_minus": 0.4e-8,
    }
    assert results["heavy_hole_mass_ratio_m0"] == {
        "value": 0.63,
        "reported_plus_minus": 0.06,
    }
    assert results["band_gap_ev"] == (
        "-0.287 + 1.717*x + 5.805e-4*T*(1 - 2.01*x) + 0.2415*x^4"
    )


def test_gap_standard_deviation_unit_is_not_silently_corrected() -> None:
    results = load_transcription()["reported_fit_results"]
    assert results["gap_standard_deviation_extracted_text"] == "4 MeV"
    assert "visual primary-page confirmation" in results[
        "gap_standard_deviation_interpretation"
    ]


def test_figure_examples_are_not_digitized_points() -> None:
    examples = load_transcription()["figure_level_recovered_examples"]
    assert [example["composition_x"] for example in examples] == [0.225, 0.29]
    assert all("not digitized" in example["status"] for example in examples)


def test_project_material_authorization_remains_blocked() -> None:
    acceptance = load_transcription()["pr385_acceptance"]
    assert acceptance["countable_material_points"] == 0
    assert acceptance["positive_point_uncertainties_recovered"] is False
    assert acceptance["eta_known"] is False
    assert acceptance["validated_neutrality_model_recovered"] is False
    assert acceptance["project_N_star_authorized"] is False
    assert acceptance["project_alpha_authorized"] is False
    assert acceptance["screening_authorized"] is False
    assert acceptance["detector_coupling_authorized"] is False

    gate = load_material_gate()
    assert gate["status"] == "blocked_no_accepted_hgcdte_reference_set"
    assert gate["accepted_material_evidence"] == []
    assert gate["material_parameter_values_authorized"] is False
    assert gate["predictive_noise_claims_authorized"] is False


def test_remaining_actions_require_visual_and_mapping_audits() -> None:
    actions = load_transcription()["remaining_primary_actions"]
    assert actions[0] == "visually confirm equations 1 through 6 from the primary PDF"
    assert any("band-gap standard deviation" in action for action in actions)
    assert any("historic P and heavy-hole mass" in action for action in actions)
