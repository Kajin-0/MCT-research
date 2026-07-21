"""Distributional propagation from composition to signed HgCdTe gap observables.

This module implements a deliberately low-cost model layer. It propagates a
declared specimen- or coarse-grained composition standard deviation through any
scalar signed-gap model ``Eg(x, T)``. It does not identify microscopic alloy
disorder, optical Urbach energy, quasiparticle linewidth, or a topological
invariant. Those require additional observation and physical models.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import erfc, sqrt

import numpy as np

from .gap_models import GapValue


@dataclass(frozen=True)
class DistributionalGapApproximation:
    """Second-order local-gap approximation for a Gaussian composition field."""

    mean_composition: float
    composition_sigma: float
    temperature_k: float
    gap_at_mean_ev: float
    mean_gap_ev: float
    composition_curvature_bias_ev: float
    gap_sigma_ev: float
    dgap_dx_ev: float
    d2gap_dx2_ev: float
    dgap_dtemperature_ev_per_k: float
    critical_temperature_sigma_k: float
    opposite_sign_fraction: float


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def gaussian_opposite_sign_fraction(mean_gap_ev: float, gap_sigma_ev: float) -> float:
    """Return the Gaussian probability of a local gap opposite in sign to its mean.

    The result is a local sign statistic. It is not a bulk topological invariant.
    At exactly zero mean the limiting value is ``0.5``. A deterministic nonzero
    gap has zero opposite-sign probability.
    """

    mean_gap = _finite_scalar("mean_gap_ev", mean_gap_ev)
    sigma_gap = _finite_scalar("gap_sigma_ev", gap_sigma_ev)
    if sigma_gap < 0.0:
        raise ValueError("gap_sigma_ev must be non-negative")
    if sigma_gap == 0.0:
        return 0.5 if mean_gap == 0.0 else 0.0
    return 0.5 * erfc(abs(mean_gap) / (sqrt(2.0) * sigma_gap))


def _central_composition_derivatives(
    model: Callable[[float, float], GapValue],
    composition: float,
    temperature_k: float,
    step: float,
) -> tuple[float, float, float]:
    if step <= 0.0:
        raise ValueError("composition_step must be positive")
    if composition - step < 0.0 or composition + step > 1.0:
        raise ValueError("composition_step leaves the physical interval [0, 1]")

    centre = float(model(composition, temperature_k))
    lower = float(model(composition - step, temperature_k))
    upper = float(model(composition + step, temperature_k))
    values = np.asarray([lower, centre, upper], dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("gap model must return finite scalar values")

    first = (upper - lower) / (2.0 * step)
    second = (upper - 2.0 * centre + lower) / step**2
    return centre, first, second


def _central_temperature_derivative(
    model: Callable[[float, float], GapValue],
    composition: float,
    temperature_k: float,
    step_k: float,
) -> float:
    if step_k <= 0.0:
        raise ValueError("temperature_step_k must be positive")

    if temperature_k >= step_k:
        lower_temperature = temperature_k - step_k
        upper_temperature = temperature_k + step_k
        lower = float(model(composition, lower_temperature))
        upper = float(model(composition, upper_temperature))
        derivative = (upper - lower) / (2.0 * step_k)
    else:
        centre = float(model(composition, temperature_k))
        upper = float(model(composition, temperature_k + step_k))
        derivative = (upper - centre) / step_k

    if not np.isfinite(derivative):
        raise ValueError("gap model must return finite scalar values")
    return derivative


def linearized_composition_gap_statistics(
    model: Callable[[float, float], GapValue],
    mean_composition: float,
    composition_sigma: float,
    temperature_k: float,
    *,
    composition_step: float = 1.0e-4,
    temperature_step_k: float = 0.1,
) -> DistributionalGapApproximation:
    """Propagate Gaussian composition variation through ``Eg(x, T)``.

    The approximation retains the second-order curvature shift of the mean,

    ``E[Eg(X,T)] ≈ Eg(x,T) + 0.5 * d2Eg/dx2 * sigma_x**2``,

    and the first-order local-gap width,

    ``sigma_E ≈ abs(dEg/dx) * sigma_x``.

    The critical-temperature width is the local implicit-function result

    ``sigma_Tc ≈ abs((dEg/dx)/(dEg/dT)) * sigma_x``.

    It is reported as infinity when the local temperature derivative vanishes and
    the composition width is nonzero.
    """

    composition = _finite_scalar("mean_composition", mean_composition)
    sigma_x = _finite_scalar("composition_sigma", composition_sigma)
    temperature = _finite_scalar("temperature_k", temperature_k)
    if not 0.0 <= composition <= 1.0:
        raise ValueError("mean_composition must lie in [0, 1]")
    if sigma_x < 0.0:
        raise ValueError("composition_sigma must be non-negative")
    if temperature < 0.0:
        raise ValueError("temperature_k must be non-negative")

    gap_at_mean, dgap_dx, d2gap_dx2 = _central_composition_derivatives(
        model,
        composition,
        temperature,
        float(composition_step),
    )
    dgap_dtemperature = _central_temperature_derivative(
        model,
        composition,
        temperature,
        float(temperature_step_k),
    )

    curvature_bias = 0.5 * d2gap_dx2 * sigma_x**2
    mean_gap = gap_at_mean + curvature_bias
    gap_sigma = abs(dgap_dx) * sigma_x

    if sigma_x == 0.0:
        critical_temperature_sigma = 0.0
    elif dgap_dtemperature == 0.0:
        critical_temperature_sigma = float("inf")
    else:
        critical_temperature_sigma = abs(dgap_dx / dgap_dtemperature) * sigma_x

    return DistributionalGapApproximation(
        mean_composition=composition,
        composition_sigma=sigma_x,
        temperature_k=temperature,
        gap_at_mean_ev=gap_at_mean,
        mean_gap_ev=mean_gap,
        composition_curvature_bias_ev=curvature_bias,
        gap_sigma_ev=gap_sigma,
        dgap_dx_ev=dgap_dx,
        d2gap_dx2_ev=d2gap_dx2,
        dgap_dtemperature_ev_per_k=dgap_dtemperature,
        critical_temperature_sigma_k=critical_temperature_sigma,
        opposite_sign_fraction=gaussian_opposite_sign_fraction(mean_gap, gap_sigma),
    )
