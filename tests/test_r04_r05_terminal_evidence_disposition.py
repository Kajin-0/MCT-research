from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from mct_research.r04_r05_terminal_evidence_disposition import (
    TerminalEvidenceDispositionError,
    terminal_summary,
    validate_terminal_evidence_disposition,
)

RECORD_PATH = Path("data/validation/r04_r05_terminal_evidence_disposition.json")


@pytest.fixture()
def record() -> dict:
    return json.loads(RECORD_PATH.read_text(encoding="utf-8"))


def test_terminal_record_validates(record: dict) -> None:
    validate_terminal_evidence_disposition(record)
    assert terminal_summary(record) == {
        "terminal_state": "TERMINAL_EVIDENCE_DISPOSITION_READY",
        "evidence_decision": "EVIDENCE_GATE_FAILED",
        "r05_recommendation": "R05_REACTIVATION_NOT_RECOMMENDED",
        "failed_gate_count": 8,
        "reopening_mode": "NEW_MATCHED_DATA_ONLY",
    }


@pytest.mark.parametrize(
    "authorization_key",
    [
        "outreach_authorized",
        "new_literature_search_required",
        "matched_data_ingestion_authorized",
        "new_random_mass_simulation_authorized",
        "full_kane_authorized",
        "manuscript_authorized",
        "cross_paper_specimen_synthesis_authorized",
    ],
)
def test_prohibited_authorizations_cannot_be_enabled(
    record: dict, authorization_key: str
) -> None:
    mutated = copy.deepcopy(record)
    mutated["authorization"][authorization_key] = True
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)


@pytest.mark.parametrize(
    "gate",
    [
        "local_variance",
        "correlation_length",
        "same_population",
        "near_critical",
        "resolution",
        "matched_null",
        "robustness",
        "decision_changing",
    ],
)
def test_partial_literature_constraints_cannot_pass_evidence_gates(
    record: dict, gate: str
) -> None:
    mutated = copy.deepcopy(record)
    mutated["matched_evidence_gates"][gate]["status"] = "PASS"
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)


def test_r04_method_retained_without_specimen_claim(record: dict) -> None:
    mutated = copy.deepcopy(record)
    mutated["program_status"]["r04_specimen_level_claim"] = "SUPPORTED"
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)


def test_r05_method_retained_without_material_activation(record: dict) -> None:
    mutated = copy.deepcopy(record)
    mutated["program_status"]["r05_material_activation"] = "ACTIVE"
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)


def test_reopening_must_start_with_new_evidence(record: dict) -> None:
    mutated = copy.deepcopy(record)
    mutated["reopening_trigger"]["first_action"] = "RUN_LARGER_SIMULATION"
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)


def test_four_literature_roles_cannot_be_collapsed(record: dict) -> None:
    mutated = copy.deepcopy(record)
    mutated["non_evidence_constraints"][0]["role"] = "MEASURED_PRIOR"
    with pytest.raises(TerminalEvidenceDispositionError):
        validate_terminal_evidence_disposition(mutated)
