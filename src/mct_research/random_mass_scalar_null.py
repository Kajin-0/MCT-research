"""Matched homogeneous and scalar-mixture DOS references for R05."""

from __future__ import annotations

from math import erfc, isfinite, pi, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


def _energies(values: ArrayLike) -> FloatArray:
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or result.size == 0:
        raise ValueError("energies must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(result)):
        raise ValueError("energies must be finite")
    return np.array(result, dtype=float, copy=True)


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def homogeneous_dirac_dos(
    energies: ArrayLike,
    mass: float,
    *,
    hbar_velocity: float = 1.0,
) -> FloatArray:
    """Return the infinite-volume 1D homogeneous Dirac DOS per length/species."""

    energy = _energies(energies)
    mass_value = float(mass)
    if not isfinite(mass_value):
        raise ValueError("mass must be finite")
    scale = _positive("hbar_velocity", hbar_velocity)
    absolute_energy = np.abs(energy)
    inside = absolute_energy > abs(mass_value)
    result = np.zeros_like(absolute_energy)
    denominator = np.sqrt(absolute_energy[inside] ** 2 - mass_value**2)
    result[inside] = absolute_energy[inside] / (pi * scale * denominator)
    return result


def gaussian_mass_pdf(mass: ArrayLike, mean_mass: float, sigma_mass: float) -> FloatArray:
    values = np.asarray(mass, dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("mass coordinates must be finite")
    mean = float(mean_mass)
    if not isfinite(mean):
        raise ValueError("mean_mass must be finite")
    sigma = _positive("sigma_mass", sigma_mass)
    return np.exp(-0.5 * ((values - mean) / sigma) ** 2) / (sqrt(2.0 * pi) * sigma)


def gaussian_scalar_mixture_dos(
    energies: ArrayLike,
    mean_mass: float,
    sigma_mass: float,
    *,
    hbar_velocity: float = 1.0,
    quadrature_order: int = 192,
) -> FloatArray:
    r"""Return the matched Gaussian scalar mixture using nonsingular theta quadrature.

    ``M = |E| sin(theta)`` transforms the homogeneous band-edge singularity into

    ``rho = |E|/(pi hbar v) integral P(|E| sin(theta)) dtheta``.
    """

    energy = _energies(energies)
    mean = float(mean_mass)
    if not isfinite(mean):
        raise ValueError("mean_mass must be finite")
    sigma = _positive("sigma_mass", sigma_mass)
    scale = _positive("hbar_velocity", hbar_velocity)
    if isinstance(quadrature_order, bool) or int(quadrature_order) != quadrature_order:
        raise ValueError("quadrature_order must be an integer")
    order = int(quadrature_order)
    if order < 32 or order > 512:
        raise ValueError("quadrature_order must lie from 32 through 512")

    nodes, weights = np.polynomial.legendre.leggauss(order)
    theta = 0.5 * pi * nodes
    theta_weights = 0.5 * pi * weights
    absolute_energy = np.abs(energy)
    mass_nodes = absolute_energy[:, np.newaxis] * np.sin(theta)[np.newaxis, :]
    densities = gaussian_mass_pdf(mass_nodes, mean, sigma)
    integral = densities @ theta_weights
    return np.asarray(absolute_energy * integral / (pi * scale), dtype=float)


def zero_mean_gaussian_scalar_dos_exact(
    energies: ArrayLike,
    sigma_mass: float,
    *,
    hbar_velocity: float = 1.0,
) -> FloatArray:
    """Return the exact zero-mean Gaussian scalar-mixture DOS.

    The direct expression contains ``exp(-q) I0(q)``.  A short asymptotic form
    avoids overflow for large q while preserving the low-energy reference.
    """

    energy = _energies(energies)
    sigma = _positive("sigma_mass", sigma_mass)
    scale = _positive("hbar_velocity", hbar_velocity)
    absolute_energy = np.abs(energy)
    q = absolute_energy**2 / (4.0 * sigma**2)
    scaled_bessel = np.empty_like(q)
    direct = q < 50.0
    scaled_bessel[direct] = np.exp(-q[direct]) * np.i0(q[direct])
    large = ~direct
    if np.any(large):
        q_large = q[large]
        scaled_bessel[large] = (
            1.0
            + 1.0 / (8.0 * q_large)
            + 9.0 / (128.0 * q_large**2)
        ) / np.sqrt(2.0 * pi * q_large)
    return np.asarray(
        absolute_energy * scaled_bessel / (scale * sqrt(2.0 * pi) * sigma),
        dtype=float,
    )


def gaussian_scalar_low_energy_slope(
    mean_mass: float,
    sigma_mass: float,
    *,
    hbar_velocity: float = 1.0,
) -> float:
    """Return the exact coefficient of ``|E|`` in the smooth scalar null."""

    scale = _positive("hbar_velocity", hbar_velocity)
    return float(gaussian_mass_pdf(np.asarray([0.0]), mean_mass, sigma_mass)[0] / scale)


def gaussian_opposite_sign_probability(mean_mass: float, sigma_mass: float) -> float:
    """Return the Gaussian local opposite-sign probability, not a topology metric."""

    mean = float(mean_mass)
    if not isfinite(mean):
        raise ValueError("mean_mass must be finite")
    sigma = float(sigma_mass)
    if not isfinite(sigma) or sigma < 0.0:
        raise ValueError("sigma_mass must be finite and non-negative")
    if sigma == 0.0:
        return 0.5 if mean == 0.0 else 0.0
    return 0.5 * erfc(abs(mean) / (sqrt(2.0) * sigma))