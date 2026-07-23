from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_terminal_result.json"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-epw-testcode-fixture-terminal-stop.md"
STATE_UPDATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-epw-testcode-fixture-terminal-stop.md"


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_terminal_result_is_fail_closed() -> None:
    result = _result()
    assert result["stage"] == "B0_epw_raw_vertex_fixture_terminal_result"
    assert result["issue"] == 300
    assert result["closed_pr"] == 305
    assert result["status"] == "stop"
    assert result["classification"] == "STOP_HARNESS_BUDGET_EXHAUSTED"
    assert result["scientific_failure_established"] is False
    assert result["backend_normalization_validated"] is False


def test_source_qualification_is_pinned_and_zero_execution() -> None:
    source = _result()["source_qualification"]
    assert source["source_commit"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["observational_patch_sha256"] == (
        "b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1"
    )
    assert source["workflow_run_id"] == 29962102178
    assert source["artifact_id"] == 8546387617
    assert source["build_count"] == 0
    assert source["scientific_execution_count"] == 0
    assert source["passed"] is True


def test_both_attempts_are_preserved_without_physics_overclaim() -> None:
    attempts = _result()["attempts"]
    assert [attempt["workflow_run_id"] for attempt in attempts] == [
        29962340413,
        29971955581,
    ]
    assert [attempt["artifact_id"] for attempt in attempts] == [
        8546683709,
        8550168667,
    ]
    assert [attempt["disabled_fixture_programs_passed"] for attempt in attempts] == [
        5,
        5,
    ]
    assert all(attempt["stdout_preserved"] is False for attempt in attempts)
    assert all(attempt["enabled_fixture_executed"] is False for attempt in attempts)
    assert all(attempt["analyzer_executed"] is False for attempt in attempts)


def test_aggregate_execution_and_decision_are_exact() -> None:
    result = _result()
    assert result["aggregate_execution"] == {
        "pinned_build_count": 2,
        "disabled_fixture_sequence_count": 2,
        "disabled_fixture_programs_passed": 10,
        "disabled_fixture_program_count": 10,
        "enabled_fixture_sequence_count": 0,
        "analyzer_execution_count": 0,
        "material_calculation_count": 0,
    }
    decision = result["decision"]
    assert decision["qe_testcode_wrapper_strategy"] == "terminated"
    assert decision["raw_complex_vertex_export"] == "not_validated"
    assert decision["scalar_diagonal_equivalence"] == "not_evaluated"
    assert decision["backend_covariance"] == "not_evaluated"
    assert decision["next_issue"] == 309
    assert decision["next_gate_execution_authorized"] is False


def test_no_execution_is_authorized() -> None:
    authorization = _result()["authorization"]
    for field in (
        "qe_epw_build",
        "fixture_execution",
        "automatic_retry",
        "parameter_sweep",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
    ):
        assert authorization[field] is False
    assert authorization["design_only_followup"] is True


def test_decision_and_state_update_preserve_claim_boundary() -> None:
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE_UPDATE.read_text(encoding="utf-8")
    assert "QE testcode-wrapped fixture strategy is terminated" in decision
    assert "backend normalization question was not evaluated" in decision
    assert "Issue #309 is design-only" in decision
    assert "STOP_HARNESS_BUDGET_EXHAUSTED" in state
    assert "Any future QE execution requires a separate bounded issue" in state
