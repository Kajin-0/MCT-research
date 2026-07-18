#!/usr/bin/env python3
"""Audit short-range and long-range polar consistency of the CdTe A0 response.

This is a zero-compute post-processing gate. It combines the stricter-response
record with bounded experimental/literature anchors and evaluates whether the
same PBE/DFPT point can support short-range Gamma optical planning and/or the
long-range polar part of an electron-phonon calculation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

ELEMENTARY_CHARGE_C = 1.602176634e-19
VACUUM_PERMITTIVITY_F_M = 8.8541878128e-12
ATOMIC_MASS_KG = 1.66053906660e-27
SPEED_OF_LIGHT_M_S = 299792458.0


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def primitive_volume_m3(lattice_angstrom: float) -> float:
    if lattice_angstrom <= 0.0:
        raise ValueError("lattice constant must be positive")
    return (lattice_angstrom * 1.0e-10) ** 3 / 4.0


def reduced_mass_kg(mass_a_u: float, mass_b_u: float) -> float:
    if mass_a_u <= 0.0 or mass_b_u <= 0.0:
        raise ValueError("atomic masses must be positive")
    mass_a = mass_a_u * ATOMIC_MASS_KG
    mass_b = mass_b_u * ATOMIC_MASS_KG
    return mass_a * mass_b / (mass_a + mass_b)


def angular_frequency_s1(wavenumber_cm1: float) -> float:
    if wavenumber_cm1 < 0.0:
        raise ValueError("wavenumber must be nonnegative")
    return 2.0 * math.pi * SPEED_OF_LIGHT_M_S * 100.0 * wavenumber_cm1


def infer_born_charge_magnitude(
    *,
    to_cm1: float,
    lo_cm1: float,
    epsilon_infinity: float,
    volume_m3: float,
    reduced_mass: float,
) -> float:
    """Infer |Z*| from zincblende LO-TO splitting in SI units."""
    if lo_cm1 <= to_cm1:
        raise ValueError("LO frequency must exceed TO frequency")
    if epsilon_infinity <= 0.0 or volume_m3 <= 0.0 or reduced_mass <= 0.0:
        raise ValueError("dielectric constant, volume, and mass must be positive")
    delta_omega2 = angular_frequency_s1(lo_cm1) ** 2 - angular_frequency_s1(to_cm1) ** 2
    numerator = (
        delta_omega2
        * VACUUM_PERMITTIVITY_F_M
        * epsilon_infinity
        * volume_m3
        * reduced_mass
    )
    return math.sqrt(numerator / ELEMENTARY_CHARGE_C**2)


def predict_lo_frequency_cm1(
    *,
    to_cm1: float,
    born_charge_magnitude: float,
    epsilon_infinity: float,
    volume_m3: float,
    reduced_mass: float,
) -> float:
    if born_charge_magnitude < 0.0:
        raise ValueError("Born-charge magnitude must be nonnegative")
    if epsilon_infinity <= 0.0 or volume_m3 <= 0.0 or reduced_mass <= 0.0:
        raise ValueError("dielectric constant, volume, and mass must be positive")
    delta_omega2 = (
        ELEMENTARY_CHARGE_C**2
        * born_charge_magnitude**2
        / (VACUUM_PERMITTIVITY_F_M * epsilon_infinity * volume_m3 * reduced_mass)
    )
    omega_lo = math.sqrt(angular_frequency_s1(to_cm1) ** 2 + delta_omega2)
    return omega_lo / (2.0 * math.pi * SPEED_OF_LIGHT_M_S * 100.0)


def _relative_error(value: float, reference: float) -> float:
    if reference == 0.0:
        raise ValueError("relative-error reference must be nonzero")
    return abs(value - reference) / abs(reference)


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("stage") != "cdte_a0_polar_response_consistency":
        raise ValueError("unexpected polar-response contract stage")

    calculation = contract["calculation"]
    anchor = contract["literature_anchor"]
    thresholds = contract["thresholds"]

    volume = primitive_volume_m3(float(calculation["lattice_angstrom"]))
    mu = reduced_mass_kg(
        float(anchor["cadmium_atomic_mass_u"]),
        float(anchor["tellurium_atomic_mass_u"]),
    )
    reference_zstar = infer_born_charge_magnitude(
        to_cm1=float(anchor["to_frequency_cm1"]),
        lo_cm1=float(anchor["lo_frequency_cm1"]),
        epsilon_infinity=float(anchor["epsilon_infinity"]),
        volume_m3=volume,
        reduced_mass=mu,
    )
    calculated_lo = predict_lo_frequency_cm1(
        to_cm1=float(calculation["simple_asr_to_frequency_cm1"]),
        born_charge_magnitude=float(calculation["asr_corrected_born_charge_magnitude_e"]),
        epsilon_infinity=float(calculation["epsilon_infinity"]),
        volume_m3=volume,
        reduced_mass=mu,
    )

    gap_ratio = float(calculation["direct_gamma_gap_ev"]) / float(anchor["direct_gap_ev"])
    dielectric_ratio = float(calculation["epsilon_infinity"]) / float(anchor["epsilon_infinity"])
    to_relative_error = _relative_error(
        float(calculation["simple_asr_to_frequency_cm1"]),
        float(anchor["to_frequency_cm1"]),
    )
    lo_relative_error = _relative_error(calculated_lo, float(anchor["lo_frequency_cm1"]))
    reference_polar_strength = reference_zstar**2 / float(anchor["epsilon_infinity"])
    calculated_polar_strength = (
        float(calculation["asr_corrected_born_charge_magnitude_e"]) ** 2
        / float(calculation["epsilon_infinity"])
    )
    polar_strength_ratio = calculated_polar_strength / reference_polar_strength

    checks = {
        "short_range_to_planning": to_relative_error
        <= float(thresholds["maximum_to_relative_error_for_planning"]),
        "electronic_gap_screening": gap_ratio
        >= float(thresholds["minimum_gap_ratio_for_electronic_screening"]),
        "dielectric_screening": float(thresholds["minimum_dielectric_ratio"])
        <= dielectric_ratio
        <= float(thresholds["maximum_dielectric_ratio"]),
        "lo_consistency": lo_relative_error <= float(thresholds["maximum_lo_relative_error"]),
        "polar_strength_consistency": float(thresholds["minimum_polar_strength_ratio"])
        <= polar_strength_ratio
        <= float(thresholds["maximum_polar_strength_ratio"]),
        "raw_born_neutrality": abs(float(calculation["raw_born_charge_sum_e"]))
        <= float(thresholds["maximum_raw_born_charge_sum_absolute_e"]),
        "reference_pressure": abs(float(calculation["pressure_kbar"]))
        <= float(thresholds["maximum_absolute_pressure_kbar_for_reference_interpretation"]),
    }

    long_range_checks = [
        "electronic_gap_screening",
        "dielectric_screening",
        "lo_consistency",
        "polar_strength_consistency",
        "raw_born_neutrality",
    ]
    long_range_usable = all(checks[name] for name in long_range_checks)
    short_range_planning = checks["short_range_to_planning"]
    hybrid_design_authorized = bool(short_range_planning and not long_range_usable)

    return {
        "schema_version": "1.0",
        "status": "cdte_polar_response_consistency_evaluated",
        "derived": {
            "primitive_volume_m3": volume,
            "reduced_mass_kg": mu,
            "reference_inferred_born_charge_magnitude_e": reference_zstar,
            "calculated_lo_frequency_cm1": calculated_lo,
            "gap_ratio": gap_ratio,
            "dielectric_ratio": dielectric_ratio,
            "to_relative_error": to_relative_error,
            "lo_relative_error": lo_relative_error,
            "reference_polar_strength_z2_over_epsilon": reference_polar_strength,
            "calculated_polar_strength_z2_over_epsilon": calculated_polar_strength,
            "polar_strength_ratio": polar_strength_ratio,
        },
        "checks": checks,
        "decision": {
            "short_range_gamma_to_planning_usable": short_range_planning,
            "short_range_gamma_to_is_reference_value": False,
            "raw_born_response_converged": checks["raw_born_neutrality"],
            "long_range_polar_response_usable": long_range_usable,
            "current_pbe_polar_ahc_authorized": long_range_usable,
            "hybrid_long_range_short_range_design_authorized": hybrid_design_authorized,
            "automatic_additional_compute_authorized": False,
            "interpretation": (
                "The tightened point gives a planning-level plausible Gamma TO frequency, "
                "but the semilocal electronic gap, macroscopic dielectric screening, raw "
                "Born neutrality, LO consistency, and long-range polar strength do not form "
                "a physically consistent polar response. Reject this PBE point for polar AHC. "
                "Design a separately validated short-range/long-range decomposition before "
                "authorizing any further calculation."
            ),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("first_principles/a0/cdte_polar_response_consistency_contract.json"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    contract = _load(args.contract)
    result = evaluate(contract)
    result["input_sha256"] = {"contract": _sha256(args.contract)}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
