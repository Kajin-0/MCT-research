"""Recoverability limits for logarithmic curvature in published tail figures.

This module asks whether a finite, rasterized log-absorption plot can distinguish
an exact exponential from the controlled Gaussian-distributed power-edge model

``alpha_p(E) = A E[(E-G)_+**p]``.

The calculation is intentionally source- and figure-bounded. It does not infer a
specimen gap distribution, composition variance, or microscopic Urbach mechanism.
Its central result is a finite-window non-falsifiability statement: when the
standardized location of the observed window is unconstrained, a sufficiently deep
Gaussian-power tail can be made arbitrarily straight over any fixed finite dynamic
range.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import erf, isfinite, log, log10, sqrt

import numpy as np


@dataclass(frozen=True)
class GaussianTailWindowStraightness:
    """Straightness of one finite Gaussian-power absorption window."""

    lower_standardized_energy: float
    upper_standardized_energy: float
    dynamic_range_decades: float
    standardized_span: float
    maximum_vertical_residual_decades: float
    rms_vertical_residual_decades: float
    maximum_horizontal_residual_fraction: float
    rms_horizontal_residual_fraction: float
    exponent: float
    sample_count: int
    quadrature_order: int
    standard_deviation_limit: float


@dataclass(frozen=True)
class PublishedFigureTraceRecoverability:
    """Pixel-space departure of a curved trace from its best straight line."""

    lower_standardized_energy: float
    upper_standardized_energy: float
    dynamic_range_decades: float
    trace_horizontal_span_px: float
    trace_vertical_span_px: float
    maximum_orthogonal_departure_px: float
    rms_orthogonal_departure_px: float
    center_uncertainty_px: float
    departure_to_uncertainty_ratio: float
    one_sigma_resolvable: bool
    three_sigma_resolvable: bool
    exponent: float


@dataclass(frozen=True)
class SourceConditionedTrace:
    """Source-parameterized trace span and curvature thresholds."""

    source_identifier: str
    composition: float
    temperature_k: float
    absorption_min_cm_inverse: float
    absorption_max_cm_inverse: float
    trace_energy_span_ev: float
    trace_horizontal_span_px: float
    trace_vertical_span_px: float
    marker_center_uncertainty_px: float
    departure_at_mean_gap_px: float
    critical_upper_z_one_sigma: float | None
    critical_upper_z_three_sigma: float | None


def _finite_positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite_nonnegative(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


@lru_cache(maxsize=16)
def _standard_normal_rule(
    quadrature_order: int,
    standard_deviation_limit: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    order = int(quadrature_order)
    limit = float(standard_deviation_limit)
    if order < 32:
        raise ValueError("quadrature_order must be at least 32")
    if not isfinite(limit) or limit <= 0.0:
        raise ValueError("standard_deviation_limit must be finite and positive")
    nodes, weights = np.polynomial.legendre.leggauss(order)
    normalization = erf(limit / sqrt(2.0))
    nodes = np.asarray(nodes, dtype=float)
    weights = np.asarray(weights, dtype=float)
    nodes.setflags(write=False)
    weights.setflags(write=False)
    return nodes, weights, float(normalization)


def _dimensionless_log_shape(
    standardized_energy: np.ndarray,
    *,
    exponent: float,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> np.ndarray:
    z = np.asarray(standardized_energy, dtype=float)
    if z.size == 0 or not np.all(np.isfinite(z)):
        raise ValueError("standardized_energy must contain finite values")
    power = _finite_nonnegative("exponent", exponent)
    nodes, weights, normalization = _standard_normal_rule(
        int(quadrature_order), float(standard_deviation_limit)
    )
    limit = float(standard_deviation_limit)
    flat = z.reshape(-1)
    values = np.zeros_like(flat)
    chunk_size = 1024
    for start in range(0, flat.size, chunk_size):
        stop = min(start + chunk_size, flat.size)
        z_chunk = flat[start:stop]
        upper = np.minimum(z_chunk, limit)
        active = upper > -limit
        if not np.any(active):
            continue
        active_upper = upper[active]
        half_width = 0.5 * (active_upper + limit)
        centre = 0.5 * (active_upper - limit)
        u = half_width[:, None] * nodes[None, :] + centre[:, None]
        excess = z_chunk[active, None] - u
        density = np.exp(-0.5 * u**2) / sqrt(2.0 * np.pi)
        if power == 0.0:
            local_power = np.ones_like(excess)
        else:
            local_power = excess**power
        integral = np.sum(
            half_width[:, None] * weights[None, :] * density * local_power,
            axis=1,
        ) / normalization
        chunk_values = np.zeros_like(z_chunk)
        chunk_values[active] = integral
        values[start:stop] = chunk_values
    if np.any(values <= 0.0) or not np.all(np.isfinite(values)):
        raise ValueError("Gaussian-power tail is not resolved in the declared window")
    return np.log10(values.reshape(z.shape))


def _lower_endpoint_for_dynamic_range(
    upper_standardized_energy: float,
    dynamic_range_decades: float,
    *,
    exponent: float,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> float:
    upper = float(upper_standardized_energy)
    upper_log = float(
        _dimensionless_log_shape(
            np.asarray([upper]),
            exponent=exponent,
            quadrature_order=quadrature_order,
            standard_deviation_limit=standard_deviation_limit,
        )[0]
    )
    target = upper_log - dynamic_range_decades
    support_floor = -standard_deviation_limit + 1.0e-6
    lower = max(support_floor, upper - 1.0)
    lower_log = float(
        _dimensionless_log_shape(
            np.asarray([lower]),
            exponent=exponent,
            quadrature_order=quadrature_order,
            standard_deviation_limit=standard_deviation_limit,
        )[0]
    )
    while lower_log > target:
        if lower <= support_floor + 1.0e-12:
            raise ValueError(
                "dynamic range extends below the declared Gaussian support; "
                "increase standard_deviation_limit"
            )
        lower = max(support_floor, lower - 1.0)
        lower_log = float(
            _dimensionless_log_shape(
                np.asarray([lower]),
                exponent=exponent,
                quadrature_order=quadrature_order,
                standard_deviation_limit=standard_deviation_limit,
            )[0]
        )
    higher = upper
    for _ in range(64):
        midpoint = 0.5 * (lower + higher)
        midpoint_log = float(
            _dimensionless_log_shape(
                np.asarray([midpoint]),
                exponent=exponent,
                quadrature_order=quadrature_order,
                standard_deviation_limit=standard_deviation_limit,
            )[0]
        )
        if midpoint_log < target:
            lower = midpoint
        else:
            higher = midpoint
    return 0.5 * (lower + higher)


def _window_coordinates(
    upper_standardized_energy: float,
    dynamic_range_decades: float,
    *,
    exponent: float,
    sample_count: int,
    quadrature_order: int,
    standard_deviation_limit: float,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    lower = _lower_endpoint_for_dynamic_range(
        upper_standardized_energy,
        dynamic_range_decades,
        exponent=exponent,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    upper = float(upper_standardized_energy)
    z_uniform = np.linspace(lower, upper, sample_count)
    log_uniform_z = _dimensionless_log_shape(
        z_uniform,
        exponent=exponent,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    dense_count = max(4 * sample_count, 1025)
    z_dense = np.linspace(lower, upper, dense_count)
    log_dense = _dimensionless_log_shape(
        z_dense,
        exponent=exponent,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    log_uniform = np.linspace(log_dense[0], log_dense[-1], sample_count)
    z_uniform_log = np.interp(log_uniform, log_dense, z_dense)
    return lower, z_uniform, log_uniform_z, z_uniform_log, log_uniform


def gaussian_power_tail_window_straightness(
    upper_standardized_energy: float,
    dynamic_range_decades: float,
    *,
    exponent: float = 0.5,
    sample_count: int = 401,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> GaussianTailWindowStraightness:
    """Quantify finite-window departure from a best exponential fit."""
    upper = float(upper_standardized_energy)
    if not isfinite(upper) or upper > 0.0:
        raise ValueError("upper_standardized_energy must be finite and <= 0")
    dynamic_range = _finite_positive("dynamic_range_decades", dynamic_range_decades)
    power = _finite_nonnegative("exponent", exponent)
    count = int(sample_count)
    order = int(quadrature_order)
    z_limit = _finite_positive("standard_deviation_limit", standard_deviation_limit)
    if count < 33:
        raise ValueError("sample_count must be at least 33")
    if order < 32:
        raise ValueError("quadrature_order must be at least 32")
    if upper <= -z_limit:
        raise ValueError("upper_standardized_energy must lie inside Gaussian support")
    lower, z_energy, log_energy, z_log, log_levels = _window_coordinates(
        upper,
        dynamic_range,
        exponent=power,
        sample_count=count,
        quadrature_order=order,
        standard_deviation_limit=z_limit,
    )
    vertical_design = np.column_stack((np.ones(count), z_energy))
    vertical_coefficients = np.linalg.lstsq(vertical_design, log_energy, rcond=None)[0]
    vertical_residual = log_energy - vertical_design @ vertical_coefficients
    horizontal_design = np.column_stack((np.ones(count), log_levels))
    horizontal_coefficients = np.linalg.lstsq(horizontal_design, z_log, rcond=None)[0]
    horizontal_residual = z_log - horizontal_design @ horizontal_coefficients
    standardized_span = upper - lower
    return GaussianTailWindowStraightness(
        lower_standardized_energy=lower,
        upper_standardized_energy=upper,
        dynamic_range_decades=dynamic_range,
        standardized_span=standardized_span,
        maximum_vertical_residual_decades=float(np.max(np.abs(vertical_residual))),
        rms_vertical_residual_decades=float(np.sqrt(np.mean(vertical_residual**2))),
        maximum_horizontal_residual_fraction=float(
            np.max(np.abs(horizontal_residual)) / standardized_span
        ),
        rms_horizontal_residual_fraction=float(
            np.sqrt(np.mean(horizontal_residual**2)) / standardized_span
        ),
        exponent=power,
        sample_count=count,
        quadrature_order=order,
        standard_deviation_limit=z_limit,
    )


def gaussian_power_tail_pixel_recoverability(
    upper_standardized_energy: float,
    dynamic_range_decades: float,
    trace_horizontal_span_px: float,
    trace_vertical_span_px: float,
    center_uncertainty_px: float,
    *,
    exponent: float = 0.5,
    sample_count: int = 401,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> PublishedFigureTraceRecoverability:
    """Map the curved model trace into plot pixels and fit a TLS straight line."""
    upper = float(upper_standardized_energy)
    if not isfinite(upper) or upper > 0.0:
        raise ValueError("upper_standardized_energy must be finite and <= 0")
    horizontal_span = _finite_positive("trace_horizontal_span_px", trace_horizontal_span_px)
    vertical_span = _finite_positive("trace_vertical_span_px", trace_vertical_span_px)
    uncertainty = _finite_positive("center_uncertainty_px", center_uncertainty_px)
    dynamic_range = _finite_positive("dynamic_range_decades", dynamic_range_decades)
    power = _finite_nonnegative("exponent", exponent)
    count = int(sample_count)
    if count < 33:
        raise ValueError("sample_count must be at least 33")
    lower, _, _, z_log, log_levels = _window_coordinates(
        upper,
        dynamic_range,
        exponent=power,
        sample_count=count,
        quadrature_order=int(quadrature_order),
        standard_deviation_limit=standard_deviation_limit,
    )
    x_px = (z_log - lower) * horizontal_span / (upper - lower)
    y_px = (
        (log_levels - log_levels[0])
        * vertical_span
        / (log_levels[-1] - log_levels[0])
    )
    points = np.column_stack((x_px, y_px))
    centered = points - np.mean(points, axis=0)
    _, _, right_vectors = np.linalg.svd(centered, full_matrices=False)
    direction = right_vectors[0]
    normal = np.asarray([-direction[1], direction[0]])
    orthogonal_residual = centered @ normal
    maximum = float(np.max(np.abs(orthogonal_residual)))
    rms = float(np.sqrt(np.mean(orthogonal_residual**2)))
    ratio = maximum / uncertainty
    return PublishedFigureTraceRecoverability(
        lower_standardized_energy=lower,
        upper_standardized_energy=upper,
        dynamic_range_decades=dynamic_range,
        trace_horizontal_span_px=horizontal_span,
        trace_vertical_span_px=vertical_span,
        maximum_orthogonal_departure_px=maximum,
        rms_orthogonal_departure_px=rms,
        center_uncertainty_px=uncertainty,
        departure_to_uncertainty_ratio=ratio,
        one_sigma_resolvable=ratio >= 1.0,
        three_sigma_resolvable=ratio >= 3.0,
        exponent=power,
    )


def critical_upper_standardized_energy(
    dynamic_range_decades: float,
    trace_horizontal_span_px: float,
    trace_vertical_span_px: float,
    center_uncertainty_px: float,
    *,
    significance: float = 1.0,
    exponent: float = 0.5,
    sample_count: int = 401,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> float | None:
    """Return the upper ``z`` threshold required to exceed pixel uncertainty."""
    sigma_multiple = _finite_positive("significance", significance)
    target = sigma_multiple * _finite_positive("center_uncertainty_px", center_uncertainty_px)
    z_limit = _finite_positive("standard_deviation_limit", standard_deviation_limit)

    def departure(z_value: float) -> float:
        return gaussian_power_tail_pixel_recoverability(
            z_value,
            dynamic_range_decades,
            trace_horizontal_span_px,
            trace_vertical_span_px,
            center_uncertainty_px,
            exponent=exponent,
            sample_count=sample_count,
            quadrature_order=quadrature_order,
            standard_deviation_limit=z_limit,
        ).maximum_orthogonal_departure_px

    if departure(0.0) < target:
        return None
    lower = -z_limit + 2.0
    lower_departure = departure(lower)
    if lower_departure >= target:
        return lower
    upper = 0.0
    for _ in range(40):
        midpoint = 0.5 * (lower + upper)
        if departure(midpoint) < target:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def finkman_modified_urbach_trace_span_ev(
    composition: float,
    temperature_k: float,
    absorption_min_cm_inverse: float,
    absorption_max_cm_inverse: float,
) -> float:
    """Return the source-conditioned energy span from Finkman 1984 Eq. (10)."""
    x = float(composition)
    temperature = float(temperature_k)
    lower = _finite_positive("absorption_min_cm_inverse", absorption_min_cm_inverse)
    upper = _finite_positive("absorption_max_cm_inverse", absorption_max_cm_inverse)
    if not isfinite(x) or x < 0.0 or x > 1.0:
        raise ValueError("composition must lie in [0, 1]")
    if not isfinite(temperature) or temperature <= 0.0:
        raise ValueError("temperature_k must be finite and positive")
    if upper <= lower:
        raise ValueError("absorption_max_cm_inverse must exceed the minimum")
    return (temperature + 81.9) * log(upper / lower) / (3.267e4 * (1.0 + x))


def source_conditioned_finkman_trace(
    *,
    source_identifier: str,
    composition: float,
    temperature_k: float,
    absorption_min_cm_inverse: float,
    absorption_max_cm_inverse: float,
    panel_energy_min_ev: float,
    panel_energy_max_ev: float,
    panel_width_px: float,
    panel_absorption_min_cm_inverse: float,
    panel_absorption_max_cm_inverse: float,
    panel_height_px: float,
    marker_center_uncertainty_px: float,
    exponent: float = 0.5,
    sample_count: int = 401,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> SourceConditionedTrace:
    """Evaluate one Finkman trace using declared panel and uncertainty inputs."""
    energy_min = float(panel_energy_min_ev)
    energy_max = float(panel_energy_max_ev)
    if not isfinite(energy_min) or not isfinite(energy_max) or energy_max <= energy_min:
        raise ValueError("panel energy bounds must be finite and increasing")
    width = _finite_positive("panel_width_px", panel_width_px)
    height = _finite_positive("panel_height_px", panel_height_px)
    panel_alpha_min = _finite_positive(
        "panel_absorption_min_cm_inverse", panel_absorption_min_cm_inverse
    )
    panel_alpha_max = _finite_positive(
        "panel_absorption_max_cm_inverse", panel_absorption_max_cm_inverse
    )
    if panel_alpha_max <= panel_alpha_min:
        raise ValueError("panel absorption bounds must be increasing")
    uncertainty = _finite_positive("marker_center_uncertainty_px", marker_center_uncertainty_px)
    trace_span_ev = finkman_modified_urbach_trace_span_ev(
        composition,
        temperature_k,
        absorption_min_cm_inverse,
        absorption_max_cm_inverse,
    )
    horizontal_span = width * trace_span_ev / (energy_max - energy_min)
    trace_dynamic_range = log10(absorption_max_cm_inverse / absorption_min_cm_inverse)
    panel_dynamic_range = log10(panel_alpha_max / panel_alpha_min)
    vertical_span = height * trace_dynamic_range / panel_dynamic_range
    at_mean = gaussian_power_tail_pixel_recoverability(
        0.0,
        trace_dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    critical_one = critical_upper_standardized_energy(
        trace_dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        significance=1.0,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    critical_three = critical_upper_standardized_energy(
        trace_dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        significance=3.0,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    return SourceConditionedTrace(
        source_identifier=str(source_identifier),
        composition=float(composition),
        temperature_k=float(temperature_k),
        absorption_min_cm_inverse=float(absorption_min_cm_inverse),
        absorption_max_cm_inverse=float(absorption_max_cm_inverse),
        trace_energy_span_ev=trace_span_ev,
        trace_horizontal_span_px=horizontal_span,
        trace_vertical_span_px=vertical_span,
        marker_center_uncertainty_px=uncertainty,
        departure_at_mean_gap_px=at_mean.maximum_orthogonal_departure_px,
        critical_upper_z_one_sigma=critical_one,
        critical_upper_z_three_sigma=critical_three,
    )
