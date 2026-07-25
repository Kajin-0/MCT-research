import numpy as np
import pytest

from mct_research.transport_noise.kane_parameter_validation import (
    KaneMaterialEvidencePoint,
    KaneParameterPoint,
    KaneValidationObservation,
    analyze_kane_validation_design,
    assess_kane_material_evidence,
    kane_log_sensitivity_matrix,
)


def nominal_parameters() -> KaneParameterPoint:
    return KaneParameterPoint(
        parabolic_density_scale_cm3=2.0e16,
        nonparabolicity_ev_inverse=8.0,
    )


def observation(
    kind: str,
    *,
    eta: float = -0.5,
    temperature_k: float = 77.0,
    uncertainty: float = 0.02,
    condition_id: str = "c1",
) -> KaneValidationObservation:
    return KaneValidationObservation(
        kind=kind,
        eta=eta,
        temperature_k=temperature_k,
        relative_standard_uncertainty=uncertainty,
        condition_id=condition_id,
    )


def evidence_point(
    evidence_id: str,
    provenance_group: str,
    condition_id: str,
    observable_kind: str,
    *,
    temperature_k: float,
    eta_known: bool = True,
    validated_neutrality_model: bool = False,
    material_specific: bool = True,
    independent_or_primary: bool = True,
) -> KaneMaterialEvidencePoint:
    return KaneMaterialEvidencePoint(
        evidence_id=evidence_id,
        provenance_group=provenance_group,
        condition_id=condition_id,
        observable_kind=observable_kind,
        composition=0.22,
        temperature_k=temperature_k,
        value=1.0e15 if observable_kind != "generalized_einstein_factor" else 1.1,
        standard_uncertainty=1.0e13 if observable_kind != "generalized_einstein_factor" else 0.02,
        material_specific=material_specific,
        independent_or_primary=independent_or_primary,
        eta_known=eta_known,
        validated_neutrality_model=validated_neutrality_model,
    )


def test_parameter_point_requires_positive_alpha_for_log_sensitivity() -> None:
    with pytest.raises(ValueError, match="positive for log-sensitivity"):
        KaneParameterPoint(1.0e16, 0.0)


def test_observation_rejects_unknown_kind_and_invalid_uncertainty() -> None:
    with pytest.raises(ValueError, match="unsupported observation kind"):
        observation("mobility")
    with pytest.raises(ValueError, match="relative_standard_uncertainty"):
        observation("density_cm3", uncertainty=0.0)


def test_absolute_and_scale_free_observables_have_expected_scale_sensitivity() -> None:
    observations = [
        observation("density_cm3"),
        observation("compressibility_cm3_per_ev"),
        observation("generalized_einstein_factor"),
    ]
    matrix = kane_log_sensitivity_matrix(observations, nominal_parameters())
    weights = np.array([50.0, 50.0, 50.0])
    np.testing.assert_allclose(matrix[:2, 0], weights[:2], rtol=0.0, atol=2.0e-8)
    assert abs(matrix[2, 0]) < 2.0e-8
    assert abs(matrix[2, 1]) > 1.0e-4


def test_repeated_density_at_one_condition_is_rank_one() -> None:
    observations = [observation("density_cm3") for _ in range(3)]
    report = analyze_kane_validation_design(observations, nominal_parameters())
    assert report.rank == 1
    assert not report.full_rank
    assert np.isinf(report.condition_number)


def test_density_plus_einstein_factor_identifies_both_parameters_locally() -> None:
    observations = [
        observation("density_cm3"),
        observation("generalized_einstein_factor"),
    ]
    report = analyze_kane_validation_design(observations, nominal_parameters())
    assert report.rank == 2
    assert report.full_rank
    assert np.isfinite(report.condition_number)


def test_matched_density_and_compressibility_identify_both_parameters_locally() -> None:
    observations = [
        observation("density_cm3"),
        observation("compressibility_cm3_per_ev"),
    ]
    report = analyze_kane_validation_design(observations, nominal_parameters())
    assert report.rank == 2
    assert report.full_rank


def test_uncertainty_rescales_rows_without_changing_unweighted_derivative() -> None:
    precise = observation("density_cm3", uncertainty=0.01)
    coarse = observation("density_cm3", uncertainty=0.04)
    matrix = kane_log_sensitivity_matrix([precise, coarse], nominal_parameters())
    np.testing.assert_allclose(matrix[0], 4.0 * matrix[1], rtol=2.0e-10, atol=2.0e-10)


def test_temperature_span_is_reported() -> None:
    observations = [
        observation("density_cm3", temperature_k=77.0, condition_id="c1"),
        observation(
            "generalized_einstein_factor",
            temperature_k=150.0,
            condition_id="c2",
        ),
    ]
    report = analyze_kane_validation_design(observations, nominal_parameters())
    assert report.unique_temperature_count == 2
    assert report.observation_count == 2


def test_empty_material_evidence_is_rejected_with_explicit_requirements() -> None:
    report = assess_kane_material_evidence([])
    assert not report.accepted
    assert "at_least_three_independent_points" in report.missing_requirements
    assert "absolute_density_scale_observable" in report.missing_requirements
    assert "scale_free_or_matched_shape_observable" in report.missing_requirements


def test_density_only_evidence_fails_shape_requirement() -> None:
    evidence = [
        evidence_point("a", "source-a", "c1", "density_cm3", temperature_k=77.0),
        evidence_point("b", "source-b", "c2", "density_cm3", temperature_k=150.0),
        evidence_point("c", "source-a", "c3", "density_cm3", temperature_k=200.0),
    ]
    report = assess_kane_material_evidence(evidence)
    assert not report.accepted
    assert "scale_free_or_matched_shape_observable" in report.missing_requirements


def test_matched_density_and_compressibility_count_as_shape_evidence() -> None:
    evidence = [
        evidence_point("a", "source-a", "c1", "density_cm3", temperature_k=77.0),
        evidence_point(
            "b",
            "source-b",
            "c1",
            "compressibility_cm3_per_ev",
            temperature_k=77.0,
        ),
        evidence_point("c", "source-a", "c2", "density_cm3", temperature_k=150.0),
    ]
    report = assess_kane_material_evidence(evidence)
    assert report.accepted
    assert report.has_scale_free_or_matched_shape_observable


def test_complete_three_point_two_source_design_passes_metadata_policy() -> None:
    evidence = [
        evidence_point("a", "source-a", "c1", "density_cm3", temperature_k=77.0),
        evidence_point(
            "b",
            "source-b",
            "c1",
            "generalized_einstein_factor",
            temperature_k=77.0,
        ),
        evidence_point("c", "source-a", "c2", "density_cm3", temperature_k=150.0),
    ]
    report = assess_kane_material_evidence(evidence)
    assert report.accepted
    assert report.evidence_count == 3
    assert report.independent_provenance_count == 2
    assert report.unique_temperature_count == 2
    assert report.missing_requirements == ()


def test_unknown_eta_without_validated_neutrality_is_rejected() -> None:
    evidence = [
        evidence_point(
            "a",
            "source-a",
            "c1",
            "density_cm3",
            temperature_k=77.0,
            eta_known=False,
        ),
        evidence_point(
            "b",
            "source-b",
            "c1",
            "generalized_einstein_factor",
            temperature_k=77.0,
        ),
        evidence_point("c", "source-a", "c2", "density_cm3", temperature_k=150.0),
    ]
    report = assess_kane_material_evidence(evidence)
    assert not report.accepted
    assert "known_eta_or_validated_neutrality" in report.missing_requirements


def test_validated_neutrality_can_supply_the_chemical_potential_basis() -> None:
    evidence = [
        evidence_point(
            "a",
            "source-a",
            "c1",
            "density_cm3",
            temperature_k=77.0,
            eta_known=False,
            validated_neutrality_model=True,
        ),
        evidence_point(
            "b",
            "source-b",
            "c1",
            "generalized_einstein_factor",
            temperature_k=77.0,
        ),
        evidence_point("c", "source-a", "c2", "density_cm3", temperature_k=150.0),
    ]
    assert assess_kane_material_evidence(evidence).accepted


def test_non_material_or_non_independent_points_are_rejected() -> None:
    evidence = [
        evidence_point(
            "a",
            "source-a",
            "c1",
            "density_cm3",
            temperature_k=77.0,
            material_specific=False,
        ),
        evidence_point(
            "b",
            "source-b",
            "c1",
            "generalized_einstein_factor",
            temperature_k=77.0,
            independent_or_primary=False,
        ),
        evidence_point("c", "source-a", "c2", "density_cm3", temperature_k=150.0),
    ]
    report = assess_kane_material_evidence(evidence)
    assert not report.accepted
    assert "all_points_hgcdte_specific" in report.missing_requirements
    assert "all_points_primary_or_independent" in report.missing_requirements
