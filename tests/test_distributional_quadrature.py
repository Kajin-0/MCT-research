from __future__ import annotations

import math

import pytest

from mct_research.distributional_quadrature import (
    gaussian_critical_temperature_distribution,
    gaussian_gap_moments,
)
from mct_research.gap_models import laurenti_gap_ev


def normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def test_linear_gap_moments_match_gaussian_transformation() -> None:
    def model(x: float, temperature_k: float) -> float:
        return 2.0 * x + 3.0e-4 * temperature_k - 0.5

    result = gaussian_gap_moments(
        model,
        0.2,
        0.01,
        100.0,
        quadrature_order=128,
    )

    assert result.mean_gap_ev == pytest.approx(-0.07, abs=1.0e-13)
    assert result.gap_sigma_ev == pytest.approx(0.02, rel=1.0e-11)
    assert result.gap_skewness == pytest.approx(0.0, abs=1.0e-11)
    assert result.negative_gap_probability == pytest.approx(normal_cdf(3.5), rel=1.0e-9)
    assert result.positive_gap_probability == pytest.approx(1.0 - normal_cdf(3.5), rel=1.0e-9)
    assert result.mean_approximation_error_ev == pytest.approx(0.0, abs=1.0e-12)
    assert result.sigma_approximation_error_ev == pytest.approx(0.0, abs=1.0e-12)


def test_quadratic_gap_moments_retain_curvature() -> None:
    def model(x: float, temperature_k: float) -> float:
        del temperature_k
        return 3.0 * x**2 - 0.1

    result = gaussian_gap_moments(
        model,
        0.2,
        0.01,
        77.0,
        quadrature_order=128,
    )

    expected_sigma = 3.0 * math.sqrt(2.0 * 0.01**4 + 4.0 * 0.2**2 * 0.01**2)
    assert result.mean_gap_ev == pytest.approx(0.0203, abs=1.0e-12)
    assert result.gap_sigma_ev == pytest.approx(expected_sigma, rel=1.0e-10)
    assert result.mean_approximation_error_ev == pytest.approx(0.0, abs=1.0e-10)


def test_physical_composition_bound_changes_effective_moments() -> None:
    def model(x: float, temperature_k: float) -> float:
        del temperature_k
        return x

    result = gaussian_gap_moments(
        model,
        0.005,
        0.01,
        0.0,
        quadrature_order=256,
    )

    assert result.physical_interval_probability == pytest.approx(
        0.6914624612740131, rel=1.0e-12
    )
    assert result.effective_mean_composition == pytest.approx(
        0.01009160433837025, rel=1.0e-11
    )
    assert result.effective_composition_sigma == pytest.approx(
        0.006972628168031896, rel=1.0e-11
    )
    assert result.mean_gap_ev == pytest.approx(result.effective_mean_composition)
    assert result.omitted_tail_probability < 1.0e-12


def test_linear_critical_temperature_distribution_is_exact() -> None:
    def model(x: float, temperature_k: float) -> float:
        return x - 0.2 + 1.0e-3 * (temperature_k - 100.0)

    result = gaussian_critical_temperature_distribution(
        model,
        0.2,
        0.01,
        temperature_bounds_k=(0.0, 200.0),
        quadrature_order=128,
        temperature_grid_size=201,
    )

    assert result.single_crossing_probability == pytest.approx(1.0, abs=1.0e-12)
    assert result.conditional_mean_temperature_k == pytest.approx(100.0, abs=1.0e-10)
    assert result.conditional_sigma_temperature_k == pytest.approx(10.0, rel=1.0e-10)
    assert result.central_composition_critical_temperature_k == pytest.approx(100.0)
    assert result.linearized_sigma_temperature_k == pytest.approx(10.0, rel=1.0e-10)
    assert result.conditional_mean_shift_k == pytest.approx(0.0, abs=1.0e-10)
    assert result.sigma_approximation_error_k == pytest.approx(0.0, abs=1.0e-9)


def test_critical_temperature_classification_retains_no_crossing_probability() -> None:
    def always_normal(x: float, temperature_k: float) -> float:
        return 0.1 + x + 1.0e-4 * temperature_k

    result = gaussian_critical_temperature_distribution(
        always_normal,
        0.2,
        0.01,
        temperature_bounds_k=(0.0, 300.0),
        quadrature_order=64,
    )

    assert result.single_crossing_probability == 0.0
    assert result.always_normal_probability == pytest.approx(1.0)
    assert result.always_inverted_probability == 0.0
    assert result.conditional_mean_temperature_k is None
    assert result.linearized_sigma_temperature_k is None


def test_multiple_temperature_roots_are_not_collapsed() -> None:
    def model(x: float, temperature_k: float) -> float:
        del x
        return 1.0e-6 * (temperature_k - 50.0) * (temperature_k - 150.0)

    result = gaussian_critical_temperature_distribution(
        model,
        0.2,
        0.0,
        temperature_bounds_k=(0.0, 200.0),
        quadrature_order=64,
        temperature_grid_size=201,
    )

    assert result.multiple_crossing_probability == 1.0
    assert result.single_crossing_probability == 0.0
    assert result.conditional_mean_temperature_k is None


def test_teppe_laurenti_exact_distribution_matches_local_limit() -> None:
    moments = gaussian_gap_moments(
        laurenti_gap_ev,
        0.155,
        0.001,
        77.0,
        quadrature_order=256,
    )
    transition = gaussian_critical_temperature_distribution(
        laurenti_gap_ev,
        0.155,
        0.001,
        temperature_bounds_k=(0.0, 300.0),
        quadrature_order=256,
        temperature_grid_size=257,
    )

    assert moments.mean_gap_ev == pytest.approx(-4.75764806e-5, abs=2.0e-13)
    assert moments.gap_sigma_ev == pytest.approx(1.71910833e-3, rel=1.0e-8)
    assert moments.negative_gap_probability == pytest.approx(0.511094, rel=2.0e-5)
    assert abs(moments.mean_approximation_error_ev) < 1.0e-10
    assert abs(moments.sigma_approximation_error_ev) < 1.0e-8

    assert transition.single_crossing_probability == pytest.approx(1.0, abs=1.0e-12)
    assert transition.central_composition_critical_temperature_k == pytest.approx(
        77.124121892, abs=1.0e-8
    )
    assert transition.conditional_mean_temperature_k == pytest.approx(
        77.09719619, abs=2.0e-6
    )
    assert transition.conditional_sigma_temperature_k == pytest.approx(
        4.46435465, rel=2.0e-7
    )
    assert transition.linearized_sigma_temperature_k == pytest.approx(
        4.46214290, rel=2.0e-7
    )


def test_quadrature_input_validation() -> None:
    with pytest.raises(ValueError, match="quadrature_order"):
        gaussian_gap_moments(laurenti_gap_ev, 0.2, 0.001, 77.0, quadrature_order=8)
    with pytest.raises(ValueError, match="mean_composition"):
        gaussian_gap_moments(laurenti_gap_ev, 1.1, 0.001, 77.0)
    with pytest.raises(ValueError, match="composition_sigma"):
        gaussian_gap_moments(laurenti_gap_ev, 0.2, -0.001, 77.0)
    with pytest.raises(ValueError, match="temperature bounds"):
        gaussian_critical_temperature_distribution(
            laurenti_gap_ev,
            0.2,
            0.001,
            temperature_bounds_k=(300.0, 0.0),
        )
