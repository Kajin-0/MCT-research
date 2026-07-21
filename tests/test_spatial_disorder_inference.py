from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_inference import (
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_log_jacobian,
    gaussian_multiscale_variance,
)


def test_variance_and_log_jacobian_reference() -> None:
    point_variance = 0.017
    correlation_length = 1.8
    scales = np.array([0.0, 0.2, 0.9, 2.7, 8.0])
    predicted = gaussian_multiscale_variance(
        point_variance, correlation_length, scales
    )
    jacobian = gaussian_multiscale_log_jacobian(
        point_variance, correlation_length, scales
    )

    q = 2.0 * scales**2 / correlation_length**2
    assert predicted == pytest.approx(point_variance / (1.0 + q), rel=1.0e-14)
    assert jacobian[:, 0] == pytest.approx(predicted, rel=1.0e-14)
    assert jacobian[:, 1] == pytest.approx(
        predicted * 2.0 * q / (1.0 + q), rel=1.0e-14
    )


def test_log_jacobian_matches_stable_central_differences() -> None:
    point_variance = 0.017
    correlation_length = 1.8
    scales = np.array([0.0, 0.2, 0.9, 2.7, 8.0])
    analytical = gaussian_multiscale_log_jacobian(
        point_variance, correlation_length, scales
    )

    # Near eps**(1/3), central differences balance truncation and subtraction
    # error in binary64. Smaller steps test cancellation, not the derivative.
    step = 1.0e-5
    d_log_variance = (
        gaussian_multiscale_variance(
            point_variance * math.exp(step), correlation_length, scales
        )
        - gaussian_multiscale_variance(
            point_variance * math.exp(-step), correlation_length, scales
        )
    ) / (2.0 * step)
    d_log_correlation = (
        gaussian_multiscale_variance(
            point_variance, correlation_length * math.exp(step), scales
        )
        - gaussian_multiscale_variance(
            point_variance, correlation_length * math.exp(-step), scales
        )
    ) / (2.0 * step)

    assert analytical[:, 0] == pytest.approx(d_log_variance, rel=5.0e-10)
    assert analytical[:, 1] == pytest.approx(
        d_log_correlation, rel=1.0e-9, abs=1.0e-14
    )


def test_one_or_repeated_scale_is_rank_one() -> None:
    one = gaussian_multiscale_fisher_information(
        0.01, 1.0, [0.7], relative_standard_deviation=0.05
    )
    repeated = gaussian_multiscale_fisher_information(
        1.0, 1.0, [0.5] * 4, relative_standard_deviation=0.1
    )

    assert one.rank == repeated.rank == 1
    assert math.isinf(one.condition_number)
    assert one.parameter_covariance is None
    assert one.null_direction is not None
    assert np.asarray(one.jacobian) @ np.asarray(one.null_direction) == pytest.approx(
        [0.0], abs=2.0e-17
    )


def test_small_and_large_probe_null_regimes() -> None:
    small = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [1.0e-10, 2.0e-10, 5.0e-10],
        relative_standard_deviation=0.05,
    )
    large = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [1.0e8, 2.0e8, 5.0e8],
        relative_standard_deviation=0.05,
    )

    assert small.regime == "small_probe"
    assert small.rank == 1
    assert np.max(np.abs(small.jacobian[:, 1])) < 1.0e-18

    assert large.regime == "large_probe"
    assert large.rank == 1
    assert large.jacobian[:, 1] / large.jacobian[:, 0] == pytest.approx(
        [2.0, 2.0, 2.0], rel=1.0e-15
    )


def test_transition_spanning_design_is_well_conditioned() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        0.01,
        2.0,
        [0.0, 0.4, 2.0, 10.0],
        relative_standard_deviation=0.05,
    )
    assert diagnostics.regime == "spanning_transition"
    assert diagnostics.rank == 2
    assert diagnostics.condition_number < 3.0
    assert diagnostics.parameter_covariance is not None
    assert diagnostics.parameter_correlation is not None
    assert -1.0 < diagnostics.parameter_correlation < 0.0
    assert diagnostics.null_direction is None


def test_intermediate_one_sided_design_is_classified() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0, 1.0, [0.2, 0.5, 0.9], relative_standard_deviation=0.1
    )
    assert diagnostics.regime == "intermediate_one_sided"
    assert diagnostics.rank == 2


def test_uncertainty_interfaces_agree_and_correlations_are_supported() -> None:
    scales = np.array([0.0, 0.5, 1.5, 4.0])
    standard_deviations = np.array([0.01, 0.02, 0.03, 0.04])
    diagonal = gaussian_multiscale_fisher_information(
        0.2,
        1.3,
        scales,
        observation_standard_deviations=standard_deviations,
    )
    full = gaussian_multiscale_fisher_information(
        0.2,
        1.3,
        scales,
        observation_covariance=np.diag(standard_deviations**2),
    )
    assert diagonal.fisher_matrix == pytest.approx(full.fisher_matrix, rel=1.0e-14)

    correlation = np.full((4, 4), 0.2)
    np.fill_diagonal(correlation, 1.0)
    correlated_covariance = correlation * np.outer(
        standard_deviations, standard_deviations
    )
    correlated = gaussian_multiscale_fisher_information(
        0.2,
        1.3,
        scales,
        observation_covariance=correlated_covariance,
    )
    assert correlated.rank == 2
    assert correlated.fisher_matrix == pytest.approx(
        correlated.fisher_matrix.T, rel=1.0e-15
    )


def test_relative_noise_amplitude_and_length_unit_invariance() -> None:
    scales = np.array([0.0, 0.2, 1.0, 4.0])
    low = gaussian_multiscale_fisher_information(
        1.0e-8, 1.0, scales, relative_standard_deviation=0.03
    )
    high = gaussian_multiscale_fisher_information(
        1.0e4, 1.0, scales, relative_standard_deviation=0.03
    )
    assert low.fisher_matrix == pytest.approx(high.fisher_matrix, rel=2.0e-14)

    length_scale = 1.0e-6
    rescaled = gaussian_multiscale_fisher_information(
        1.0e-8,
        length_scale,
        scales * length_scale,
        relative_standard_deviation=0.03,
    )
    assert rescaled.probe_scale_ratios == pytest.approx(low.probe_scale_ratios)
    assert rescaled.fisher_matrix == pytest.approx(low.fisher_matrix, rel=2.0e-14)


def test_custom_rank_tolerance_and_immutable_outputs() -> None:
    practical = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [0.01, 0.02, 0.03],
        relative_standard_deviation=0.05,
        rank_relative_tolerance=0.02,
    )
    assert practical.rank == 1
    assert practical.null_direction is not None

    full = gaussian_multiscale_fisher_information(
        1.0, 1.0, [0.0, 1.0, 3.0], relative_standard_deviation=0.05
    )
    arrays = (
        full.predicted_variance,
        full.probe_scale_ratios,
        full.jacobian,
        full.observation_covariance,
        full.fisher_matrix,
        full.singular_values,
        full.parameter_covariance,
    )
    assert all(array is not None and not array.flags.writeable for array in arrays)


def test_invalid_model_and_scale_inputs() -> None:
    with pytest.raises(ValueError, match="point_variance"):
        gaussian_multiscale_variance(0.0, 1.0, [1.0])
    with pytest.raises(ValueError, match="correlation_length"):
        gaussian_multiscale_variance(1.0, math.inf, [1.0])
    with pytest.raises(ValueError, match="non-empty"):
        gaussian_multiscale_variance(1.0, 1.0, [])
    with pytest.raises(ValueError, match="one-dimensional"):
        gaussian_multiscale_variance(1.0, 1.0, [[1.0, 2.0]])
    with pytest.raises(ValueError, match="non-negative"):
        gaussian_multiscale_variance(1.0, 1.0, [-1.0])


def test_invalid_uncertainty_inputs() -> None:
    scales = [0.0, 1.0]
    with pytest.raises(ValueError, match="exactly one"):
        gaussian_multiscale_fisher_information(1.0, 1.0, scales)
    with pytest.raises(ValueError, match="exactly one"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            relative_standard_deviation=0.1,
            observation_standard_deviations=[0.1, 0.1],
        )
    with pytest.raises(ValueError, match="shape"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            observation_standard_deviations=[0.1],
        )
    with pytest.raises(ValueError, match="positive"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            observation_standard_deviations=[0.1, 0.0],
        )
    with pytest.raises(ValueError, match="symmetric"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            observation_covariance=[[1.0, 0.2], [0.1, 1.0]],
        )
    with pytest.raises(ValueError, match="positive definite"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            observation_covariance=[[1.0, 1.0], [1.0, 1.0]],
        )


def test_invalid_rank_tolerance() -> None:
    kwargs = dict(
        point_variance=1.0,
        correlation_length=1.0,
        probe_sigmas=[0.0, 1.0],
        relative_standard_deviation=0.1,
    )
    with pytest.raises(ValueError, match="rank_relative_tolerance"):
        gaussian_multiscale_fisher_information(
            **kwargs, rank_relative_tolerance=0.0
        )
    with pytest.raises(ValueError, match="less than one"):
        gaussian_multiscale_fisher_information(
            **kwargs, rank_relative_tolerance=1.0
        )
