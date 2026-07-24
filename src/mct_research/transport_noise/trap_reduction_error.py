"""Reduction-error gate for constant-coefficient trap elimination.

The exact steady elimination of one reversible trap level has the form

    U_exact = kappa_eff(N, P) * (N*P - K_eq),

where kappa_eff is positive and state dependent. This module quantifies the
error made by replacing it with a constant coefficient evaluated at a declared
reference state. It provides an exact symmetric logarithmic state-domain
radius for a requested relative pair-rate tolerance and a conservative radius
across a finite declared uncertainty ensemble.

The module is dimensionless and architecture-only. It does not establish a
material-specific HgCdTe validity domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .trap_kinetics_prototype import (
    ReversibleTrapParameters,
    effective_mass_action_coefficient,
    trap_eliminated_pair_rate,
)


@dataclass(frozen=True)
class ConstantKappaReference:
    """Reference state and frozen eliminated pair coefficient."""

    electron_density: float
    hole_density: float
    coefficient: float


@dataclass(frozen=True)
class ReductionErrorMetrics:
    """Exact/reduced rates and frozen-coefficient relative error."""

    exact_coefficient: NDArray[np.float64]
    reduced_coefficient: float
    coefficient_relative_error: NDArray[np.float64]
    exact_pair_rate: NDArray[np.float64]
    reduced_pair_rate: NDArray[np.float64]
    absolute_pair_rate_error: NDArray[np.float64]


@dataclass(frozen=True)
class ScenarioRadius:
    """One uncertainty scenario and its exact admissible log-radius."""

    name: str
    radius: float
    reference: ConstantKappaReference


@dataclass(frozen=True)
class ConservativeReductionBoundary:
    """Worst-case symmetric log-domain boundary over declared scenarios."""

    tolerance: float
    conservative_radius: float
    minimum_density_factor: float
    maximum_density_factor: float
    controlling_scenario: str
    scenarios: tuple[ScenarioRadius, ...]


def constant_kappa_reference(
    *,
    trap_parameters: ReversibleTrapParameters,
    electron_density: float | None = None,
    hole_density: float | None = None,
) -> ConstantKappaReference:
    """Freeze ``kappa_eff`` at a positive reference state."""

    electron = (
        trap_parameters.equilibrium_electron_density
        if electron_density is None
        else float(electron_density)
    )
    hole = (
        trap_parameters.equilibrium_hole_density
        if hole_density is None
        else float(hole_density)
    )
    if not isfinite(electron) or electron <= 0.0:
        raise ValueError("reference electron density must be finite and positive")
    if not isfinite(hole) or hole <= 0.0:
        raise ValueError("reference hole density must be finite and positive")
    coefficient = float(
        effective_mass_action_coefficient(
            electron,
            hole,
            trap_parameters=trap_parameters,
        )
    )
    if not isfinite(coefficient) or coefficient < 0.0:
        raise ValueError("reference coefficient must be finite and non-negative")
    return ConstantKappaReference(
        electron_density=electron,
        hole_density=hole,
        coefficient=coefficient,
    )


def constant_kappa_pair_rate(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
    reference: ConstantKappaReference,
) -> float | NDArray[np.float64]:
    """Evaluate the frozen-coefficient mass-action reduction."""

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    if electron.shape != hole.shape:
        raise ValueError("electron_density and hole_density must have equal shape")
    if not np.all(np.isfinite(electron)) or not np.all(np.isfinite(hole)):
        raise ValueError("carrier densities must contain only finite values")
    if np.any(electron <= 0.0) or np.any(hole <= 0.0):
        raise ValueError("carrier densities must be positive")
    result = reference.coefficient * (
        electron * hole - trap_parameters.equilibrium_product
    )
    if result.ndim == 0:
        return float(result)
    return result


def reduction_error_metrics(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
    reference: ConstantKappaReference,
) -> ReductionErrorMetrics:
    """Compare exact steady trap elimination with frozen ``kappa``.

    Away from ``N*P=K_eq``, the pair-rate relative error equals
    ``|kappa_0/kappa_eff - 1|`` because the exact and reduced rates share the
    same mass-action numerator. At detailed balance both rates vanish, so the
    coefficient ratio remains the well-defined limiting diagnostic.
    """

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    if electron.shape != hole.shape:
        raise ValueError("electron_density and hole_density must have equal shape")
    exact_coefficient = np.asarray(
        effective_mass_action_coefficient(
            electron,
            hole,
            trap_parameters=trap_parameters,
        ),
        dtype=float,
    )
    if reference.coefficient == 0.0:
        relative = np.zeros_like(exact_coefficient)
    else:
        relative = np.abs(reference.coefficient / exact_coefficient - 1.0)
    exact_rate = np.asarray(
        trap_eliminated_pair_rate(
            electron,
            hole,
            trap_parameters=trap_parameters,
        ),
        dtype=float,
    )
    reduced_rate = np.asarray(
        constant_kappa_pair_rate(
            electron,
            hole,
            trap_parameters=trap_parameters,
            reference=reference,
        ),
        dtype=float,
    )
    return ReductionErrorMetrics(
        exact_coefficient=exact_coefficient,
        reduced_coefficient=reference.coefficient,
        coefficient_relative_error=relative,
        exact_pair_rate=exact_rate,
        reduced_pair_rate=reduced_rate,
        absolute_pair_rate_error=np.abs(reduced_rate - exact_rate),
    )


def symmetric_log_domain_radius(
    *,
    trap_parameters: ReversibleTrapParameters,
    tolerance: float,
    reference: ConstantKappaReference | None = None,
) -> float:
    """Return the exact largest symmetric log-density radius.

    The domain is

    ``N=N0 exp(xi_n)``, ``P=P0 exp(xi_p)``, with
    ``|xi_n|<=r`` and ``|xi_p|<=r``.

    The eliminated denominator is positive and affine in ``N`` and ``P``;
    therefore its extrema occur at the two equal-sign corners. The returned
    radius is the largest ``r`` for which
    ``|kappa_0/kappa_eff - 1| <= tolerance`` everywhere in the rectangle.
    """

    error = float(tolerance)
    if not isfinite(error) or not 0.0 < error < 1.0:
        raise ValueError("tolerance must be finite and strictly between 0 and 1")
    frozen = (
        constant_kappa_reference(trap_parameters=trap_parameters)
        if reference is None
        else reference
    )
    carrier_part = (
        trap_parameters.electron_capture_coefficient
        * frozen.electron_density
        + trap_parameters.hole_capture_coefficient * frozen.hole_density
    )
    emission_part = (
        trap_parameters.electron_emission_coefficient
        + trap_parameters.hole_emission_coefficient
    )
    if carrier_part <= 0.0:
        return float("inf")
    denominator0 = carrier_part + emission_part

    maximum_ratio = (
        denominator0 * (1.0 + error) - emission_part
    ) / carrier_part
    upper_radius = 0.0 if maximum_ratio <= 1.0 else log(maximum_ratio)

    minimum_ratio = (
        denominator0 * (1.0 - error) - emission_part
    ) / carrier_part
    lower_radius = (
        float("inf") if minimum_ratio <= 0.0 else -log(minimum_ratio)
    )
    return min(upper_radius, lower_radius)


def corner_coefficient_errors(
    *,
    trap_parameters: ReversibleTrapParameters,
    radius: float,
    reference: ConstantKappaReference | None = None,
) -> NDArray[np.float64]:
    """Return frozen-coefficient relative errors at four log-domain corners."""

    value = float(radius)
    if not isfinite(value) or value < 0.0:
        raise ValueError("radius must be finite and non-negative")
    frozen = (
        constant_kappa_reference(trap_parameters=trap_parameters)
        if reference is None
        else reference
    )
    factors = np.exp(np.array([-value, value]))
    electron, hole = np.meshgrid(
        frozen.electron_density * factors,
        frozen.hole_density * factors,
        indexing="ij",
    )
    metrics = reduction_error_metrics(
        electron,
        hole,
        trap_parameters=trap_parameters,
        reference=frozen,
    )
    return metrics.coefficient_relative_error


def conservative_reduction_boundary(
    scenarios: Iterable[tuple[str, ReversibleTrapParameters]],
    *,
    tolerance: float,
) -> ConservativeReductionBoundary:
    """Return the worst exact radius across a finite declared ensemble."""

    records: list[ScenarioRadius] = []
    names: set[str] = set()
    for name, parameters in scenarios:
        label = str(name).strip()
        if not label:
            raise ValueError("scenario names must be non-empty")
        if label in names:
            raise ValueError("scenario names must be unique")
        names.add(label)
        reference = constant_kappa_reference(trap_parameters=parameters)
        radius = symmetric_log_domain_radius(
            trap_parameters=parameters,
            tolerance=tolerance,
            reference=reference,
        )
        records.append(
            ScenarioRadius(name=label, radius=radius, reference=reference)
        )
    if not records:
        raise ValueError("at least one scenario is required")
    controlling = min(records, key=lambda record: record.radius)
    return ConservativeReductionBoundary(
        tolerance=float(tolerance),
        conservative_radius=controlling.radius,
        minimum_density_factor=float(np.exp(-controlling.radius)),
        maximum_density_factor=float(np.exp(controlling.radius)),
        controlling_scenario=controlling.name,
        scenarios=tuple(records),
    )
