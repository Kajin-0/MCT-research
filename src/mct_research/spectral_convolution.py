"""Controlled spectral operators for distributed HgCdTe band gaps.

The primary operator averages a declared power-law intrinsic absorption edge over
an independently declared Gaussian distribution of local gaps.  It is a
controlled reproduction layer for the inhomogeneous-broadening argument in
Herrmann, Moellmann, and Tomm (1992); it is not the complete Anderson/Herrmann
Kane, band-filling, free-carrier, excitonic, or defect-state model.

All energies are in electron volts and absorption coefficients are in inverse
centimetres when the supplied amplitude or normalization uses those units.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class ExponentialTailFit:
    """Log-linear fit of an apparent exponential absorption tail."""

    tail_energy_ev: float
    log_slope_ev_inverse: float
    log_intercept: float
    r_squared: float
    log_rmse: float
    point_count: int
    energy_lower_ev: float
    energy_upper_ev: float
    absorption_lower_cm_inverse: float
    absorption_upper_cm_inverse: float


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def herrmann_gap_sigma_ev(source_scale_s_ev: float) -> float:
    """Convert Herrmann et al. (1992) Eq. (8) ``s`` to standard deviation.

    The source writes the Gaussian-like gap distribution as

    ``P(G) = exp(-(G-Gbar)**2/(4*s**2)) / (2*s*sqrt(pi))``.

    Therefore its ordinary standard deviation is ``sqrt(2)*s``.  This function
    performs only that convention conversion; it does not infer ``s`` from an
    observed Urbach energy.
    """

    source_scale = _finite_scalar("source_scale_s_ev", source_scale_s_ev)
    if source_scale < 0.0:
        raise ValueError("source_scale_s_ev must be non-negative")
    return sqrt(2.0) * source_scale


def _standard_normal_quadrature(
    *,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    order = int(quadrature_order)
    z_limit = _finite_scalar("standard_deviation_limit", standard_deviation_limit)
    if order < 32:
        raise ValueError("quadrature_order must be at least 32")
    if z_limit <= 0.0:
        raise ValueError("standard_deviation_limit must be positive")

    canonical_nodes, canonical_weights = np.polynomial.legendre.leggauss(order)
    z_nodes = z_limit * canonical_nodes
    normal_density = np.exp(-0.5 * z_nodes**2) / sqrt(2.0 * np.pi)
    raw_weights = z_limit * canonical_weights * normal_density
    normalization = float(np.sum(raw_weights))
    if normalization <= 0.0 or not np.isfinite(normalization):
        raise ValueError("quadrature failed to resolve the Gaussian distribution")
    return (
        np.asarray(z_nodes, dtype=float),
        np.asarray(raw_weights / normalization, dtype=float),
    )


def gaussian_gap_convolved_power_absorption(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    *,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> NDArray[np.float64]:
    """Average a sharp power-law edge over a Gaussian local-gap distribution.

    For a local gap ``G``, the controlled intrinsic edge is

    ``alpha(E | G) = A * max(E-G, 0)**p``.

    The returned spectrum is its expectation for
    ``G ~ Normal(mean_gap_ev, gap_sigma_ev**2)``.  ``p=0.5`` is the simple
    square-root edge used for the principal Herrmann reproduction.  Values from
    ``0.5`` to ``2`` provide a controlled nonparabolic sensitivity family; they
    are not a replacement for the complete Kane absorption model.
    """

    energy = np.asarray(photon_energy_ev, dtype=float)
    if not np.all(np.isfinite(energy)):
        raise ValueError("photon_energy_ev must be finite")
    mean_gap = _finite_scalar("mean_gap_ev", mean_gap_ev)
    sigma_gap = _finite_scalar("gap_sigma_ev", gap_sigma_ev)
    power = _finite_scalar("exponent", exponent)
    amplitude = _finite_scalar(
        "amplitude_cm_inverse_ev_power", amplitude_cm_inverse_ev_power
    )
    if sigma_gap < 0.0:
        raise ValueError("gap_sigma_ev must be non-negative")
    if power < 0.0:
        raise ValueError("exponent must be non-negative")
    if amplitude < 0.0:
        raise ValueError("amplitude_cm_inverse_ev_power must be non-negative")

    energy_flat = energy.reshape(-1)
    if sigma_gap == 0.0:
        excess = energy_flat - mean_gap
        if power == 0.0:
            absorption = amplitude * (excess >= 0.0).astype(float)
        else:
            absorption = amplitude * np.maximum(excess, 0.0) ** power
        return np.asarray(absorption.reshape(energy.shape), dtype=float)

    z_nodes, weights = _standard_normal_quadrature(
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    local_gaps = mean_gap + sigma_gap * z_nodes
    absorption = np.empty_like(energy_flat)

    # Chunking keeps the temporary node-by-energy array bounded for dense spectra.
    chunk_size = 2048
    for start in range(0, energy_flat.size, chunk_size):
        stop = min(start + chunk_size, energy_flat.size)
        excess = energy_flat[start:stop][None, :] - local_gaps[:, None]
        if power == 0.0:
            local_absorption = (excess >= 0.0).astype(float)
        else:
            local_absorption = np.maximum(excess, 0.0) ** power
        absorption[start:stop] = amplitude * np.sum(
            weights[:, None] * local_absorption,
            axis=0,
        )

    return np.asarray(absorption.reshape(energy.shape), dtype=float)


def normalized_gaussian_gap_convolved_power_absorption(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    *,
    exponent: float = 0.5,
    absorption_at_mean_gap_cm_inverse: float = 1000.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> NDArray[np.float64]:
    """Return a convolved spectrum normalized at the declared mean gap.

    This isolates lineshape and fit-window sensitivity from an otherwise
    arbitrary matrix-element prefactor.  The normalization is a declared
    modeling choice, not a source-measured universal HgCdTe constant.
    """

    sigma_gap = _finite_scalar("gap_sigma_ev", gap_sigma_ev)
    target = _finite_scalar(
        "absorption_at_mean_gap_cm_inverse",
        absorption_at_mean_gap_cm_inverse,
    )
    if sigma_gap <= 0.0:
        raise ValueError("gap_sigma_ev must be positive for mean-gap normalization")
    if target <= 0.0:
        raise ValueError("absorption_at_mean_gap_cm_inverse must be positive")

    reference = float(
        gaussian_gap_convolved_power_absorption(
            np.asarray([mean_gap_ev], dtype=float),
            mean_gap_ev,
            sigma_gap,
            exponent=exponent,
            quadrature_order=quadrature_order,
            standard_deviation_limit=standard_deviation_limit,
        )[0]
    )
    if reference <= 0.0 or not np.isfinite(reference):
        raise ValueError("mean-gap absorption normalization is not resolvable")

    return gaussian_gap_convolved_power_absorption(
        photon_energy_ev,
        mean_gap_ev,
        sigma_gap,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=target / reference,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )


def fit_exponential_absorption_tail(
    photon_energy_ev: ArrayLike,
    absorption_cm_inverse: ArrayLike,
    *,
    absorption_bounds_cm_inverse: tuple[float, float] = (1.0, 100.0),
    maximum_energy_ev: float | None = None,
    minimum_points: int = 8,
) -> ExponentialTailFit:
    """Fit ``ln(alpha) = intercept + E/W`` over a declared absorption range."""

    energy = np.asarray(photon_energy_ev, dtype=float).reshape(-1)
    absorption = np.asarray(absorption_cm_inverse, dtype=float).reshape(-1)
    if energy.shape != absorption.shape:
        raise ValueError("photon energy and absorption arrays must have equal shape")
    if energy.size < 2 or not np.all(np.isfinite(energy)):
        raise ValueError("photon_energy_ev must contain finite values")
    if not np.all(np.isfinite(absorption)) or np.any(absorption < 0.0):
        raise ValueError("absorption_cm_inverse must be finite and non-negative")
    if np.any(np.diff(energy) <= 0.0):
        raise ValueError("photon_energy_ev must be strictly increasing")

    alpha_lower = _finite_scalar(
        "absorption_bounds_cm_inverse[0]", absorption_bounds_cm_inverse[0]
    )
    alpha_upper = _finite_scalar(
        "absorption_bounds_cm_inverse[1]", absorption_bounds_cm_inverse[1]
    )
    if alpha_lower <= 0.0 or alpha_lower >= alpha_upper:
        raise ValueError("absorption bounds must be positive and strictly ordered")
    count_minimum = int(minimum_points)
    if count_minimum < 3:
        raise ValueError("minimum_points must be at least 3")

    mask = (absorption >= alpha_lower) & (absorption <= alpha_upper)
    if maximum_energy_ev is not None:
        energy_maximum = _finite_scalar("maximum_energy_ev", maximum_energy_ev)
        mask &= energy <= energy_maximum
    selected_energy = energy[mask]
    selected_absorption = absorption[mask]
    if selected_energy.size < count_minimum:
        raise ValueError("declared fit window contains too few points")

    log_absorption = np.log(selected_absorption)
    design = np.column_stack([selected_energy, np.ones_like(selected_energy)])
    coefficients, _, _, _ = np.linalg.lstsq(design, log_absorption, rcond=None)
    slope = float(coefficients[0])
    intercept = float(coefficients[1])
    if slope <= 0.0 or not np.isfinite(slope):
        raise ValueError("fitted absorption tail does not have a positive log slope")

    fitted = slope * selected_energy + intercept
    residual = log_absorption - fitted
    residual_sum = float(np.sum(residual**2))
    centred_sum = float(np.sum((log_absorption - np.mean(log_absorption)) ** 2))
    r_squared = 1.0 if centred_sum == 0.0 else 1.0 - residual_sum / centred_sum

    return ExponentialTailFit(
        tail_energy_ev=1.0 / slope,
        log_slope_ev_inverse=slope,
        log_intercept=intercept,
        r_squared=r_squared,
        log_rmse=sqrt(residual_sum / selected_energy.size),
        point_count=int(selected_energy.size),
        energy_lower_ev=float(selected_energy[0]),
        energy_upper_ev=float(selected_energy[-1]),
        absorption_lower_cm_inverse=alpha_lower,
        absorption_upper_cm_inverse=alpha_upper,
    )
