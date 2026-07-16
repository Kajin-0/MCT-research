from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "first_principles/a0/cdte_pseudopotential_selection.json"
LEDGER = ROOT / "first_principles/pseudopotential_matrix.csv"


def _selection() -> dict:
    return json.loads(SELECTION.read_text(encoding="utf-8"))


def test_selection_is_pinned_but_not_executed() -> None:
    value = _selection()
    assert value["stage"] == "A0_selection_only"
    assert value["run_executed"] is False
    assert value["scientific_result_available"] is False
    assert value["upstream"]["commit"] == "7aa01a3fcf5ad226caf25bd387a9be9612be9f27"
    assert value["verification_state"]["local_sha256_verified"] is False
    assert value["verification_state"]["static_calculation_run"] is False
    assert value["verification_state"]["phonon_calculation_run"] is False


def test_hartree_hints_are_converted_to_rydberg() -> None:
    value = _selection()
    for metadata in value["elements"].values():
        for level in ("low", "normal", "high"):
            assert metadata["cutoff_hints_rydberg"][level] == 2 * metadata["cutoff_hints_hartree"][level]
    compound = value["cdte_cutoff_ladder_rydberg"]
    assert (compound["low"], compound["normal"], compound["high"]) == (94, 102, 114)
    assert compound["ecutrho"] is None


def test_ledger_retains_local_hash_and_result_gates() -> None:
    rows = list(csv.DictReader(LEDGER.read_text(encoding="utf-8").splitlines()))
    rows = [row for row in rows if row["set_id"] == "pd_fr_pbe_v04_primary" and row["material"] == "CdTe"]
    assert {row["element"] for row in rows} == {"Cd", "Te"}
    for row in rows:
        assert row["sha256"] == "PENDING_LOCAL_ACQUISITION"
        assert row["status"] == "exact_upstream_file_selected_local_hash_pending"
        assert row["static_gap_mev"] == ""
        assert row["phonon_status"] == ""
