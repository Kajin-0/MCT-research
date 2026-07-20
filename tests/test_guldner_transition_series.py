from __future__ import annotations

import math
from pathlib import Path

from mct_research.historical_gap_models import (
    weiler_1977_gap_ev,
    wiley_dexter_1969_gap_ev,
)
from tools.analyze_guldner_transition_series import analyze

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "data/evidence/hgcdte_guldner_camassel_low_temperature_series.json"


def result() -> dict[str, object]:
    return analyze(SERIES)


def test_wiley_and_weiler_reference_values() -> None:
    assert math.isclose(
        wiley_dexter_1969_gap_ev(0.203, 77),
        0.110599,
        abs_tol=1e-12,
    )
    assert math.isclose(
        weiler_1977_gap_ev(0.203, 77),
        0.094509,
        abs_tol=1e-12,
    )


def test_guldner_series_preserves_secondary_primary_boundary() -> None:
    data = result()
    assert data["row_count"] == 12
    assert data["temperature_K"] == 4.2
    assert data["data_status"] == (
        "secondary exact transcription with primary-figure consistency screen"
    )
    assert data["decision"]["primary_exact_point_promotion_authorized"] is False


def test_transition_composition_rejects_schmit_and_wiley_only() -> None:
    data = result()
    assert data["reported_transition_interval"] == [0.16, 0.17]
    assert data["decision"]["transition_interval_rejected_models"] == [
        "schmit_stelzer_1969",
        "wiley_dexter_1969",
    ]
    assert set(data["decision"]["transition_interval_satisfied_models"]) == {
        "weiler_1977",
        "hansen_1982",
        "seiler_1990",
        "laurenti_reconstructed",
        "provisional_hansen_pade",
        "chu_1983",
    }


def test_weiler_crossing_is_inside_but_wiley_crossing_is_below() -> None:
    comparisons = result()["model_comparisons"]
    assert 0.1641 < comparisons["weiler_1977"]["critical_composition"] < 0.1642
    assert comparisons["weiler_1977"]["critical_composition_status"] == (
        "inside_reported_transition_interval"
    )
    assert 0.1562 < comparisons["wiley_dexter_1969"]["critical_composition"] < 0.1564
    assert comparisons["wiley_dexter_1969"]["critical_composition_status"] == (
        "below_reported_transition_interval"
    )


def test_hansen_and_pade_are_numerically_indistinguishable_on_this_screen() -> None:
    data = result()
    assert data["decision"]["lowest_mae_model"] == "provisional_hansen_pade"
    assert data["model_comparisons"]["provisional_hansen_pade"]["mae_meV"] < 5.38
    assert data["model_comparisons"]["hansen_1982"]["mae_meV"] < 5.44
    assert data["decision"]["hansen_pade_mae_difference_meV"] < 0.06
    assert data["decision"]["hansen_over_pade_ranking_authorized"] is False


def test_low_temperature_series_does_not_authorize_global_fit() -> None:
    decision = result()["decision"]
    assert decision["strict_material_law_ranking_authorized"] is False
    assert decision["new_universal_gap_refit_authorized"] is False
