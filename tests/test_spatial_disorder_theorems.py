from __future__ import annotations

import math

import pytest

from mct_research.spatial_disorder import isotropic_gaussian_effective_variance
from mct_research.spatial_disorder_theorems import (
    cutoff_standard_deviation_um,
    probe_averaged_gap_moments,
    recover_isotropic_gaussian_two_scales,
    single_scale_point_variance_family,
    top_hat_exponential_effective_variance_1d,
    top_hat_gaussian_effective_variance_1d,
    two_scale_log_parameter_condition_number,
)


def _simpson(function, lower: float, upper: float, intervals: int = 20000) -> float:
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + index * step) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + index * step) for index in range(2, intervals, 2))
    return total * step / 3.0


@pytest.mark.parametrize("dimension", [1, 2, 3, 4])
def test_arbitrary_dimensional_inverse(dimension: int) -> None:
    point_variance = 4.9e-5
    correlation_length = 3.7
    scale_1, scale_2 = 0.4, 14.0
    variance_1 = isotropic_gaussian_effective_variance(
        point_variance, correlation_length, scale_1, dimension=dimension
    )
    variance_2 = isotropic_gaussian_effective_variance(
        point_variance, correlation_length, scale_2, dimension=dimension
    )
    recovered = recover_isotropic_gaussian_two_scales(
        variance_1, variance_2, scale_1, scale_2, dimension=dimension
    )
    assert recovered.point_variance == pytest.approx(point_variance, rel=3.0e-13)
    assert recovered.correlation_length == pytest.approx(correlation_length, rel=3.0e-13)
    assert recovered.relative_reconstruction_residual < 5.0e-14


def test_one_scale_family_is_exact_and_nonunique() -> None:
    observed = 3.2e-6
    inferred = []
    for correlation_length in (0.5, 2.0, 10.0, 100.0):
        point_variance = single_scale_point_variance_family(
            observed, correlation_length, 10.0, dimension=2
        )
        inferred.append(point_variance)
        assert isotropic_gaussian_effective_variance(
            point_variance, correlation_length, 10.0, dimension=2
        ) == pytest.approx(observed, rel=3.0e-15)
    assert max(inferred) / min(inferred) > 100.0


def test_two_scale_conditioning_regimes() -> None:
    near_equal = two_scale_log_parameter_condition_number(5.0, 5.0, 5.05)
    straddling = two_scale_log_parameter_condition_number(5.0, 0.5, 50.0)
    both_large = two_scale_log_parameter_condition_number(5.0, 50.0, 500.0)
    both_small = two_scale_log_parameter_condition_number(5.0, 0.005, 0.05)
    assert near_equal == pytest.approx(632.8977824409359, rel=2.0e-12)
    assert straddling == pytest.approx(2.6833803015680533, rel=2.0e-12)
    assert both_large > 1000.0
    assert both_small > 5000.0
    assert math.isinf(two_scale_log_parameter_condition_number(5.0, 5.0, 5.0))


@pytest.mark.parametrize("ratio", [1.0e-5, 0.1, 1.0, 10.0, 100.0])
def test_gaussian_top_hat_matches_quadrature(ratio: float) -> None:
    point_variance, correlation_length = 2.0e-5, 3.0
    length = ratio * correlation_length
    numerical = 2.0 / length**2 * _simpson(
        lambda h: (length - h)
        * point_variance
        * math.exp(-0.5 * (h / correlation_length) ** 2),
        0.0,
        length,
    )
    exact = top_hat_gaussian_effective_variance_1d(
        point_variance, correlation_length, length
    )
    assert exact == pytest.approx(numerical, rel=3.0e-10, abs=1.0e-16)


@pytest.mark.parametrize("ratio", [1.0e-6, 0.1, 1.0, 10.0, 100.0])
def test_exponential_top_hat_matches_quadrature(ratio: float) -> None:
    point_variance, correlation_length = 2.0e-5, 3.0
    length = ratio * correlation_length
    numerical = 2.0 / length**2 * _simpson(
        lambda h: (length - h)
        * point_variance
        * math.exp(-h / correlation_length),
        0.0,
        length,
    )
    exact = top_hat_exponential_effective_variance_1d(
        point_variance, correlation_length, length
    )
    assert exact == pytest.approx(numerical, rel=3.0e-10, abs=1.0e-16)


def test_quadratic_gap_moments_are_exact() -> None:
    def gap(composition: float, temperature_k: float) -> float:
        del temperature_k
        return 0.3 + 1.7 * composition + 0.8 * composition**2

    mean_composition = 0.22
    point_variance = 4.0e-5
    result = probe_averaged_gap_moments(
        gap,
        mean_composition,
        77.0,
        point_variance,
        2.0,
        1.5,
        dimension=2,
        derivative_step=1.0e-4,
    )
    effective = isotropic_gaussian_effective_variance(
        point_variance, 2.0, 1.5, dimension=2
    )
    first, second = 1.7 + 1.6 * mean_composition, 1.6
    assert result.mean_gap_ev == pytest.approx(
        gap(mean_composition, 77.0) + 0.5 * second * effective,
        abs=2.0e-12,
    )
    assert result.gap_variance_ev2 == pytest.approx(
        first**2 * effective + 0.5 * second**2 * effective**2,
        rel=3.0e-9,
    )


def test_declared_hgcdte_scale_effect() -> None:
    point_variance = 0.005**2
    slope = 1.7191085
    gap_sigmas = [
        slope
        * math.sqrt(
            isotropic_gaussian_effective_variance(
                point_variance, 5.0, scale, dimension=2
            )
        )
        for scale in (1.0, 100.0)
    ]
    cutoff_energy = 1.239841984 / 10.0
    assert gap_sigmas[0] * 1000.0 == pytest.approx(8.27106462700978)
    assert gap_sigmas[1] * 1000.0 == pytest.approx(0.3037085609168189)
    assert gap_sigmas[0] / gap_sigmas[1] == pytest.approx(27.23355773061365)
    assert cutoff_standard_deviation_um(gap_sigmas[0], 10.0, cutoff_energy) == pytest.approx(
        0.6671063517566591
    )
    assert cutoff_standard_deviation_um(gap_sigmas[1], 10.0, cutoff_energy) == pytest.approx(
        0.024495747428796455
    )


@pytest.mark.parametrize(
    "operation",
    [
        lambda: single_scale_point_variance_family(0.0, 1.0, 1.0),
        lambda: recover_isotropic_gaussian_two_scales(1.0, 0.5, 1.0, 1.0),
        lambda: recover_isotropic_gaussian_two_scales(1.0, 1.0, 1.0, 2.0),
        lambda: top_hat_gaussian_effective_variance_1d(1.0, 1.0, 0.0),
        lambda: top_hat_exponential_effective_variance_1d(1.0, -1.0, 1.0),
        lambda: cutoff_standard_deviation_um(1.0, 1.0, 0.0),
    ],
)
def test_invalid_inputs(operation) -> None:
    with pytest.raises(ValueError):
        operation()
