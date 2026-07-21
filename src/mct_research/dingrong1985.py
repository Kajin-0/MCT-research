"""Source-faithful carrier-shift reproduction for Dingrong et al. (1985).

The paper reports a finite-temperature Kane density integral for an In-doped
HgCdTe specimen with ``n = 7e17 cm^-3`` and prints ``P = 8e-8 eV cm``.  This
module keeps the printed equation, printed parameter, and tabulated results as
separate objects so source-internal consistency can be tested rather than
silently repaired.

It does not implement the paper's full below-gap free-carrier absorption model,
which depends on external Haga and Tang definitions.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import isfinite, pi, sqrt
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

K_BOLTZMANN_EV_PER_K = 8.617333262145e-5
DINGRONG_ELECTRON_DENSITY_CM3 = 7.0e17
DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM = 8.0e-8


@dataclass(frozen=True)
class DingrongTablePoint:
    """One source-table row and its reproduced carrier result."""

    temperature_k: float
    bandgap_ev: float
    source_fermi_shift_ev: float
    source_fermi_energy_ev: float
    source_optical_gap_ev: float
    reduced_fermi_level: float
    reproduced_fermi_shift_ev: float
    reproduced_fermi_energy_ev: float
    shift_residual_ev: float
    optical_gap_residual_ev: float


@dataclass(frozen=True)
class DingrongTableReproduction:
    """Four-temperature source reproduction and source-consistency metrics."""

    momentum_matrix_ev_cm: float
    points: tuple[DingrongTablePoint, ...]
    shift_rms_error_ev: float
    shift_max_abs_error_ev: float
    optical_gap_rms_error_ev: float
    optical_gap_max_abs_error_ev: float


@dataclass(frozen=True)
class MomentumMatrixAudit:
    """Momentum matrix values implied independently by rounded source rows."""

    row_implied_values_ev_cm: tuple[float, ...]
    mean_ev_cm: float
    sample_standard_deviation_ev_cm: float
    minimum_ev_cm: float
    maximum_ev_cm: float


def _finite_positive(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


@lru_cache(maxsize=None)
def _legendre_rule(order: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    if isinstance(order, bool) or int(order) != order or order < 32:
        raise ValueError("quadrature_order must be an integer >= 32")
    nodes, weights = np.polynomial.legendre.leggauss(int(order))
    return np.asarray(nodes, dtype=float), np.asarray(weights, dtype=float)


def _fermi_occupation(argument: NDArray[np.float64]) -> NDArray[np.float64]:
    result = np.empty_like(argument)
    high = argument > 40.0
    low = argument < -40.0
    middle = ~(high | low)
    result[high] = np.exp(-argument[high])
    result[low] = 1.0
    result[middle] = 1.0 / (1.0 + np.exp(argument[middle]))
    return result


def kane_density_integral(
    reduced_fermi_level: float,
    reduced_gap: float,
    *,
    quadrature_order: int = 256,
) -> float:
    """Evaluate the dimensionless integral printed as Dingrong Eq. (2)."""

    eta = float(reduced_fermi_level)
    phi = _finite_positive(reduced_gap, name="reduced_gap")
    if not isfinite(eta):
        raise ValueError("reduced_fermi_level must be finite")

    nodes, weights = _legendre_rule(quadrature_order)
    upper = max(80.0, eta + 40.0)
    epsilon = 0.5 * upper * (nodes + 1.0)
    occupation = _fermi_occupation(epsilon - eta)
    integrand = (
        np.sqrt(epsilon)
        * np.sqrt(epsilon + phi)
        * (2.0 * epsilon + phi)
        * occupation
    )
    return float(0.5 * upper * np.dot(weights, integrand))


def dingrong_electron_density_cm3(
    *,
    reduced_fermi_level: float,
    temperature_k: float,
    bandgap_ev: float,
    momentum_matrix_ev_cm: float = DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    quadrature_order: int = 256,
) -> float:
    """Return the electron density from the source's finite-T Kane integral."""

    temperature = _finite_positive(temperature_k, name="temperature_k")
    gap = _finite_positive(bandgap_ev, name="bandgap_ev")
    momentum = _finite_positive(
        momentum_matrix_ev_cm,
        name="momentum_matrix_ev_cm",
    )
    thermal_energy = K_BOLTZMANN_EV_PER_K * temperature
    reduced_gap = gap / thermal_energy
    integral = kane_density_integral(
        reduced_fermi_level,
        reduced_gap,
        quadrature_order=quadrature_order,
    )
    prefactor = (
        3.0
        / (4.0 * pi**2)
        * sqrt(3.0 / 2.0)
        * thermal_energy**3
        / momentum**3
    )
    return float(prefactor * integral)


def solve_reduced_fermi_level(
    *,
    electron_density_cm3: float,
    temperature_k: float,
    bandgap_ev: float,
    momentum_matrix_ev_cm: float = DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    quadrature_order: int = 256,
    relative_tolerance: float = 1.0e-12,
) -> float:
    """Invert the monotone source density equation by deterministic bisection."""

    target = _finite_positive(
        electron_density_cm3,
        name="electron_density_cm3",
    )
    tolerance = _finite_positive(relative_tolerance, name="relative_tolerance")
    low = -40.0
    high = 80.0

    def residual(eta: float) -> float:
        return dingrong_electron_density_cm3(
            reduced_fermi_level=eta,
            temperature_k=temperature_k,
            bandgap_ev=bandgap_ev,
            momentum_matrix_ev_cm=momentum_matrix_ev_cm,
            quadrature_order=quadrature_order,
        ) - target

    low_residual = residual(low)
    high_residual = residual(high)
    if low_residual >= 0.0 or high_residual <= 0.0:
        raise RuntimeError("failed to bracket the reduced Fermi level")

    for _ in range(100):
        middle = 0.5 * (low + high)
        middle_residual = residual(middle)
        if abs(middle_residual) <= tolerance * target:
            return float(middle)
        if middle_residual < 0.0:
            low = middle
        else:
            high = middle
    return float(0.5 * (low + high))


def solve_fermi_shift_ev(
    *,
    electron_density_cm3: float,
    temperature_k: float,
    bandgap_ev: float,
    momentum_matrix_ev_cm: float = DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    quadrature_order: int = 256,
) -> float:
    """Return ``Ef-Ec`` in eV from the source density equation."""

    eta = solve_reduced_fermi_level(
        electron_density_cm3=electron_density_cm3,
        temperature_k=temperature_k,
        bandgap_ev=bandgap_ev,
        momentum_matrix_ev_cm=momentum_matrix_ev_cm,
        quadrature_order=quadrature_order,
    )
    return float(eta * K_BOLTZMANN_EV_PER_K * float(temperature_k))


def implied_momentum_matrix_ev_cm(
    *,
    electron_density_cm3: float,
    temperature_k: float,
    bandgap_ev: float,
    fermi_shift_ev: float,
    quadrature_order: int = 256,
) -> float:
    """Return the momentum matrix implied by one tabulated Fermi shift.

    The inversion is exact for the printed density equation because density is
    proportional to ``P^-3`` at fixed reduced Fermi level.
    """

    target = _finite_positive(
        electron_density_cm3,
        name="electron_density_cm3",
    )
    temperature = _finite_positive(temperature_k, name="temperature_k")
    gap = _finite_positive(bandgap_ev, name="bandgap_ev")
    shift = _finite_positive(fermi_shift_ev, name="fermi_shift_ev")
    thermal_energy = K_BOLTZMANN_EV_PER_K * temperature
    eta = shift / thermal_energy
    phi = gap / thermal_energy
    integral = kane_density_integral(
        eta,
        phi,
        quadrature_order=quadrature_order,
    )
    numerator = (
        3.0
        / (4.0 * pi**2)
        * sqrt(3.0 / 2.0)
        * thermal_energy**3
        * integral
    )
    return float((numerator / target) ** (1.0 / 3.0))


def audit_momentum_matrix(
    *,
    temperatures_k: Sequence[float],
    bandgaps_ev: Sequence[float],
    source_fermi_shifts_ev: Sequence[float],
    electron_density_cm3: float = DINGRONG_ELECTRON_DENSITY_CM3,
    quadrature_order: int = 256,
) -> MomentumMatrixAudit:
    """Return row-wise momentum matrices implied by a rounded source table."""

    if not (
        len(temperatures_k)
        == len(bandgaps_ev)
        == len(source_fermi_shifts_ev)
        and len(temperatures_k) > 1
    ):
        raise ValueError("source sequences must have equal length greater than one")
    values = np.asarray(
        [
            implied_momentum_matrix_ev_cm(
                electron_density_cm3=electron_density_cm3,
                temperature_k=temperature,
                bandgap_ev=gap,
                fermi_shift_ev=shift,
                quadrature_order=quadrature_order,
            )
            for temperature, gap, shift in zip(
                temperatures_k,
                bandgaps_ev,
                source_fermi_shifts_ev,
                strict=True,
            )
        ],
        dtype=float,
    )
    return MomentumMatrixAudit(
        row_implied_values_ev_cm=tuple(float(value) for value in values),
        mean_ev_cm=float(np.mean(values)),
        sample_standard_deviation_ev_cm=float(np.std(values, ddof=1)),
        minimum_ev_cm=float(np.min(values)),
        maximum_ev_cm=float(np.max(values)),
    )


def reproduce_table(
    *,
    temperatures_k: Sequence[float],
    bandgaps_ev: Sequence[float],
    source_fermi_shifts_ev: Sequence[float],
    source_fermi_energies_ev: Sequence[float],
    source_optical_gaps_ev: Sequence[float],
    momentum_matrix_ev_cm: float,
    electron_density_cm3: float = DINGRONG_ELECTRON_DENSITY_CM3,
    quadrature_order: int = 256,
) -> DingrongTableReproduction:
    """Reproduce all source rows for one declared momentum matrix value."""

    lengths = {
        len(temperatures_k),
        len(bandgaps_ev),
        len(source_fermi_shifts_ev),
        len(source_fermi_energies_ev),
        len(source_optical_gaps_ev),
    }
    if len(lengths) != 1 or next(iter(lengths)) == 0:
        raise ValueError("all source sequences must have one common nonzero length")

    points: list[DingrongTablePoint] = []
    for temperature, gap, source_shift, source_energy, optical_gap in zip(
        temperatures_k,
        bandgaps_ev,
        source_fermi_shifts_ev,
        source_fermi_energies_ev,
        source_optical_gaps_ev,
        strict=True,
    ):
        eta = solve_reduced_fermi_level(
            electron_density_cm3=electron_density_cm3,
            temperature_k=temperature,
            bandgap_ev=gap,
            momentum_matrix_ev_cm=momentum_matrix_ev_cm,
            quadrature_order=quadrature_order,
        )
        reproduced_shift = eta * K_BOLTZMANN_EV_PER_K * float(temperature)
        reproduced_energy = float(gap) + reproduced_shift
        points.append(
            DingrongTablePoint(
                temperature_k=float(temperature),
                bandgap_ev=float(gap),
                source_fermi_shift_ev=float(source_shift),
                source_fermi_energy_ev=float(source_energy),
                source_optical_gap_ev=float(optical_gap),
                reduced_fermi_level=float(eta),
                reproduced_fermi_shift_ev=float(reproduced_shift),
                reproduced_fermi_energy_ev=float(reproduced_energy),
                shift_residual_ev=float(reproduced_shift - float(source_shift)),
                optical_gap_residual_ev=float(reproduced_energy - float(optical_gap)),
            )
        )

    shift_residuals = np.asarray([point.shift_residual_ev for point in points])
    optical_residuals = np.asarray(
        [point.optical_gap_residual_ev for point in points]
    )
    return DingrongTableReproduction(
        momentum_matrix_ev_cm=float(momentum_matrix_ev_cm),
        points=tuple(points),
        shift_rms_error_ev=float(np.sqrt(np.mean(shift_residuals**2))),
        shift_max_abs_error_ev=float(np.max(np.abs(shift_residuals))),
        optical_gap_rms_error_ev=float(np.sqrt(np.mean(optical_residuals**2))),
        optical_gap_max_abs_error_ev=float(np.max(np.abs(optical_residuals))),
    )
