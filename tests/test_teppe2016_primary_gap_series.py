from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_teppe2016_primary_gap_series import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/teppe2016_primary_magneto_optical_gap_points.csv"


def test_teppe_audit_is_deterministic() -> None:
    assert analyze(DATA) == analyze(DATA)


def test_reported_composition_conflict_reverses_model_ranking() -> None:
    result = analyze(DATA)
    assert result["winner_by_hypothesis"] == {
        "figure_and_main_text_x_0p175": "laurenti",
        "methods_x_0p170": "provisional_hansen_pade",
    }
    assert result["decision"][
        "model_ranking_reverses_across_reported_compositions"
    ] is True
    assert result["decision"]["strict_universal_model_promotion_authorized"] is False


def test_hypothesis_metrics_match_reference_values() -> None:
    result = analyze(DATA)["reported_composition_hypotheses"]
    figure = result["figure_and_main_text_x_0p175"]
    methods = result["methods_x_0p170"]

    assert figure["laurenti"]["rmse_mev"] == pytest.approx(4.200495693486347, abs=1e-10)
    assert figure["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        8.37748159526179, abs=1e-10
    )
    assert methods["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        5.066541241467016, abs=1e-10
    )
    assert methods["hansen"]["rmse_mev"] == pytest.approx(5.353313823999478, abs=1e-10)


def test_profiled_composition_exposes_model_dependent_calibration() -> None:
    fitted = analyze(DATA)["sample_a_profiled_composition"]
    assert fitted["provisional_hansen_pade"]["best_composition_x"] == pytest.approx(
        0.170466, abs=1e-6
    )
    assert fitted["laurenti"]["best_composition_x"] == pytest.approx(0.175068, abs=1e-6)
    assert fitted["provisional_hansen_pade"]["rmse_mev"] < 2.0
    assert fitted["laurenti"]["rmse_mev"] > 4.0


def test_source_is_primary_but_not_strict_fit_authority() -> None:
    result = analyze(DATA)
    assert result["source"]["point_count"] == 5
    assert result["source"]["composition_conflict_delta_x"] == pytest.approx(0.005)
    assert result["decision"]["teppe_series_admitted_as_primary_benchmark"] is True
    assert result["decision"][
        "provisional_hansen_pade_global_leading_claim_withdrawn"
    ] is True
