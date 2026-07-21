"""Controlled multiscale spatial-disorder measurement design.

This module composes three previously validated Stage 1 layers:

1. isotropic two-dimensional Gaussian composition-covariance filtering;
2. a declared first-order local gap closure,
   ``sigma_G = abs(dE_g/dx) * sigma_x,eff``;
3. operation-order-correct lateral response-cutoff extraction.

The result is a falsifiable forward prediction from probe scale to effective gap
width and reported cutoff.  It does not infer composition, evaluate gap-law
curvature, select a covariance family, or implement the Chang 2006 absorption
shape.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_cutoff import lateral_gaussian_gap_response_cutoff

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def _finite_positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _validated_probe_sigmas(value: ArrayLike) -> tuple[FloatArray, tuple[int, ...]]:
    scales = np.asarray(value, dtype=float)
    if scales.ndim > 1:
        raise ValueError("probe_sigmas must be a scalar or one-dimensional array")
    if scales.ndim == 1 and scales.size == 0:
        raise ValueError("probe_sigmas must not be empty")
    if not np.all(np.isfinite(scales)):
        raise ValueError("probe_sigmas must contain only finite values")
    if np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be non-negative")
    shape = scales.shape
    return np.array(scales.reshape(-1), dtype=float, copy=True), shape


def _read_only_float(value: ArrayLike, shape: tuple[int, ...]) -> FloatArray:
    result = np.array(value, dtype=float, copy=True).reshape(shape)
    result.setflags(write=False)
    return result


def _read_only_int(value: ArrayLike, shape: tuple[int, ...]) -> IntArray:
    result = np.array(value, dtype=np.int64, copy=True).reshape(shape)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class MultiscaleGapWidthPrediction:
    """First-order composition-to-gap width prediction at declared probe scales."""

    probe_sigmas: FloatArray
    probe_scale_ratios: FloatArray
    effective_composition_variance: FloatArray
    effective_composition_standard_deviation: FloatArray
    effective_gap_standard_deviation_ev: FloatArray
    point_composition_variance: float
    correlation_length: float
    gap_slope_ev_per_fraction: float


@dataclass(frozen=True)
class MultiscaleCutoffPrediction:
    """Operation-order cutoff predictions at multiple probe scales."""

    gap_width: MultiscaleGapWidthPrediction
    transmission_averaged_energy_ev: FloatArray
    mean_absorption_closure_energy_ev: FloatArray
    energy_shift_ev: FloatArray
    transmission_averaged_wavelength_um: FloatArray
    mean_absorption_closure_wavelength_um: FloatArray
    wavelength_shift_um: FloatArray
    transmission_response_residual: FloatArray
    mean_absorption_response_residual: FloatArray
    transmission_iterations: IntArray
    mean_absorption_iterations: IntArray
    mean_gap_ev: float
    thickness_cm: float
    target_response: float
    lower_energy_ev: float
    upper_energy_ev: float
    exponent: float
    amplitude_cm_inverse_ev_power: float


def multiscale_gaussian_gap_width(
    *,
    point_composition_variance: float,
    correlation_length: float,
    gap_slope_ev_per_fraction: float,
    probe_sigmas: ArrayLike,
) -> MultiscaleGapWidthPrediction:
    """Return the exact filtered composition width and linearized gap width.

    For the isotropic two-dimensional Gaussian benchmark,

    ``V_x(s) = sigma_x**2 / (1 + 2 s**2 / xi**2)``.

    The gap propagation is explicitly first order:

    ``sigma_G(s) = abs(dE_g/dx) * sqrt(V_x(s))``.
    """

    point_variance = _finite_positive(
        "point_composition_variance", point_composition_variance
    )
    correlation = _finite_positive("correlation_length", correlation_length)
    gap_slope = _finite_scalar("gap_slope_ev_per_fraction", gap_slope_ev_per_fraction)
    scales_flat, shape = _validated_probe_sigmas(probe_sigmas)

    scale_ratios = scales_flat / correlation
    log_denominator = np.logaddexp(
        0.0,
        log(2.0) + 2.0 * np.where(
            scales_flat > 0.0,
            np.log(scales_flat, where=scales_flat > 0.0, out=np.zeros_like(scales_flat)),
            -np.inf,
        ) - 2.0 * log(correlation),
    )
    effective_variance = np.exp(log(point_variance) - log_denominator)
    effective_standard_deviation = np.sqrt(effective_variance)
    effective_gap_standard_deviation = abs(gap_slope) * effective_standard_deviation

    if (
        not np.all(np.isfinite(effective_variance))
        or np.any(effective_variance <= 0.0)
        or not np.all(np.isfinite(effective_gap_standard_deviation))
    ):
        raise ValueError("probe scales cause the filtered disorder prediction to underflow")

    return MultiscaleGapWidthPrediction(
        probe_sigmas=_read_only_float(scales_flat, shape),
        probe_scale_ratios=_read_only_float(scale_ratios, shape),
        effective_composition_variance=_read_only_float(effective_variance, shape),
        effective_composition_standard_deviation=_read_only_float(
            effective_standard_deviation, shape
        ),
        effective_gap_standard_deviation_ev=_read_only_float(
            effective_gap_standard_deviation, shape
        ),
        point_composition_variance=point_variance,
        correlation_length=correlation,
        gap_slope_ev_per_fraction=gap_slope,
    )


def multiscale_gaussian_gap_cutoff_prediction(
    *,
    point_composition_variance: float,
    correlation_length: float,
    gap_slope_ev_per_fraction: float,
    probe_sigmas: ArrayLike,
    mean_gap_ev: float,
    thickness_cm: float,
    lower_energy_ev: float,
    upper_energy_ev: float,
    target_response: float = 0.5,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
    absolute_tolerance_ev: float = 1.0e-10,
    response_tolerance: float = 1.0e-12,
    max_iterations: int = 256,
) -> MultiscaleCutoffPrediction:
    """Propagate scale-filtered linearized gap width to fixed-response cutoffs.

    Input order is preserved.  No monotonic cutoff theorem is imposed across
    probe scales; only the validated per-scale Jensen ordering is inherited from
    :func:`lateral_gaussian_gap_response_cutoff`.
    """

    width = multiscale_gaussian_gap_width(
        point_composition_variance=point_composition_variance,
        correlation_length=correlation_length,
        gap_slope_ev_per_fraction=gap_slope_ev_per_fraction,
        probe_sigmas=probe_sigmas,
    )
    shape = width.probe_sigmas.shape
    gap_sigmas = np.asarray(width.effective_gap_standard_deviation_ev).reshape(-1)

    true_energy: list[float] = []
    closure_energy: list[float] = []
    energy_shift: list[float] = []
    true_wavelength: list[float] = []
    closure_wavelength: list[float] = []
    wavelength_shift: list[float] = []
    true_residual: list[float] = []
    closure_residual: list[float] = []
    true_iterations: list[int] = []
    closure_iterations: list[int] = []

    metadata = None
    for gap_sigma in gap_sigmas:
        comparison = lateral_gaussian_gap_response_cutoff(
            mean_gap_ev=mean_gap_ev,
            gap_sigma_ev=float(gap_sigma),
            thickness_cm=thickness_cm,
            lower_energy_ev=lower_energy_ev,
            upper_energy_ev=upper_energy_ev,
            target_response=target_response,
            exponent=exponent,
            amplitude_cm_inverse_ev_power=amplitude_cm_inverse_ev_power,
            quadrature_order=quadrature_order,
            standard_deviation_limit=standard_deviation_limit,
            absolute_tolerance_ev=absolute_tolerance_ev,
            response_tolerance=response_tolerance,
            max_iterations=max_iterations,
        )
        metadata = comparison
        true_energy.append(comparison.transmission_averaged_energy_ev)
        closure_energy.append(comparison.mean_absorption_closure_energy_ev)
        energy_shift.append(comparison.energy_shift_ev)
        true_wavelength.append(comparison.transmission_averaged_wavelength_um)
        closure_wavelength.append(comparison.mean_absorption_closure_wavelength_um)
        wavelength_shift.append(comparison.wavelength_shift_um)
        true_residual.append(comparison.transmission_response_residual)
        closure_residual.append(comparison.mean_absorption_response_residual)
        true_iterations.append(comparison.transmission_iterations)
        closure_iterations.append(comparison.mean_absorption_iterations)

    if metadata is None:
        raise RuntimeError("validated probe scales produced no cutoff predictions")

    return MultiscaleCutoffPrediction(
        gap_width=width,
        transmission_averaged_energy_ev=_read_only_float(true_energy, shape),
        mean_absorption_closure_energy_ev=_read_only_float(closure_energy, shape),
        energy_shift_ev=_read_only_float(energy_shift, shape),
        transmission_averaged_wavelength_um=_read_only_float(true_wavelength, shape),
        mean_absorption_closure_wavelength_um=_read_only_float(
            closure_wavelength, shape
        ),
        wavelength_shift_um=_read_only_float(wavelength_shift, shape),
        transmission_response_residual=_read_only_float(true_residual, shape),
        mean_absorption_response_residual=_read_only_float(closure_residual, shape),
        transmission_iterations=_read_only_int(true_iterations, shape),
        mean_absorption_iterations=_read_only_int(closure_iterations, shape),
        mean_gap_ev=float(metadata.transmission_averaged_energy_ev * 0.0 + mean_gap_ev),
        thickness_cm=float(thickness_cm),
        target_response=float(metadata.target_response),
        lower_energy_ev=float(metadata.lower_energy_ev),
        upper_energy_ev=float(metadata.upper_energy_ev),
        exponent=float(exponent),
        amplitude_cm_inverse_ev_power=float(amplitude_cm_inverse_ev_power),
    )
