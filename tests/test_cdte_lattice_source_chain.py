import json
from pathlib import Path

from tools.analyze_cdte_lattice_source_chain import analyze
from tools.check_cdte_a0_readiness import evaluate_readiness


ROOT = Path(__file__).resolve().parents[1]


def test_historical_source_chain_analyzer_remains_planning_diagnostic():
    result = analyze()
    assert result["status"] == "source_chain_audited_but_execution_gate_remains_closed"
    assert result["williams1969"]["decision_206c"] == "printed_calculated_value_is_a_typographical_error"
    assert 6.474 < result["provisional_zero_k_derivation"]["a0_lower_a"]
    assert result["provisional_zero_k_derivation"]["a0_upper_a"] < 6.480
    assert result["provisional_zero_k_derivation"]["authorization"] == "planning_diagnostic_only"


def test_run_spec_records_bounded_primary_source_chain_and_exclusion():
    specification = json.loads(
        (ROOT / "first_principles/a0/cdte_a0_run_spec.json").read_text(
            encoding="utf-8"
        )
    )
    structure = specification["structure"]
    source = structure["execution_lattice_constant_source"]
    anchor = source["absolute_anchor_candidate"]
    transformation = source["transformation_to_reference"]

    assert structure["execution_lattice_constant_angstrom"] == 6.476035479332049
    assert source["source_type"] == "primary_experimental_with_bounded_transform"
    assert anchor["source_sha256"] == (
        "963891204abd0b3c434297eec3a1d337c7bc67a3b937eda4bdfc373746702bab"
    )
    assert anchor["status"].startswith("primary_cdte_xray_measurement_acquired_audited")
    assert not anchor["execution_value_authorized"]
    assert transformation["thermal_expansion_doi"] == [
        "10.1088/0022-3719/8/13/012",
        "10.1364/AO.11.000841",
    ]
    assert transformation["thermal_expansion_source_sha256"] == (
        "832c7b191d1a93a5f828e63125ea8dcd18e42c998b33f77b3ee1239f54a5afe7"
    )
    assert transformation["low_temperature_source_sha256"] == (
        "521e58912b46c6fba70f6e7c24135d79e8aa50d8ddc93addbaf97c4d38f74237"
    )
    assert transformation["excluded_non_cdte_source"]["doi"] == (
        "10.1088/0022-3719/13/9/011"
    )
    assert transformation["integration_temperature_bounds_k"] == [0, 293.15]
    assert transformation["uncertainty_model_status"] == (
        "approved_conservative_interval_model"
    )
    assert source["execution_uncertainty"]["type"] == (
        "conservative_absolute_bound_not_standard_uncertainty"
    )
    assert source["execution_uncertainty"]["volume_sensitivity_gate_passed"] is True


def test_bounded_source_chain_passes_provenance_but_runtime_still_blocks():
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
    assert "execution_lattice_constant_provenance" not in report["blocking_checks"]
    assert {
        "quantum_espresso_installed_binary_recorded",
        "quantum_espresso_release_syntax_checked",
        "abinit_installed_binary_recorded",
        "abinit_release_syntax_checked",
        "runtime_pseudopotential_hashes_verified",
        "render_manifests_recorded",
    }.issubset(report["blocking_checks"])
    assert specification["structure"]["execution_lattice_constant_angstrom"] > 0
    assert not specification["readiness_claim"]["ready_for_execution"]
