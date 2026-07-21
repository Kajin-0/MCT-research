"""Nonlinear posterior propagation for common probe-scale calibration.

For the isotropic two-dimensional Gaussian covariance/Gaussian probe benchmark,

``V_i = A / (1 + 2 (s_i exp(delta))**2 / xi**2)``,

define ``u = log(A)``, ``v = log(xi)``, and ``lambda = v - delta``.
Any likelihood whose scale dependence enters only through ``s_i exp(delta)/xi``
depends on ``(u, lambda)`` and not on ``v`` and ``delta`` separately.

With an independent calibration prior and a translation-invariant prior on
``v``, the transformed posterior factorizes exactly.  Consequently the
absolute log-correlation-length posterior is the convolution of the
relative-scale posterior and the calibration prior; their cumulants add.

The numerical routines below provide deterministic grid verification and a
bounded-prior failure diagnostic.  They are intentionally narrow and do not
form a general Bayesian inference framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, sqrt
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]
LikelihoodKind = Literal["log_gaussian", "gaussian"]


@dataclass(frozen=True)
class DiscreteDistribution1D:
    """Normalized probability mass on one uniform grid with four cumulants."""

    grid: FloatArray
    probability_mass: FloatArray
    spacing: float
    mean: float
    variance: float
    third_cumulant: float
    fourth_cumulant: float
    skewness: float | None
    excess_kurtosis: float | None


@dataclass(frozen=True)
class RelativeScalePosterior:
    """Posterior for ``(log A, log xi_relative)`` on a uniform 2D grid."""

    log_point_variance_grid: FloatArray
    log_relative_correlation_grid: FloatArray
    probability_mass: FloatMatrix
    mean: FloatArray
    covariance: FloatMatrix
    relative_correlation_distribution: DiscreteDistribution1D
    log_normalizer: float
    boundary_mass: float
    likelihood: str


@dataclass(frozen=True)
class CommonScalePosterior:
    """Exact posterior summary after independent common-scale calibration."""

    relative_posterior: RelativeScalePosterior
    calibration_prior: DiscreteDistribution1D
    absolute_log_correlation_distribution: DiscreteDistribution1D
    mean: FloatArray
    covariance: FloatMatrix
    covariance_increment: FloatMatrix
    log_correlation_cumulants: FloatArray
    variance_addition_residual: float
    cross_covariance_residual: float


@dataclass(frozen=True)
class DirectBoundedPosteriorDiagnostics:
    """Direct 3D grid posterior under a bounded absolute log-length prior."""

    mean: FloatArray
    covariance: FloatMatrix
    variable_order: tuple[str, str, str, str]
    log_absolute_correlation_boundary_mass: float
    posterior_calibration_total_variation: float
    posterior_calibration_mean_shift: float
    posterior_calibration_variance_shift: float
    relative_calibration_covariance: float
    variance_addition_residual: float
    cross_covariance_residual: float
    log_normalizer: float
    likelihood: str


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _uniform_grid(name: str, values: ArrayLike, *, minimum_size: int = 2) -> tuple[FloatArray, float]:
    grid = np.asarray(values, dtype=float)
    if grid.ndim != 1 or grid.size < minimum_size:
        raise ValueError(f"{name} must be one-dimensional with at least {minimum_size} points")
    if not np.all(np.isfinite(grid)) or np.any(np.diff(grid) <= 0.0):
        raise ValueError(f"{name} must be finite and strictly increasing")
    differences = np.diff(grid)
    spacing = float(differences[0])
    if not np.allclose(differences, spacing, rtol=2.0e-12, atol=2.0e-14 * max(1.0, abs(spacing))):
        raise ValueError(f"{name} must be uniformly spaced")
    return _read_only(grid), spacing


def _normalized_mass(probability_mass: ArrayLike, shape: tuple[int, ...]) -> FloatArray:
    mass = np.asarray(probability_mass, dtype=float)
    if mass.shape != shape:
        raise ValueError(f"probability_mass must have shape {shape}")
    if not np.all(np.isfinite(mass)) or np.any(mass < 0.0):
        raise ValueError("probability_mass must be finite and non-negative")
    total = float(np.sum(mass))
    if not isfinite(total) or total <= 0.0:
        raise ValueError("probability_mass must have positive total mass")
    return _read_only(mass / total)


def discrete_distribution(grid: ArrayLike, probability_mass: ArrayLike) -> DiscreteDistribution1D:
    """Normalize one uniform-grid mass distribution and return its cumulants."""

    points, spacing = _uniform_grid("grid", grid)
    mass = _normalized_mass(probability_mass, (points.size,))
    mean = float(np.dot(np.asarray(mass), np.asarray(points)))
    centered = np.asarray(points) - mean
    variance = float(np.dot(np.asarray(mass), centered**2))
    third = float(np.dot(np.asarray(mass), centered**3))
    fourth_central = float(np.dot(np.asarray(mass), centered**4))
    fourth_cumulant = fourth_central - 3.0 * variance * variance
    if variance > 0.0:
        skewness = third / variance**1.5
        excess_kurtosis = fourth_cumulant / (variance * variance)
    else:
        skewness = None
        excess_kurtosis = None
    return DiscreteDistribution1D(
        grid=points,
        probability_mass=mass,
        spacing=spacing,
        mean=mean,
        variance=variance,
        third_cumulant=third,
        fourth_cumulant=fourth_cumulant,
        skewness=skewness,
        excess_kurtosis=excess_kurtosis,
    )


def gaussian_grid_distribution(
    grid: ArrayLike,
    mean: float,
    standard_deviation: float,
) -> DiscreteDistribution1D:
    """Return a normalized Gaussian prior sampled on a uniform grid."""

    points, _ = _uniform_grid("grid", grid)
    location = float(mean)
    if not isfinite(location):
        raise ValueError("mean must be finite")
    scale = _positive_scalar("standard_deviation", standard_deviation)
    exponent = -0.5 * ((np.asarray(points) - location) / scale) ** 2
    exponent -= float(np.max(exponent))
    return discrete_distribution(points, np.exp(exponent))


def _validated_observations(
    observed_variances: ArrayLike,
    probe_sigmas: ArrayLike,
) -> tuple[FloatArray, FloatArray]:
    observed = np.asarray(observed_variances, dtype=float)
    scales = np.asarray(probe_sigmas, dtype=float)
    if observed.ndim != 1 or scales.ndim != 1 or observed.shape != scales.shape or observed.size < 2:
        raise ValueError("observed_variances and probe_sigmas must be matching 1D arrays with at least two entries")
    if not np.all(np.isfinite(observed)) or np.any(observed <= 0.0):
        raise ValueError("observed_variances must be finite and positive")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    return _read_only(observed), _read_only(scales)


def _validated_uncertainty(
    size: int,
    likelihood: LikelihoodKind,
    *,
    observation_standard_deviations: ArrayLike | None,
    log_observation_standard_deviations: ArrayLike | None,
    relative_standard_deviation: float | None,
) -> FloatArray:
    supplied = sum(
        value is not None
        for value in (
            observation_standard_deviations,
            log_observation_standard_deviations,
            relative_standard_deviation,
        )
    )
    if supplied != 1:
        raise ValueError("provide exactly one observation uncertainty specification")

    if relative_standard_deviation is not None:
        relative = _positive_scalar("relative_standard_deviation", relative_standard_deviation)
        if likelihood == "log_gaussian":
            value = sqrt(log(1.0 + relative * relative))
            return _read_only(np.full(size, value, dtype=float))
        raise ValueError("relative_standard_deviation is supported only for log_gaussian likelihood")

    selected = (
        log_observation_standard_deviations
        if likelihood == "log_gaussian"
        else observation_standard_deviations
    )
    rejected = (
        observation_standard_deviations
        if likelihood == "log_gaussian"
        else log_observation_standard_deviations
    )
    if rejected is not None:
        raise ValueError("uncertainty specification does not match the selected likelihood")
    values = np.asarray(selected, dtype=float)
    if values.ndim == 0:
        values = np.full(size, float(values), dtype=float)
    if values.shape != (size,) or not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("observation standard deviations must be scalar or a finite positive vector")
    return _read_only(values)


def _predicted_variance(
    log_point_variance: FloatArray,
    log_relative_correlation: FloatArray,
    probe_sigmas: FloatArray,
) -> FloatArray:
    point_variance = np.exp(np.asarray(log_point_variance))[..., np.newaxis]
    inverse_xi_squared = np.exp(-2.0 * np.asarray(log_relative_correlation))[..., np.newaxis]
    denominator = 1.0 + 2.0 * np.asarray(probe_sigmas) ** 2 * inverse_xi_squared
    return point_variance / denominator


def _log_likelihood(
    predicted: FloatArray,
    observed: FloatArray,
    uncertainty: FloatArray,
    likelihood: LikelihoodKind,
) -> FloatArray:
    if likelihood == "log_gaussian":
        residual = (np.log(np.asarray(observed)) - np.log(predicted)) / np.asarray(uncertainty)
        normalization = np.log(np.asarray(uncertainty)) + np.log(np.asarray(observed))
    elif likelihood == "gaussian":
        residual = (np.asarray(observed) - predicted) / np.asarray(uncertainty)
        normalization = np.log(np.asarray(uncertainty))
    else:
        raise ValueError("likelihood must be 'log_gaussian' or 'gaussian'")
    return -0.5 * np.sum(residual * residual, axis=-1) - np.sum(normalization)


def _normalize_log_mass(log_mass: FloatArray) -> tuple[FloatArray, float]:
    maximum = float(np.max(log_mass))
    if not isfinite(maximum):
        raise ValueError("posterior log mass has no finite support")
    shifted = np.exp(np.asarray(log_mass) - maximum)
    total = float(np.sum(shifted))
    if not isfinite(total) or total <= 0.0:
        raise ArithmeticError("posterior normalization failed")
    return _read_only(shifted / total), maximum + log(total)


def relative_scale_posterior_grid(
    observed_variances: ArrayLike,
    probe_sigmas: ArrayLike,
    log_point_variance_grid: ArrayLike,
    log_relative_correlation_grid: ArrayLike,
    *,
    likelihood: LikelihoodKind = "log_gaussian",
    observation_standard_deviations: ArrayLike | None = None,
    log_observation_standard_deviations: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    log_prior_mass: ArrayLike | None = None,
    boundary_cells: int = 2,
) -> RelativeScalePosterior:
    """Return the deterministic posterior for ``(log A, log xi_relative)``."""

    observed, scales = _validated_observations(observed_variances, probe_sigmas)
    u_grid, _ = _uniform_grid("log_point_variance_grid", log_point_variance_grid)
    lambda_grid, _ = _uniform_grid(
        "log_relative_correlation_grid",
        log_relative_correlation_grid,
    )
    uncertainty = _validated_uncertainty(
        observed.size,
        likelihood,
        observation_standard_deviations=observation_standard_deviations,
        log_observation_standard_deviations=log_observation_standard_deviations,
        relative_standard_deviation=relative_standard_deviation,
    )
    predicted = _predicted_variance(
        np.asarray(u_grid)[:, np.newaxis],
        np.asarray(lambda_grid)[np.newaxis, :],
        scales,
    )
    log_mass = _log_likelihood(predicted, observed, uncertainty, likelihood)
    if log_prior_mass is not None:
        prior = np.asarray(log_prior_mass, dtype=float)
        if prior.shape != log_mass.shape or not np.all(np.isfinite(prior) | np.isneginf(prior)):
            raise ValueError("log_prior_mass must match the posterior grid and contain finite values or -inf")
        log_mass = log_mass + prior
    mass, log_normalizer = _normalize_log_mass(log_mass)

    u_values = np.asarray(u_grid)[:, np.newaxis]
    lambda_values = np.asarray(lambda_grid)[np.newaxis, :]
    mean_u = float(np.sum(np.asarray(mass) * u_values))
    mean_lambda = float(np.sum(np.asarray(mass) * lambda_values))
    centered_u = u_values - mean_u
    centered_lambda = lambda_values - mean_lambda
    covariance = np.array(
        [
            [
                np.sum(np.asarray(mass) * centered_u**2),
                np.sum(np.asarray(mass) * centered_u * centered_lambda),
            ],
            [
                np.sum(np.asarray(mass) * centered_u * centered_lambda),
                np.sum(np.asarray(mass) * centered_lambda**2),
            ],
        ],
        dtype=float,
    )
    lambda_distribution = discrete_distribution(
        lambda_grid,
        np.sum(np.asarray(mass), axis=0),
    )
    if isinstance(boundary_cells, bool) or int(boundary_cells) != boundary_cells or not 1 <= int(boundary_cells) * 2 < min(u_grid.size, lambda_grid.size):
        raise ValueError("boundary_cells must be a positive integer smaller than half each grid")
    cells = int(boundary_cells)
    boundary_mask = np.zeros(mass.shape, dtype=bool)
    boundary_mask[:cells, :] = True
    boundary_mask[-cells:, :] = True
    boundary_mask[:, :cells] = True
    boundary_mask[:, -cells:] = True
    boundary_mass = float(np.sum(np.asarray(mass)[boundary_mask]))

    return RelativeScalePosterior(
        log_point_variance_grid=u_grid,
        log_relative_correlation_grid=lambda_grid,
        probability_mass=mass,
        mean=_read_only([mean_u, mean_lambda]),
        covariance=_read_only(covariance),
        relative_correlation_distribution=lambda_distribution,
        log_normalizer=float(log_normalizer),
        boundary_mass=boundary_mass,
        likelihood=likelihood,
    )


def combine_common_scale_calibration(
    relative_posterior: RelativeScalePosterior,
    calibration_prior: DiscreteDistribution1D,
) -> CommonScalePosterior:
    """Apply the exact common-scale posterior convolution and moment identities."""

    lambda_distribution = relative_posterior.relative_correlation_distribution
    spacing_scale = max(1.0, abs(lambda_distribution.spacing), abs(calibration_prior.spacing))
    if not np.isclose(
        lambda_distribution.spacing,
        calibration_prior.spacing,
        rtol=2.0e-12,
        atol=2.0e-14 * spacing_scale,
    ):
        raise ValueError("relative posterior and calibration prior must use the same grid spacing")
    convolution_mass = np.convolve(
        np.asarray(lambda_distribution.probability_mass),
        np.asarray(calibration_prior.probability_mass),
    )
    absolute_grid = (
        lambda_distribution.grid[0]
        + calibration_prior.grid[0]
        + lambda_distribution.spacing * np.arange(convolution_mass.size)
    )
    absolute_distribution = discrete_distribution(absolute_grid, convolution_mass)

    relative_covariance = np.asarray(relative_posterior.covariance)
    covariance = np.array(relative_covariance, copy=True)
    covariance[1, 1] += calibration_prior.variance
    covariance_increment = covariance - relative_covariance
    mean = np.array(
        [
            relative_posterior.mean[0],
            relative_posterior.mean[1] + calibration_prior.mean,
        ],
        dtype=float,
    )
    expected_cumulants = np.array(
        [
            lambda_distribution.mean + calibration_prior.mean,
            lambda_distribution.variance + calibration_prior.variance,
            lambda_distribution.third_cumulant + calibration_prior.third_cumulant,
            lambda_distribution.fourth_cumulant + calibration_prior.fourth_cumulant,
        ],
        dtype=float,
    )
    obtained_cumulants = np.array(
        [
            absolute_distribution.mean,
            absolute_distribution.variance,
            absolute_distribution.third_cumulant,
            absolute_distribution.fourth_cumulant,
        ],
        dtype=float,
    )

    return CommonScalePosterior(
        relative_posterior=relative_posterior,
        calibration_prior=calibration_prior,
        absolute_log_correlation_distribution=absolute_distribution,
        mean=_read_only(mean),
        covariance=_read_only(covariance),
        covariance_increment=_read_only(covariance_increment),
        log_correlation_cumulants=_read_only(obtained_cumulants),
        variance_addition_residual=float(obtained_cumulants[1] - expected_cumulants[1]),
        cross_covariance_residual=float(covariance[0, 1] - relative_covariance[0, 1]),
    )


def direct_bounded_common_scale_posterior(
    observed_variances: ArrayLike,
    probe_sigmas: ArrayLike,
    log_point_variance_grid: ArrayLike,
    log_absolute_correlation_grid: ArrayLike,
    calibration_prior: DiscreteDistribution1D,
    *,
    likelihood: LikelihoodKind = "log_gaussian",
    observation_standard_deviations: ArrayLike | None = None,
    log_observation_standard_deviations: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    boundary_cells: int = 2,
) -> DirectBoundedPosteriorDiagnostics:
    """Integrate the direct ``(u, v, delta)`` posterior with bounded ``v``.

    A uniform discrete prior is used on the supplied ``u`` and ``v`` grids.  The
    finite ``v`` support intentionally exposes the condition under which exact
    factorization fails.
    """

    observed, scales = _validated_observations(observed_variances, probe_sigmas)
    u_grid, _ = _uniform_grid("log_point_variance_grid", log_point_variance_grid)
    v_grid, _ = _uniform_grid(
        "log_absolute_correlation_grid",
        log_absolute_correlation_grid,
    )
    delta_grid = calibration_prior.grid
    uncertainty = _validated_uncertainty(
        observed.size,
        likelihood,
        observation_standard_deviations=observation_standard_deviations,
        log_observation_standard_deviations=log_observation_standard_deviations,
        relative_standard_deviation=relative_standard_deviation,
    )
    u_values = np.asarray(u_grid)[:, np.newaxis, np.newaxis]
    v_values = np.asarray(v_grid)[np.newaxis, :, np.newaxis]
    delta_values = np.asarray(delta_grid)[np.newaxis, np.newaxis, :]
    lambda_values = v_values - delta_values
    predicted = _predicted_variance(u_values, lambda_values, scales)
    log_mass = _log_likelihood(predicted, observed, uncertainty, likelihood)
    prior_mass = np.asarray(calibration_prior.probability_mass)
    with np.errstate(divide="ignore"):
        log_mass = log_mass + np.log(prior_mass)[np.newaxis, np.newaxis, :]
    mass, log_normalizer = _normalize_log_mass(log_mass)

    variables = (u_values, v_values, delta_values, lambda_values)
    means = np.array(
        [float(np.sum(np.asarray(mass) * variable)) for variable in variables],
        dtype=float,
    )
    covariance = np.empty((4, 4), dtype=float)
    for first in range(4):
        centered_first = variables[first] - means[first]
        for second in range(first, 4):
            value = float(
                np.sum(
                    np.asarray(mass)
                    * centered_first
                    * (variables[second] - means[second])
                )
            )
            covariance[first, second] = value
            covariance[second, first] = value

    posterior_delta_mass = np.sum(np.asarray(mass), axis=(0, 1))
    posterior_delta = discrete_distribution(delta_grid, posterior_delta_mass)
    total_variation = 0.5 * float(
        np.sum(
            np.abs(
                np.asarray(posterior_delta.probability_mass)
                - np.asarray(calibration_prior.probability_mass)
            )
        )
    )
    if isinstance(boundary_cells, bool) or int(boundary_cells) != boundary_cells or not 1 <= int(boundary_cells) * 2 < v_grid.size:
        raise ValueError("boundary_cells must be a positive integer smaller than half the v grid")
    cells = int(boundary_cells)
    boundary_mass = float(
        np.sum(np.asarray(mass)[:, :cells, :])
        + np.sum(np.asarray(mass)[:, -cells:, :])
    )

    # Variable order is (u, v, delta, lambda), with v=lambda+delta.
    variance_addition_residual = covariance[1, 1] - (
        covariance[3, 3] + calibration_prior.variance
    )
    cross_covariance_residual = covariance[0, 1] - covariance[0, 3]

    return DirectBoundedPosteriorDiagnostics(
        mean=_read_only(means),
        covariance=_read_only(covariance),
        variable_order=(
            "log_point_variance",
            "log_absolute_correlation",
            "common_log_scale_error",
            "log_relative_correlation",
        ),
        log_absolute_correlation_boundary_mass=boundary_mass,
        posterior_calibration_total_variation=total_variation,
        posterior_calibration_mean_shift=posterior_delta.mean - calibration_prior.mean,
        posterior_calibration_variance_shift=(
            posterior_delta.variance - calibration_prior.variance
        ),
        relative_calibration_covariance=float(covariance[3, 2]),
        variance_addition_residual=float(variance_addition_residual),
        cross_covariance_residual=float(cross_covariance_residual),
        log_normalizer=float(log_normalizer),
        likelihood=likelihood,
    )
