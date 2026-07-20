from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/templates/hgcdte_paired_gap_feasibility_template.json"
TOOL_PATH = ROOT / "tools/audit_hgcdte_paired_gap_feasibility.py"

spec = importlib.util.spec_from_file_location("paired_feasibility_audit", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "feasibility.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _document_role(role: dict, *, state: str) -> None:
    role["status"] = state
    role["accountable_owner_id"] = f"owner_{role['role_id']}"
    role["organization_id"] = f"org_{role['role_id']}"
    role["contact_id"] = f"contact_{role['role_id']}"
    role["capability_evidence_ids"] = [f"evidence_{role['role_id']}"]
    role["geometry_limits_documented"] = True
    role["state_altering_steps_documented"] = True
    role["calibration_or_process_plan_id"] = f"plan_{role['role_id']}"
    if role["native_data_release"] != "not_applicable":
        role["native_data_release"] = "confirmed"
    if role["processing_code_available"] != "not_applicable":
        role["processing_code_available"] = "confirmed"
    if role["covariance_available"] != "not_applicable":
        role["covariance_available"] = "confirmed"
    role["throughput_documented"] = True
    role["turnaround_documented"] = True
    role["shipping_storage_documented"] = True
    role["data_rights_status"] = "compatible"
    role["publication_rights_status"] = "compatible"
    role["cost_estimate_status"] = "estimated"
    role["blocking_assumptions"] = [] if state == "confirmed" else ["resolution_pending"]


def _assess_all(payload: dict, *, role_state: str, gate_state: str) -> None:
    payload["status"] = "completed_review"
    for role in payload["roles"]:
        _document_role(role, state=role_state)
    for gate in payload["pilot_gates"]:
        gate["status"] = gate_state
        gate["evidence_ids"] = [f"evidence_{gate['gate_id']}"]


def _make_pilot_ready(payload: dict) -> None:
    _assess_all(payload, role_state="confirmed", gate_state="confirmed")


def _complete_pilot(payload: dict) -> None:
    _make_pilot_ready(payload)
    payload["pilot_execution"] = {
        "status": "complete",
        "completed_specimen_count": 2,
        "completed_primary_observation_count": 8,
        "minimum_technical_replicates": 2,
        "same_area_pairing_pass": True,
        "temperature_gate_pass": True,
        "native_data_transfer_pass": True,
        "calibration_transfer_pass": True,
        "pre_post_state_drift_pass": True,
        "irreversible_processing_detected": False,
        "failure_records": [],
    }


def _make_prescreening_ready(payload: dict) -> None:
    _complete_pilot(payload)
    payload["prescreening_plan"] = {
        "documented": True,
        "candidate_pool_count": 12,
        "two_composition_levels": True,
        "composition_carrier_vacancy_measured_before_selection": True,
        "selection_algorithm_predeclared": True,
        "same_polarity_requirement_declared": True,
        "aliasing_gate_declared": True,
    }


def _make_full_ready(payload: dict) -> None:
    _make_prescreening_ready(payload)
    payload["prescreening_result"] = {
        "status": "complete",
        "selected_core_specimen_count": 8,
        "maximum_composition_sigma_x": 0.001,
        "same_carrier_polarity_at_6K": True,
        "same_carrier_polarity_at_300K": True,
        "carrier_separation_sigma_6K": 3.5,
        "carrier_separation_sigma_300K": 3.2,
        "vacancy_separation_sigma_6K": 3.1,
        "vacancy_separation_sigma_300K": 3.4,
        "carrier_vacancy_correlation_6K": 0.2,
        "carrier_vacancy_correlation_300K": -0.3,
        "specimen_ids_frozen": True,
        "processing_histories_frozen": True,
    }


def test_empty_template_is_not_ready() -> None:
    result = module.audit(DATA_PATH)
    assert result["readiness_status"] == "not_ready"
    assert result["unknown_role_count"] == 8
    assert result["unknown_pilot_gate_count"] == 13
    assert result["pilot_primary_observation_count"] == 8
    assert result["full_primary_observation_count"] == 32


def test_completed_review_does_not_imply_pilot_readiness(tmp_path: Path) -> None:
    payload = _payload()
    _assess_all(payload, role_state="conditional", gate_state="conditional")
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "capability_review_complete"
    assert result["logistics_pilot_ready"] is False


def test_confirmed_capabilities_make_pilot_ready(tmp_path: Path) -> None:
    payload = _payload()
    _make_pilot_ready(payload)
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "logistics_pilot_ready"
    assert result["confirmed_role_count"] == 8
    assert result["confirmed_pilot_gate_count"] == 13


def test_completed_pilot_remains_non_identifying(tmp_path: Path) -> None:
    payload = _payload()
    _complete_pilot(payload)
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "logistics_pilot_complete"
    assert result["pilot_identifies_carrier_term"] is False
    assert result["pilot_identifies_vacancy_term"] is False
    assert result["full_experiment_ready"] is False


def test_prescreening_plan_is_separate_stage(tmp_path: Path) -> None:
    payload = _payload()
    _make_prescreening_ready(payload)
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "prescreening_ready"
    assert result["full_experiment_ready"] is False


def test_full_readiness_requires_achieved_prescreening(tmp_path: Path) -> None:
    payload = _payload()
    _make_full_ready(payload)
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "full_experiment_ready"
    assert result["full_experiment_ready"] is True


def test_full_readiness_fails_on_composition_uncertainty(tmp_path: Path) -> None:
    payload = _payload()
    _make_full_ready(payload)
    payload["prescreening_result"]["maximum_composition_sigma_x"] = 0.0016
    result = module.audit(_write(tmp_path, payload))
    assert result["readiness_status"] == "prescreening_ready"
    assert "prescreening:composition_sigma_x_above_hard_maximum" in result["blockers"]


def test_full_readiness_fails_on_carrier_vacancy_aliasing(tmp_path: Path) -> None:
    payload = _payload()
    _make_full_ready(payload)
    payload["prescreening_result"]["carrier_vacancy_correlation_6K"] = 0.51
    result = module.audit(_write(tmp_path, payload))
    assert result["full_experiment_ready"] is False
    assert "prescreening:carrier_vacancy_aliasing_6K" in result["blockers"]


def test_confirmed_role_without_evidence_fails_pilot_gate(tmp_path: Path) -> None:
    payload = _payload()
    _make_pilot_ready(payload)
    payload["roles"][0]["capability_evidence_ids"] = []
    result = module.audit(_write(tmp_path, payload))
    assert result["logistics_pilot_ready"] is False
    assert any("confirmed_without_complete_documentation" in item for item in result["blockers"])


def test_confirmed_gate_without_evidence_fails_closed(tmp_path: Path) -> None:
    payload = _payload()
    _make_pilot_ready(payload)
    payload["pilot_gates"][0]["evidence_ids"] = []
    result = module.audit(_write(tmp_path, payload))
    assert result["logistics_pilot_ready"] is False
    assert any("confirmed_without_evidence" in item for item in result["blockers"])


def test_pilot_claim_boundary_cannot_be_promoted(tmp_path: Path) -> None:
    payload = _payload()
    payload["claim_boundary"]["logistics_pilot_identifies_vacancy_effect"] = True
    with pytest.raises(ValueError, match="claim boundary"):
        module.audit(_write(tmp_path, payload))


def test_full_design_cannot_be_reduced(tmp_path: Path) -> None:
    payload = _payload()
    payload["full_experiment_plan"]["specimen_count"] = 4
    with pytest.raises(ValueError, match="full experiment plan"):
        module.audit(_write(tmp_path, payload))
