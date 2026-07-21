"""Probe-scale calibration limits for Gaussian multiscale disorder inference.

For the isotropic two-dimensional Gaussian benchmark

``V(s) = A / (1 + 2 s**2 / xi**2)``,

the local physics parameters are ``(log A, log xi)``. Probe-width errors are
represented by a low-dimensional Gaussian nuisance vector ``z`` and a declared
basis ``B`` such that ``delta log(s) = B z``. The nuisance parameters are
marginalized analytically with a Fisher-matrix Schur complement.

A common calibration mode has ``B = 1``. In that case
``dV/dlog(s) = -dV/dlog(xi)``, so the data identify only the relative scale
between the probe width and the correlation length.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_inference import (
    _finite_positive_scalar,
    _model_terms,
    _read_only_array,
    _validated_observation_covariance,
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_log_jacobian,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


def gaussian_probe_log_jacobian(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
) -> FloatArray:
    """Return ``dV_i/dlog(s_i)`` for every declared probe scale."""

    predicted, transition_fraction, _ = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    return _read_only_array(-2.0 * predicted * transition_fraction)


def _validated_nuisance_basis(
    probe_count: int,
    nuisance_basis: ArrayLike,
) -> FloatMatrix:
    basis = np.asarray(nuisance_basis, dtype=float)
    if basis.ndim == 1:
        basis = basis[:, np.newaxis]
    if basis.ndim != 2 or basis.shape[0] != probe_count or basis.shape[1] == 0:
        raise ValueError(
            "nuisance_basis must have shape "
            f"({probe_count}, k) with at least one nuisance mode"
        )
    if not np.all(np.isfinite(basis)):
        raise ValueError("nuisance_basis must contain only finite values")
    return _read_only_array(basis)


def _validated_positive_definite_covariance(
    name: str,
    covariance: ArrayLike,
    dimension: int,
) -> FloatMatrix:
    result = np.asarray(covariance, dtype=float)
    if result.shape != (dimension, dimension):
        raise ValueError(f"{name} must have shape ({dimension}, {dimension})")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(result, ord=np.inf)))
    if not np.allclose(
        result,
        result.T,
        rtol=1.0e-12,
        atol=1.0e-14 * scale,
    ):
        raise ValueError(f"{name} must be symmetric")
    try:
        np.linalg.cholesky(result)
    except np.linalg.LinAlgError as exc:
        raise ValueError(f"{name} must be positive definite") from exc
    return _read_only_array(result)


def _rank_diagnostics(
    fisher: FloatMatrix,
    rank_relative_tolerance: float | None,
) -> tuple[FloatArray, int, float, float]:
    if rank_relative_tolerance is None:
        rank_rtol = max(fisher.shape) * np.finfo(float).eps
    else:
        rank_rtol = _finite_positive_scalar(
            "rank_relative_tolerance",
            rank_relative_tolerance,
        )
        if rank_rtol >= 1.0:
            raise ValueError("rank_relative_tolerance must be less than one")

    eigenvalues = np.linalg.eigvalsh(np.asarray(fisher))
    scale = max(1.0, float(np.linalg.norm(fisher, ord=np.inf)))
    if float(np.min(eigenvalues)) < -1.0e-12 * scale:
        raise ArithmeticError(
            "marginalized Fisher matrix is not positive semidefinite"
        )
    eigenvalues = np.clip(eigenvalues, 0.0, None)[::-1]
    singular_values = np.sqrt(eigenvalues)
    leading = float(singular_values[0])
    absolute_tolerance = rank_rtol * leading if leading > 0.0 else rank_rtol
    rank = int(np.count_nonzero(singular_values > absolute_tolerance))
    condition_number = (
        float(singular_values[0] / singular_values[1])
        if rank == 2
        else float("inf")
    )
    return (
        _read_only_array(singular_values),
        rank,
        float(absolute_tolerance),
        condition_number,
    )


@dataclass(frozen=True)
class GaussianProbeScaleUncertaintyDiagnostics:
    """Local recoverability after marginalizing probe-scale nuisance modes."""

    predicted_variance: FloatArray
    probe_scale_ratios: FloatArray
    physics_jacobian: FloatMatrix
    probe_log_jacobian: FloatArray
    nuisance_basis: FloatMatrix
    nuisance_jacobian: FloatMatrix
    observation_covariance: FloatMatrix
    nuisance_covariance: FloatMatrix
    augmented_fisher_matrix: FloatMatrix
    marginalized_fisher_matrix: FloatMatrix
    singular_values: FloatArray
    rank: int
    rank_tolerance: float
    condition_number: float
    base_parameter_covariance: FloatMatrix | None
    parameter_covariance: FloatMatrix | None
    parameter_correlation: float | None
    parameter_standard_deviation_inflation: FloatArray | None


def gaussian_multiscale_fisher_with_probe_uncertainty(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    nuisance_basis: ArrayLike,
    nuisance_covariance: ArrayLike,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    rank_relative_tolerance: float | None = None,
) -> GaussianProbeScaleUncertaintyDiagnostics:
    """Marginalize declared Gaussian log-probe-scale calibration modes.

    ``nuisance_basis`` maps a nuisance vector ``z`` to log-scale errors:

    ``delta log(s) = nuisance_basis @ z``.

    ``nuisance_covariance`` is the prior covariance of ``z``. Exactly one
    observation-uncertainty specification must be supplied.
    """

    predicted, _, ratios = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    physics_jacobian = gaussian_multiscale_log_jacobian(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    probe_log_jacobian = gaussian_probe_log_jacobian(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    basis = _validated_nuisance_basis(predicted.size, nuisance_basis)
    nuisance_prior = _validated_positive_definite_covariance(
        "nuisance_covariance",
        nuisance_covariance,
        basis.shape[1],
    )
    covariance = _validated_observation_covariance(
        predicted,
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
    )

    nuisance_jacobian = np.asarray(probe_log_jacobian)[:, np.newaxis] * np.asarray(
        basis
    )
    observation_cholesky = np.linalg.cholesky(np.asarray(covariance))
    whitened_physics = np.linalg.solve(
        observation_cholesky,
        np.asarray(physics_jacobian),
    )
    whitened_nuisance = np.linalg.solve(
        observation_cholesky,
        nuisance_jacobian,
    )

    nuisance_cholesky = np.linalg.cholesky(np.asarray(nuisance_prior))
    identity = np.eye(basis.shape[1], dtype=float)
    nuisance_precision = np.linalg.solve(
        nuisance_cholesky.T,
        np.linalg.solve(nuisance_cholesky, identity),
    )

    physics_block = whitened_physics.T @ whitened_physics
    cross_block = whitened_physics.T @ whitened_nuisance
    nuisance_block = whitened_nuisance.T @ whitened_nuisance + nuisance_precision

    augmented = np.block(
        [
            [physics_block, cross_block],
            [cross_block.T, nuisance_block],
        ]
    )
    augmented = 0.5 * (augmented + augmented.T)

    marginalized = physics_block - cross_block @ np.linalg.solve(
        nuisance_block,
        cross_block.T,
    )
    marginalized = 0.5 * (marginalized + marginalized.T)

    singular_values, rank, rank_tolerance, condition_number = _rank_diagnostics(
        marginalized,
        rank_relative_tolerance,
    )

    base = gaussian_multiscale_fisher_information(
        point_variance,
        correlation_length,
        probe_sigmas,
        observation_covariance=np.asarray(covariance),
        rank_relative_tolerance=rank_relative_tolerance,
    )
    base_covariance = base.parameter_covariance

    if rank == 2:
        parameter_covariance_array = np.linalg.inv(marginalized)
        parameter_covariance = _read_only_array(parameter_covariance_array)
        parameter_correlation = float(
            parameter_covariance_array[0, 1]
            / np.sqrt(
                parameter_covariance_array[0, 0]
                * parameter_covariance_array[1, 1]
            )
        )
        if base_covariance is None:
            inflation = None
        else:
            inflation = _read_only_array(
                np.sqrt(
                    np.diag(parameter_covariance_array)
                    / np.diag(np.asarray(base_covariance))
                )
            )
    else:
        parameter_covariance = None
        parameter_correlation = None
        inflation = None

    return GaussianProbeScaleUncertaintyDiagnostics(
        predicted_variance=predicted,
        probe_scale_ratios=ratios,
        physics_jacobian=physics_jacobian,
        probe_log_jacobian=probe_log_jacobian,
        nuisance_basis=basis,
        nuisance_jacobian=_read_only_array(nuisance_jacobian),
        observation_covariance=covariance,
        nuisance_covariance=nuisance_prior,
        augmented_fisher_matrix=_read_only_array(augmented),
        marginalized_fisher_matrix=_read_only_array(marginalized),
        singular_values=singular_values,
        rank=rank,
        rank_tolerance=rank_tolerance,
        condition_number=condition_number,
        base_parameter_covariance=base_covariance,
        parameter_covariance=parameter_covariance,
        parameter_correlation=parameter_correlation,
        parameter_standard_deviation_inflation=inflation,
    )


def gaussian_common_probe_scale_calibration(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    log_scale_standard_deviation: float,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    rank_relative_tolerance: float | None = None,
) -> GaussianProbeScaleUncertaintyDiagnostics:
    """Return diagnostics for one common multiplicative probe-scale error."""

    log_scale_std = float(log_scale_standard_deviation)
    if not isfinite(log_scale_std) or log_scale_std <= 0.0:
        raise ValueError(
            "log_scale_standard_deviation must be finite and positive"
        )
    predicted, _, _ = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    return gaussian_multiscale_fisher_with_probe_uncertainty(
        point_variance,
        correlation_length,
        probe_sigmas,
        nuisance_basis=np.ones((predicted.size, 1), dtype=float),
        nuisance_covariance=np.array([[log_scale_std**2]], dtype=float),
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
        rank_relative_tolerance=rank_relative_tolerance,
    )
