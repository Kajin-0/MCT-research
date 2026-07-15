"""Matrix-level projection onto one-P and two-P bulk Kane manifolds."""

from __future__ import annotations

from dataclasses import fields
from typing import Callable, Iterable, Mapping, Sequence, TypeVar

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


class ProjectionError(RuntimeError):
    """Raised when a Kane parameter projection is rank deficient."""


def _real_vector(matrix: NDArray[np.complex128]) -> NDArray[np.float64]:
    flat = np.asarray(matrix, dtype=np.complex128).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


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


def _fit_model(
    k_points,
    matrices,
    *,
    parameter_type,
    parameter_names,
    model,
    weights,
    rcond,
):
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

    rows = []
    targets = []
    zero = parameter_type()
    for k, matrix, weight in zip(k_points, matrices, weights_array, strict=True):
        matrix = np.asarray(matrix, dtype=np.complex128)
        if matrix.shape != (8, 8):
            raise ValueError(f"each matrix must have shape (8, 8), got {matrix.shape}")
        templates = _templates(k, parameter_type, parameter_names, model)
        design = np.column_stack([_real_vector(templates[name]) for name in parameter_names])
        target = _real_vector(matrix - model(k, zero))
        scale = float(np.sqrt(weight))
        rows.append(scale * design)
        targets.append(scale * target)

    a = np.vstack(rows)
    b = np.concatenate(targets)
    solution, residuals, rank, singular_values = np.linalg.lstsq(a, b, rcond=rcond)
    if rank < len(parameter_names):
        raise ProjectionError(
            f"rank-deficient Kane projection: rank={rank}, required={len(parameter_names)}"
        )

    params = parameter_type(**dict(zip(parameter_names, solution, strict=True)))
    fitted = np.concatenate(
        [
            _real_vector(model(k, params) - model(k, zero)) * np.sqrt(weight)
            for k, weight in zip(k_points, weights_array, strict=True)
        ]
    )
    weighted_target = np.concatenate(targets)
    residual_norm = np.linalg.norm(weighted_target - fitted)
    target_norm = max(np.linalg.norm(weighted_target), np.finfo(float).eps)
    diagnostics = {
        "rank": float(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "absolute_residual": float(residual_norm),
        "relative_residual": float(residual_norm / target_norm),
        "reported_lstsq_residual": float(residuals[0]) if residuals.size else 0.0,
    }
    return params, diagnostics


def fit_parameters(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    *,
    weights: Sequence[float] | None = None,
    rcond: float | None = None,
) -> tuple[KaneParameters, Mapping[str, float]]:
    return _fit_model(
        k_points,
        matrices,
        parameter_type=KaneParameters,
        parameter_names=PARAMETER_NAMES,
        model=hamiltonian,
        weights=weights,
        rcond=rcond,
    )


def fit_extended_parameters(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    *,
    weights: Sequence[float] | None = None,
    rcond: float | None = None,
) -> tuple[ExtendedKaneParameters, Mapping[str, float]]:
    return _fit_model(
        k_points,
        matrices,
        parameter_type=ExtendedKaneParameters,
        parameter_names=EXTENDED_PARAMETER_NAMES,
        model=hamiltonian_two_p,
        weights=weights,
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
):
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

    rows = []
    for k, weight in zip(k_points, weights_array, strict=True):
        templates = _templates(k, parameter_type, parameter_names, model)
        design = np.column_stack([_real_vector(templates[name]) for name in parameter_names])
        rows.append(float(np.sqrt(weight)) * design)

    a = np.vstack(rows)
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
    }


def design_diagnostics(k_points, *, weights=None) -> Mapping[str, object]:
    return _design_diagnostics(
        k_points,
        parameter_type=KaneParameters,
        parameter_names=PARAMETER_NAMES,
        model=hamiltonian,
        weights=weights,
    )


def extended_design_diagnostics(k_points, *, weights=None) -> Mapping[str, object]:
    return _design_diagnostics(
        k_points,
        parameter_type=ExtendedKaneParameters,
        parameter_names=EXTENDED_PARAMETER_NAMES,
        model=hamiltonian_two_p,
        weights=weights,
    )
