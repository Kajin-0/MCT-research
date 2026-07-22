"""Exact sampling statistics for correlated Gaussian spatial-disorder maps.

A finite-resolution map contains correlated observations when neighboring probe
kernels sample overlapping material correlation volumes.  This module provides:

- exact cross covariance between two Gaussian-filtered measurements;
- covariance matrices for arbitrary sample centers and Gaussian kernels;
- exact Gaussian quadratic-form moments for the usual map sample variance;
- effective sample counts for map means and variance estimators;
- deterministic regular-grid construction.

The mathematics is model conditioned.  It does not identify a specimen
covariance, prescribe a universal scan pitch, or make correlated quadratic forms
exactly chi-square distributed.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder import GaussianCovariance, GaussianKernel

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


@dataclass(frozen=True)
class GaussianMapSamplingDiagnostics:
    """Exact first two moments for a finite correlated Gaussian map."""

    nominal_sample_count: int
    average_marginal_variance: float
    marginal_variance_relative_spread: float
    map_mean_variance: float
    map_mean_effective_sample_count: float
    naive_sample_variance_expectation: float
    naive_sample_variance_relative_bias: float
    naive_sample_variance_variance: float
    naive_sample_variance_relative_standard_deviation: float
    variance_effective_degrees_of_freedom: float
    covariance_condition_number: float


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _validated_positions(positions: ArrayLike, dimension: int | None = None) -> FloatMatrix:
    result = np.asarray(positions, dtype=float)
    if result.ndim != 2 or result.shape[0] == 0 or result.shape[1] == 0:
        raise ValueError("positions must have shape (sample_count, dimension)")
    if dimension is not None and result.shape[1] != dimension:
        raise ValueError(f"positions must have spatial dimension {dimension}")
    if not np.all(np.isfinite(result)):
        raise ValueError("positions must contain only finite values")
    return _read_only(result)


def _validated_map_covariance(covariance_matrix: ArrayLike) -> FloatMatrix:
    result = np.asarray(covariance_matrix, dtype=float)
    if result.ndim != 2 or result.shape[0] != result.shape[1] or result.shape[0] < 2:
        raise ValueError("covariance_matrix must be square with at least two samples")
    if not np.all(np.isfinite(result)):
        raise ValueError("covariance_matrix must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(result, ord=np.inf)))
    if not np.allclose(result, result.T, rtol=1.0e-12, atol=1.0e-14 * scale):
        raise ValueError("covariance_matrix must be symmetric")
    eigenvalues = np.linalg.eigvalsh(result)
    tolerance = 128.0 * np.finfo(float).eps * max(
        1.0,
        scale,
        float(np.max(np.abs(eigenvalues))),
    )
    if float(np.min(eigenvalues)) < -tolerance:
        raise ValueError("covariance_matrix must be positive semidefinite")
    diagonal = np.diag(result)
    if np.any(diagonal <= 0.0):
        raise ValueError("covariance_matrix diagonal must be positive")
    return _read_only(result)


def gaussian_filtered_cross_covariance(
    covariance: GaussianCovariance,
    kernel_i: GaussianKernel,
    kernel_j: GaussianKernel,
    displacement: ArrayLike,
) -> float:
    r"""Return exact covariance between two Gaussian-filtered measurements.

    For material covariance matrix :math:`\Lambda`, kernel covariance matrices
    :math:`\Sigma_i,\Sigma_j`, and center displacement :math:`\Delta r`,

    .. math::

       \operatorname{Cov}(X_i,X_j)=A
       \sqrt{\frac{\det\Lambda}
       {\det(\Lambda+\Sigma_i+\Sigma_j)}}
       \exp\left[-\frac12\Delta r^T
       (\Lambda+\Sigma_i+\Sigma_j)^{-1}\Delta r\right].
    """

    if not isinstance(covariance, GaussianCovariance):
        raise TypeError("covariance must be a GaussianCovariance")
    if not isinstance(kernel_i, GaussianKernel) or not isinstance(kernel_j, GaussianKernel):
        raise TypeError("kernel_i and kernel_j must be GaussianKernel instances")
    if covariance.dimension != kernel_i.dimension or covariance.dimension != kernel_j.dimension:
        raise ValueError("covariance and kernel dimensions must match")

    delta = np.asarray(displacement, dtype=float)
    if delta.shape != (covariance.dimension,):
        raise ValueError(f"displacement must have shape ({covariance.dimension},)")
    if not np.all(np.isfinite(delta)):
        raise ValueError("displacement must contain only finite values")

    material = np.asarray(covariance.correlation_matrix)
    combined = (
        material
        + np.asarray(kernel_i.covariance_matrix)
        + np.asarray(kernel_j.covariance_matrix)
    )
    sign_material, logdet_material = np.linalg.slogdet(material)
    sign_combined, logdet_combined = np.linalg.slogdet(combined)
    if sign_material <= 0.0 or sign_combined <= 0.0:
        raise RuntimeError("validated matrices produced a non-positive determinant")
    quadratic = float(delta @ np.linalg.solve(combined, delta))
    log_value = (
        np.log(covariance.variance)
        + 0.5 * (float(logdet_material) - float(logdet_combined))
        - 0.5 * quadratic
    )
    result = float(exp(log_value))
    if not isfinite(result) or result < 0.0:
        raise ArithmeticError("filtered cross covariance is non-finite")
    return result


def gaussian_map_covariance_matrix(
    covariance: GaussianCovariance,
    positions: ArrayLike,
    kernels: GaussianKernel | Sequence[GaussianKernel],
) -> FloatMatrix:
    """Return the exact covariance matrix for arbitrary sample centers.

    ``kernels`` may be one common kernel or one kernel per position.  The latter
    supports mixed-resolution maps without replacing the established single-
    kernel variance theorem.
    """

    if not isinstance(covariance, GaussianCovariance):
        raise TypeError("covariance must be a GaussianCovariance")
    points = _validated_positions(positions, covariance.dimension)
    sample_count = points.shape[0]

    if isinstance(kernels, GaussianKernel):
        kernel_list = [kernels] * sample_count
    else:
        kernel_list = list(kernels)
        if len(kernel_list) != sample_count:
            raise ValueError("kernels must contain one entry per position")
        if not all(isinstance(kernel, GaussianKernel) for kernel in kernel_list):
            raise TypeError("every kernel must be a GaussianKernel")
    if any(kernel.dimension != covariance.dimension for kernel in kernel_list):
        raise ValueError("covariance and kernel dimensions must match")

    result = np.empty((sample_count, sample_count), dtype=float)
    for row in range(sample_count):
        for column in range(row, sample_count):
            value = gaussian_filtered_cross_covariance(
                covariance,
                kernel_list[row],
                kernel_list[column],
                np.asarray(points[row]) - np.asarray(points[column]),
            )
            result[row, column] = value
            result[column, row] = value

    result = 0.5 * (result + result.T)
    result.setflags(write=False)
    return result


def regular_grid_positions(
    shape: Sequence[int],
    spacing: float | Sequence[float],
    *,
    origin: ArrayLike | None = None,
) -> FloatMatrix:
    """Return Cartesian regular-grid sample centers in row-major order."""

    dimensions = tuple(shape)
    if not dimensions or any(
        isinstance(value, bool) or int(value) != value or int(value) <= 0
        for value in dimensions
    ):
        raise ValueError("shape must contain positive integers")
    dimensions = tuple(int(value) for value in dimensions)
    ndim = len(dimensions)

    if np.isscalar(spacing):
        spacing_values = np.full(ndim, float(spacing), dtype=float)
    else:
        spacing_values = np.asarray(spacing, dtype=float)
        if spacing_values.shape != (ndim,):
            raise ValueError(f"spacing must have shape ({ndim},)")
    if not np.all(np.isfinite(spacing_values)) or np.any(spacing_values <= 0.0):
        raise ValueError("spacing must be finite and positive")

    if origin is None:
        origin_values = np.zeros(ndim, dtype=float)
    else:
        origin_values = np.asarray(origin, dtype=float)
        if origin_values.shape != (ndim,):
            raise ValueError(f"origin must have shape ({ndim},)")
        if not np.all(np.isfinite(origin_values)):
            raise ValueError("origin must contain only finite values")

    axes = [
        origin_values[index]
        + spacing_values[index] * np.arange(dimensions[index], dtype=float)
        for index in range(ndim)
    ]
    mesh = np.meshgrid(*axes, indexing="ij")
    points = np.column_stack([axis.reshape(-1) for axis in mesh])
    return _read_only(points)


def gaussian_map_sampling_diagnostics(
    covariance_matrix: ArrayLike,
) -> GaussianMapSamplingDiagnostics:
    r"""Return exact mean and naive sample-variance moments.

    For :math:`y\sim N(0,C)` and
    :math:`P=I-11^T/n`, the usual estimator is

    .. math::

       s^2_{\rm naive}=y^TPy/(n-1).

    Its exact moments are

    .. math::

       \mathbb E[s^2_{\rm naive}]=\operatorname{tr}(PC)/(n-1),

       \operatorname{Var}(s^2_{\rm naive})
       =2\operatorname{tr}[(PC)^2]/(n-1)^2.

    ``variance_effective_degrees_of_freedom`` moment matches a scaled chi-square
    distribution.  It is not an exact distributional identity for arbitrary
    covariance eigenvalue spectra.
    """

    matrix = np.asarray(_validated_map_covariance(covariance_matrix))
    sample_count = matrix.shape[0]
    ones = np.ones(sample_count, dtype=float)
    average_marginal = float(np.mean(np.diag(matrix)))
    marginal_spread = float(
        (np.max(np.diag(matrix)) - np.min(np.diag(matrix))) / average_marginal
    )

    mean_variance = float(ones @ matrix @ ones / sample_count**2)
    if mean_variance <= 0.0:
        raise ArithmeticError("map mean variance must be positive")
    effective_mean_count = average_marginal / mean_variance

    projector = np.eye(sample_count, dtype=float) - np.ones(
        (sample_count, sample_count), dtype=float
    ) / sample_count
    projected = projector @ matrix
    first_trace = float(np.trace(projected))
    second_trace = float(np.trace(projected @ projected))
    roundoff_scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    tolerance = 256.0 * np.finfo(float).eps * roundoff_scale**2 * sample_count
    if first_trace < -tolerance or second_trace < -tolerance:
        raise ArithmeticError("quadratic-form moments left their physical interval")
    first_trace = max(first_trace, 0.0)
    second_trace = max(second_trace, 0.0)

    expected_sample_variance = first_trace / (sample_count - 1)
    sample_variance_variance = 2.0 * second_trace / (sample_count - 1) ** 2
    relative_bias = expected_sample_variance / average_marginal - 1.0
    if expected_sample_variance > 0.0:
        relative_standard_deviation = (
            sample_variance_variance**0.5 / expected_sample_variance
        )
    else:
        relative_standard_deviation = 0.0
    if second_trace > 0.0:
        effective_degrees = first_trace**2 / second_trace
    else:
        effective_degrees = 0.0

    eigenvalues = np.linalg.eigvalsh(matrix)
    positive = eigenvalues[eigenvalues > np.finfo(float).eps * np.max(eigenvalues)]
    condition_number = (
        float(np.max(positive) / np.min(positive))
        if positive.size
        else float("inf")
    )

    return GaussianMapSamplingDiagnostics(
        nominal_sample_count=sample_count,
        average_marginal_variance=average_marginal,
        marginal_variance_relative_spread=marginal_spread,
        map_mean_variance=mean_variance,
        map_mean_effective_sample_count=float(effective_mean_count),
        naive_sample_variance_expectation=float(expected_sample_variance),
        naive_sample_variance_relative_bias=float(relative_bias),
        naive_sample_variance_variance=float(sample_variance_variance),
        naive_sample_variance_relative_standard_deviation=float(
            relative_standard_deviation
        ),
        variance_effective_degrees_of_freedom=float(effective_degrees),
        covariance_condition_number=condition_number,
    )


def gaussian_regular_grid_sampling_diagnostics(
    covariance: GaussianCovariance,
    kernel: GaussianKernel,
    shape: Sequence[int],
    spacing: float | Sequence[float],
) -> tuple[FloatMatrix, GaussianMapSamplingDiagnostics]:
    """Build a regular map covariance matrix and return exact diagnostics."""

    positions = regular_grid_positions(shape, spacing)
    covariance_matrix = gaussian_map_covariance_matrix(covariance, positions, kernel)
    return covariance_matrix, gaussian_map_sampling_diagnostics(covariance_matrix)
