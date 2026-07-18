"""Analytical HgCdTe band-gap baselines and provisional candidates.

The functions in this module return the signed zone-centre gap in electron volts,
with ``x`` denoting Cd mole fraction in Hg(1-x)Cd(x)Te and ``temperature_k`` in
kelvin.

The Laurenti expression is a high-confidence reconstruction of the equation
reproduced by Teppe et al. (2016). Its original data, fitting procedure, validity
range, and coefficient uncertainties have not yet been reconstructed from the
1990 primary paper.

The Hansen-Pade function is explicitly provisional. Its two thermal coefficients
were selected by specimen-level cross-validation of the Seiler 1990 temperature
series and have not yet received broad historical or independent-source
validation. Structurally it is a zero-anchored constrained member of the Seiler
rational family, not a new functional family.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray

GapValue = float | NDArray[np.float64]

# Provisional all-specimen shape fit from PR #110.  These values are effective
# empirical coefficients, not identified microscopic phonon parameters.
HANSEN_PADE_ALPHA_EV_PER_K = 5.918273117836612e-4
HANSEN_PADE_TAU_K = 18.059294367159467


def _validated_inputs(
    x: ArrayLike,
    temperature_k: ArrayLike,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    composition = np.asarray(x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    composition, temperature = np.broadcast_arrays(composition, temperature)

    if not np.all(np.isfinite(composition)) or not np.all(np.isfinite(temperature)):
        raise ValueError("composition and temperature must be finite")
    if np.any((composition < 0.0) | (composition > 1.0)):
        raise ValueError("Cd mole fraction x must lie in [0, 1]")
    if np.any(temperature < 0.0):
        raise ValueError("temperature must be non-negative")
    return composition, temperature


def _scalar_or_array(value: NDArray[np.float64]) -> GapValue:
    return float(value) if value.ndim == 0 else value


def _hansen_zero_temperature_gap(composition: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.asarray(
        -0.302
        + 1.930 * composition
        - 0.810 * composition**2
        + 0.832 * composition**3,
        dtype=float,
    )


def hansen_gap_ev(x: ArrayLike, temperature_k: ArrayLike) -> GapValue:
    """Return the Hansen-Schmit-Casselman signed gap in eV."""

    composition, temperature = _validated_inputs(x, temperature_k)
    gap = _hansen_zero_temperature_gap(composition) + 5.35e-4 * temperature * (
        1.0 - 2.0 * composition
    )
    return _scalar_or_array(gap)


def provisional_hansen_pade_gap_ev(
    x: ArrayLike,
    temperature_k: ArrayLike,
    *,
    alpha_ev_per_k: float = HANSEN_PADE_ALPHA_EV_PER_K,
    tau_k: float = HANSEN_PADE_TAU_K,
) -> GapValue:
    """Return the provisional zero-anchored Hansen-Pade signed gap in eV.

    The analytical form is

    ``Eg = Eg_Hansen(x,0) + alpha*(1-2*x)*T^3/(T^2+tau^2)``.

    The default fit gives ``alpha=5.918273117836612e-4 eV/K`` and
    ``tau=18.059294367159467 K``.  It was selected from three Seiler 1990
    temperature-series specimens using specimen-level holdouts.  Only one of
    those series has an independently reported composition, so this function is
    a leading research candidate rather than a production reference equation.

    At low temperature the thermal increment is cubic and has zero initial
    slope. At high temperature its slope approaches
    ``alpha*(1-2*x)``. ``alpha`` and ``tau`` are effective fit coefficients.
    """

    composition, temperature = _validated_inputs(x, temperature_k)
    alpha = float(alpha_ev_per_k)
    tau = float(tau_k)
    if not np.isfinite(alpha) or alpha <= 0.0:
        raise ValueError("alpha_ev_per_k must be finite and positive")
    if not np.isfinite(tau) or tau <= 0.0:
        raise ValueError("tau_k must be finite and positive")

    thermal = alpha * (1.0 - 2.0 * composition) * temperature**3 / (
        temperature**2 + tau**2
    )
    return _scalar_or_array(_hansen_zero_temperature_gap(composition) + thermal)


def laurenti_gap_ev(x: ArrayLike, temperature_k: ArrayLike) -> GapValue:
    """Return the reconstructed Laurenti signed gap in eV.

    The analytical form is

    ``Eg = -0.303(1-x) + 1.606x - 0.132x(1-x)
           + 1e-4 A(x) T^2 / (T + B(x))``

    with ``A(x)=6.3(1-x)-3.25x-5.92x(1-x)`` and
    ``B(x)=11(1-x)+78.7x``.
    """

    composition, temperature = _validated_inputs(x, temperature_k)
    one_minus_x = 1.0 - composition
    amplitude = (
        6.3 * one_minus_x
        - 3.25 * composition
        - 5.92 * composition * one_minus_x
    )
    characteristic_temperature = 11.0 * one_minus_x + 78.7 * composition
    gap_zero_temperature = (
        -0.303 * one_minus_x
        + 1.606 * composition
        - 0.132 * composition * one_minus_x
    )
    gap = (
        gap_zero_temperature
        + 1.0e-4
        * amplitude
        * temperature**2
        / (temperature + characteristic_temperature)
    )
    return _scalar_or_array(gap)


def bracketed_root(
    function: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    absolute_tolerance: float = 1.0e-10,
    max_iterations: int = 256,
) -> float:
    """Find one root of a continuous scalar function by bisection."""

    if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
        raise ValueError("root bounds must be finite and strictly ordered")
    if absolute_tolerance <= 0.0:
        raise ValueError("absolute_tolerance must be positive")

    left = float(lower)
    right = float(upper)
    f_left = float(function(left))
    f_right = float(function(right))
    if not np.isfinite(f_left) or not np.isfinite(f_right):
        raise ValueError("function must be finite at both root bounds")
    if f_left == 0.0:
        return left
    if f_right == 0.0:
        return right
    if np.signbit(f_left) == np.signbit(f_right):
        raise ValueError("root is not bracketed")

    for _ in range(max_iterations):
        midpoint = 0.5 * (left + right)
        f_midpoint = float(function(midpoint))
        if not np.isfinite(f_midpoint):
            raise ValueError("function became non-finite during root search")
        if f_midpoint == 0.0 or 0.5 * (right - left) <= absolute_tolerance:
            return midpoint
        if np.signbit(f_midpoint) == np.signbit(f_left):
            left = midpoint
            f_left = f_midpoint
        else:
            right = midpoint

    raise RuntimeError("root search did not converge")


def critical_temperature_k(
    model: Callable[[float, float], GapValue],
    x: float,
    *,
    temperature_bounds_k: tuple[float, float] = (0.0, 500.0),
) -> float:
    """Solve ``model(x, T)=0`` inside the declared temperature interval."""

    _validated_inputs(x, temperature_bounds_k[0])
    _validated_inputs(x, temperature_bounds_k[1])
    return bracketed_root(
        lambda temperature: float(model(x, temperature)),
        *temperature_bounds_k,
    )


def critical_composition(
    model: Callable[[float, float], GapValue],
    temperature_k: float,
    *,
    composition_bounds: tuple[float, float] = (0.0, 1.0),
) -> float:
    """Solve ``model(x, T)=0`` inside the declared composition interval."""

    _validated_inputs(composition_bounds[0], temperature_k)
    _validated_inputs(composition_bounds[1], temperature_k)
    return bracketed_root(
        lambda composition: float(model(composition, temperature_k)),
        *composition_bounds,
    )
