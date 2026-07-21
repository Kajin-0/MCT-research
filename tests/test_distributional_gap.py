from __future__ import annotations

import math

import pytest

from mct_research.distributional_gap import (
    gaussian_opposite_sign_fraction,
    linearized_composition_gap_statistics,
)
from mct_research.gap_models import laurenti_gap_ev


def test_gaussian_opposite_sign_reference_values() -> None:
    assert gaussian_opposite_sign_fraction(1.0, 1.0) == pytest.approx(
        0.15865525393145707
    )
    assert gaussian_opposite_sign_fraction(0.0, 0.0) == 0.5
    assert gaussian_opposite_sign_fraction(1.0, 0.0) == 0.0


def test_linear_model_propagation_is_exact() -> None:
    def model(x: float, temperature_k: float) -> float:
        return 2.0 * x + 3.0e-4 * temperature_k - 0.5

    result = linearized_composition_gap_statistics(
        model,
        0.2,
        0.01,
        100.0,
    )

    assert result.gap_at_mean_ev == pytest.approx(-0.07)
    assert result.mean_gap_ev == pytest.approx(-0.07)
    assert result.composition_curvature_bias_ev == pytest.approx(0.0, abs=1.0e-12)
    assert result.gap_sigma_ev == pytest.approx(0.02)
    assert result.dgap_dx_ev == pytest.approx(2.0)
    assert result.dgap_dtemperature_ev_per_k == pytest.approx(3.0e-4)
    assert result.critical_temperature_sigma_k == pytest.approx(66.6666666667)
    assert result.opposite_sign_fraction == pytest.approx(
        0.5 * math.erfc(0.07 / (math.sqrt(2.0) * 0.02))
    )


def test_quadratic_curvature_shift_matches_gaussian_moment() -> None:
    def model(x: float, temperature_k: float) -> float:
        del temperature_k
        return 3.0 * x**2 - 0.1

    result = linearized_composition_gap_statistics(
        model,
        0.2,
        0.01,
        77.0,
    )

    assert result.gap_at_mean_ev == pytest.approx(0.02)
    assert result.d2gap_dx2_ev == pytest.approx(6.0, rel=1.0e-7)
    assert result.composition_curvature_bias_ev == pytest.approx(3.0e-4)
    assert result.mean_gap_ev == pytest.approx(0.0203)


def test_teppe_near_critical_laurenti_screen() -> None:
    result = linearized_composition_gap_statistics(
        laurenti_gap_ev,
        0.155,
        0.001,
        77.0,
    )

    assert result.gap_at_mean_ev == pytest.approx(-4.78120358e-5, abs=1.0e-12)
    assert result.gap_sigma_ev == pytest.approx(1.71910851e-3, rel=1.0e-8)
    assert result.critical_temperature_sigma_k == pytest.approx(
        4.46315319, rel=1.0e-8
    )
    assert result.opposite_sign_fraction == pytest.approx(
        0.488960646, rel=1.0e-8
    )


def test_zero_composition_width_is_deterministic() -> None:
    result = linearized_composition_gap_statistics(
        laurenti_gap_ev,
        0.175,
        0.0,
        77.0,
    )
    assert result.gap_sigma_ev == 0.0
    assert result.composition_curvature_bias_ev == 0.0
    assert result.critical_temperature_sigma_k == 0.0
    assert result.opposite_sign_fraction == 0.0


def test_input_validation() -> None:
    with pytest.raises(ValueError, match="mean_composition"):
        linearized_composition_gap_statistics(laurenti_gap_ev, -0.1, 0.001, 77.0)
    with pytest.raises(ValueError, match="composition_sigma"):
        linearized_composition_gap_statistics(laurenti_gap_ev, 0.2, -0.001, 77.0)
    with pytest.raises(ValueError, match="physical interval"):
        linearized_composition_gap_statistics(
            laurenti_gap_ev,
            0.00005,
            0.001,
            77.0,
        )
    with pytest.raises(ValueError, match="non-negative"):
        gaussian_opposite_sign_fraction(0.01, -0.001)
