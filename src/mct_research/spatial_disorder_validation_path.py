"""Qualification of external validation paths for R04 spatial disorder.

This module separates multiresolution evidence from merely multimodal,
spatially resolved, or depth-observation evidence. It is a source-readiness
protocol, not a scientific inference engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class EvidenceState(str, Enum):
    """Source-bounded state for one required evidence item."""

    CONFIRMED = "confirmed"
    ABSENT = "absent"
    UNKNOWN = "unknown"
    NOT_RETRIEVED = "not_retrieved"
    NOT_APPLICABLE = "not_applicable"


class QualificationClass(str, Enum):
    """Permitted uses of a candidate source."""

    DIRECT_MULTIRESOLUTION_VALIDATION = "direct_multiresolution_validation"
    PARTIAL_MULTIRESOLUTION_BENCHMARK = "partial_multiresolution_benchmark"
    SINGLE_SCALE_SPATIAL_BENCHMARK = "single_scale_spatial_benchmark"
    CROSS_MODALITY_CONTEXT = "cross_modality_context"
    SOURCE_BOUNDED_FIGURE_BENCHMARK = "source_bounded_figure_benchmark"
    DEPTH_OBSERVATION_MODEL_CONTEXT = "depth_observation_model_context"
    NOT_QUALIFIABLE = "not_qualifiable_from_available_record"


_DIRECT_REQUIREMENTS = (
    "same_specimen",
    "same_spatial_region",
    "numerical_data_available",
    "kernel_characterized",
    "spatial_registration",
    "thickness_characterized",
    "depth_model_declared",
    "uncertainty_characterized",
    "observable_defined",
    "preprocessing_declared",
)


@dataclass(frozen=True)
class ValidationCandidate:
    """Source-bounded evidence for one external validation candidate."""

    source_id: str
    citation: str
    doi: str | None
    record_scope: str
    same_specimen: EvidenceState
    same_spatial_region: EvidenceState
    numerical_data_available: EvidenceState
    independent_effective_scale_count: int
    reusable_high_resolution_map: EvidenceState
    declared_filterable_scale_count: int
    kernel_characterized: EvidenceState
    spatial_registration: EvidenceState
    thickness_characterized: EvidenceState
    depth_model_declared: EvidenceState
    uncertainty_characterized: EvidenceState
    observable_defined: EvidenceState
    preprocessing_declared: EvidenceState
    modality_count: int
    spatial_map_reported: EvidenceState
    rendered_figure_available: EvidenceState
    depth_profile_observation_model: EvidenceState = EvidenceState.NOT_APPLICABLE
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must be non-empty")
        if not self.citation.strip():
            raise ValueError("citation must be non-empty")
        if not self.record_scope.strip():
            raise ValueError("record_scope must be non-empty")
        if self.independent_effective_scale_count < 0:
            raise ValueError(
                "independent_effective_scale_count must be non-negative"
            )
        if self.declared_filterable_scale_count < 0:
            raise ValueError(
                "declared_filterable_scale_count must be non-negative"
            )
        if self.modality_count < 1:
            raise ValueError("modality_count must be positive")
        if (
            self.reusable_high_resolution_map is EvidenceState.CONFIRMED
            and self.numerical_data_available is not EvidenceState.CONFIRMED
        ):
            raise ValueError(
                "a reusable high-resolution map requires confirmed numerical data"
            )
        if (
            self.declared_filterable_scale_count > 0
            and self.reusable_high_resolution_map is not EvidenceState.CONFIRMED
        ):
            raise ValueError(
                "declared_filterable_scale_count requires a reusable "
                "high-resolution map"
            )


@dataclass(frozen=True)
class ValidationQualification:
    """Deterministic qualification decision for one candidate."""

    source_id: str
    qualification: QualificationClass
    direct_route: str | None
    direct_validation_ready: bool
    missing_direct_requirements: tuple[str, ...]
    blocking_evidence_states: tuple[str, ...]
    permitted_uses: tuple[str, ...]
    prohibited_uses: tuple[str, ...]
    required_data_request: tuple[str, ...]


@dataclass(frozen=True)
class ValidationPortfolioDecision:
    """Portfolio-level decision across a set of candidate sources."""

    status: str
    direct_candidate_ids: tuple[str, ...]
    partial_multiresolution_candidate_ids: tuple[str, ...]
    qualifications: tuple[ValidationQualification, ...]
    minimum_next_action: tuple[str, ...]


def _confirmed(candidate: ValidationCandidate, name: str) -> bool:
    return getattr(candidate, name) is EvidenceState.CONFIRMED


def _direct_route(candidate: ValidationCandidate) -> str | None:
    common_ready = all(
        _confirmed(candidate, name) for name in _DIRECT_REQUIREMENTS
    )
    if not common_ready:
        return None
    if candidate.independent_effective_scale_count >= 3:
        return "independent_measured_scales"
    if (
        candidate.reusable_high_resolution_map is EvidenceState.CONFIRMED
        and candidate.declared_filterable_scale_count >= 3
    ):
        return "reusable_high_resolution_map"
    return None


def _missing_direct_requirements(
    candidate: ValidationCandidate,
) -> tuple[str, ...]:
    missing = [
        name
        for name in _DIRECT_REQUIREMENTS
        if getattr(candidate, name) is not EvidenceState.CONFIRMED
    ]
    if (
        candidate.independent_effective_scale_count < 3
        and not (
            candidate.reusable_high_resolution_map is EvidenceState.CONFIRMED
            and candidate.declared_filterable_scale_count >= 3
        )
    ):
        missing.append("three_effective_scales_or_reusable_map")
    return tuple(missing)


def _blocking_states(candidate: ValidationCandidate) -> tuple[str, ...]:
    values: list[str] = []
    for name in _DIRECT_REQUIREMENTS:
        state = getattr(candidate, name)
        if state is not EvidenceState.CONFIRMED:
            values.append(f"{name}:{state.value}")
    return tuple(values)


def _required_request(
    candidate: ValidationCandidate,
    missing: tuple[str, ...],
) -> tuple[str, ...]:
    del candidate
    requests: list[str] = []
    if "numerical_data_available" in missing:
        requests.append(
            "Provide the original numerical map or spectra with coordinates; "
            "rendered figures are insufficient."
        )
    if "three_effective_scales_or_reusable_map" in missing:
        requests.append(
            "Provide the same registered region at three calibrated effective "
            "scales, or one numerical high-resolution map that may be filtered "
            "by at least three declared kernels."
        )
    if "kernel_characterized" in missing:
        requests.append(
            "Provide measured or reconstructable PSF, aperture, pixel, or "
            "scan-bin kernels for every scale."
        )
    if (
        "spatial_registration" in missing
        or "same_spatial_region" in missing
    ):
        requests.append(
            "Provide common coordinates or a registration transform proving "
            "that the scales observe the same region."
        )
    if "uncertainty_characterized" in missing:
        requests.append(
            "Provide repeats, pointwise uncertainty, or a covariance model "
            "sufficient to construct observation covariance."
        )
    if (
        "thickness_characterized" in missing
        or "depth_model_declared" in missing
    ):
        requests.append(
            "Provide specimen thickness and the depth-weighting or absorption "
            "model used by the observable."
        )
    if (
        "observable_defined" in missing
        or "preprocessing_declared" in missing
    ):
        requests.append(
            "Provide the exact observable definition and preprocessing or "
            "fitting chain."
        )
    if "same_specimen" in missing:
        requests.append(
            "Identify the specimen and preserve that identity across all records."
        )
    return tuple(dict.fromkeys(requests))


def qualify_validation_candidate(
    candidate: ValidationCandidate,
) -> ValidationQualification:
    """Classify one candidate without inferring beyond its evidence states."""

    route = _direct_route(candidate)
    missing = _missing_direct_requirements(candidate)
    if route is not None:
        qualification = QualificationClass.DIRECT_MULTIRESOLUTION_VALIDATION
        permitted = (
            "run R04 multiscale recovery and covariance-family closure tests",
            "construct the declared joint uncertainty envelope",
        )
        prohibited = (
            "claim universal covariance physics",
            "claim specimen inference beyond the declared data and model",
        )
    elif (
        candidate.same_specimen is EvidenceState.CONFIRMED
        and candidate.independent_effective_scale_count >= 2
        and (
            candidate.numerical_data_available is EvidenceState.CONFIRMED
            or candidate.rendered_figure_available is EvidenceState.CONFIRMED
        )
    ):
        qualification = QualificationClass.PARTIAL_MULTIRESOLUTION_BENCHMARK
        permitted = (
            "establish source-bounded qualitative dependence on probe scale",
            "define the missing third-scale, kernel, and uncertainty requirements",
        )
        prohibited = (
            "perform three-scale covariance-family closure",
            "recover specimen covariance parameters from rendered curves or nominal beam diameters",
            "treat two scales as direct multiresolution validation",
        )
    elif (
        candidate.modality_count >= 2
        and candidate.same_specimen is EvidenceState.CONFIRMED
        and candidate.same_spatial_region is EvidenceState.CONFIRMED
    ):
        qualification = QualificationClass.CROSS_MODALITY_CONTEXT
        permitted = (
            "compare modality-conditioned observables on the same region",
            "define a future registered multimodal experiment",
        )
        prohibited = (
            "treat modality count as probe-scale count",
            "recover correlation length from one effective lateral scale",
        )
    elif (
        candidate.numerical_data_available is EvidenceState.CONFIRMED
        and candidate.spatial_map_reported is EvidenceState.CONFIRMED
        and candidate.kernel_characterized is EvidenceState.CONFIRMED
    ):
        qualification = QualificationClass.SINGLE_SCALE_SPATIAL_BENCHMARK
        permitted = (
            "test one-scale forward prediction and map-sampling corrections",
        )
        prohibited = (
            "separately infer point variance and correlation length",
            "test covariance-family closure from fewer than three scales",
        )
    elif (
        candidate.rendered_figure_available is EvidenceState.CONFIRMED
        and candidate.spatial_map_reported is EvidenceState.CONFIRMED
    ):
        qualification = QualificationClass.SOURCE_BOUNDED_FIGURE_BENCHMARK
        permitted = (
            "audit qualitative map structure and published summary statistics",
            "perform explicitly source-bounded figure recoverability studies",
        )
        prohibited = (
            "represent digitized pixels as original numerical data",
            "perform direct multiresolution validation",
        )
    elif (
        candidate.depth_profile_observation_model is EvidenceState.CONFIRMED
        and candidate.same_specimen is EvidenceState.CONFIRMED
        and candidate.thickness_characterized is EvidenceState.CONFIRMED
        and candidate.depth_model_declared is EvidenceState.CONFIRMED
        and candidate.observable_defined is EvidenceState.CONFIRMED
        and candidate.preprocessing_declared is EvidenceState.CONFIRMED
    ):
        qualification = QualificationClass.DEPTH_OBSERVATION_MODEL_CONTEXT
        permitted = (
            "constrain a depth-averaged absorption observation operator and its preprocessing sensitivity",
            "separate through-thickness grading hypotheses from lateral spatial-disorder hypotheses",
        )
        prohibited = (
            "treat through-thickness grading as lateral covariance or probe-scale evidence",
            "infer lateral correlation length or claim direct multiresolution validation",
        )
    else:
        qualification = QualificationClass.NOT_QUALIFIABLE
        permitted = (
            "record the source and unresolved evidence state",
        )
        prohibited = (
            "perform quantitative R04 validation",
            "fill missing metadata by assumption",
        )

    return ValidationQualification(
        source_id=candidate.source_id,
        qualification=qualification,
        direct_route=route,
        direct_validation_ready=route is not None,
        missing_direct_requirements=missing,
        blocking_evidence_states=_blocking_states(candidate),
        permitted_uses=permitted,
        prohibited_uses=prohibited,
        required_data_request=_required_request(candidate, missing),
    )


def qualify_validation_portfolio(
    candidates: Iterable[ValidationCandidate],
) -> ValidationPortfolioDecision:
    """Return a deterministic portfolio decision sorted by source identifier."""

    ordered = tuple(sorted(candidates, key=lambda item: item.source_id))
    if not ordered:
        raise ValueError("at least one validation candidate is required")
    if len({item.source_id for item in ordered}) != len(ordered):
        raise ValueError("source_id values must be unique")
    qualifications = tuple(
        qualify_validation_candidate(item) for item in ordered
    )
    direct = tuple(
        item.source_id
        for item in qualifications
        if item.direct_validation_ready
    )
    partial = tuple(
        item.source_id
        for item in qualifications
        if item.qualification
        is QualificationClass.PARTIAL_MULTIRESOLUTION_BENCHMARK
    )
    if direct:
        status = "direct_validation_available"
        next_action = (
            "Freeze the selected source record and run the R04 joint model "
            "using its declared kernels, covariance, raster geometry, and "
            "observable chain.",
        )
    else:
        status = "external_data_blocked"
        if partial:
            next_action = (
                "Use the partial multiresolution source only as qualitative "
                "scale-dependence evidence; do not infer covariance parameters.",
                "Obtain its original numerical spectra or maps, measured kernels, "
                "uncertainty covariance, spatial registration, and a third scale, "
                "or obtain one numerical high-resolution map reusable under "
                "three declared kernels.",
            )
        else:
            next_action = (
                "Obtain one numerical same-region dataset at three calibrated "
                "effective scales, or one numerical high-resolution map reusable "
                "under three declared kernels.",
                "Require kernel metadata, spatial registration, thickness/depth "
                "model, uncertainty covariance, observable definition, and "
                "preprocessing provenance before inference.",
            )
    return ValidationPortfolioDecision(
        status=status,
        direct_candidate_ids=direct,
        partial_multiresolution_candidate_ids=partial,
        qualifications=qualifications,
        minimum_next_action=next_action,
    )
