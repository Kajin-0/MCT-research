from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
SOURCE_RESULT = ROOT / "first_principles/b0/r02_epw_raw_vertex_source_qualification_result.json"
HARNESS_STOP = (
    ROOT
    / "first_principles/b0/"
    / "r02_epw_raw_vertex_fixture_harness_stop_29962340413.json"
)
SELECTION = ROOT / "research/capability_audits/qe76_epw61_raw_vertex_fixture_selection.md"
SOURCE_DRIVER = ROOT / "tools/qualify_epw_raw_vertex_sources.sh"
SOURCE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-source-qualification.yml"
FIXTURE_DRIVER = ROOT / "tools/run_epw_raw_vertex_fixture_ci.sh"
FIXTURE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-fixture.yml"
STDOUT_SELECTOR = ROOT / "tools/select_epw_fixture_stdout.py"
STDOUT_SELECTOR_TEST = ROOT / "tests/test_select_epw_fixture_stdout.py"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _source_result() -> dict:
    return json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))


def _harness_stop() -> dict:
    return json.loads(HARNESS_STOP.read_text(encoding="utf-8"))


def test_phase_two_is_one_audited_replacement_gate() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_raw_vertex_fixture"
    assert contract["issue"] == 300
    assert contract["phase"] == "fixture_execution"
    assert contract["execution_mode"] == "one_audited_replacement_after_harness_stop"
    auth = contract["authorization"]
    assert auth["source_clone_and_hash"] is True
    assert auth["qe_epw_build"] is True
    assert auth["upstream_fixture_execution"] is True
    assert auth["observational_export_patch_application"] is True
    assert auth["exactly_one_pinned_build"] is True
    assert auth["exactly_two_fixture_runs_same_state"] is True
    assert auth["one_audited_replacement_build"] is True
    assert auth["one_replacement_disabled_enabled_pair"] is True
    assert auth["cdte_hgte_or_alloy_calculation"] is False
    assert auth["a1_a2_a3"] is False
    assert auth["automatic_retry"] is False
    assert auth["automatic_phase_transition"] is False


def test_fixture_is_pinned_upstream_nonpolar_diamond() -> None:
    contract = _contract()
    source = contract["source"]
    assert source["repository"] == "QEF/q-e"
    assert source["release_tag"] == "qe-7.6"
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    fixture = contract["fixture"]
    assert fixture["upstream_category"] == "epw_base"
    assert fixture["material"] == "diamond"
    assert fixture["epsilon_response_enabled"] is False
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["external_band_count"] == 4
    assert fixture["intermediate_band_count"] == 4
    assert fixture["deterministic_stdout_pattern"] == (
        "test.out.*.inp=epw1.in.args=3"
    )


def test_all_source_and_corrected_patch_hashes_are_committed() -> None:
    contract = _contract()
    assert all(
        len(value["git_blob_sha"]) == 40
        for value in contract["source"]["required_files"].values()
    )
    assert all(
        len(value["sha256"]) == 64
        for value in contract["source"]["required_files"].values()
    )
    patch = contract["observational_patch"]
    assert patch["sha256"] == (
        "b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1"
    )
    assert patch["disabled_by_default"] is True
    assert patch["scientific_contraction_added"] is False
    qualification = contract["source_qualification"]
    assert qualification["current_patch_qualified"] is True
    assert qualification["observational_patch_sha256"] == patch["sha256"]


def test_corrected_patch_qualification_is_immutable_and_zero_execution() -> None:
    contract = _contract()
    result = _source_result()
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
    assert result["execution"]["material_calculation_executed"] is False


def test_prior_harness_stop_is_immutable_and_non_scientific() -> None:
    contract = _contract()
    stop = _harness_stop()
    assert stop["workflow_run_id"] == 29962340413
    assert stop["workflow_job_id"] == 89066052310
    assert stop["artifact_id"] == 8546683709
    assert stop["artifact_digest"] == (
        "sha256:9073466e47eff31d301d7d9b54675edffc420e7f160cecd3c8a523c057166971"
    )
    assert stop["classification"] == "HARNESS_STOP"
    assert stop["last_stage"] == "fixture_disabled"
    assert stop["execution"]["build_count"] == 1
    assert stop["execution"]["scientific_execution_count"] == 1
    assert stop["disabled_fixture"]["upstream_programs_passed"] == 5
    assert stop["disabled_fixture"]["stdout_preserved"] is False
    assert stop["failure"]["scientific_failure"] is False
    assert stop["replacement_authorization"]["maximum_replacement_builds"] == 1
    assert contract["prior_attempt"]["record_path"] == str(
        HARNESS_STOP.relative_to(ROOT)
    )
    assert contract["prior_attempt"]["artifact_digest"] == stop["artifact_digest"]


def test_replacement_keeps_all_physics_and_thresholds_fixed() -> None:
    replacement = _contract()["replacement_authorization"]
    assert replacement["authorized"] is True
    assert replacement["maximum_replacement_builds"] == 1
    assert replacement["required_replacement_fixture_sequences"] == [
        "exporter_disabled",
        "exporter_enabled",
    ]
    for field in (
        "deterministic_stdout_capture_required",
        "source_commit_unchanged",
        "source_tree_unchanged",
        "observational_patch_unchanged",
        "pseudopotential_unchanged",
        "fixture_inputs_unchanged",
        "thresholds_unchanged",
    ):
        assert replacement[field] is True
    assert replacement["automatic_retry"] is False
    assert replacement["automatic_phase_transition"] is False


def test_normalization_and_export_window_are_explicit() -> None:
    contract = _contract()
    normalization = contract["normalization"]
    assert "abs(epf17)^2*inv_wq*g2_tmp" in normalization[
        "backend_scalar_identity"
    ]
    assert "sqrt(inv_wq*g2_tmp)*ryd2ev" in normalization[
        "normalized_vertex_for_repository"
    ]
    window = contract["fixture"]["selected_export_window"]
    assert window["ik_global"] == 1
    assert all(
        window[name]
        for name in (
            "all_q_points",
            "all_modes",
            "all_external_bands",
            "all_intermediate_bands",
            "all_temperatures",
        )
    )


def test_source_driver_remains_hash_only_and_verifies_current_patch() -> None:
    text = SOURCE_DRIVER.read_text(encoding="utf-8")
    assert "patch_requalification_only" in text
    assert "current_patch_qualified" in text
    assert "hashlib.sha256" in text
    assert "scientific_execution_count=0" in text
    assert "./configure" not in text
    assert "make -C" not in text
    assert "pw.x" not in text
    assert "ph.x" not in text
    assert "epw.x" not in text


def test_source_workflow_remains_bounded_to_hash_verification() -> None:
    text = SOURCE_WORKFLOW.read_text(encoding="utf-8")
    assert "timeout-minutes: 20" in text
    assert "bash tools/qualify_epw_raw_vertex_sources.sh" in text
    assert "r02-epw-raw-vertex-source-evidence" in text
    assert "make pw" not in text
    assert "make epw" not in text


def test_fixture_driver_has_one_replacement_build_and_pair() -> None:
    text = FIXTURE_DRIVER.read_text(encoding="utf-8")
    assert "build_count=1" in text
    assert text.count("run_fixture disabled") == 1
    assert text.count("run_fixture enabled") == 1
    assert "scientific_execution_count=$((scientific_execution_count + 1))" in text
    assert 'test "$scientific_execution_count" -eq 2' in text
    assert "git -C \"$WORK/qe\" apply --check" in text
    assert "make -j2 pw ph epw" in text
    assert "test.out.*.inp=epw1.in.args=3" in text
    assert "expected exactly one" in text
    assert "for cutoff" not in text
    assert "for kgrid" not in text
    assert "while true" not in text.lower()
    assert "until " not in text.lower()
    assert "CdTe" not in text
    assert "HgTe" not in text


def test_repository_stdout_selector_has_regression_tests() -> None:
    selector = STDOUT_SELECTOR.read_text(encoding="utf-8")
    tests = STDOUT_SELECTOR_TEST.read_text(encoding="utf-8")
    assert "test.out.*.inp=epw1.in.args=3" in selector
    assert "expected exactly one" in selector
    assert "test_missing_output_fails_closed" in tests
    assert "test_ambiguous_outputs_fail_closed" in tests
    assert "test_preserves_output_before_fixture_cleanup" in tests


def test_fixture_workflow_enforces_resource_ceiling_and_evidence() -> None:
    text = FIXTURE_WORKFLOW.read_text(encoding="utf-8")
    assert "timeout-minutes: 120" in text
    assert "bash tools/run_epw_raw_vertex_fixture_ci.sh" in text
    assert "r02-epw-raw-vertex-fixture-evidence" in text
    assert "OMP_NUM_THREADS: '1'" in text


def test_selection_record_preserves_two_phase_and_claim_boundaries() -> None:
    text = SELECTION.read_text(encoding="utf-8")
    assert "Select the upstream `test-suite/epw_base` diamond fixture" in text
    assert "`lpolar=.true.`" in text
    assert "Phase 2 — closed until a new commit" in text
    assert "does not establish" in text
