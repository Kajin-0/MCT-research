from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_teppe2016_primary_gap_series import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/teppe2016_primary_magneto_optical_gap_points.csv"


def test_teppe_audit_is_deterministic() -> None:
    assert analyze(DATA) == analyze(DATA)


def test_lower_precision_sensitivity_changes_model_ranking() -> None:
    result = analyze(DATA)
    assert result["winner_by_interpretation"] == {
        "primary_nominal_x_0p175": "laurenti",
        "lower_precision_methods_sensitivity_x_0p17": "provisional_hansen_pade",
    }
    assert result["decision"][
        "model_ranking_changes_under_lower_precision_sensitivity"
    ] is True
    assert result["decision"][
        "methods_value_is_independent_exact_composition_measurement"
    ] is False
    assert result["decision"]["primary_nominal_composition_for_benchmark"] == pytest.approx(0.175)
    assert result["decision"]["strict_universal_model_promotion_authorized"] is False


def test_interpretation_metrics_match_reference_values() -> None:
    result = analyze(DATA)["composition_precision_interpretations"]
    nominal = result["primary_nominal_x_0p175"]
    sensitivity = result["lower_precision_methods_sensitivity_x_0p17"]

    assert nominal["laurenti"]["rmse_mev"] == pytest.approx(4.200495693486347, abs=1e-10)
    assert nominal["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        8.37748159526179, abs=1e-10
    )
    assert sensitivity["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        5.066541241467016, abs=1e-10
    )
    assert sensitivity["hansen"]["rmse_mev"] == pytest.approx(
        5.353313823999478, abs=1e-10
    )


def test_profiled_composition_exposes_model_dependent_calibration() -> None:
    fitted = analyze(DATA)["sample_a_profiled_composition"]
    assert fitted["provisional_hansen_pade"]["best_composition_x"] == pytest.approx(
        0.170466, abs=1e-6
    )
    assert fitted["laurenti"]["best_composition_x"] == pytest.approx(0.175068, abs=1e-6)
    assert fitted["provisional_hansen_pade"]["rmse_mev"] < 2.0
    assert fitted["laurenti"]["rmse_mev"] > 4.0


def test_source_is_primary_but_composition_uncertainty_blocks_strict_ranking() -> None:
    result = analyze(DATA)
    assert result["source"]["point_count"] == 5
    assert result["source"]["sample_a_primary_nominal_composition"] == pytest.approx(0.175)
    assert result["source"]["sample_a_methods_lower_precision_summary"] == pytest.approx(0.17)
    assert result["decision"]["teppe_series_admitted_as_primary_benchmark"] is True
    assert result["decision"]["laurenti_global_promotion_authorized"] is False
    assert result["decision"][
        "provisional_hansen_pade_global_leading_claim_withdrawn"
    ] is True
