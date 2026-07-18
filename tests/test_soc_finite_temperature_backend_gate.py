from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools.audit_soc_finite_temperature_backends import evaluate

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/decision_memos/soc_finite_temperature_backend_gate.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_no_backend_is_directly_ready() -> None:
    result = evaluate(_contract())
    decision = result["decision"]

    assert decision["direct_A1_backend_selected"] is False
    assert decision["direct_A1_backend_candidates"] == []
    assert decision["no_existing_route_closes_all_requirements"] is True
    assert decision["preferred_next_design"] == (
        "zg_selected_band_matrix_reconstruction_oracle"
    )
    assert decision["secondary_design"] == (
        "qe_ahc_nonmagnetic_soc_capability_test"
    )
    assert decision["automatic_additional_compute_authorized"] is False


def test_route_specific_blockers_are_preserved() -> None:
    result = evaluate(_contract())["route_results"]

    qe = result["qe_ph_postahc"]
    assert "soc_nonmagnetic" in qe["unresolved_hard_gates"]
    assert qe["direct_A1_ready"] is False

    epw = result["epw_standard"]
    assert "complete_thermal_effect" in epw["failed_hard_gates"]
    assert "offdiagonal_eight_band_matrix" in epw["unresolved_hard_gates"]

    abinit = result["abinit_modern_eph"]
    assert "soc_nonmagnetic" in abinit["failed_hard_gates"]
    assert "offdiagonal_eight_band_matrix" in abinit["failed_hard_gates"]

    zg = result["zg_special_displacement"]
    assert "complete_thermal_effect" in zg["passed_hard_gates"]
    assert "soc_nonmagnetic" in zg["passed_hard_gates"]
    assert "offdiagonal_eight_band_matrix" in zg["unresolved_hard_gates"]
    assert "fixed_or_reconstructable_gauge" in zg["unresolved_hard_gates"]


def test_unverified_does_not_count_as_pass() -> None:
    result = evaluate(_contract())["route_results"]
    assert result["qe_ph_postahc"]["direct_A1_ready"] is False
    assert result["zg_special_displacement"]["direct_A1_ready"] is False


def test_unexpected_direct_backend_fails_audit() -> None:
    contract = copy.deepcopy(_contract())
    route = contract["routes"]["qe_ph_postahc"]
    for gate in contract["hard_gates_for_direct_A1"]:
        route["capabilities"][gate] = "pass"

    with pytest.raises(RuntimeError, match="unexpectedly identifies direct A1"):
        evaluate(contract)


def test_execution_authorization_drift_fails_closed() -> None:
    contract = copy.deepcopy(_contract())
    contract["routes"]["zg_special_displacement"]["execution_authorized"] = True

    with pytest.raises(ValueError, match="execution-blocked"):
        evaluate(contract)
