"""Canonical real coordinate systems for 8x8 complex matrices.

Hermitian matrices use an orthonormal 64-coordinate basis under the Frobenius
inner product. General complex matrices retain the legacy 128-coordinate
real/imaginary representation. Covariance transforms are explicit between the
two spaces.
"""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

MATRIX_DIMENSION = 8
HERMITIAN_OBSERVATION_DIMENSION = MATRIX_DIMENSION**2
COMPLEX_OBSERVATION_DIMENSION = 2 * MATRIX_DIMENSION**2
SQRT_TWO = float(np.sqrt(2.0))

ComplexMatrix = NDArray[np.complex128]
RealVector = NDArray[np.float64]
RealMatrix = NDArray[np.float64]


def _matrix(value: ComplexMatrix) -> ComplexMatrix:
    matrix = np.asarray(value, dtype=np.complex128)
    expected = (MATRIX_DIMENSION, MATRIX_DIMENSION)
    if matrix.shape != expected:
        raise ValueError(f"matrix must have shape {expected}, got {matrix.shape}")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("matrix contains non-finite values")
    return matrix


def complex_vector(matrix: ComplexMatrix) -> RealVector:
    """Stack real and imaginary parts of a general complex 8x8 matrix."""

    flat = _matrix(matrix).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def complex_matrix(vector: RealVector) -> ComplexMatrix:
    """Invert :func:`complex_vector`."""

    coordinates = np.asarray(vector, dtype=float)
    if coordinates.shape != (COMPLEX_OBSERVATION_DIMENSION,):
        raise ValueError(
            "complex coordinates must have shape "
            f"({COMPLEX_OBSERVATION_DIMENSION},)"
        )
    if not np.all(np.isfinite(coordinates)):
        raise ValueError("complex coordinates contain non-finite values")
    real = coordinates[: MATRIX_DIMENSION**2].reshape(MATRIX_DIMENSION, MATRIX_DIMENSION)
    imag = coordinates[MATRIX_DIMENSION**2 :].reshape(MATRIX_DIMENSION, MATRIX_DIMENSION)
    return np.asarray(real + 1j * imag, dtype=np.complex128)


def hermitian_residual(matrix: ComplexMatrix) -> float:
    """Return relative Frobenius distance from Hermiticity."""

    value = _matrix(matrix)
    scale = max(float(np.linalg.norm(value, ord="fro")), np.finfo(float).eps)
    return float(np.linalg.norm(value - value.conj().T, ord="fro") / scale)


def hermitian_vector(
    matrix: ComplexMatrix,
    *,
    tolerance: float = 1.0e-10,
) -> RealVector:
    """Map one Hermitian 8x8 matrix to 64 orthonormal real coordinates.

    Ordering is eight real diagonal entries, followed by the scaled real upper
    triangle and then the scaled imaginary upper triangle. Euclidean coordinate
    norm equals matrix Frobenius norm.
    """

    value = _matrix(matrix)
    residual = hermitian_residual(value)
    if residual > tolerance:
        raise ValueError(
            f"matrix must be Hermitian within tolerance: residual={residual:.6g}"
        )
    value = 0.5 * (value + value.conj().T)
    diagonal = np.real(np.diag(value))
    upper = np.triu_indices(MATRIX_DIMENSION, k=1)
    real_upper = SQRT_TWO * np.real(value[upper])
    imag_upper = SQRT_TWO * np.imag(value[upper])
    return np.concatenate((diagonal, real_upper, imag_upper))


def hermitian_matrix(vector: RealVector) -> ComplexMatrix:
    """Invert :func:`hermitian_vector`."""

    coordinates = np.asarray(vector, dtype=float)
    if coordinates.shape != (HERMITIAN_OBSERVATION_DIMENSION,):
        raise ValueError(
            "Hermitian coordinates must have shape "
            f"({HERMITIAN_OBSERVATION_DIMENSION},)"
        )
    if not np.all(np.isfinite(coordinates)):
        raise ValueError("Hermitian coordinates contain non-finite values")

    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    matrix[np.diag_indices(MATRIX_DIMENSION)] = coordinates[:MATRIX_DIMENSION]
    upper = np.triu_indices(MATRIX_DIMENSION, k=1)
    count = upper[0].size
    real_upper = coordinates[MATRIX_DIMENSION : MATRIX_DIMENSION + count] / SQRT_TWO
    imag_upper = coordinates[MATRIX_DIMENSION + count :] / SQRT_TWO
    matrix[upper] = real_upper + 1j * imag_upper
    matrix[(upper[1], upper[0])] = real_upper - 1j * imag_upper
    return matrix


def hermitian_embedding() -> RealMatrix:
    """Return the 128x64 orthonormal embedding into complex coordinates."""

    embedding = np.zeros(
        (COMPLEX_OBSERVATION_DIMENSION, HERMITIAN_OBSERVATION_DIMENSION),
        dtype=float,
    )
    for column in range(HERMITIAN_OBSERVATION_DIMENSION):
        basis = np.zeros(HERMITIAN_OBSERVATION_DIMENSION, dtype=float)
        basis[column] = 1.0
        embedding[:, column] = complex_vector(hermitian_matrix(basis))
    return embedding


_HERMITIAN_EMBEDDING = hermitian_embedding()


def legacy_covariance_to_hermitian(covariance: RealMatrix) -> RealMatrix:
    """Project one legacy 128D covariance onto the Hermitian subspace."""

    value = np.asarray(covariance, dtype=float)
    expected = (COMPLEX_OBSERVATION_DIMENSION, COMPLEX_OBSERVATION_DIMENSION)
    if value.shape != expected:
        raise ValueError(f"legacy covariance must have shape {expected}")
    transformed = _HERMITIAN_EMBEDDING.T @ value @ _HERMITIAN_EMBEDDING
    return 0.5 * (transformed + transformed.T)


def hermitian_covariance_to_legacy(covariance: RealMatrix) -> RealMatrix:
    """Embed a 64D Hermitian covariance into the legacy 128D space."""

    value = np.asarray(covariance, dtype=float)
    expected = (HERMITIAN_OBSERVATION_DIMENSION, HERMITIAN_OBSERVATION_DIMENSION)
    if value.shape != expected:
        raise ValueError(f"Hermitian covariance must have shape {expected}")
    transformed = _HERMITIAN_EMBEDDING @ value @ _HERMITIAN_EMBEDDING.T
    return 0.5 * (transformed + transformed.T)


def complex_real_linear_map(
    transform: Callable[[ComplexMatrix], ComplexMatrix],
) -> RealMatrix:
    """Return the 128D real representation of a real-linear matrix map."""

    mapping = np.zeros(
        (COMPLEX_OBSERVATION_DIMENSION, COMPLEX_OBSERVATION_DIMENSION), dtype=float
    )
    for column in range(COMPLEX_OBSERVATION_DIMENSION):
        basis = np.zeros(COMPLEX_OBSERVATION_DIMENSION, dtype=float)
        basis[column] = 1.0
        transformed = _matrix(transform(complex_matrix(basis)))
        mapping[:, column] = complex_vector(transformed)
    return mapping


def hermitian_real_linear_map(
    transform: Callable[[ComplexMatrix], ComplexMatrix],
    *,
    tolerance: float = 1.0e-10,
) -> RealMatrix:
    """Return the 64D real representation of a Hermiticity-preserving map."""

    mapping = np.zeros(
        (HERMITIAN_OBSERVATION_DIMENSION, HERMITIAN_OBSERVATION_DIMENSION),
        dtype=float,
    )
    for column in range(HERMITIAN_OBSERVATION_DIMENSION):
        basis = np.zeros(HERMITIAN_OBSERVATION_DIMENSION, dtype=float)
        basis[column] = 1.0
        transformed = _matrix(transform(hermitian_matrix(basis)))
        mapping[:, column] = hermitian_vector(transformed, tolerance=tolerance)
    return mapping


def covariance_linear_map(
    covariance: RealMatrix,
    transform: Callable[[ComplexMatrix], ComplexMatrix],
) -> RealMatrix:
    """Push a 64D Hermitian or 128D complex covariance through a map."""

    value = np.asarray(covariance, dtype=float)
    if value.shape == (
        HERMITIAN_OBSERVATION_DIMENSION,
        HERMITIAN_OBSERVATION_DIMENSION,
    ):
        mapping = hermitian_real_linear_map(transform)
    elif value.shape == (
        COMPLEX_OBSERVATION_DIMENSION,
        COMPLEX_OBSERVATION_DIMENSION,
    ):
        mapping = complex_real_linear_map(transform)
    else:
        raise ValueError(
            "covariance must use 64D Hermitian or 128D complex coordinates"
        )
    transformed = mapping @ value @ mapping.T
    return 0.5 * (transformed + transformed.T)
