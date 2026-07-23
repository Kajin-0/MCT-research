from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/r02_epw_same_state_terminal_result.json"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-epw-same-state-replay-harness-stop.md"
STATE_UPDATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-epw-same-state-replay-harness-stop.md"


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_terminal_result_is_harness_stop_not_scientific_failure() -> None:
    result = _result()
    assert result["stage"] == "B0_epw_same_state_attribution_terminal_result"
    assert result["issue"] == 332
    assert result["closed_pr"] == 333
    assert result["status"] == "stop"
    assert result["classification"] == "STOP_HARNESS"
    assert result["harness_failure_established"] is True
    assert result["scientific_failure_established"] is False
    assert result["historical_issue_313_result_changed"] is False
    assert result["exporter_noninterference_established"] is False
    assert result["exporter_causal_perturbation_established"] is False
    assert result["backend_normalization_validated"] is False


def test_workflow_and_artifact_identity_are_immutable() -> None:
    workflow = _result()["workflow"]
    assert workflow == {
        "run_id": 30020494017,
        "job_id": 89251617785,
        "head_sha": "6b7cee7aa043789a273e1b12d2738522992385a6",
        "artifact_id": 8569280948,
        "artifact_digest": "sha256:1d80fb575a5d736dbd3211edb7dad4c694c151a7209dffed954489924e65dcd8",
        "artifact_size_bytes": 241357,
    }


def test_source_patch_and_executables_are_pinned() -> None:
    source = _result()["source"]
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["observational_patch_sha256"] == (
        "b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1"
    )
    assert source["applied_patch_sha256"] == (
        "a0c25cc7041847f59e0436a1c45b4dc2d2e49a0527c8f8ddb4414063fab558aa"
    )
    assert source["executables_sha256"] == {
        "pw.x": "572e97aca36d6841d31add2ad803b1ebaf234af9f006c847afdc146aa02a2d73",
        "ph.x": "e1717cb27c1b9227947331dce0ea1b1d50db580a8bdd2a16fe15c2864eacd51a",
        "epw.x": "9692de1f980314548a7df455d679340d45a028a4768cf14bd42b06fe7800855f",
    }


def test_build_preparation_and_freeze_completed() -> None:
    execution = _result()["execution"]
    assert execution["build_count"] == 1
    assert execution["preparation_command_count"] == 6
    assert execution["preparation_commands_with_zero_exit_code"] == 6
    assert execution["prepared_state_file_count"] == 168
    assert execution["replay_count_authorized"] == 3
    assert execution["replays_launched"] == 1
    assert execution["replays_completed"] == 0
    assert execution["disabled_a_launched"] is True
    assert execution["disabled_b_launched"] is False
    assert execution["enabled_launched"] is False
    assert execution["raw_exporter_invoked"] is False
    assert _result()["fixture"]["material_calculation_count"] == 0


def test_three_pre_replay_states_are_identical() -> None:
    state = _result()["prepared_state"]
    assert state["complete_tree_manifest_created"] is True
    assert state["required_paths_present"] is True
    assert state["three_pre_replay_manifests_identical"] is True
    assert state["manifest_payload_sha256"] == (
        "6478b7db2839930e8edfdf9350b5f530255a7356305c1da9f89d77be22123289"
    )
    expected_file_hash = (
        "646df1e09b0bd986ca980fa5a7193721c8bdbeb05a727b3fc5dd16cfd4a7148c"
    )
    assert state["prepared_manifest_file_sha256"] == expected_file_hash
    assert state["disabled_a_pre_manifest_sha256"] == expected_file_hash
    assert state["disabled_b_pre_manifest_sha256"] == expected_file_hash
    assert state["enabled_pre_manifest_sha256"] == expected_file_hash
    assert state["pre_replay_gate_sha256"] == (
        "dbf1e4bacbd11a63dc2677aed22e55cf8658a9cc7537c853dbba22d57e5b0eda"
    )
    assert state["post_replay_manifests_created"] is False
    assert state["state_mutation_evaluated"] is False


def test_disabled_a_sigsegv_identity_is_exact() -> None:
    failure = _result()["failure"]
    assert failure["replay_id"] == "disabled_a"
    assert failure["exporter_enabled"] is False
    assert failure["exit_code"] == 139
    assert failure["signal"] == "SIGSEGV"
    assert failure["occurred_before_self_energy_evaluation"] is True
    assert failure["routine"] == "wigner_divide_ndegen_epmat"
    assert failure["source_path"] == "EPW/src/wigner.f90"
    assert failure["source_line"] == 1009
    assert failure["caller"] == "build_wannier"
    assert failure["caller_source_path"] == "EPW/src/wannier.f90"
    assert failure["caller_source_line"] == 452
    assert failure["disabled_a_stdout_sha256"] == (
        "da3421f9bae60fc2cef344756e67d32818de4d17990fe812c237615560654a46"
    )
    assert failure["disabled_a_stderr_sha256"] == (
        "24c2562bb9088f776b78fee404e1369ada4a3dbd7a937cd3001515181874b3bd"
    )


def test_source_diagnosis_is_explicitly_an_inference() -> None:
    inference = _result()["source_supported_inference"]
    assert "serial epwread path" in inference["statement"]
    assert "without a visible serial-branch allocation" in inference["statement"]
    assert len(inference["support"]) == 4
    assert inference["causal_diagnosis_proven"] is False
    assert inference["minimal_patch_validated"] is False


def test_all_scientific_and_post_replay_gates_are_not_evaluated() -> None:
    gates = _result()["gates"]
    assert gates == {
        "source_and_build": "passed",
        "preparation": "passed",
        "pre_replay_state_identity": "passed",
        "disabled_a_replay": "harness_failure",
        "disabled_baseline_reproducibility": "not_evaluated",
        "enabled_attribution": "not_evaluated",
        "raw_vertex_diagnostics": "not_evaluated",
        "post_replay_state_integrity": "not_evaluated",
    }
    assert all(value is None for value in _result()["metrics"].values())


def test_decision_and_authorization_are_fail_closed() -> None:
    result = _result()
    decision = result["decision"]
    assert decision["serial_epwread_same_state_protocol"] == "terminated"
    assert decision["exporter_attribution"] == "not_evaluated"
    assert decision["raw_export_normalization"] == "not_evaluated"
    assert decision["soc_spinor_fixture"] == "not_authorized"
    assert decision["material_self_energy"] == "not_authorized"
    assert decision["next_gate"] == "design_only_serial_epwread_source_diagnosis"
    assert decision["next_gate_execution_authorized"] is False

    authorization = result["authorization"]
    for field in (
        "additional_build",
        "additional_preparation",
        "additional_replay",
        "automatic_retry",
        "mpi_substitution",
        "source_patch_execution",
        "alternate_build",
        "threshold_change",
        "parameter_sweep",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
    ):
        assert authorization[field] is False
    assert authorization["design_only_source_diagnosis"] is True


def test_records_do_not_authorize_execution_or_overstate_causality() -> None:
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE_UPDATE.read_text(encoding="utf-8")
    assert "STOP_HARNESS" in decision
    assert "likely serial `epwread` allocation defect" in decision
    assert "does not prove the diagnosis" in decision
    assert "No execution is authorized" in decision
    assert "source-level confirmation" in state
    assert "patched-source execution" in state
    assert "Open only for design" in state
