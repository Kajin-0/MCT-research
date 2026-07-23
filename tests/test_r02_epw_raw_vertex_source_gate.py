from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
SOURCE_RESULT = ROOT / "first_principles/b0/r02_epw_raw_vertex_source_qualification_result.json"
FIRST_STOP = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_harness_stop_29962340413.json"
TERMINAL_STOP = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_terminal_harness_stop_29971955581.json"
SELECTION = ROOT / "research/capability_audits/qe76_epw61_raw_vertex_fixture_selection.md"
SOURCE_DRIVER = ROOT / "tools/qualify_epw_raw_vertex_sources.sh"
SOURCE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-source-qualification.yml"
FIXTURE_DRIVER = ROOT / "tools/run_epw_raw_vertex_fixture_ci.sh"
FIXTURE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-fixture.yml"
STDOUT_SELECTOR = ROOT / "tools/select_epw_fixture_stdout.py"
STDOUT_SELECTOR_TEST = ROOT / "tests/test_select_epw_fixture_stdout.py"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_fixture_contract_is_terminal_and_design_only() -> None:
    contract = _json(CONTRACT)
    assert contract["stage"] == "B0_epw_raw_vertex_fixture"
    assert contract["issue"] == 300
    assert contract["phase"] == "terminal_harness_stop"
    assert contract["execution_mode"] == "no_further_execution_under_issue_300"
    authorization = contract["authorization"]
    for field in (
        "source_clone_and_hash",
        "qe_epw_build",
        "upstream_fixture_execution",
        "observational_export_patch_application",
        "additional_fixture_execution",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "dense_interpolation",
        "automatic_retry",
        "automatic_phase_transition",
    ):
        assert authorization[field] is False
    assert authorization["design_only_followup"] is True


def test_fixture_is_still_the_pinned_nonpolar_diamond_reference() -> None:
    contract = _json(CONTRACT)
    source = contract["source"]
    assert source["repository"] == "QEF/q-e"
    assert source["release_tag"] == "qe-7.6"
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert all(
        len(value["git_blob_sha"]) == 40
        for value in source["required_files"].values()
    )
    assert all(
        len(value["sha256"]) == 64
        for value in source["required_files"].values()
    )
    fixture = contract["fixture"]
    assert fixture["material"] == "diamond"
    assert fixture["epsilon_response_enabled"] is False
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["testcode_fixture_path_terminated"] is True


def test_corrected_patch_qualification_is_immutable_and_zero_execution() -> None:
    contract = _json(CONTRACT)
    result = _json(SOURCE_RESULT)
    assert result["status"] == "passed"
    assert result["workflow_run_id"] == 29962102178
    assert result["artifact_id"] == 8546387617
    assert result["artifact_digest"] == (
        "sha256:71531640506e788996169b0eaad4c19ee19fc9986f87cee56606cb182345b725"
    )
    assert result["source_file_manifest_sha256"] == (
        "c8ecca6ab427a262d5939545d2e834700604dc738de01d9e0285843a3be5360d"
    )
    assert result["source_commit"] == contract["source"]["commit_sha"]
    assert result["source_tree_archive_sha256"] == contract["source"][
        "source_tree_archive_sha256"
    ]
    assert result["observational_patch_sha256"] == contract[
        "observational_patch"
    ]["sha256"]
    assert result["execution"]["scientific_execution_count"] == 0
    assert result["execution"]["qe_epw_build_executed"] is False


def test_first_harness_stop_is_preserved() -> None:
    stop = _json(FIRST_STOP)
    assert stop["workflow_run_id"] == 29962340413
    assert stop["artifact_id"] == 8546683709
    assert stop["artifact_digest"] == (
        "sha256:9073466e47eff31d301d7d9b54675edffc420e7f160cecd3c8a523c057166971"
    )
    assert stop["classification"] == "HARNESS_STOP"
    assert stop["execution"]["build_count"] == 1
    assert stop["execution"]["scientific_execution_count"] == 1
    assert stop["disabled_fixture"]["upstream_programs_passed"] == 5
    assert stop["disabled_fixture"]["stdout_preserved"] is False
    assert stop["failure"]["scientific_failure"] is False


def test_terminal_harness_stop_exhausts_execution_authority() -> None:
    stop = _json(TERMINAL_STOP)
    assert stop["workflow_run_id"] == 29971955581
    assert stop["workflow_job_id"] == 89095664081
    assert stop["artifact_id"] == 8550168667
    assert stop["artifact_digest"] == (
        "sha256:59e73383c7b25a77cb6bc45a19adae80e0c644c1dfc26509c1e7175620e2fe61"
    )
    assert stop["classification"] == "TERMINAL_HARNESS_STOP"
    assert stop["last_stage"] == "fixture_disabled"
    execution = stop["execution"]
    assert execution["build_count"] == 1
    assert execution["scientific_execution_count"] == 1
    assert execution["disabled_fixture_sequence_executed"] is True
    assert execution["enabled_fixture_sequence_executed"] is False
    assert execution["analyzer_executed"] is False
    assert stop["disabled_fixture"]["upstream_programs_passed"] == 5
    assert stop["disabled_fixture"]["stdout_preserved"] is False
    assert stop["failure"]["scientific_failure"] is False
    assert stop["failure"]["normalization_evaluated"] is False
    assert stop["authorization"]["additional_qe_epw_build"] is False
    assert stop["authorization"]["additional_fixture_execution"] is False
    assert stop["authorization"]["design_only_followup"] is True


def test_contract_aggregates_both_consumed_attempts() -> None:
    contract = _json(CONTRACT)
    attempts = contract["attempts"]
    assert [attempt["workflow_run_id"] for attempt in attempts] == [
        29962340413,
        29971955581,
    ]
    assert [attempt["classification"] for attempt in attempts] == [
        "HARNESS_STOP",
        "TERMINAL_HARNESS_STOP",
    ]
    aggregate = contract["aggregate_execution"]
    assert aggregate == {
        "pinned_build_count": 2,
        "disabled_fixture_sequence_count": 2,
        "enabled_fixture_sequence_count": 0,
        "analyzer_execution_count": 0,
        "material_calculation_count": 0,
    }
    decision = contract["terminal_decision"]
    assert decision["scientific_failure"] is False
    assert decision["backend_normalization_validated"] is False
    assert decision["testcode_wrapper_strategy_terminated"] is True
    assert decision["additional_execution_under_issue_300"] is False
    assert decision["next_strategy_execution_authorized"] is False


def test_source_qualification_workflow_is_frozen() -> None:
    text = SOURCE_WORKFLOW.read_text(encoding="utf-8")
    assert "frozen-source-record" in text
    assert "timeout-minutes: 10" in text
    assert "Validate immutable source and terminal records" in text
    assert "Clone exact source and calculate immutable hashes" not in text
    assert "bash tools/qualify_epw_raw_vertex_sources.sh" not in text
    assert "git fetch" not in text


def test_fixture_execution_workflow_is_frozen() -> None:
    text = FIXTURE_WORKFLOW.read_text(encoding="utf-8")
    assert "frozen-terminal-harness-stop" in text
    assert "timeout-minutes: 10" in text
    assert "Verify fail-closed fixture state" in text
    assert "bash tools/run_epw_raw_vertex_fixture_ci.sh" not in text
    assert "Install compiler and numerical dependencies" not in text
    assert "make -j2 pw ph epw" not in text


def test_historical_driver_remains_auditable_but_unreachable() -> None:
    text = FIXTURE_DRIVER.read_text(encoding="utf-8")
    assert "build_count=1" in text
    assert text.count("run_fixture disabled") == 1
    assert text.count("run_fixture enabled") == 1
    assert "test.out.*.inp=epw1.in.args=3" in text
    assert "make -j2 pw ph epw" in text
    assert "for cutoff" not in text
    assert "for kgrid" not in text
    assert "while true" not in text.lower()
    assert "until " not in text.lower()
    assert "run_epw_raw_vertex_fixture_ci.sh" not in FIXTURE_WORKFLOW.read_text(
        encoding="utf-8"
    )


def test_repository_stdout_selector_has_fail_closed_regressions() -> None:
    selector = STDOUT_SELECTOR.read_text(encoding="utf-8")
    tests = STDOUT_SELECTOR_TEST.read_text(encoding="utf-8")
    assert "test.out.*.inp=epw1.in.args=3" in selector
    assert "expected exactly one" in selector
    assert "test_missing_output_fails_closed" in tests
    assert "test_ambiguous_outputs_fail_closed" in tests
    assert "test_preserves_output_before_fixture_cleanup" in tests


def test_next_step_is_design_only_direct_execution() -> None:
    contract = _json(CONTRACT)
    transition = contract["phase_transition_requirements"]
    for field in (
        "terminal_stop_record_committed",
        "fixture_workflow_frozen",
        "issue_300_closed_before_new_execution",
        "new_design_issue_required",
        "source_level_command_reconstruction_required",
        "synthetic_capture_tests_required",
        "dry_run_manifest_required",
        "separate_execution_authorization_required",
    ):
        assert transition[field] is True
    assert contract["terminal_decision"]["next_strategy"] == (
        "design_direct_executable_fixture_with_explicit_stdout_stderr_redirection"
    )


def test_selection_record_retains_original_claim_boundaries() -> None:
    text = SELECTION.read_text(encoding="utf-8")
    assert "Select the upstream `test-suite/epw_base` diamond fixture" in text
    assert "`lpolar=.true.`" in text
    assert "does not establish" in text


def test_source_driver_is_preserved_but_unreachable() -> None:
    assert SOURCE_DRIVER.is_file()
    assert "bash tools/qualify_epw_raw_vertex_sources.sh" not in SOURCE_WORKFLOW.read_text(
        encoding="utf-8"
    )
