from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "first_principles/b0/r02_epw_replay_output_boundary_source_audit.json"
CONTRACT = ROOT / "first_principles/b0/r02_epw_replay_output_boundary_contract.json"
CAPABILITY = ROOT / "research/capability_audits/qe76_epw61_nonmutating_replay_boundary.md"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-epw-nonmutating-replay-boundary.md"
STATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-epw-nonmutating-replay-boundary.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_audit_is_pinned_and_design_only() -> None:
    audit = _json(AUDIT)
    assert audit["stage"] == "B0_epw_replay_output_boundary_source_audit"
    assert audit["issue"] == 355
    assert audit["classification"] == "REPLAY_BOUNDARY_SUPPORTED"
    assert audit["runtime_validation_performed"] is False
    assert audit["source"]["commit_sha"] == (
        "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    )
    assert audit["authorization"] == {
        "source_and_design_work": True,
        "runtime_validation": False,
        "automatic_executable_successor": False,
    }


def test_all_upstream_git_blob_identities_are_exact() -> None:
    expected = {
        "EPW/src/input.f90": "caf48c74542f522aeff9ed8431e27512999c3ced",
        "EPW/src/readin.f90": "1f4a3bca3aa511d9782e3d50ce4c66d47f9f5589",
        "EPW/src/ep_coarse_unfolding.f90": "b9dcb97df833c42d1e3d793c5d66046a42c7ff77",
        "EPW/src/epw.f90": "fca6e313d45ef636a81ca45b3585d2abe3124da5",
        "EPW/src/stop.f90": "33e504b8c473ac5ca9ad26a59e56b8e5eda0c29a",
        "EPW/src/printing.f90": "5437074def616e315e85f3cdfd988fbabcbb1aeb",
        "EPW/src/io/io_var.f90": "39e6f840dea02719607f370ab743233575b01346",
        "test-suite/epw_base/epw2.in": "a30b69515a204f74d1565f43806efa72f064e67a",
    }
    assert _json(AUDIT)["source"]["git_blobs"] == expected
    assert _json(CONTRACT)["source"]["git_blobs"] == expected


def test_epb_ownership_and_output_only_delta_are_consistent() -> None:
    audit = _json(AUDIT)
    ownership = audit["diam_epb1_ownership"]
    assert ownership["file_role"] == (
        "optional coarse Bloch-representation serialization output"
    )
    assert ownership["consumed_when_epwread_true_epbread_false"] is False
    assert ownership["written_when_epbwrite_true"] is True
    assert ownership["required_by_electron_self_energy_replay"] is False
    assessment = audit["epbwrite_false_assessment"]
    assert assessment["changes_physical_parameters"] is False
    assert assessment["changes_self_energy_parameters"] is False
    assert assessment["changes_restart_read_path"] is False
    assert assessment["changes_in_memory_interpolation_or_self_energy_contraction"] is False
    assert assessment["suppresses_only_optional_epb_serialization"] is True


def test_completion_evidence_has_independent_source_grounded_components() -> None:
    evidence = _json(AUDIT)["completion_evidence"]
    assert evidence["source_grounded_total_marker"] == "Total program execution"
    assert evidence["self_energy_timer"] == "selfen_elec_"
    assert evidence["self_energy_timer_requirement"] == "positive call count"
    assert evidence["physical_result_unit"] == "linewidth_elself"
    assert evidence["physical_result_pattern"] == "linewidth.elself.*"
    assert evidence["rejected_post_hoc_markers"] == [
        "JOB DONE.",
        "Electron Self-Energy",
    ]


def test_contract_and_audit_preserve_historical_stop_and_no_runtime_claim() -> None:
    audit = _json(AUDIT)
    contract = _json(CONTRACT)
    assert audit["proof_obligations_satisfied"][
        "historical_issue_350_stop_preserved"
    ] is True
    assert contract["historical_issue_350_result_unchanged"] is True
    assert audit["remaining_uncertainty"] == {
        "runtime_nonmutation_with_epbwrite_false": "not tested",
        "future_exporter_noninterference": "not tested",
        "soc_or_material_applicability": "not tested",
    }
    assert contract["authorization"]["epw_replay_execution"] is False
    assert contract["authorization"]["automatic_executable_successor"] is False


def test_documents_use_supported_classification_and_closed_execution_boundary() -> None:
    capability = CAPABILITY.read_text(encoding="utf-8")
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE.read_text(encoding="utf-8")
    for text in (capability, decision, state):
        assert "REPLAY_BOUNDARY_SUPPORTED" in text
        assert "not authorized" in text.lower()
    assert "SERIAL_EPWREAD_PATCH_VALIDATION_STOP" in decision
    assert "historical" in decision.lower()
    assert "automatic executable successor" in capability.lower()
