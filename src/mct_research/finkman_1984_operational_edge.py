"""Source-bound Finkman-Schacham 1984 absorption-tail operators.

The source labels the energy at ``alpha=500 cm^-1`` as ``Eg`` because it
approximately tracks the half-peak response of a 10 um photoconductive detector.
This module preserves that quantity as an operational absorption edge. It does
not identify an intrinsic material band gap.
"""
from __future__ import annotations

import math

SOURCE_DOI = "10.1063/1.333828"
SOURCE_CONTENT_FINGERPRINT_SHA256 = (
    "1f983b17b6f69da2cb9c9ac341d43c5a938dd2cc81f7dea0c5cc43c7d1af18b8"
)
COMPOSITION_RANGE = (0.205, 0.29)
TEMPERATURE_RANGE_K = (80.0, 300.0)
ABSORPTION_RANGE_CM1 = (20.0, 1000.0)
OPERATIONAL_EDGE_THRESHOLD_CM1 = 500.0
ZERO_INTERCEPT_REFERENCE_THICKNESS_UM = 500.0
ZERO_INTERCEPT_REFERENCE_TEMPERATURE_K = 300.0
EV_TO_WAVENUMBER_CM1 = 8065.544005

T0_K = 81.9
SIGMA0_K_PER_EV = 3.267e4
LN_ALPHA0_OFFSET = -18.88
LN_ALPHA0_X_COEFFICIENT = 53.61
E0_CONSTANT_EV = -0.3424
E0_X_COEFFICIENT_EV = 1.838
E0_X4_COEFFICIENT_EV = 0.148
_BOUNDARY_TOLERANCE_CM1 = 1.0e-9


def _finite(value: float, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _validate_composition(composition_x: float) -> float:
    x = _finite(composition_x, name="composition_x")
    if not COMPOSITION_RANGE[0] <= x <= COMPOSITION_RANGE[1]:
        raise ValueError(
            "Finkman 1984 operator requires composition_x in "
            f"[{COMPOSITION_RANGE[0]}, {COMPOSITION_RANGE[1]}]"
        )
    return x


def _validate_temperature(temperature_k: float) -> float:
    temperature = _finite(temperature_k, name="temperature_k")
    if not TEMPERATURE_RANGE_K[0] <= temperature <= TEMPERATURE_RANGE_K[1]:
        raise ValueError(
            "Finkman 1984 operator requires temperature_k in "
            f"[{TEMPERATURE_RANGE_K[0]}, {TEMPERATURE_RANGE_K[1]}]"
        )
    return temperature


def _validate_absorption(absorption_cm1: float) -> float:
    absorption = _finite(absorption_cm1, name="absorption_cm1")
    lower, upper = ABSORPTION_RANGE_CM1
    if (
        absorption < lower - _BOUNDARY_TOLERANCE_CM1
        or absorption > upper + _BOUNDARY_TOLERANCE_CM1
    ):
        raise ValueError(
            "Finkman 1984 operator requires absorption_cm1 in "
            f"[{lower}, {upper}]"
        )
    return min(max(absorption, lower), upper)


def source_edge_origin_ev(composition_x: float) -> float:
    """Return the composition polynomial used in source Eq. (10)."""

    x = _validate_composition(composition_x)
    return E0_CONSTANT_EV + E0_X_COEFFICIENT_EV * x + E0_X4_COEFFICIENT_EV * x**4


def energy_at_absorption_cm1(
    absorption_cm1: float,
    temperature_k: float,
    composition_x: float,
) -> float:
    """Return source Eq. (10), the energy of a fixed absorption crossing."""

    absorption = _validate_absorption(absorption_cm1)
    temperature = _validate_temperature(temperature_k)
    x = _validate_composition(composition_x)
    tail_term = (temperature + T0_K) / (SIGMA0_K_PER_EV * (1.0 + x))
    logarithmic_coordinate = (
        math.log(absorption) - LN_ALPHA0_OFFSET - LN_ALPHA0_X_COEFFICIENT * x
    )
    return source_edge_origin_ev(x) + tail_term * logarithmic_coordinate


def absorption_cm1_at_energy(
    energy_ev: float,
    temperature_k: float,
    composition_x: float,
) -> float:
    """Invert source Eq. (10), failing outside the declared absorption range."""

    energy = _finite(energy_ev, name="energy_ev")
    temperature = _validate_temperature(temperature_k)
    x = _validate_composition(composition_x)
    exponent = (
        SIGMA0_K_PER_EV
        * (1.0 + x)
        / (temperature + T0_K)
        * (energy - source_edge_origin_ev(x))
        + LN_ALPHA0_OFFSET
        + LN_ALPHA0_X_COEFFICIENT * x
    )
    absorption = math.exp(exponent)
    return _validate_absorption(absorption)


def operational_edge_500_cm1(temperature_k: float, composition_x: float) -> float:
    """Return Eq. (10) at the source's detector-related 500 cm^-1 threshold."""

    return energy_at_absorption_cm1(
        OPERATIONAL_EDGE_THRESHOLD_CM1,
        temperature_k,
        composition_x,
    )


def published_eq11_operational_edge_ev(
    temperature_k: float,
    composition_x: float,
) -> float:
    """Return the separately rounded closed form printed as source Eq. (11).

    The rounded coefficients make this form differ from Eq. (10) evaluated at
    500 cm^-1 by up to approximately 0.257 meV in the declared source domain.
    """

    temperature = _validate_temperature(temperature_k)
    x = _validate_composition(composition_x)
    thermal = (7.68e-4 * temperature + 6.29e-2) * (1.0 - 2.14 * x) / (1.0 + x)
    return source_edge_origin_ev(x) + thermal


def zero_intercept_absorption_cm1(thickness_um: float) -> float:
    """Return source Eq. (12), ``alpha=e/d``, with thickness converted to cm."""

    thickness = _finite(thickness_um, name="thickness_um")
    if thickness <= 0.0:
        raise ValueError("thickness_um must be positive")
    thickness_cm = thickness * 1.0e-4
    return math.e / thickness_cm


def zero_intercept_energy_ev(
    thickness_um: float,
    temperature_k: float,
    composition_x: float,
) -> float:
    """Return the zero-intercept edge when ``e/d`` lies in the source domain."""

    return energy_at_absorption_cm1(
        zero_intercept_absorption_cm1(thickness_um),
        temperature_k,
        composition_x,
    )


def energy_ev_to_wavenumber_cm1(energy_ev: float) -> float:
    """Convert photon energy to spectroscopic wavenumber."""

    energy = _finite(energy_ev, name="energy_ev")
    if energy <= 0.0:
        raise ValueError("energy_ev must be positive")
    return energy * EV_TO_WAVENUMBER_CM1


def composition_from_zero_intercept_wavenumber_300k_500um(
    zero_intercept_wavenumber_cm1: float,
) -> float:
    """Return source Eq. (13) for a 300 K, 0.5 mm zero-intercept wavenumber."""

    zi = _finite(
        zero_intercept_wavenumber_cm1,
        name="zero_intercept_wavenumber_cm1",
    )
    if zi <= 0.0:
        raise ValueError("zero_intercept_wavenumber_cm1 must be positive")
    composition = 7.785e-2 + 1.096e-4 * zi - 3.713e-9 * zi**2
    if not 0.2 <= composition <= 0.3:
        raise ValueError(
            "Finkman 1984 zero-intercept composition calibration is restricted to "
            "0.2 <= x <= 0.3 at 300 K and 500 um thickness"
        )
    return float(composition)
