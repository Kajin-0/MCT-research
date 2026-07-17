from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.derive_cdte_execution_lattice import derive


DECISION_PATH = Path("first_principles/a0/cdte_lattice_execution_decision.json")
SOURCE_PATH = Path("first_principles/a0/browder1972_optica_table_source.json")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _synthetic_acquisition() -> dict:
    source = _load(SOURCE_PATH)
    return {
        "success": True,
        "citation": source["citation"],
        "source_url": source["publisher_source"]["url"],
        "source_sha256": "f" * 64,
        "table_validation": {
            "exact_match": True,
            "publisher_rows_sha256": source["publisher_source"][
                "canonical_table_rows_sha256"
            ],
            "maximum_temperature_difference_k": 0.0,
            "maximum_alpha_difference_1e6_per_k": 0.0,
        },
    }


def test_committed_decision_passes_declared_gate() -> None:
    decision = _load(DECISION_PATH)
    assert decision["status"] == (
        "authorized_for_fixed_volume_a0_sensitivity_not_metrology_reference"
    )
    assert decision["decision"][
        "physical_volume_provenance_gate_passed_for_a0_sensitivity"
    ] is True
    assert decision["reference_lattice"]["central_angstrom"] == pytest.approx(
        6.476035479332049, abs=1e-14
    )
    assert decision["reference_lattice"][
        "conservative_absolute_bound_angstrom"
    ] == pytest.approx(0.0018149594091957418, abs=1e-15)
    assert decision["reference_lattice"]["uncertainty_type"] == (
        "conservative_absolute_bound_not_standard_uncertainty"
    )
    assert decision["cross_checks"]["all_contained"] is True
    assert all(decision["gate_components"].values())


def test_volume_provenance_bound_is_small_relative_to_a0_offset() -> None:
    gate = _load(DECISION_PATH)["volume_sensitivity_gate"]
    assert gate["passed"] is True
    assert gate["maximum_absolute_volume_fraction"] < 0.001
    assert gate["fraction_of_intended_offset"] < 0.20
    assert gate["intended_one_sided_a0_volume_offset"] == 0.005


def test_derivation_reproduces_committed_numerical_decision() -> None:
    expected = _load(DECISION_PATH)
    actual = derive(_synthetic_acquisition())

    assert actual["reference_lattice"] == expected["reference_lattice"]
    assert actual["uncertainty_components"] == expected["uncertainty_components"]
    assert actual["cross_checks"] == expected["cross_checks"]
    assert actual["volume_sensitivity_gate"] == expected["volume_sensitivity_gate"]
    assert actual["gate_components"] == expected["gate_components"]
    assert actual["decision"] == expected["decision"]
    assert actual["source_chain"]["bridge_shape"][
        "canonical_table_sha256"
    ] == expected["source_chain"]["bridge_shape"]["canonical_table_sha256"]


def test_bound_is_conservative_not_a_standard_uncertainty() -> None:
    decision = _load(DECISION_PATH)
    assert decision["decision"]["metrology_grade_zero_k_lattice_claim"] is False
    assert decision["decision"]["quasiharmonic_path_authorized"] is False
    assert decision["decision"][
        "new_electronic_structure_run_authorized_by_this_manifest"
    ] is False
    assert decision["uncertainty_components"]["combination_rule"] == (
        "linear sum of absolute component bounds"
    )
