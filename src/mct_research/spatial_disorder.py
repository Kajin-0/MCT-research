"""Exact Gaussian spatial-disorder and measurement-kernel benchmarks.

This module implements the first executable tranche of the Stage 1 spatial-
disorder program.  It treats the Cd fraction as a stationary Gaussian-correlated
field and the measurement as a normalized Gaussian spatial kernel.  The module
contains exact analytical variance filtering and a two-scale inversion for the
isotropic two-dimensional benchmark.

It does not implement optical absorption, detector cutoff, photoluminescence,
random-mass Kane physics, or a universal HgCdTe covariance law.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatMatrix = NDArray[np.float64]
FloatVector = NDArray[np.float64]


_SYMMETRY_RTOL = 1.0e-12
_SYMMETRY_ATOL_FACTOR = 1.0e-14
_PSD_TOLERANCE_FACTOR = 64.0
_DEGENERACY_TOLERANCE_FACTOR = 64.0


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


def _positive_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, (int, np.integer)):
        raise ValueError("dimension must be a positive integer")
    result = int(dimension)
    if result <= 0:
        raise ValueError("dimension must be a positive integer")
    return result


def _validated_symmetric_matrix(
    name: str,
    value: ArrayLike,
    *,
    positive_definite: bool,
) -> FloatMatrix:
    matrix = np.array(value, dtype=float, copy=True)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError(f"{name} must be a non-empty square matrix")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must contain only finite values")

    scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    if not np.allclose(
        matrix,
        matrix.T,
        rtol=_SYMMETRY_RTOL,
        atol=_SYMMETRY_ATOL_FACTOR * scale,
    ):
        raise ValueError(f"{name} must be symmetric")

    if positive_definite:
        try:
            np.linalg.cholesky(matrix)
        except np.linalg.LinAlgError as exc:
            raise ValueError(f"{name} must be positive definite") from exc
    else:
        eigenvalues = np.linalg.eigvalsh(matrix)
        tolerance = (
            _PSD_TOLERANCE_FACTOR
            * np.finfo(float).eps
            * max(1.0, float(np.max(np.abs(eigenvalues))), scale)
        )
        if float(np.min(eigenvalues)) < -tolerance:
            raise ValueError(f"{name} must be positive semidefinite")

    matrix.setflags(write=False)
    return matrix


def _validated_displacement(displacement: ArrayLike, dimension: int) -> FloatVector:
    vector = np.asarray(displacement, dtype=float)
    if vector.shape != (dimension,):
        raise ValueError(f"displacement must have shape ({dimension},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("displacement must contain only finite values")
    return vector


@dataclass(frozen=True)
class GaussianCovariance:
    """Stationary Gaussian covariance for a dimensionless composition field.

    The covariance is

    ``C(h) = variance * exp(-0.5 * h.T @ Lambda^-1 @ h)``,

    where ``correlation_matrix`` is ``Lambda``.  The square roots of the
    eigenvalues of ``Lambda`` are Gaussian correlation standard deviations.  A
    principal-axis displacement equal to one such scale reduces the covariance
    to ``exp(-1/2)`` of its point value.
    """

    variance: float
    correlation_matrix: ArrayLike

    correlation_length_convention: ClassVar[str] = (
        "sqrt(eigenvalue) gives the exp(-1/2) Gaussian correlation scale"
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "variance",
            _finite_positive_scalar("variance", self.variance),
        )
        object.__setattr__(
            self,
            "correlation_matrix",
            _validated_symmetric_matrix(
                "correlation_matrix",
                self.correlation_matrix,
                positive_definite=True,
            ),
        )

    @classmethod
    def isotropic(
        cls,
        variance: float,
        correlation_length: float,
        dimension: int,
    ) -> GaussianCovariance:
        """Construct an isotropic Gaussian covariance in ``dimension`` dimensions."""

        point_variance = _finite_positive_scalar("variance", variance)
        xi = _finite_positive_scalar("correlation_length", correlation_length)
        ndim = _positive_dimension(dimension)
        return cls(point_variance, np.eye(ndim, dtype=float) * xi**2)

    @property
    def dimension(self) -> int:
        """Return the spatial dimension."""

        return int(np.asarray(self.correlation_matrix).shape[0])

    def covariance(self, displacement: ArrayLike) -> float:
        """Evaluate ``C(h)`` for one displacement vector."""

        vector = _validated_displacement(displacement, self.dimension)
        quadratic_form = float(
            vector @ np.linalg.solve(np.asarray(self.correlation_matrix), vector)
        )
        return float(self.variance * exp(-0.5 * quadratic_form))


@dataclass(frozen=True)
class GaussianKernel:
    """Normalized Gaussian measurement kernel.

    ``covariance_matrix`` is the covariance of the specimen-plane kernel.  A
    positive-semidefinite matrix is permitted so that zero-width point-probe
    limits and lower-dimensional limiting kernels can be represented exactly.
    """

    covariance_matrix: ArrayLike

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "covariance_matrix",
            _validated_symmetric_matrix(
                "covariance_matrix",
                self.covariance_matrix,
                positive_definite=False,
            ),
        )

    @classmethod
    def isotropic(cls, probe_sigma: float, dimension: int) -> GaussianKernel:
        """Construct an isotropic Gaussian kernel with standard deviation ``s``."""

        sigma = _finite_nonnegative_scalar("probe_sigma", probe_sigma)
        ndim = _positive_dimension(dimension)
        return cls(np.eye(ndim, dtype=float) * sigma**2)

    @property
    def dimension(self) -> int:
        """Return the spatial dimension."""

        return int(np.asarray(self.covariance_matrix).shape[0])


@dataclass(frozen=True)
class GaussianTwoScaleInversion:
    """Exact isotropic two-dimensional inversion result."""

    point_variance: float
    correlation_length: float


def gaussian_gaussian_effective_variance(
    covariance: GaussianCovariance,
    kernel: GaussianKernel,
) -> float:
    """Return the exact variance after Gaussian-kernel averaging.

    The analytical identity is

    ``variance * det(I + 2 Sigma_w Lambda^-1)^(-1/2)``,

    evaluated through the equivalent stable log-determinant form

    ``variance * sqrt(det(Lambda) / det(Lambda + 2 Sigma_w))``.
    """

    if not isinstance(covariance, GaussianCovariance):
        raise TypeError("covariance must be a GaussianCovariance")
    if not isinstance(kernel, GaussianKernel):
        raise TypeError("kernel must be a GaussianKernel")
    if covariance.dimension != kernel.dimension:
        raise ValueError("covariance and kernel dimensions must match")

    correlation_matrix = np.asarray(covariance.correlation_matrix)
    kernel_matrix = np.asarray(kernel.covariance_matrix)
    filtered_matrix = correlation_matrix + 2.0 * kernel_matrix

    sign_correlation, logdet_correlation = np.linalg.slogdet(correlation_matrix)
    sign_filtered, logdet_filtered = np.linalg.slogdet(filtered_matrix)
    if sign_correlation <= 0.0 or sign_filtered <= 0.0:
        raise RuntimeError("validated covariance matrices produced a non-positive determinant")

    log_attenuation = 0.5 * (float(logdet_correlation) - float(logdet_filtered))
    return float(covariance.variance * exp(log_attenuation))


def isotropic_gaussian_effective_variance(
    point_variance: float,
    correlation_length: float,
    probe_sigma: float,
    *,
    dimension: int = 2,
) -> float:
    """Return the isotropic Gaussian effective variance.

    ``V = point_variance * (1 + 2 probe_sigma**2 / correlation_length**2)**(-d/2)``.
    The log-domain evaluation remains stable for very large scale ratios.
    """

    variance = _finite_positive_scalar("point_variance", point_variance)
    xi = _finite_positive_scalar("correlation_length", correlation_length)
    sigma = _finite_nonnegative_scalar("probe_sigma", probe_sigma)
    ndim = _positive_dimension(dimension)

    if sigma == 0.0:
        return variance

    log_scale_ratio_squared = 2.0 * (log(sigma) - log(xi))
    log_denominator = float(
        np.logaddexp(0.0, log(2.0) + log_scale_ratio_squared)
    )
    return float(exp(log(variance) - 0.5 * ndim * log_denominator))


def two_scale_gaussian_inversion(
    variance_at_s1: float,
    variance_at_s2: float,
    probe_sigma_1: float,
    probe_sigma_2: float,
) -> GaussianTwoScaleInversion:
    """Invert two isotropic two-dimensional Gaussian-kernel variances.

    The model is ``V(s) = sigma_x**2 / (1 + 2 s**2 / xi**2)``.  The
    implementation uses the equivalent line

    ``1/V(s) = 1/sigma_x**2 + 2 s**2/(sigma_x**2 xi**2)``

    because its slope and intercept provide stable physical validity checks.
    Equal probe sizes, equal effective variances, non-monotone data, and
    non-positive inferred parameters are rejected explicitly.
    """

    variance_1 = _finite_positive_scalar("variance_at_s1", variance_at_s1)
    variance_2 = _finite_positive_scalar("variance_at_s2", variance_at_s2)
    sigma_1 = _finite_nonnegative_scalar("probe_sigma_1", probe_sigma_1)
    sigma_2 = _finite_nonnegative_scalar("probe_sigma_2", probe_sigma_2)

    scale_1_squared = sigma_1**2
    scale_2_squared = sigma_2**2
    delta_scale_squared = scale_2_squared - scale_1_squared
    if delta_scale_squared == 0.0:
        raise ValueError("probe sizes must be distinct")
    if not isfinite(delta_scale_squared):
        raise ValueError("squared probe-size difference must be finite")

    inverse_variance_1 = 1.0 / variance_1
    inverse_variance_2 = 1.0 / variance_2
    delta_inverse_variance = inverse_variance_2 - inverse_variance_1
    inverse_scale = max(abs(inverse_variance_1), abs(inverse_variance_2))
    degeneracy_tolerance = (
        _DEGENERACY_TOLERANCE_FACTOR * np.finfo(float).eps * inverse_scale
    )
    if abs(delta_inverse_variance) <= degeneracy_tolerance:
        raise ValueError("two-scale inversion is degenerate because variances are equal")

    slope = delta_inverse_variance / delta_scale_squared
    if not isfinite(slope) or slope <= 0.0:
        raise ValueError("effective variance must decrease as probe size increases")

    intercept = (
        scale_2_squared * inverse_variance_1
        - scale_1_squared * inverse_variance_2
    ) / delta_scale_squared
    if not isfinite(intercept) or intercept <= 0.0:
        raise ValueError("two-scale data imply a non-positive point variance")

    point_variance = 1.0 / intercept
    correlation_length_squared = 2.0 * intercept / slope
    if (
        not isfinite(point_variance)
        or point_variance <= 0.0
        or not isfinite(correlation_length_squared)
        or correlation_length_squared <= 0.0
    ):
        raise ValueError("two-scale data imply non-physical Gaussian parameters")

    return GaussianTwoScaleInversion(
        point_variance=float(point_variance),
        correlation_length=float(correlation_length_squared**0.5),
    )
