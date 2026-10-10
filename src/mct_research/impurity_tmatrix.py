"""Finite-rank lattice impurity T matrices and their true energy derivatives.

An embedded resolvent is g=P(z-H)^(-1)P*. Its derivative is NOT -g@g:
propagation outside the support must be retained. No positivity assertion is
made for the real derivative inside a host continuum.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class SpectralEmbedding:
    """Columns are embedded host eigenmodes including sqrt(quadrature weight)."""

    energies: NDArray
    modes: NDArray

    def resolvent(self, z: complex, derivative: int = 0) -> NDArray:
        if derivative not in (0, 1):
            raise ValueError("Only the resolvent and its first derivative are supported")
        denominators = z - self.energies
        if np.any(denominators == 0):
            raise ValueError("Evaluation at an unresolved host pole")
        factors = 1 / denominators if derivative == 0 else -1 / denominators**2
        return (self.modes * factors) @ self.modes.conj().T

    def derivative_contraction(self, z: complex, vectors: NDArray) -> NDArray:
        """vectors* g'(z) vectors, without forming a dense g' matrix."""
        projected = self.modes.conj().T @ vectors
        return -projected.conj().T @ (projected / (z - self.energies)[:, None] ** 2)


def t_matrix(potential: NDArray, resolvent: NDArray) -> NDArray:
    """T=(1-Vg)^(-1)V = V(1-gV)^(-1), allowing singular V."""
    identity = np.eye(potential.shape[0], dtype=complex)
    return np.linalg.solve(identity - potential @ resolvent, potential)


def t_derivative(t: NDArray, resolvent_derivative: NDArray) -> NDArray:
    return t @ resolvent_derivative @ t


def branch_trace(matrix: NDArray, states: NDArray) -> complex:
    """Trace per state in a degenerate Gamma sector; states need not be local-unit norm."""
    return complex(np.trace(states.conj().T @ matrix @ states) / states.shape[1])


def endpoint_reference_shifts(full_h: float, full_c: float, chord_slope: float) -> tuple[float, float]:
    """Residual dilute shifts when the coherent reference already contains the chord."""
    return full_h - chord_slope, full_c + chord_slope


def mass_hermite(x: NDArray | float, mass_h: float, mass_c: float,
                 full_t_h: float, full_t_c: float) -> NDArray:
    """Endpoint cubic using FULL host-referenced T: u0=tH, u1=-tC.

    This is a boundary interpolation, not a claim that it is the alloy mass.
    Common-mode projection/analytic continuation must be specified separately.
    """
    x = np.asarray(x)
    delta = mass_c - mass_h
    k = x * (1 - x)
    return (mass_h + delta * x + (full_t_h + full_t_c) * k / 2
            + (full_t_h - full_t_c - 2 * delta) * k * (1 - 2 * x) / 2)
