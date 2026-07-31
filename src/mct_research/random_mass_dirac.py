"""Minimal one-dimensional random-mass Dirac Hamiltonian for R05 Phase 0."""

from __future__ import annotations

from functools import lru_cache
from math import isfinite, pi
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
ComplexMatrix = NDArray[np.complex128]
BoundaryCondition = Literal["periodic", "antiperiodic"]

_SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _mass_array(mass: ArrayLike) -> FloatArray:
    values = np.asarray(mass, dtype=float)
    if values.ndim != 1 or values.size < 8:
        raise ValueError("mass must be a one-dimensional array with at least 8 points")
    if not np.all(np.isfinite(values)):
        raise ValueError("mass must contain only finite values")
    return np.array(values, dtype=float, copy=True)


def fourier_wave_numbers(
    grid_points: int,
    length: float,
    boundary: BoundaryCondition = "periodic",
) -> FloatArray:
    """Return the discrete Fourier momenta for the selected boundary twist."""

    if isinstance(grid_points, bool) or int(grid_points) != grid_points:
        raise ValueError("grid_points must be an integer")
    count = int(grid_points)
    if count < 8:
        raise ValueError("grid_points must be at least 8")
    box_length = _positive("length", length)
    if boundary not in ("periodic", "antiperiodic"):
        raise ValueError("boundary must be 'periodic' or 'antiperiodic'")
    modes = np.fft.fftfreq(count) * count
    twist = 0.0 if boundary == "periodic" else 0.5
    return np.asarray(2.0 * pi * (modes + twist) / box_length, dtype=float)


@lru_cache(maxsize=32)
def _momentum_matrix_cached(
    grid_points: int,
    length: float,
    boundary: BoundaryCondition,
) -> ComplexMatrix:
    count = int(grid_points)
    box_length = float(length)
    x = np.arange(count, dtype=float) * (box_length / count)
    wave_numbers = fourier_wave_numbers(count, box_length, boundary)
    basis = np.exp(1j * np.outer(x, wave_numbers)) / np.sqrt(count)
    momentum = (basis * wave_numbers[np.newaxis, :]) @ basis.conjugate().T
    momentum = 0.5 * (momentum + momentum.conjugate().T)
    momentum.setflags(write=False)
    return momentum


def fourier_momentum_matrix(
    grid_points: int,
    length: float,
    boundary: BoundaryCondition = "periodic",
) -> ComplexMatrix:
    """Return the Hermitian Fourier-pseudospectral representation of ``-i d/dx``."""

    return np.array(
        _momentum_matrix_cached(int(grid_points), float(length), boundary),
        dtype=complex,
        copy=True,
    )


def dirac_hamiltonian(
    mass: ArrayLike,
    length: float,
    *,
    hbar_velocity: float = 1.0,
    boundary: BoundaryCondition = "periodic",
) -> ComplexMatrix:
    r"""Return ``H = hbar v sigma_x k + M(x) sigma_z``.

    The basis is spinor-major: all coordinates of the ``sigma_z=+1`` component
    followed by all coordinates of the ``sigma_z=-1`` component.
    """

    mass_values = _mass_array(mass)
    box_length = _positive("length", length)
    velocity_scale = _positive("hbar_velocity", hbar_velocity)
    momentum = fourier_momentum_matrix(mass_values.size, box_length, boundary)
    mass_matrix = np.diag(mass_values.astype(complex))
    hamiltonian = velocity_scale * np.kron(_SIGMA_X, momentum) + np.kron(
        _SIGMA_Z, mass_matrix
    )
    return np.asarray(0.5 * (hamiltonian + hamiltonian.conjugate().T), dtype=complex)


def dirac_eigenvalues(
    mass: ArrayLike,
    length: float,
    *,
    hbar_velocity: float = 1.0,
    boundary: BoundaryCondition = "periodic",
) -> FloatArray:
    """Return all sorted eigenvalues of the finite Fourier oracle."""

    values = np.linalg.eigvalsh(
        dirac_hamiltonian(
            mass,
            length,
            hbar_velocity=hbar_velocity,
            boundary=boundary,
        )
    )
    return np.asarray(values, dtype=float)


def homogeneous_reference_eigenvalues(
    grid_points: int,
    length: float,
    mass: float,
    *,
    hbar_velocity: float = 1.0,
    boundary: BoundaryCondition = "periodic",
) -> FloatArray:
    """Return exact finite-box eigenvalues for a constant mass."""

    mass_value = float(mass)
    if not isfinite(mass_value):
        raise ValueError("mass must be finite")
    scale = _positive("hbar_velocity", hbar_velocity)
    wave_numbers = fourier_wave_numbers(grid_points, length, boundary)
    positive = np.sqrt((scale * wave_numbers) ** 2 + mass_value**2)
    return np.sort(np.concatenate((-positive, positive))).astype(float)


def hermiticity_residual(matrix: ArrayLike) -> float:
    """Return a relative Frobenius Hermiticity residual."""

    values = np.asarray(matrix, dtype=complex)
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("matrix must be square")
    scale = max(float(np.linalg.norm(values, ord="fro")), 1.0)
    return float(np.linalg.norm(values - values.conjugate().T, ord="fro") / scale)


def paired_spectrum_residual(eigenvalues: ArrayLike) -> float:
    """Return the maximum particle-hole pairing residual relative to spectral scale."""

    values = np.sort(np.asarray(eigenvalues, dtype=float))
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("eigenvalues must be a finite non-empty one-dimensional array")
    scale = max(float(np.max(np.abs(values))), 1.0)
    return float(np.max(np.abs(values + values[::-1])) / scale)


def periodic_domain_wall_pair(
    grid_points: int,
    length: float,
    mass_amplitude: float,
    wall_width: float,
) -> FloatArray:
    """Return a smooth periodic profile containing two sign-changing walls.

    Near each zero of ``sin(2 pi x/L)``, the profile approaches a hyperbolic
    tangent wall with the declared width.  The two walls are separated by L/2.
    """

    if isinstance(grid_points, bool) or int(grid_points) != grid_points:
        raise ValueError("grid_points must be an integer")
    count = int(grid_points)
    if count < 8:
        raise ValueError("grid_points must be at least 8")
    box_length = _positive("length", length)
    amplitude = _positive("mass_amplitude", mass_amplitude)
    width = _positive("wall_width", wall_width)
    x = np.arange(count, dtype=float) * (box_length / count)
    argument_scale = box_length / (2.0 * pi * width)
    return np.asarray(
        amplitude * np.tanh(argument_scale * np.sin(2.0 * pi * x / box_length)),
        dtype=float,
    )