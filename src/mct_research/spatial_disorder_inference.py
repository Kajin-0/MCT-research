"""Recoverability diagnostics for Gaussian multiscale disorder measurements.

The model is the isotropic two-dimensional Gaussian benchmark

``V(s) = A / (1 + 2 s**2 / xi**2)``,

with positive point variance ``A`` and correlation length ``xi``.  The default
parameterization is ``(log A, log xi)`` so Fisher conditioning is dimensionless.
This module diagnoses information content; it does not estimate parameters from
experimental data or choose a covariance family.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


def _finite_positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _validated_scales(probe_sigmas: ArrayLike) -> FloatArray:
    scales = np.array(probe_sigmas, dtype=float, copy=True)
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("probe_sigmas must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(scales)):
        raise ValueError("probe_sigmas must contain only finite values")
    if np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be non-negative")
    scales.setflags(write=False)
    return scales


def _read_only_array(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _model_terms(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    variance = _finite_positive_scalar("point_variance", point_variance)
    correlation = _finite_positive_scalar("correlation_length", correlation_length)
    scales = _validated_scales(probe_sigmas)

    log_q = np.full(scales.shape, -np.inf, dtype=float)
    positive = scales > 0.0
    log_q[positive] = (
        log(2.0)
        + 2.0 * np.log(scales[positive])
        - 2.0 * log(correlation)
    )
    log_denominator = np.logaddexp(0.0, log_q)
    predicted = np.exp(log(variance) - log_denominator)
    transition_fraction = np.exp(log_q - log_denominator)
    transition_fraction[~positive] = 0.0

    if not np.all(np.isfinite(predicted)) or np.any(predicted <= 0.0):
        raise ValueError("probe scales cause predicted variances to underflow")
    ratios = scales / correlation
    return (
        _read_only_array(predicted),
        _read_only_array(transition_fraction),
        _read_only_array(ratios),
    )


def gaussian_multiscale_variance(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
) -> FloatArray:
    """Return ``V(s)=A/(1+2s**2/xi**2)`` at each probe scale."""

    predicted, _, _ = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    return predicted


def gaussian_multiscale_log_jacobian(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
) -> FloatMatrix:
    """Return the Jacobian with respect to ``(log A, log xi)``.

    The columns are

    ``dV/dlogA = V``

    and

    ``dV/dlogxi = 2 V q/(1+q)``, where ``q=2s**2/xi**2``.
    """

    predicted, transition_fraction, _ = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    jacobian = np.column_stack(
        (
            predicted,
            2.0 * predicted * transition_fraction,
        )
    )
    return _read_only_array(jacobian)


def _validated_observation_covariance(
    predicted: FloatArray,
    *,
    observation_standard_deviations: ArrayLike | None,
    observation_covariance: ArrayLike | None,
    relative_standard_deviation: float | None,
) -> FloatMatrix:
    supplied = sum(
        item is not None
        for item in (
            observation_standard_deviations,
            observation_covariance,
            relative_standard_deviation,
        )
    )
    if supplied != 1:
        raise ValueError(
            "provide exactly one uncertainty specification: standard deviations, "
            "covariance, or relative_standard_deviation"
        )

    size = predicted.size
    if relative_standard_deviation is not None:
        relative = _finite_positive_scalar(
            "relative_standard_deviation", relative_standard_deviation
        )
        standard_deviations = relative * predicted
        covariance = np.diag(standard_deviations**2)
    elif observation_standard_deviations is not None:
        standard_deviations = np.asarray(
            observation_standard_deviations,
            dtype=float,
        )
        if standard_deviations.shape != (size,):
            raise ValueError(
                f"observation_standard_deviations must have shape ({size},)"
            )
        if not np.all(np.isfinite(standard_deviations)) or np.any(
            standard_deviations <= 0.0
        ):
            raise ValueError(
                "observation_standard_deviations must be finite and positive"
            )
        covariance = np.diag(standard_deviations**2)
    else:
        covariance = np.asarray(observation_covariance, dtype=float)
        if covariance.shape != (size, size):
            raise ValueError(f"observation_covariance must have shape ({size}, {size})")
        if not np.all(np.isfinite(covariance)):
            raise ValueError("observation_covariance must contain only finite values")
        scale = max(1.0, float(np.linalg.norm(covariance, ord=np.inf)))
        if not np.allclose(
            covariance,
            covariance.T,
            rtol=1.0e-12,
            atol=1.0e-14 * scale,
        ):
            raise ValueError("observation_covariance must be symmetric")
        try:
            np.linalg.cholesky(covariance)
        except np.linalg.LinAlgError as exc:
            raise ValueError("observation_covariance must be positive definite") from exc

    result = np.array(covariance, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _classify_regime(ratios: FloatArray) -> str:
    if float(np.max(ratios)) <= 0.1:
        return "small_probe"
    if float(np.min(ratios)) >= 10.0:
        return "large_probe"
    if float(np.min(ratios)) < 1.0 < float(np.max(ratios)):
        return "spanning_transition"
    return "intermediate_one_sided"


@dataclass(frozen=True)
class GaussianRecoverabilityDiagnostics:
    """Fisher diagnostics for ``(log point variance, log correlation length)``."""

    predicted_variance: FloatArray
    probe_scale_ratios: FloatArray
    jacobian: FloatMatrix
    observation_covariance: FloatMatrix
    fisher_matrix: FloatMatrix
    singular_values: FloatArray
    rank: int
    rank_tolerance: float
    condition_number: float
    parameter_covariance: FloatMatrix | None
    parameter_correlation: float | None
    null_direction: FloatArray | None
    regime: str


def gaussian_multiscale_fisher_information(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    *,
    observation_standard_deviations: ArrayLike | None = None,
    observation_covariance: ArrayLike | None = None,
    relative_standard_deviation: float | None = None,
    rank_relative_tolerance: float | None = None,
) -> GaussianRecoverabilityDiagnostics:
    """Return practical recoverability diagnostics for a multiscale design.

    Exactly one uncertainty specification must be supplied.  The calculation
    whitens the analytical log-parameter Jacobian by Cholesky factorization, so
    correlated measurement errors are handled without explicitly inverting the
    observation covariance.
    """

    predicted, _, ratios = _model_terms(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    jacobian = gaussian_multiscale_log_jacobian(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
    covariance = _validated_observation_covariance(
        predicted,
        observation_standard_deviations=observation_standard_deviations,
        observation_covariance=observation_covariance,
        relative_standard_deviation=relative_standard_deviation,
    )

    if rank_relative_tolerance is None:
        rank_rtol = max(jacobian.shape) * np.finfo(float).eps
    else:
        rank_rtol = _finite_positive_scalar(
            "rank_relative_tolerance", rank_relative_tolerance
        )
        if rank_rtol >= 1.0:
            raise ValueError("rank_relative_tolerance must be less than one")

    cholesky = np.linalg.cholesky(np.asarray(covariance))
    whitened_jacobian = np.linalg.solve(cholesky, np.asarray(jacobian))
    _, singular_values, right_vectors_transpose = np.linalg.svd(
        whitened_jacobian,
        full_matrices=True,
    )
    padded_singular_values = np.zeros(2, dtype=float)
    padded_singular_values[: singular_values.size] = singular_values
    leading = float(padded_singular_values[0])
    absolute_tolerance = rank_rtol * leading if leading > 0.0 else rank_rtol
    rank = int(np.count_nonzero(padded_singular_values > absolute_tolerance))

    fisher = whitened_jacobian.T @ whitened_jacobian
    fisher = 0.5 * (fisher + fisher.T)
    if rank == 2:
        condition_number = float(
            padded_singular_values[0] / padded_singular_values[1]
        )
        parameter_covariance_array = np.linalg.inv(fisher)
        parameter_correlation = float(
            parameter_covariance_array[0, 1]
            / np.sqrt(
                parameter_covariance_array[0, 0]
                * parameter_covariance_array[1, 1]
            )
        )
        parameter_covariance_result: FloatMatrix | None = _read_only_array(
            parameter_covariance_array
        )
        null_direction_result: FloatArray | None = None
    else:
        condition_number = float("inf")
        parameter_covariance_result = None
        parameter_correlation = None
        null_direction = right_vectors_transpose[-1]
        if null_direction[0] < 0.0 or (
            null_direction[0] == 0.0 and null_direction[1] < 0.0
        ):
            null_direction = -null_direction
        null_direction_result = _read_only_array(null_direction)

    return GaussianRecoverabilityDiagnostics(
        predicted_variance=predicted,
        probe_scale_ratios=ratios,
        jacobian=jacobian,
        observation_covariance=covariance,
        fisher_matrix=_read_only_array(fisher),
        singular_values=_read_only_array(padded_singular_values),
        rank=rank,
        rank_tolerance=float(absolute_tolerance),
        condition_number=condition_number,
        parameter_covariance=parameter_covariance_result,
        parameter_correlation=parameter_correlation,
        null_direction=null_direction_result,
        regime=_classify_regime(ratios),
    )
