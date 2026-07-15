"""Matrix-level projection onto the bulk 8-band Kane parameter manifold."""

from __future__ import annotations

from dataclasses import fields
from typing import Iterable, Mapping, Sequence

import numpy as np
from numpy.typing import NDArray

from .kane8 import KaneParameters, hamiltonian

PARAMETER_NAMES = tuple(field.name for field in fields(KaneParameters))


class ProjectionError(RuntimeError):
    """Raised when the Kane parameter projection is rank deficient."""


def _real_vector(matrix: NDArray[np.complex128]) -> NDArray[np.float64]:
    """Vectorize a complex matrix without discarding phase information."""

    flat = np.asarray(matrix, dtype=np.complex128).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def fixed_hamiltonian(k: Iterable[float]) -> NDArray[np.complex128]:
    """Parameter-independent free-electron conduction contribution."""

    return hamiltonian(k, KaneParameters())


def parameter_templates(k: Iterable[float]) -> dict[str, NDArray[np.complex128]]:
    """Return exact linear templates dH/dp_a at one k point."""

    base = fixed_hamiltonian(k)
    templates: dict[str, NDArray[np.complex128]] = {}
    for name in PARAMETER_NAMES:
        kwargs = {parameter_name: 0.0 for parameter_name in PARAMETER_NAMES}
        kwargs[name] = 1.0
        templates[name] = hamiltonian(k, KaneParameters(**kwargs)) - base
    return templates


def fit_parameters(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    *,
    weights: Sequence[float] | None = None,
    rcond: float | None = None,
) -> tuple[KaneParameters, Mapping[str, float]]:
    """Fit Kane parameters to full complex Hamiltonian matrices.

    The fit solves the real least-squares problem obtained by stacking real
    and imaginary matrix elements. The parameter-independent conduction
    ``alpha*k^2`` term is removed before fitting.
    """

    if len(k_points) != len(matrices):
        raise ValueError("k_points and matrices must have equal length")
    if not k_points:
        raise ValueError("at least one k point is required")

    if weights is None:
        weights_array = np.ones(len(k_points), dtype=float)
    else:
        weights_array = np.asarray(weights, dtype=float)
        if weights_array.shape != (len(k_points),):
            raise ValueError("weights must contain one value per k point")
        if np.any(weights_array <= 0.0) or not np.all(np.isfinite(weights_array)):
            raise ValueError("weights must be finite and strictly positive")

    rows: list[NDArray[np.float64]] = []
    targets: list[NDArray[np.float64]] = []

    for k, matrix, weight in zip(k_points, matrices, weights_array, strict=True):
        matrix = np.asarray(matrix, dtype=np.complex128)
        if matrix.shape != (8, 8):
            raise ValueError(f"each matrix must have shape (8, 8), got {matrix.shape}")
        templates = parameter_templates(k)
        design = np.column_stack([_real_vector(templates[name]) for name in PARAMETER_NAMES])
        target = _real_vector(matrix - fixed_hamiltonian(k))
        scale = float(np.sqrt(weight))
        rows.append(scale * design)
        targets.append(scale * target)

    a = np.vstack(rows)
    b = np.concatenate(targets)
    solution, residuals, rank, singular_values = np.linalg.lstsq(a, b, rcond=rcond)

    if rank < len(PARAMETER_NAMES):
        raise ProjectionError(
            f"rank-deficient Kane projection: rank={rank}, required={len(PARAMETER_NAMES)}"
        )

    params = KaneParameters(**dict(zip(PARAMETER_NAMES, solution, strict=True)))
    fitted = np.concatenate(
        [
            _real_vector(hamiltonian(k, params) - fixed_hamiltonian(k))
            * np.sqrt(weight)
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


def closure_residual(
    k_points: Sequence[Iterable[float]],
    matrices: Sequence[NDArray[np.complex128]],
    params: KaneParameters,
    *,
    weights: Sequence[float] | None = None,
) -> float:
    """Normalized Frobenius residual of a fitted Kane model.

    The denominator is the weighted norm of the supplied matrices after
    subtracting their Gamma-point reference when a Gamma matrix is present;
    otherwise the raw weighted matrix norm is used.
    """

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
        residual = target - hamiltonian(k, params)
        numerator += float(weight * np.linalg.norm(residual, ord="fro") ** 2)
        reference_difference = target if gamma_reference is None else target - gamma_reference
        denominator += float(weight * np.linalg.norm(reference_difference, ord="fro") ** 2)

    if denominator <= np.finfo(float).eps:
        return 0.0 if numerator <= np.finfo(float).eps else float("inf")
    return float(np.sqrt(numerator / denominator))


def design_diagnostics(
    k_points: Sequence[Iterable[float]],
    *,
    weights: Sequence[float] | None = None,
) -> Mapping[str, object]:
    """Return rank and singular-value diagnostics for a proposed k grid.

    This inspects identifiability before any electronic-structure matrices are
    fitted. A rank below the number of parameters means at least one Kane
    invariant is exactly unobservable on the chosen grid.
    """

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

    rows: list[NDArray[np.float64]] = []
    for k, weight in zip(k_points, weights_array, strict=True):
        templates = parameter_templates(k)
        design = np.column_stack([_real_vector(templates[name]) for name in PARAMETER_NAMES])
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
        "parameter_count": len(PARAMETER_NAMES),
        "condition_number": condition_number,
        "singular_values": singular_values,
    }
