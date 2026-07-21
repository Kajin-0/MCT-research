"""Deterministic quadrature for bounded HgCdTe composition distributions.

The routines in this module propagate a declared Gaussian composition model,
conditioned on the physical interval ``0 <= x <= 1``, through a scalar signed-gap
law. They distinguish exact distributional moments from local Taylor
approximations and retain the probability that a critical-temperature crossing
is absent from a declared observation window.

The distribution is a metrology or specimen-state model supplied by the caller.
It is not inferred from an Urbach energy, photoluminescence linewidth, or nominal
composition label.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import erf, exp, pi, sqrt

import numpy as np
from numpy.typing import NDArray

from .distributional_gap import linearized_composition_gap_statistics
from .gap_models import GapValue, bracketed_root


@dataclass(frozen=True)
class GaussianGapMoments:
    """Exact quadrature moments of a bounded Gaussian composition model."""

    declared_mean_composition: float
    declared_composition_sigma: float
    effective_mean_composition: float
    effective_composition_sigma: float
    physical_interval_probability: float
    omitted_tail_probability: float
    temperature_k: float
    mean_gap_ev: float
    gap_sigma_ev: float
    gap_skewness: float
    negative_gap_probability: float
    near_zero_gap_probability: float
    positive_gap_probability: float
    linearized_mean_gap_ev: float
    linearized_gap_sigma_ev: float
    mean_approximation_error_ev: float
    sigma_approximation_error_ev: float
    quadrature_order: int


@dataclass(frozen=True)
class CriticalTemperatureDistribution:
    """Critical-temperature distribution over a bounded composition model.

    Temperature moments are conditional on exactly one crossing inside the
    declared interval. The corresponding probability must always be reported.
    """

    declared_mean_composition: float
    declared_composition_sigma: float
    effective_mean_composition: float
    effective_composition_sigma: float
    temperature_lower_k: float
    temperature_upper_k: float
    single_crossing_probability: float
    always_normal_probability: float
    always_inverted_probability: float
    multiple_crossing_probability: float
    unresolved_probability: float
    conditional_mean_temperature_k: float | None
    conditional_sigma_temperature_k: float | None
    conditional_skewness: float | None
    central_composition_critical_temperature_k: float | None
    linearized_sigma_temperature_k: float | None
    conditional_mean_shift_k: float | None
    sigma_approximation_error_k: float | None
    quadrature_order: int
    temperature_grid_size: int


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def _validate_distribution_inputs(
    mean_composition: float,
    composition_sigma: float,
) -> tuple[float, float]:
    mean = _finite_scalar("mean_composition", mean_composition)
    sigma = _finite_scalar("composition_sigma", composition_sigma)
    if not 0.0 <= mean <= 1.0:
        raise ValueError("mean_composition must lie in [0, 1]")
    if sigma < 0.0:
        raise ValueError("composition_sigma must be non-negative")
    return mean, sigma


def _bounded_gaussian_nodes(
    mean_composition: float,
    composition_sigma: float,
    *,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    float,
    float,
    float,
    float,
]:
    mean, sigma = _validate_distribution_inputs(mean_composition, composition_sigma)
    order = int(quadrature_order)
    z_limit = _finite_scalar("standard_deviation_limit", standard_deviation_limit)
    if order < 16:
        raise ValueError("quadrature_order must be at least 16")
    if z_limit <= 0.0:
        raise ValueError("standard_deviation_limit must be positive")

    if sigma == 0.0:
        return (
            np.asarray([mean], dtype=float),
            np.asarray([1.0], dtype=float),
            1.0,
            0.0,
            mean,
            0.0,
        )

    lower_z = (0.0 - mean) / sigma
    upper_z = (1.0 - mean) / sigma
    physical_probability = _normal_cdf(upper_z) - _normal_cdf(lower_z)
    if physical_probability <= 0.0:
        raise ValueError("bounded Gaussian has zero probability in [0, 1]")

    integration_lower = max(lower_z, -z_limit)
    integration_upper = min(upper_z, z_limit)
    if integration_lower >= integration_upper:
        raise ValueError("quadrature interval is empty")

    canonical_nodes, canonical_weights = np.polynomial.legendre.leggauss(order)
    half_width = 0.5 * (integration_upper - integration_lower)
    centre = 0.5 * (integration_upper + integration_lower)
    z_nodes = half_width * canonical_nodes + centre
    normal_density = np.exp(-0.5 * z_nodes**2) / sqrt(2.0 * pi)
    raw_weights = half_width * canonical_weights * normal_density
    integrated_probability = float(np.sum(raw_weights))
    if integrated_probability <= 0.0 or not np.isfinite(integrated_probability):
        raise ValueError("quadrature failed to resolve the bounded Gaussian")

    weights = np.asarray(raw_weights / integrated_probability, dtype=float)
    composition_nodes = np.asarray(mean + sigma * z_nodes, dtype=float)
    omitted_tail_probability = max(
        0.0,
        1.0 - integrated_probability / physical_probability,
    )
    effective_mean = float(np.sum(weights * composition_nodes))
    effective_variance = float(
        np.sum(weights * (composition_nodes - effective_mean) ** 2)
    )
    effective_sigma = sqrt(max(effective_variance, 0.0))
    return (
        composition_nodes,
        weights,
        physical_probability,
        omitted_tail_probability,
        effective_mean,
        effective_sigma,
    )


def _composition_roots(
    model: Callable[[float, float], GapValue],
    temperature_k: float,
    *,
    grid_size: int,
) -> list[float]:
    size = int(grid_size)
    if size < 33:
        raise ValueError("composition_root_grid_size must be at least 33")

    grid = np.linspace(0.0, 1.0, size)
    values = np.asarray([float(model(float(x), temperature_k)) for x in grid])
    if not np.all(np.isfinite(values)):
        raise ValueError("gap model must be finite on the composition grid")

    roots: list[float] = []
    for index in range(size - 1):
        left = float(grid[index])
        right = float(grid[index + 1])
        f_left = float(values[index])
        f_right = float(values[index + 1])
        if f_left == 0.0:
            roots.append(left)
        if f_left * f_right < 0.0:
            roots.append(
                bracketed_root(
                    lambda composition: float(model(composition, temperature_k)),
                    left,
                    right,
                )
            )
    if values[-1] == 0.0:
        roots.append(1.0)

    roots.sort()
    unique: list[float] = []
    for root in roots:
        if not unique or abs(root - unique[-1]) > 1.0e-9:
            unique.append(root)
    return unique


def _bounded_interval_probability(
    mean: float,
    sigma: float,
    left: float,
    right: float,
) -> float:
    if right <= left:
        return 0.0
    if sigma == 0.0:
        return 1.0 if left <= mean <= right else 0.0
    normalization = _normal_cdf((1.0 - mean) / sigma) - _normal_cdf(
        (0.0 - mean) / sigma
    )
    probability = _normal_cdf((right - mean) / sigma) - _normal_cdf(
        (left - mean) / sigma
    )
    return max(0.0, probability / normalization)


def _gap_sign_probabilities(
    model: Callable[[float, float], GapValue],
    mean: float,
    sigma: float,
    temperature_k: float,
    *,
    zero_tolerance_ev: float,
    composition_root_grid_size: int,
) -> tuple[float, float, float]:
    tolerance = _finite_scalar("zero_tolerance_ev", zero_tolerance_ev)
    if tolerance < 0.0:
        raise ValueError("zero_tolerance_ev must be non-negative")

    if sigma == 0.0:
        gap = float(model(mean, temperature_k))
        if gap < -tolerance:
            return 1.0, 0.0, 0.0
        if gap > tolerance:
            return 0.0, 0.0, 1.0
        return 0.0, 1.0, 0.0

    if tolerance > 0.0:
        nodes, weights, *_ = _bounded_gaussian_nodes(
            mean,
            sigma,
            quadrature_order=max(512, composition_root_grid_size // 2),
            standard_deviation_limit=8.0,
        )
        gaps = np.asarray([float(model(float(x), temperature_k)) for x in nodes])
        negative = float(np.sum(weights[gaps < -tolerance]))
        positive = float(np.sum(weights[gaps > tolerance]))
        near_zero = max(0.0, 1.0 - negative - positive)
        return negative, near_zero, positive

    roots = _composition_roots(
        model,
        temperature_k,
        grid_size=composition_root_grid_size,
    )
    boundaries = [0.0, *roots, 1.0]
    negative = 0.0
    positive = 0.0
    for left, right in zip(boundaries[:-1], boundaries[1:], strict=True):
        if right <= left:
            continue
        midpoint = 0.5 * (left + right)
        gap = float(model(midpoint, temperature_k))
        probability = _bounded_interval_probability(mean, sigma, left, right)
        if gap < 0.0:
            negative += probability
        elif gap > 0.0:
            positive += probability
    near_zero = max(0.0, 1.0 - negative - positive)
    return negative, near_zero, positive


def gaussian_gap_moments(
    model: Callable[[float, float], GapValue],
    mean_composition: float,
    composition_sigma: float,
    temperature_k: float,
    *,
    quadrature_order: int = 128,
    standard_deviation_limit: float = 8.0,
    zero_tolerance_ev: float = 0.0,
    composition_root_grid_size: int = 2049,
) -> GaussianGapMoments:
    """Return exact quadrature moments and local-approximation errors."""

    mean, sigma = _validate_distribution_inputs(mean_composition, composition_sigma)
    temperature = _finite_scalar("temperature_k", temperature_k)
    if temperature < 0.0:
        raise ValueError("temperature_k must be non-negative")

    (
        nodes,
        weights,
        physical_probability,
        omitted_probability,
        effective_mean,
        effective_sigma,
    ) = _bounded_gaussian_nodes(
        mean,
        sigma,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    gaps = np.asarray([float(model(float(x), temperature)) for x in nodes])
    if not np.all(np.isfinite(gaps)):
        raise ValueError("gap model must return finite scalar values")

    mean_gap = float(np.sum(weights * gaps))
    variance = float(np.sum(weights * (gaps - mean_gap) ** 2))
    gap_sigma = sqrt(max(variance, 0.0))
    if gap_sigma == 0.0:
        skewness = 0.0
    else:
        third_moment = float(np.sum(weights * (gaps - mean_gap) ** 3))
        skewness = third_moment / gap_sigma**3

    negative, near_zero, positive = _gap_sign_probabilities(
        model,
        mean,
        sigma,
        temperature,
        zero_tolerance_ev=zero_tolerance_ev,
        composition_root_grid_size=composition_root_grid_size,
    )
    linearized = linearized_composition_gap_statistics(
        model,
        mean,
        sigma,
        temperature,
    )

    return GaussianGapMoments(
        declared_mean_composition=mean,
        declared_composition_sigma=sigma,
        effective_mean_composition=effective_mean,
        effective_composition_sigma=effective_sigma,
        physical_interval_probability=physical_probability,
        omitted_tail_probability=omitted_probability,
        temperature_k=temperature,
        mean_gap_ev=mean_gap,
        gap_sigma_ev=gap_sigma,
        gap_skewness=skewness,
        negative_gap_probability=negative,
        near_zero_gap_probability=near_zero,
        positive_gap_probability=positive,
        linearized_mean_gap_ev=linearized.mean_gap_ev,
        linearized_gap_sigma_ev=linearized.gap_sigma_ev,
        mean_approximation_error_ev=mean_gap - linearized.mean_gap_ev,
        sigma_approximation_error_ev=gap_sigma - linearized.gap_sigma_ev,
        quadrature_order=int(quadrature_order),
    )


def _temperature_roots(
    model: Callable[[float, float], GapValue],
    composition: float,
    temperature_lower_k: float,
    temperature_upper_k: float,
    *,
    grid_size: int,
) -> tuple[list[float], NDArray[np.float64]]:
    size = int(grid_size)
    if size < 33:
        raise ValueError("temperature_grid_size must be at least 33")
    temperatures = np.linspace(temperature_lower_k, temperature_upper_k, size)
    gaps = np.asarray(
        [float(model(composition, float(temperature))) for temperature in temperatures]
    )
    if not np.all(np.isfinite(gaps)):
        raise ValueError("gap model must be finite on the temperature grid")

    roots: list[float] = []
    for index in range(size - 1):
        left = float(temperatures[index])
        right = float(temperatures[index + 1])
        f_left = float(gaps[index])
        f_right = float(gaps[index + 1])
        if f_left == 0.0:
            roots.append(left)
        if f_left * f_right < 0.0:
            roots.append(
                bracketed_root(
                    lambda temperature: float(model(composition, temperature)),
                    left,
                    right,
                )
            )
    if gaps[-1] == 0.0:
        roots.append(float(temperature_upper_k))

    roots.sort()
    unique: list[float] = []
    for root in roots:
        if not unique or abs(root - unique[-1]) > 1.0e-7:
            unique.append(root)
    return unique, gaps


def gaussian_critical_temperature_distribution(
    model: Callable[[float, float], GapValue],
    mean_composition: float,
    composition_sigma: float,
    *,
    temperature_bounds_k: tuple[float, float] = (0.0, 300.0),
    quadrature_order: int = 128,
    standard_deviation_limit: float = 8.0,
    temperature_grid_size: int = 257,
) -> CriticalTemperatureDistribution:
    """Propagate a bounded Gaussian composition model into critical temperature.

    A quadrature node contributes to the conditional temperature distribution
    only when exactly one root of ``Eg(x,T)=0`` occurs inside the declared
    interval. Nodes with no root are classified by the sign over the sampled
    interval; nodes with multiple roots are retained separately.
    """

    mean, sigma = _validate_distribution_inputs(mean_composition, composition_sigma)
    lower = _finite_scalar("temperature_lower_k", temperature_bounds_k[0])
    upper = _finite_scalar("temperature_upper_k", temperature_bounds_k[1])
    if lower < 0.0 or upper <= lower:
        raise ValueError("temperature bounds must be non-negative and ordered")

    nodes, weights, _, _, effective_mean, effective_sigma = _bounded_gaussian_nodes(
        mean,
        sigma,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )

    root_values: list[float] = []
    root_weights: list[float] = []
    always_normal = 0.0
    always_inverted = 0.0
    multiple = 0.0
    unresolved = 0.0

    for composition, weight in zip(nodes, weights, strict=True):
        roots, sampled_gaps = _temperature_roots(
            model,
            float(composition),
            lower,
            upper,
            grid_size=temperature_grid_size,
        )
        probability = float(weight)
        if len(roots) == 1:
            root_values.append(roots[0])
            root_weights.append(probability)
        elif len(roots) > 1:
            multiple += probability
        elif np.all(sampled_gaps > 0.0):
            always_normal += probability
        elif np.all(sampled_gaps < 0.0):
            always_inverted += probability
        else:
            unresolved += probability

    crossing_probability = float(sum(root_weights))
    conditional_mean: float | None = None
    conditional_sigma: float | None = None
    conditional_skewness: float | None = None
    if crossing_probability > 0.0:
        roots_array = np.asarray(root_values, dtype=float)
        conditional_weights = np.asarray(root_weights, dtype=float) / crossing_probability
        conditional_mean = float(np.sum(conditional_weights * roots_array))
        variance = float(
            np.sum(conditional_weights * (roots_array - conditional_mean) ** 2)
        )
        conditional_sigma = sqrt(max(variance, 0.0))
        if conditional_sigma == 0.0:
            conditional_skewness = 0.0
        else:
            third_moment = float(
                np.sum(conditional_weights * (roots_array - conditional_mean) ** 3)
            )
            conditional_skewness = third_moment / conditional_sigma**3

    central_roots, _ = _temperature_roots(
        model,
        mean,
        lower,
        upper,
        grid_size=temperature_grid_size,
    )
    central_critical_temperature: float | None = None
    linearized_sigma: float | None = None
    conditional_mean_shift: float | None = None
    sigma_error: float | None = None
    if len(central_roots) == 1:
        central_critical_temperature = central_roots[0]
        local = linearized_composition_gap_statistics(
            model,
            mean,
            sigma,
            central_critical_temperature,
        )
        linearized_sigma = local.critical_temperature_sigma_k
        if conditional_mean is not None:
            conditional_mean_shift = conditional_mean - central_critical_temperature
        if conditional_sigma is not None:
            sigma_error = conditional_sigma - linearized_sigma

    total = crossing_probability + always_normal + always_inverted + multiple + unresolved
    if not np.isclose(total, 1.0, atol=5.0e-12):
        raise RuntimeError("critical-temperature probability accounting is incomplete")

    return CriticalTemperatureDistribution(
        declared_mean_composition=mean,
        declared_composition_sigma=sigma,
        effective_mean_composition=effective_mean,
        effective_composition_sigma=effective_sigma,
        temperature_lower_k=lower,
        temperature_upper_k=upper,
        single_crossing_probability=crossing_probability,
        always_normal_probability=always_normal,
        always_inverted_probability=always_inverted,
        multiple_crossing_probability=multiple,
        unresolved_probability=unresolved,
        conditional_mean_temperature_k=conditional_mean,
        conditional_sigma_temperature_k=conditional_sigma,
        conditional_skewness=conditional_skewness,
        central_composition_critical_temperature_k=central_critical_temperature,
        linearized_sigma_temperature_k=linearized_sigma,
        conditional_mean_shift_k=conditional_mean_shift,
        sigma_approximation_error_k=sigma_error,
        quadrature_order=int(quadrature_order),
        temperature_grid_size=int(temperature_grid_size),
    )
