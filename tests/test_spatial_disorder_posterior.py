from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_inference import (
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_variance,
)
from mct_research.spatial_disorder_posterior import (
    combine_common_scale_calibration,
    direct_bounded_common_scale_posterior,
    discrete_distribution,
    gaussian_grid_distribution,
    relative_scale_posterior_grid,
)


def _synthetic_case() -> tuple[float, float, np.ndarray, np.ndarray]:
    point_variance = 0.03
    correlation_length = 1.4
    scales = np.array([0.2, 0.7, 2.0, 6.0])
    observed = gaussian_multiscale_variance(
        point_variance,
        correlation_length,
        scales,
    )
    return point_variance, correlation_length, scales, observed


def _relative_posterior(
    relative_uncertainty: float,
    *,
    half_width_u: float = 0.8,
    half_width_lambda: float = 1.2,
    points_u: int = 121,
    points_lambda: int = 145,
):
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_lambda = math.log(correlation_length)
    u_grid = np.linspace(true_u - half_width_u, true_u + half_width_u, points_u)
    lambda_grid = np.linspace(
        true_lambda - half_width_lambda,
        true_lambda + half_width_lambda,
        points_lambda,
    )
    return relative_scale_posterior_grid(
        observed,
        scales,
        u_grid,
        lambda_grid,
        relative_standard_deviation=relative_uncertainty,
        likelihood="log_gaussian",
    )


def test_relative_posterior_normalization_and_immutability() -> None:
    posterior = _relative_posterior(0.05)
    assert np.sum(posterior.probability_mass) == pytest.approx(1.0, abs=3.0e-15)
    assert posterior.boundary_mass < 1.0e-8
    assert posterior.mean.shape == (2,)
    assert posterior.covariance.shape == (2, 2)
    assert np.all(np.linalg.eigvalsh(posterior.covariance) > 0.0)
    arrays = (
        posterior.log_point_variance_grid,
        posterior.log_relative_correlation_grid,
        posterior.probability_mass,
        posterior.mean,
        posterior.covariance,
        posterior.relative_correlation_distribution.grid,
        posterior.relative_correlation_distribution.probability_mass,
    )
    assert all(not array.flags.writeable for array in arrays)


def test_exact_common_scale_convolution_adds_all_four_cumulants() -> None:
    posterior = _relative_posterior(0.08)
    spacing = posterior.relative_correlation_distribution.spacing
    calibration_grid = spacing * np.arange(-20, 21)
    # Deliberately asymmetric and non-Gaussian.
    mass = np.exp(-0.5 * ((calibration_grid + 0.04) / 0.09) ** 2)
    mass *= 1.0 + 0.8 * (calibration_grid > 0.0)
    calibration = discrete_distribution(calibration_grid, mass)
    combined = combine_common_scale_calibration(posterior, calibration)

    relative = posterior.relative_correlation_distribution
    expected = np.array(
        [
            relative.mean + calibration.mean,
            relative.variance + calibration.variance,
            relative.third_cumulant + calibration.third_cumulant,
            relative.fourth_cumulant + calibration.fourth_cumulant,
        ]
    )
    assert combined.log_correlation_cumulants == pytest.approx(
        expected,
        rel=3.0e-12,
        abs=3.0e-15,
    )
    assert combined.covariance_increment == pytest.approx(
        np.array([[0.0, 0.0], [0.0, calibration.variance]]),
        rel=3.0e-13,
        abs=3.0e-15,
    )
    assert combined.variance_addition_residual == pytest.approx(0.0, abs=3.0e-15)
    assert combined.cross_covariance_residual == pytest.approx(0.0, abs=3.0e-15)


def test_zero_width_calibration_recovers_relative_posterior() -> None:
    posterior = _relative_posterior(0.05)
    spacing = posterior.relative_correlation_distribution.spacing
    calibration = discrete_distribution(
        [-spacing, 0.0, spacing],
        [0.0, 1.0, 0.0],
    )
    combined = combine_common_scale_calibration(posterior, calibration)

    assert combined.calibration_prior.variance == pytest.approx(0.0)
    assert combined.absolute_log_correlation_distribution.mean == pytest.approx(
        posterior.relative_correlation_distribution.mean,
        abs=6.0e-15,
    )
    assert combined.covariance == pytest.approx(posterior.covariance, abs=3.0e-15)


def test_direct_three_dimensional_posterior_verifies_broad_prior_factorization() -> None:
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_v = math.log(correlation_length)
    step = 0.025
    u_grid = true_u + step * np.arange(-32, 33)
    lambda_grid = true_v + step * np.arange(-48, 49)
    delta_grid = step * np.arange(-16, 17)
    calibration = gaussian_grid_distribution(delta_grid, 0.0, 0.10)

    relative = relative_scale_posterior_grid(
        observed,
        scales,
        u_grid,
        lambda_grid,
        relative_standard_deviation=0.08,
    )
    combined = combine_common_scale_calibration(relative, calibration)
    v_grid = true_v + step * np.arange(-72, 73)
    direct = direct_bounded_common_scale_posterior(
        observed,
        scales,
        u_grid,
        v_grid,
        calibration,
        relative_standard_deviation=0.08,
    )

    assert direct.log_absolute_correlation_boundary_mass < 1.0e-9
    assert direct.posterior_calibration_total_variation < 2.0e-9
    assert direct.posterior_calibration_mean_shift == pytest.approx(0.0, abs=2.0e-10)
    assert direct.posterior_calibration_variance_shift == pytest.approx(0.0, abs=2.0e-10)
    assert direct.relative_calibration_covariance == pytest.approx(0.0, abs=2.0e-10)
    assert direct.variance_addition_residual == pytest.approx(0.0, abs=3.0e-10)
    assert direct.cross_covariance_residual == pytest.approx(0.0, abs=3.0e-10)
    assert direct.mean[:2] == pytest.approx(combined.mean, abs=3.0e-8)
    assert direct.covariance[:2, :2] == pytest.approx(
        combined.covariance,
        rel=3.0e-6,
        abs=3.0e-9,
    )


def test_bounded_absolute_length_prior_breaks_factorization_near_boundary() -> None:
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_v = math.log(correlation_length)
    step = 0.025
    u_grid = true_u + step * np.arange(-32, 33)
    delta_grid = step * np.arange(-16, 17)
    calibration = gaussian_grid_distribution(delta_grid, 0.0, 0.10)

    broad = direct_bounded_common_scale_posterior(
        observed,
        scales,
        u_grid,
        true_v + step * np.arange(-72, 73),
        calibration,
        relative_standard_deviation=0.08,
    )
    narrow = direct_bounded_common_scale_posterior(
        observed,
        scales,
        u_grid,
        true_v + step * np.arange(-7, 8),
        calibration,
        relative_standard_deviation=0.08,
        boundary_cells=2,
    )

    assert narrow.log_absolute_correlation_boundary_mass > 0.02
    assert narrow.posterior_calibration_total_variation > broad.posterior_calibration_total_variation + 1.0e-3
    assert abs(narrow.relative_calibration_covariance) > 1.0e-4
    assert abs(narrow.variance_addition_residual) > 1.0e-4


def test_fisher_covariance_is_recovered_in_small_noise_limit() -> None:
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_lambda = math.log(correlation_length)
    relative_uncertainty = 0.01
    posterior = relative_scale_posterior_grid(
        observed,
        scales,
        np.linspace(true_u - 0.12, true_u + 0.12, 241),
        np.linspace(true_lambda - 0.12, true_lambda + 0.12, 241),
        relative_standard_deviation=relative_uncertainty,
    )
    fisher = gaussian_multiscale_fisher_information(
        point_variance,
        correlation_length,
        scales,
        relative_standard_deviation=relative_uncertainty,
    )

    assert fisher.parameter_covariance is not None
    assert posterior.covariance == pytest.approx(
        fisher.parameter_covariance,
        rel=0.025,
        abs=2.0e-7,
    )


def test_fisher_error_grows_but_remains_small_for_broad_log_gaussian_posterior() -> None:
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_lambda = math.log(correlation_length)

    errors = []
    for uncertainty, half_width, points in (
        (0.05, 0.7, 181),
        (0.30, 2.0, 241),
    ):
        posterior = relative_scale_posterior_grid(
            observed,
            scales,
            np.linspace(true_u - half_width, true_u + half_width, points),
            np.linspace(true_lambda - half_width, true_lambda + half_width, points),
            relative_standard_deviation=uncertainty,
        )
        fisher = gaussian_multiscale_fisher_information(
            point_variance,
            correlation_length,
            scales,
            relative_standard_deviation=uncertainty,
        )
        relative_error = np.linalg.norm(
            posterior.covariance - np.asarray(fisher.parameter_covariance)
        ) / np.linalg.norm(np.asarray(fisher.parameter_covariance))
        errors.append(relative_error)

    assert errors[0] < 0.001
    assert errors[1] > 10.0 * errors[0]
    assert errors[1] < 0.03


def test_length_unit_invariance_of_relative_and_absolute_posteriors() -> None:
    point_variance, correlation_length, scales, observed = _synthetic_case()
    true_u = math.log(point_variance)
    true_lambda = math.log(correlation_length)
    step = 0.02
    u_grid = true_u + step * np.arange(-40, 41)
    lambda_grid = true_lambda + step * np.arange(-60, 61)
    calibration = gaussian_grid_distribution(step * np.arange(-20, 21), 0.0, 0.08)

    reference = relative_scale_posterior_grid(
        observed,
        scales,
        u_grid,
        lambda_grid,
        relative_standard_deviation=0.06,
    )
    unit_shift = math.log(1.0e-6)
    rescaled = relative_scale_posterior_grid(
        observed,
        scales * 1.0e-6,
        u_grid,
        lambda_grid + unit_shift,
        relative_standard_deviation=0.06,
    )

    assert rescaled.mean[0] == pytest.approx(reference.mean[0], abs=3.0e-13)
    assert rescaled.mean[1] - unit_shift == pytest.approx(reference.mean[1], abs=3.0e-13)
    assert rescaled.covariance == pytest.approx(reference.covariance, rel=3.0e-12)

    combined_reference = combine_common_scale_calibration(reference, calibration)
    combined_rescaled = combine_common_scale_calibration(rescaled, calibration)
    assert combined_rescaled.mean[1] - unit_shift == pytest.approx(
        combined_reference.mean[1],
        abs=3.0e-13,
    )
    assert combined_rescaled.covariance == pytest.approx(
        combined_reference.covariance,
        rel=3.0e-12,
    )


@pytest.mark.parametrize(
    "operation, message",
    [
        (
            lambda: discrete_distribution([0.0], [1.0]),
            "at least 2",
        ),
        (
            lambda: discrete_distribution([0.0, 1.0, 2.1], [1.0, 1.0, 1.0]),
            "uniformly spaced",
        ),
        (
            lambda: relative_scale_posterior_grid(
                [1.0, 0.5],
                [0.2, 1.0],
                [-1.0, 0.0],
                [-1.0, 0.0],
            ),
            "exactly one",
        ),
        (
            lambda: relative_scale_posterior_grid(
                [1.0, 0.5],
                [0.2, 1.0],
                [-1.0, 0.0],
                [-1.0, 0.0],
                likelihood="gaussian",
                relative_standard_deviation=0.1,
            ),
            "supported only",
        ),
        (
            lambda: combine_common_scale_calibration(
                _relative_posterior(0.05),
                discrete_distribution([-0.1, 0.0, 0.1], [0.2, 0.6, 0.2]),
            ),
            "same grid spacing",
        ),
    ],
)
def test_invalid_inputs(operation, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        operation()
