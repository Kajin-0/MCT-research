"""Covariance-family misspecification diagnostics for multiscale disorder.

The inverse under test is the isotropic 2D Gaussian covariance observed with
Gaussian probes: V(s)=A/(1+2s**2/xi**2). Its reciprocal is affine in s**2, so
three distinct probe scales provide the first exact family-closure test.

All synthetic covariance families below share point variance A and 2D integral
correlation area 2*pi*xi**2. Nothing here selects a covariance law for HgCdTe.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from math import erfc, exp, isfinite, log, pi, sqrt
from typing import Literal

import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.typing import ArrayLike, NDArray

CovarianceFamily = Literal["gaussian", "exponential", "matern32", "matern52"]
FloatArray = NDArray[np.float64]
SUPPORTED_COVARIANCE_FAMILIES = (
    "gaussian",
    "exponential",
    "matern32",
    "matern52",
)


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _nonnegative(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _family(value: str) -> str:
    if value not in SUPPORTED_COVARIANCE_FAMILIES:
        allowed = ", ".join(SUPPORTED_COVARIANCE_FAMILIES)
        raise ValueError(f"family must be one of: {allowed}")
    return value


def _scales(
    values: ArrayLike,
    *,
    minimum_size: int = 1,
    increasing: bool = False,
) -> FloatArray:
    result = np.array(values, dtype=float, copy=True)
    if result.ndim != 1 or result.size < minimum_size:
        raise ValueError(
            f"probe_sigmas must be a one-dimensional array with at least "
            f"{minimum_size} entries"
        )
    if not np.all(np.isfinite(result)):
        raise ValueError("probe_sigmas must contain only finite values")
    if np.any(result < 0.0):
        raise ValueError("probe_sigmas must be non-negative")
    if increasing and np.any(np.diff(result) <= 0.0):
        raise ValueError("probe_sigmas must be strictly increasing")
    result.setflags(write=False)
    return result


def _variances(values: ArrayLike, size: int) -> FloatArray:
    result = np.array(values, dtype=float, copy=True)
    if result.shape != (size,):
        raise ValueError(f"effective_variances must have shape ({size},)")
    if not np.all(np.isfinite(result)) or np.any(result <= 0.0):
        raise ValueError("effective_variances must be finite and positive")
    result.setflags(write=False)
    return result


def _readonly(values: ArrayLike) -> FloatArray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def normalized_radial_covariance(
    family: CovarianceFamily | str,
    radius_over_correlation_length: ArrayLike,
) -> FloatArray:
    """Return C(r)/C(0) with integral area 2*pi*xi**2."""

    selected = _family(str(family))
    radius = np.array(radius_over_correlation_length, dtype=float, copy=True)
    if not np.all(np.isfinite(radius)) or np.any(radius < 0.0):
        raise ValueError(
            "radius_over_correlation_length must be finite and non-negative"
        )
    if selected == "gaussian":
        result = np.exp(-0.5 * radius**2)
    elif selected == "exponential":
        result = np.exp(-radius)
    elif selected == "matern32":
        scaled = sqrt(3.0) * radius
        result = (1.0 + scaled) * np.exp(-scaled)
    else:
        scaled = sqrt(5.0) * radius
        result = (1.0 + scaled + scaled**2 / 3.0) * np.exp(-scaled)
    return _readonly(result)


@lru_cache(maxsize=None)
def _legendre_rule(order: int, limit: float) -> tuple[FloatArray, FloatArray]:
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise ValueError("quadrature_order must be an integer")
    if order < 16:
        raise ValueError("quadrature_order must be at least 16")
    upper = _positive("integration_limit", limit)
    nodes, weights = leggauss(int(order))
    return (
        _readonly(0.5 * upper * (nodes + 1.0)),
        _readonly(0.5 * upper * weights),
    )


def exponential_gaussian_probe_attenuation(
    probe_to_correlation_ratio: float,
) -> float:
    """Exact 2D exponential-covariance attenuation for a Gaussian probe."""

    ratio = _nonnegative(
        "probe_to_correlation_ratio", probe_to_correlation_ratio
    )
    if ratio == 0.0:
        return 1.0
    if ratio <= 8.0:
        return float(
            1.0 - sqrt(pi) * ratio * exp(ratio**2) * erfc(ratio)
        )

    inverse_square = 1.0 / ratio**2
    term = 0.5 * inverse_square
    result = term
    n = 1
    for _ in range(1, 16):
        term *= -(2 * n + 1) * 0.5 * inverse_square
        if abs(term) > abs(result) and n > 3:
            break
        result += term
        n += 1
    if not isfinite(result) or result <= 0.0:
        raise RuntimeError("exponential attenuation evaluation failed")
    return float(result)


def _quadrature_attenuation(
    family: str,
    ratio: float,
    *,
    quadrature_order: int,
    integration_limit: float,
) -> float:
    if ratio == 0.0:
        return 1.0
    nodes, weights = _legendre_rule(quadrature_order, integration_limit)
    covariance = normalized_radial_covariance(
        family, 2.0 * ratio * nodes
    )
    integrand = 2.0 * nodes * np.exp(-nodes**2) * covariance
    result = float(np.dot(weights, integrand))
    if not isfinite(result) or result <= 0.0 or result > 1.0 + 1.0e-12:
        raise RuntimeError("quadrature produced a non-physical attenuation")
    return min(1.0, result)


def gaussian_probe_filtered_variance_family(
    family: CovarianceFamily | str,
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    quadrature_order: int = 64,
    integration_limit: float = 10.0,
) -> FloatArray:
    """Return filtered variance for Gaussian probes and one covariance family."""

    selected = _family(str(family))
    amplitude = _positive("point_variance", point_variance)
    correlation = _positive("correlation_length", correlation_length)
    scales = _scales(probe_sigmas)
    result = np.empty(scales.size)
    for index, scale in enumerate(scales):
        ratio = float(scale / correlation)
        if selected == "gaussian":
            attenuation = 1.0 / (1.0 + 2.0 * ratio**2)
        elif selected == "exponential":
            attenuation = exponential_gaussian_probe_attenuation(ratio)
        else:
            attenuation = _quadrature_attenuation(
                selected,
                ratio,
                quadrature_order=quadrature_order,
                integration_limit=integration_limit,
            )
        result[index] = amplitude * attenuation
    if not np.all(np.isfinite(result)) or np.any(result <= 0.0):
        raise RuntimeError("filtered variances are non-physical")
    return _readonly(result)


@dataclass(frozen=True)
class ThreeScaleGaussianClosure:
    probe_sigmas: FloatArray
    effective_variances: FloatArray
    interpolated_middle_reciprocal_variance: float
    signed_reciprocal_residual: float
    normalized_reciprocal_residual: float


def three_scale_gaussian_closure(
    probe_sigmas: ArrayLike,
    effective_variances: ArrayLike,
) -> ThreeScaleGaussianClosure:
    """Test reciprocal affinity in s**2 for exactly three scales."""

    scales = _scales(probe_sigmas, minimum_size=3, increasing=True)
    if scales.size != 3:
        raise ValueError(
            "three_scale_gaussian_closure requires exactly three scales"
        )
    values = _variances(effective_variances, 3)
    squared = scales**2
    reciprocal = 1.0 / values
    fraction = float(
        (squared[1] - squared[0]) / (squared[2] - squared[0])
    )
    interpolated = float(
        reciprocal[0]
        + fraction * (reciprocal[2] - reciprocal[0])
    )
    residual = float(reciprocal[1] - interpolated)
    normalization = float(np.max(np.abs(reciprocal)))
    return ThreeScaleGaussianClosure(
        scales,
        values,
        interpolated,
        residual,
        residual / normalization,
    )


@dataclass(frozen=True)
class GaussianPairwiseInversions:
    pair_indices: NDArray[np.int64]
    point_variances: FloatArray
    correlation_lengths: FloatArray
    point_variance_spread_ratio: float
    correlation_length_spread_ratio: float


def _invert_pair(
    variance_1: float,
    variance_2: float,
    scale_1: float,
    scale_2: float,
) -> tuple[float, float]:
    x1, x2 = scale_1**2, scale_2**2
    y1, y2 = 1.0 / variance_1, 1.0 / variance_2
    slope = (y2 - y1) / (x2 - x1)
    intercept = (x2 * y1 - x1 * y2) / (x2 - x1)
    if not isfinite(slope) or slope <= 0.0:
        raise ValueError("effective variance must decrease with probe scale")
    if not isfinite(intercept) or intercept <= 0.0:
        raise ValueError(
            "pair implies a non-positive Gaussian point variance"
        )
    correlation_squared = 2.0 * intercept / slope
    if not isfinite(correlation_squared) or correlation_squared <= 0.0:
        raise ValueError(
            "pair implies a non-positive Gaussian correlation length"
        )
    return 1.0 / intercept, sqrt(correlation_squared)


def pairwise_gaussian_inversions(
    probe_sigmas: ArrayLike,
    effective_variances: ArrayLike,
) -> GaussianPairwiseInversions:
    """Infer Gaussian parameters independently from every scale pair."""

    scales = _scales(probe_sigmas, minimum_size=2, increasing=True)
    values = _variances(effective_variances, scales.size)
    pairs = list(combinations(range(scales.size), 2))
    parameters = [
        _invert_pair(
            float(values[i]),
            float(values[j]),
            float(scales[i]),
            float(scales[j]),
        )
        for i, j in pairs
    ]
    amplitudes = np.array([item[0] for item in parameters])
    correlations = np.array([item[1] for item in parameters])
    pair_indices = np.array(pairs, dtype=np.int64)
    pair_indices.setflags(write=False)
    return GaussianPairwiseInversions(
        pair_indices,
        _readonly(amplitudes),
        _readonly(correlations),
        float(np.max(amplitudes) / np.min(amplitudes)),
        float(np.max(correlations) / np.min(correlations)),
    )


@dataclass(frozen=True)
class GaussianSurrogateFit:
    point_variance: float
    correlation_length: float
    predicted_variance: FloatArray
    log_residuals: FloatArray
    rms_log_error: float
    maximum_relative_error: float
    objective_value: float
    iterations: int


def fit_gaussian_surrogate_log_variance(
    probe_sigmas: ArrayLike,
    effective_variances: ArrayLike,
    *,
    weights: ArrayLike | None = None,
    log_correlation_tolerance: float = 1.0e-12,
    maximum_iterations: int = 256,
) -> GaussianSurrogateFit:
    """Fit a Gaussian surrogate by weighted log-variance least squares."""

    scales = _scales(probe_sigmas, minimum_size=2, increasing=True)
    values = _variances(effective_variances, scales.size)
    positive_scales = scales[scales > 0.0]
    if positive_scales.size == 0:
        raise ValueError("at least one probe scale must be positive")

    if weights is None:
        normalized_weights = np.full(scales.size, 1.0 / scales.size)
    else:
        weight_array = np.array(weights, dtype=float, copy=True)
        if weight_array.shape != (scales.size,):
            raise ValueError(f"weights must have shape ({scales.size},)")
        if not np.all(np.isfinite(weight_array)) or np.any(
            weight_array <= 0.0
        ):
            raise ValueError("weights must be finite and positive")
        normalized_weights = weight_array / np.sum(weight_array)

    tolerance = _positive(
        "log_correlation_tolerance", log_correlation_tolerance
    )
    if isinstance(maximum_iterations, bool) or not isinstance(
        maximum_iterations, (int, np.integer)
    ) or maximum_iterations <= 0:
        raise ValueError("maximum_iterations must be a positive integer")

    log_values = np.log(values)
    log_offset = float(np.dot(normalized_weights, log_values))
    centered_log_values = log_values - log_offset
    reference_scale = exp(float(np.mean(np.log(positive_scales))))
    normalized_squared = (scales / reference_scale) ** 2

    def profile(log_ratio: float) -> tuple[float, float, float]:
        q = 2.0 * normalized_squared * exp(-2.0 * log_ratio)
        denominator = np.log1p(q)
        transition = q / (1.0 + q)
        centered_log_amplitude = float(
            np.dot(
                normalized_weights,
                centered_log_values + denominator,
            )
        )
        residuals = (
            centered_log_amplitude
            - denominator
            - centered_log_values
        )
        objective = float(np.dot(normalized_weights, residuals**2))
        derivative = float(
            4.0 * np.dot(normalized_weights, residuals * transition)
        )
        return (
            objective,
            centered_log_amplitude + log_offset,
            derivative,
        )

    lower = log(float(np.min(positive_scales) / reference_scale)) - 12.0
    upper = log(float(np.max(positive_scales) / reference_scale)) + 12.0
    _, _, derivative_lower = profile(lower)
    _, _, derivative_upper = profile(upper)
    if derivative_lower > 0.0 or derivative_upper < 0.0:
        raise RuntimeError("failed to bracket Gaussian surrogate optimum")

    iterations = 0
    while iterations < int(maximum_iterations):
        if upper - lower <= tolerance:
            break
        midpoint = 0.5 * (lower + upper)
        _, _, derivative_midpoint = profile(midpoint)
        if derivative_midpoint > 0.0:
            upper = midpoint
        else:
            lower = midpoint
        iterations += 1

    log_ratio = 0.5 * (lower + upper)
    objective, log_amplitude, _ = profile(log_ratio)
    correlation = reference_scale * exp(log_ratio)
    amplitude = exp(log_amplitude)
    predicted = amplitude / (
        1.0 + 2.0 * normalized_squared / exp(2.0 * log_ratio)
    )
    residuals = np.log(predicted) - log_values
    relative_errors = predicted / values - 1.0
    return GaussianSurrogateFit(
        amplitude,
        correlation,
        _readonly(predicted),
        _readonly(residuals),
        float(sqrt(np.dot(normalized_weights, residuals**2))),
        float(np.max(np.abs(relative_errors))),
        objective,
        iterations,
    )


@dataclass(frozen=True)
class CovarianceFamilyMisspecification:
    true_family: str
    true_point_variance: float
    true_correlation_length: float
    probe_sigmas: FloatArray
    true_filtered_variance: FloatArray
    all_three_scale_indices: NDArray[np.int64]
    normalized_three_scale_residuals: FloatArray
    maximum_absolute_three_scale_residual: float
    pairwise_inversions: GaussianPairwiseInversions
    gaussian_surrogate: GaussianSurrogateFit
    point_variance_bias_ratio: float
    correlation_length_bias_ratio: float


def covariance_family_misspecification_diagnostics(
    true_family: CovarianceFamily | str,
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    fit_weights: ArrayLike | None = None,
    quadrature_order: int = 64,
    integration_limit: float = 10.0,
) -> CovarianceFamilyMisspecification:
    """Generate one family and diagnose a misspecified Gaussian inverse."""

    selected = _family(str(true_family))
    amplitude = _positive("point_variance", point_variance)
    correlation = _positive("correlation_length", correlation_length)
    scales = _scales(probe_sigmas, minimum_size=3, increasing=True)
    filtered = gaussian_probe_filtered_variance_family(
        selected,
        amplitude,
        correlation,
        scales,
        quadrature_order=quadrature_order,
        integration_limit=integration_limit,
    )

    triples = list(combinations(range(scales.size), 3))
    residuals = np.array(
        [
            three_scale_gaussian_closure(
                scales[list(indices)],
                filtered[list(indices)],
            ).normalized_reciprocal_residual
            for indices in triples
        ]
    )
    triple_indices = np.array(triples, dtype=np.int64)
    triple_indices.setflags(write=False)
    pairwise = pairwise_gaussian_inversions(scales, filtered)
    surrogate = fit_gaussian_surrogate_log_variance(
        scales,
        filtered,
        weights=fit_weights,
    )
    return CovarianceFamilyMisspecification(
        selected,
        amplitude,
        correlation,
        scales,
        filtered,
        triple_indices,
        _readonly(residuals),
        float(np.max(np.abs(residuals))),
        pairwise,
        surrogate,
        surrogate.point_variance / amplitude,
        surrogate.correlation_length / correlation,
    )
