from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/r02_epw_direct_fixture_terminal_result.json"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-epw-direct-fixture-nonperturbation-stop.md"
STATE_UPDATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-epw-direct-fixture-nonperturbation-stop.md"


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_terminal_result_stops_at_predeclared_nonperturbation_gate() -> None:
    result = _result()
    assert result["stage"] == "B0_epw_direct_fixture_terminal_result"
    assert result["issue"] == 313
    assert result["closed_pr"] == 315
    assert result["status"] == "stop"
    assert result["classification"] == "STOP_NONPERTURBATION_GATE"
    assert result["scientific_failure_established"] is False
    assert result["exporter_nonperturbation_validated"] is False
    assert result["exporter_causal_perturbation_established"] is False
    assert result["backend_normalization_validated"] is False


def test_workflow_and_artifact_identity_are_immutable() -> None:
    workflow = _result()["workflow"]
    assert workflow["run_id"] == 29974357056
    assert workflow["job_id"] == 89102877132
    assert workflow["head_sha"] == "973f480035dd9d0e5d9471b1a94ccd84825ce8e0"
    assert workflow["artifact_id"] == 8550988501
    assert workflow["artifact_digest"] == (
        "sha256:516340d80619da0145a29d53c9ab0fbbf6e747649f3254b5fafb78ebba589da4"
    )
    assert workflow["artifact_size_bytes"] == 2_212_617


def test_source_patch_and_executables_are_pinned() -> None:
    source = _result()["source"]
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["observational_patch_sha256"] == (
        "b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1"
    )
    assert source["executables_sha256"] == {
        "pw.x": "5a58debaea913401b7da27c12cd2f8f346c958c420d65dd9f87b882000a5339f",
        "ph.x": "810d536a9ecdcdd281866d676604948ea4ad2c422733d967efd1025ca182478e",
        "epw.x": "0e9409b836c37bc0e2158caa987c75f70d4e0349592df8837ac55b28f5c9a4e6",
    }


def test_direct_execution_completed_exactly_once() -> None:
    execution = _result()["execution"]
    assert execution == {
        "build_count": 1,
        "sequence_count": 2,
        "disabled_sequence_count": 1,
        "enabled_sequence_count": 1,
        "command_count": 12,
        "commands_with_zero_exit_code": 12,
        "preserved_stdout_stderr_count": 24,
        "exit_code_file_count": 12,
        "material_calculation_count": 0,
        "focused_test_count": 28,
        "focused_tests_passed": 28,
    }
    fixture = _result()["fixture"]
    assert fixture["testcode_used"] is False
    assert fixture["output_discovery_used"] is False
    assert fixture["material_role"] == "upstream_nonpolar_software_fixture_only"
    assert fixture["soc_enabled"] is False


def test_raw_export_is_complete_and_finite() -> None:
    raw = _result()["raw_export"]
    assert raw["row_count"] == 20_736
    assert raw["active_row_count"] == 20_688
    assert raw["zero_mask_row_count"] == 48
    assert raw["unique_q_temperature_count"] == 216
    assert raw["contribution_count"] == 1_296
    assert raw["complete_four_band_blocks"] is True
    assert raw["nonfinite_value_detected"] is False


def test_diagnostic_matrix_and_normalization_checks_pass() -> None:
    checks = _result()["diagnostic_checks"]
    assert checks["normalization_identity"]["passed"] is True
    assert checks["normalization_identity"]["residual_ry2"] < 1e-14
    assert checks["per_row_real_diagonal"]["passed"] is True
    assert checks["per_row_real_diagonal"]["residual_ev"] < 1e-12
    assert checks["summed_real_diagonal"]["passed"] is True
    assert checks["summed_real_diagonal"]["residual_ev"] < 1e-12
    assert checks["synthetic_external_covariance"]["passed"] is True
    assert checks["synthetic_external_covariance"]["residual_ev"] < 1e-12
    assert checks["q_weight_closure"] == {
        "passed": True,
        "residual": 0.0,
        "threshold": 1e-12,
    }
    assert checks["acoustic_mask"]["passed"] is True
    assert checks["retarded_imaginary_sign"]["failure_count"] == 0


def test_selected_window_diagonal_is_reconstructed() -> None:
    diagonal = _result()["selected_window_real_diagonal_ev"]
    differences = [
        abs(backend - reconstructed)
        for backend, reconstructed in zip(
            diagonal["backend"], diagonal["reconstructed"], strict=True
        )
    ]
    assert max(differences) < 1e-12


def test_nonperturbation_gate_fails_without_retrospective_relaxation() -> None:
    gate = _result()["nonperturbation_gate"]
    assert gate["passed"] is False
    assert gate["threshold_ev"] == 1e-12
    assert gate["maximum_self_energy_difference_ev"] == 1.9286256500095078e-7
    assert gate["maximum_energy_difference_ev"] == 1.554600004283202e-9
    assert gate["self_energy_threshold_exceedance_factor"] > 190_000
    assert gate["energy_threshold_exceedance_factor"] > 1_500
    assert gate["comparison_row_count"] == 864


def test_attribution_and_authorization_remain_fail_closed() -> None:
    result = _result()
    interpretation = result["interpretation"]
    assert "cannot be attributed uniquely" in interpretation["attribution"]
    assert "do not override" in interpretation["authorization_value"]
    decision = result["decision"]
    assert decision["direct_full_sequence_exporter_strategy"] == "terminated"
    assert decision["raw_export_normalization"] == (
        "diagnostically_consistent_but_not_validated"
    )
    assert decision["standard_output_nonperturbation"] == "failed"
    assert decision["next_gate_execution_authorized"] is False
    authorization = result["authorization"]
    for field in (
        "additional_build",
        "additional_sequence",
        "automatic_retry",
        "threshold_change",
        "parameter_sweep",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
    ):
        assert authorization[field] is False
    assert authorization["design_only_followup"] is True


def test_decision_and_state_update_preserve_scope() -> None:
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE_UPDATE.read_text(encoding="utf-8")
    assert "STOP_NONPERTURBATION_GATE" in decision
    assert "cannot distinguish those explanations" in decision
    assert "threshold was predeclared" in decision
    assert "same-immutable-state attribution" in state
    assert "Any future" not in state or "Open only for design" in state
