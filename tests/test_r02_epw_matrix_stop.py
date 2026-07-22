from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "first_principles/b0/qe76_epw61_matrix_export_capability_result.json"
DECISION = ROOT / "research/decision_records/2026-07-22-r02-epw-lower-fan-matrix-stop.md"
STATE = ROOT / "research/programs/finite_temperature_kane/state.md"


def _load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_source_state_is_fully_pinned() -> None:
    result = _load()
    source = result["source"]
    assert source["repository"] == "QEF/q-e"
    assert source["release_tag"] == "qe-7.6"
    assert source["tag_commit_sha"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["epw_version"] == "6.1"
    assert source["files"]["EPW/src/selfen.f90"]["git_blob_sha"] == (
        "be4858854d1ab26d27b3acf52a9a30c21fa8b472"
    )
    assert source["files"]["EPW/src/wfpt.f90"]["git_blob_sha"] == (
        "526405829090c4214eb87cff2af90bbd257efe3d"
    )


def test_lower_fan_information_gate_fails_for_the_declared_reason() -> None:
    result = _load()
    lower = result["source_findings"]["lower_fan"]
    assert lower["complex_vertex_available"] is True
    assert lower["complete_matrix_already_computed"] is False
    assert lower["observational_export_without_new_contraction"] is False
    assert "abs(epf17" in lower["standard_contraction"]
    assert "sigmar_all" in lower["standard_accumulator"]


def test_upper_fan_and_debye_waller_are_not_misclassified() -> None:
    result = _load()
    upper = result["source_findings"]["upper_fan"]
    dw = result["source_findings"]["debye_waller"]
    assert upper["complete_complex_intermediate_available"] is True
    assert upper["standard_output_is_band_diagonal_real"] is True
    assert dw["complete_complex_intermediate_available"] is True
    assert dw["standard_output_is_band_diagonal_real"] is True


def test_mandatory_gate_returns_stop_without_weighted_partial_pass() -> None:
    result = _load()
    gates = result["mandatory_gates"]
    assert gates["pinned_qe76_source"] == "PASS"
    assert gates["candidate_insulating_nonpolar_upstream_fixture"] == "PASS"
    assert gates["lower_fan_complex_matrix_exists_before_diagonal_reduction"] == "FAIL"
    assert gates["disabled_by_default_exporter_can_be_observational_only"] == "FAIL"
    assert gates["all_required_components_exportable_without_algorithm_change"] == "FAIL"
    assert result["decision"]["classification"] == "STOP"


def test_no_build_or_material_run_was_silently_authorized() -> None:
    result = _load()
    execution = result["execution"]
    assert execution["qe_epw_build_executed"] is False
    assert execution["upstream_test_executed"] is False
    assert execution["combined_fixture_executed"] is False
    assert execution["material_calculation_executed"] is False
    authorization = result["authorization"]
    assert all(value is False for value in authorization.values())
    assert result["decision"]["automatic_followup_authorized"] is False
    assert result["decision"]["cdte_smoke_test_design_authorized"] is False


def test_decision_record_preserves_narrow_claim_boundary() -> None:
    text = DECISION.read_text(encoding="utf-8")
    assert "does not establish that QE or EPW is incorrect" in text
    assert "scientific implementation, not an exporter" in text
    assert "No QE/EPW build" in text
    assert "CdTe, HgTe, HgCdTe" in text


def test_program_state_preserves_stop_and_fail_closed_continuation() -> None:
    text = STATE.read_text(encoding="utf-8")
    assert "observational full-matrix exporter path" in text
    assert "terminated" in text
    assert "## Selected continuation architecture" in text
    assert "Sigma_SR_lower_Fan" in text
    assert "Sigma_LR_Frohlich" in text
    assert "external matrix Fan contraction" in text
    assert "CdTe, HgTe, or alloy AHC calculations" in text
    assert "Not authorized" in text
