from __future__ import annotations

import numpy as np

from mct_research.random_mass_dos import (
    average_random_mass_dos,
    effect_size,
    gaussian_broadened_dos,
    gaussian_convolve_uniform_grid,
)


def _integrate(values: np.ndarray, coordinates: np.ndarray) -> float:
    implementation = getattr(np, "trapezoid", None)
    if implementation is None:
        implementation = np.trapz
    return float(implementation(values, coordinates))


def test_dos_kernel_and_convolution_preserve_spectral_weight() -> None:
    energies = np.linspace(-6.0, 6.0, 2401)
    levels = np.array([-1.0, 1.0])
    dos = gaussian_broadened_dos(
        energies, levels, length=2.0, broadening=0.1
    )
    assert abs(_integrate(dos, energies) - 1.0) < 1.0e-10
    convolved = gaussian_convolve_uniform_grid(energies, dos, 0.2)
    assert abs(_integrate(convolved, energies) - 1.0) < 1.0e-10
    result = effect_size(
        energies, convolved, convolved, energy_window=(-2.0, 2.0)
    )
    assert result.delta_1 == 0.0
    assert result.delta_infinity == 0.0


def test_small_random_mass_ensemble_is_deterministic() -> None:
    energies = np.linspace(-2.0, 2.0, 101)
    first = average_random_mass_dos(
        energies,
        0.0,
        0.3,
        1.0,
        16.0,
        64,
        0.1,
        4,
        seed=716,
        boundary="antiperiodic",
    )
    second = average_random_mass_dos(
        energies,
        0.0,
        0.3,
        1.0,
        16.0,
        64,
        0.1,
        4,
        seed=716,
        boundary="antiperiodic",
    )
    assert np.array_equal(first.realization_dos, second.realization_dos)
    assert np.array_equal(first.mean_dos, second.mean_dos)
    assert np.all(first.mean_dos >= 0.0)