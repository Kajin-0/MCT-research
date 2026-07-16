from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_krishnamurthy1995_kane_closure import analyze_table

TABLE = Path("data/theory/krishnamurthy1995_hg078cd022_table2.csv")


def test_table_ii_hyperbola_reproduces_all_printed_mass_ratios() -> None:
    rows, summary = analyze_table(TABLE)

    assert len(rows) == 21
    reproduction = summary["table_reproduction"]
    assert reproduction["row_count"] == 21
    assert (
        reproduction["maximum_absolute_mass_ratio_fractional_error"]
        < 1.2e-3
    )
    assert reproduction["rms_mass_ratio_fractional_error"] < 5.0e-4
    assert (
        reproduction["maximum_relative_velocity_convention_difference"]
        < 6.0e-4
    )


def test_robust_paper_convention_velocity_drift_stays_below_five_percent() -> None:
    _, summary = analyze_table(TABLE)

    decision = summary["decision_rule"]
    drift = summary["equivalent_hyperbolic_velocity"]["drift_1_to_300k"]

    assert drift["maximum_absolute_drift"] == pytest.approx(
        0.027920782768194652
    )
    assert drift["rms_drift"] == pytest.approx(0.013169084405583148)
    assert drift["mean_signed_drift"] == pytest.approx(
        -0.009158253236138288
    )
    assert decision["large_P_T_renormalization_supported"] is False
    assert decision["decision"] == "large_P_T_renormalization_not_supported"


def test_reduced_gap_mass_velocity_is_convention_sensitive() -> None:
    _, summary = analyze_table(TABLE)

    reduced = summary["reduced_gap_mass_diagnostic"]
    assert reduced["drift_1_to_300k"]["maximum_absolute_drift"] == pytest.approx(
        0.08528275733074486
    )
    assert reduced["c_over_half_gap_300k"] == pytest.approx(
        0.8305131254001648
    )

    comparison = summary["mass_model_comparison_1_to_300k"]
    assert (
        comparison["gap_only_fixed_velocity"][
            "maximum_absolute_fractional_error"
        ]
        == pytest.approx(0.17783866335942466)
    )
    assert (
        comparison["gap_plus_reported_hyperbolic_velocity_forced_into_Eg_over_2"][
            "maximum_absolute_fractional_error"
        ]
        == pytest.approx(0.24647189303220207)
    )
    assert (
        comparison["complete_reported_hyperbola"][
            "maximum_absolute_fractional_error"
        ]
        < 1.2e-3
    )


def test_one_mev_low_temperature_turnover_is_not_resolved_closure() -> None:
    _, summary = analyze_table(TABLE)

    turnover = summary["low_temperature_turnover"]
    assert turnover["minimum_temperature_k"] == 20.0
    assert turnover["depth_relative_to_1k_mev"] == pytest.approx(1.04)
    assert abs(turnover["hyperbolic_velocity_drift_at_minimum"]) < 2.0e-4
    assert turnover["resolved_closure_effect"] is False
