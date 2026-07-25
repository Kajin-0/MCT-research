import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = (
    REPOSITORY_ROOT
    / "configs"
    / "transport_noise"
    / "kane_material_validation_gate.json"
)


def load_gate() -> dict:
    return json.loads(GATE_PATH.read_text(encoding="utf-8"))


def test_gate_remains_blocked_without_accepted_hgcdte_evidence() -> None:
    gate = load_gate()
    assert gate["status"] == "blocked_no_accepted_hgcdte_reference_set"
    assert gate["accepted_material_evidence"] == []
    assert gate["decision"] == (
        "validation_design_accepted_material_closure_not_accepted"
    )


def test_gate_pins_two_parameter_coordinates_and_observable_classes() -> None:
    gate = load_gate()
    assert gate["parameters_under_test"] == [
        "parabolic_density_scale_cm3",
        "nonparabolicity_ev_inverse",
    ]
    structural = gate["structural_identifiability"]
    assert structural["method"] == "weighted_log_sensitivity_svd"
    assert "density_cm3" in structural["absolute_scale_observables"]
    assert "compressibility_cm3_per_ev" in structural[
        "absolute_scale_observables"
    ]
    assert structural["scale_free_shape_observables"] == [
        "generalized_einstein_factor"
    ]


def test_gate_requires_three_points_two_sources_and_temperature_span() -> None:
    requirements = load_gate()["minimum_external_evidence"]
    assert requirements["point_count"] == 3
    assert requirements["provenance_group_count"] == 2
    assert requirements["temperature_count"] == 2
    assert requirements["requires_hgcdte_specific_points"]
    assert requirements["requires_primary_or_independent_points"]
    assert requirements["requires_positive_standard_uncertainty"]
    assert requirements["requires_known_eta_or_validated_neutrality"]


def test_gate_requires_holdout_adequacy_and_three_band_decision() -> None:
    tests = load_gate()["model_adequacy_tests_after_parameter_identification"]
    assert "hold_out_prediction_error_with_uncertainty" in tests
    assert "residual_structure_against_temperature_and_composition" in tests
    assert (
        "decision_on_simplified_dispersion_versus_full_three_band_model" in tests
    )


def test_material_outputs_and_detector_coupling_remain_unauthorized() -> None:
    gate = load_gate()
    for key in (
        "material_parameter_values_authorized",
        "equilibrium_density_authorized",
        "chemical_compressibility_authorized",
        "screening_authorized",
        "detector_coupling_authorized",
        "predictive_noise_claims_authorized",
    ):
        assert gate[key] is False
