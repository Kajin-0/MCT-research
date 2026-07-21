from __future__ import annotations

import math

import pytest

from mct_research.spatial_disorder import isotropic_gaussian_effective_variance
from mct_research.spatial_disorder_inference import (
    cutoff_standard_deviation_um,
    probe_averaged_gap_moments,
    recover_isotropic_gaussian_two_scales,
    single_scale_point_variance_family,
    top_hat_exponential_effective_variance_1d,
    top_hat_gaussian_effective_variance_1d,
    two_scale_log_parameter_condition_number,
)


def _simpson(function, lower: float, upper: float, intervals: int = 20000) -> float:
    if intervals % 2:
        raise ValueError("intervals must be even")
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(
        function(lower + index * step) for index in range(1, intervals, 2)
    )
    total += 2.0 * sum(
        function(lower + index * step) for index in range(2, intervals, 2)
    )
    return total * step / 3.0


@pytest.mark.parametrize("dimension", [1, 2, 3, 4])
def test_general_dimensional_two_scale_inverse(dimension: int) -> None:
    point_variance = 4.9e-5
    correlation_length = 3.7
    scale_1 = 0.4
    scale_2 = 14.0
    variance_1 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_1,
        dimension=dimension,
    )
    variance_2 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_2,
        dimension=dimension,
    )

    recovered = recover_isotropic_gaussian_two_scales(
        variance_1,
        variance_2,
        scale_1,
        scale_2,
        dimension=dimension,
    )

    assert recovered.point_variance == pytest.approx(point_variance, rel=3.0e-13)
    assert recovered.correlation_length == pytest.approx(
        correlation_length, rel=3.0e-13
    )
    assert recovered.relative_reconstruction_residual < 5.0e-14


def test_one_scale_family_is_exact_and_nonunique() -> None:
    observed_variance = 3.2e-6
    probe_sigma = 10.0
    inferred = []
    for correlation_length in (0.5, 2.0, 10.0, 100.0):
        point_variance = single_scale_point_variance_family(
            observed_variance,
            correlation_length,
            probe_sigma,
            dimension=2,
        )
        inferred.append(point_variance)
        reconstructed = isotropic_gaussian_effective_variance(
            point_variance,
            correlation_length,
            probe_sigma,
            dimension=2,
        )
        assert reconstructed == pytest.approx(observed_variance, rel=3.0e-15)
    assert max(inferred) / min(inferred) > 100.0


def test_conditioning_penalizes_equal_and_same_asymptotic_scales() -> None:
    correlation_length = 5.0
    near_equal = two_scale_log_parameter_condition_number(
        correlation_length, 5.0, 5.05, dimension=2
    )
    straddling = two_scale_log_parameter_condition_number(
        correlation_length, 0.5, 50.0, dimension=2
    )
    both_large = two_scale_log_parameter_condition_number(
        correlation_length, 50.0, 500.0, dimension=2
    )
    both_small = two_scale_log_parameter_condition_number(
        correlation_length, 0.005, 0.05, dimension=2
    )

    assert near_equal == pytest.approx(632.8977824409359, rel=2.0e-12)
    assert straddling == pytest.approx(2.6833803015680533, rel=2.0e-12)
    assert both_large > 1000.0
    assert both_small > 10000.0
    assert math.isinf(
        two_scale_log_parameter_condition_number(
            correlation_length, 5.0, 5.0, dimension=2
        )
    )


@pytest.mark.parametrize("ratio", [1.0e-5, 0.1, 1.0, 10.0, 100.0])
def test_gaussian_top_hat_matches_independent_quadrature(ratio: float) -> None:
    point_variance = 2.0e-5
    correlation_length = 3.0
    length = ratio * correlation_length
    numerical = 2.0 / (length * length) * _simpson(
        lambda separation: (
            (length - separation)
            * point_variance
            * math.exp(-0.5 * (separation / correlation_length) ** 2)
        ),
        0.0,
        length,
    )
    exact = top_hat_gaussian_effective_variance_1d(
        point_variance,
        correlation_length,
        length,
    )
    assert exact == pytest.approx(numerical, rel=3.0e-10, abs=1.0e-16)


@pytest.mark.parametrize("ratio", [1.0e-6, 0.1, 1.0, 10.0, 100.0])
def test_exponential_top_hat_matches_independent_quadrature(ratio: float) -> None:
    point_variance = 2.0e-5
    correlation_length = 3.0
    length = ratio * correlation_length
    numerical = 2.0 / (length * length) * _simpson(
        lambda separation: (
            (length - separation)
            * point_variance
            * math.exp(-separation / correlation_length)
        ),
        0.0,
        length,
    )
    exact = top_hat_exponential_effective_variance_1d(
        point_variance,
        correlation_length,
        length,
    )
    assert exact == pytest.approx(numerical, rel=3.0e-10, abs=1.0e-16)


def test_quadratic_gap_propagation_matches_exact_gaussian_moments() -> None:
    mean_composition = 0.22
    point_variance = 4.0e-5
    correlation_length = 2.0
    probe_sigma = 1.5

    def quadratic_gap(composition: float, temperature_k: float) -> float:
        del temperature_k
        return 0.3 + 1.7 * composition + 0.8 * composition**2

    result = probe_averaged_gap_moments(
        quadratic_gap,
        mean_composition,
        77.0,
        point_variance,
        correlation_length,
        probe_sigma,
        dimension=2,
        derivative_step=1.0e-4,
    )
    effective_variance = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        probe_sigma,
        dimension=2,
    )
    first = 1.7 + 1.6 * mean_composition
    second = 1.6
    exact_mean = quadratic_gap(mean_composition, 77.0) + 0.5 * second * effective_variance
    exact_variance = (
        first * first * effective_variance
        + 0.5 * second * second * effective_variance**2
    )

    assert result.mean_gap_ev == pytest.approx(exact_mean, abs=2.0e-12)
    assert result.gap_variance_ev2 == pytest.approx(exact_variance, rel=3.0e-9)


def test_declared_hgcdte_scale_effect_is_large() -> None:
    point_variance = 0.005**2
    correlation_length_um = 5.0
    gap_slope_ev = 1.7191085
    cutoff_wavelength_um = 10.0
    cutoff_energy_ev = 1.239841984 / cutoff_wavelength_um

    gap_sigmas = []
    cutoff_sigmas = []
    for probe_sigma_um in (1.0, 5.0, 10.0, 100.0):
        effective = isotropic_gaussian_effective_variance(
            point_variance,
            correlation_length_um,
            probe_sigma_um,
            dimension=2,
        )
        gap_sigma = gap_slope_ev * math.sqrt(effective)
        gap_sigmas.append(gap_sigma)
        cutoff_sigmas.append(
            cutoff_standard_deviation_um(
                gap_sigma,
                cutoff_wavelength_um,
                cutoff_energy_ev,
            )
        )

    assert gap_sigmas[0] * 1000.0 == pytest.approx(8.27106462700978)
    assert gap_sigmas[-1] * 1000.0 == pytest.approx(0.3037085609168189)
    assert gap_sigmas[0] / gap_sigmas[-1] == pytest.approx(27.23355773061365)
    assert cutoff_sigmas[0] == pytest.approx(0.6671063517566591)
    assert cutoff_sigmas[-1] == pytest.approx(0.024495747428796455)


@pytest.mark.parametrize(
    "operation",
    [
        lambda: single_scale_point_variance_family(0.0, 1.0, 1.0),
        lambda: single_scale_point_variance_family(1.0, 0.0, 1.0),
        lambda: recover_isotropic_gaussian_two_scales(1.0, 0.5, 1.0, 1.0),
        lambda: recover_isotropic_gaussian_two_scales(1.0, 1.0, 1.0, 2.0),
        lambda: recover_isotropic_gaussian_two_scales(
            0.5, 0.7, 1.0, 2.0, dimension=2
        ),
        lambda: top_hat_gaussian_effective_variance_1d(1.0, 1.0, 0.0),
        lambda: top_hat_exponential_effective_variance_1d(1.0, -1.0, 1.0),
        lambda: cutoff_standard_deviation_um(1.0, 1.0, 0.0),
    ],
)
def test_invalid_inputs_are_rejected(operation) -> None:
    with pytest.raises(ValueError):
        operation()
