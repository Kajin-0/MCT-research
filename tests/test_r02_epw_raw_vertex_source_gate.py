from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
SOURCE_RESULT = (
    ROOT / "first_principles/b0/r02_epw_raw_vertex_source_qualification_result.json"
)
SELECTION = ROOT / "research/capability_audits/qe76_epw61_raw_vertex_fixture_selection.md"
SOURCE_DRIVER = ROOT / "tools/qualify_epw_raw_vertex_sources.sh"
SOURCE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-source-qualification.yml"
FIXTURE_DRIVER = ROOT / "tools/run_epw_raw_vertex_fixture_ci.sh"
FIXTURE_WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-fixture.yml"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _source_result() -> dict:
    return json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))


def test_phase_two_is_exactly_one_hash_pinned_fixture_gate() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_raw_vertex_fixture"
    assert contract["issue"] == 300
    assert contract["phase"] == "fixture_execution"
    auth = contract["authorization"]
    assert auth["source_clone_and_hash"] is True
    assert auth["qe_epw_build"] is True
    assert auth["upstream_fixture_execution"] is True
    assert auth["observational_export_patch_application"] is True
    assert auth["exactly_one_pinned_build"] is True
    assert auth["exactly_two_fixture_runs_same_state"] is True
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
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert source["epw_version"] == "6.1"
    fixture = contract["fixture"]
    assert fixture["upstream_category"] == "epw_base"
    assert fixture["material"] == "diamond"
    assert fixture["epsilon_response_enabled"] is False
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["external_band_count"] == 4
    assert fixture["intermediate_band_count"] == 4


def test_all_upstream_sha256_values_and_patch_digest_are_committed() -> None:
    contract = _contract()
    files = contract["source"]["required_files"]
    assert set(files) == {
        "EPW/src/selfen.f90",
        "test-suite/epw_base/scf.in",
        "test-suite/epw_base/ph.in",
        "test-suite/epw_base/scf_epw.in",
        "test-suite/epw_base/nscf_epw.in",
        "test-suite/epw_base/epw1.in",
        "pseudo/C_3.98148.UPF",
    }
    for value in files.values():
        assert len(value["git_blob_sha"]) == 40
        assert len(value["sha256"]) == 64
    patch = contract["observational_patch"]
    assert patch["path"] == "patches/qe76-epw61-r02-raw-vertex-export.patch"
    assert patch["sha256"] == (
        "8ab1f6733d096afa0d975819f56eda2c7428e47e7cc15fe6fc6fdae6fb3e47a4"
    )
    assert patch["disabled_by_default"] is True
    assert patch["scientific_contraction_added"] is False


def test_source_qualification_result_is_immutable_and_zero_execution() -> None:
    contract = _contract()
    result = _source_result()
    assert result["status"] == "passed"
    assert result["workflow_run_id"] == 29960964318
    assert result["artifact_id"] == 8545959823
    assert result["artifact_digest"] == (
        "sha256:467a7162704217efa1f49a79aa0e4d6a5a9b819c06cc4dfdf895b1966ebee811"
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


def test_normalization_and_export_window_are_explicit() -> None:
    contract = _contract()
    normalization = contract["normalization"]
    assert "abs(epf17)^2*inv_wq*g2_tmp" in normalization["backend_scalar_identity"]
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


def test_source_driver_remains_hash_only_even_after_phase_transition() -> None:
    text = SOURCE_DRIVER.read_text(encoding="utf-8")
    assert "git -C \"$WORK/qe\" fetch --depth 1 origin \"$SOURCE_COMMIT\"" in text
    assert "git_blob_sha" in text
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


def test_fixture_driver_has_one_build_two_runs_and_no_retry() -> None:
    text = FIXTURE_DRIVER.read_text(encoding="utf-8")
    assert "build_count=1" in text
    assert text.count("run_fixture disabled") == 1
    assert text.count("run_fixture enabled") == 1
    assert "scientific_execution_count=$((scientific_execution_count + 1))" in text
    assert 'test "$scientific_execution_count" -eq 2' in text
    assert "git -C \"$WORK/qe\" apply --check" in text
    assert "make -j2 pw ph epw" in text
    assert "for cutoff" not in text
    assert "for kgrid" not in text
    assert "retry" not in text.lower()
    assert "CdTe" not in text
    assert "HgTe" not in text


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
