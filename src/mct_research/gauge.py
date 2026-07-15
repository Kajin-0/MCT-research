"""Gauge alignment utilities for projected electronic subspaces.

The functions operate on column-orthonormal basis matrices. They solve the
unitary orthogonal-Procrustes problem by the polar factor of the overlap
matrix and expose principal-angle diagnostics needed to reject unstable
alignments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import NDArray

ComplexMatrix = NDArray[np.complex128]
KANE_IRREP_BLOCKS: tuple[slice, ...] = (slice(0, 2), slice(2, 6), slice(6, 8))


class GaugeAlignmentError(RuntimeError):
    """Raised when two subspaces cannot be aligned stably."""


@dataclass(frozen=True)
class AlignmentDiagnostics:
    """Condition and residual diagnostics for one aligned subspace."""

    singular_values: NDArray[np.float64]
    principal_angles_rad: NDArray[np.float64]
    minimum_overlap: float
    maximum_angle_rad: float
    projector_distance: float
    basis_residual: float


def _as_basis(basis: ComplexMatrix, *, name: str) -> ComplexMatrix:
    array = np.asarray(basis, dtype=np.complex128)
    if array.ndim != 2:
        raise ValueError(f"{name} must be a two-dimensional basis matrix")
    if array.shape[0] < array.shape[1]:
        raise ValueError(f"{name} must have at least as many rows as columns")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains non-finite values")
    return array


def orthonormality_residual(basis: ComplexMatrix) -> float:
    """Return ``||B^dagger B-I||_F / sqrt(m)`` for an ``N x m`` basis."""

    basis = _as_basis(basis, name="basis")
    dimension = basis.shape[1]
    gram = basis.conjugate().T @ basis
    return float(np.linalg.norm(gram - np.eye(dimension), ord="fro") / np.sqrt(dimension))


def _validate_orthonormal(basis: ComplexMatrix, *, name: str, tolerance: float) -> None:
    residual = orthonormality_residual(basis)
    if residual > tolerance:
        raise ValueError(
            f"{name} columns are not orthonormal: residual={residual:.3e}, "
            f"tolerance={tolerance:.3e}"
        )


def procrustes_unitary(
    reference: ComplexMatrix,
    target: ComplexMatrix,
    *,
    minimum_singular_value: float = 1.0e-8,
    orthonormality_tolerance: float = 1.0e-10,
) -> tuple[ComplexMatrix, AlignmentDiagnostics]:
    """Return the unitary that rotates ``target`` toward ``reference``.

    The returned matrix ``U`` minimizes ``||target @ U - reference||_F``
    over unitary ``U``. The singular values of ``target^dagger reference``
    are the cosines of the principal angles between the two subspaces.
    """

    reference = _as_basis(reference, name="reference")
    target = _as_basis(target, name="target")
    if reference.shape != target.shape:
        raise ValueError(
            f"reference and target must have equal shape, got "
            f"{reference.shape} and {target.shape}"
        )
    if not 0.0 <= minimum_singular_value <= 1.0:
        raise ValueError("minimum_singular_value must lie in [0, 1]")

    _validate_orthonormal(
        reference, name="reference", tolerance=orthonormality_tolerance
    )
    _validate_orthonormal(target, name="target", tolerance=orthonormality_tolerance)

    overlap = target.conjugate().T @ reference
    left, singular_values, right_h = np.linalg.svd(overlap, full_matrices=False)
    rotation = left @ right_h

    minimum_overlap = float(np.min(singular_values))
    if minimum_overlap < minimum_singular_value:
        raise GaugeAlignmentError(
            "subspace overlap is too small for stable gauge alignment: "
            f"s_min={minimum_overlap:.6g}, required={minimum_singular_value:.6g}"
        )

    aligned = target @ rotation
    clipped = np.clip(singular_values, 0.0, 1.0)
    angles = np.arccos(clipped)
    projector_reference = reference @ reference.conjugate().T
    projector_target = target @ target.conjugate().T
    dimension = reference.shape[1]
    diagnostics = AlignmentDiagnostics(
        singular_values=singular_values,
        principal_angles_rad=angles,
        minimum_overlap=minimum_overlap,
        maximum_angle_rad=float(np.max(angles)),
        projector_distance=float(
            np.linalg.norm(projector_reference - projector_target, ord="fro")
            / np.sqrt(2.0 * dimension)
        ),
        basis_residual=float(
            np.linalg.norm(aligned - reference, ord="fro") / np.sqrt(dimension)
        ),
    )
    return rotation, diagnostics


def align_basis(
    reference: ComplexMatrix,
    target: ComplexMatrix,
    *,
    blocks: Sequence[slice | Sequence[int]] | None = None,
    minimum_singular_value: float = 1.0e-8,
    orthonormality_tolerance: float = 1.0e-10,
) -> tuple[ComplexMatrix, ComplexMatrix, tuple[AlignmentDiagnostics, ...]]:
    """Align a target basis globally or block by block.

    Block-restricted alignment is the appropriate default at ``Gamma`` for
    the Kane irreducible subspaces ``Gamma6``, ``Gamma8``, and ``Gamma7``.
    It prevents an arbitrary numerical rotation from mixing inequivalent
    irreducible representations when their eigenvalues approach one another.
    """

    reference = _as_basis(reference, name="reference")
    target = _as_basis(target, name="target")
    if reference.shape != target.shape:
        raise ValueError("reference and target must have equal shape")

    dimension = reference.shape[1]
    if blocks is None:
        rotation, diagnostics = procrustes_unitary(
            reference,
            target,
            minimum_singular_value=minimum_singular_value,
            orthonormality_tolerance=orthonormality_tolerance,
        )
        return target @ rotation, rotation, (diagnostics,)

    rotation = np.zeros((dimension, dimension), dtype=np.complex128)
    used: set[int] = set()
    all_diagnostics: list[AlignmentDiagnostics] = []
    for block in blocks:
        indices = np.arange(dimension)[block] if isinstance(block, slice) else np.asarray(block)
        indices = np.asarray(indices, dtype=int).reshape(-1)
        if indices.size == 0:
            raise ValueError("alignment blocks must not be empty")
        if np.any(indices < 0) or np.any(indices >= dimension):
            raise ValueError("alignment block index is out of range")
        if len(set(indices.tolist())) != indices.size:
            raise ValueError("alignment blocks may not repeat an index")
        if any(int(index) in used for index in indices):
            raise ValueError("alignment blocks must be disjoint")
        used.update(int(index) for index in indices)

        block_rotation, diagnostics = procrustes_unitary(
            reference[:, indices],
            target[:, indices],
            minimum_singular_value=minimum_singular_value,
            orthonormality_tolerance=orthonormality_tolerance,
        )
        rotation[np.ix_(indices, indices)] = block_rotation
        all_diagnostics.append(diagnostics)

    if used != set(range(dimension)):
        missing = sorted(set(range(dimension)) - used)
        raise ValueError(f"alignment blocks do not cover all basis columns: {missing}")

    return target @ rotation, rotation, tuple(all_diagnostics)


def rotate_operator(operator: ComplexMatrix, basis_rotation: ComplexMatrix) -> ComplexMatrix:
    """Transform an operator after the basis change ``B -> B U``."""

    operator = np.asarray(operator, dtype=np.complex128)
    basis_rotation = np.asarray(basis_rotation, dtype=np.complex128)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("operator must be square")
    if basis_rotation.shape != operator.shape:
        raise ValueError("basis_rotation must have the same shape as operator")
    return basis_rotation.conjugate().T @ operator @ basis_rotation


def parallel_transport_sequence(
    bases: Iterable[ComplexMatrix],
    *,
    anchor: ComplexMatrix | None = None,
    minimum_singular_value: float = 1.0e-8,
) -> tuple[list[ComplexMatrix], list[ComplexMatrix], list[AlignmentDiagnostics]]:
    """Sequentially align a path of bases by discrete parallel transport."""

    raw = [np.asarray(basis, dtype=np.complex128) for basis in bases]
    if not raw:
        raise ValueError("at least one basis is required")

    aligned: list[ComplexMatrix] = []
    rotations: list[ComplexMatrix] = []
    diagnostics: list[AlignmentDiagnostics] = []

    if anchor is None:
        first = raw[0]
        _validate_orthonormal(first, name="first basis", tolerance=1.0e-10)
        aligned.append(first.copy())
        rotations.append(np.eye(first.shape[1], dtype=np.complex128))
        start_index = 1
    else:
        first_aligned, first_rotation, first_diagnostics = align_basis(
            anchor,
            raw[0],
            minimum_singular_value=minimum_singular_value,
        )
        aligned.append(first_aligned)
        rotations.append(first_rotation)
        diagnostics.extend(first_diagnostics)
        start_index = 1

    for index in range(start_index, len(raw)):
        next_aligned, rotation, step_diagnostics = align_basis(
            aligned[-1],
            raw[index],
            minimum_singular_value=minimum_singular_value,
        )
        aligned.append(next_aligned)
        rotations.append(rotation)
        diagnostics.extend(step_diagnostics)

    return aligned, rotations, diagnostics
