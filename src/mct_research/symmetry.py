"""Symmetry-restoration utilities for the Kane basis."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from .gauge import KANE_IRREP_BLOCKS
from .kane8 import time_reversal_unitary

ComplexMatrix = NDArray[np.complex128]


def hermitize(matrix: ComplexMatrix) -> ComplexMatrix:
    """Return the Hermitian part of a square matrix."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    return 0.5 * (matrix + matrix.conjugate().T)


def gamma_irrep_symmetrize(
    matrix: ComplexMatrix,
    *,
    blocks: Sequence[slice | Sequence[int]] = KANE_IRREP_BLOCKS,
) -> ComplexMatrix:
    """Project a Gamma-point operator onto the cubic irrep scalar form.

    For one copy each of ``Gamma6``, ``Gamma8``, and ``Gamma7``, Schur's
    lemma requires the symmetry-preserving operator to be scalar within each
    irreducible block and zero between inequivalent blocks. Complex block
    traces are retained, so this also applies to a non-Hermitian self-energy.
    """

    matrix = np.asarray(matrix, dtype=np.complex128)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    dimension = matrix.shape[0]
    result = np.zeros_like(matrix)

    used: set[int] = set()
    for block in blocks:
        indices = np.arange(dimension)[block] if isinstance(block, slice) else np.asarray(block)
        indices = np.asarray(indices, dtype=int).reshape(-1)
        if indices.size == 0:
            raise ValueError("symmetry blocks must not be empty")
        if np.any(indices < 0) or np.any(indices >= dimension):
            raise ValueError("symmetry block index is out of range")
        if any(int(index) in used for index in indices):
            raise ValueError("symmetry blocks must be disjoint")
        used.update(int(index) for index in indices)
        scalar = np.trace(matrix[np.ix_(indices, indices)]) / indices.size
        result[np.ix_(indices, indices)] = scalar * np.eye(indices.size)

    if used != set(range(dimension)):
        missing = sorted(set(range(dimension)) - used)
        raise ValueError(f"symmetry blocks do not cover all indices: {missing}")
    return result


def gamma_irrep_residual(matrix: ComplexMatrix) -> float:
    """Normalized distance from the symmetry-preserving Gamma-point form."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    projected = gamma_irrep_symmetrize(matrix)
    scale = max(np.linalg.norm(matrix, ord="fro"), np.finfo(float).eps)
    return float(np.linalg.norm(matrix - projected, ord="fro") / scale)


def forbidden_gamma_coupling_norm(matrix: ComplexMatrix) -> float:
    """Return the normalized Gamma6-Gamma8 coupling magnitude."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    if matrix.shape != (8, 8):
        raise ValueError("matrix must have shape (8, 8)")
    coupling = matrix[0:2, 2:6]
    scale = max(np.linalg.norm(matrix, ord="fro"), np.finfo(float).eps)
    return float(np.sqrt(2.0) * np.linalg.norm(coupling, ord="fro") / scale)


def time_reversal_pair_symmetrize(
    matrix_at_k: ComplexMatrix,
    matrix_at_minus_k: ComplexMatrix,
) -> tuple[ComplexMatrix, ComplexMatrix]:
    """Symmetrize a pair so ``H(k)=U_T H(-k)^* U_T^dagger`` exactly."""

    matrix_at_k = np.asarray(matrix_at_k, dtype=np.complex128)
    matrix_at_minus_k = np.asarray(matrix_at_minus_k, dtype=np.complex128)
    if matrix_at_k.shape != matrix_at_minus_k.shape or matrix_at_k.shape != (8, 8):
        raise ValueError("both matrices must have shape (8, 8)")

    unitary = time_reversal_unitary()
    transformed_minus = unitary @ matrix_at_minus_k.conjugate() @ unitary.conjugate().T
    sym_k = 0.5 * (matrix_at_k + transformed_minus)

    transformed_k = unitary @ matrix_at_k.conjugate() @ unitary.conjugate().T
    sym_minus = 0.5 * (matrix_at_minus_k + transformed_k)
    return sym_k, sym_minus


def time_reversal_pair_residual(
    matrix_at_k: ComplexMatrix,
    matrix_at_minus_k: ComplexMatrix,
) -> float:
    """Normalized residual of the time-reversal pair relation."""

    matrix_at_k = np.asarray(matrix_at_k, dtype=np.complex128)
    matrix_at_minus_k = np.asarray(matrix_at_minus_k, dtype=np.complex128)
    unitary = time_reversal_unitary()
    transformed = unitary @ matrix_at_minus_k.conjugate() @ unitary.conjugate().T
    scale = max(np.linalg.norm(matrix_at_k, ord="fro"), np.finfo(float).eps)
    return float(np.linalg.norm(matrix_at_k - transformed, ord="fro") / scale)
