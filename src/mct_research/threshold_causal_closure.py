"""Conditional R07 threshold kernels and certificates; no material inputs.

The root certificate requires a common support-free real interval and an
independently certified composition slope. Causality alone inside a continuum
does not establish it. The density bound is gap-side, not a PV/retarded bound
on the interior of a cut.
"""

import math

import numpy as np


def quadratic_threshold_kernel(z: complex, threshold: float, cutoff: float,
                               coefficient: float, orientation: int = 1) -> complex:
    """Cauchy transform of c sqrt(epsilon), t=threshold+orientation*epsilon.

    coefficient has units sqrt(energy); cutoff and threshold have energy units.
    This is a finite positive measure and is causal for Im(z)>0. The finite
    gap-side threshold limit is allowed; real interior-cut values require an
    explicit boundary prescription and are rejected by this helper.
    """
    if (orientation not in (-1, 1) or not np.isfinite(threshold)
            or not np.isfinite(cutoff) or cutoff <= 0
            or not np.isfinite(coefficient) or coefficient < 0
            or not np.isfinite(complex(z))):
        raise ValueError("Finite energy, positive cutoff and nonnegative weight required")
    w = complex(z) - threshold
    a = -orientation * w
    if a.imag == 0 and -cutoff <= a.real < 0:
        raise ValueError("A real cut value needs an explicit retarded prescription")
    if a == 0:
        integral = 2 * math.sqrt(cutoff)
    else:
        root = np.sqrt(a)
        integral = 2 * (math.sqrt(cutoff)
                        - root * np.arctan(math.sqrt(cutoff) / root))
    return complex(-orientation * coefficient * integral)


def positive_quadratic_envelope_kernel(z: complex, threshold: float,
                                      cutoff: float, coefficient: float,
                                      density_error: float,
                                      orientation: int = 1) -> complex:
    """Positive lower envelope c sqrt(epsilon)-B epsilon**(3/2).

    Use only with an independent |rho-c sqrt(epsilon)|<=B epsilon**(3/2)
    certificate. B*cutoff<=c makes this retained measure nonnegative. Its
    complement is then positive and bounded by 2B epsilon**(3/2).
    """
    if (not np.isfinite(density_error) or density_error < 0
            or density_error * cutoff > coefficient):
        raise ValueError("The retained density must be a nonnegative lower envelope")
    # Validate all other arguments with the positive half-power kernel.
    half = -orientation * quadratic_threshold_kernel(
        z, threshold, cutoff, 1.0, orientation)
    a = -orientation * (complex(z) - threshold)
    three_halves = 2 * cutoff**1.5 / 3 - a * half
    if not np.isfinite(coefficient) or coefficient < 0:
        raise ValueError("Finite nonnegative weight required")
    return complex(-orientation * (coefficient * half - density_error * three_halves))


def subleading_density_remainder_bound(detuning: float, coefficient: float,
                                      exponent: float, cutoff: float) -> float:
    """Gap-side value remainder after constant/linear subtraction at an edge.

    Assumes |r(epsilon)|<=coefficient*epsilon**exponent, exponent>1. Bounds
    detuning**2*integral |r|/[epsilon**2*(epsilon+detuning)]. The same formula
    divided by sin(theta/2) holds in the slit sector |arg(a)|<=pi-theta.
    This function does not infer or certify a density envelope.
    """
    if (not all(np.isfinite(v) for v in (detuning, coefficient, exponent, cutoff))
            or detuning < 0 or coefficient < 0 or exponent <= 1 or cutoff <= 0):
        raise ValueError("Nonnegative detuning/weight, exponent>1 and cutoff>0 required")
    if detuning == 0 or coefficient == 0:
        return 0.0
    if exponent < 2:
        return coefficient * math.pi * detuning**exponent / math.sin(math.pi*(exponent-1))
    if exponent == 2:
        return coefficient * detuning**2 * math.log1p(cutoff/detuning)
    return coefficient * detuning**2 * cutoff**(exponent-2) / (exponent-2)


def causal_mass_root_error_bound(eps6: float, eps8: float,
                                 mass_composition_slope_min: float) -> float:
    """Conditional |delta x_c| <= max(eps6,eps8)/m, without raw T' inputs.

    eps are uniform branch-denominator errors in energy. The true and candidate
    common roots must be connected by a support-free real energy segment at
    every relevant x; finite threshold endpoint limits are allowed. The true
    reduced mass must have lower composition secant slope m>0 between roots.
    Bracket/existence and these physical hypotheses are caller obligations.
    """
    if (not all(np.isfinite(v) for v in (eps6, eps8, mass_composition_slope_min))
            or eps6 < 0 or eps8 < 0 or mass_composition_slope_min <= 0):
        raise ValueError("Finite nonnegative errors and a positive slope required")
    return max(eps6, eps8) / mass_composition_slope_min
