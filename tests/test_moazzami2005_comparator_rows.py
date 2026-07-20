from pathlib import Path

import pytest

from tools.analyze_moazzami2005_manuscript_comparators import analyze

ROOT = Path(__file__).resolve().parents[1]


def test_complete_candidate_residual_rows() -> None:
    result = analyze(ROOT)
    expected_models = {
        "hansen",
        "published_seiler",
        "laurenti",
        "provisional_hansen_pade",
    }
    for specimen in result["specimens"]:
        assert specimen["composition_sigma_x"] is None
        assert specimen["model_candidate_nominal_winners"] == ["published_seiler"]
        assert len(specimen["candidates"]) == 14
        for row in specimen["candidates"]:
            assert set(row["absolute_residuals_mev"]) == expected_models


def test_published_seiler_predictions() -> None:
    by_id = {item["specimen_id"]: item for item in analyze(ROOT)["specimens"]}
    assert by_id["moazzami2005_x0.226"]["model_predictions_mev"][
        "published_seiler"
    ] == pytest.approx(190.11175067821742, abs=1.0e-12)
    assert by_id["moazzami2005_x0.310"]["model_predictions_mev"][
        "published_seiler"
    ] == pytest.approx(304.0585564043113, abs=1.0e-12)
