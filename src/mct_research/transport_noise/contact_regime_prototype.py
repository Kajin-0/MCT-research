"""Dimensionless contact benchmark utilities."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite


@dataclass(frozen=True)
class ContactRegimePoint:
    label: str
    transfer_number: float
    resistance_ratio: float


@dataclass(frozen=True)
class BarrierRegimePoint:
    reduced_barrier: float
    exchange_attenuation: float


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


def contact_transfer_number(transfer_velocity: float, length: float, diffusivity: float) -> float:
    return _positive("transfer_velocity", transfer_velocity) * _positive("length", length) / _positive("diffusivity", diffusivity)


def contact_resistance_ratio(specific_contact_resistivity: float, bulk_resistivity: float, length: float) -> float:
    return _positive("specific_contact_resistivity", specific_contact_resistivity) / (_positive("bulk_resistivity", bulk_resistivity) * _positive("length", length))


def matched_linear_specific_contact_resistivity(transfer_velocity: float, carrier_density: float, susceptibility_voltage: float, elementary_charge: float = 1.602176634e-19) -> float:
    return _positive("susceptibility_voltage", susceptibility_voltage) / (_positive("elementary_charge", elementary_charge) * _positive("transfer_velocity", transfer_velocity) * _positive("carrier_density", carrier_density))


def matched_linear_bulk_resistivity(mobility: float, carrier_density: float, elementary_charge: float = 1.602176634e-19) -> float:
    return 1.0 / (_positive("elementary_charge", elementary_charge) * _positive("mobility", mobility) * _positive("carrier_density", carrier_density))


def activated_exchange_number(unbarriered_transfer_number: float, reduced_barrier: float) -> float:
    return _positive("unbarriered_transfer_number", unbarriered_transfer_number) * exp(-_nonnegative("reduced_barrier", reduced_barrier))


def classify_transfer_regime(transfer_number: float) -> str:
    gamma = _positive("transfer_number", transfer_number)
    if gamma <= 1.0e-2:
        return "blocking_asymptote"
    if gamma >= 1.0e2:
        return "reservoir_asymptote"
    return "mixed_transfer"


def contact_regime_ladder() -> tuple[ContactRegimePoint, ...]:
    values = (("strongly_blocking", 1.0e-3), ("weak_transfer", 1.0e-1), ("matched", 1.0), ("strong_transfer", 1.0e1), ("reservoir_like", 1.0e3))
    return tuple(ContactRegimePoint(label, gamma, 1.0 / gamma) for label, gamma in values)


def barrier_regime_ladder() -> tuple[BarrierRegimePoint, ...]:
    return tuple(BarrierRegimePoint(beta, exp(-beta)) for beta in (0.0, 0.1, 1.0, 3.0, 10.0))
