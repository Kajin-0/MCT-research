from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.audit_blue1964_sign_identifiability import (
    HIGH_ENERGY_NEAR_DEGENERACY_EV,
    SOURCE_COUNTEREXAMPLE,
    audit,
    quantize,
)


ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "experimental" / "blue1964_table2_optical_gaps.csv"
REFERENCE = ROOT / "validation" / "blue1964_sign_identifiability_reference.json"
DECISION_NOTE = (
    ROOT / "docs" / "insights" / "0029_blue1964_signed_gap_noncommensurability.md"
)


def _result() -> dict[str, object]:
    return audit(OBSERVATIONS)


def test_source_counterexample_is_exact() -> None:
    assert SOURCE_COUNTEREXAMPLE == {
        "temperature_k": 50.0,
        "actual_edge_gap_ev": 0.0,
        "band_curvature_scale_ev": 0.03,
        "source_status": "hypothetical_example_explicitly_stated_by_Blue_1964",
    }
    result = _result()
    assert result["source_counterexample"] == SOURCE_COUNTEREXAMPLE
    assert result["identifiability_decision"][
        "blue_parameter_equals_actual_edge_gap"
    ] is False


def test_high_energy_near_degeneracy_set_is_exact() -> None:
    assert HIGH_ENERGY_NEAR_DEGENERACY_EV == (0.02, 0.03, 0.04)
    result = _result()["source_high_energy_near_degeneracy"]
    assert result["trial_curvature_scales_ev"] == pytest.approx([0.02, 0.03, 0.04])
    assert result["magnitude_identifiability_status"] == (
        "weak_non_unique_in_the_declared_high_absorption_comparison"
    )


def test_all_blue_rows_remain_positive_and_signed_gap_ineligible() -> None:
    contract = _result()["observation_contract"]
    assert contract["row_count"] == 7
    assert contract["parameter_min_ev"] == pytest.approx(0.03)
    assert contract["parameter_max_ev"] == pytest.approx(0.365)
    assert contract["all_parameters_positive"] is True
    assert contract["all_rows_signed_gap_eligible"] is False
    assert contract["measurement_class"] == (
        "theory_conditioned_positive_optical_gap_parameter"
    )
    assert contract["fit_region_alpha_cm_inverse"] == "approximately_above_1e3"


def test_sign_and_unique_magnitude_are_not_identified() -> None:
    decision = _result()["identifiability_decision"]
    assert decision == {
        "source_parameterization_represents_signed_band_order": False,
        "blue_parameter_equals_actual_edge_gap": False,
        "sign_of_modern_Gamma6_minus_Gamma8_identified": False,
        "one_to_one_gap_magnitude_identified": False,
        "direct_signed_gap_residual_ranking_authorized": False,
        "external_validated_observation_operator_required": True,
        "universal_numerical_correction_identified": False,
    }


def test_audit_performs_no_fit_correction_or_signed_model_evaluation() -> None:
    bookkeeping = _result()["analysis_bookkeeping"]
    assert bookkeeping == {
        "fitted_parameter_count": 0,
        "correction_coefficient_count": 0,
        "signed_model_evaluations": 0,
        "source_rows_modified": 0,
    }
    scientific = _result()["scientific_decision"]
    assert scientific["blue_table_directly_commensurate_with_signed_gap_laws"] is False
    assert scientific["production_equation_authorized"] is False
    assert scientific["manuscript_authorized"] is False


def test_immutable_certificate_regenerates_exactly() -> None:
    expected = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert quantize(_result()) == expected


def test_decision_note_preserves_source_and_claim_boundaries() -> None:
    text = DECISION_NOTE.read_text(encoding="utf-8")
    required = (
        "actual energy gap at 50 K = 0",
        "band shape corresponds to a gap scale = 0.03 eV",
        "0.02 eV\n0.03 eV\n0.04 eV",
        "does not identify the sign or a unique magnitude",
        "excluded from direct residual ranking of signed gap equations",
        "does not establish:\n\n- the corrected signed gap",
    )
    assert all(token in text for token in required)
