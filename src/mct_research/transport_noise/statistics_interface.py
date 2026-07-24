"""Source-independent carrier-statistics interface for R06 Phase 1C.

The historical Madarasz/Lowney HgCdTe equation sets are not available at
symbol-exact implementation quality.  This module therefore defines the
thermodynamic quantities that any future statistics closure must provide
without claiming to reproduce those papers.  A parabolic Fermi-Dirac closure
is supplied only as a mathematical benchmark.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Protocol, runtime_checkable

from .statistics_prototype import BOLTZMANN_EV_PER_K, normalized_fermi_dirac


@dataclass(frozen=True)
class CarrierStatisticsState:
    """Density and thermodynamic response from one carrier closure evaluation.

    ``compressibility_cm3_per_ev`` is the positive derivative of carrier
    density with respect to the carrier chemical potential.  For holes it is
    the magnitude of the derivative with respect to the electron chemical
    potential; the charge sign is applied by the electrostatic assembly.
    """

    eta: float
    temperature_k: float
    density_scale_cm3: float
    normalized_density: float
    normalized_compressibility: float
    density_cm3: float
    compressibility_cm3_per_ev: float
    generalized_einstein_factor: float

    def __post_init__(self) -> None:
        values = (
            self.eta,
            self.temperature_k,
            self.density_scale_cm3,
            self.normalized_density,
            self.normalized_compressibility,
            self.density_cm3,
            self.compressibility_cm3_per_ev,
            self.generalized_einstein_factor,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("statistics state values must be finite")
        if self.temperature_k <= 0.0:
            raise ValueError("temperature_k must be positive")
        if self.density_scale_cm3 <= 0.0:
            raise ValueError("density_scale_cm3 must be positive")
        if self.normalized_density <= 0.0:
            raise ValueError("normalized_density must be positive")
        if self.normalized_compressibility <= 0.0:
            raise ValueError("normalized_compressibility must be positive")
        if self.density_cm3 <= 0.0:
            raise ValueError("density_cm3 must be positive")
        if self.compressibility_cm3_per_ev <= 0.0:
            raise ValueError("compressibility_cm3_per_ev must be positive")
        if self.generalized_einstein_factor <= 0.0:
            raise ValueError("generalized_einstein_factor must be positive")

    @property
    def thermal_energy_ev(self) -> float:
        """Return ``k_B T`` in electronvolts."""

        return BOLTZMANN_EV_PER_K * self.temperature_k

    @property
    def thermodynamic_einstein_ratio(self) -> float:
        r"""Return ``n / (k_B T * dn/dmu)``.

        A self-consistent closure must make this equal to
        ``generalized_einstein_factor`` up to numerical error.
        """

        return self.density_cm3 / (
            self.thermal_energy_ev * self.compressibility_cm3_per_ev
        )


@runtime_checkable
class CarrierStatisticsClosure(Protocol):
    """Protocol required by the deterministic and later stochastic solvers."""

    def evaluate(self, *, eta: float, temperature_k: float) -> CarrierStatisticsState:
        """Evaluate density and susceptibility at one reduced chemical potential."""


@dataclass(frozen=True)
class ParabolicFermiClosure:
    """Fixed-density-scale parabolic Fermi-Dirac benchmark closure.

    The density scale is supplied explicitly.  This class is not an HgCdTe
    density-of-states model and is not authorized for material prediction.
    """

    density_scale_cm3: float

    def __post_init__(self) -> None:
        scale = float(self.density_scale_cm3)
        if not isfinite(scale) or scale <= 0.0:
            raise ValueError("density_scale_cm3 must be finite and positive")
        object.__setattr__(self, "density_scale_cm3", scale)

    def evaluate(self, *, eta: float, temperature_k: float) -> CarrierStatisticsState:
        return evaluate_parabolic_carrier_statistics(
            eta=eta,
            temperature_k=temperature_k,
            density_scale_cm3=self.density_scale_cm3,
        )


@dataclass(frozen=True)
class BipolarStatisticsState:
    """Electron and hole statistics evaluated at a common temperature."""

    electron: CarrierStatisticsState
    hole: CarrierStatisticsState

    def __post_init__(self) -> None:
        if abs(self.electron.temperature_k - self.hole.temperature_k) > 1.0e-12:
            raise ValueError("electron and hole statistics must share one temperature")

    @property
    def net_charge_number_density_cm3(self) -> float:
        """Return the carrier part of ``p-n`` in number-density units."""

        return self.hole.density_cm3 - self.electron.density_cm3

    @property
    def charge_compressibility_cm3_per_ev(self) -> float:
        """Return the positive electron-plus-hole charge susceptibility scale."""

        return (
            self.electron.compressibility_cm3_per_ev
            + self.hole.compressibility_cm3_per_ev
        )


def _finite_positive(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def evaluate_parabolic_carrier_statistics(
    *,
    eta: float,
    temperature_k: float,
    density_scale_cm3: float,
) -> CarrierStatisticsState:
    r"""Evaluate the parabolic Fermi benchmark and its susceptibility.

    With the normalized complete Fermi-Dirac convention used by R06,

    .. math::

        n=N_*\mathcal F_{1/2}(\eta),
        \qquad
        \frac{\partial n}{\partial\mu}
        =\frac{N_*}{k_BT}\mathcal F_{-1/2}(\eta),

    and therefore

    .. math::

        \Theta=\frac{n}{k_BT\,\partial n/\partial\mu}
        =\frac{\mathcal F_{1/2}}{\mathcal F_{-1/2}}.
    """

    eta_value = float(eta)
    if not isfinite(eta_value):
        raise ValueError("eta must be finite")
    temperature = _finite_positive(temperature_k, name="temperature_k")
    scale = _finite_positive(density_scale_cm3, name="density_scale_cm3")
    fermi_half = float(normalized_fermi_dirac(0.5, eta_value))
    fermi_minus_half = float(normalized_fermi_dirac(-0.5, eta_value))
    thermal_energy = BOLTZMANN_EV_PER_K * temperature
    density = scale * fermi_half
    compressibility = scale * fermi_minus_half / thermal_energy
    return CarrierStatisticsState(
        eta=eta_value,
        temperature_k=temperature,
        density_scale_cm3=scale,
        normalized_density=fermi_half,
        normalized_compressibility=fermi_minus_half,
        density_cm3=density,
        compressibility_cm3_per_ev=compressibility,
        generalized_einstein_factor=fermi_half / fermi_minus_half,
    )


def evaluate_parabolic_bipolar_statistics(
    *,
    electron_eta: float,
    hole_eta: float,
    temperature_k: float,
    electron_density_scale_cm3: float,
    hole_density_scale_cm3: float,
) -> BipolarStatisticsState:
    """Evaluate the benchmark electron and hole closures at one temperature."""

    return BipolarStatisticsState(
        electron=evaluate_parabolic_carrier_statistics(
            eta=electron_eta,
            temperature_k=temperature_k,
            density_scale_cm3=electron_density_scale_cm3,
        ),
        hole=evaluate_parabolic_carrier_statistics(
            eta=hole_eta,
            temperature_k=temperature_k,
            density_scale_cm3=hole_density_scale_cm3,
        ),
    )


def thermodynamic_identity_relative_error(state: CarrierStatisticsState) -> float:
    """Return the relative mismatch in the generalized Einstein identity."""

    expected = state.generalized_einstein_factor
    return abs(state.thermodynamic_einstein_ratio - expected) / expected
