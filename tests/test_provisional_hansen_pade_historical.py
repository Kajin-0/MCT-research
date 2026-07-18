from __future__ import annotations

from pathlib import Path

from tools.screen_provisional_hansen_pade_historical import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv"


def test_historical_screen_is_deterministic_and_complete() -> None:
    first = analyze(DATA)
    second = analyze(DATA)

    assert first["all_rows"]["metrics"] == second["all_rows"]["metrics"]
    assert first["screen_checks"] == second["screen_checks"]
    assert first["all_rows"]["count"] == 18
    assert first["independently_composed_present_samples"]["count"] == 3
    assert first["legacy_compositions_not_audited_by_seiler"]["count"] == 14


def test_provisional_model_passes_bounded_historical_screen() -> None:
    result = analyze(DATA)
    assert all(result["screen_checks"].values())
    assert result["decision"]["historical_screen_passed"] is True
    assert result["decision"]["provisional_status_retained"] is True
    assert result["decision"]["production_equation_authorized"] is False
    assert result["decision"]["static_composition_law_is_controlling_limitation"] is True


def test_historical_screen_preserves_all_comparators() -> None:
    result = analyze(DATA)
    expected = {
        "hansen",
        "published_seiler",
        "laurenti",
        "provisional_hansen_pade",
    }
    assert set(result["all_rows"]["metrics"]) == expected
    assert set(result["independently_composed_present_samples"]["metrics"]) == expected
    assert set(result["legacy_compositions_not_audited_by_seiler"]["metrics"]) == expected
