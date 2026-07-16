"""Gauge- and covariance-consistent preprocessing of imported matrices."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable, Sequence

import numpy as np
from numpy.typing import NDArray

from .dataio import MatrixRecord, OBSERVATION_DIMENSION
from .gauge import AlignmentDiagnostics, KANE_IRREP_BLOCKS, rotate_operator
from .symmetry import gamma_irrep_residual, gamma_irrep_symmetrize

ComplexMatrix = NDArray[np.complex128]
RealMatrix = NDArray[np.float64]


@dataclass(frozen=True)
class ProcessingDiagnostics:
    gauge: tuple[AlignmentDiagnostics, ...]
    symmetry_residual_before: float | None
    covariance_trace_before: float | None
    covariance_trace_after: float | None


def rotation_from_overlap(
    overlap: ComplexMatrix,
    *,
    blocks: Sequence[slice | Sequence[int]] | None = None,
    minimum_singular_value: float = 1.0e-8,
) -> tuple[ComplexMatrix, tuple[AlignmentDiagnostics, ...]]:
    """Construct target-to-reference gauge rotation from ``target^dagger reference``."""

    overlap = np.asarray(overlap, dtype=np.complex128)
    if overlap.shape != (8, 8):
        raise ValueError("overlap must have shape (8, 8)")
    if not 0.0 <= minimum_singular_value <= 1.0:
        raise ValueError("minimum_singular_value must lie in [0, 1]")

    selected_blocks = (slice(0, 8),) if blocks is None else tuple(blocks)
    rotation = np.zeros((8, 8), dtype=np.complex128)
    diagnostics: list[AlignmentDiagnostics] = []
    used: set[int] = set()

    for block in selected_blocks:
        indices = np.arange(8)[block] if isinstance(block, slice) else np.asarray(block)
        indices = np.asarray(indices, dtype=int).reshape(-1)
        if indices.size == 0 or np.any(indices < 0) or np.any(indices >= 8):
            raise ValueError("invalid overlap alignment block")
        if any(int(index) in used for index in indices):
            raise ValueError("overlap alignment blocks must be disjoint")
        used.update(int(index) for index in indices)

        block_overlap = overlap[np.ix_(indices, indices)]
        left, singular_values, right_h = np.linalg.svd(block_overlap, full_matrices=False)
        block_rotation = left @ right_h
        minimum = float(np.min(singular_values))
        if minimum < minimum_singular_value:
            raise ValueError(
                "subspace overlap is too small for stable gauge alignment: "
                f"s_min={minimum:.6g}, required={minimum_singular_value:.6g}"
            )
        rotation[np.ix_(indices, indices)] = block_rotation
        clipped = np.clip(singular_values, 0.0, 1.0)
        angles = np.arccos(clipped)
        diagnostics.append(
            AlignmentDiagnostics(
                singular_values=singular_values,
                principal_angles_rad=angles,
                minimum_overlap=minimum,
                maximum_angle_rad=float(np.max(angles)),
                projector_distance=float(
                    np.sqrt(np.mean(np.maximum(0.0, 1.0 - clipped * clipped)))
                ),
                basis_residual=float(
                    np.sqrt(max(0.0, 2.0 - 2.0 * float(np.mean(clipped))))
                ),
            )
        )

    if used != set(range(8)):
        raise ValueError("overlap alignment blocks must cover all eight states")
    return rotation, tuple(diagnostics)


def real_linear_map(
    transform: Callable[[ComplexMatrix], ComplexMatrix],
) -> RealMatrix:
    """Return the 128x128 real representation of a complex-linear matrix map."""

    mapping = np.zeros((OBSERVATION_DIMENSION, OBSERVATION_DIMENSION), dtype=float)
    for column in range(OBSERVATION_DIMENSION):
        basis = np.zeros((8, 8), dtype=np.complex128)
        if column < 64:
            basis.reshape(-1)[column] = 1.0
        else:
            basis.reshape(-1)[column - 64] = 1.0j
        transformed = np.asarray(transform(basis), dtype=np.complex128).reshape(-1)
        mapping[:, column] = np.concatenate((transformed.real, transformed.imag))
    return mapping


def rotate_covariance(covariance: RealMatrix, rotation: ComplexMatrix) -> RealMatrix:
    """Transform matrix covariance consistently with ``O -> U^dagger O U``."""

    covariance = np.asarray(covariance, dtype=float)
    linear_map = real_linear_map(lambda operator: rotate_operator(operator, rotation))
    transformed = linear_map @ covariance @ linear_map.T
    return 0.5 * (transformed + transformed.T)


def project_covariance(
    covariance: RealMatrix,
    transform: Callable[[ComplexMatrix], ComplexMatrix],
) -> RealMatrix:
    """Push a covariance through a linear matrix projection."""

    covariance = np.asarray(covariance, dtype=float)
    linear_map = real_linear_map(transform)
    transformed = linear_map @ covariance @ linear_map.T
    return 0.5 * (transformed + transformed.T)


def process_record(
    record: MatrixRecord,
    *,
    align_blocks: Sequence[slice | Sequence[int]] | None = None,
    restore_gamma_symmetry: bool = True,
    gamma_tolerance_inv_a: float = 1.0e-12,
    minimum_singular_value: float = 1.0e-8,
) -> tuple[MatrixRecord, ProcessingDiagnostics]:
    """Gauge-align and optionally symmetry-restore one imported record."""

    matrix = record.matrix.copy()
    covariance = None if record.covariance is None else record.covariance.copy()
    covariance_trace_before = None if covariance is None else float(np.trace(covariance))
    gauge_diagnostics: tuple[AlignmentDiagnostics, ...] = ()

    if record.basis_overlap is not None:
        blocks = align_blocks
        if blocks is None and np.linalg.norm(record.k_inv_a) <= gamma_tolerance_inv_a:
            blocks = KANE_IRREP_BLOCKS
        rotation, gauge_diagnostics = rotation_from_overlap(
            record.basis_overlap,
            blocks=blocks,
            minimum_singular_value=minimum_singular_value,
        )
        matrix = rotate_operator(matrix, rotation)
        if covariance is not None:
            covariance = rotate_covariance(covariance, rotation)

    symmetry_before = None
    if restore_gamma_symmetry and np.linalg.norm(record.k_inv_a) <= gamma_tolerance_inv_a:
        symmetry_before = gamma_irrep_residual(matrix)
        matrix = gamma_irrep_symmetrize(matrix)
        if covariance is not None:
            covariance = project_covariance(covariance, gamma_irrep_symmetrize)

    processed = replace(
        record,
        matrix=matrix,
        basis_overlap=np.eye(8, dtype=np.complex128),
        covariance=covariance,
        metadata={
            **record.metadata,
            "processed": True,
            "gamma_symmetry_restored": symmetry_before is not None,
        },
    )
    diagnostics = ProcessingDiagnostics(
        gauge=gauge_diagnostics,
        symmetry_residual_before=symmetry_before,
        covariance_trace_before=covariance_trace_before,
        covariance_trace_after=None if covariance is None else float(np.trace(covariance)),
    )
    return processed, diagnostics
