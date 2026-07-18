from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tools.analyze_gap_observation_identifiability import analyze

ROOT = Path(__file__).resolve().parents[1]
CHU = ROOT / "data/experimental/chu_sher_2008_table4_4_room_temperature_gap.csv"
MECHANISMS = ROOT / "data/evidence/hgcdte_gap_observation_mechanisms.csv"


def test_observation_audit_is_deterministic() -> None:
    first = analyze(CHU, MECHANISMS)
    second = analyze(CHU, MECHANISMS)
    assert first == second


def test_signed_residual_and_confounding_regression() -> None:
    result = analyze(CHU, MECHANISMS)
    source = result["source_residuals"]
    confounding = result["confounding_diagnostics"]

    assert source["positive_count"] == 7
    assert source["negative_count"] == 1
    assert source["metrics"]["mean_signed_mev"] == pytest.approx(
        9.039188186513025, abs=1e-12
    )
    assert source["metrics"]["rmse_mev"] == pytest.approx(
        11.991099243506273, abs=1e-12
    )
    assert source["constant_offset_removed_rmse_mev"] == pytest.approx(
        7.879056923034651, abs=1e-12
    )
    assert source["correlation_with_composition_x"] == pytest.approx(
        0.9611683700850845, abs=1e-12
    )
    assert source["correlation_with_alpha_at_gap"] == pytest.approx(
        0.9287975776520855, abs=1e-12
    )

    assert confounding["composition_alpha_at_gap_correlation"] == pytest.approx(
        0.9847966555523553, abs=1e-12
    )
    assert confounding["variance_inflation_factor"] == pytest.approx(
        33.139415598489734, abs=1e-10
    )
    assert confounding["normalized_two_predictor_condition_number"] == pytest.approx(
        11.425847998887601, abs=1e-10
    )


def test_diagnostic_predictors_do_not_identify_a_mechanism() -> None:
    result = analyze(CHU, MECHANISMS)
    predictors = result["diagnostic_predictors"]

    assert predictors["composition_x"]["leave_one_out_metrics"][
        "rmse_mev"
    ] == pytest.approx(2.9616857729793544, abs=1e-11)
    assert predictors["alpha_at_gap_cm1"]["leave_one_out_metrics"][
        "rmse_mev"
    ] == pytest.approx(4.015106930829681, abs=1e-11)
    assert predictors["composition_x_plus_alpha_at_gap"][
        "leave_one_out_metrics"
    ]["rmse_mev"] == pytest.approx(2.9308430707547215, abs=1e-11)

    assert result["identification_checks"][
        "composition_and_alpha_at_gap_are_separable"
    ] is False
    assert np.isfinite(
        predictors["composition_x_plus_alpha_at_gap"]["training_metrics"][
            "rmse_mev"
        ]
    )


def test_mechanism_decisions_are_sign_and_metadata_gated() -> None:
    result = analyze(CHU, MECHANISMS)
    mechanisms = result["mechanism_assessments"]
    decision = result["decision"]

    assert mechanisms["hg_vacancy_absorption_edge"]["sign_compatible"] is False
    assert mechanisms["absorption_edge_extraction_method"][
        "magnitude_sufficient"
    ] is False
    assert mechanisms["burstein_moss_band_filling"]["sign_compatible"] is True
    assert mechanisms["burstein_moss_band_filling"]["identified"] is False

    assert decision["hg_vacancy_explanation_rejected_by_sign"] is True
    assert decision["burstein_moss_retained_as_plausible_but_unidentified"] is True
    assert decision["universal_material_law_change_authorized"] is False
    assert decision["production_observation_operator_identified"] is False
    assert decision["measurement_class_metadata_must_be_preserved"] is True


def test_mechanism_ledger_is_provenance_bound() -> None:
    result = analyze(CHU, MECHANISMS)
    ledger = {row["mechanism"]: row for row in result["mechanism_ledger"]}

    assert ledger["hg_vacancy_absorption_edge"]["source_doi"] == "10.1063/1.2221411"
    assert ledger["burstein_moss_band_filling"]["source_doi"] == (
        "10.1016/0020-0891(80)90053-6"
    )
    assert ledger["chu_intrinsic_absorption_fit"]["source_doi"] == (
        "10.1016/0020-0891(91)90110-2"
    )
