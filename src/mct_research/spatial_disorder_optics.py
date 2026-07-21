"""Lateral transmission averaging for a distributed local band edge.

This module compares two distinct operations for laterally heterogeneous columns
of uniform thickness:

``mean_alpha(E) = E_G[alpha(E | G)]``

and

``alpha_T(E) = -log(E_G[exp(-d alpha(E | G))]) / d``.

The local controlled edge is ``alpha(E | G) = A max(E-G, 0)**p`` with a
Gaussian distribution of column gaps.  Jensen's inequality requires
``alpha_T <= mean_alpha``.  The implementation preserves that operation order
and evaluates averaged transmission in the log domain.

It is not a depth-varying ray model, a complete HgCdTe absorption law, or a
detector-response calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, isfinite, log, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spectral_convolution import gaussian_gap_convolved_power_absorption

FloatArray = NDArray[np.float64]


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _validated_quadrature_order(order: int) -> int:
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise ValueError("quadrature_order must be an integer")
    result = int(order)
    if result < 32 or result > 4096:
        raise ValueError("quadrature_order must lie between 32 and 4096")
    return result


def _read_only_array(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _normal_cdf(value: FloatArray) -> FloatArray:
    flattened = np.asarray(value, dtype=float).reshape(-1)
    result = np.fromiter(
        (0.5 * (1.0 + erf(float(item) / sqrt(2.0))) for item in flattened),
        dtype=float,
        count=flattened.size,
    )
    return result.reshape(np.asarray(value).shape)


def _log_nonnegative(value: FloatArray) -> FloatArray:
    array = np.asarray(value, dtype=float)
    result = np.full(array.shape, -np.inf, dtype=float)
    positive = array > 0.0
    result[positive] = np.log(array[positive])
    return result


def _row_logsumexp(log_values: FloatArray) -> FloatArray:
    maximum = np.max(log_values, axis=1)
    result = np.full(maximum.shape, -np.inf, dtype=float)
    finite = np.isfinite(maximum)
    if np.any(finite):
        result[finite] = maximum[finite] + np.log(
            np.sum(
                np.exp(log_values[finite] - maximum[finite, None]),
                axis=1,
            )
        )
    return result


def _local_power_absorption(
    photon_energy_ev: FloatArray,
    mean_gap_ev: float,
    *,
    exponent: float,
    amplitude_cm_inverse_ev_power: float,
) -> FloatArray:
    excess = photon_energy_ev - mean_gap_ev
    if exponent == 0.0:
        return amplitude_cm_inverse_ev_power * (excess >= 0.0).astype(float)
    return amplitude_cm_inverse_ev_power * np.maximum(excess, 0.0) ** exponent


def _validated_inputs(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    thickness_cm: float,
    exponent: float,
    amplitude_cm_inverse_ev_power: float,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> tuple[FloatArray, float, float, float, float, float, int, float]:
    energy = np.asarray(photon_energy_ev, dtype=float)
    if not np.all(np.isfinite(energy)):
        raise ValueError("photon_energy_ev must contain only finite values")
    mean_gap = _finite_scalar("mean_gap_ev", mean_gap_ev)
    sigma_gap = _finite_scalar("gap_sigma_ev", gap_sigma_ev)
    thickness = _finite_scalar("thickness_cm", thickness_cm)
    power = _finite_scalar("exponent", exponent)
    amplitude = _finite_scalar(
        "amplitude_cm_inverse_ev_power", amplitude_cm_inverse_ev_power
    )
    order = _validated_quadrature_order(quadrature_order)
    z_limit = _finite_scalar("standard_deviation_limit", standard_deviation_limit)

    if sigma_gap < 0.0:
        raise ValueError("gap_sigma_ev must be non-negative")
    if thickness <= 0.0:
        raise ValueError("thickness_cm must be positive")
    if power < 0.0:
        raise ValueError("exponent must be non-negative")
    if amplitude < 0.0:
        raise ValueError("amplitude_cm_inverse_ev_power must be non-negative")
    if z_limit <= 0.0:
        raise ValueError("standard_deviation_limit must be positive")

    return (
        energy,
        mean_gap,
        sigma_gap,
        thickness,
        power,
        amplitude,
        order,
        z_limit,
    )


def gaussian_gap_averaged_log_transmission(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    thickness_cm: float,
    *,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> FloatArray:
    """Return ``log(E_G[exp(-d alpha(E|G))])`` for Gaussian column gaps.

    The Gaussian is truncated symmetrically at ``standard_deviation_limit`` and
    renormalized, matching the controlled distribution convention used by
    :func:`gaussian_gap_convolved_power_absorption`.  The absorbing interval is
    integrated only where ``G <= E``; the transparent probability is added
    analytically.  Log-sum-exp evaluation keeps optically thick cases stable.
    """

    (
        energy,
        mean_gap,
        sigma_gap,
        thickness,
        power,
        amplitude,
        order,
        z_limit,
    ) = _validated_inputs(
        photon_energy_ev,
        mean_gap_ev,
        gap_sigma_ev,
        thickness_cm,
        exponent,
        amplitude_cm_inverse_ev_power,
        quadrature_order,
        standard_deviation_limit,
    )

    if amplitude == 0.0:
        return np.zeros(energy.shape, dtype=float)

    flat_energy = energy.reshape(-1)
    if sigma_gap == 0.0:
        local_absorption = _local_power_absorption(
            flat_energy,
            mean_gap,
            exponent=power,
            amplitude_cm_inverse_ev_power=amplitude,
        )
        return np.asarray((-thickness * local_absorption).reshape(energy.shape))

    normal_probability = erf(z_limit / sqrt(2.0))
    if normal_probability <= 0.0 or not isfinite(normal_probability):
        raise ValueError("quadrature failed to resolve the Gaussian distribution")
    log_normal_probability = log(normal_probability)
    standardized_energy = (flat_energy - mean_gap) / sigma_gap

    clipped_threshold = np.clip(standardized_energy, -z_limit, z_limit)
    lower_cdf = 0.5 * (1.0 + erf(-z_limit / sqrt(2.0)))
    upper_cdf = 0.5 * (1.0 + erf(z_limit / sqrt(2.0)))
    active_mass = _normal_cdf(clipped_threshold) - lower_cdf
    active_mass = np.clip(active_mass, 0.0, normal_probability)
    transparent_mass = np.clip(normal_probability - active_mass, 0.0, normal_probability)

    if power == 0.0:
        optical_depth = thickness * amplitude
        log_total = np.logaddexp(
            _log_nonnegative(transparent_mass),
            _log_nonnegative(active_mass) - optical_depth,
        )
        log_transmission = log_total - log_normal_probability
        return np.asarray(log_transmission.reshape(energy.shape), dtype=float)

    canonical_nodes, canonical_weights = np.polynomial.legendre.leggauss(order)
    log_weights = np.log(canonical_weights)
    log_two_pi_half = 0.5 * log(2.0 * np.pi)
    log_transmission = np.zeros(flat_energy.shape, dtype=float)

    chunk_size = 512
    for start in range(0, flat_energy.size, chunk_size):
        stop = min(start + chunk_size, flat_energy.size)
        z_energy = standardized_energy[start:stop]
        upper = np.minimum(z_energy, z_limit)
        active = upper > -z_limit
        chunk_log_active = np.full(z_energy.shape, -np.inf, dtype=float)

        if np.any(active):
            active_upper = upper[active]
            half_width = 0.5 * (active_upper + z_limit)
            centre = 0.5 * (active_upper - z_limit)
            z_nodes = (
                half_width[:, None] * canonical_nodes[None, :]
                + centre[:, None]
            )
            excess_ev = sigma_gap * np.maximum(
                z_energy[active, None] - z_nodes,
                0.0,
            )
            with np.errstate(over="ignore", invalid="ignore"):
                local_absorption = amplitude * excess_ev**power
            if np.any(np.isnan(local_absorption)):
                raise ValueError("local absorption became undefined")

            log_terms = (
                np.log(half_width)[:, None]
                + log_weights[None, :]
                - 0.5 * z_nodes**2
                - log_two_pi_half
                - thickness * local_absorption
            )
            chunk_log_active[active] = _row_logsumexp(log_terms)

        chunk_log_transparent = _log_nonnegative(transparent_mass[start:stop])
        chunk_log_total = np.logaddexp(
            chunk_log_transparent,
            chunk_log_active,
        )
        log_transmission[start:stop] = chunk_log_total - log_normal_probability

    tolerance = 256.0 * np.finfo(float).eps
    if np.any(np.isnan(log_transmission)) or np.any(log_transmission > tolerance):
        raise RuntimeError("averaged log transmission left its physical interval")
    log_transmission = np.minimum(log_transmission, 0.0)
    return np.asarray(log_transmission.reshape(energy.shape), dtype=float)


@dataclass(frozen=True)
class LateralTransmissionObservation:
    """Operation-order diagnostics for laterally averaged transmission."""

    mean_absorption_cm_inverse: FloatArray
    log_averaged_transmission: FloatArray
    averaged_transmission: FloatArray
    transmission_effective_absorption_cm_inverse: FloatArray
    jensen_gap_cm_inverse: FloatArray
    relative_closure_error: FloatArray


def lateral_gaussian_gap_transmission_observation(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    thickness_cm: float,
    *,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> LateralTransmissionObservation:
    """Compare arithmetic absorption averaging with transmission averaging.

    ``relative_closure_error`` is defined as

    ``(mean_absorption - alpha_T) / mean_absorption``

    where the mean absorption is positive, and zero otherwise.
    """

    (
        energy,
        mean_gap,
        sigma_gap,
        thickness,
        power,
        amplitude,
        order,
        z_limit,
    ) = _validated_inputs(
        photon_energy_ev,
        mean_gap_ev,
        gap_sigma_ev,
        thickness_cm,
        exponent,
        amplitude_cm_inverse_ev_power,
        quadrature_order,
        standard_deviation_limit,
    )

    if sigma_gap == 0.0:
        mean_absorption = _local_power_absorption(
            energy,
            mean_gap,
            exponent=power,
            amplitude_cm_inverse_ev_power=amplitude,
        )
    elif amplitude == 0.0:
        mean_absorption = np.zeros(energy.shape, dtype=float)
    elif power == 0.0:
        standardized_energy = (energy - mean_gap) / sigma_gap
        clipped_threshold = np.clip(standardized_energy, -z_limit, z_limit)
        normal_probability = erf(z_limit / sqrt(2.0))
        lower_cdf = 0.5 * (1.0 + erf(-z_limit / sqrt(2.0)))
        active_probability = (
            _normal_cdf(clipped_threshold) - lower_cdf
        ) / normal_probability
        mean_absorption = amplitude * np.clip(active_probability, 0.0, 1.0)
    else:
        mean_absorption = gaussian_gap_convolved_power_absorption(
            energy,
            mean_gap,
            sigma_gap,
            exponent=power,
            amplitude_cm_inverse_ev_power=amplitude,
            quadrature_order=order,
            standard_deviation_limit=z_limit,
        )

    log_transmission = gaussian_gap_averaged_log_transmission(
        energy,
        mean_gap,
        sigma_gap,
        thickness,
        exponent=power,
        amplitude_cm_inverse_ev_power=amplitude,
        quadrature_order=order,
        standard_deviation_limit=z_limit,
    )
    effective_absorption = -log_transmission / thickness
    jensen_gap = np.asarray(mean_absorption, dtype=float) - effective_absorption

    scale = np.maximum.reduce(
        [
            np.ones(jensen_gap.shape, dtype=float),
            np.abs(np.asarray(mean_absorption, dtype=float)),
            np.abs(effective_absorption),
        ]
    )
    tolerance = 1.0e-10 * scale
    if np.any(jensen_gap < -tolerance):
        raise RuntimeError("numerical result violates the Jensen absorption bound")
    jensen_gap = np.maximum(jensen_gap, 0.0)

    relative_error = np.zeros(jensen_gap.shape, dtype=float)
    positive_mean = np.asarray(mean_absorption) > 0.0
    relative_error[positive_mean] = (
        jensen_gap[positive_mean] / np.asarray(mean_absorption)[positive_mean]
    )

    with np.errstate(under="ignore"):
        averaged_transmission = np.exp(log_transmission)

    return LateralTransmissionObservation(
        mean_absorption_cm_inverse=_read_only_array(mean_absorption),
        log_averaged_transmission=_read_only_array(log_transmission),
        averaged_transmission=_read_only_array(averaged_transmission),
        transmission_effective_absorption_cm_inverse=_read_only_array(
            effective_absorption
        ),
        jensen_gap_cm_inverse=_read_only_array(jensen_gap),
        relative_closure_error=_read_only_array(relative_error),
    )
