"""Bias diagnostics for a misspecified Gaussian spatial-covariance inverse.

This module extends :mod:`spatial_disorder_covariance_families`.  It does not
redefine covariance families, probe filtering, or the three-scale invariant.
Instead it quantifies two consequences after a non-Gaussian covariance is
nevertheless interpreted with the two-parameter Gaussian inverse:

1. drift of inferred point variance and correlation length across scale pairs;
2. bias of the best global Gaussian surrogate in log-variance space.

All results are controlled synthetic diagnostics, not specimen estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import exp, isfinite, log, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_covariance_families import (
    SUPPORTED_MATERN_SMOOTHNESS,
    gaussian_reference_variance,
    matern_gaussian_probe_variance_2d,
)
from .spatial_disorder_theorems import recover_isotropic_gaussian_two_scales

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _validated_scales_and_variances(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
    *,
    minimum_count: int,
) -> tuple[FloatArray, FloatArray]:
    scales = np.asarray(probe_sigmas, dtype=float)
    values = np.asarray(variances, dtype=float)
    if scales.ndim != 1 or values.ndim != 1 or scales.shape != values.shape:
        raise ValueError(
            "probe_sigmas and variances must be matching one-dimensional arrays"
        )
    if scales.size < minimum_count:
        raise ValueError(f"at least {minimum_count} scales are required")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("variances must be finite and positive")
    if np.unique(scales).size != scales.size:
        raise ValueError("probe_sigmas must be distinct")
    order = np.argsort(scales)
    sorted_scales = np.array(scales[order], dtype=float, copy=True)
    sorted_values = np.array(values[order], dtype=float, copy=True)
    sorted_scales.setflags(write=False)
    sorted_values.setflags(write=False)
    return sorted_scales, sorted_values


def _read_only_float(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _read_only_int(value: ArrayLike) -> IntArray:
    result = np.array(value, dtype=np.int64, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class GaussianPairwiseParameterDrift:
    """Gaussian parameters recovered independently from every scale pair."""

    probe_sigmas: FloatArray
    observed_variances: FloatArray
    pair_indices: IntArray
    point_variances: FloatArray
    correlation_lengths: FloatArray
    point_variance_spread_ratio: float
    correlation_length_spread_ratio: float


def gaussian_pairwise_parameter_drift(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
) -> GaussianPairwiseParameterDrift:
    """Recover the Gaussian parameters from every pair of probe scales.

    Exact Gaussian-family data return one common parameter pair.  Under family
    misspecification, the recovered values depend on which scales were selected.
    """

    scales, values = _validated_scales_and_variances(
        probe_sigmas,
        variances,
        minimum_count=2,
    )
    pairs = list(combinations(range(scales.size), 2))
    recoveries = [
        recover_isotropic_gaussian_two_scales(
            float(values[first]),
            float(values[second]),
            float(scales[first]),
            float(scales[second]),
            dimension=2,
        )
        for first, second in pairs
    ]
    point_variances = np.array(
        [result.point_variance for result in recoveries], dtype=float
    )
    correlation_lengths = np.array(
        [result.correlation_length for result in recoveries], dtype=float
    )
    return GaussianPairwiseParameterDrift(
        probe_sigmas=scales,
        observed_variances=values,
        pair_indices=_read_only_int(pairs),
        point_variances=_read_only_float(point_variances),
        correlation_lengths=_read_only_float(correlation_lengths),
        point_variance_spread_ratio=float(
            np.max(point_variances) / np.min(point_variances)
        ),
        correlation_length_spread_ratio=float(
            np.max(correlation_lengths) / np.min(correlation_lengths)
        ),
    )


@dataclass(frozen=True)
class GaussianLogVarianceSurrogate:
    """Best Gaussian surrogate under weighted log-variance loss."""

    probe_sigmas: FloatArray
    observed_variances: FloatArray
    normalized_weights: FloatArray
    fitted_point_variance: float
    fitted_correlation_length: float
    fitted_variances: FloatArray
    log_residuals: FloatArray
    rms_log_error: float
    maximum_absolute_relative_variance_error: float
    objective_value: float
    iterations: int


def fit_gaussian_log_variance_surrogate(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
    *,
    weights: ArrayLike | None = None,
    log_correlation_tolerance: float = 1.0e-12,
    maximum_iterations: int = 256,
) -> GaussianLogVarianceSurrogate:
    """Fit a Gaussian covariance surrogate in relative log-variance space.

    For each trial correlation length the optimal log point variance is exact.
    The remaining one-dimensional profile is solved by derivative-bracketed
    bisection after nondimensionalizing length and centering log variance.  This
    makes the result invariant to length units and variance amplitude.
    """

    scales, values = _validated_scales_and_variances(
        probe_sigmas,
        variances,
        minimum_count=2,
    )
    positive_scales = scales[scales > 0.0]
    if positive_scales.size == 0:
        raise ValueError("at least one probe scale must be positive")

    if weights is None:
        normalized_weights = np.full(scales.size, 1.0 / scales.size)
    else:
        supplied_weights = np.asarray(weights, dtype=float)
        if supplied_weights.shape != values.shape:
            raise ValueError("weights must match the variance array")
        if not np.all(np.isfinite(supplied_weights)) or np.any(
            supplied_weights <= 0.0
        ):
            raise ValueError("weights must be finite and positive")
        normalized_weights = supplied_weights / np.sum(supplied_weights)

    tolerance = _positive(
        "log_correlation_tolerance", log_correlation_tolerance
    )
    if isinstance(maximum_iterations, bool) or not isinstance(
        maximum_iterations, (int, np.integer)
    ) or maximum_iterations <= 0:
        raise ValueError("maximum_iterations must be a positive integer")

    log_values = np.log(values)
    log_value_offset = float(np.dot(normalized_weights, log_values))
    centered_log_values = log_values - log_value_offset
    reference_scale = exp(float(np.mean(np.log(positive_scales))))
    normalized_scale_squared = (scales / reference_scale) ** 2

    def profile(log_correlation_ratio: float) -> tuple[float, float, float]:
        q = 2.0 * normalized_scale_squared * exp(
            -2.0 * log_correlation_ratio
        )
        log_denominator = np.log1p(q)
        transition_fraction = q / (1.0 + q)
        centered_log_amplitude = float(
            np.dot(
                normalized_weights,
                centered_log_values + log_denominator,
            )
        )
        residuals = (
            centered_log_amplitude
            - log_denominator
            - centered_log_values
        )
        objective = float(np.dot(normalized_weights, residuals**2))
        derivative = float(
            4.0
            * np.dot(
                normalized_weights,
                residuals * transition_fraction,
            )
        )
        return (
            objective,
            centered_log_amplitude + log_value_offset,
            derivative,
        )

    lower = log(float(np.min(positive_scales) / reference_scale)) - 12.0
    upper = log(float(np.max(positive_scales) / reference_scale)) + 12.0
    _, _, derivative_lower = profile(lower)
    _, _, derivative_upper = profile(upper)
    if derivative_lower > 0.0 or derivative_upper < 0.0:
        raise RuntimeError("failed to bracket the Gaussian surrogate optimum")

    iterations = 0
    while iterations < int(maximum_iterations) and upper - lower > tolerance:
        midpoint = 0.5 * (lower + upper)
        _, _, derivative_midpoint = profile(midpoint)
        if derivative_midpoint > 0.0:
            upper = midpoint
        else:
            lower = midpoint
        iterations += 1

    log_correlation_ratio = 0.5 * (lower + upper)
    objective, log_amplitude, _ = profile(log_correlation_ratio)
    correlation_length = reference_scale * exp(log_correlation_ratio)
    point_variance = exp(log_amplitude)
    fitted = point_variance / (
        1.0
        + 2.0
        * normalized_scale_squared
        / exp(2.0 * log_correlation_ratio)
    )
    log_residuals = np.log(fitted) - log_values
    relative_errors = fitted / values - 1.0

    return GaussianLogVarianceSurrogate(
        probe_sigmas=scales,
        observed_variances=values,
        normalized_weights=_read_only_float(normalized_weights),
        fitted_point_variance=float(point_variance),
        fitted_correlation_length=float(correlation_length),
        fitted_variances=_read_only_float(fitted),
        log_residuals=_read_only_float(log_residuals),
        rms_log_error=float(
            sqrt(np.dot(normalized_weights, log_residuals**2))
        ),
        maximum_absolute_relative_variance_error=float(
            np.max(np.abs(relative_errors))
        ),
        objective_value=float(objective),
        iterations=iterations,
    )


@dataclass(frozen=True)
class GaussianInverseFamilyBias:
    """Pairwise drift and global-surrogate bias for one synthetic family."""

    true_family: str
    true_matern_smoothness: float | None
    true_point_variance: float
    true_correlation_length: float
    probe_sigmas: FloatArray
    true_filtered_variances: FloatArray
    pairwise_drift: GaussianPairwiseParameterDrift
    global_surrogate: GaussianLogVarianceSurrogate
    point_variance_bias_ratio: float
    correlation_length_bias_ratio: float


def _bias_from_values(
    family: str,
    smoothness: float | None,
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    values: ArrayLike,
    *,
    weights: ArrayLike | None,
) -> GaussianInverseFamilyBias:
    amplitude = _positive("point_variance", point_variance)
    correlation = _positive("correlation_length", correlation_length)
    pairwise = gaussian_pairwise_parameter_drift(probe_sigmas, values)
    surrogate = fit_gaussian_log_variance_surrogate(
        probe_sigmas,
        values,
        weights=weights,
    )
    return GaussianInverseFamilyBias(
        true_family=family,
        true_matern_smoothness=smoothness,
        true_point_variance=amplitude,
        true_correlation_length=correlation,
        probe_sigmas=pairwise.probe_sigmas,
        true_filtered_variances=pairwise.observed_variances,
        pairwise_drift=pairwise,
        global_surrogate=surrogate,
        point_variance_bias_ratio=float(
            surrogate.fitted_point_variance / amplitude
        ),
        correlation_length_bias_ratio=float(
            surrogate.fitted_correlation_length / correlation
        ),
    )


def gaussian_family_inverse_bias(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    weights: ArrayLike | None = None,
) -> GaussianInverseFamilyBias:
    """Return the zero-misspecification Gaussian reference diagnostics."""

    values = gaussian_reference_variance(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    return _bias_from_values(
        "gaussian",
        None,
        point_variance,
        correlation_length,
        probe_sigmas,
        values,
        weights=weights,
    )


def matern_family_gaussian_inverse_bias(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    smoothness: float,
    *,
    weights: ArrayLike | None = None,
    quadrature_order: int = 96,
) -> GaussianInverseFamilyBias:
    """Force a half-integer Matérn field through the Gaussian inverse."""

    nu = float(smoothness)
    if nu not in SUPPORTED_MATERN_SMOOTHNESS:
        raise ValueError(
            "smoothness must be one of "
            f"{SUPPORTED_MATERN_SMOOTHNESS}"
        )
    values = matern_gaussian_probe_variance_2d(
        point_variance,
        correlation_length,
        probe_sigmas,
        nu,
        quadrature_order=quadrature_order,
    )
    return _bias_from_values(
        f"matern_{nu:g}",
        nu,
        point_variance,
        correlation_length,
        probe_sigmas,
        values,
        weights=weights,
    )
