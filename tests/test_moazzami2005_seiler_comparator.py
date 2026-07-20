from pathlib import Path

import pytest

from tools.analyze_moazzami2005_manuscript_comparators import analyze

ROOT = Path(__file__).resolve().parents[1]


def test_seiler_comparator_and_claim_gate() -> None:
    result = analyze(ROOT)
    decision = result["decision"]
    assert decision["published_seiler_comparator_included"] is True
    assert decision["all_fitted_model_candidates_nominally_prefer_published_seiler"] is True
    assert decision["strict_material_model_ranking_authorized"] is False


def test_seiler_hansen_nominal_separation() -> None:
    decision = analyze(ROOT)["decision"]
    assert decision["hansen_seiler_prediction_separation_mev_range"] == pytest.approx(
        [0.17655559568868284, 0.2546117537825976], abs=1.0e-12
    )
    assert decision["minimum_fitted_candidate_nominal_winner_margin_mev"] == pytest.approx(
        0.17655559568868284, abs=1.0e-12
    )
