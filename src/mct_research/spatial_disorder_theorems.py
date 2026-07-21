"""Exact theorem extensions and HgCdTe propagation for spatial disorder.

This module complements, rather than replaces, the covariance core, depth-kernel
benchmarks, and multiscale Fisher diagnostics.  It provides:

- the explicit one-scale non-identifiability family;
- the exact two-scale inverse in arbitrary spatial dimension;
- a closed logarithmic condition number for two-scale designs;
- exact one-dimensional top-hat formulas for Gaussian and exponential
  covariance;
- second-order propagation through a declared HgCdTe signed-gap law;
- first-order conversion from gap spread to cutoff-wavelength spread.

All length arguments within a call must use the same units.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

from .spatial_disorder import isotropic_gaussian_effective_variance


@dataclass(frozen=True)
class GaussianTwoScaleRecovery:
    """Exact arbitrary-dimensional recovery from two Gaussian probe scales."""

    point_variance: float
    point_standard_deviation: float
    correlation_length: float
    dimension: int
    probe_sigma_1: float
    probe_sigma_2: float
    effective_variance_1: float
    effective_variance_2: float
    powered_variance_ratio: float
    log_parameter_condition_number: float
    relative_reconstruction_residual: float


@dataclass(frozen=True)
class ProbeAveragedGapMoments:
    """Second-order moments of a gap law under filtered Gaussian composition."""

    gap_at_mean_ev: float
    mean_gap_ev: float
    gap_variance_ev2: float
    gap_standard_deviation_ev: float
    effective_composition_variance: float
    effective_composition_standard_deviation: float
    first_composition_derivative_ev: float
    second_composition_derivative_ev: float


def _finite(name: str, value: float) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _positive(name: str, value: float) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise ValueError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: float) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return result


def _dimension(value: int) -> int:
    if isinstance(value, bool) or int(value) != value or int(value) <= 0:
        raise ValueError("dimension must be a positive integer")
    return int(value)


def single_scale_point_variance_family(
    effective_variance: float,
    correlation_length: float,
    probe_sigma: float,
    *,
    dimension: int = 2,
) -> float:
    r"""Return one exact member of the one-scale non-identifiability family.

    Holding :math:`V_a` and :math:`a` fixed, every positive :math:`\ell`
    corresponds to

    .. math::

       \sigma_x^2(\ell)=V_a\left(1+2a^2/\ell^2\right)^{D/2}.
    """

    observed = _positive("effective_variance", effective_variance)
    xi = _positive("correlation_length", correlation_length)
    scale = _nonnegative("probe_sigma", probe_sigma)
    ndim = _dimension(dimension)
    return observed * (1.0 + 2.0 * (scale / xi) ** 2) ** (0.5 * ndim)


def two_scale_log_parameter_condition_number(
    correlation_length: float,
    probe_sigma_1: float,
    probe_sigma_2: float,
    *,
    dimension: int = 2,
) -> float:
    r"""Return the 2-norm condition number in logarithmic parameters.

    With :math:`y_i=\log V_i` and
    :math:`\theta=(\log\sigma_x^2,\log\ell)`, the Jacobian rows are

    .. math::

       J_i=(1,g_i),\qquad
       g_i=D\frac{2a_i^2/\ell^2}{1+2a_i^2/\ell^2}.
    """

    xi = _positive("correlation_length", correlation_length)
    scale_1 = _nonnegative("probe_sigma_1", probe_sigma_1)
    scale_2 = _nonnegative("probe_sigma_2", probe_sigma_2)
    ndim = _dimension(dimension)

    def sensitivity(scale: float) -> float:
        ratio = 2.0 * (scale / xi) ** 2
        return ndim * ratio / (1.0 + ratio)

    g_1 = sensitivity(scale_1)
    g_2 = sensitivity(scale_2)
    trace = 2.0 + g_1 * g_1 + g_2 * g_2
    determinant = (g_1 - g_2) ** 2
    discriminant = max(trace * trace - 4.0 * determinant, 0.0)
    root = math.sqrt(discriminant)
    eigenvalue_max = 0.5 * (trace + root)
    eigenvalue_min = 0.5 * (trace - root)
    if eigenvalue_min <= 0.0:
        return math.inf
    return math.sqrt(eigenvalue_max / eigenvalue_min)


def recover_isotropic_gaussian_two_scales(
    effective_variance_1: float,
    effective_variance_2: float,
    probe_sigma_1: float,
    probe_sigma_2: float,
    *,
    dimension: int = 2,
) -> GaussianTwoScaleRecovery:
    r"""Recover point variance and correlation length in arbitrary dimension.

    Define

    .. math::

       q=\left(V_1/V_2\right)^{2/D}.

    The exact inverse is

    .. math::

       \ell^2=2\frac{a_2^2-q a_1^2}{q-1},
       \qquad
       \sigma_x^2=V_1\left(1+2a_1^2/\ell^2\right)^{D/2}.
    """

    variance_1 = _positive("effective_variance_1", effective_variance_1)
    variance_2 = _positive("effective_variance_2", effective_variance_2)
    scale_1 = _nonnegative("probe_sigma_1", probe_sigma_1)
    scale_2 = _nonnegative("probe_sigma_2", probe_sigma_2)
    ndim = _dimension(dimension)
    if scale_1 == scale_2:
        raise ValueError("probe scales must be distinct")

    powered_ratio = (variance_1 / variance_2) ** (2.0 / ndim)
    denominator = powered_ratio - 1.0
    tolerance = 128.0 * math.ulp(1.0) * max(1.0, abs(powered_ratio))
    if abs(denominator) <= tolerance:
        raise ValueError("two-scale inversion is degenerate because variances are equal")

    correlation_length_squared = 2.0 * (
        scale_2 * scale_2 - powered_ratio * scale_1 * scale_1
    ) / denominator
    if (
        not math.isfinite(correlation_length_squared)
        or correlation_length_squared <= 0.0
    ):
        raise ValueError("variance pair is inconsistent with a positive correlation length")

    correlation_length = math.sqrt(correlation_length_squared)
    point_variance = single_scale_point_variance_family(
        variance_1,
        correlation_length,
        scale_1,
        dimension=ndim,
    )
    reconstructed_1 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_1,
        dimension=ndim,
    )
    reconstructed_2 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_2,
        dimension=ndim,
    )
    residual = max(
        abs(reconstructed_1 - variance_1) / variance_1,
        abs(reconstructed_2 - variance_2) / variance_2,
    )
    return GaussianTwoScaleRecovery(
        point_variance=point_variance,
        point_standard_deviation=math.sqrt(point_variance),
        correlation_length=correlation_length,
        dimension=ndim,
        probe_sigma_1=scale_1,
        probe_sigma_2=scale_2,
        effective_variance_1=variance_1,
        effective_variance_2=variance_2,
        powered_variance_ratio=powered_ratio,
        log_parameter_condition_number=two_scale_log_parameter_condition_number(
            correlation_length,
            scale_1,
            scale_2,
            dimension=ndim,
        ),
        relative_reconstruction_residual=residual,
    )


def top_hat_gaussian_effective_variance_1d(
    point_variance: float,
    correlation_length: float,
    window_length: float,
) -> float:
    r"""Return the exact 1D top-hat variance for Gaussian covariance."""

    variance = _positive("point_variance", point_variance)
    xi = _positive("correlation_length", correlation_length)
    length = _positive("window_length", window_length)
    ratio = length / xi
    if ratio < 1.0e-3:
        attenuation = (
            1.0
            - ratio**2 / 12.0
            + ratio**4 / 120.0
            - ratio**6 / 1344.0
        )
    else:
        bracket = (
            ratio
            * math.sqrt(math.pi / 2.0)
            * math.erf(ratio / math.sqrt(2.0))
            + math.expm1(-0.5 * ratio * ratio)
        )
        attenuation = 2.0 * bracket / (ratio * ratio)
    return variance * attenuation


def top_hat_exponential_effective_variance_1d(
    point_variance: float,
    correlation_length: float,
    window_length: float,
) -> float:
    r"""Return the exact 1D top-hat variance for exponential covariance."""

    variance = _positive("point_variance", point_variance)
    xi = _positive("correlation_length", correlation_length)
    length = _positive("window_length", window_length)
    ratio = length / xi
    if ratio < 1.0e-4:
        attenuation = (
            1.0
            - ratio / 3.0
            + ratio**2 / 12.0
            - ratio**3 / 60.0
            + ratio**4 / 360.0
        )
    else:
        attenuation = 2.0 * (ratio + math.expm1(-ratio)) / (ratio * ratio)
    return variance * attenuation


def probe_averaged_gap_moments(
    gap_model: Callable[[float, float], float],
    mean_composition: float,
    temperature_k: float,
    point_composition_variance: float,
    correlation_length: float,
    probe_sigma: float,
    *,
    dimension: int = 2,
    derivative_step: float = 1.0e-5,
) -> ProbeAveragedGapMoments:
    r"""Propagate filtered Gaussian composition through a signed-gap law.

    .. math::

       \mathbb E[E_g]\simeq E_g(\bar x,T)+\tfrac12 E_{g,xx}V_a,

    .. math::

       \operatorname{Var}(E_g)\simeq E_{g,x}^2V_a
       +\tfrac12 E_{g,xx}^2V_a^2.

    The variance is exact for a quadratic composition dependence and Gaussian
    probe-averaged composition.
    """

    composition = _finite("mean_composition", mean_composition)
    temperature = _finite("temperature_k", temperature_k)
    point_variance = _positive(
        "point_composition_variance", point_composition_variance
    )
    xi = _positive("correlation_length", correlation_length)
    scale = _nonnegative("probe_sigma", probe_sigma)
    ndim = _dimension(dimension)
    step = _positive("derivative_step", derivative_step)

    effective_variance = isotropic_gaussian_effective_variance(
        point_variance,
        xi,
        scale,
        dimension=ndim,
    )
    center = float(gap_model(composition, temperature))
    plus = float(gap_model(composition + step, temperature))
    minus = float(gap_model(composition - step, temperature))
    if not all(math.isfinite(value) for value in (center, plus, minus)):
        raise ValueError("gap_model returned a non-finite value")

    first = (plus - minus) / (2.0 * step)
    second = (plus - 2.0 * center + minus) / (step * step)
    mean_gap = center + 0.5 * second * effective_variance
    gap_variance = (
        first * first * effective_variance
        + 0.5 * second * second * effective_variance * effective_variance
    )
    return ProbeAveragedGapMoments(
        gap_at_mean_ev=center,
        mean_gap_ev=mean_gap,
        gap_variance_ev2=gap_variance,
        gap_standard_deviation_ev=math.sqrt(max(gap_variance, 0.0)),
        effective_composition_variance=effective_variance,
        effective_composition_standard_deviation=math.sqrt(effective_variance),
        first_composition_derivative_ev=first,
        second_composition_derivative_ev=second,
    )


def cutoff_standard_deviation_um(
    gap_standard_deviation_ev: float,
    cutoff_wavelength_um: float,
    cutoff_energy_ev: float,
) -> float:
    r"""Convert a small gap spread to first-order cutoff-wavelength spread."""

    gap_sigma = _nonnegative("gap_standard_deviation_ev", gap_standard_deviation_ev)
    wavelength = _positive("cutoff_wavelength_um", cutoff_wavelength_um)
    energy = abs(_finite("cutoff_energy_ev", cutoff_energy_ev))
    if energy == 0.0:
        raise ValueError("cutoff_energy_ev must be non-zero")
    return wavelength * gap_sigma / energy
