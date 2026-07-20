from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/templates/hgcdte_paired_gap_partner_outreach_response_template.json"
TOOL_PATH = ROOT / "tools/audit_hgcdte_partner_outreach_response.py"

spec = importlib.util.spec_from_file_location("partner_outreach_audit", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "outreach.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _approve_and_send(payload: dict, index: int = 0) -> dict:
    payload["package_status"] = "outreach_in_progress"
    payload["claim_boundary"]["messages_sent"] = True
    payload["claim_boundary"]["direct_outreach_performed"] = True
    candidate = payload["candidates"][index]
    candidate["outreach_state"] = "sent"
    candidate["recipient_public_contact_id"] = f"public_contact:{candidate['candidate_id']}"
    candidate["approval_evidence_id"] = f"approval:{candidate['candidate_id']}"
    candidate["external_message_evidence_id"] = f"message:{candidate['candidate_id']}"
    candidate["event_log"].extend(
        [
            {
                "event_type": "approved_to_send",
                "timestamp": "2026-07-20T20:20:00Z",
                "evidence_id": candidate["approval_evidence_id"],
                "external_message": False,
            },
            {
                "event_type": "sent",
                "timestamp": "2026-07-20T20:21:00Z",
                "evidence_id": candidate["external_message_evidence_id"],
                "external_message": True,
            },
        ]
    )
    return candidate


def _add_conditional_response(candidate: dict) -> None:
    candidate["outreach_state"] = "response_received"
    candidate["event_log"].append(
        {
            "event_type": "response_received",
            "timestamp": "2026-07-21T12:00:00Z",
            "evidence_id": f"response:{candidate['candidate_id']}",
            "external_message": True,
        }
    )
    candidate["response"] = {
        "state": "written_conditional",
        "received_at": "2026-07-21T12:00:00Z",
        "evidence_ids": [f"response:{candidate['candidate_id']}"],
        "accountable_contact_id": f"contact:{candidate['candidate_id']}",
        "summary": "Facility is interested subject to specimen review.",
        "role_assessments": [
            {
                "role_id": candidate["role_ids"][0],
                "recommendation": "conditional",
                "evidence_ids": [f"response:{candidate['candidate_id']}"],
                "unresolved_assumptions": ["specimen geometry review pending"],
            }
        ],
        "gate_assessments": [],
        "unresolved_assumptions": ["specimen geometry review pending"],
    }


def test_initial_package_is_drafts_ready_with_no_contact() -> None:
    result = module.audit(DATA_PATH)
    assert result["candidate_count"] == 5
    assert result["draft_ready_count"] == 5
    assert result["approved_to_send_or_later_count"] == 0
    assert result["sent_or_later_count"] == 0
    assert result["response_record_count"] == 0
    assert result["external_messages_sent"] is False
    assert result["direct_outreach_performed"] is False


def test_priority_candidate_and_role_inventory_is_frozen() -> None:
    payload = _payload()
    assert [item["candidate_id"] for item in payload["candidates"]] == list(
        module.EXPECTED_CANDIDATES
    )
    for item in payload["candidates"]:
        assert tuple(item["role_ids"]) == module.EXPECTED_ROLES[item["candidate_id"]]


def test_valid_sent_transition_is_auditable(tmp_path: Path) -> None:
    payload = _payload()
    _approve_and_send(payload)
    result = module.audit(_write(tmp_path, payload))
    assert result["sent_or_later_count"] == 1
    assert result["external_messages_sent"] is True
    assert result["response_record_count"] == 0


def test_sent_state_requires_prior_approval_evidence(tmp_path: Path) -> None:
    payload = _payload()
    payload["package_status"] = "outreach_in_progress"
    payload["claim_boundary"]["messages_sent"] = True
    payload["claim_boundary"]["direct_outreach_performed"] = True
    candidate = payload["candidates"][0]
    candidate["outreach_state"] = "sent"
    candidate["recipient_public_contact_id"] = "public_contact:test"
    candidate["external_message_evidence_id"] = "message:test"
    candidate["event_log"].append(
        {
            "event_type": "sent",
            "timestamp": "2026-07-20T20:21:00Z",
            "evidence_id": "message:test",
            "external_message": True,
        }
    )
    with pytest.raises(ValueError, match="approval evidence"):
        module.audit(_write(tmp_path, payload))


def test_sent_state_requires_external_message_evidence(tmp_path: Path) -> None:
    payload = _payload()
    candidate = _approve_and_send(payload)
    candidate["external_message_evidence_id"] = None
    with pytest.raises(ValueError, match="sent message evidence"):
        module.audit(_write(tmp_path, payload))


def test_response_cannot_precede_sent_outreach(tmp_path: Path) -> None:
    payload = _payload()
    payload["package_status"] = "outreach_in_progress"
    candidate = payload["candidates"][0]
    candidate["outreach_state"] = "response_received"
    candidate["response"]["state"] = "unsupported_verbal"
    candidate["response"]["received_at"] = "2026-07-21T12:00:00Z"
    candidate["response"]["evidence_ids"] = ["note:test"]
    with pytest.raises(ValueError, match="approval evidence|before sent outreach"):
        module.audit(_write(tmp_path, payload))


def test_valid_written_conditional_response_is_ingested(tmp_path: Path) -> None:
    payload = _payload()
    candidate = _approve_and_send(payload)
    _add_conditional_response(candidate)
    result = module.audit(_write(tmp_path, payload))
    assert result["response_record_count"] == 1
    assert result["conditional_role_recommendation_count"] == 1
    assert result["confirmed_role_recommendation_count"] == 0
    assert result["automatic_feasibility_mutation_authorized"] is False


def test_conditional_response_requires_accountable_contact(tmp_path: Path) -> None:
    payload = _payload()
    candidate = _approve_and_send(payload)
    _add_conditional_response(candidate)
    candidate["response"]["accountable_contact_id"] = None
    with pytest.raises(ValueError, match="accountable contact"):
        module.audit(_write(tmp_path, payload))


def test_conditional_role_requires_explicit_assumptions(tmp_path: Path) -> None:
    payload = _payload()
    candidate = _approve_and_send(payload)
    _add_conditional_response(candidate)
    candidate["response"]["role_assessments"][0]["unresolved_assumptions"] = []
    with pytest.raises(ValueError, match="evidence or assumptions"):
        module.audit(_write(tmp_path, payload))


def test_written_confirmed_requires_complete_role_fields(tmp_path: Path) -> None:
    payload = _payload()
    candidate = _approve_and_send(payload)
    candidate["outreach_state"] = "response_received"
    candidate["response"] = {
        "state": "written_confirmed",
        "received_at": "2026-07-21T12:00:00Z",
        "evidence_ids": ["response:test"],
        "accountable_contact_id": "contact:test",
        "summary": "Confirmed.",
        "role_assessments": [
            {
                "role_id": "material_provider",
                "recommendation": "confirmed",
                "evidence_ids": ["response:test"],
                "unresolved_assumptions": [],
            }
        ],
        "gate_assessments": [],
        "unresolved_assumptions": [],
    }
    with pytest.raises(ValueError, match="confirmed role missing"):
        module.audit(_write(tmp_path, payload))


def test_private_contact_details_are_rejected(tmp_path: Path) -> None:
    payload = _payload()
    payload["candidates"][0]["email"] = "person@example.org"
    with pytest.raises(ValueError, match="private contact details"):
        module.audit(_write(tmp_path, payload))


def test_automatic_feasibility_mutation_cannot_be_authorized(tmp_path: Path) -> None:
    payload = _payload()
    payload["claim_boundary"]["automatic_feasibility_mutation_authorized"] = True
    with pytest.raises(ValueError, match="claim boundary"):
        module.audit(_write(tmp_path, payload))
