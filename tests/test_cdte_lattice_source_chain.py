import json
from pathlib import Path

from tools.analyze_cdte_lattice_source_chain import analyze
from tools.check_cdte_a0_readiness import evaluate_readiness


ROOT = Path(__file__).resolve().parents[1]


def test_cdte_lattice_source_chain_remains_fail_closed():
    result = analyze()
    assert result["status"] == "source_chain_audited_but_execution_gate_remains_closed"
    assert result["williams1969"]["decision_206c"] == "printed_calculated_value_is_a_typographical_error"
    assert 6.474 < result["provisional_zero_k_derivation"]["a0_lower_a"]
    assert result["provisional_zero_k_derivation"]["a0_upper_a"] < 6.480
    assert result["provisional_zero_k_derivation"]["authorization"] == "planning_diagnostic_only"


def test_run_spec_records_audited_sources_and_excludes_non_cdte_citation():
    specification = json.loads(
        (ROOT / "first_principles/a0/cdte_a0_run_spec.json").read_text(
            encoding="utf-8"
        )
    )
    source = specification["structure"]["execution_lattice_constant_source"]
    anchor = source["absolute_anchor_candidate"]
    transformation = source["transformation_to_reference"]

    assert anchor["source_sha256"] == (
        "963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab"
    )
    assert anchor["status"] == "primary_cdte_xray_measurement_acquired_audited"
    assert not anchor["execution_value_authorized"]
    assert transformation["thermal_expansion_doi"] == (
        "10.1088/0022-3719/8/13/012"
    )
    assert transformation["thermal_expansion_source_sha256"] == (
        "521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237"
    )
    assert transformation["excluded_non_cdte_source"]["doi"] == (
        "10.1088/0022-3719/13/9/011"
    )
    assert transformation["uncovered_interval_to_room_temperature_k"] == [
        90,
        293.15,
    ]
    assert transformation["planning_diagnostic"]["authorization"] == (
        "planning_diagnostic_only_not_execution_input"
    )


def test_corrected_source_chain_still_blocks_execution_readiness():
    specification = json.loads(
        (ROOT / "first_principles/a0/cdte_a0_run_spec.json").read_text(
            encoding="utf-8"
        )
    )
    selection = json.loads(
        (
            ROOT
            / "first_principles/a0/cdte_pseudopotential_selection.json"
        ).read_text(encoding="utf-8")
    )
    report = evaluate_readiness(specification, selection)

    assert not report["ready_for_execution"]
    assert "execution_lattice_constant_provenance" in report["blocking_checks"]
    assert specification["structure"]["execution_lattice_constant_angstrom"] is None
    assert not specification["readiness_claim"]["ready_for_execution"]
