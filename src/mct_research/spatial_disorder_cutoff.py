"""Detector-cutoff operation order for laterally heterogeneous columns.

The controlled response curves are

``R_true(E) = 1 - E_G[exp(-d alpha(E | G))]``

and

``R_mean(E) = 1 - exp(-d E_G[alpha(E | G)])``.

The first averages transmitted intensity before response extraction; the second
uses the arithmetic mean absorption as a scalar closure.  Jensen's inequality
requires ``R_true <= R_mean``.  For monotone curves, a fixed-response cutoff
therefore obeys ``E_cut,true >= E_cut,mean``.

This module uses the controlled Gaussian-gap power edge.  It is not a complete
HgCdTe detector model and does not distribute the Chang 2006 parameter set.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .detector_cutoff import cutoff_wavelength_um
from .spatial_disorder_optics import (
    lateral_gaussian_gap_transmission_observation,
)

FloatArray = NDArray[np.float64]


def _finite_positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _target_response(value: float) -> float:
    response = float(value)
    if not isfinite(response) or not 0.0 < response < 1.0:
        raise ValueError("target_response must lie strictly between zero and one")
    return response


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be a positive integer")
    result = int(value)
    if result <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return result


def _read_only_array(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class LateralResponseCurves:
    """Response curves for the exact transmission average and scalar closure."""

    transmission_averaged_response: FloatArray
    mean_absorption_closure_response: FloatArray
    closure_response_excess: FloatArray


@dataclass(frozen=True)
class LateralCutoffComparison:
    """Fixed-response cutoff comparison for two operation orders."""

    transmission_averaged_energy_ev: float
    mean_absorption_closure_energy_ev: float
    energy_shift_ev: float
    transmission_averaged_wavelength_um: float
    mean_absorption_closure_wavelength_um: float
    wavelength_shift_um: float
    target_response: float
    transmission_response_at_cutoff: float
    mean_absorption_response_at_cutoff: float
    transmission_response_residual: float
    mean_absorption_response_residual: float
    transmission_iterations: int
    mean_absorption_iterations: int
    lower_energy_ev: float
    upper_energy_ev: float
    absolute_tolerance_ev: float
    response_tolerance: float


def lateral_gaussian_gap_response_curves(
    photon_energy_ev: ArrayLike,
    mean_gap_ev: float,
    gap_sigma_ev: float,
    thickness_cm: float,
    *,
    exponent: float = 0.5,
    amplitude_cm_inverse_ev_power: float = 1.0,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> LateralResponseCurves:
    """Return exact-mixture and mean-absorption response curves.

    The response convention is single-pass absorptance, ``R=1-T``.  Numerical
    roundoff smaller than the declared tolerance is clipped to preserve the exact
    Jensen ordering; a material violation raises ``RuntimeError``.
    """

    observation = lateral_gaussian_gap_transmission_observation(
        photon_energy_ev,
        mean_gap_ev,
        gap_sigma_ev,
        thickness_cm,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude_cm_inverse_ev_power,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    thickness = _finite_positive("thickness_cm", thickness_cm)

    transmission_response = -np.expm1(observation.log_averaged_transmission)
    closure_response = -np.expm1(
        -thickness * observation.mean_absorption_cm_inverse
    )
    response_excess = closure_response - transmission_response

    tolerance = 2.0e-10
    if np.any(response_excess < -tolerance):
        raise RuntimeError("response curves violate the Jensen ordering")
    response_excess = np.maximum(response_excess, 0.0)

    for name, values in (
        ("transmission response", transmission_response),
        ("mean-absorption response", closure_response),
    ):
        if not np.all(np.isfinite(values)) or np.any(values < -tolerance) or np.any(
            values > 1.0 + tolerance
        ):
            raise RuntimeError(f"{name} left its physical interval")

    return LateralResponseCurves(
        transmission_averaged_response=_read_only_array(
            np.clip(transmission_response, 0.0, 1.0)
        ),
        mean_absorption_closure_response=_read_only_array(
            np.clip(closure_response, 0.0, 1.0)
        ),
        closure_response_excess=_read_only_array(response_excess),
    )


def _bisect_monotone_response(
    evaluate_response,
    *,
    lower_energy_ev: float,
    upper_energy_ev: float,
    target_response: float,
    absolute_tolerance_ev: float,
    response_tolerance: float,
    max_iterations: int,
    label: str,
) -> tuple[float, float, int]:
    left = lower_energy_ev
    right = upper_energy_ev
    left_response = float(evaluate_response(left))
    right_response = float(evaluate_response(right))

    bracket_tolerance = response_tolerance
    if left_response > target_response + bracket_tolerance:
        raise ValueError(f"{label} response already exceeds target at lower bracket")
    if right_response < target_response - bracket_tolerance:
        raise ValueError(f"{label} response does not reach target at upper bracket")
    if abs(left_response - target_response) <= response_tolerance:
        return left, left_response, 0
    if abs(right_response - target_response) <= response_tolerance:
        return right, right_response, 0

    midpoint = 0.5 * (left + right)
    midpoint_response = float(evaluate_response(midpoint))
    for iteration in range(1, max_iterations + 1):
        midpoint = 0.5 * (left + right)
        midpoint_response = float(evaluate_response(midpoint))
        if abs(midpoint_response - target_response) <= response_tolerance:
            return midpoint, midpoint_response, iteration
        if midpoint_response >= target_response:
            right = midpoint
        else:
            left = midpoint
        if 0.5 * (right - left) <= absolute_tolerance_ev:
            midpoint = 0.5 * (left + right)
            midpoint_response = float(evaluate_response(midpoint))
            return midpoint, midpoint_response, iteration

    raise RuntimeError(f"{label} cutoff bisection exceeded max_iterations")


def lateral_gaussian_gap_response_cutoff(
    *,
    mean_gap_ev: float,
    gap_sigma_ev: float,
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
) -> LateralCutoffComparison:
    """Solve both operation-order cutoffs by deterministic bisection.

    The user supplies a common positive-energy bracket.  Both response curves
    must bracket the target.  The returned energy shift is

    ``E_cut,true - E_cut,mean``

    and is non-negative within the bisection tolerance.  The wavelength shift is
    ``lambda_cut,true - lambda_cut,mean`` and has the opposite sign.
    """

    lower = _finite_positive("lower_energy_ev", lower_energy_ev)
    upper = _finite_positive("upper_energy_ev", upper_energy_ev)
    if upper <= lower:
        raise ValueError("upper_energy_ev must exceed lower_energy_ev")
    target = _target_response(target_response)
    energy_tolerance = _finite_positive(
        "absolute_tolerance_ev", absolute_tolerance_ev
    )
    if energy_tolerance >= 0.5 * (upper - lower):
        raise ValueError("absolute_tolerance_ev must resolve the energy bracket")
    response_tol = _finite_positive("response_tolerance", response_tolerance)
    if response_tol >= 1.0:
        raise ValueError("response_tolerance must be less than one")
    iterations = _positive_integer("max_iterations", max_iterations)

    # Validate all local-model and quadrature inputs once before iteration.
    lateral_gaussian_gap_response_curves(
        np.asarray([lower, upper]),
        mean_gap_ev,
        gap_sigma_ev,
        thickness_cm,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude_cm_inverse_ev_power,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )

    def evaluate(energy_ev: float) -> tuple[float, float]:
        curves = lateral_gaussian_gap_response_curves(
            np.asarray([energy_ev]),
            mean_gap_ev,
            gap_sigma_ev,
            thickness_cm,
            exponent=exponent,
            amplitude_cm_inverse_ev_power=amplitude_cm_inverse_ev_power,
            quadrature_order=quadrature_order,
            standard_deviation_limit=standard_deviation_limit,
        )
        return (
            float(curves.transmission_averaged_response[0]),
            float(curves.mean_absorption_closure_response[0]),
        )

    true_energy, true_response, true_iterations = _bisect_monotone_response(
        lambda energy: evaluate(energy)[0],
        lower_energy_ev=lower,
        upper_energy_ev=upper,
        target_response=target,
        absolute_tolerance_ev=energy_tolerance,
        response_tolerance=response_tol,
        max_iterations=iterations,
        label="transmission-averaged",
    )
    closure_energy, closure_response, closure_iterations = _bisect_monotone_response(
        lambda energy: evaluate(energy)[1],
        lower_energy_ev=lower,
        upper_energy_ev=upper,
        target_response=target,
        absolute_tolerance_ev=energy_tolerance,
        response_tolerance=response_tol,
        max_iterations=iterations,
        label="mean-absorption closure",
    )

    energy_shift = true_energy - closure_energy
    ordering_tolerance = 2.0 * energy_tolerance
    if energy_shift < -ordering_tolerance:
        raise RuntimeError("cutoff energies violate the Jensen ordering")
    energy_shift = max(energy_shift, 0.0)

    true_wavelength = cutoff_wavelength_um(true_energy)
    closure_wavelength = cutoff_wavelength_um(closure_energy)
    wavelength_shift = true_wavelength - closure_wavelength
    wavelength_tolerance = (
        2.0
        * energy_tolerance
        * max(true_wavelength / true_energy, closure_wavelength / closure_energy)
    )
    if wavelength_shift > wavelength_tolerance:
        raise RuntimeError("cutoff wavelengths violate the inverse-energy ordering")
    wavelength_shift = min(wavelength_shift, 0.0)

    return LateralCutoffComparison(
        transmission_averaged_energy_ev=float(true_energy),
        mean_absorption_closure_energy_ev=float(closure_energy),
        energy_shift_ev=float(energy_shift),
        transmission_averaged_wavelength_um=float(true_wavelength),
        mean_absorption_closure_wavelength_um=float(closure_wavelength),
        wavelength_shift_um=float(wavelength_shift),
        target_response=target,
        transmission_response_at_cutoff=float(true_response),
        mean_absorption_response_at_cutoff=float(closure_response),
        transmission_response_residual=float(true_response - target),
        mean_absorption_response_residual=float(closure_response - target),
        transmission_iterations=true_iterations,
        mean_absorption_iterations=closure_iterations,
        lower_energy_ev=lower,
        upper_energy_ev=upper,
        absolute_tolerance_ev=energy_tolerance,
        response_tolerance=response_tol,
    )
