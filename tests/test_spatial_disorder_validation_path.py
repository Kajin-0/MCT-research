from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    QualificationClass,
    ValidationCandidate,
    qualify_validation_candidate,
    qualify_validation_portfolio,
)
from tools.build_spatial_disorder_validation_path_reference import (
    build_reference,
    candidate_records,
)


def _candidate(**overrides) -> ValidationCandidate:
    values = dict(
        source_id="direct",
        citation="Controlled numerical multiresolution map",
        doi=None,
        record_scope="original numerical arrays and instrument record",
        same_specimen=EvidenceState.CONFIRMED,
        same_spatial_region=EvidenceState.CONFIRMED,
        numerical_data_available=EvidenceState.CONFIRMED,
        independent_effective_scale_count=3,
        reusable_high_resolution_map=EvidenceState.ABSENT,
        declared_filterable_scale_count=0,
        kernel_characterized=EvidenceState.CONFIRMED,
        spatial_registration=EvidenceState.CONFIRMED,
        thickness_characterized=EvidenceState.CONFIRMED,
        depth_model_declared=EvidenceState.CONFIRMED,
        uncertainty_characterized=EvidenceState.CONFIRMED,
        observable_defined=EvidenceState.CONFIRMED,
        preprocessing_declared=EvidenceState.CONFIRMED,
        modality_count=1,
        spatial_map_reported=EvidenceState.CONFIRMED,
        rendered_figure_available=EvidenceState.CONFIRMED,
        notes=(),
    )
    values.update(overrides)
    return ValidationCandidate(**values)


def test_three_measured_scales_qualify_for_direct_validation() -> None:
    result = qualify_validation_candidate(_candidate())
    assert result.qualification is (
        QualificationClass.DIRECT_MULTIRESOLUTION_VALIDATION
    )
    assert result.direct_validation_ready is True
    assert result.direct_route == "independent_measured_scales"
    assert result.missing_direct_requirements == ()


def test_reusable_high_resolution_map_is_second_direct_route() -> None:
    result = qualify_validation_candidate(
        _candidate(
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.CONFIRMED,
            declared_filterable_scale_count=3,
        )
    )
    assert result.direct_validation_ready is True
    assert result.direct_route == "reusable_high_resolution_map"


def test_two_modalities_at_one_scale_are_not_multiresolution() -> None:
    result = qualify_validation_candidate(
        _candidate(
            source_id="multimodal",
            independent_effective_scale_count=1,
            modality_count=2,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
        )
    )
    assert result.qualification is QualificationClass.CROSS_MODALITY_CONTEXT
    assert result.direct_validation_ready is False
    assert "three_effective_scales_or_reusable_map" in (
        result.missing_direct_requirements
    )
    assert any(
        "modality count" in item for item in result.prohibited_uses
    )


def test_single_scale_numerical_map_has_limited_benchmark_use() -> None:
    result = qualify_validation_candidate(
        _candidate(
            source_id="single_scale",
            same_spatial_region=EvidenceState.UNKNOWN,
            independent_effective_scale_count=1,
            spatial_registration=EvidenceState.NOT_APPLICABLE,
        )
    )
    assert result.qualification is (
        QualificationClass.SINGLE_SCALE_SPATIAL_BENCHMARK
    )
    assert result.direct_validation_ready is False
    assert any("one-scale" in item for item in result.permitted_uses)


def test_rendered_map_without_arrays_is_figure_benchmark_only() -> None:
    result = qualify_validation_candidate(
        _candidate(
            source_id="figure",
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            kernel_characterized=EvidenceState.ABSENT,
            uncertainty_characterized=EvidenceState.ABSENT,
        )
    )
    assert result.qualification is (
        QualificationClass.SOURCE_BOUNDED_FIGURE_BENCHMARK
    )
    assert any("original numerical data" in item for item in result.prohibited_uses)


def test_unretrieved_record_is_not_qualifiable() -> None:
    candidate = _candidate(
        source_id="abstract_only",
        same_specimen=EvidenceState.UNKNOWN,
        same_spatial_region=EvidenceState.NOT_RETRIEVED,
        numerical_data_available=EvidenceState.NOT_RETRIEVED,
        independent_effective_scale_count=0,
        reusable_high_resolution_map=EvidenceState.NOT_RETRIEVED,
        kernel_characterized=EvidenceState.NOT_RETRIEVED,
        spatial_registration=EvidenceState.NOT_RETRIEVED,
        thickness_characterized=EvidenceState.UNKNOWN,
        depth_model_declared=EvidenceState.UNKNOWN,
        uncertainty_characterized=EvidenceState.UNKNOWN,
        observable_defined=EvidenceState.UNKNOWN,
        preprocessing_declared=EvidenceState.NOT_RETRIEVED,
        modality_count=4,
        spatial_map_reported=EvidenceState.UNKNOWN,
        rendered_figure_available=EvidenceState.UNKNOWN,
    )
    result = qualify_validation_candidate(candidate)
    assert result.qualification is QualificationClass.NOT_QUALIFIABLE
    assert result.direct_validation_ready is False
    assert "numerical_data_available:not_retrieved" in (
        result.blocking_evidence_states
    )


def test_missing_metadata_produces_concrete_data_requests() -> None:
    result = qualify_validation_candidate(
        _candidate(
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.ABSENT,
            uncertainty_characterized=EvidenceState.ABSENT,
            thickness_characterized=EvidenceState.ABSENT,
            depth_model_declared=EvidenceState.ABSENT,
            preprocessing_declared=EvidenceState.ABSENT,
        )
    )
    joined = " ".join(result.required_data_request)
    assert "original numerical map" in joined
    assert "three calibrated effective scales" in joined
    assert "PSF" in joined
    assert "registration transform" in joined
    assert "covariance" in joined
    assert "thickness" in joined
    assert "preprocessing" in joined


def test_adjustable_aperture_without_sweep_does_not_qualify() -> None:
    chang = candidate_records()[0]
    result = qualify_validation_candidate(chang)
    assert chang.independent_effective_scale_count == 1
    assert result.direct_validation_ready is False
    assert result.qualification is (
        QualificationClass.SOURCE_BOUNDED_FIGURE_BENCHMARK
    )


def test_same_region_multimodal_source_is_context_not_scale_evidence() -> None:
    furstenberg = candidate_records()[1]
    result = qualify_validation_candidate(furstenberg)
    assert furstenberg.modality_count == 2
    assert furstenberg.independent_effective_scale_count == 1
    assert result.qualification is QualificationClass.CROSS_MODALITY_CONTEXT


def test_abstract_only_source_preserves_not_retrieved_state() -> None:
    ruzhevich = candidate_records()[2]
    result = qualify_validation_candidate(ruzhevich)
    assert ruzhevich.record_scope.endswith("full text not retrieved")
    assert result.qualification is QualificationClass.NOT_QUALIFIABLE
    assert "spatial_registration:not_retrieved" in result.blocking_evidence_states


def test_current_portfolio_is_external_data_blocked() -> None:
    decision = qualify_validation_portfolio(candidate_records())
    assert decision.status == "external_data_blocked"
    assert decision.direct_candidate_ids == ()
    assert len(decision.qualifications) == 3
    assert any("three calibrated" in item for item in decision.minimum_next_action)


def test_portfolio_with_direct_candidate_is_available() -> None:
    decision = qualify_validation_portfolio((_candidate(),))
    assert decision.status == "direct_validation_available"
    assert decision.direct_candidate_ids == ("direct",)


def test_portfolio_output_is_sorted_by_source_id() -> None:
    decision = qualify_validation_portfolio(
        (
            _candidate(source_id="zeta"),
            _candidate(source_id="alpha"),
        )
    )
    assert tuple(item.source_id for item in decision.qualifications) == (
        "alpha",
        "zeta",
    )


def test_duplicate_source_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="unique"):
        qualify_validation_portfolio((_candidate(), _candidate()))


def test_empty_portfolio_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least one"):
        qualify_validation_portfolio(())


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"source_id": ""}, "source_id"),
        ({"citation": ""}, "citation"),
        ({"record_scope": ""}, "record_scope"),
        ({"independent_effective_scale_count": -1}, "non-negative"),
        ({"declared_filterable_scale_count": -1}, "non-negative"),
        ({"modality_count": 0}, "positive"),
    ],
)
def test_invalid_candidate_fields_are_rejected(kwargs, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _candidate(**kwargs)


def test_reusable_map_requires_numerical_data() -> None:
    with pytest.raises(ValueError, match="numerical data"):
        _candidate(
            numerical_data_available=EvidenceState.ABSENT,
            reusable_high_resolution_map=EvidenceState.CONFIRMED,
            declared_filterable_scale_count=3,
        )


def test_filterable_scale_count_requires_reusable_map() -> None:
    with pytest.raises(ValueError, match="reusable"):
        _candidate(
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=3,
        )


def test_outputs_are_frozen() -> None:
    candidate = _candidate()
    result = qualify_validation_candidate(candidate)
    decision = qualify_validation_portfolio((candidate,))
    with pytest.raises(FrozenInstanceError):
        candidate.source_id = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.source_id = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        decision.status = "changed"  # type: ignore[misc]


def test_reference_has_expected_exact_classifications() -> None:
    reference = build_reference()
    assert reference["status"] == "external_data_blocked"
    assert reference["direct_candidate_ids"] == []
    by_source = {
        item["source_id"]: item["qualification"]
        for item in reference["qualifications"]
    }
    assert by_source == {
        "chang_2005_infrared_mapping": (
            "source_bounded_figure_benchmark"
        ),
        "furstenberg_2005_pl_transmission_mapping": (
            "cross_modality_context"
        ),
        "ruzhevich_2024_optical_microscopic_disorder": (
            "not_qualifiable_from_available_record"
        ),
    }
    headline = reference["headline"]
    assert headline["direct_validation_candidate_count"] == 0
    assert "data-blocked" in headline["decision"]
