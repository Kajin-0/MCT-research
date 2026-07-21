from __future__ import annotations

import math

import pytest

from mct_research.spatial_disorder import (
    gaussian_probe_standard_deviation,
    gaussian_probe_variance,
    probe_averaged_gap_moments,
    recover_gaussian_disorder_two_scales,
    single_scale_microscopic_variance,
    top_hat_variance_exponential_1d,
    top_hat_variance_gaussian_1d,
    two_scale_log_jacobian_condition_number,
)


def _simpson_integral(function, lower: float, upper: float, intervals: int = 20000) -> float:
    if intervals % 2:
        raise ValueError("Simpson intervals must be even")
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


@pytest.mark.parametrize("dimension", [1, 2, 3])
def test_gaussian_probe_exact_limits(dimension: int) -> None:
    microscopic_variance = 2.5e-5
    correlation_length = 7.0
    assert gaussian_probe_variance(
        microscopic_variance, correlation_length, 0.0, dimension
    ) == pytest.approx(microscopic_variance)

    probe_scale = 1.0e4 * correlation_length
    obtained = gaussian_probe_variance(
        microscopic_variance, correlation_length, probe_scale, dimension
    )
    asymptotic = microscopic_variance * (
        correlation_length / (math.sqrt(2.0) * probe_scale)
    ) ** dimension
    assert obtained == pytest.approx(asymptotic, rel=1.0e-8)


def test_single_scale_is_an_exact_nonidentifiability_family() -> None:
    observed = 3.2e-6
    probe_scale = 10.0
    dimension = 2
    microscopic_variances = []
    for correlation_length in (0.5, 2.0, 10.0, 100.0):
        microscopic = single_scale_microscopic_variance(
            observed, correlation_length, probe_scale, dimension
        )
        microscopic_variances.append(microscopic)
        assert gaussian_probe_variance(
            microscopic, correlation_length, probe_scale, dimension
        ) == pytest.approx(observed, rel=2.0e-15)
    assert max(microscopic_variances) / min(microscopic_variances) > 100.0


@pytest.mark.parametrize("dimension", [1, 2, 3])
def test_two_scale_inverse_recovers_exact_parameters(dimension: int) -> None:
    microscopic_variance = 4.9e-5
    correlation_length = 3.7
    first_scale = 0.4
    second_scale = 14.0
    first = gaussian_probe_variance(
        microscopic_variance, correlation_length, first_scale, dimension
    )
    second = gaussian_probe_variance(
        microscopic_variance, correlation_length, second_scale, dimension
    )
    recovered = recover_gaussian_disorder_two_scales(
        first, second, first_scale, second_scale, dimension
    )
    assert recovered.microscopic_variance == pytest.approx(
        microscopic_variance, rel=2.0e-14
    )
    assert recovered.correlation_length == pytest.approx(
        correlation_length, rel=2.0e-14
    )
    assert recovered.relative_reconstruction_residual < 5.0e-15
    assert math.isfinite(recovered.log_parameter_condition_number)


def test_two_scale_conditioning_exposes_bad_scale_choices() -> None:
    correlation_length = 1.0
    near_equal = two_scale_log_jacobian_condition_number(
        correlation_length, 1.0, 1.01, 2
    )
    straddling = two_scale_log_jacobian_condition_number(
        correlation_length, 0.1, 10.0, 2
    )
    both_large = two_scale_log_jacobian_condition_number(
        correlation_length, 10.0, 100.0, 2
    )
    assert near_equal > 500.0
    assert straddling < 3.0
    assert both_large > 100.0
    assert math.isinf(
        two_scale_log_jacobian_condition_number(
            correlation_length, 1.0, 1.0, 2
        )
    )


@pytest.mark.parametrize("ratio", [1.0e-5, 0.1, 1.0, 10.0, 100.0])
def test_gaussian_top_hat_formula_matches_independent_quadrature(ratio: float) -> None:
    microscopic_variance = 2.0e-5
    correlation_length = 3.0
    length = ratio * correlation_length
    covariance = lambda separation: microscopic_variance * math.exp(
        -0.5 * (separation / correlation_length) ** 2
    )
    numerical = 2.0 / (length * length) * _simpson_integral(
        lambda separation: (length - separation) * covariance(separation),
        0.0,
        length,
    )
    exact = top_hat_variance_gaussian_1d(
        microscopic_variance, correlation_length, length
    )
    assert exact == pytest.approx(numerical, rel=2.0e-10, abs=1.0e-16)


@pytest.mark.parametrize("ratio", [1.0e-6, 0.1, 1.0, 10.0, 100.0])
def test_exponential_top_hat_formula_matches_independent_quadrature(ratio: float) -> None:
    microscopic_variance = 2.0e-5
    correlation_length = 3.0
    length = ratio * correlation_length
    covariance = lambda separation: microscopic_variance * math.exp(
        -separation / correlation_length
    )
    numerical = 2.0 / (length * length) * _simpson_integral(
        lambda separation: (length - separation) * covariance(separation),
        0.0,
        length,
    )
    exact = top_hat_variance_exponential_1d(
        microscopic_variance, correlation_length, length
    )
    assert exact == pytest.approx(numerical, rel=2.0e-10, abs=1.0e-16)


def test_quadratic_gap_propagation_is_exact_for_gaussian_composition() -> None:
    mean_composition = 0.22
    microscopic_variance = 4.0e-5
    correlation_length = 2.0
    probe_scale = 1.5
    dimension = 2

    def quadratic_gap(composition: float, temperature_k: float) -> float:
        del temperature_k
        return 0.3 + 1.7 * composition + 0.8 * composition**2

    moments = probe_averaged_gap_moments(
        quadratic_gap,
        mean_composition,
        77.0,
        microscopic_variance,
        correlation_length,
        probe_scale,
        dimension,
        derivative_step=1.0e-4,
    )
    variance = gaussian_probe_variance(
        microscopic_variance, correlation_length, probe_scale, dimension
    )
    first = 1.7 + 1.6 * mean_composition
    second = 1.6
    exact_mean = quadratic_gap(mean_composition, 77.0) + 0.5 * second * variance
    exact_variance = first**2 * variance + 0.5 * second**2 * variance**2
    assert moments.mean_gap_ev == pytest.approx(exact_mean, abs=2.0e-12)
    assert moments.gap_variance_ev2 == pytest.approx(exact_variance, rel=2.0e-9)


def test_standard_deviation_wrapper() -> None:
    obtained = gaussian_probe_standard_deviation(0.005, 5.0, 10.0, 2)
    assert obtained == pytest.approx(0.005 / 3.0)


@pytest.mark.parametrize(
    "call",
    [
        lambda: gaussian_probe_variance(-1.0, 1.0, 1.0, 2),
        lambda: gaussian_probe_variance(1.0, 0.0, 1.0, 2),
        lambda: gaussian_probe_variance(1.0, 1.0, -1.0, 2),
        lambda: gaussian_probe_variance(1.0, 1.0, 1.0, 0),
        lambda: recover_gaussian_disorder_two_scales(1.0, 0.5, 1.0, 1.0, 2),
        lambda: recover_gaussian_disorder_two_scales(1.0, 1.0, 1.0, 2.0, 2),
        lambda: top_hat_variance_gaussian_1d(1.0, 1.0, 0.0),
        lambda: top_hat_variance_exponential_1d(1.0, -1.0, 1.0),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
