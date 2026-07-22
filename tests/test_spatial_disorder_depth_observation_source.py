from __future__ import annotations

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    QualificationClass,
    qualify_validation_candidate,
)
from tools.build_spatial_disorder_depth_observation_source_reference import (
    build_reference,
    candidate_records,
)


def _records_by_id():
    return {item.source_id: item for item in candidate_records()}


def test_ariel_1995_is_depth_observation_context() -> None:
    ariel = _records_by_id()["ariel_1995_derivative_depth_grading"]
    result = qualify_validation_candidate(ariel)

    assert ariel.doi == "10.1063/1.113916"
    assert ariel.depth_profile_observation_model is EvidenceState.CONFIRMED
    assert ariel.independent_effective_scale_count == 1
    assert ariel.spatial_map_reported is EvidenceState.ABSENT
    assert result.qualification is (
        QualificationClass.DEPTH_OBSERVATION_MODEL_CONTEXT
    )
    assert result.direct_validation_ready is False


def test_ariel_method_chain_is_declared() -> None:
    ariel = _records_by_id()["ariel_1995_derivative_depth_grading"]
    notes = " ".join(ariel.notes)

    assert "Room-temperature FTIR" in notes
    assert "smoothed" in notes
    assert "first-derivative maximum" in notes
    assert "second derivative" in notes
    assert "Eg_min" in notes
    assert "Eg_max" in notes
    assert "Delta Eg = Eg_max - Eg_min" in notes
    assert "integral_0^d" in notes


def test_ariel_source_statistics_are_exactly_bounded() -> None:
    notes = " ".join(
        _records_by_id()["ariel_1995_derivative_depth_grading"].notes
    )

    assert "500 micrometres" in notes
    assert "10-25 micrometres" in notes
    assert "below 0.005 eV" in notes
    assert "approximately 0.02 eV" in notes
    assert "10-20 V/cm" in notes
    assert "around 30 V/cm" in notes
    assert "linear grading" in notes


def test_ariel_limitations_are_preserved() -> None:
    notes = " ".join(
        _records_by_id()["ariel_1995_derivative_depth_grading"].notes
    )

    assert "thicker than 15 micrometres" in notes
    assert "band nonparabolicity" in notes
    assert "Burstein-Moss shift" in notes
    assert "Excessive smoothing" in notes
    assert "do not provide precise numerical band-gap values" in notes
    assert "No lateral coordinates" in notes
    assert "aperture or PSF" in notes


def test_depth_grading_is_not_promoted_to_spatial_evidence() -> None:
    ariel = _records_by_id()["ariel_1995_derivative_depth_grading"]
    result = qualify_validation_candidate(ariel)

    assert ariel.same_spatial_region is EvidenceState.NOT_APPLICABLE
    assert ariel.spatial_registration is EvidenceState.NOT_APPLICABLE
    assert ariel.numerical_data_available is EvidenceState.ABSENT
    assert "three_effective_scales_or_reusable_map" in (
        result.missing_direct_requirements
    )
    assert any("through-thickness grading" in item for item in result.prohibited_uses)
    assert any("lateral correlation length" in item for item in result.prohibited_uses)


def test_reference_preserves_prior_benchmarks_and_adds_ariel() -> None:
    reference = build_reference()
    by_source = {
        item["source_id"]: item["qualification"]
        for item in reference["qualifications"]
    }

    assert reference["schema_version"] == "1.3"
    assert reference["status"] == "external_data_blocked"
    assert reference["direct_candidate_ids"] == []
    assert reference["partial_multiresolution_candidate_ids"] == [
        "gopal_1992_two_beam_transmission"
    ]
    assert len(by_source) == 12
    assert by_source["ariel_1995_derivative_depth_grading"] == (
        "depth_observation_model_context"
    )
    assert by_source["gopal_1992_two_beam_transmission"] == (
        "partial_multiresolution_benchmark"
    )
    assert by_source["phillips_2003_pixel_scale_absorption_mapping"] == (
        "source_bounded_figure_benchmark"
    )


def test_reference_records_depth_operator_headline_and_boundaries() -> None:
    reference = build_reference()
    headline = reference["headline"]
    boundaries = " ".join(reference["claim_boundaries"])

    assert headline["nearest_depth_observation_model_context"] == (
        "ariel_1995_derivative_depth_grading"
    )
    assert headline["depth_observation_temperature_k"] == 300.0
    assert headline["bulk_sample_thickness_micrometre"] == 500.0
    assert headline["epitaxial_layer_thickness_range_micrometre"] == [10.0, 25.0]
    assert headline["interface_grading_non_negligible_below_micrometre"] == 15.0
    assert headline["bulk_band_gap_variation_upper_bound_ev"] == 0.005
    assert headline["lpe_band_gap_variation_approximate_ev"] == 0.02
    assert headline["lpe_linear_grading_field_range_v_per_cm"] == [10.0, 20.0]
    assert headline["mocvd_linear_grading_field_approximate_v_per_cm"] == 30.0
    assert "through-thickness Delta Eg" in boundaries
    assert "one effective lateral measurement kernel" in boundaries
    assert "Smoothing and fringe filtering" in boundaries
    assert "15 micrometres" in boundaries
