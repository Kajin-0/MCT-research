#!/usr/bin/env python3
"""Synthetic two-radius finite-k extraction and held-out [110] closure check.

The calculation uses normalized curvature units C = hbar^2/(2m0) = 1. It is
an analytical/numerical protocol check, not a physical HgCdTe result.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable

C = 1.0
H = 0.02
TRUE = {
    "Eg": 0.12,
    "Delta": 0.95,
    "P8": 8.4,
    "P7": 7.9,
    "F": -0.35,
    "gamma1": 4.3,
    "gamma2": 1.2,
    "gamma3": 1.55,
}
CONTAMINATION = {
    "P8_cubic": 12.0,
    "P7_cubic": -9.0,
    "c6_quartic": 40.0,
    "hh001_quartic": -15.0,
    "lh001_quartic": 12.0,
    "hh111_quartic": 10.0,
    "lh111_quartic": -8.0,
    "hh110_quartic": 7.0,
    "lh110_quartic": -6.0,
}


def odd_value(linear: float, cubic: float, k: float) -> float:
    return linear * k + cubic * k**3


def even_value(quadratic: float, quartic: float, k: float) -> float:
    return quadratic * k**2 + quartic * k**4


def odd_derivative(function: Callable[[float], float], h: float) -> float:
    return (function(h) - function(-h)) / (2.0 * h)


def even_coefficient(function: Callable[[float], float], h: float) -> float:
    return (function(h) + function(-h) - 2.0 * function(0.0)) / (2.0 * h**2)


def richardson(coarse: float, fine: float) -> float:
    """Remove the leading O(h^2) contamination."""
    return (4.0 * fine - coarse) / 3.0


def two_radius_odd(linear: float, cubic: float) -> tuple[float, float]:
    function = lambda k: odd_value(linear, cubic, k)
    coarse = odd_derivative(function, H)
    fine = odd_derivative(function, H / 2.0)
    return coarse, richardson(coarse, fine)


def two_radius_even(quadratic: float, quartic: float) -> tuple[float, float]:
    function = lambda k: even_value(quadratic, quartic, k)
    coarse = even_coefficient(function, H)
    fine = even_coefficient(function, H / 2.0)
    return coarse, richardson(coarse, fine)


def max_parameter_error(parameters: dict[str, float]) -> float:
    return max(abs(parameters[name] - TRUE[name]) for name in TRUE)


def analyze() -> dict[str, object]:
    c6 = C * (1.0 + 2.0 * TRUE["F"])
    hh001 = -C * (TRUE["gamma1"] - 2.0 * TRUE["gamma2"])
    lh001 = -C * (TRUE["gamma1"] + 2.0 * TRUE["gamma2"])
    hh111 = -C * (TRUE["gamma1"] - 2.0 * TRUE["gamma3"])
    lh111 = -C * (TRUE["gamma1"] + 2.0 * TRUE["gamma3"])

    p8_coarse, p8 = two_radius_odd(TRUE["P8"], CONTAMINATION["P8_cubic"])
    p7_coarse, p7 = two_radius_odd(TRUE["P7"], CONTAMINATION["P7_cubic"])
    c6_coarse, c6_fit = two_radius_even(c6, CONTAMINATION["c6_quartic"])
    hh001_coarse, hh001_fit = two_radius_even(hh001, CONTAMINATION["hh001_quartic"])
    lh001_coarse, lh001_fit = two_radius_even(lh001, CONTAMINATION["lh001_quartic"])
    hh111_coarse, hh111_fit = two_radius_even(hh111, CONTAMINATION["hh111_quartic"])
    lh111_coarse, lh111_fit = two_radius_even(lh111, CONTAMINATION["lh111_quartic"])

    coarse = {
        "Eg": TRUE["Eg"],
        "Delta": TRUE["Delta"],
        "P8": p8_coarse,
        "P7": p7_coarse,
        "F": 0.5 * (c6_coarse / C - 1.0),
        "gamma1": -0.25 * (hh001_coarse + lh001_coarse + hh111_coarse + lh111_coarse) / C,
        "gamma2": (hh001_coarse - lh001_coarse) / (4.0 * C),
        "gamma3": (hh111_coarse - lh111_coarse) / (4.0 * C),
    }

    gamma1_001 = -(hh001_fit + lh001_fit) / (2.0 * C)
    gamma1_111 = -(hh111_fit + lh111_fit) / (2.0 * C)
    fitted = {
        "Eg": TRUE["Eg"],
        "Delta": TRUE["Delta"],
        "P8": p8,
        "P7": p7,
        "F": 0.5 * (c6_fit / C - 1.0),
        "gamma1": 0.5 * (gamma1_001 + gamma1_111),
        "gamma2": (hh001_fit - lh001_fit) / (4.0 * C),
        "gamma3": (hh111_fit - lh111_fit) / (4.0 * C),
    }

    split110 = math.sqrt(fitted["gamma2"] ** 2 + 3.0 * fitted["gamma3"] ** 2)
    predicted110 = {
        "hh": -C * (fitted["gamma1"] - split110),
        "lh": -C * (fitted["gamma1"] + split110),
    }
    true_split110 = math.sqrt(TRUE["gamma2"] ** 2 + 3.0 * TRUE["gamma3"] ** 2)
    true110 = {
        "hh": -C * (TRUE["gamma1"] - true_split110),
        "lh": -C * (TRUE["gamma1"] + true_split110),
    }
    _, observed_hh110 = two_radius_even(true110["hh"], CONTAMINATION["hh110_quartic"])
    _, observed_lh110 = two_radius_even(true110["lh"], CONTAMINATION["lh110_quartic"])
    observed110 = {"hh": observed_hh110, "lh": observed_lh110}

    coarse_error = max_parameter_error(coarse)
    fitted_error = max_parameter_error(fitted)
    holdout_error = max(abs(predicted110[key] - observed110[key]) for key in predicted110)
    gamma1_direction_mismatch = abs(gamma1_001 - gamma1_111)

    if fitted_error > 1.0e-11 or holdout_error > 1.0e-11:
        raise RuntimeError("two-radius Kane extraction or held-out closure failed")
    if coarse_error <= 1.0e-4:
        raise RuntimeError("synthetic contamination is too weak to test Richardson cancellation")

    return {
        "status": "analytical_protocol_only_not_physical_HgCdTe_data",
        "normalized_curvature_constant_C": C,
        "radii": [H, H / 2.0],
        "training_directions": ["[001]", "[111]"],
        "holdout_direction": "[110]",
        "true_parameters": TRUE,
        "single_radius_parameters": coarse,
        "two_radius_parameters": fitted,
        "single_radius_maximum_parameter_error": coarse_error,
        "two_radius_maximum_parameter_error": fitted_error,
        "gamma1_direction_mismatch": gamma1_direction_mismatch,
        "heldout_110_predicted_curvatures": predicted110,
        "heldout_110_observed_curvatures": observed110,
        "heldout_110_maximum_error": holdout_error,
        "production_rule": (
            "Use paired plus/minus k at h and h/2; extract odd and even parts, "
            "remove leading O(h^2) contamination, train on [001] and [111], "
            "and reject the parameter set if the unused [110] matrix/curvature "
            "residual exceeds the declared numerical and projection uncertainty."
        ),
    }


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
