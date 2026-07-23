from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_same_state_attribution_contract.json"
AUDIT = ROOT / "research/capability_audits/qe76_epw61_same_state_attribution_design.md"

EXPECTED_SOURCE_BLOBS = {
    "EPW/src/epw.f90": "fca6e313d45ef636a81ca45b3585d2abe3124da5",
    "EPW/src/ep_coarse_unfolding.f90": "b9dcb97df833c42d1e3d793c5d66046a42c7ff77",
    "EPW/src/wannier.f90": "a2b706939505a84b2d082e5a83a3dbb1ae8eef57",
    "EPW/src/use_wannier.f90": "104bfee94e9b32e5cb1f86c47382f34090393f3b",
    "EPW/src/io/io.f90": "73fb24ecbf4b690c460006ec354d0b9a7772a044",
    "test-suite/epw_base/epw1.in": "624b4f8a47b003443a131f15afb7815b33a3398e",
    "test-suite/epw_base/epw2.in": "a30b69515a204f74d1565f43806efa72f064e67a",
}


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_all_pinned_upstream_git_blob_ids_are_exact() -> None:
    contract = _contract()
    assert contract["source"]["commit_sha"] == (
        "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    )
    assert contract["source"]["files"] == EXPECTED_SOURCE_BLOBS


def test_control_flow_model_matches_pinned_source_audit() -> None:
    flow = _contract()["upstream_control_flow"]
    assert flow["epwread_skips_pw_restart_loading"] is True
    assert flow["epwread_skips_coarse_regeneration_in_ep_coarse_unfolding"] is True
    assert flow["epwread_reads_crystal_fmt_directly_in_ep_coarse_unfolding"] is True
    assert flow["epwread_reconstructs_wigner_seitz_from_saved_centers"] is True
    assert flow["epwread_calls_epw_read"] is True
    assert flow["epwread_calls_epw_read_ws_data"] is False
    assert flow["wannierize_false_loads_existing_rotation_matrices"] is True
    assert flow["epmatwp_open_mode_mpi"] == "MPI_MODE_RDONLY"
    assert flow["formatted_restart_open_status"] == "old"


def test_consumed_paths_are_distinguished_from_preparation_outputs() -> None:
    state = _contract()["prepared_state"]
    assert state["source_audited_consumed_paths"] == [
        "epwdata.fmt",
        "crystal.fmt",
        "vmedata.fmt",
        "dmedata.fmt",
        "diam.epmatwp",
        "diam.ukk",
    ]
    assert state["source_audited_preparation_outputs"] == [
        "epwdata.fmt",
        "crystal.fmt",
        "vmedata.fmt",
        "dmedata.fmt",
        "wigner.fmt",
        "diam.epmatwp",
        "diam.ukk",
    ]
    assert state["source_audited_required_paths"] == state[
        "source_audited_preparation_outputs"
    ]
    assert state["wigner_fmt_written_by_preparation"] is True
    assert state["wigner_fmt_consumed_by_replay_path"] is False


def test_audit_document_contains_no_superseded_source_identities_or_calls() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    for path, blob in EXPECTED_SOURCE_BLOBS.items():
        assert path in text
        assert blob in text
    assert "11020ee802f815eb446769980bca6d9f065590fa" not in text
    assert "a2b95b9641180a01a8889df526aef74f32a47c21" not in text
    assert "does **not** call `epw_read_ws_data`" in text
    assert "reads `crystal.fmt` directly" in text
