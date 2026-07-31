from __future__ import annotations

import numpy as np

from mct_research.random_mass_dos import (
    finite_box_gaussian_quadrature_dos,
    gaussian_convolve_uniform_grid,
)
from mct_research.random_mass_scalar_null import (
    gaussian_opposite_sign_probability,
    gaussian_scalar_low_energy_slope,
    gaussian_scalar_mixture_dos,
    zero_mean_gaussian_scalar_dos_exact,
)


def _integrate(values: np.ndarray, coordinates: np.ndarray) -> float:
    implementation = getattr(np, "trapezoid", None)
    if implementation is None:
        implementation = np.trapz
    return float(implementation(values, coordinates))


def test_scalar_quadrature_matches_exact_zero_mean_gaussian_formula() -> None:
    energies = np.linspace(-3.0, 3.0, 301)
    quadrature = gaussian_scalar_mixture_dos(
        energies, 0.0, 0.8, quadrature_order=256
    )
    exact = zero_mean_gaussian_scalar_dos_exact(energies, 0.8)
    assert np.max(np.abs(quadrature - exact)) < 2.0e-12


def test_scalar_low_energy_slope_matches_probability_density_at_zero() -> None:
    energies = np.array([1.0e-5, 2.0e-5, 4.0e-5])
    values = gaussian_scalar_mixture_dos(
        energies, 0.4, 0.7, quadrature_order=256
    )
    slope = gaussian_scalar_low_energy_slope(0.4, 0.7)
    assert np.max(np.abs(values / energies - slope) / slope) < 1.0e-8


def test_boundary_averaged_finite_box_null_matches_broadened_analytic_null() -> None:
    energies = np.linspace(-3.0, 3.0, 601)
    periodic = finite_box_gaussian_quadrature_dos(
        energies,
        0.0,
        0.8,
        64.0,
        128,
        0.12,
        boundary="periodic",
        quadrature_order=128,
    )
    antiperiodic = finite_box_gaussian_quadrature_dos(
        energies,
        0.0,
        0.8,
        64.0,
        128,
        0.12,
        boundary="antiperiodic",
        quadrature_order=128,
    )
    finite = 0.5 * (periodic + antiperiodic)
    analytic = gaussian_scalar_mixture_dos(energies, 0.0, 0.8)
    broadened = gaussian_convolve_uniform_grid(energies, analytic, 0.12)
    mask = np.abs(energies) <= 1.5
    numerator = _integrate(np.abs(finite[mask] - broadened[mask]), energies[mask])
    denominator = _integrate(broadened[mask], energies[mask])
    assert numerator / denominator < 0.012


def test_opposite_sign_probability_is_bounded_and_not_relabelled() -> None:
    assert gaussian_opposite_sign_probability(0.0, 1.0) == 0.5
    assert gaussian_opposite_sign_probability(5.0, 1.0) < 3.0e-7
    assert gaussian_opposite_sign_probability(1.0, 0.0) == 0.0