"""Probe-scale calibration limits for Gaussian multiscale disorder inference.

The physical benchmark is

``V(s) = A / (1 + 2 s**2 / xi**2)``

with physical log parameters ``(log A, log xi)``.  Nominal probe scales may
carry multiplicative calibration errors represented in log space as

``delta_log_s = B @ eta``.

The nuisance coordinates ``eta`` may describe a common calibration factor,
independent per-scale errors, or any declared low-dimensional correlated basis.
Gaussian priors are incorporated through nuisance precision, and calibration
coordinates are marginalized analytically by a Schur complement.

This module provides local linear-Gaussian information diagnostics.  It does not
calibrate an instrument, infer a specimen covariance family, or validate the
Gaussian covariance/Gaussian probe model experimentally.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_inference import (
    GaussianRecoverabilityDiagnostics,
    gaussian_multiscale_fisher_information,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


@dataclass(frozen=True)
class ProbeScaleCalibrationDiagnostics:
    """Marginal physical-parameter information after calibration uncertainty."""

    base_diagnostics: GaussianRecoverabilityDiagnostics
    calibration_basis: FloatMatrix
    probe_log_jacobian: FloatArray
    nuisance_jacobian: FloatMatrix
    nuisance_prior_precision: FloatMatrix
    joint_fisher_matrix: FloatMatrix
    nuisance_fisher_matrix: FloatMatrix
    marginalized_fisher_matrix: FloatMatrix
    singular_values: FloatArray
    rank: int
    rank_tolerance: float
    condition_number: float
    parameter_covariance: FloatMatrix | None
    parameter_correlation: float | None
    standard_deviation_inflation: FloatArray | None
    null_direction: FloatArray | None
    nuisance_dimension: int
    calibration_mode: str


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _finite_positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def common_log_scale_basis(number_of_scales: int) -> FloatMatrix:
    """Return a one-column common multiplicative probe-scale error basis."""

    if isinstance(number_of_scales, bool) or int(number_of_scales) != number_of_scales:
        raise ValueError("number_of_scales must be a positive integer")
    size = int(number_of_scales)
    if size <= 0:
        raise ValueError("number_of_scales must be a positive integer")
    return _read_only(np.ones((size, 1), dtype=float))


def independent_log_scale_basis(number_of_scales: int) -> FloatMatrix:
    """Return one independent multiplicative calibration coordinate per scale."""

    if isinstance(number_of_scales, bool) or int(number_of_scales) != number_of_scales:
        raise ValueError("number_of_scales must be a positive integer")
    size = int(number_of_scales)
    if size <= 0:
        raise ValueError("number_of_scales must be a positive integer")
    return _read_only(np.eye(size, dtype=float))


def _validated_basis(calibration_basis: ArrayLike, number_of_scales: int) -> FloatMatrix:
    basis = np.asarray(calibration_basis, dtype=float)
    if basis.ndim == 1:
        basis = basis.reshape(-1, 1)
    if basis.ndim != 2 or basis.shape[0] != number_of_scales or basis.shape[1] == 0:
        raise ValueError(
            "calibration_basis must have shape "
            f"({number_of_scales}, nuisance_dimension)"
        )
    if not np.all(np.isfinite(basis)):
        raise ValueError("calibration_basis must contain only finite values")
    return _read_only(basis)


def _validated_symmetric_matrix(
    name: str,
    value: ArrayLike,
    dimension: int,
    *,
    positive_definite: bool,
) -> FloatMatrix:
    matrix = np.asarray(value, dtype=float)
    if matrix.shape != (dimension, dimension):
        raise ValueError(f"{name} must have shape ({dimension}, {dimension})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    if not np.allclose(matrix, matrix.T, rtol=1.0e-12, atol=1.0e-14 * scale):
        raise ValueError(f"{name} must be symmetric")
    eigenvalues = np.linalg.eigvalsh(0.5 * (matrix + matrix.T))
    tolerance = 128.0 * np.finfo(float).eps * scale
    if positive_definite:
        if float(np.min(eigenvalues)) <= tolerance:
            raise ValueError(f"{name} must be positive definite")
    elif float(np.min(eigenvalues)) < -tolerance:
        raise ValueError(f"{name} must be positive semidefinite")
    return _read_only(0.5 * (matrix + matrix.T))


def _nuisance_prior_precision(
    dimension: int,
    *,
    calibration_prior_standard_deviations: ArrayLike | None,
    calibration_prior_covariance: ArrayLike | None,
    calibration_prior_precision: ArrayLike | None,
) -> FloatMatrix:
    supplied = sum(
        item is not None
        for item in (
            calibration_prior_standard_deviations,
            calibration_prior_covariance,
            calibration_prior_precision,
        )
    )
    if supplied > 1:
        raise ValueError(
            "provide at most one calibration prior specification: standard "
            "deviations, covariance, or precision"
        )
    if supplied == 0:
        return _read_only(np.zeros((dimension, dimension), dtype=float))

    if calibration_prior_standard_deviations is not None:
        standard_deviations = np.asarray(
            calibration_prior_standard_deviations,
            dtype=float,
        )
        if standard_deviations.ndim == 0:
            standard_deviations = np.full(
                dimension,
                float(standard_deviations),
                dtype=float,
            )
        if standard_deviations.shape != (dimension,):
            raise ValueError(
                "calibration_prior_standard_deviations must be scalar or have "
                f"shape ({dimension},)"
            )
        if not np.all(np.isfinite(standard_deviations)) or np.any(
            standard_deviations <= 0.0
        ):
            raise ValueError(
                "calibration_prior_standard_deviations must be finite and positive"
            )
        return _read_only(np.diag(1.0 / standard_deviations**2))

    if calibration_prior_covariance is not None:
        covariance = _validated_symmetric_matrix(
            "calibration_prior_covariance",
            calibration_prior_covariance,
            dimension,
            positive_definite=True,
        )
        cholesky = np.linalg.cholesky(np.asarray(covariance))
        identity = np.eye(dimension, dtype=float)
        precision = np.linalg.solve(cholesky.T, np.linalg.solve(cholesky, identity))
        return _read_only(0.5 * (precision + precision.T))

    return _validated_symmetric_matrix(
        "calibration_prior_precision",
        calibration_prior_precision,
        dimension,
        positive_definite=False,
    )


def _symmetric_pseudoinverse(matrix: FloatMatrix) -> FloatMatrix:
    symmetric = 0.5 * (np.asarray(matrix) + np.asarray(matrix).T)
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    leading = max(1.0, float(np.max(np.abs(eigenvalues))))
    tolerance = max(matrix.shape) * np.finfo(float).eps * leading
    inverse_eigenvalues = np.zeros_like(eigenvalues)
    positive = eigenvalues > tolerance
    inverse_eigenvalues[positive] = 1.0 / eigenvalues[positive]
    result = (eigenvectors * inverse_eigenvalues) @ eigenvectors.T
    return _read_only(0.5 * (result + result.T))


def _rank_diagnostics(
    fisher_matrix: FloatMatrix,
    rank_relative_tolerance: float | None,
) -> tuple[FloatArray, int, float, float, FloatMatrix | None, float | None, FloatArray | None]:
    fisher = 0.5 * (np.asarray(fisher_matrix) + np.asarray(fisher_matrix).T)
    eigenvalues, eigenvectors = np.linalg.eigh(fisher)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = np.maximum(eigenvalues[order], 0.0)
    eigenvectors = eigenvectors[:, order]
    singular_values = np.sqrt(eigenvalues)

    if rank_relative_tolerance is None:
        rank_rtol = fisher.shape[0] * np.finfo(float).eps
    else:
        rank_rtol = _finite_positive_scalar(
            "rank_relative_tolerance",
            rank_relative_tolerance,
        )
        if rank_rtol >= 1.0:
            raise ValueError("rank_relative_tolerance must be less than one")
    leading = float(singular_values[0]) if singular_values.size else 0.0
    absolute_tolerance = rank_rtol * leading if leading > 0.0 else rank_rtol
    rank = int(np.count_nonzero(singular_values > absolute_tolerance))

    if rank == fisher.shape[0]:
        condition_number = float(singular_values[0] / singular_values[-1])
        covariance = np.linalg.inv(fisher)
        covariance = 0.5 * (covariance + covariance.T)
        correlation = float(
            covariance[0, 1]
            / np.sqrt(covariance[0, 0] * covariance[1, 1])
        )
        return (
            _read_only(singular_values),
            rank,
            float(absolute_tolerance),
            condition_number,
            _read_only(covariance),
            correlation,
            None,
        )

    null_direction = eigenvectors[:, -1]
    if null_direction[0] < 0.0 or (
        null_direction[0] == 0.0 and null_direction[1] < 0.0
    ):
        null_direction = -null_direction
    return (
        _read_only(singular_values),
        rank,
        float(absolute_tolerance),
        float("inf"),
        None,
        None,
        _read_only(null_direction),
    )


def gaussian_probe_scale_calibration_information(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    calibration_basis: ArrayLike,
    *,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    calibration_prior_standard_deviations: ArrayLike | None = None,
    calibration_prior_covariance: ArrayLike | None = None,
    calibration_prior_precision: ArrayLike | None = None,
    rank_relative_tolerance: float | None = None,
    calibration_mode: str = "declared_basis",
) -> ProbeScaleCalibrationDiagnostics:
    """Return physical information after marginalizing probe-scale calibration.

    The nuisance basis maps calibration coordinates to per-observation log-scale
    errors.  If ``B`` is the basis and ``j_s`` is the vector
    ``dV_i/dlog(s_i)``, then the nuisance Jacobian is

    ``J_eta = diag(j_s) @ B``.

    Exactly one observation-uncertainty interface must be supplied, matching
    :func:`gaussian_multiscale_fisher_information`.  A calibration prior is
    optional.  Omitting it represents an uncalibrated nuisance mode.
    """

    if not isinstance(calibration_mode, str) or not calibration_mode.strip():
        raise ValueError("calibration_mode must be a non-empty string")

    base = gaussian_multiscale_fisher_information(
        point_variance,
        correlation_length,
        probe_sigmas,
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
        rank_relative_tolerance=rank_relative_tolerance,
    )
    number_of_scales = base.predicted_variance.size
    basis = _validated_basis(calibration_basis, number_of_scales)
    nuisance_dimension = basis.shape[1]
    prior_precision = _nuisance_prior_precision(
        nuisance_dimension,
        calibration_prior_standard_deviations=calibration_prior_standard_deviations,
        calibration_prior_covariance=calibration_prior_covariance,
        calibration_prior_precision=calibration_prior_precision,
    )

    # A change in log probe scale is exactly opposite to a change in log xi.
    probe_log_jacobian = -np.asarray(base.jacobian)[:, 1]
    nuisance_jacobian = probe_log_jacobian[:, None] * np.asarray(basis)

    cholesky = np.linalg.cholesky(np.asarray(base.observation_covariance))
    whitened_physical = np.linalg.solve(cholesky, np.asarray(base.jacobian))
    whitened_nuisance = np.linalg.solve(cholesky, nuisance_jacobian)

    physical_fisher = whitened_physical.T @ whitened_physical
    physical_nuisance = whitened_physical.T @ whitened_nuisance
    nuisance_fisher = (
        whitened_nuisance.T @ whitened_nuisance + np.asarray(prior_precision)
    )
    nuisance_fisher = 0.5 * (nuisance_fisher + nuisance_fisher.T)

    nuisance_inverse = _symmetric_pseudoinverse(_read_only(nuisance_fisher))
    marginalized = (
        physical_fisher
        - physical_nuisance @ np.asarray(nuisance_inverse) @ physical_nuisance.T
    )
    marginalized = 0.5 * (marginalized + marginalized.T)

    joint = np.block(
        [
            [physical_fisher, physical_nuisance],
            [physical_nuisance.T, nuisance_fisher],
        ]
    )
    joint = 0.5 * (joint + joint.T)

    (
        singular_values,
        rank,
        rank_tolerance,
        condition_number,
        parameter_covariance,
        parameter_correlation,
        null_direction,
    ) = _rank_diagnostics(_read_only(marginalized), rank_relative_tolerance)

    if parameter_covariance is not None and base.parameter_covariance is not None:
        inflation = np.sqrt(
            np.diag(np.asarray(parameter_covariance))
            / np.diag(np.asarray(base.parameter_covariance))
        )
        inflation_result: FloatArray | None = _read_only(inflation)
    else:
        inflation_result = None

    return ProbeScaleCalibrationDiagnostics(
        base_diagnostics=base,
        calibration_basis=basis,
        probe_log_jacobian=_read_only(probe_log_jacobian),
        nuisance_jacobian=_read_only(nuisance_jacobian),
        nuisance_prior_precision=prior_precision,
        joint_fisher_matrix=_read_only(joint),
        nuisance_fisher_matrix=_read_only(nuisance_fisher),
        marginalized_fisher_matrix=_read_only(marginalized),
        singular_values=singular_values,
        rank=rank,
        rank_tolerance=rank_tolerance,
        condition_number=condition_number,
        parameter_covariance=parameter_covariance,
        parameter_correlation=parameter_correlation,
        standard_deviation_inflation=inflation_result,
        null_direction=null_direction,
        nuisance_dimension=nuisance_dimension,
        calibration_mode=calibration_mode.strip(),
    )


def common_probe_scale_calibration_information(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    calibration_log_standard_deviation: float | None,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    rank_relative_tolerance: float | None = None,
) -> ProbeScaleCalibrationDiagnostics:
    """Convenience wrapper for one shared multiplicative scale calibration.

    Set ``calibration_log_standard_deviation=None`` for an uncalibrated common
    scale.  A finite value is the Gaussian prior standard deviation of the common
    log-scale error.
    """

    scales = np.asarray(probe_sigmas, dtype=float)
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("probe_sigmas must be a non-empty one-dimensional array")
    prior = (
        None
        if calibration_log_standard_deviation is None
        else [_finite_positive_scalar(
            "calibration_log_standard_deviation",
            calibration_log_standard_deviation,
        )]
    )
    return gaussian_probe_scale_calibration_information(
        point_variance,
        correlation_length,
        scales,
        common_log_scale_basis(scales.size),
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
        calibration_prior_standard_deviations=prior,
        rank_relative_tolerance=rank_relative_tolerance,
        calibration_mode="common_log_scale",
    )


def independent_probe_scale_calibration_information(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    calibration_log_standard_deviations: ArrayLike,
    *,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    rank_relative_tolerance: float | None = None,
) -> ProbeScaleCalibrationDiagnostics:
    """Convenience wrapper for independent per-scale log calibration errors."""

    scales = np.asarray(probe_sigmas, dtype=float)
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("probe_sigmas must be a non-empty one-dimensional array")
    return gaussian_probe_scale_calibration_information(
        point_variance,
        correlation_length,
        scales,
        independent_log_scale_basis(scales.size),
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
        calibration_prior_standard_deviations=calibration_log_standard_deviations,
        rank_relative_tolerance=rank_relative_tolerance,
        calibration_mode="independent_log_scales",
    )
