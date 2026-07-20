from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/evidence/hgcdte_paired_gap_public_candidate_landscape.json"
TOOL_PATH = ROOT / "tools/audit_hgcdte_public_candidate_landscape.py"

spec = importlib.util.spec_from_file_location("public_candidate_audit", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "landscape.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_landscape_audit_passes() -> None:
    result = module.audit(DATA_PATH)
    assert result["candidate_count"] == 8
    assert result["priority_1_candidate_count"] == 6
    assert result["priority_2_candidate_count"] == 2
    assert result["official_source_count"] == 14
    assert result["target_role_count"] == 7
    assert result["covered_role_count"] == 7
    assert result["candidate_role_assignments"] == 9
    assert result["unresolved_candidate_gate_count"] == 53


def test_public_evidence_promotes_no_readiness() -> None:
    result = module.audit(DATA_PATH)
    assert result["confirmed_role_count"] == 0
    assert result["confirmed_gate_count"] == 0
    assert result["feasibility_readiness_promoted"] is False


def test_maglab_deadline_interval_is_frozen() -> None:
    result = module.audit(DATA_PATH)
    assert result["next_maglab_deadline"] == "2026-11-13"
    assert result["days_from_evidence_date_to_maglab_deadline"] == 116


def test_primary_contact_sequence_is_role_driven() -> None:
    result = module.audit(DATA_PATH)
    assert result["recommended_first_contact_ids"] == [
        "uic_microphysics_laboratory",
        "national_maglab_ir_thz",
        "wsu_positron_annihilation_spectrometer",
        "ut_austin_epma",
        "utk_electromagnetic_properties_lab",
    ]


def test_candidate_cannot_be_promoted_to_confirmed(tmp_path: Path) -> None:
    payload = _payload()
    payload["candidates"][0]["candidate_status"] = "confirmed"
    with pytest.raises(ValueError, match="promoted"):
        module.audit(_write(tmp_path, payload))


def test_public_evidence_cannot_change_readiness(tmp_path: Path) -> None:
    payload = _payload()
    payload["candidates"][0]["readiness_effect"] = "capability_review_complete"
    with pytest.raises(ValueError, match="readiness"):
        module.audit(_write(tmp_path, payload))


def test_official_https_source_is_required(tmp_path: Path) -> None:
    payload = _payload()
    payload["candidates"][0]["official_sources"][0]["url"] = "https://example.com/claim"
    with pytest.raises(ValueError, match="non-official"):
        module.audit(_write(tmp_path, payload))


def test_every_candidate_requires_unresolved_hard_gates(tmp_path: Path) -> None:
    payload = _payload()
    payload["candidates"][0]["unresolved_hard_gates"] = []
    with pytest.raises(ValueError, match="unresolved gates"):
        module.audit(_write(tmp_path, payload))


def test_role_coverage_must_match_candidate_records(tmp_path: Path) -> None:
    payload = _payload()
    payload["role_coverage"]["material_provider"] = []
    with pytest.raises(ValueError, match="role coverage"):
        module.audit(_write(tmp_path, payload))


def test_direct_outreach_cannot_be_claimed(tmp_path: Path) -> None:
    payload = _payload()
    payload["decision"]["direct_outreach_performed"] = True
    with pytest.raises(ValueError, match="decision"):
        module.audit(_write(tmp_path, payload))


def test_candidate_endorsement_cannot_be_claimed(tmp_path: Path) -> None:
    payload = _payload()
    payload["decision"]["candidate_endorsement_authorized"] = True
    with pytest.raises(ValueError, match="decision"):
        module.audit(_write(tmp_path, payload))


def test_feasibility_template_cannot_be_claimed_modified(tmp_path: Path) -> None:
    payload = _payload()
    payload["status_boundary"]["feasibility_template_modified"] = True
    with pytest.raises(ValueError, match="status boundary"):
        module.audit(_write(tmp_path, payload))
