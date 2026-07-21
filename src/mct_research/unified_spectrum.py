"""Unified distributional, carrier-shift, and detector-response spectrum.

This module composes the controlled Gaussian local-gap convolution with a
spatially uniform carrier-induced edge translation and a single-pass
Beer-Lambert response. It is designed to expose exact parameter invariances.
It is not a complete microscopic HgCdTe spectrum.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .detector_cutoff import single_pass_absorptance
from .spectral_convolution import gaussian_gap_convolved_power_absorption


@dataclass(frozen=True)
class UnifiedSpectrumJacobianDiagnostics:
    """Local rank diagnostics for one dense response spectrum."""

    photon_energy_ev: NDArray[np.float64]
    response: NDArray[np.float64]
    parameter_names: tuple[str, ...]
    jacobian: NDArray[np.float64]
    singular_values: NDArray[np.float64]
    relative_singular_values: NDArray[np.float64]
    numerical_rank: int
    condition_number: float
    carrier_marker_scale_cm_inverse_per_ev: float


def _finite_positive(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def _finite_nonnegative(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return number


def unified_response_spectrum(
    photon_energy_ev: ArrayLike,
    *,
    zero_density_gap_ev: float,
    uniform_carrier_shift_ev: float,
    gap_sigma_ev: float,
    intrinsic_exponent: float,
    absorption_amplitude_cm_inverse_ev_power: float,
    effective_thickness_um: float,
    carrier_marker_scale_cm_inverse_per_ev: float = 0.0,
    carrier_marker_reference_energy_ev: float = 0.1,
    quadrature_order: int = 256,
) -> NDArray[np.float64]:
    """Return a controlled single-state optical response spectrum.

    The local-gap mean is

    ``mu_G = zero_density_gap_ev + uniform_carrier_shift_ev``.

    The optional marker is a deliberately generic non-translational carrier
    term,

    ``alpha_marker = B * Delta_carrier * (E_ref/E)^2``.

    It demonstrates how independently calibrated carrier-dependent spectral
    structure can break the gap/carrier translation degeneracy. It is not the
    Dingrong free-carrier absorption model.
    """

    energy = np.asarray(photon_energy_ev, dtype=float)
    if energy.ndim != 1 or energy.size < 2:
        raise ValueError("photon_energy_ev must be a one-dimensional array")
    if not np.all(np.isfinite(energy)) or np.any(energy <= 0.0):
        raise ValueError("photon_energy_ev must be finite and positive")
    if np.any(np.diff(energy) <= 0.0):
        raise ValueError("photon_energy_ev must be strictly increasing")

    gap = float(zero_density_gap_ev)
    shift = float(uniform_carrier_shift_ev)
    if not isfinite(gap):
        raise ValueError("zero_density_gap_ev must be finite")
    if not isfinite(shift):
        raise ValueError("uniform_carrier_shift_ev must be finite")
    sigma = _finite_positive(gap_sigma_ev, name="gap_sigma_ev")
    exponent = _finite_nonnegative(intrinsic_exponent, name="intrinsic_exponent")
    amplitude = _finite_positive(
        absorption_amplitude_cm_inverse_ev_power,
        name="absorption_amplitude_cm_inverse_ev_power",
    )
    thickness = _finite_positive(
        effective_thickness_um,
        name="effective_thickness_um",
    )
    marker_scale = _finite_nonnegative(
        carrier_marker_scale_cm_inverse_per_ev,
        name="carrier_marker_scale_cm_inverse_per_ev",
    )
    marker_reference = _finite_positive(
        carrier_marker_reference_energy_ev,
        name="carrier_marker_reference_energy_ev",
    )
    if marker_scale > 0.0 and shift < 0.0:
        raise ValueError(
            "uniform_carrier_shift_ev must be non-negative when the marker is enabled"
        )

    mean_gap = gap + shift
    absorption = gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude,
        quadrature_order=quadrature_order,
    )
    if marker_scale > 0.0:
        absorption = absorption + (
            marker_scale * shift * (marker_reference / energy) ** 2
        )

    return single_pass_absorptance(absorption, thickness)


def unified_spectrum_jacobian(
    photon_energy_ev: ArrayLike,
    *,
    zero_density_gap_ev: float,
    uniform_carrier_shift_ev: float,
    gap_sigma_ev: float,
    intrinsic_exponent: float,
    absorption_amplitude_cm_inverse_ev_power: float,
    effective_thickness_um: float,
    carrier_marker_scale_cm_inverse_per_ev: float = 0.0,
    carrier_marker_reference_energy_ev: float = 0.1,
    energy_step_ev: float = 1.0e-6,
    relative_step: float = 1.0e-5,
    relative_rank_tolerance: float = 1.0e-8,
    quadrature_order: int = 256,
) -> UnifiedSpectrumJacobianDiagnostics:
    """Return a Jacobian for ``(Eg0, Delta_carrier, ln sigma, ln A, ln d)``."""

    energy = np.asarray(photon_energy_ev, dtype=float)
    energy_step = _finite_positive(energy_step_ev, name="energy_step_ev")
    log_step = _finite_positive(relative_step, name="relative_step")
    rank_tolerance = _finite_positive(
        relative_rank_tolerance,
        name="relative_rank_tolerance",
    )
    marker_scale = _finite_nonnegative(
        carrier_marker_scale_cm_inverse_per_ev,
        name="carrier_marker_scale_cm_inverse_per_ev",
    )

    gap = float(zero_density_gap_ev)
    shift = float(uniform_carrier_shift_ev)
    if not isfinite(gap):
        raise ValueError("zero_density_gap_ev must be finite")
    if not isfinite(shift):
        raise ValueError("uniform_carrier_shift_ev must be finite")
    sigma = _finite_positive(gap_sigma_ev, name="gap_sigma_ev")
    amplitude = _finite_positive(
        absorption_amplitude_cm_inverse_ev_power,
        name="absorption_amplitude_cm_inverse_ev_power",
    )
    thickness = _finite_positive(
        effective_thickness_um,
        name="effective_thickness_um",
    )

    parameters = np.asarray(
        [gap, shift, log(sigma), log(amplitude), log(thickness)],
        dtype=float,
    )
    steps = np.asarray(
        [energy_step, energy_step, log_step, log_step, log_step],
        dtype=float,
    )

    def evaluate(values: NDArray[np.float64]) -> NDArray[np.float64]:
        return unified_response_spectrum(
            energy,
            zero_density_gap_ev=float(values[0]),
            uniform_carrier_shift_ev=float(values[1]),
            gap_sigma_ev=float(np.exp(values[2])),
            intrinsic_exponent=intrinsic_exponent,
            absorption_amplitude_cm_inverse_ev_power=float(np.exp(values[3])),
            effective_thickness_um=float(np.exp(values[4])),
            carrier_marker_scale_cm_inverse_per_ev=marker_scale,
            carrier_marker_reference_energy_ev=carrier_marker_reference_energy_ev,
            quadrature_order=quadrature_order,
        )

    base_response = evaluate(parameters)
    jacobian = np.empty((energy.size, parameters.size), dtype=float)
    for column, step in enumerate(steps):
        plus = parameters.copy()
        minus = parameters.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (evaluate(plus) - evaluate(minus)) / (2.0 * step)

    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    if singular_values.size == 0 or singular_values[0] == 0.0:
        relative = np.zeros_like(singular_values)
        rank = 0
        condition = float("inf")
    else:
        relative = singular_values / singular_values[0]
        rank = int(np.count_nonzero(relative > rank_tolerance))
        condition = (
            float(singular_values[0] / singular_values[-1])
            if singular_values[-1] > 0.0
            else float("inf")
        )

    return UnifiedSpectrumJacobianDiagnostics(
        photon_energy_ev=np.asarray(energy, dtype=float),
        response=base_response,
        parameter_names=(
            "zero_density_gap_ev",
            "uniform_carrier_shift_ev",
            "ln_gap_sigma",
            "ln_absorption_amplitude",
            "ln_effective_thickness",
        ),
        jacobian=jacobian,
        singular_values=np.asarray(singular_values, dtype=float),
        relative_singular_values=np.asarray(relative, dtype=float),
        numerical_rank=rank,
        condition_number=condition,
        carrier_marker_scale_cm_inverse_per_ev=marker_scale,
    )
