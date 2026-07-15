"""Matrix-level projection onto one-P and two-P bulk Kane manifolds.

The fitting routines support ordinary least squares, scalar point weights, and
full covariance-weighted generalized least squares over the real-vectorized
complex Hamiltonian matrices.
"""

from __future__ import annotations

from dataclasses import fields
from typing import Iterable, Mapping, Sequence, TypeVar

import numpy as np
from numpy.typing import NDArray

from .kane8 import (
    ExtendedKaneParameters,
    KaneParameters,
    hamiltonian,
    hamiltonian_two_p,
)

ParameterType = TypeVar("ParameterType", KaneParameters, ExtendedKaneParameters)
PARAMETER_NAMES = tuple(field.name for field in fields(KaneParameters))
EXTENDED_PARAMETER_NAMES = tuple(field.name for field in fields(ExtendedKaneParameters))
OBSERVATION_DIMENSION = 2 * 8 * 8


class ProjectionError(RuntimeError):
    """Raised when a Kane parameter projection is rank deficient."""


def real_vector(matrix: NDArray[np.complex128]) -> NDArray[np.float64]:
    """Stack real and imaginary parts of an 8x8 complex matrix."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    if matrix.shape != (8, 8):
        raise ValueError(f"matrix must have shape (8, 8), got {matrix.shape}")
    flat = matrix.reshape(-1)
    return np.concatenate((flat.real, flat.imag))


_real_vector = real_vector


def _templates(k, parameter_type, parameter_names, model):
    base = model(k, parameter_type())
    templates = {}
    for name in parameter_names:
        kwargs = {parameter_name: 0.0 for parameter_name in parameter_names}
        kwargs[name] = 1.0
        templates[name] = model(k, parameter_type(**kwargs)) - base
    return templates


def fixed_hamiltonian(k: Iterable[float]) -> NDArray[np.complex128]:
    return hamiltonian(k, KaneParameters())


def parameter_templates(k: Iterable[float]) -> dict[str, NDArray[np.complex128]]:
    return _templates(k, KaneParameters, PARAMETER_NAMES, hamiltonian)


def extended_parameter_templates(k: Iterable[float]) -> dict[str, NDArray[np.complex128]]:
    return _templates(k, ExtendedKaneParameters, EXTENDED_PARAMETER_NAMES, hamiltonian_two_p)


def covariance_whitener(
    covariance: NDArray[np.float64],
    *,
    relative_floor: float = 1.0e-12,
) -> tuple[NDArray[np.float64], Mapping[str, float]]:
    """Return a symmetric inverse-square-root whitener for one covariance.

    Eigenvalues below ``relative_floor * lambda_max`` are clipped to that
    floor. The regularization is explicit in the returned diagnostics because
    a poorly conditioned covariance can otherwise dominate the inferred
    parameter uncertainty.
    """

    covariance = np.asarray(covariance, dtype=float)
    if covariance.shape != (OBSERVATION_DIMENSION, OBSERVATION_DIMENSION):
        raise ValueError(
            "each covariance must have shape "
            f"({OBSERVATION_DIMENSION}, {OBSERVATION_DIMENSION})"
        )
    if not np.all(np.isfinite(covariance)):
        raise ValueError("covariance contains non-finite values")
    if not 0.0 < relative_floor < 1.0:
        raise ValueError("relative_floor must lie strictly between zero and one")

    symmetric = 0.5 * (covariance + covariance.T)
    symmetry_residual = np.linalg.norm(covariance - covariance.T, ord="fro")
    scale = max(np.linalg.norm(symmetric, ord="fro"), np.finfo(float).eps)
    if symmetry_residual / scale > 1.0e-10:
        raise ValueError("covariance must be symmetric")

    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    maximum = float(np.max(eigenvalues))
    if maximum <= 0.0:
        raise ValueError("covariance must have at least one positive eigenvalue")
    tolerance = relative_floor * maximum
    if float(np.min(eigenvalues)) < -1.0e-10 * maximum:
        raise ValueError("covariance is not positive semidefinite")

    clipped = np.maximum(eigenvalues, tolerance)
    whitener = (eigenvectors * (1.0 / np.sqrt(clipped))) @ eigenvectors.T
    diagnostics = {
        "minimum_eigenvalue": float(np.min(eigenvalues)),
        "maximum_eigenvalue": maximum,
        "regularization_floor": tolerance,
        "regularized_eigenvalues": float(np.count_nonzero(eigenvalues < tolerance)),
        "condition_number_after_regularization": float(np.max(clipped) / np.min(clipped)),
    }
    return whitener, diagnostics


def _validate_inputs(k_points, matrices, weights, covariances):
    if len(k_points) != len(matrices):
        raise ValueError("k_points and matrices must have equal length")
    if not k_points:
        raise ValueError("at least one k point is required")

    weights_array = (
        np.ones(len(k_points), dtype=float)
        if weights is None
        else np.asarray(weights, dtype=float)
    )
    if weights_array.shape != (len(k_points),):
        raise ValueError("weights must contain one value per k point")
    if np.any(weights_array <= 0.0) or not np.all(np.isfinite(weights_array)):
        raise ValueError("weights must be finite and strictly positive")

    if covariances is not None and len(covariances) != len(k_points):
        raise ValueError("covariances must contain one matrix per k point")
    return weights_array


def _build_whitened_system(
    k_points,
    matrices,
    *,
    parameter_type,
    parameter_names,
    model,
    weights,
    covariances,
    covariance_floor,
):
    weights_array = _validate_inputs(k_points, matrices, weights, covariances)
    rows = []
    targets = []
    covariance_diagnostics = []
    zero = parameter_type()

    for index, (k, matrix, weight) in enumerate(
        zip(k_points, matrices, weights_array, strict=True)
    ):
        matrix = np.asarray(matrix, dtype=np.complex128)
        if matrix.shape != (8, 8):
            raise ValueError(f"each matrix must have shape (8, 8), got {matrix.shape}")

        templates = _templates(k, parameter_type, parameter_names, model)
        design = np.column_stack(
            [real_vector(templates[name]) for name in parameter_names]
        )
        target = real_vector(matrix - model(k, zero))

        if covariances is None:
            whitener = np.eye(OBSERVATION_DIMENSION)
        else:
            whitener, diagnostics = covariance_whitener(
                covariances[index], relative_floor=covariance_floor
            )
            covariance_diagnostics.append(diagnostics)

        scale = float(np.sqrt(weight))
        rows.append(scale * (whitener @ design))
        targets.append(scale * (whitener @ target))

    return (
        np.vstack(rows),
        np.concatenate(targets),
        weights_array,
        covariance_diagnostics,
    )


def _parameter_uncertainty(
    design: NDArray[np.float64],
    residual_sum_squares: float,
    rank: int,
    *,
    covariance_is_absolute: bool,
    parameter_names,
    rcond: float | None,
):
    normal = design.T @ design
    cutoff = 1.0e-15 if rcond is None else rcond
    inverse_normal = np.linalg.pinv(normal, rcond=cutoff, hermitian=True)
    degrees_of_freedom = max(design.shape[0] - rank, 0)

    if covariance_is_absolute:
        scale = 1.0
    elif degrees_of_freedom > 0:
        scale = residual_sum_squares / degrees_of_freedom
    else:
        scale = float("nan")

    parameter_covariance = inverse_normal * scale
    standard_errors_array = np.sqrt(
        np.clip(np.diag(parameter_covariance), a_min=0.0, a_max=None)
    )
    standard_errors = dict(
        zip(parameter_names, standard_errors_array.tolist(), strict=True)
    )

    denominator = np.outer(standard_errors_array, standard_errors_array)
    correlation = np.divide(
        parameter_covariance,
        denominator,
        out=np.zeros_like(parameter_covariance),
        where=denominator > 0.0,
    )
    return {
        "normal_matrix": normal,
        "parameter_covariance": parameter_covariance,
        "parameter_standard_errors": standard_errors,
        "parameter_correlation": correlation,
        "degrees_of_freedom": float(degrees_of_freedom),
        "variance_scale": float(scale),
    }


def _fit_model(
    k_points,
    matrices,
    *,
    parameter_type,
    parameter_names,
    model,
    weights,
    covariances,
    covariance_floor,
    rcond,
):
    a, b, _, covariance_diagnostics = _build_whitened_system(
        k_points,
        matrices,
        parameter_type=parameter_type,
        parameter_names=parameter_names,
        model=model,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
    )

    solution, residuals, rank, singular_values = np.linalg.lstsq(a, b, rcond=rcond)
    if rank < len(parameter_names):
        raise ProjectionError(
            f"rank-deficient Kane projection: rank={rank}, required={len(parameter_names)}"
        )

    predicted = a @ solution
    residual_vector = b - predicted
    residual_sum_squares = float(residual_vector @ residual_vector)
    residual_norm = float(np.sqrt(residual_sum_squares))
    target_norm = max(float(np.linalg.norm(b)), np.finfo(float).eps)
    params = parameter_type(**dict(zip(parameter_names, solution, strict=True)))

    uncertainty = _parameter_uncertainty(
        a,
        residual_sum_squares,
        rank,
        covariance_is_absolute=covariances is not None,
        parameter_names=parameter_names,
        rcond=rcond,
    )
    degrees_of_freedom = int(uncertainty["degrees_of_freedom"])
    diagnostics: dict[str, object] = {
        "rank": float(rank),
        "observation_count": float(a.shape[0]),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "absolute_residual": residual_norm,
        "relative_residual": float(residual_norm / target_norm),
        "chi_square": residual_sum_squares,
        "reduced_chi_square": (
            float(residual_sum_squares / degrees_of_freedom)
            if degrees_of_freedom > 0
            else float("nan")
        ),
        "reported_lstsq_residual": float(residuals[0]) if residuals.size else 0.0,
        "singular_values": singular_values,
        "covariance_diagnostics": covariance_diagnostics,
    }
    diagnostics.update(uncertainty)
    return params, diagnostics


def fit_parameters(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    *,
    weights: Sequence[float] | None = None,
    covariances: Sequence[NDArray[np.float64]] | None = None,
    covariance_floor: float = 1.0e-12,
    rcond: float | None = None,
) -> tuple[KaneParameters, Mapping[str, object]]:
    return _fit_model(
        k_points,
        matrices,
        parameter_type=KaneParameters,
        parameter_names=PARAMETER_NAMES,
        model=hamiltonian,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
        rcond=rcond,
    )


def fit_extended_parameters(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    *,
    weights: Sequence[float] | None = None,
    covariances: Sequence[NDArray[np.float64]] | None = None,
    covariance_floor: float = 1.0e-12,
    rcond: float | None = None,
) -> tuple[ExtendedKaneParameters, Mapping[str, object]]:
    return _fit_model(
        k_points,
        matrices,
        parameter_type=ExtendedKaneParameters,
        parameter_names=EXTENDED_PARAMETER_NAMES,
        model=hamiltonian_two_p,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
        rcond=rcond,
    )


def _closure_residual(k_points, matrices, params, model, *, weights):
    if len(k_points) != len(matrices):
        raise ValueError("k_points and matrices must have equal length")
    if not k_points:
        raise ValueError("at least one k point is required")

    weights_array = (
        np.ones(len(k_points), dtype=float)
        if weights is None
        else np.asarray(weights, dtype=float)
    )
    if weights_array.shape != (len(k_points),):
        raise ValueError("weights must contain one value per k point")

    gamma_reference = None
    for k, matrix in zip(k_points, matrices, strict=True):
        if np.linalg.norm(np.asarray(tuple(k), dtype=float)) < 1e-15:
            gamma_reference = np.asarray(matrix, dtype=np.complex128)
            break

    numerator = 0.0
    denominator = 0.0
    for k, matrix, weight in zip(k_points, matrices, weights_array, strict=True):
        target = np.asarray(matrix, dtype=np.complex128)
        residual = target - model(k, params)
        numerator += float(weight * np.linalg.norm(residual, ord="fro") ** 2)
        reference_difference = target if gamma_reference is None else target - gamma_reference
        denominator += float(weight * np.linalg.norm(reference_difference, ord="fro") ** 2)

    if denominator <= np.finfo(float).eps:
        return 0.0 if numerator <= np.finfo(float).eps else float("inf")
    return float(np.sqrt(numerator / denominator))


def closure_residual(
    k_points,
    matrices,
    params: KaneParameters,
    *,
    weights=None,
) -> float:
    return _closure_residual(k_points, matrices, params, hamiltonian, weights=weights)


def extended_closure_residual(
    k_points,
    matrices,
    params: ExtendedKaneParameters,
    *,
    weights=None,
) -> float:
    return _closure_residual(k_points, matrices, params, hamiltonian_two_p, weights=weights)


def _design_diagnostics(
    k_points,
    *,
    parameter_type,
    parameter_names,
    model,
    weights,
    covariances,
    covariance_floor,
):
    matrices = [model(k, parameter_type()) for k in k_points]
    a, _, _, covariance_diagnostics = _build_whitened_system(
        k_points,
        matrices,
        parameter_type=parameter_type,
        parameter_names=parameter_names,
        model=model,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
    )
    singular_values = np.linalg.svd(a, compute_uv=False)
    tolerance = np.finfo(float).eps * max(a.shape) * singular_values[0]
    rank = int(np.count_nonzero(singular_values > tolerance))
    condition_number = (
        float(singular_values[0] / singular_values[-1])
        if singular_values[-1] > tolerance
        else float("inf")
    )
    return {
        "rank": rank,
        "parameter_count": len(parameter_names),
        "condition_number": condition_number,
        "singular_values": singular_values,
        "covariance_diagnostics": covariance_diagnostics,
    }


def design_diagnostics(
    k_points,
    *,
    weights=None,
    covariances=None,
    covariance_floor: float = 1.0e-12,
) -> Mapping[str, object]:
    return _design_diagnostics(
        k_points,
        parameter_type=KaneParameters,
        parameter_names=PARAMETER_NAMES,
        model=hamiltonian,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
    )


def extended_design_diagnostics(
    k_points,
    *,
    weights=None,
    covariances=None,
    covariance_floor: float = 1.0e-12,
) -> Mapping[str, object]:
    return _design_diagnostics(
        k_points,
        parameter_type=ExtendedKaneParameters,
        parameter_names=EXTENDED_PARAMETER_NAMES,
        model=hamiltonian_two_p,
        weights=weights,
        covariances=covariances,
        covariance_floor=covariance_floor,
    )
