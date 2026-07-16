from __future__ import annotations

import pytest

from tools.analyze_teppe2016_constant_velocity_null import analyze


def test_signed_gap_transition_is_preserved() -> None:
    _, summary = analyze()
    assert summary["sample_a_gap_annotations_mev"] == [5.0, 28.0, 36.0, 56.0]
    assert summary["sample_b_gap_annotations_mev"] == [-24.0, -14.0, 0.0, 18.0]
    assert summary["sample_b_critical_temperature_k"] == 77.0


def test_quoted_velocity_uncertainty_is_about_five_percent() -> None:
    _, summary = analyze()
    assert summary["velocity_m_per_s"] == 1.07e6
    assert summary["velocity_sigma_m_per_s"] == 5.0e4
    assert summary["velocity_relative_sigma"] == pytest.approx(0.04672897196261682)


def test_krishnamurthy_drift_is_inside_teppe_velocity_scale() -> None:
    _, summary = analyze()
    assert summary["krishnamurthy_max_velocity_drift_1_300k"] == pytest.approx(
        0.027920782768194652
    )
    assert summary["krishnamurthy_drift_to_teppe_sigma_ratio"] == pytest.approx(
        0.5975047512393655
    )
    assert summary["constant_velocity_null_supported"] is True


def test_full_eight_band_matrix_element_is_not_claimed() -> None:
    _, summary = analyze()
    assert summary["full_8band_P_identified"] is False
    assert "Gamma7" in summary["model_boundary"]
    assert "not direct validation" in summary["claim_boundary"]
