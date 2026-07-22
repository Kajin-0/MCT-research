from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
SELECTION = ROOT / "research/capability_audits/qe76_epw61_raw_vertex_fixture_selection.md"
DRIVER = ROOT / "tools/qualify_epw_raw_vertex_sources.sh"
WORKFLOW = ROOT / ".github/workflows/r02-epw-raw-vertex-source-qualification.yml"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_phase_one_is_source_qualification_only() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_raw_vertex_fixture"
    assert contract["issue"] == 300
    assert contract["phase"] == "source_qualification_only"
    auth = contract["authorization"]
    assert auth["source_clone_and_hash"] is True
    assert auth["qe_epw_build"] is False
    assert auth["upstream_fixture_execution"] is False
    assert auth["observational_export_patch_application"] is False
    assert auth["cdte_hgte_or_alloy_calculation"] is False
    assert auth["automatic_retry"] is False
    assert auth["automatic_phase_transition"] is False


def test_fixture_is_pinned_upstream_nonpolar_diamond() -> None:
    contract = _contract()
    source = contract["source"]
    assert source["repository"] == "QEF/q-e"
    assert source["release_tag"] == "qe-7.6"
    assert source["commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["epw_version"] == "6.1"
    fixture = contract["fixture"]
    assert fixture["upstream_category"] == "epw_base"
    assert fixture["material"] == "diamond"
    assert fixture["epsilon_response_enabled"] is False
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["external_band_count"] == 4
    assert fixture["intermediate_band_count"] == 4


def test_all_upstream_git_objects_are_predeclared_but_sha256_is_unresolved() -> None:
    files = _contract()["source"]["required_files"]
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
        assert value["sha256"] is None


def test_phase_transition_requires_committed_hashes_and_cannot_be_automatic() -> None:
    contract = _contract()
    requirements = contract["phase_transition_requirements"]
    assert requirements["all_required_sha256_committed"] is True
    assert requirements["source_qualification_artifact_digest_committed"] is True
    assert requirements["observational_patch_sha256_committed"] is True
    assert requirements["focused_tests_pass"] is True
    assert contract["authorization"]["automatic_phase_transition"] is False


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


def test_driver_clones_and_hashes_but_cannot_build_or_execute() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "git -C \"$WORK/qe\" fetch --depth 1 origin \"$SOURCE_COMMIT\"" in text
    assert "git_blob_sha" in text
    assert "hashlib.sha256" in text
    assert "scientific_execution_count=0" in text
    assert 'assert auth["qe_epw_build"] is False' in text
    assert 'assert auth["upstream_fixture_execution"] is False' in text
    assert "./configure" not in text
    assert "make -C" not in text
    assert "pw.x" not in text
    assert "ph.x" not in text
    assert "epw.x" not in text


def test_workflow_is_bounded_to_source_qualification() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "timeout-minutes: 20" in text
    assert "python -m pytest -vv tests/test_r02_epw_raw_vertex_source_gate.py" in text
    assert "bash tools/qualify_epw_raw_vertex_sources.sh" in text
    assert "r02-epw-raw-vertex-source-evidence" in text
    assert "make pw" not in text
    assert "make epw" not in text


def test_selection_record_rejects_polar_bas_and_material_claims() -> None:
    text = SELECTION.read_text(encoding="utf-8")
    assert "Select the upstream `test-suite/epw_base` diamond fixture" in text
    assert "`lpolar=.true.`" in text
    assert "Phase 2 — closed until a new commit" in text
    assert "does not establish" in text
