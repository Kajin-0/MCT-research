from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "first_principles/a0/cdte_pseudopotential_selection.json"
HASHES = ROOT / "first_principles/a0/cdte_pseudopotential_hash_manifest.json"
LEDGER = ROOT / "first_principles/pseudopotential_matrix.csv"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_selection_runtime_is_verified_but_science_is_not_executed() -> None:
    value = _read(SELECTION)
    assert value["stage"] == "A0_runtime_verified_selection"
    assert value["run_executed"] is False
    assert value["scientific_result_available"] is False
    state = value["verification_state"]
    assert state["downloaded_byte_sha256_verified"] is True
    assert state["runtime_file_hash_verified"] is True
    assert state["qe_syntax_checked"] is True
    assert state["abinit_syntax_checked"] is True
    assert state["static_calculation_run"] is False
    assert state["phonon_calculation_run"] is False


def test_selection_hashes_match_manifest() -> None:
    selection = _read(SELECTION)
    manifest = _read(HASHES)
    assert manifest["acquisition_complete"] is True
    assert manifest["calculation_executed"] is False
    assert manifest["pseudopotential_files_committed"] is False
    for element in ("Cd", "Te"):
        selected = selection["elements"][element]
        assert selected["upf_sha256"] == manifest["files"][f"{element}_upf"]["sha256"]
        assert selected["psp8_sha256"] == manifest["files"][f"{element}_psp8"]["sha256"]
        assert selected["upf_git_blob_sha1"] == manifest["files"][f"{element}_upf"]["git_blob_sha1"]
        assert selected["psp8_git_blob_sha1"] == manifest["files"][f"{element}_psp8"]["git_blob_sha1"]


def test_hartree_hints_are_converted_to_rydberg() -> None:
    value = _read(SELECTION)
    for metadata in value["elements"].values():
        for level in ("low", "normal", "high"):
            assert metadata["cutoff_hints_rydberg"][level] == 2 * metadata["cutoff_hints_hartree"][level]
    compound = value["cdte_cutoff_ladder_rydberg"]
    assert (compound["low"], compound["normal"], compound["high"]) == (94, 102, 114)
    assert compound["ecutrho"] is None


def test_ledger_records_hashes_without_results() -> None:
    rows = list(csv.DictReader(LEDGER.read_text(encoding="utf-8").splitlines()))
    rows = [row for row in rows if row["set_id"] == "pd_fr_pbe_v04_primary" and row["material"] == "CdTe"]
    expected = {
        "Cd": "d79c48e48b2dcf1f5d347bc0b53d31b01b04acefbf7eb6f8d9f969a73a937cbd",
        "Te": "db5bfbdcbf39096cf2a25c6382f4b07e93e25fe88a162014789466fb5fff6519",
    }
    assert {row["element"] for row in rows} == set(expected)
    for row in rows:
        assert row["sha256"] == expected[row["element"]]
        assert row["status"] == "exact_upstream_bytes_verified_A0_not_run"
        assert row["static_gap_mev"] == ""
        assert row["phonon_status"] == ""
