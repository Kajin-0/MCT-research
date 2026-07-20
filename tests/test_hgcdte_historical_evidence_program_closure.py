from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data/derived/hgcdte_historical_evidence_program_closure.json"
TOOL_PATH = ROOT / "tools/audit_hgcdte_historical_evidence_program_closure.py"

spec = importlib.util.spec_from_file_location("historical_closure_audit", TOOL_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _payload() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "closure.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_closure_audit_passes() -> None:
    result = module.audit(DATA_PATH)
    assert result["answered_question_count"] == 5
    assert result["evidence_pr_count"] == 14
    assert result["historical_integration_complete"] is True
    assert result["close_parent_issue"] is True


def test_composition_scale_dwarfs_manuscript_ordering() -> None:
    result = module.audit(DATA_PATH)
    assert result["minimum_composition_scale_meV"] == pytest.approx(8.945)
    assert result["maximum_manuscript_model_separation_meV"] == pytest.approx(0.255)
    assert result["composition_to_model_separation_ratio"] == pytest.approx(35.07843137254902)


def test_all_five_questions_are_present() -> None:
    questions = _payload()["questions"]
    assert set(questions) == {
        "independent_magneto_labs",
        "groves_sign_change",
        "absorption_method_spread",
        "chang_real_spectrum_enlargement",
        "historical_model_ordering",
    }


def test_stop_rules_cannot_be_cleared(tmp_path: Path) -> None:
    payload = _payload()
    payload["stop_rules"]["composition_dominates"] = False
    with pytest.raises(ValueError, match="stop-rule"):
        module.audit(_write(tmp_path, payload))


def test_universal_selection_cannot_be_promoted(tmp_path: Path) -> None:
    payload = _payload()
    payload["questions"]["historical_model_ordering"]["universal_selection"] = True
    with pytest.raises(ValueError, match="model-ordering"):
        module.audit(_write(tmp_path, payload))


def test_chang_readiness_cannot_be_promoted(tmp_path: Path) -> None:
    payload = _payload()
    payload["questions"]["chang_real_spectrum_enlargement"]["native_data_recovered"] = True
    with pytest.raises(ValueError, match="readiness"):
        module.audit(_write(tmp_path, payload))


def test_observation_coordinates_cannot_be_pooled(tmp_path: Path) -> None:
    payload = _payload()
    payload["questions"]["absorption_method_spread"]["pool_as_one_distribution"] = True
    with pytest.raises(ValueError, match="pooled"):
        module.audit(_write(tmp_path, payload))


def test_groves_sign_rejection_is_preserved(tmp_path: Path) -> None:
    payload = _payload()
    payload["questions"]["groves_sign_change"]["schmit_stelzer_pass"] = True
    with pytest.raises(ValueError, match="Schmit-Stelzer"):
        module.audit(_write(tmp_path, payload))


def test_evidence_inventory_cannot_drop_primary_core(tmp_path: Path) -> None:
    payload = _payload()
    payload["evidence_prs"].remove(158)
    with pytest.raises(ValueError, match="evidence inventory"):
        module.audit(_write(tmp_path, payload))


def test_next_track_cannot_revert_to_unpaired_literature(tmp_path: Path) -> None:
    payload = _payload()
    payload["decision"]["next_track"] = "unpaired_literature_accumulation"
    with pytest.raises(ValueError, match="final program decision"):
        module.audit(_write(tmp_path, payload))
