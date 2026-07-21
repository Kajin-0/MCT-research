"""Depth-kernel filtering benchmarks for stationary composition disorder.

The functions in this module quantify how a normalized exponential depth
sensitivity filters a one-dimensional stationary covariance in a finite slab.
They provide exact semi-infinite formulas, an exact finite-slab result for
exponential covariance, and a deterministic Gauss--Legendre reference
integrator.

This layer does not model optical transmission, edge extraction, detector
cutoff, photoluminescence, or microscopic Kane disorder.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erfc, exp, expm1, isfinite, pi, sqrt
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder import GaussianCovariance

FloatArray = NDArray[np.float64]
IlluminationSide = Literal["front", "back"]


def _finite_positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _validated_quadrature_order(order: int) -> int:
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise ValueError("quadrature_order must be an integer")
    result = int(order)
    if result < 2 or result > 2048:
        raise ValueError("quadrature_order must lie between 2 and 2048")
    return result


@dataclass(frozen=True)
class ExponentialCovariance1D:
    """Stationary one-dimensional exponential covariance.

    ``C(dz) = variance * exp(-abs(dz)/correlation_length)``.
    The correlation length is therefore the ``1/e`` lag.
    """

    variance: float
    correlation_length: float

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "variance",
            _finite_positive_scalar("variance", self.variance),
        )
        object.__setattr__(
            self,
            "correlation_length",
            _finite_positive_scalar("correlation_length", self.correlation_length),
        )

    @property
    def dimension(self) -> int:
        return 1

    def covariance(self, displacement: float) -> float:
        lag = float(displacement)
        if not isfinite(lag):
            raise ValueError("displacement must be finite")
        return float(self.variance * exp(-abs(lag) / self.correlation_length))


@dataclass(frozen=True)
class ExponentialDepthKernel:
    """Normalized exponential depth sensitivity in a finite slab.

    For front incidence,

    ``w(z) = a exp(-a z)/(1-exp(-a d))``.

    For back incidence, the kernel is reflected about the slab midplane.
    ``attenuation_coefficient`` and ``thickness`` must use reciprocal units.
    """

    attenuation_coefficient: float
    thickness: float
    side: IlluminationSide = "front"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "attenuation_coefficient",
            _finite_positive_scalar(
                "attenuation_coefficient", self.attenuation_coefficient
            ),
        )
        object.__setattr__(
            self,
            "thickness",
            _finite_positive_scalar("thickness", self.thickness),
        )
        if self.side not in ("front", "back"):
            raise ValueError("side must be 'front' or 'back'")

    @property
    def normalization_denominator(self) -> float:
        """Return ``1-exp(-a d)`` using a cancellation-safe evaluation."""

        return float(-expm1(-self.attenuation_coefficient * self.thickness))

    def weight(self, depth: ArrayLike) -> float | FloatArray:
        """Evaluate the normalized kernel at one or more depths."""

        values = np.asarray(depth, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("depth must contain only finite values")
        tolerance = 32.0 * np.finfo(float).eps * max(1.0, self.thickness)
        if np.any(values < -tolerance) or np.any(values > self.thickness + tolerance):
            raise ValueError("depth must lie within the finite slab")
        clipped = np.clip(values, 0.0, self.thickness)
        optical_depth = clipped if self.side == "front" else self.thickness - clipped
        result = (
            self.attenuation_coefficient
            * np.exp(-self.attenuation_coefficient * optical_depth)
            / self.normalization_denominator
        )
        if result.ndim == 0:
            return float(result)
        return np.asarray(result, dtype=float)


def semi_infinite_exponential_depth_ratio(
    attenuation_coefficient: float,
    correlation_length: float,
) -> float:
    """Return the semi-infinite variance ratio for exponential covariance.

    ``ratio = a xi/(1+a xi)``.
    """

    attenuation = _finite_positive_scalar(
        "attenuation_coefficient", attenuation_coefficient
    )
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    product = attenuation * correlation
    if not isfinite(product):
        return 1.0
    return float(product / (1.0 + product))


def _large_argument_gaussian_ratio(product: float) -> float:
    """Evaluate the large-``a xi`` asymptotic series without overflow."""

    inverse_squared = 1.0 / (product * product)
    total = 1.0
    term = 1.0
    previous_magnitude = abs(term)
    for order in range(1, 64):
        term *= -(2 * order - 1) * inverse_squared
        magnitude = abs(term)
        if magnitude > previous_magnitude:
            break
        total += term
        if magnitude <= np.finfo(float).eps * abs(total):
            break
        previous_magnitude = magnitude
    return float(total)


def semi_infinite_gaussian_depth_ratio(
    attenuation_coefficient: float,
    correlation_length: float,
) -> float:
    """Return the semi-infinite variance ratio for Gaussian covariance.

    The exact expression is

    ``sqrt(pi/2) q exp(q**2/2) erfc(q/sqrt(2))``, where ``q=a xi``.

    For large ``q`` the direct form overflows even though the ratio tends to one,
    so an optimally truncated asymptotic series is used beyond ``q=20``.
    """

    attenuation = _finite_positive_scalar(
        "attenuation_coefficient", attenuation_coefficient
    )
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    product = attenuation * correlation
    if not isfinite(product):
        return 1.0
    if product > 20.0:
        ratio = _large_argument_gaussian_ratio(product)
    else:
        ratio = (
            sqrt(pi / 2.0)
            * product
            * exp(0.5 * product * product)
            * erfc(product / sqrt(2.0))
        )
    if not 0.0 < ratio <= 1.0:
        raise RuntimeError("Gaussian semi-infinite ratio left its physical interval")
    return float(ratio)


def _thin_slab_exponential_ratio_series(
    attenuation_coefficient: float,
    inverse_correlation_length: float,
    thickness: float,
) -> float:
    """Fifth-order removable-limit series for a thin slab."""

    a = attenuation_coefficient
    b = inverse_correlation_length
    d = thickness
    return float(
        1.0
        - b * d / 3.0
        + b**2 * d**2 / 12.0
        + (a**2 * b / 90.0 - b**3 / 60.0) * d**3
        + b**2 * (-a**2 / 240.0 + b**2 / 360.0) * d**4
        + (-a**4 * b / 2520.0 + a**2 * b**3 / 1008.0 - b**5 / 2520.0)
        * d**5
    )


def _weighted_exponential_difference(
    attenuation_coefficient: float,
    inverse_correlation_length: float,
    thickness: float,
) -> float:
    """Return the second exact finite-slab integral without overflow."""

    a = attenuation_coefficient
    b = inverse_correlation_length
    d = thickness
    difference = a - b
    scaled_difference = difference * d
    if abs(scaled_difference) < 1.0e-6:
        y = scaled_difference
        exponential_relative = (
            1.0
            + y / 2.0
            + y**2 / 6.0
            + y**3 / 24.0
            + y**4 / 120.0
            + y**5 / 720.0
        )
        return float(d * exp(-2.0 * a * d) * exponential_relative)
    if scaled_difference > 0.0:
        return float(
            exp(-(a + b) * d)
            * (-expm1(-scaled_difference))
            / difference
        )
    return float(exp(-2.0 * a * d) * expm1(scaled_difference) / difference)


def finite_slab_exponential_depth_ratio(
    attenuation_coefficient: float,
    correlation_length: float,
    thickness: float,
) -> float:
    """Return the exact finite-slab ratio for exponential covariance.

    The normalized exponential kernel may be incident from either side; reflection
    symmetry makes the variance identical for a stationary covariance in a
    homogeneous slab.
    """

    attenuation = _finite_positive_scalar(
        "attenuation_coefficient", attenuation_coefficient
    )
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    slab = _finite_positive_scalar("thickness", thickness)
    inverse_correlation = 1.0 / correlation

    if max(attenuation * slab, inverse_correlation * slab) < 1.0e-3:
        ratio = _thin_slab_exponential_ratio_series(
            attenuation,
            inverse_correlation,
            slab,
        )
    else:
        first_integral = -expm1(
            -(attenuation + inverse_correlation) * slab
        ) / (attenuation + inverse_correlation)
        second_integral = _weighted_exponential_difference(
            attenuation,
            inverse_correlation,
            slab,
        )
        normalization = -expm1(-attenuation * slab)
        ratio = attenuation * (first_integral - second_integral) / normalization**2

    tolerance = 256.0 * np.finfo(float).eps
    if not isfinite(ratio) or ratio <= 0.0 or ratio > 1.0 + tolerance:
        raise RuntimeError("finite-slab exponential ratio left its physical interval")
    return float(min(ratio, 1.0))


def finite_slab_depth_effective_variance(
    covariance: GaussianCovariance | ExponentialCovariance1D,
    kernel: ExponentialDepthKernel,
    *,
    quadrature_order: int = 96,
) -> float:
    """Numerically evaluate finite-slab depth-filtered variance.

    Deterministic Gauss--Legendre quadrature discretizes the normalized kernel,
    then evaluates the covariance quadratic form.  This is a reference integrator
    for analytical validation, not an optical forward model.
    """

    if not isinstance(kernel, ExponentialDepthKernel):
        raise TypeError("kernel must be an ExponentialDepthKernel")
    if not isinstance(covariance, (GaussianCovariance, ExponentialCovariance1D)):
        raise TypeError(
            "covariance must be a one-dimensional GaussianCovariance or "
            "ExponentialCovariance1D"
        )
    if isinstance(covariance, GaussianCovariance) and covariance.dimension != 1:
        raise ValueError("Gaussian covariance must be one-dimensional for depth filtering")

    order = _validated_quadrature_order(quadrature_order)
    canonical_nodes, canonical_weights = np.polynomial.legendre.leggauss(order)
    depth = 0.5 * kernel.thickness * (canonical_nodes + 1.0)
    integration_weights = 0.5 * kernel.thickness * canonical_weights
    weighted_kernel = integration_weights * np.asarray(kernel.weight(depth), dtype=float)
    numerical_normalization = float(np.sum(weighted_kernel))
    if not isfinite(numerical_normalization) or numerical_normalization <= 0.0:
        raise RuntimeError("quadrature produced an invalid kernel normalization")
    weighted_kernel = weighted_kernel / numerical_normalization

    lags = np.abs(depth[:, None] - depth[None, :])
    if isinstance(covariance, ExponentialCovariance1D):
        covariance_matrix = covariance.variance * np.exp(
            -lags / covariance.correlation_length
        )
        point_variance = covariance.variance
    else:
        correlation_variance = float(np.asarray(covariance.correlation_matrix)[0, 0])
        covariance_matrix = covariance.variance * np.exp(
            -0.5 * lags**2 / correlation_variance
        )
        point_variance = covariance.variance

    result = float(weighted_kernel @ covariance_matrix @ weighted_kernel)
    tolerance = 1024.0 * np.finfo(float).eps * point_variance
    if not isfinite(result) or result <= 0.0 or result > point_variance + tolerance:
        raise RuntimeError("finite-slab quadrature left the physical variance interval")
    return float(min(result, point_variance))
