from __future__ import annotations

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    QualificationClass,
    qualify_validation_candidate,
)
from tools.build_spatial_disorder_spatial_method_source_reference import (
    build_reference,
    candidate_records,
)


def _records_by_id():
    return {item.source_id: item for item in candidate_records()}


def test_ariel_1996_is_spatial_observation_method_context() -> None:
    ariel = _records_by_id()[
        "ariel_1996_same_wafer_differential_absorption"
    ]
    result = qualify_validation_candidate(ariel)

    assert ariel.doi is None
    assert ariel.spatial_point_observation_method is EvidenceState.CONFIRMED
    assert ariel.same_specimen is EvidenceState.CONFIRMED
    assert ariel.independent_effective_scale_count == 1
    assert result.qualification is (
        QualificationClass.SPATIAL_OBSERVATION_METHOD_CONTEXT
    )
    assert result.direct_validation_ready is False


def test_ariel_1996_abstract_method_facts_are_preserved() -> None:
    notes = " ".join(
        _records_by_id()[
            "ariel_1996_same_wafer_differential_absorption"
        ].notes
    )

    assert "room-temperature" in notes
    assert "interference fringes" in notes
    assert "high-frequency noise" in notes
    assert "8 micrometres" in notes
    assert "0.1 micrometre" in notes
    assert "differentiated twice" in notes
    assert "different points on the same HgCdTe wafer" in notes
    assert "lateral and transverse" in notes
    assert "0.5 meV" in notes


def test_ariel_1996_is_not_promoted_to_map_or_multiresolution() -> None:
    ariel = _records_by_id()[
        "ariel_1996_same_wafer_differential_absorption"
    ]
    result = qualify_validation_candidate(ariel)

    assert ariel.spatial_map_reported is EvidenceState.UNKNOWN
    assert ariel.kernel_characterized is EvidenceState.NOT_RETRIEVED
    assert ariel.numerical_data_available is EvidenceState.NOT_RETRIEVED
    assert ariel.spatial_registration is EvidenceState.UNKNOWN
    assert "three_effective_scales_or_reusable_map" in (
        result.missing_direct_requirements
    )
    assert any("calibrated raster" in item for item in result.prohibited_uses)
    assert any("method accuracy" in item for item in result.prohibited_uses)


def test_reference_preserves_prior_roles_and_adds_thirteenth_candidate() -> None:
    reference = build_reference()
    by_source = {
        item["source_id"]: item["qualification"]
        for item in reference["qualifications"]
    }

    assert reference["schema_version"] == "1.4"
    assert reference["status"] == "external_data_blocked"
    assert reference["direct_candidate_ids"] == []
    assert reference["partial_multiresolution_candidate_ids"] == [
        "gopal_1992_two_beam_transmission"
    ]
    assert len(by_source) == 13
    assert by_source[
        "ariel_1996_same_wafer_differential_absorption"
    ] == "spatial_observation_method_context"
    assert by_source["ariel_1995_derivative_depth_grading"] == (
        "depth_observation_model_context"
    )
    assert by_source["phillips_2003_pixel_scale_absorption_mapping"] == (
        "source_bounded_figure_benchmark"
    )


def test_reference_records_abstract_limits_without_guessing_doi() -> None:
    reference = build_reference()
    headline = reference["headline"]
    boundaries = " ".join(reference["claim_boundaries"])
    candidates = {
        item["source_id"]: item for item in reference["candidates"]
    }
    ariel = candidates["ariel_1996_same_wafer_differential_absorption"]

    assert headline["nearest_spatial_observation_method_context"] == (
        "ariel_1996_same_wafer_differential_absorption"
    )
    assert headline["minimum_reliable_layer_thickness_micrometre"] == 8.0
    assert headline["reported_thickness_accuracy_micrometre"] == 0.1
    assert headline["reported_band_gap_method_accuracy_mev"] == 0.5
    assert headline["same_wafer_multiple_positions_reported"] is True
    assert headline["reported_effective_lateral_scale_count"] == 1
    assert headline["spatial_method_doi_status"] == "unresolved_not_guessed"
    assert headline["price_boyd_review_doi"] == (
        "10.1088/0268-1242/8/6S/006"
    )
    assert headline["price_boyd_full_text_status"] == "not_retrieved"
    assert ariel["doi"] is None
    assert "spatial sampling intent" in boundaries
    assert "one effective lateral scale" in boundaries
    assert "not repeat uncertainty" in boundaries
    assert "unresolved DOI" in boundaries
