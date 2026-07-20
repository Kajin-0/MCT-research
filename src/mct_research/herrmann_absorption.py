"""Provenance-bounded primitives recoverable from Herrmann et al. (1993).

Herrmann et al. report an exponential Urbach segment, a linear-in-temperature
width law, and an equilibrium limiting form for the band-filling factor.  The
paper does not reproduce a self-contained implementation of the complete Kane
absorption and non-equilibrium filling model.  This module therefore exposes
only the equations that can be implemented without reconstructive assumptions.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

Value = float | NDArray[np.float64]

BOLTZMANN_EV_PER_K = 8.617333262e-5
HERRMANN_1993_SOURCE_DOI = "10.1063/1.352954"
HERRMANN_1992_PRECURSOR_DOI = "10.1016/0022-0248(92)90851-9"


def _broadcast_finite(*values: ArrayLike, names: tuple[str, ...]) -> tuple[NDArray[np.float64], ...]:
    arrays = tuple(np.asarray(value, dtype=float) for value in values)
    arrays = tuple(np.broadcast_arrays(*arrays))
    for array, name in zip(arrays, names, strict=True):
        if not np.all(np.isfinite(array)):
            raise ValueError(f"{name} must be finite")
    return arrays


def _scalar_or_array(value: NDArray[np.float64]) -> Value:
    return float(value) if value.ndim == 0 else value


def herrmann_urbach_width_ev(
    temperature_k: ArrayLike,
    permanent_broadening_ev: ArrayLike,
    thermal_slope_dimensionless: ArrayLike,
) -> Value:
    """Return the explicit Herrmann Urbach width ``W0(T)`` in eV.

    The source equation is

    ``W0(T) = E_permanent + a * k_B * T``.

    Herrmann et al. denote the permanent broadening by ``E_p``.  The descriptive
    name used here prevents confusion with the unrelated Kane energy commonly
    written with the same symbol.
    """

    temperature, permanent, slope = _broadcast_finite(
        temperature_k,
        permanent_broadening_ev,
        thermal_slope_dimensionless,
        names=("temperature_k", "permanent_broadening_ev", "thermal_slope_dimensionless"),
    )
    if np.any(temperature < 0.0):
        raise ValueError("temperature_k must be nonnegative")
    if np.any(permanent <= 0.0):
        raise ValueError("permanent_broadening_ev must be positive")
    if np.any(slope < 0.0):
        raise ValueError("thermal_slope_dimensionless must be nonnegative")

    width = permanent + slope * BOLTZMANN_EV_PER_K * temperature
    if np.any(width <= 0.0):
        raise ValueError("computed Urbach width must be positive")
    return _scalar_or_array(np.asarray(width, dtype=float))


def herrmann_urbach_tail_alpha_cm1(
    photon_energy_ev: ArrayLike,
    transition_energy_ev: ArrayLike,
    transition_absorption_cm1: ArrayLike,
    tail_width_ev: ArrayLike,
) -> Value:
    """Evaluate the explicit below-transition Herrmann Urbach segment.

    The recoverable source equation is

    ``alpha(E) = alpha(E0) * exp((E - E0) / W0)``.

    This function is intentionally fail-closed above ``E0``.  The continuation
    into the Kane region requires the complete source model and matching
    conventions, which are not self-contained in the 1993 paper.
    """

    energy, transition, alpha_transition, width = _broadcast_finite(
        photon_energy_ev,
        transition_energy_ev,
        transition_absorption_cm1,
        tail_width_ev,
        names=(
            "photon_energy_ev",
            "transition_energy_ev",
            "transition_absorption_cm1",
            "tail_width_ev",
        ),
    )
    if np.any(alpha_transition <= 0.0):
        raise ValueError("transition_absorption_cm1 must be positive")
    if np.any(width <= 0.0):
        raise ValueError("tail_width_ev must be positive")

    tolerance = 32.0 * np.finfo(float).eps * np.maximum(1.0, np.abs(transition))
    if np.any(energy > transition + tolerance):
        raise ValueError(
            "Herrmann Urbach primitive is restricted to photon_energy_ev <= transition_energy_ev"
        )

    absorption = alpha_transition * np.exp((energy - transition) / width)
    return _scalar_or_array(np.asarray(absorption, dtype=float))


def herrmann_equilibrium_band_filling_factor(
    photon_energy_ev: ArrayLike,
    quasi_fermi_split_ev: ArrayLike,
    temperature_k: ArrayLike,
) -> Value:
    """Return the equilibrium limiting band-filling factor reported in 1993.

    The explicit limiting expression is

    ``tanh((E - delta_mu) / (4 k_B T))``.

    It is exposed as a standalone primitive only.  It is not a reconstruction of
    the paper's complete pumped-absorption or luminescence calculation.
    """

    energy, split, temperature = _broadcast_finite(
        photon_energy_ev,
        quasi_fermi_split_ev,
        temperature_k,
        names=("photon_energy_ev", "quasi_fermi_split_ev", "temperature_k"),
    )
    if np.any(temperature <= 0.0):
        raise ValueError("temperature_k must be positive for the band-filling factor")
    factor = np.tanh((energy - split) / (4.0 * BOLTZMANN_EV_PER_K * temperature))
    return _scalar_or_array(np.asarray(factor, dtype=float))
