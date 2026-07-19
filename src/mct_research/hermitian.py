"""Independent real coordinates for Hermitian 8x8 matrix observables.

The coordinate map is an isometry for the Frobenius inner product.  Diagonal
entries are stored directly.  For every upper-triangular entry ``H[i, j]`` with
``i < j``, the vector stores ``sqrt(2) * Re(H[i, j])`` and
``sqrt(2) * Im(H[i, j])``.  Consequently an 8x8 Hermitian matrix has exactly 64
independent real coordinates and ``dot(hvec(A), hvec(B)) == Re tr(A^dagger B)``.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Final

import numpy as np
from numpy.typing import ArrayLike, NDArray

MATRIX_DIMENSION: Final[int] = 8
OBSERVATION_DIMENSION: Final[int] = MATRIX_DIMENSION**2
LEGACY_COMPLEX_CARTESIAN_DIMENSION: Final[int] = 2 * MATRIX_DIMENSION**2
SQRT_TWO: Final[float] = float(np.sqrt(2.0))

ComplexMatrix = NDArray[np.complex128]
RealVector = NDArray[np.float64]
RealMatrix = NDArray[np.float64]


def _as_square_matrix(matrix: ArrayLike, *, name: str = "matrix") -> ComplexMatrix:
    candidate = np.asarray(matrix, dtype=np.complex128)
    expected = (MATRIX_DIMENSION, MATRIX_DIMENSION)
    if candidate.shape != expected:
        raise ValueError(f"{name} must have shape {expected}, got {candidate.shape}")
    if not np.all(np.isfinite(candidate)):
        raise ValueError(f"{name} contains non-finite values")
    return candidate


def hermiticity_residual(matrix: ArrayLike) -> float:
    """Return normalized Frobenius distance from Hermiticity."""

    candidate = _as_square_matrix(matrix)
    scale = max(float(np.linalg.norm(candidate, ord="fro")), np.finfo(float).eps)
    return float(np.linalg.norm(candidate - candidate.conjugate().T, ord="fro") / scale)


def hermitize(matrix: ArrayLike) -> ComplexMatrix:
    """Return the Hermitian projection of an 8x8 complex matrix."""

    candidate = _as_square_matrix(matrix)
    return 0.5 * (candidate + candidate.conjugate().T)


def hermitian_vector(
    matrix: ArrayLike,
    *,
    hermiticity_tolerance: float = 1.0e-10,
) -> RealVector:
    """Return the 64 independent Frobenius-isometric Hermitian coordinates."""

    candidate = _as_square_matrix(matrix)
    if not np.isfinite(hermiticity_tolerance) or hermiticity_tolerance < 0.0:
        raise ValueError("hermiticity_tolerance must be finite and non-negative")
    residual = hermiticity_residual(candidate)
    if residual > hermiticity_tolerance:
        raise ValueError(
            "matrix must be Hermitian for 64D coordinates: "
            f"residual={residual:.3e}, tolerance={hermiticity_tolerance:.3e}"
        )

    result = np.empty(OBSERVATION_DIMENSION, dtype=float)
    result[:MATRIX_DIMENSION] = np.diag(candidate).real
    index = MATRIX_DIMENSION
    for row in range(MATRIX_DIMENSION):
        for column in range(row + 1, MATRIX_DIMENSION):
            value = candidate[row, column]
            result[index] = SQRT_TWO * value.real
            result[index + 1] = SQRT_TWO * value.imag
            index += 2
    if index != OBSERVATION_DIMENSION:
        raise RuntimeError("Hermitian coordinate construction has the wrong size")
    return result


def matrix_from_hermitian_vector(vector: ArrayLike) -> ComplexMatrix:
    """Reconstruct an 8x8 Hermitian matrix from 64 independent coordinates."""

    values = np.asarray(vector, dtype=float)
    if values.shape != (OBSERVATION_DIMENSION,):
        raise ValueError(
            f"vector must have shape ({OBSERVATION_DIMENSION},), got {values.shape}"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("vector contains non-finite values")

    result = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    result[np.diag_indices(MATRIX_DIMENSION)] = values[:MATRIX_DIMENSION]
    index = MATRIX_DIMENSION
    for row in range(MATRIX_DIMENSION):
        for column in range(row + 1, MATRIX_DIMENSION):
            value = (values[index] + 1j * values[index + 1]) / SQRT_TWO
            result[row, column] = value
            result[column, row] = np.conjugate(value)
            index += 2
    return result


def complex_cartesian_vector(matrix: ArrayLike) -> RealVector:
    """Return the legacy 128D real/imaginary vector of a general complex matrix."""

    candidate = _as_square_matrix(matrix)
    flat = candidate.reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def matrix_from_complex_cartesian_vector(vector: ArrayLike) -> ComplexMatrix:
    """Reconstruct a general complex 8x8 matrix from legacy 128D coordinates."""

    values = np.asarray(vector, dtype=float)
    if values.shape != (LEGACY_COMPLEX_CARTESIAN_DIMENSION,):
        raise ValueError(
            "legacy vector must have shape "
            f"({LEGACY_COMPLEX_CARTESIAN_DIMENSION},), got {values.shape}"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("legacy vector contains non-finite values")
    split = MATRIX_DIMENSION**2
    return (values[:split] + 1j * values[split:]).reshape(
        MATRIX_DIMENSION, MATRIX_DIMENSION
    )


def hermitian_linear_map(
    transform: Callable[[ComplexMatrix], ComplexMatrix],
) -> RealMatrix:
    """Return the 64x64 real map induced on Hermitian coordinates."""

    mapping = np.empty((OBSERVATION_DIMENSION, OBSERVATION_DIMENSION), dtype=float)
    for column in range(OBSERVATION_DIMENSION):
        basis_vector = np.zeros(OBSERVATION_DIMENSION, dtype=float)
        basis_vector[column] = 1.0
        basis_matrix = matrix_from_hermitian_vector(basis_vector)
        transformed = np.asarray(transform(basis_matrix), dtype=np.complex128)
        mapping[:, column] = hermitian_vector(transformed)
    return mapping


@lru_cache(maxsize=1)
def legacy_hermitian_projection_map() -> RealMatrix:
    """Return the 64x128 map from legacy coordinates to Hermitian coordinates.

    The map first projects a general complex matrix onto its Hermitian part and
    then applies the Frobenius-isometric 64D coordinate map.  It exists only for
    explicit migration of schema-1 covariance; new data must be supplied in 64D.
    """

    mapping = np.empty(
        (OBSERVATION_DIMENSION, LEGACY_COMPLEX_CARTESIAN_DIMENSION), dtype=float
    )
    for column in range(LEGACY_COMPLEX_CARTESIAN_DIMENSION):
        basis_vector = np.zeros(LEGACY_COMPLEX_CARTESIAN_DIMENSION, dtype=float)
        basis_vector[column] = 1.0
        matrix = matrix_from_complex_cartesian_vector(basis_vector)
        mapping[:, column] = hermitian_vector(hermitize(matrix))
    mapping.setflags(write=False)
    return mapping


def legacy_covariance_to_hermitian(covariance: ArrayLike) -> RealMatrix:
    """Project a legacy 128D covariance into the independent 64D coordinates."""

    candidate = np.asarray(covariance, dtype=float)
    expected = (
        LEGACY_COMPLEX_CARTESIAN_DIMENSION,
        LEGACY_COMPLEX_CARTESIAN_DIMENSION,
    )
    if candidate.shape != expected:
        raise ValueError(f"legacy covariance must have shape {expected}, got {candidate.shape}")
    if not np.all(np.isfinite(candidate)):
        raise ValueError("legacy covariance contains non-finite values")
    symmetric = 0.5 * (candidate + candidate.T)
    scale = max(float(np.linalg.norm(symmetric, ord="fro")), np.finfo(float).eps)
    if np.linalg.norm(candidate - candidate.T, ord="fro") / scale > 1.0e-10:
        raise ValueError("legacy covariance must be symmetric")
    eigenvalues = np.linalg.eigvalsh(symmetric)
    maximum = max(float(np.max(eigenvalues)), np.finfo(float).eps)
    if float(np.min(eigenvalues)) < -1.0e-10 * maximum:
        raise ValueError("legacy covariance must be positive semidefinite")

    projection = legacy_hermitian_projection_map()
    result = projection @ symmetric @ projection.T
    return 0.5 * (result + result.T)
