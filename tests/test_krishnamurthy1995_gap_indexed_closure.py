from __future__ import annotations

import csv
from pathlib import Path

import pytest

from tools.analyze_krishnamurthy1995_gap_indexed_closure import analyze

TABLE = Path("data/theory/krishnamurthy1995_hg078cd022_table2.csv")
LEDGER = Path(
    "data/theory/krishnamurthy1995_hg078cd022_gap_indexed_closure.csv"
)


def test_literal_direct_proportionality_fails_table_ii() -> None:
    _, summary = analyze(TABLE)
    strict = summary["strict_direct_proportionality_1_300k"]

    assert strict["c_over_gap_fractional_change_1_to_300k"] == pytest.approx(
        -0.19773562036174552
    )
    assert strict["c_ratio_from_gap_ratio"][
        "maximum_absolute_fractional_error"
    ] == pytest.approx(0.24647189303220185)
    assert strict["mass_ratio_from_gap_ratio"][
        "maximum_absolute_fractional_error"
    ] == pytest.approx(0.17783866335942466)
    assert strict["decision"] == "strict_mathematical_proportionality_not_supported"


def test_gap_indexed_relations_predict_heldout_mass_below_two_percent() -> None:
    _, summary = analyze(TABLE)
    diagnostic = summary["gap_indexed_affine_diagnostic"]

    assert diagnostic["c_of_gap"]["intercept_ev"] == pytest.approx(
        0.028075264018913356
    )
    assert diagnostic["c_of_gap"]["slope"] == pytest.approx(
        0.275577447670434
    )
    assert diagnostic["c_of_gap"][
        "heldout_maximum_absolute_error_mev"
    ] == pytest.approx(2.466971273469551)
    assert diagnostic["gamma_of_gap"][
        "heldout_fractional_metrics"
    ]["maximum_absolute_fractional_error"] == pytest.approx(
        0.025032150891851956
    )
    assert diagnostic["reconstructed_mass_ratio"][
        "heldout_fractional_metrics"
    ]["maximum_absolute_fractional_error"] == pytest.approx(
        0.012827882049095574
    )


def test_low_temperature_turnover_does_not_resolve_extra_temperature_variable() -> None:
    _, summary = analyze(TABLE)
    turnover = summary["low_temperature_turnover_identifiability"]

    assert turnover["gap_difference_mev"] == pytest.approx(-0.11)
    assert turnover["c_difference_mev"] == pytest.approx(0.4)
    assert turnover["gamma_difference"] == pytest.approx(-0.0384)
    assert turnover["resolved_independent_temperature_effect"] is False


def test_low_temperature_gap_indexed_relations_must_not_be_extrapolated_to_600k() -> None:
    _, summary = analyze(TABLE)
    high = summary["high_temperature_stop"]

    assert high["maximum_c_fractional_error_350_600k"] == pytest.approx(
        0.45744249936194736
    )
    assert high["maximum_gamma_fractional_error_350_600k"] == pytest.approx(
        0.3560457899972417
    )
    assert high["maximum_mass_fractional_error_350_600k"] == pytest.approx(
        0.1663787936226212
    )


def test_committed_ledger_matches_fresh_analysis() -> None:
    expected_rows, _ = analyze(TABLE)
    recorded_rows = list(
        csv.DictReader(LEDGER.read_text(encoding="utf-8").splitlines())
    )

    assert len(recorded_rows) == len(expected_rows) == 21
    for expected, recorded in zip(expected_rows, recorded_rows, strict=True):
        assert set(recorded) == set(expected)
        for name, value in expected.items():
            if name == "scope":
                assert recorded[name] == value
            else:
                assert float(recorded[name]) == pytest.approx(
                    value,
                    rel=1.0e-12,
                    abs=1.0e-12,
                )
