"""Degenerate carrier-filling operators for HgCdTe optical edges.

This module implements a deliberately declared zero-temperature spherical-band
model. It separates the latent zero-density gap, conduction-band filling,
valence-band recoil, and an optional density-scaled band-gap-renormalization
term. It does not implement the full Dingrong free-carrier absorption theory,
finite-temperature Fermi integrals, anisotropy, many-valley structure, or a
production HgCdTe band model.

Densities are supplied in cm^-3, masses as ratios to the free-electron mass,
wavevectors are returned in inverse angstrom, and energies are in electron volts.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite, log, pi, sqrt

import numpy as np
from numpy.typing import NDArray

# CODATA-compatible value of hbar^2/(2*m0) in eV A^2.
HBAR2_OVER_2M0_EV_A2 = 3.80998211615486


@dataclass(frozen=True)
class CarrierFilledEdge:
    """One zero-temperature carrier-filled direct-transition estimate."""

    electron_density_cm3: float
    valley_degeneracy: float
    fermi_wavevector_inverse_angstrom: float
    parabolic_conduction_energy_ev: float
    nonparabolic_conduction_energy_ev: float
    valence_recoil_energy_ev: float
    burstein_moss_shift_ev: float
    bandgap_renormalization_ev: float
    observation_shift_ev: float
    zero_density_gap_ev: float
    optical_edge_ev: float
    parabolic_burstein_moss_shift_ev: float
    parabolic_overestimate_ev: float
    nonparabolicity_parameter: float


@dataclass(frozen=True)
class CarrierEdgeJacobianDiagnostics:
    """Local identifiability diagnostics for a density-series edge model."""

    electron_densities_cm3: NDArray[np.float64]
    optical_edges_ev: NDArray[np.float64]
    parameter_names: tuple[str, ...]
    jacobian: NDArray[np.float64]
    singular_values: NDArray[np.float64]
    relative_singular_values: NDArray[np.float64]
    numerical_rank: int
    condition_number: float


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


def fermi_wavevector_inverse_angstrom(
    electron_density_cm3: float,
    *,
    valley_degeneracy: float = 1.0,
) -> float:
    """Return the zero-temperature Fermi wavevector for spherical valleys.

    The density relation includes spin degeneracy inside
    ``n = g_v*k_F^3/(3*pi^2)``. ``valley_degeneracy`` therefore counts
    equivalent valleys only.
    """

    density = _finite_positive(
        electron_density_cm3,
        name="electron_density_cm3",
    )
    degeneracy = _finite_positive(
        valley_degeneracy,
        name="valley_degeneracy",
    )
    density_inverse_angstrom_cubed = density * 1.0e-24
    return float((3.0 * pi**2 * density_inverse_angstrom_cubed / degeneracy) ** (1.0 / 3.0))


def parabolic_kinetic_energy_ev(
    fermi_wavevector_inverse_angstrom: float,
    effective_mass_ratio: float,
) -> float:
    """Return ``hbar^2*k^2/(2*m*)`` in eV."""

    wavevector = _finite_nonnegative(
        fermi_wavevector_inverse_angstrom,
        name="fermi_wavevector_inverse_angstrom",
    )
    mass_ratio = _finite_positive(
        effective_mass_ratio,
        name="effective_mass_ratio",
    )
    return float(HBAR2_OVER_2M0_EV_A2 * wavevector**2 / mass_ratio)


def kane_nonparabolic_energy_ev_from_parabolic(
    parabolic_energy_ev: float,
    nonparabolicity_ev_inverse: float,
) -> float:
    """Solve ``E*(1+alpha*E)=E_par`` for the positive energy branch."""

    parabolic_energy = _finite_nonnegative(
        parabolic_energy_ev,
        name="parabolic_energy_ev",
    )
    alpha = _finite_nonnegative(
        nonparabolicity_ev_inverse,
        name="nonparabolicity_ev_inverse",
    )
    if alpha == 0.0 or parabolic_energy == 0.0:
        return parabolic_energy

    # The rationalized form avoids cancellation when alpha*E_par is small.
    return float(
        2.0 * parabolic_energy
        / (1.0 + sqrt(1.0 + 4.0 * alpha * parabolic_energy))
    )


def density_scaled_bandgap_renormalization_ev(
    electron_density_cm3: float,
    coefficient_ev_at_1e18_cm3: float,
) -> float:
    """Return a negative ``n^(1/3)`` gap-renormalization contribution.

    ``coefficient_ev_at_1e18_cm3`` is a positive magnitude. The returned shift
    is negative. This is a sensitivity basis, not a universal HgCdTe law.
    """

    density = _finite_positive(
        electron_density_cm3,
        name="electron_density_cm3",
    )
    coefficient = _finite_nonnegative(
        coefficient_ev_at_1e18_cm3,
        name="coefficient_ev_at_1e18_cm3",
    )
    return float(-coefficient * (density / 1.0e18) ** (1.0 / 3.0))


def carrier_filled_optical_edge_ev(
    *,
    zero_density_gap_ev: float,
    electron_density_cm3: float,
    conduction_edge_mass_ratio: float,
    nonparabolicity_ev_inverse: float,
    valence_mass_ratio: float,
    valley_degeneracy: float = 1.0,
    bandgap_renormalization_ev: float = 0.0,
    observation_shift_ev: float = 0.0,
) -> CarrierFilledEdge:
    """Return a zero-temperature direct-transition filling estimate.

    The model assumes a Kane-type nonparabolic conduction branch,

    ``E_c*(1+alpha*E_c)=hbar^2*k_F^2/(2*m_edge)``,

    and a parabolic valence recoil at the same vertical-transition wavevector.
    The many-body and observation shifts are supplied independently and are not
    inferred inside this function.
    """

    gap = float(zero_density_gap_ev)
    bgr = float(bandgap_renormalization_ev)
    observation = float(observation_shift_ev)
    if not isfinite(gap):
        raise ValueError("zero_density_gap_ev must be finite")
    if not isfinite(bgr):
        raise ValueError("bandgap_renormalization_ev must be finite")
    if not isfinite(observation):
        raise ValueError("observation_shift_ev must be finite")

    alpha = _finite_nonnegative(
        nonparabolicity_ev_inverse,
        name="nonparabolicity_ev_inverse",
    )
    density = _finite_positive(
        electron_density_cm3,
        name="electron_density_cm3",
    )
    degeneracy = _finite_positive(
        valley_degeneracy,
        name="valley_degeneracy",
    )
    conduction_mass = _finite_positive(
        conduction_edge_mass_ratio,
        name="conduction_edge_mass_ratio",
    )
    valence_mass = _finite_positive(
        valence_mass_ratio,
        name="valence_mass_ratio",
    )

    wavevector = fermi_wavevector_inverse_angstrom(
        density,
        valley_degeneracy=degeneracy,
    )
    conduction_parabolic = parabolic_kinetic_energy_ev(
        wavevector,
        conduction_mass,
    )
    conduction_nonparabolic = kane_nonparabolic_energy_ev_from_parabolic(
        conduction_parabolic,
        alpha,
    )
    valence_recoil = parabolic_kinetic_energy_ev(wavevector, valence_mass)
    filling_shift = conduction_nonparabolic + valence_recoil
    parabolic_shift = conduction_parabolic + valence_recoil
    optical_edge = gap + filling_shift + bgr + observation

    return CarrierFilledEdge(
        electron_density_cm3=density,
        valley_degeneracy=degeneracy,
        fermi_wavevector_inverse_angstrom=wavevector,
        parabolic_conduction_energy_ev=conduction_parabolic,
        nonparabolic_conduction_energy_ev=conduction_nonparabolic,
        valence_recoil_energy_ev=valence_recoil,
        burstein_moss_shift_ev=filling_shift,
        bandgap_renormalization_ev=bgr,
        observation_shift_ev=observation,
        zero_density_gap_ev=gap,
        optical_edge_ev=optical_edge,
        parabolic_burstein_moss_shift_ev=parabolic_shift,
        parabolic_overestimate_ev=parabolic_shift - filling_shift,
        nonparabolicity_parameter=alpha * conduction_parabolic,
    )


def carrier_edge_density_series_jacobian(
    *,
    electron_densities_cm3: Sequence[float],
    zero_density_gap_ev: float,
    conduction_edge_mass_ratio: float,
    nonparabolicity_ev_inverse: float,
    valence_mass_ratio: float,
    bgr_coefficient_ev_at_1e18_cm3: float,
    valley_degeneracy: float = 1.0,
    relative_step: float = 1.0e-5,
    relative_rank_tolerance: float = 1.0e-8,
) -> CarrierEdgeJacobianDiagnostics:
    """Return a log-parameter Jacobian for a carrier-density edge series.

    The parameter vector is

    ``(ln Eg, ln m_edge, ln alpha, ln m_valence, ln C_BGR)``.

    All five reference values must be positive. This is an identifiability
    diagnostic for a declared positive-gap, positive-renormalization-magnitude
    regime; it is not a general signed-gap fit API.
    """

    if len(electron_densities_cm3) == 0:
        raise ValueError("electron_densities_cm3 must not be empty")
    densities = np.asarray(
        [
            _finite_positive(value, name="electron density")
            for value in electron_densities_cm3
        ],
        dtype=float,
    )
    if np.unique(densities).size != densities.size:
        raise ValueError("electron_densities_cm3 must be unique")

    degeneracy = _finite_positive(
        valley_degeneracy,
        name="valley_degeneracy",
    )
    step = _finite_positive(relative_step, name="relative_step")
    rank_tolerance = _finite_positive(
        relative_rank_tolerance,
        name="relative_rank_tolerance",
    )
    parameter_values = np.asarray(
        [
            _finite_positive(zero_density_gap_ev, name="zero_density_gap_ev"),
            _finite_positive(
                conduction_edge_mass_ratio,
                name="conduction_edge_mass_ratio",
            ),
            _finite_positive(
                nonparabolicity_ev_inverse,
                name="nonparabolicity_ev_inverse",
            ),
            _finite_positive(valence_mass_ratio, name="valence_mass_ratio"),
            _finite_positive(
                bgr_coefficient_ev_at_1e18_cm3,
                name="bgr_coefficient_ev_at_1e18_cm3",
            ),
        ],
        dtype=float,
    )
    log_parameters = np.log(parameter_values)

    def evaluate(log_values: NDArray[np.float64]) -> NDArray[np.float64]:
        gap, conduction_mass, alpha, valence_mass, bgr_coefficient = np.exp(
            log_values
        )
        edges: list[float] = []
        for density in densities:
            bgr = density_scaled_bandgap_renormalization_ev(
                float(density),
                float(bgr_coefficient),
            )
            result = carrier_filled_optical_edge_ev(
                zero_density_gap_ev=float(gap),
                electron_density_cm3=float(density),
                conduction_edge_mass_ratio=float(conduction_mass),
                nonparabolicity_ev_inverse=float(alpha),
                valence_mass_ratio=float(valence_mass),
                valley_degeneracy=degeneracy,
                bandgap_renormalization_ev=bgr,
            )
            edges.append(result.optical_edge_ev)
        return np.asarray(edges, dtype=float)

    base_edges = evaluate(log_parameters)
    jacobian = np.empty((densities.size, log_parameters.size), dtype=float)
    for column in range(log_parameters.size):
        plus = log_parameters.copy()
        minus = log_parameters.copy()
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
            if singular_values.size == log_parameters.size
            and singular_values[-1] > 0.0
            else float("inf")
        )

    return CarrierEdgeJacobianDiagnostics(
        electron_densities_cm3=densities,
        optical_edges_ev=base_edges,
        parameter_names=(
            "ln_zero_density_gap",
            "ln_conduction_edge_mass",
            "ln_nonparabolicity",
            "ln_valence_mass",
            "ln_bgr_coefficient",
        ),
        jacobian=jacobian,
        singular_values=np.asarray(singular_values, dtype=float),
        relative_singular_values=np.asarray(relative, dtype=float),
        numerical_rank=rank,
        condition_number=condition,
    )
