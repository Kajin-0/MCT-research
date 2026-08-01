"""Validate the terminal R04/R05 evidence disposition.

The validator protects the distinction between retained method assets and missing
specimen-level evidence. It intentionally performs no scientific inference.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

TERMINAL_STATE = "TERMINAL_EVIDENCE_DISPOSITION_READY"
EVIDENCE_DECISION = "EVIDENCE_GATE_FAILED"
R05_RECOMMENDATION = "R05_REACTIVATION_NOT_RECOMMENDED"
REQUIRED_GATES = {
    "local_variance",
    "correlation_length",
    "same_population",
    "near_critical",
    "resolution",
    "matched_null",
    "robustness",
    "decision_changing",
}
PROHIBITED_AUTHORIZATIONS = {
    "outreach_authorized",
    "new_literature_search_required",
    "matched_data_ingestion_authorized",
    "new_random_mass_simulation_authorized",
    "full_kane_authorized",
    "manuscript_authorized",
    "cross_paper_specimen_synthesis_authorized",
}


class TerminalEvidenceDispositionError(ValueError):
    """Raised when the terminal evidence record violates a frozen boundary."""


def load_terminal_evidence_disposition(path: str | Path) -> dict[str, Any]:
    """Load and validate a terminal evidence-disposition JSON record."""

    with Path(path).open("r", encoding="utf-8") as handle:
        record = json.load(handle)
    validate_terminal_evidence_disposition(record)
    return record


def validate_terminal_evidence_disposition(record: Mapping[str, Any]) -> None:
    """Validate decision vocabulary, failed gates, and reopening boundaries."""

    if record.get("terminal_state") != TERMINAL_STATE:
        raise TerminalEvidenceDispositionError("terminal state is not frozen")
    if record.get("evidence_decision") != EVIDENCE_DECISION:
        raise TerminalEvidenceDispositionError("evidence decision must remain failed")
    if record.get("r05_recommendation") != R05_RECOMMENDATION:
        raise TerminalEvidenceDispositionError("R05 reactivation recommendation changed")

    authorization = record.get("authorization")
    if not isinstance(authorization, Mapping):
        raise TerminalEvidenceDispositionError("authorization block is missing")
    for key in PROHIBITED_AUTHORIZATIONS:
        if authorization.get(key) is not False:
            raise TerminalEvidenceDispositionError(f"{key} must remain false")

    status = record.get("program_status")
    if not isinstance(status, Mapping):
        raise TerminalEvidenceDispositionError("program status is missing")
    required_status = {
        "r04_method_framework": "RETAINED",
        "r04_external_validation_branch": "PAUSED_UNTIL_NEW_MATCHED_DATA",
        "r04_specimen_level_claim": "NOT_SUPPORTED",
        "r04_manuscript_authorization": "DENIED",
        "r05_method_benchmark": "RETAINED",
        "r05_material_activation": "BLOCKED",
        "r05_full_kane": "NOT_AUTHORIZED",
    }
    for key, value in required_status.items():
        if status.get(key) != value:
            raise TerminalEvidenceDispositionError(f"invalid program status: {key}")

    gates = record.get("matched_evidence_gates")
    if not isinstance(gates, Mapping) or set(gates) != REQUIRED_GATES:
        raise TerminalEvidenceDispositionError("the eight matched evidence gates are incomplete")
    for name, gate in gates.items():
        if not isinstance(gate, Mapping) or gate.get("status") != "FAIL":
            raise TerminalEvidenceDispositionError(f"gate {name} must remain FAIL")
        reason = gate.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise TerminalEvidenceDispositionError(f"gate {name} lacks a reason")

    constraints = record.get("non_evidence_constraints")
    if not isinstance(constraints, list) or len(constraints) != 4:
        raise TerminalEvidenceDispositionError("four non-evidence roles are required")
    roles = {entry.get("role") for entry in constraints if isinstance(entry, Mapping)}
    expected_roles = {
        "DESIGN_TARGET",
        "DRIFT_STRESS_CASE",
        "KERNEL_METHOD_BENCHMARK",
        "STM_ARTIFACT_ENVELOPE",
    }
    if roles != expected_roles:
        raise TerminalEvidenceDispositionError("literature semantic roles changed")

    reopening = record.get("reopening_trigger")
    if not isinstance(reopening, Mapping):
        raise TerminalEvidenceDispositionError("reopening trigger is missing")
    if reopening.get("mode") != "NEW_MATCHED_DATA_ONLY":
        raise TerminalEvidenceDispositionError("reopening mode must require new matched data")
    if reopening.get("first_action") != "INGEST_AND_VALIDATE_NEW_EVIDENCE":
        raise TerminalEvidenceDispositionError("reopening must start with evidence ingestion")
    required = reopening.get("required")
    if not isinstance(required, list) or len(required) < 5:
        raise TerminalEvidenceDispositionError("reopening evidence package is incomplete")
    prohibited = reopening.get("prohibited_first_actions")
    if not isinstance(prohibited, list):
        raise TerminalEvidenceDispositionError("prohibited reopening actions are missing")
    for phrase in (
        "larger random-mass simulation",
        "full-Kane disorder calculation",
        "manuscript drafting",
        "cross-paper specimen synthesis",
    ):
        if phrase not in prohibited:
            raise TerminalEvidenceDispositionError(f"missing prohibited action: {phrase}")


def terminal_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a compact non-inferential summary after validation."""

    validate_terminal_evidence_disposition(record)
    return {
        "terminal_state": record["terminal_state"],
        "evidence_decision": record["evidence_decision"],
        "r05_recommendation": record["r05_recommendation"],
        "failed_gate_count": sum(
            gate["status"] == "FAIL"
            for gate in record["matched_evidence_gates"].values()
        ),
        "reopening_mode": record["reopening_trigger"]["mode"],
    }
