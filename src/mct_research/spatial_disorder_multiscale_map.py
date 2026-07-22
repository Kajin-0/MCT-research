"""Cross-scale covariance of variance estimates from one correlated raster.

This module composes the Gaussian filtered-map covariance theorem with exact
moments of jointly Gaussian quadratic forms.  It quantifies the information in
multiple probe scales measured on the same spatial realization.

The first-order covariance of logarithmic variance estimates is a delta-method
result.  The underlying correlated quadratic forms are not asserted to be
jointly log-normal or exactly chi-square distributed.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder import GaussianCovariance
from .spatial_disorder_inference import (
    gaussian_multiscale_log_jacobian,
    gaussian_multiscale_variance,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]
FloatTensor4 = NDArray[np.float64]


@dataclass(frozen=True)
class MultiscaleMapVarianceStatistics:
    """Exact quadratic-form moments and first-order log covariance."""

    probe_sigmas: FloatArray
    nominal_pixel_count: int
    marginal_filtered_variances: FloatArray
    expected_naive_variances: FloatArray
    deterministic_bias_factors: FloatArray
    raw_variance_estimator_covariance: FloatMatrix
    bias_corrected_estimator_covariance: FloatMatrix
    delta_log_variance_covariance: FloatMatrix
    delta_log_variance_standard_deviations: FloatArray
    delta_log_variance_correlation: FloatMatrix
    moment_matched_effective_degrees_of_freedom: FloatArray


@dataclass(frozen=True)
class MultiscaleMapFisherComparison:
    """Parameter information with full map covariance versus independent pixels."""

    log_parameter_jacobian: FloatMatrix
    full_log_observation_covariance: FloatMatrix
    nominal_independent_pixel_log_covariance: FloatMatrix
    full_fisher_matrix: FloatMatrix
    nominal_independent_pixel_fisher_matrix: FloatMatrix
    full_parameter_covariance: FloatMatrix
    nominal_independent_pixel_parameter_covariance: FloatMatrix
    parameter_standard_deviation_inflation: FloatArray
    parameter_covariance_determinant_inflation: float
    full_parameter_correlation: float
    nominal_parameter_correlation: float


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _validated_positions(positions: ArrayLike, dimension: int) -> FloatMatrix:
    result = np.asarray(positions, dtype=float)
    if result.ndim != 2 or result.shape[0] < 2 or result.shape[1] != dimension:
        raise ValueError(
            f"positions must have shape (pixel_count, {dimension}) with at least two pixels"
        )
    if not np.all(np.isfinite(result)):
        raise ValueError("positions must contain only finite values")
    return _read_only(result)


def _validated_scales(probe_sigmas: ArrayLike) -> FloatArray:
    result = np.asarray(probe_sigmas, dtype=float)
    if result.ndim != 1 or result.size < 2:
        raise ValueError("probe_sigmas must contain at least two scales")
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    if np.unique(result).size != result.size:
        raise ValueError("probe_sigmas must be distinct")
    return _read_only(result)


def _validated_covariance(name: str, covariance: ArrayLike, size: int) -> FloatMatrix:
    result = np.asarray(covariance, dtype=float)
    if result.shape != (size, size):
        raise ValueError(f"{name} must have shape ({size}, {size})")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(result, ord=np.inf)))
    if not np.allclose(result, result.T, rtol=1.0e-12, atol=1.0e-14 * scale):
        raise ValueError(f"{name} must be symmetric")
    eigenvalues = np.linalg.eigvalsh(result)
    tolerance = 256.0 * np.finfo(float).eps * max(
        1.0, scale, float(np.max(np.abs(eigenvalues)))
    )
    if float(np.min(eigenvalues)) < -tolerance:
        raise ValueError(f"{name} must be positive semidefinite")
    return _read_only(result)


def gaussian_multiscale_map_covariance_blocks(
    covariance: GaussianCovariance,
    positions: ArrayLike,
    probe_sigmas: ArrayLike,
) -> FloatTensor4:
    r"""Return exact map covariance blocks for isotropic Gaussian probes.

    For scales :math:`s_i,s_j`, material covariance matrix :math:`\Lambda`,
    and center displacement :math:`\delta`, each block element is

    .. math::

       A\sqrt{\frac{\det\Lambda}
       {\det(\Lambda+(s_i^2+s_j^2)I)}}
       \exp\left[-\frac12\delta^T
       (\Lambda+(s_i^2+s_j^2)I)^{-1}\delta\right].

    This is the existing filtered cross-covariance theorem evaluated in a
    vectorized common-raster construction.
    """

    if not isinstance(covariance, GaussianCovariance):
        raise TypeError("covariance must be a GaussianCovariance")
    points = _validated_positions(positions, covariance.dimension)
    scales = _validated_scales(probe_sigmas)
    material = np.asarray(covariance.correlation_matrix)
    sign_material, logdet_material = np.linalg.slogdet(material)
    if sign_material <= 0.0:
        raise RuntimeError("validated material covariance has non-positive determinant")

    displacements = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    scale_count = scales.size
    pixel_count = points.shape[0]
    blocks = np.empty(
        (scale_count, scale_count, pixel_count, pixel_count), dtype=float
    )
    identity = np.eye(covariance.dimension, dtype=float)
    log_point_variance = np.log(covariance.variance)

    for row, scale_i in enumerate(scales):
        for column in range(row, scale_count):
            scale_j = scales[column]
            combined = material + (scale_i * scale_i + scale_j * scale_j) * identity
            sign_combined, logdet_combined = np.linalg.slogdet(combined)
            if sign_combined <= 0.0:
                raise RuntimeError("combined covariance has non-positive determinant")
            inverse = np.linalg.inv(combined)
            quadratic = np.einsum(
                "...i,ij,...j->...",
                displacements,
                inverse,
                displacements,
                optimize=True,
            )
            values = np.exp(
                log_point_variance
                + 0.5 * (float(logdet_material) - float(logdet_combined))
                - 0.5 * quadratic
            )
            blocks[row, column] = values
            blocks[column, row] = values.T

    blocks.setflags(write=False)
    return blocks


def _centered_trace(covariance: FloatMatrix) -> float:
    """Return ``tr(P C)`` without forming the centering matrix."""

    size = covariance.shape[0]
    return float(np.trace(covariance) - np.sum(covariance) / size)


def _centered_cross_trace(block: FloatMatrix) -> float:
    r"""Return ``tr(P C_ij P C_ji)`` in quadratic storage.

    With ``C_ji=C_ij.T`` and ``P=I-11.T/n``,

    ``tr(P A P A.T) = ||A||_F^2 - (||A1||^2+||A.T1||^2)/n
                       + (1.T A 1)^2/n^2``.
    """

    size = block.shape[0]
    row_sums = np.sum(block, axis=1)
    column_sums = np.sum(block, axis=0)
    total = float(np.sum(block))
    result = (
        float(np.sum(block * block))
        - float(row_sums @ row_sums + column_sums @ column_sums) / size
        + total * total / (size * size)
    )
    tolerance = 512.0 * np.finfo(float).eps * max(
        1.0, float(np.sum(block * block))
    )
    if result < -tolerance:
        raise ArithmeticError("centered cross trace left its physical interval")
    return max(result, 0.0)


def gaussian_multiscale_map_variance_statistics(
    covariance_blocks: ArrayLike,
    probe_sigmas: ArrayLike,
) -> MultiscaleMapVarianceStatistics:
    r"""Return exact cross-scale moments of naive map variance estimators.

    For map vectors :math:`y_i,y_j`, centering matrix :math:`P`, and

    .. math::

       q_i=y_i^TPy_i/(n-1),

    joint Gaussianity gives

    .. math::

       \mathbb E[q_i]=\operatorname{tr}(P C_{ii})/(n-1),

       \operatorname{Cov}(q_i,q_j)=
       2\operatorname{tr}(P C_{ij}P C_{ji})/(n-1)^2.

    The returned log covariance is the first-order delta-method result
    ``Cov(q_i,q_j)/(E[q_i]E[q_j])``.
    """

    scales = _validated_scales(probe_sigmas)
    blocks = np.asarray(covariance_blocks, dtype=float)
    if blocks.ndim != 4:
        raise ValueError("covariance_blocks must have four dimensions")
    scale_count = scales.size
    if blocks.shape[0] != scale_count or blocks.shape[1] != scale_count:
        raise ValueError("covariance_blocks scale dimensions must match probe_sigmas")
    if blocks.shape[2] != blocks.shape[3] or blocks.shape[2] < 2:
        raise ValueError("covariance blocks must be square with at least two pixels")
    if not np.all(np.isfinite(blocks)):
        raise ValueError("covariance_blocks must contain only finite values")
    pixel_count = blocks.shape[2]

    marginal = np.empty(scale_count, dtype=float)
    expected = np.empty(scale_count, dtype=float)
    raw_covariance = np.empty((scale_count, scale_count), dtype=float)

    for index in range(scale_count):
        diagonal_block = np.asarray(blocks[index, index])
        marginal[index] = float(np.mean(np.diag(diagonal_block)))
        expected[index] = _centered_trace(diagonal_block) / (pixel_count - 1)
        if marginal[index] <= 0.0 or expected[index] <= 0.0:
            raise ArithmeticError("variance expectation must be positive")

    for row in range(scale_count):
        for column in range(row, scale_count):
            block = np.asarray(blocks[row, column])
            reverse = np.asarray(blocks[column, row])
            scale = max(1.0, float(np.linalg.norm(block, ord=np.inf)))
            if not np.allclose(
                reverse,
                block.T,
                rtol=1.0e-12,
                atol=1.0e-14 * scale,
            ):
                raise ValueError("opposite covariance blocks must be transposes")
            value = 2.0 * _centered_cross_trace(block) / (pixel_count - 1) ** 2
            raw_covariance[row, column] = value
            raw_covariance[column, row] = value

    raw_covariance = np.asarray(
        _validated_covariance(
            "raw_variance_estimator_covariance",
            raw_covariance,
            scale_count,
        )
    )
    bias = expected / marginal
    corrected_covariance = raw_covariance / np.outer(bias, bias)
    log_covariance = raw_covariance / np.outer(expected, expected)
    log_covariance = np.asarray(
        _validated_covariance(
            "delta_log_variance_covariance",
            log_covariance,
            scale_count,
        )
    )
    log_standard_deviations = np.sqrt(np.diag(log_covariance))
    correlation = log_covariance / np.outer(
        log_standard_deviations, log_standard_deviations
    )
    effective_degrees = 2.0 / np.diag(log_covariance)

    return MultiscaleMapVarianceStatistics(
        probe_sigmas=scales,
        nominal_pixel_count=pixel_count,
        marginal_filtered_variances=_read_only(marginal),
        expected_naive_variances=_read_only(expected),
        deterministic_bias_factors=_read_only(bias),
        raw_variance_estimator_covariance=_read_only(raw_covariance),
        bias_corrected_estimator_covariance=_read_only(corrected_covariance),
        delta_log_variance_covariance=_read_only(log_covariance),
        delta_log_variance_standard_deviations=_read_only(
            log_standard_deviations
        ),
        delta_log_variance_correlation=_read_only(correlation),
        moment_matched_effective_degrees_of_freedom=_read_only(
            effective_degrees
        ),
    )


def _parameter_correlation(covariance: FloatMatrix) -> float:
    return float(
        covariance[0, 1]
        / np.sqrt(covariance[0, 0] * covariance[1, 1])
    )


def gaussian_multiscale_map_fisher_comparison(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    delta_log_variance_covariance: ArrayLike,
    *,
    nominal_pixel_count: int,
) -> MultiscaleMapFisherComparison:
    """Compare full same-raster information with independent-pixel counting.

    The full covariance is the delta-method covariance of the cross-scale map
    variance estimators.  The nominal comparison assumes every raster pixel is
    independent at every scale and assumes zero cross-scale covariance:
    ``2 I/(n-1)``.
    """

    variance = _positive_scalar("point_variance", point_variance)
    correlation_length_value = _positive_scalar(
        "correlation_length", correlation_length
    )
    scales = _validated_scales(probe_sigmas)
    if isinstance(nominal_pixel_count, bool) or int(nominal_pixel_count) != nominal_pixel_count:
        raise ValueError("nominal_pixel_count must be an integer")
    pixel_count = int(nominal_pixel_count)
    if pixel_count < 2:
        raise ValueError("nominal_pixel_count must be at least two")

    full_covariance = np.asarray(
        _validated_covariance(
            "delta_log_variance_covariance",
            delta_log_variance_covariance,
            scales.size,
        )
    )
    predicted = gaussian_multiscale_variance(
        variance, correlation_length_value, scales
    )
    variance_jacobian = gaussian_multiscale_log_jacobian(
        variance, correlation_length_value, scales
    )
    log_jacobian = np.asarray(variance_jacobian) / np.asarray(predicted)[:, None]
    nominal_covariance = np.eye(scales.size, dtype=float) * 2.0 / (pixel_count - 1)

    full_precision = np.linalg.pinv(full_covariance, hermitian=True)
    nominal_precision = np.linalg.inv(nominal_covariance)
    full_fisher = log_jacobian.T @ full_precision @ log_jacobian
    nominal_fisher = log_jacobian.T @ nominal_precision @ log_jacobian
    full_fisher = 0.5 * (full_fisher + full_fisher.T)
    nominal_fisher = 0.5 * (nominal_fisher + nominal_fisher.T)
    if np.linalg.matrix_rank(full_fisher) != 2:
        raise ValueError("full same-raster design does not identify both parameters")
    if np.linalg.matrix_rank(nominal_fisher) != 2:
        raise ValueError("nominal design does not identify both parameters")

    full_parameter_covariance = np.linalg.inv(full_fisher)
    nominal_parameter_covariance = np.linalg.inv(nominal_fisher)
    inflation = np.sqrt(
        np.diag(full_parameter_covariance)
        / np.diag(nominal_parameter_covariance)
    )
    determinant_inflation = float(
        np.linalg.det(full_parameter_covariance)
        / np.linalg.det(nominal_parameter_covariance)
    )

    return MultiscaleMapFisherComparison(
        log_parameter_jacobian=_read_only(log_jacobian),
        full_log_observation_covariance=_read_only(full_covariance),
        nominal_independent_pixel_log_covariance=_read_only(nominal_covariance),
        full_fisher_matrix=_read_only(full_fisher),
        nominal_independent_pixel_fisher_matrix=_read_only(nominal_fisher),
        full_parameter_covariance=_read_only(full_parameter_covariance),
        nominal_independent_pixel_parameter_covariance=_read_only(
            nominal_parameter_covariance
        ),
        parameter_standard_deviation_inflation=_read_only(inflation),
        parameter_covariance_determinant_inflation=determinant_inflation,
        full_parameter_correlation=_parameter_correlation(
            full_parameter_covariance
        ),
        nominal_parameter_correlation=_parameter_correlation(
            nominal_parameter_covariance
        ),
    )
