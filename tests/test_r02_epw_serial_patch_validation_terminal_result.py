from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/r02_epw_serial_patch_validation_terminal_result.json"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-serial-epwread-patch-validation-stop.md"
STATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-serial-epwread-patch-validation-stop.md"


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_terminal_classification_remains_strict_stop() -> None:
    result = _result()
    assert result["stage"] == "B0_epw_serial_patch_validation_terminal_result"
    assert result["issue"] == 350
    assert result["closed_pr"] == 352
    assert result["status"] == "stop"
    assert result["classification"] == "SERIAL_EPWREAD_PATCH_VALIDATION_STOP"
    assert result["strict_harness_passed"] is False
    assert result["material_prediction_validated"] is False


def test_workflow_artifact_and_head_are_immutable() -> None:
    workflow = _result()["workflow"]
    assert workflow == {
        "run_id": 30046644183,
        "job_id": 89339231302,
        "head_sha": "33939fbaaee71ad1952e14534675e55396460d85",
        "artifact_id": 8579603653,
        "artifact_digest": "sha256:17c155f502ecc36cfd88940035ff3c84166d23ac483e09f70ed04dd4a7eb7a67",
        "artifact_size_bytes": 294560,
    }


def test_prebuild_static_attempt_consumed_no_scientific_authorization() -> None:
    attempt = _result()["prebuild_attempt"]
    assert attempt["run_id"] == 30045897907
    assert attempt["artifact_id"] == 8579298688
    assert attempt["build_count"] == 0
    assert attempt["preparation_count"] == 0
    assert attempt["replay_count"] == 0
    assert attempt["scientific_authorization_consumed"] is False
    assert attempt["focused_tests_collected"] == 39
    assert attempt["focused_tests_passed"] == 37


def test_source_patch_input_and_executables_are_pinned() -> None:
    source = _result()["source"]
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["io_f90_git_blob_sha"] == (
        "73fb24ecbf4b690c460006ec354d0b9a7772a044"
    )
    assert source["patch_sha256"] == (
        "ce24ab3ce90f8fa0d0d098f8e8761511204a99bf96589b9ff37eaff79a330e70"
    )
    assert source["replay_input_sha256"] == (
        "6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73"
    )
    assert source["patched_source_check"] == {
        "epmatwp_allocation_count": 1,
        "allocation_before_mpi_split": True,
    }
    assert set(source["executables_sha256"]) == {"pw.x", "ph.x", "epw.x"}


def test_single_execution_completed_without_material_work() -> None:
    execution = _result()["execution"]
    assert execution == {
        "build_count": 1,
        "preparation_count": 1,
        "preparation_command_count": 6,
        "preparation_commands_with_zero_exit_code": 6,
        "replay_count": 1,
        "replay_exit_code": 0,
        "material_calculation_count": 0,
        "focused_tests_collected": 39,
        "focused_tests_passed": 39,
    }
    fixture = _result()["fixture"]
    assert fixture["material_role"] == "upstream_nonpolar_software_fixture_only"
    assert fixture["soc_enabled"] is False
    assert fixture["exporter_enabled"] is False
    assert fixture["export_environment_variables_unset"] is True
    assert fixture["raw_export_candidates"] == []


def test_crash_is_removed_and_self_energy_execution_completed() -> None:
    result = _result()
    assert result["serial_restart_crash_removed"] is True
    assert result["electron_self_energy_execution_completed"] is True
    runtime = result["runtime_evidence"]
    assert runtime["crash_markers_present"] == {
        "SIGSEGV": False,
        "Segmentation fault": False,
        "wigner_divide_ndegen_epmat": False,
    }
    actual = runtime["actual_completion_evidence"]
    assert actual["saved_wannier_state_read"] is True
    assert actual["electron_phonon_interpolation_present"] is True
    assert actual["selfen_elec_call_count"] == 216
    assert actual["total_program_execution_present"] is True
    assert actual["reported_epw_wall_seconds"] == 1.67


def test_state_mutation_is_exact_and_binding() -> None:
    state = _result()["prepared_state"]
    assert state["prepared_file_count"] == 168
    assert state["replay_pre_file_count"] == 168
    assert state["replay_post_file_count"] == 168
    assert state["prepared_manifest_sha256"] == state["replay_pre_manifest_sha256"]
    assert state["replay_post_manifest_sha256"] != state["replay_pre_manifest_sha256"]
    assert state["clone_identity_before_replay"] is True
    assert state["deleted_paths"] == []
    assert state["new_paths"] == []
    assert state["unauthorized_new_paths"] == []
    assert state["byte_identity_passed"] is False
    assert state["mutated_paths"] == [
        {
            "path": "diam.epb1",
            "before_size_bytes": 1137036,
            "before_sha256": "cae2607e190fbf4ef25ad27f49231bbfff011d5d42f234d86beccefdd9654b55",
            "after_size_bytes": 660,
            "after_sha256": "834e3e9735f346b065f8ec270c4cdce672d72a901f684e5afba1e08eac3d29c1",
        }
    ]


def test_literal_marker_contract_is_not_rewritten_after_execution() -> None:
    runtime = _result()["runtime_evidence"]
    assert runtime["predeclared_literal_markers"] == {
        "Electron Self-Energy": False,
        "JOB DONE.": False,
    }
    failures = _result()["binding_failures"]
    assert failures["preexisting_state_mutation"] is True
    assert failures["required_literal_completion_markers_missing"] is True
    assert failures["retrospective_marker_substitution_allowed"] is False
    assert failures["retrospective_state_allowlist_change_allowed"] is False


def test_decision_is_partial_runtime_support_not_harness_promotion() -> None:
    decision = _result()["decision"]
    assert decision["serial_epwread_allocation_diagnosis"] == "runtime_supported"
    assert decision["serial_restart_crash"] == "removed_in_patched_fixture"
    assert decision["strict_restart_harness"] == "failed"
    assert decision["patch_merge_authorized"] is False
    assert decision["additional_execution_under_issue_350"] is False
    assert decision["next_gate_execution_authorized"] is False


def test_authorization_remains_closed() -> None:
    authorization = _result()["authorization"]
    for field in (
        "additional_build",
        "additional_preparation",
        "additional_replay",
        "patch_adjustment",
        "marker_relaxation",
        "state_allowlist_relaxation",
        "mpi_execution",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
    ):
        assert authorization[field] is False
    assert authorization["design_only_followup"] is True


def test_documents_preserve_stop_and_design_only_boundary() -> None:
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE.read_text(encoding="utf-8")
    assert "SERIAL_EPWREAD_PATCH_VALIDATION_STOP" in decision
    assert "runtime-supported" in decision
    assert "diam.epb1" in decision
    assert "No future run is authorized" in decision
    assert "RUNTIME_SUPPORTED" in state
    assert "Open only for design" in state
    assert "additional build" in state
