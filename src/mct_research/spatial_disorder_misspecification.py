"""Covariance-family misspecification diagnostics for multiscale disorder.

The declared inverse model is the isotropic two-dimensional Gaussian
covariance observed with Gaussian probes,

    V_G(s) = A / (1 + 2 s**2 / xi**2).

Its reciprocal is affine in s**2, so three distinct probe scales provide the
first exact closure test. This module compares that inverse against several
isotropic covariance families normalized to the same point variance and the
same two-dimensional integral correlation area, 2*pi*xi**2.

The calculations are controlled synthetic diagnostics. They do not select a
covariance family for HgCdTe and do not fit specimen data.
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

SUPPORTED_COVARIANCE_FAMILIES: tuple[str, ...] = (
    "gaussian",
    "exponential",
    "matern32",
    "matern52",
)


def _finite_positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite_nonnegative_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _validated_family(family: str) -> str:
    if family not in SUPPORTED_COVARIANCE_FAMILIES:
        allowed = ", ".join(SUPPORTED_COVARIANCE_FAMILIES)
        raise ValueError(f"family must be one of: {allowed}")
    return family


def _validated_scales(
    probe_sigmas: ArrayLike,
    *,
    minimum_size: int = 1,
    strictly_increasing: bool = False,
) -> FloatArray:
    scales = np.array(probe_sigmas, dtype=float, copy=True)
    if scales.ndim != 1 or scales.size < minimum_size:
        raise ValueError(
            f"probe_sigmas must be a one-dimensional array with at least "
            f"{minimum_size} entries"
        )
    if not np.all(np.isfinite(scales)):
        raise ValueError("probe_sigmas must contain only finite values")
    if np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be non-negative")
    if strictly_increasing and np.any(np.diff(scales) <= 0.0):
        raise ValueError("probe_sigmas must be strictly increasing")
    scales.setflags(write=False)
    return scales


def _validated_variances(
    effective_variances: ArrayLike,
    *,
    expected_size: int,
) -> FloatArray:
    values = np.array(effective_variances, dtype=float, copy=True)
    if values.shape != (expected_size,):
        raise ValueError(f"effective_variances must have shape ({expected_size},)")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("effective_variances must be finite and positive")
    values.setflags(write=False)
    return values


def _read_only_array(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def normalized_radial_covariance(
    family: CovarianceFamily | str,
    radius_over_correlation_length: ArrayLike,
) -> FloatArray:
    """Return ``C(r)/C(0)`` for a supported isotropic covariance family.

    The scale parameter ``xi`` is chosen so every family has the same
    two-dimensional integral correlation area,

    ``integral C(r)/C(0) d^2r = 2*pi*xi**2``.
    """

    selected = _validated_family(str(family))
    radius = np.array(radius_over_correlation_length, dtype=float, copy=True)
    if not np.all(np.isfinite(radius)) or np.any(radius < 0.0):
        raise ValueError(
            "radius_over_correlation_length must be finite and non-negative"
        )

    if selected == "gaussian":
        values = np.exp(-0.5 * radius**2)
    elif selected == "exponential":
        values = np.exp(-radius)
    elif selected == "matern32":
        scaled = sqrt(3.0) * radius
        values = (1.0 + scaled) * np.exp(-scaled)
    else:
        scaled = sqrt(5.0) * radius
        values = (1.0 + scaled + scaled**2 / 3.0) * np.exp(-scaled)

    return _read_only_array(values)


@lru_cache(maxsize=None)
def _legendre_rule(order: int, integration_limit: float) -> tuple[FloatArray, FloatArray]:
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise ValueError("quadrature_order must be an integer")
    if order < 16:
        raise ValueError("quadrature_order must be at least 16")
    limit = _finite_positive_scalar("integration_limit", integration_limit)
    nodes, weights = leggauss(int(order))
    radial_nodes = 0.5 * limit * (nodes + 1.0)
    radial_weights = 0.5 * limit * weights
    return _read_only_array(radial_nodes), _read_only_array(radial_weights)


def exponential_gaussian_probe_attenuation(
    probe_to_correlation_ratio: float,
) -> float:
    """Return the exact exponential-covariance attenuation in two dimensions.

    For ``u=s/xi``,

    ``V(s)/A = 1 - sqrt(pi) u exp(u**2) erfc(u)``.

    The asymptotic expansion of the small positive remainder is used for large
    ``u`` to avoid overflow and subtractive cancellation.
    """

    ratio = _finite_nonnegative_scalar(
        "probe_to_correlation_ratio", probe_to_correlation_ratio
    )
    if ratio == 0.0:
        return 1.0
    if ratio <= 8.0:
        return float(1.0 - sqrt(pi) * ratio * exp(ratio**2) * erfc(ratio))

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

    radial_nodes, radial_weights = _legendre_rule(
        quadrature_order, float(integration_limit)
    )
    # If Y has density 2*y*exp(-y**2), then H=2*s*Y is the radial
    # displacement between two independent 2D Gaussian probe draws.
    normalized_radius = 2.0 * ratio * radial_nodes
    covariance = normalized_radial_covariance(family, normalized_radius)
    integrand = 2.0 * radial_nodes * np.exp(-radial_nodes**2) * covariance
    attenuation = float(np.dot(radial_weights, integrand))
    if not isfinite(attenuation) or attenuation <= 0.0 or attenuation > 1.0 + 1e-12:
        raise RuntimeError("quadrature produced a non-physical attenuation")
    return min(1.0, attenuation)


def gaussian_probe_filtered_variance_family(
    family: CovarianceFamily | str,
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    quadrature_order: int = 64,
    integration_limit: float = 10.0,
) -> FloatArray:
    """Return Gaussian-probe filtered variance for a covariance family.

    Non-Gaussian Matérn families are evaluated by deterministic Gauss-Legendre
    quadrature of

    ``V(s)/A = integral 2*y*exp(-y**2) c(2*(s/xi)*y) dy``.

    Gaussian and exponential families use exact expressions.
    """

    selected = _validated_family(str(family))
    variance = _finite_positive_scalar("point_variance", point_variance)
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    scales = _validated_scales(probe_sigmas)

    values = np.empty(scales.size, dtype=float)
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
        values[index] = variance * attenuation

    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise RuntimeError("filtered variances are non-physical")
    return _read_only_array(values)


@dataclass(frozen=True)
class ThreeScaleGaussianClosure:
    """Exact reciprocal-affinity closure test for three distinct scales."""

    probe_sigmas: FloatArray
    effective_variances: FloatArray
    interpolated_middle_reciprocal_variance: float
    signed_reciprocal_residual: float
    normalized_reciprocal_residual: float


def three_scale_gaussian_closure(
    probe_sigmas: ArrayLike,
    effective_variances: ArrayLike,
) -> ThreeScaleGaussianClosure:
    """Test whether three measurements satisfy the Gaussian inverse exactly."""

    scales = _validated_scales(
        probe_sigmas, minimum_size=3, strictly_increasing=True
    )
    if scales.size != 3:
        raise ValueError("three_scale_gaussian_closure requires exactly three scales")
    variances = _validated_variances(effective_variances, expected_size=3)

    x = scales**2
    y = 1.0 / variances
    fraction = float((x[1] - x[0]) / (x[2] - x[0]))
    interpolated = float(y[0] + fraction * (y[2] - y[0]))
    residual = float(y[1] - interpolated)
    scale = max(abs(float(y[0])), abs(float(y[1])), abs(float(y[2])))

    return ThreeScaleGaussianClosure(
        probe_sigmas=scales,
        effective_variances=variances,
        interpolated_middle_reciprocal_variance=interpolated,
        signed_reciprocal_residual=residual,
        normalized_reciprocal_residual=float(residual / scale),
    )


@dataclass(frozen=True)
class GaussianPairwiseInversions:
    """Gaussian parameters inferred independently from every scale pair."""

    pair_indices: NDArray[np.int64]
    point_variances: FloatArray
    correlation_lengths: FloatArray
    point_variance_spread_ratio: float
    correlation_length_spread_ratio: float


def _two_scale_gaussian_inversion(
    variance_1: float,
    variance_2: float,
    scale_1: float,
    scale_2: float,
) -> tuple[float, float]:
    x1 = scale_1**2
    x2 = scale_2**2
    y1 = 1.0 / variance_1
    y2 = 1.0 / variance_2
    slope = (y2 - y1) / (x2 - x1)
    intercept = (x2 * y1 - x1 * y2) / (x2 - x1)
    if not isfinite(slope) or slope <= 0.0:
        raise ValueError("effective variance must decrease with probe scale")
    if not isfinite(intercept) or intercept <= 0.0:
        raise ValueError("pair implies a non-positive Gaussian point variance")
    point_variance = 1.0 / intercept
    correlation_squared = 2.0 * intercept / slope
    if not isfinite(correlation_squared) or correlation_squared <= 0.0:
        raise ValueError("pair implies a non-positive Gaussian correlation length")
    return float(point_variance), float(sqrt(correlation_squared))


def pairwise_gaussian_inversions(
    probe_sigmas: ArrayLike,
    effective_variances: ArrayLike,
) -> GaussianPairwiseInversions:
    """Fit the Gaussian inverse to every scale pair independently."""

    scales = _validated_scales(
        probe_sigmas, minimum_size=2, strictly_increasing=True
    )
    variances = _validated_variances(
        effective_variances, expected_size=scales.size
    )

    pairs = list(combinations(range(scales.size), 2))
    parameters = [
        _two_scale_gaussian_inversion(
            float(variances[i]),
            float(variances[j]),
            float(scales[i]),
            float(scales[j]),
        )
        for i, j in pairs
    ]
    point_variances = np.array([item[0] for item in parameters], dtype=float)
    correlation_lengths = np.array([item[1] for item in parameters], dtype=float)
    pair_array = np.array(pairs, dtype=np.int64)
    pair_array.setflags(write=False)

    return GaussianPairwiseInversions(
        pair_indices=pair_array,
        point_variances=_read_only_array(point_variances),
        correlation_lengths=_read_only_array(correlation_lengths),
        point_variance_spread_ratio=float(
            np.max(point_variances) / np.min(point_variances)
        ),
        correlation_length_spread_ratio=float(
            np.max(correlation_lengths) / np.min(correlation_lengths)
        ),
    )


@dataclass(frozen=True)
class GaussianSurrogateFit:
    """Best Gaussian surrogate under weighted log-variance least squares."""

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
    """Fit the best Gaussian surrogate to two or more positive variances.

    For each trial ``log xi``, the optimal ``log A`` is analytical. The
    remaining one-dimensional objective is minimized by a deterministic
    golden-section search.
    """

    scales = _validated_scales(
        probe_sigmas, minimum_size=2, strictly_increasing=True
    )
    variances = _validated_variances(
        effective_variances, expected_size=scales.size
    )
    positive_scales = scales[scales > 0.0]
    if positive_scales.size == 0:
        raise ValueError("at least one probe scale must be positive")

    if weights is None:
        normalized_weights = np.full(scales.size, 1.0 / scales.size)
    else:
        weight_array = np.array(weights, dtype=float, copy=True)
        if weight_array.shape != (scales.size,):
            raise ValueError(f"weights must have shape ({scales.size},)")
        if not np.all(np.isfinite(weight_array)) or np.any(weight_array <= 0.0):
            raise ValueError("weights must be finite and positive")
        normalized_weights = weight_array / np.sum(weight_array)

    tolerance = _finite_positive_scalar(
        "log_correlation_tolerance", log_correlation_tolerance
    )
    if isinstance(maximum_iterations, bool) or not isinstance(
        maximum_iterations, (int, np.integer)
    ):
        raise ValueError("maximum_iterations must be a positive integer")
    if maximum_iterations <= 0:
        raise ValueError("maximum_iterations must be a positive integer")

    log_observed = np.log(variances)
    scale_squared = scales**2

    def profile(log_correlation: float) -> tuple[float, float]:
        q = 2.0 * scale_squared * exp(-2.0 * log_correlation)
        log_denominator = np.log1p(q)
        log_amplitude = float(
            np.dot(normalized_weights, log_observed + log_denominator)
        )
        residuals = log_amplitude - log_denominator - log_observed
        objective = float(np.dot(normalized_weights, residuals**2))
        return objective, log_amplitude

    lower = log(float(np.min(positive_scales))) - 12.0
    upper = log(float(np.max(positive_scales))) + 12.0
    golden = 0.5 * (sqrt(5.0) - 1.0)
    left = upper - golden * (upper - lower)
    right = lower + golden * (upper - lower)
    f_left, _ = profile(left)
    f_right, _ = profile(right)

    iterations = 0
    while iterations < int(maximum_iterations):
        if upper - lower <= tolerance:
            break
        if f_left <= f_right:
            upper = right
            right = left
            f_right = f_left
            left = upper - golden * (upper - lower)
            f_left, _ = profile(left)
        else:
            lower = left
            left = right
            f_left = f_right
            right = lower + golden * (upper - lower)
            f_right, _ = profile(right)
        iterations += 1

    log_correlation = 0.5 * (lower + upper)
    objective, log_amplitude = profile(log_correlation)
    correlation = exp(log_correlation)
    amplitude = exp(log_amplitude)
    predicted = amplitude / (1.0 + 2.0 * scale_squared / correlation**2)
    log_residuals = np.log(predicted) - log_observed
    relative_errors = predicted / variances - 1.0

    return GaussianSurrogateFit(
        point_variance=float(amplitude),
        correlation_length=float(correlation),
        predicted_variance=_read_only_array(predicted),
        log_residuals=_read_only_array(log_residuals),
        rms_log_error=float(sqrt(np.dot(normalized_weights, log_residuals**2))),
        maximum_relative_error=float(np.max(np.abs(relative_errors))),
        objective_value=float(objective),
        iterations=iterations,
    )


@dataclass(frozen=True)
class CovarianceFamilyMisspecification:
    """Synthetic bias and closure diagnostics for one true covariance family."""

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

    selected = _validated_family(str(true_family))
    variance = _finite_positive_scalar("point_variance", point_variance)
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    scales = _validated_scales(
        probe_sigmas, minimum_size=3, strictly_increasing=True
    )
    filtered = gaussian_probe_filtered_variance_family(
        selected,
        variance,
        correlation,
        scales,
        quadrature_order=quadrature_order,
        integration_limit=integration_limit,
    )

    triple_indices = list(combinations(range(scales.size), 3))
    residuals = []
    for indices in triple_indices:
        closure = three_scale_gaussian_closure(
            scales[list(indices)],
            filtered[list(indices)],
        )
        residuals.append(closure.normalized_reciprocal_residual)

    triple_array = np.array(triple_indices, dtype=np.int64)
    triple_array.setflags(write=False)
    residual_array = np.array(residuals, dtype=float)
    pairwise = pairwise_gaussian_inversions(scales, filtered)
    surrogate = fit_gaussian_surrogate_log_variance(
        scales,
        filtered,
        weights=fit_weights,
    )

    return CovarianceFamilyMisspecification(
        true_family=selected,
        true_point_variance=variance,
        true_correlation_length=correlation,
        probe_sigmas=scales,
        true_filtered_variance=filtered,
        all_three_scale_indices=triple_array,
        normalized_three_scale_residuals=_read_only_array(residual_array),
        maximum_absolute_three_scale_residual=float(
            np.max(np.abs(residual_array))
        ),
        pairwise_inversions=pairwise,
        gaussian_surrogate=surrogate,
        point_variance_bias_ratio=float(surrogate.point_variance / variance),
        correlation_length_bias_ratio=float(
            surrogate.correlation_length / correlation
        ),
    )
