"""Differential diagnostics for Gaussian-distributed absorption edges.

This module analyzes the controlled distributional observation operator

``alpha_p(E) = A E[(E-G)_+**p]``

for ``G ~ Normal(mean_gap, gap_sigma**2)`` and ``p >= 0``.  It evaluates the
local logarithmic slope, local apparent tail energy, and logarithmic curvature
without numerically differentiating a sampled spectrum.

The result is an observation-model diagnostic.  It does not identify a measured
HgCdTe Urbach energy with composition variance, a quasiparticle linewidth, a PL
width, or a spatial correlation length.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, gamma, isfinite, pi, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spectral_convolution import gaussian_gap_convolved_power_absorption

FloatArray = NDArray[np.float64]


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _read_only(value: ArrayLike, shape: tuple[int, ...]) -> FloatArray:
    result = np.array(value, dtype=float, copy=True).reshape(shape)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class GaussianPowerTailDiagnostics:
    """Exact differential diagnostics within the truncated Gaussian benchmark."""

    photon_energy_ev: FloatArray
    standardized_energy: FloatArray
    absorption_cm_inverse: FloatArray
    log_slope_ev_inverse: FloatArray
    local_tail_energy_ev: FloatArray
    log_curvature_ev_inverse_squared: FloatArray
    dimensionless_log_slope: FloatArray
    dimensionless_local_tail_energy: FloatArray
    dimensionless_log_curvature: FloatArray
    mean_gap_ev: float
    gap_sigma_ev: float
    exponent: float
    amplitude_cm_inverse_ev_power: float
    quadrature_order: int
    standard_deviation_limit: float


@dataclass(frozen=True)
class GaussianPowerTailAsymptotic:
    """Leading deep-subgap asymptotic in standardized energy coordinates."""

    standardized_energy: FloatArray
    dimensionless_absorption_shape: FloatArray
    dimensionless_log_slope: FloatArray
    dimensionless_local_tail_energy: FloatArray
    dimensionless_log_curvature: FloatArray
    exponent: float


def gaussian_power_tail_diagnostics(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    *,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> GaussianPowerTailDiagnostics:
    """Return local slope, apparent tail energy, and log curvature.

    Write

    ``z = (E-mean_gap)/gap_sigma``

    and

    ``F_p(z) = integral_0^infinity t**p phi(z-t) dt``.

    The absorption is ``A gap_sigma**p F_p``.  The derivative identities are

    ``F_p' = F_(p+1) - z F_p``

    and

    ``F_p'' = F_(p+2) - 2 z F_(p+1) + (z**2-1) F_p``.

    The implementation uses the same finite Gaussian support and normalization
    as :func:`gaussian_gap_convolved_power_absorption`.  Exponentially small
    boundary corrections are included explicitly, so the derivatives remain
    consistent with that truncated numerical operator rather than silently
    mixing truncated spectra with infinite-domain derivatives.

    The function is intentionally restricted to the subgap region ``E <=
    mean_gap`` and to energies resolved inside the declared Gaussian support.
    """

    energy = np.asarray(photon_energy_ev, dtype=float)
    if energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("photon_energy_ev must contain finite values")
    shape = energy.shape
    energy_flat = np.array(energy.reshape(-1), dtype=float, copy=True)

    mean_gap = _finite_scalar("mean_gap_ev", mean_gap_ev)
    sigma_gap = _finite_scalar("gap_sigma_ev", gap_sigma_ev)
    power = _finite_scalar("exponent", exponent)
    amplitude = _finite_scalar(
        "amplitude_cm_inverse_ev_power", amplitude_cm_inverse_ev_power
    )
    z_limit = _finite_scalar("standard_deviation_limit", standard_deviation_limit)
    order = int(quadrature_order)

    if sigma_gap <= 0.0:
        raise ValueError("gap_sigma_ev must be positive")
    if power < 0.0:
        raise ValueError("exponent must be non-negative")
    if amplitude <= 0.0:
        raise ValueError("amplitude_cm_inverse_ev_power must be positive")
    if order < 32:
        raise ValueError("quadrature_order must be at least 32")
    if z_limit <= 0.0:
        raise ValueError("standard_deviation_limit must be positive")

    energy_tolerance = 64.0 * np.finfo(float).eps * max(
        1.0, abs(mean_gap), sigma_gap
    )
    if np.any(energy_flat > mean_gap + energy_tolerance):
        raise ValueError("tail diagnostics require photon_energy_ev <= mean_gap_ev")

    standardized = (energy_flat - mean_gap) / sigma_gap
    if np.any(standardized <= -z_limit):
        raise ValueError(
            "standardized energies must lie above -standard_deviation_limit"
        )

    common = dict(
        mean_gap_ev=0.0,
        gap_sigma_ev=1.0,
        amplitude_cm_inverse_ev_power=1.0,
        quadrature_order=order,
        standard_deviation_limit=z_limit,
    )
    moment_p = gaussian_gap_convolved_power_absorption(
        standardized,
        exponent=power,
        **common,
    ).reshape(-1)
    moment_p1 = gaussian_gap_convolved_power_absorption(
        standardized,
        exponent=power + 1.0,
        **common,
    ).reshape(-1)
    moment_p2 = gaussian_gap_convolved_power_absorption(
        standardized,
        exponent=power + 2.0,
        **common,
    ).reshape(-1)

    normal_probability = erf(z_limit / sqrt(2.0))
    boundary_density = exp(-0.5 * z_limit**2) / sqrt(2.0 * pi)
    boundary_base = standardized + z_limit
    boundary_p = (
        boundary_base**power * boundary_density / normal_probability
    )
    if power == 0.0:
        boundary_p_derivative = np.zeros_like(boundary_base)
    else:
        boundary_p_derivative = (
            power
            * boundary_base ** (power - 1.0)
            * boundary_density
            / normal_probability
        )

    first_derivative = moment_p1 - standardized * moment_p + boundary_p
    second_derivative = (
        moment_p2
        - 2.0 * standardized * moment_p1
        + (standardized**2 - 1.0) * moment_p
        + z_limit * boundary_p
        + boundary_p_derivative
    )

    if (
        not np.all(np.isfinite(moment_p))
        or np.any(moment_p <= 0.0)
        or not np.all(np.isfinite(first_derivative))
        or np.any(first_derivative <= 0.0)
        or not np.all(np.isfinite(second_derivative))
    ):
        raise ValueError("declared tail region is not numerically resolved")

    dimensionless_log_slope = first_derivative / moment_p
    dimensionless_log_curvature = (
        second_derivative / moment_p - dimensionless_log_slope**2
    )
    dimensionless_local_tail_energy = 1.0 / dimensionless_log_slope

    absorption = amplitude * sigma_gap**power * moment_p
    log_slope = dimensionless_log_slope / sigma_gap
    local_tail_energy = sigma_gap * dimensionless_local_tail_energy
    log_curvature = dimensionless_log_curvature / sigma_gap**2

    return GaussianPowerTailDiagnostics(
        photon_energy_ev=_read_only(energy_flat, shape),
        standardized_energy=_read_only(standardized, shape),
        absorption_cm_inverse=_read_only(absorption, shape),
        log_slope_ev_inverse=_read_only(log_slope, shape),
        local_tail_energy_ev=_read_only(local_tail_energy, shape),
        log_curvature_ev_inverse_squared=_read_only(log_curvature, shape),
        dimensionless_log_slope=_read_only(dimensionless_log_slope, shape),
        dimensionless_local_tail_energy=_read_only(
            dimensionless_local_tail_energy, shape
        ),
        dimensionless_log_curvature=_read_only(
            dimensionless_log_curvature, shape
        ),
        mean_gap_ev=mean_gap,
        gap_sigma_ev=sigma_gap,
        exponent=power,
        amplitude_cm_inverse_ev_power=amplitude,
        quadrature_order=order,
        standard_deviation_limit=z_limit,
    )


def gaussian_power_deep_tail_asymptotic(
    standardized_energy: ArrayLike,
    *,
    exponent: float = 0.5,
) -> GaussianPowerTailAsymptotic:
    """Return the leading ``z -> -infinity`` Gaussian-power tail asymptotic.

    The dimensionless absorption shape is

    ``Gamma(p+1) phi(z) (-z)**(-(p+1))``.

    The associated leading differential quantities are

    ``d log(alpha)/dz = -z - (p+1)/z``

    and

    ``d2 log(alpha)/dz2 = -1 + (p+1)/z**2``.

    This is an asymptotic diagnostic, not an equality at finite ``z``.
    """

    values = np.asarray(standardized_energy, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("standardized_energy must contain finite values")
    if np.any(values >= 0.0):
        raise ValueError("deep-tail asymptotic requires standardized_energy < 0")
    shape = values.shape
    z = np.array(values.reshape(-1), dtype=float, copy=True)

    power = _finite_scalar("exponent", exponent)
    if power < 0.0:
        raise ValueError("exponent must be non-negative")

    dimensionless_absorption = (
        gamma(power + 1.0)
        * np.exp(-0.5 * z**2)
        / sqrt(2.0 * pi)
        * (-z) ** (-(power + 1.0))
    )
    dimensionless_log_slope = -z - (power + 1.0) / z
    dimensionless_local_tail_energy = 1.0 / dimensionless_log_slope
    dimensionless_log_curvature = -1.0 + (power + 1.0) / z**2

    return GaussianPowerTailAsymptotic(
        standardized_energy=_read_only(z, shape),
        dimensionless_absorption_shape=_read_only(
            dimensionless_absorption, shape
        ),
        dimensionless_log_slope=_read_only(dimensionless_log_slope, shape),
        dimensionless_local_tail_energy=_read_only(
            dimensionless_local_tail_energy, shape
        ),
        dimensionless_log_curvature=_read_only(
            dimensionless_log_curvature, shape
        ),
        exponent=power,
    )
