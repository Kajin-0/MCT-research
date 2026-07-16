from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_seiler1990_figure7_digitization import analyze

DATA = Path("data/experimental/seiler1990_figure7_digitized.csv")


def test_marker_counts_and_specimen_separation() -> None:
    summary = analyze(DATA)

    assert summary["total_marker_count"] == 34
    assert summary["marker_count_by_sample"] == {"1": 14, "2": 11, "3": 9}
    assert "HSC" in summary["composition_admissibility"]["sample_2"]
    assert "independently" in summary["composition_admissibility"]["sample_3"]


def test_digitization_calibration_is_sub_mev() -> None:
    summary = analyze(DATA)
    digitization = summary["digitization"]

    assert digitization["temperature_half_width_k_by_panel"]["a"] == pytest.approx(
        0.381316
    )
    assert digitization["temperature_half_width_k_by_panel"]["c"] == pytest.approx(
        0.190658
    )
    assert max(digitization["gap_half_width_mev_by_panel"].values()) < 0.13


def test_published_nonlinear_shape_reproduces_markers_better_in_sample() -> None:
    summary = analyze(DATA)
    comparison = summary["specimen_offset_shape_comparison"]
    hansen = comparison["hansen_linear_temperature_shape"]["pooled"]
    seiler = comparison["seiler_published_nonlinear_shape"]["pooled"]

    assert hansen["rmse_mev"] == pytest.approx(1.8238791365621003)
    assert hansen["maximum_absolute_mev"] == pytest.approx(3.0133810013942934)
    assert seiler["rmse_mev"] == pytest.approx(1.0611342630539922)
    assert seiler["maximum_absolute_mev"] == pytest.approx(1.993890230121508)
    assert comparison["pooled_rmse_fractional_reduction"] == pytest.approx(
        0.41819924260213603
    )
    assert "in-sample" in comparison["decision"]


def test_low_temperature_markers_change_less_than_hansen_linear_shape() -> None:
    summary = analyze(DATA)
    checks = summary["approximately_5_to_10k_plateau_checks"]

    assert [item["sample_number"] for item in checks] == [1, 2, 3]
    assert [item["observed_gap_change_mev"] for item in checks] == pytest.approx(
        [0.498753, 0.249688, -0.099626]
    )
    assert [item["hansen_linear_change_mev"] for item in checks] == pytest.approx(
        [1.27787975622, 1.30761944001, 1.27828789274]
    )
    assert all(item["observed_minus_hansen_mev"] < 0.0 for item in checks)
