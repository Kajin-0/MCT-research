"""Validation-design tools for the project-defined simplified Kane closure.

This module does not fit HgCdTe material parameters.  It answers two narrower
Phase 1C questions:

1. whether a proposed set of positive observables locally identifies the
   simplified-Kane scale ``N_*`` and nonparabolicity ``alpha``; and
2. whether a set of external evidence records satisfies the declared minimum
   provenance and coverage requirements for a future material-validation gate.

A full-rank synthetic design is not material validation.  Material prediction
remains blocked until accepted HgCdTe evidence is supplied.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Literal, Sequence

import numpy as np
from numpy.typing import NDArray

from .project_kane_statistics import evaluate_simplified_kane_statistics

ObservationKind = Literal[
    "density_cm3",
    "compressibility_cm3_per_ev",
    "generalized_einstein_factor",
]

_ABSOLUTE_KINDS = frozenset({"density_cm3", "compressibility_cm3_per_ev"})
_SCALE_FREE_KINDS = frozenset({"generalized_einstein_factor"})
_VALID_KINDS = _ABSOLUTE_KINDS | _SCALE_FREE_KINDS


@dataclass(frozen=True)
class KaneParameterPoint:
    """Positive nominal parameters used only for local design analysis."""

    parabolic_density_scale_cm3: float
    nonparabolicity_ev_inverse: float

    def __post_init__(self) -> None:
        scale = float(self.parabolic_density_scale_cm3)
        alpha = float(self.nonparabolicity_ev_inverse)
        if not isfinite(scale) or scale <= 0.0:
            raise ValueError("parabolic_density_scale_cm3 must be finite and positive")
        if not isfinite(alpha) or alpha <= 0.0:
            raise ValueError(
                "nonparabolicity_ev_inverse must be finite and positive for "
                "log-sensitivity analysis"
            )
        object.__setattr__(self, "parabolic_density_scale_cm3", scale)
        object.__setattr__(self, "nonparabolicity_ev_inverse", alpha)


@dataclass(frozen=True)
class KaneValidationObservation:
    """One proposed positive observable for local identifiability analysis.

    ``relative_standard_uncertainty`` is used only as a row weight.  The design
    analysis does not treat synthetic uncertainties as material evidence.
    """

    kind: ObservationKind
    eta: float
    temperature_k: float
    relative_standard_uncertainty: float = 1.0
    condition_id: str = "unspecified"

    def __post_init__(self) -> None:
        if self.kind not in _VALID_KINDS:
            raise ValueError(f"unsupported observation kind: {self.kind}")
        eta = float(self.eta)
        temperature = float(self.temperature_k)
        uncertainty = float(self.relative_standard_uncertainty)
        if not isfinite(eta):
            raise ValueError("eta must be finite")
        if not isfinite(temperature) or temperature <= 0.0:
            raise ValueError("temperature_k must be finite and positive")
        if not isfinite(uncertainty) or uncertainty <= 0.0:
            raise ValueError(
                "relative_standard_uncertainty must be finite and positive"
            )
        if not str(self.condition_id).strip():
            raise ValueError("condition_id must be non-empty")
        object.__setattr__(self, "eta", eta)
        object.__setattr__(self, "temperature_k", temperature)
        object.__setattr__(self, "relative_standard_uncertainty", uncertainty)
        object.__setattr__(self, "condition_id", str(self.condition_id))


@dataclass(frozen=True)
class KaneIdentifiabilityReport:
    """Weighted log-sensitivity and rank diagnostics for two parameters."""

    sensitivity_matrix: NDArray[np.float64]
    singular_values: NDArray[np.float64]
    fisher_information: NDArray[np.float64]
    rank: int
    full_rank: bool
    condition_number: float
    observation_count: int
    unique_temperature_count: int
    observation_kinds: tuple[str, ...]


@dataclass(frozen=True)
class KaneMaterialEvidencePoint:
    """Metadata contract for one future HgCdTe validation point.

    The value is intentionally not interpreted here.  This structure records
    whether the point is usable for an eventual material gate.
    """

    evidence_id: str
    provenance_group: str
    condition_id: str
    observable_kind: ObservationKind
    composition: float
    temperature_k: float
    value: float
    standard_uncertainty: float
    material_specific: bool
    independent_or_primary: bool
    eta_known: bool = False
    validated_neutrality_model: bool = False

    def __post_init__(self) -> None:
        if self.observable_kind not in _VALID_KINDS:
            raise ValueError(f"unsupported observation kind: {self.observable_kind}")
        for name, value in (
            ("composition", self.composition),
            ("temperature_k", self.temperature_k),
            ("value", self.value),
            ("standard_uncertainty", self.standard_uncertainty),
        ):
            if not isfinite(float(value)):
                raise ValueError(f"{name} must be finite")
        if not 0.0 <= float(self.composition) <= 1.0:
            raise ValueError("composition must lie in [0, 1]")
        if float(self.temperature_k) <= 0.0:
            raise ValueError("temperature_k must be positive")
        if float(self.value) <= 0.0:
            raise ValueError("value must be positive")
        if float(self.standard_uncertainty) <= 0.0:
            raise ValueError("standard_uncertainty must be positive")
        for name in ("evidence_id", "provenance_group", "condition_id"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class KaneMaterialEvidenceReport:
    """Result of the declared minimum material-evidence policy."""

    accepted: bool
    evidence_count: int
    independent_provenance_count: int
    unique_temperature_count: int
    has_absolute_scale_observable: bool
    has_scale_free_or_matched_shape_observable: bool
    all_points_material_specific: bool
    all_points_independent_or_primary: bool
    all_points_have_chemical_potential_basis: bool
    missing_requirements: tuple[str, ...]


def _predict_observation(
    observation: KaneValidationObservation,
    parameters: KaneParameterPoint,
) -> float:
    state = evaluate_simplified_kane_statistics(
        eta=observation.eta,
        temperature_k=observation.temperature_k,
        parabolic_density_scale_cm3=parameters.parabolic_density_scale_cm3,
        nonparabolicity_ev_inverse=parameters.nonparabolicity_ev_inverse,
    ).carrier
    if observation.kind == "density_cm3":
        return float(state.density_cm3)
    if observation.kind == "compressibility_cm3_per_ev":
        return float(state.compressibility_cm3_per_ev)
    return float(state.generalized_einstein_factor)


def kane_log_sensitivity_matrix(
    observations: Sequence[KaneValidationObservation],
    parameters: KaneParameterPoint,
    *,
    log_step: float = 1.0e-4,
) -> NDArray[np.float64]:
    """Return weighted derivatives of log observables with respect to log parameters.

    The columns correspond to ``log(N_*)`` and ``log(alpha)``.  Each row is
    divided by the declared relative standard uncertainty for that observation.
    """

    if not observations:
        raise ValueError("at least one observation is required")
    step = float(log_step)
    if not isfinite(step) or not 1.0e-7 <= step <= 5.0e-2:
        raise ValueError("log_step must be finite and lie in [1e-7, 5e-2]")

    base_scale = parameters.parabolic_density_scale_cm3
    base_alpha = parameters.nonparabolicity_ev_inverse
    plus_scale = KaneParameterPoint(base_scale * exp(step), base_alpha)
    minus_scale = KaneParameterPoint(base_scale * exp(-step), base_alpha)
    plus_alpha = KaneParameterPoint(base_scale, base_alpha * exp(step))
    minus_alpha = KaneParameterPoint(base_scale, base_alpha * exp(-step))

    matrix = np.empty((len(observations), 2), dtype=float)
    for row, observation in enumerate(observations):
        weight = 1.0 / observation.relative_standard_uncertainty
        scale_derivative = (
            np.log(_predict_observation(observation, plus_scale))
            - np.log(_predict_observation(observation, minus_scale))
        ) / (2.0 * step)
        alpha_derivative = (
            np.log(_predict_observation(observation, plus_alpha))
            - np.log(_predict_observation(observation, minus_alpha))
        ) / (2.0 * step)
        matrix[row, 0] = weight * scale_derivative
        matrix[row, 1] = weight * alpha_derivative
    if not np.all(np.isfinite(matrix)):
        raise FloatingPointError("non-finite Kane sensitivity matrix")
    return matrix


def analyze_kane_validation_design(
    observations: Sequence[KaneValidationObservation],
    parameters: KaneParameterPoint,
    *,
    log_step: float = 1.0e-4,
    relative_rank_tolerance: float = 1.0e-10,
) -> KaneIdentifiabilityReport:
    """Evaluate local two-parameter rank and conditioning."""

    tolerance = float(relative_rank_tolerance)
    if not isfinite(tolerance) or not 0.0 < tolerance < 1.0:
        raise ValueError("relative_rank_tolerance must lie in (0, 1)")
    matrix = kane_log_sensitivity_matrix(
        observations,
        parameters,
        log_step=log_step,
    )
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    largest = float(singular_values[0]) if singular_values.size else 0.0
    threshold = tolerance * largest
    rank = int(np.count_nonzero(singular_values > threshold)) if largest > 0.0 else 0
    full_rank = rank == 2
    if full_rank:
        condition_number = float(singular_values[0] / singular_values[-1])
    else:
        condition_number = float("inf")
    return KaneIdentifiabilityReport(
        sensitivity_matrix=matrix,
        singular_values=singular_values.astype(float),
        fisher_information=(matrix.T @ matrix).astype(float),
        rank=rank,
        full_rank=full_rank,
        condition_number=condition_number,
        observation_count=len(observations),
        unique_temperature_count=len({item.temperature_k for item in observations}),
        observation_kinds=tuple(item.kind for item in observations),
    )


def _has_matched_density_compressibility_pair(
    evidence: Sequence[KaneMaterialEvidencePoint],
) -> bool:
    by_condition: dict[str, set[str]] = {}
    for point in evidence:
        by_condition.setdefault(point.condition_id, set()).add(point.observable_kind)
    return any(
        {"density_cm3", "compressibility_cm3_per_ev"}.issubset(kinds)
        for kinds in by_condition.values()
    )


def assess_kane_material_evidence(
    evidence: Sequence[KaneMaterialEvidencePoint],
    *,
    minimum_points: int = 3,
    minimum_provenance_groups: int = 2,
    minimum_temperatures: int = 2,
) -> KaneMaterialEvidenceReport:
    """Apply the declared minimum evidence policy without fitting parameters."""

    if minimum_points < 1 or minimum_provenance_groups < 1 or minimum_temperatures < 1:
        raise ValueError("minimum evidence counts must be positive")
    points = tuple(evidence)
    provenance_count = len({point.provenance_group for point in points})
    temperature_count = len({point.temperature_k for point in points})
    has_absolute = any(point.observable_kind in _ABSOLUTE_KINDS for point in points)
    has_shape = any(point.observable_kind in _SCALE_FREE_KINDS for point in points)
    has_shape = has_shape or _has_matched_density_compressibility_pair(points)
    all_material = bool(points) and all(point.material_specific for point in points)
    all_independent = bool(points) and all(
        point.independent_or_primary for point in points
    )
    all_basis = bool(points) and all(
        point.eta_known or point.validated_neutrality_model for point in points
    )

    missing: list[str] = []
    if len(points) < minimum_points:
        missing.append("at_least_three_independent_points")
    if provenance_count < minimum_provenance_groups:
        missing.append("at_least_two_provenance_groups")
    if temperature_count < minimum_temperatures:
        missing.append("temperature_span")
    if not has_absolute:
        missing.append("absolute_density_scale_observable")
    if not has_shape:
        missing.append("scale_free_or_matched_shape_observable")
    if not all_material:
        missing.append("all_points_hgcdte_specific")
    if not all_independent:
        missing.append("all_points_primary_or_independent")
    if not all_basis:
        missing.append("known_eta_or_validated_neutrality")

    return KaneMaterialEvidenceReport(
        accepted=not missing,
        evidence_count=len(points),
        independent_provenance_count=provenance_count,
        unique_temperature_count=temperature_count,
        has_absolute_scale_observable=has_absolute,
        has_scale_free_or_matched_shape_observable=has_shape,
        all_points_material_specific=all_material,
        all_points_independent_or_primary=all_independent,
        all_points_have_chemical_potential_basis=all_basis,
        missing_requirements=tuple(missing),
    )
