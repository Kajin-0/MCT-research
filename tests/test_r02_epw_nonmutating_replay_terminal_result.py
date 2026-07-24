from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/r02_epw_nonmutating_replay_terminal_result.json"
DECISION = ROOT / "research/decision_records/2026-07-24-r02-epw-nonmutating-replay-pass.md"
STATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-24-epw-nonmutating-replay-pass.md"


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_terminal_result_is_bounded_pass() -> None:
    result = _result()
    assert result["stage"] == "B0_epw_nonmutating_replay_terminal_result"
    assert result["issue"] == 371
    assert result["closed_executable_pr"] == 372
    assert result["status"] == "pass"
    assert result["classification"] == "PASS_NONMUTATING_SERIAL_REPLAY"
    assert result["claim_boundary"].startswith(
        "This pass validates one patched, exporter-disabled"
    )


def test_preflight_failure_consumed_no_scientific_authorization() -> None:
    preflight = _result()["preflight_attempt"]
    assert preflight["workflow_run_id"] == 30107570717
    assert preflight["artifact_id"] == 8602243538
    assert preflight["classification"] == "STOP_HARNESS"
    assert preflight["last_stage"] == "focused_tests"
    assert preflight["build_count"] == 0
    assert preflight["preparation_count"] == 0
    assert preflight["replay_count"] == 0
    assert preflight["authorization_consumed"] is False
    assert "structural test assertion" in preflight["correction"]
    assert "No contract" in preflight["correction"]


def test_controlling_workflow_and_artifact_are_immutable() -> None:
    workflow = _result()["workflow"]
    assert workflow["run_id"] == 30107733166
    assert workflow["job_id"] == 89529197616
    assert workflow["head_sha"] == "a50739354b767545acb44c9be98f0d48acf2acf8"
    assert workflow["artifact_id"] == 8602492899
    assert workflow["artifact_digest"] == (
        "sha256:c3aeb035173b582f33a65ca1688048257ea8c10c092fa6f6d987d0c328f0d032"
    )
    assert workflow["artifact_archive_size_bytes"] == 305_174
    assert workflow["evidence_tree_size_bytes"] == 3_605_225


def test_source_patch_contracts_and_executables_are_pinned() -> None:
    result = _result()
    source = result["source"]
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["allocation_patch_sha256"] == (
        "ce24ab3ce90f8fa0d0d098f8e8761511204a99bf96589b9ff37eaff79a330e70"
    )
    assert source["patched_source_allocation_count"] == 1
    assert source["patched_allocation_before_mpi_split"] is True
    assert source["executables_sha256"] == {
        "pw.x": "34210babb972f8f18398214462832bee893a53b552fc714bc5f1f91efeb537d0",
        "ph.x": "159fece8541dc1de9cb5ea1326476465ef3602c10f4d1c015525d2c1c9acff07",
        "epw.x": "3ef0ccfa9bfb7a85268449e18d476301bae38522fd5b3750056929557a533071",
    }
    contracts = result["contracts"]
    assert contracts["boundary_contract_git_blob_sha"] == (
        "daf45bab4df80d0762a115460757d11098dcc1ae"
    )
    assert contracts["replay_input_git_blob_sha"] == (
        "480ad888c3c24f84d516b3daeb6a2558cd8044e1"
    )
    assert contracts["replay_input_sha256"] == (
        "e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda"
    )


def test_execution_is_exactly_one_build_preparation_and_replay() -> None:
    execution = _result()["execution"]
    assert execution == {
        "build_count": 1,
        "preparation_count": 1,
        "preparation_command_count": 6,
        "preparation_commands_with_zero_exit_code": 6,
        "serial_replay_count": 1,
        "replay_exit_code": 0,
        "analyzer_exit_code": 0,
        "material_calculation_count": 0,
    }
    fixture = _result()["fixture"]
    assert fixture["material_role"] == "upstream_nonpolar_software_fixture_only"
    assert fixture["soc_enabled"] is False
    assert fixture["exporter_enabled"] is False
    assert fixture["epbwrite"] is False
    assert fixture["epbread"] is False
    assert fixture["epwread"] is True
    assert fixture["electron_self_energy_enabled"] is True


def test_seed_projection_is_reproducible_and_complete() -> None:
    result = _result()
    manifests = result["state_manifests"]
    assert manifests["preparation"]["file_count"] == 168
    assert manifests["projected_seed"]["file_count"] == 162
    assert manifests["replay_pre"]["file_count"] == 162
    assert manifests["replay_post"]["file_count"] == 165
    assert manifests["projected_seed"]["manifest_sha256"] == (
        manifests["replay_pre"]["manifest_sha256"]
    )
    assert manifests["seed_and_replay_pre_identical"] is True
    projection = result["seed_projection"]
    assert projection["removed_forbidden_paths"] == ["diam.epb1"]
    assert projection["removed_declared_outputs"] == [
        "EPW.bib",
        "diam.kgmap",
        "diam_0.kmap",
        "linewidth.elself.300.000K",
        "selecq.fmt",
    ]
    assert projection["removed_transient_paths"] == []


def test_filesystem_integrity_passes_without_epb_or_unknown_outputs() -> None:
    integrity = _result()["filesystem_integrity"]
    assert integrity["passed"] is True
    for key in (
        "deleted_immutable_paths",
        "mutated_immutable_paths",
        "forbidden_created_paths",
        "forbidden_existing_paths",
        "unknown_created_paths",
        "declared_outputs_present_in_seed",
        "created_transient_files",
    ):
        assert integrity[key] == []
    assert integrity["created_declared_outputs"] == [
        "EPW.bib",
        "linewidth.elself.300.000K",
        "selecq.fmt",
    ]
    assert not any("epb" in path.lower() for path in integrity["created_declared_outputs"])
    assert not any("vertex" in path.lower() for path in integrity["created_declared_outputs"])


def test_completion_evidence_is_independently_sufficient() -> None:
    completion = _result()["completion_evidence"]
    assert completion["passed"] is True
    assert completion["classification"] == "EPW_COMPLETION_EVIDENCE_PASS"
    assert completion["exit_code_zero"] is True
    assert completion["fatal_or_signal_markers_present"] is False
    assert completion["total_program_execution_present"] is True
    assert completion["selfen_timer_match_count"] == 1
    assert completion["selfen_timer_calls"] == [216]
    assert completion["selfen_timer_positive_call_count"] is True
    assert completion["linewidth_output"] == {
        "path": "linewidth.elself.300.000K",
        "size_bytes": 414_841,
        "numeric_row_count": 5_184,
    }


def test_decision_and_authorization_remain_fail_closed() -> None:
    result = _result()
    decision = result["decision"]
    assert decision["serial_epwread_allocation_patch"] == (
        "runtime_supported_for_pinned_serial_fixture"
    )
    assert decision["nonmutating_replay_boundary"] == (
        "validated_for_pinned_serial_fixture"
    )
    assert decision["serial_restart_harness"] == "validated"
    assert decision["exporter_noninterference"] == "not_evaluated"
    assert decision["soc_spinor_fixture"] == "not_authorized"
    assert decision["material_self_energy"] == "not_authorized"
    assert decision["next_gate_execution_authorized"] is False
    assert decision["automatic_successor_authorized"] is False
    authorization = result["authorization"]
    for field in (
        "additional_issue_371_build",
        "additional_issue_371_preparation",
        "additional_issue_371_replay",
        "automatic_retry",
        "exporter_enabled_execution",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
    ):
        assert authorization[field] is False
    assert authorization["separate_design_followup"] is True


def test_documents_preserve_claim_boundary_and_historical_stop() -> None:
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE.read_text(encoding="utf-8")
    for text in (decision, state):
        assert "PASS_NONMUTATING_SERIAL_REPLAY" in text
        assert "exporter noninterference" in text.lower()
        assert "material" in text.lower()
    assert "historical issue-350 stop remains unchanged" in decision
    assert "prior issue-350 strict stop remains historically binding" in state
    assert "separate" in decision.lower()
    assert "separate review" in state.lower()
