from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.analyze_cdte_polar_response_consistency import (
    evaluate,
    infer_born_charge_magnitude,
    predict_lo_frequency_cm1,
    primitive_volume_m3,
    reduced_mass_kg,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/a0/cdte_polar_response_consistency_contract.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_lo_to_round_trip_recovers_reference_charge() -> None:
    contract = _contract()
    calculation = contract["calculation"]
    anchor = contract["literature_anchor"]
    volume = primitive_volume_m3(calculation["lattice_angstrom"])
    mu = reduced_mass_kg(
        anchor["cadmium_atomic_mass_u"], anchor["tellurium_atomic_mass_u"]
    )
    charge = infer_born_charge_magnitude(
        to_cm1=anchor["to_frequency_cm1"],
        lo_cm1=anchor["lo_frequency_cm1"],
        epsilon_infinity=anchor["epsilon_infinity"],
        volume_m3=volume,
        reduced_mass=mu,
    )
    recovered_lo = predict_lo_frequency_cm1(
        to_cm1=anchor["to_frequency_cm1"],
        born_charge_magnitude=charge,
        epsilon_infinity=anchor["epsilon_infinity"],
        volume_m3=volume,
        reduced_mass=mu,
    )

    assert charge == pytest.approx(2.1577283410001624, rel=1e-12)
    assert recovered_lo == pytest.approx(anchor["lo_frequency_cm1"], rel=1e-12)


def test_current_point_passes_only_short_range_planning_gate() -> None:
    result = evaluate(_contract())
    checks = result["checks"]
    decision = result["decision"]
    derived = result["derived"]

    assert checks["short_range_to_planning"] is True
    assert checks["electronic_gap_screening"] is False
    assert checks["dielectric_screening"] is False
    assert checks["lo_consistency"] is False
    assert checks["polar_strength_consistency"] is False
    assert checks["raw_born_neutrality"] is False
    assert checks["reference_pressure"] is False

    assert derived["calculated_lo_frequency_cm1"] == pytest.approx(
        155.19483750248767, rel=1e-12
    )
    assert derived["gap_ratio"] == pytest.approx(0.3252452583387833, rel=1e-12)
    assert derived["dielectric_ratio"] == pytest.approx(
        8.841544803404255, rel=1e-12
    )
    assert derived["polar_strength_ratio"] == pytest.approx(
        0.3030005853426023, rel=1e-12
    )

    assert decision["short_range_gamma_to_planning_usable"] is True
    assert decision["short_range_gamma_to_is_reference_value"] is False
    assert decision["long_range_polar_response_usable"] is False
    assert decision["current_pbe_polar_ahc_authorized"] is False
    assert decision["hybrid_long_range_short_range_design_authorized"] is True
    assert decision["automatic_additional_compute_authorized"] is False


def test_consistent_anchor_passes_long_range_gate() -> None:
    contract = _contract()
    anchor = contract["literature_anchor"]
    volume = primitive_volume_m3(contract["calculation"]["lattice_angstrom"])
    mu = reduced_mass_kg(
        anchor["cadmium_atomic_mass_u"], anchor["tellurium_atomic_mass_u"]
    )
    reference_charge = infer_born_charge_magnitude(
        to_cm1=anchor["to_frequency_cm1"],
        lo_cm1=anchor["lo_frequency_cm1"],
        epsilon_infinity=anchor["epsilon_infinity"],
        volume_m3=volume,
        reduced_mass=mu,
    )
    calculation = contract["calculation"]
    calculation.update(
        {
            "direct_gamma_gap_ev": anchor["direct_gap_ev"],
            "epsilon_infinity": anchor["epsilon_infinity"],
            "raw_born_charge_sum_e": 0.0,
            "asr_corrected_born_charge_magnitude_e": reference_charge,
            "simple_asr_to_frequency_cm1": anchor["to_frequency_cm1"],
            "pressure_kbar": 0.0,
        }
    )

    result = evaluate(contract)
    assert all(result["checks"].values())
    assert result["decision"]["long_range_polar_response_usable"] is True
    assert result["decision"]["current_pbe_polar_ahc_authorized"] is True
    assert result["decision"]["hybrid_long_range_short_range_design_authorized"] is False


def test_invalid_physical_inputs_fail_closed() -> None:
    with pytest.raises(ValueError, match="LO frequency"):
        infer_born_charge_magnitude(
            to_cm1=167.0,
            lo_cm1=141.0,
            epsilon_infinity=7.05,
            volume_m3=1.0,
            reduced_mass=1.0,
        )
