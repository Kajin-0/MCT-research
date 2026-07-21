from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_inference import (
    GaussianRecoverabilityDiagnostics,
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_log_jacobian,
    gaussian_multiscale_variance,
)


def test_multiscale_variance_reference_values() -> None:
    result = gaussian_multiscale_variance(
        point_variance=0.02,
        correlation_length=2.0,
        probe_sigmas=[0.0, 1.0, 2.0, 4.0],
    )
    assert result == pytest.approx(
        [0.02, 0.02 / 1.5, 0.02 / 3.0, 0.02 / 9.0],
        rel=1.0e-14,
    )


def test_log_jacobian_matches_central_finite_differences() -> None:
    point_variance = 0.017
    correlation_length = 1.8
    scales = np.array([0.0, 0.2, 0.9, 2.7, 8.0])
    analytical = gaussian_multiscale_log_jacobian(
        point_variance,
        correlation_length,
        scales,
    )
    step = 1.0e-6
    derivative_log_variance = (
        gaussian_multiscale_variance(
            point_variance * math.exp(step),
            correlation_length,
            scales,
        )
        - gaussian_multiscale_variance(
            point_variance * math.exp(-step),
            correlation_length,
            scales,
        )
    ) / (2.0 * step)
    derivative_log_correlation = (
        gaussian_multiscale_variance(
            point_variance,
            correlation_length * math.exp(step),
            scales,
        )
        - gaussian_multiscale_variance(
            point_variance,
            correlation_length * math.exp(-step),
            scales,
        )
    ) / (2.0 * step)

    assert analytical[:, 0] == pytest.approx(
        derivative_log_variance,
        rel=2.0e-10,
    )
    assert analytical[:, 1] == pytest.approx(
        derivative_log_correlation,
        rel=3.0e-10,
        abs=1.0e-14,
    )


def test_one_scale_has_rank_one_and_null_direction() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        0.01,
        1.0,
        [0.7],
        relative_standard_deviation=0.05,
    )
    assert isinstance(diagnostics, GaussianRecoverabilityDiagnostics)
    assert diagnostics.rank == 1
    assert math.isinf(diagnostics.condition_number)
    assert diagnostics.parameter_covariance is None
    assert diagnostics.parameter_correlation is None
    assert diagnostics.null_direction is not None
    assert np.asarray(diagnostics.jacobian) @ np.asarray(
        diagnostics.null_direction
    ) == pytest.approx([0.0], abs=2.0e-17)


def test_repeated_probe_scales_remain_rank_one() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [0.5, 0.5, 0.5, 0.5],
        relative_standard_deviation=0.1,
    )
    assert diagnostics.rank == 1
    assert diagnostics.singular_values[1] <= diagnostics.rank_tolerance


def test_small_probe_regime_loses_correlation_information() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [1.0e-10, 2.0e-10, 5.0e-10],
        relative_standard_deviation=0.05,
    )
    assert diagnostics.regime == "small_probe"
    assert diagnostics.rank == 1
    assert np.max(np.abs(diagnostics.jacobian[:, 1])) < 1.0e-18


def test_large_probe_regime_loses_separate_amplitude_and_length() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [1.0e8, 2.0e8, 5.0e8],
        relative_standard_deviation=0.05,
    )
    assert diagnostics.regime == "large_probe"
    assert diagnostics.rank == 1
    normalized = diagnostics.jacobian[:, 1] / diagnostics.jacobian[:, 0]
    assert normalized == pytest.approx([2.0, 2.0, 2.0], rel=1.0e-15)


def test_balanced_multiscale_design_is_full_rank_and_well_conditioned() -> None:
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


def test_intermediate_one_sided_regime_classification() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [0.2, 0.5, 0.9],
        relative_standard_deviation=0.1,
    )
    assert diagnostics.regime == "intermediate_one_sided"
    assert diagnostics.rank == 2


def test_standard_deviations_and_diagonal_covariance_agree() -> None:
    scales = np.array([0.0, 0.5, 1.5, 4.0])
    standard_deviations = np.array([0.01, 0.02, 0.03, 0.04])
    direct = gaussian_multiscale_fisher_information(
        0.2,
        1.3,
        scales,
        observation_standard_deviations=standard_deviations,
    )
    covariance = gaussian_multiscale_fisher_information(
        0.2,
        1.3,
        scales,
        observation_covariance=np.diag(standard_deviations**2),
    )
    assert direct.fisher_matrix == pytest.approx(covariance.fisher_matrix, rel=1.0e-14)
    assert direct.singular_values == pytest.approx(
        covariance.singular_values,
        rel=1.0e-14,
    )
    assert direct.condition_number == pytest.approx(covariance.condition_number)


def test_correlated_observation_covariance_is_supported() -> None:
    scales = np.array([0.1, 0.7, 2.0, 6.0])
    standard_deviations = np.array([0.02, 0.03, 0.025, 0.04])
    correlation = np.full((4, 4), 0.2)
    np.fill_diagonal(correlation, 1.0)
    covariance = correlation * np.outer(standard_deviations, standard_deviations)
    diagnostics = gaussian_multiscale_fisher_information(
        0.1,
        1.0,
        scales,
        observation_covariance=covariance,
    )
    assert diagnostics.rank == 2
    assert np.asarray(diagnostics.fisher_matrix) == pytest.approx(
        np.asarray(diagnostics.fisher_matrix).T,
        rel=1.0e-15,
    )
    assert np.all(np.linalg.eigvalsh(diagnostics.fisher_matrix) > 0.0)


def test_relative_noise_conditioning_is_amplitude_invariant() -> None:
    scales = [0.0, 0.2, 1.0, 4.0]
    low = gaussian_multiscale_fisher_information(
        1.0e-8,
        1.0,
        scales,
        relative_standard_deviation=0.03,
    )
    high = gaussian_multiscale_fisher_information(
        1.0e4,
        1.0,
        scales,
        relative_standard_deviation=0.03,
    )
    assert low.fisher_matrix == pytest.approx(high.fisher_matrix, rel=2.0e-14)
    assert low.condition_number == pytest.approx(high.condition_number, rel=2.0e-14)


def test_consistent_length_rescaling_leaves_diagnostics_invariant() -> None:
    scales = np.array([0.0, 0.3, 1.0, 3.0])
    reference = gaussian_multiscale_fisher_information(
        0.01,
        1.0,
        scales,
        relative_standard_deviation=0.04,
    )
    length_scale = 1.0e-6
    scaled = gaussian_multiscale_fisher_information(
        0.01,
        1.0 * length_scale,
        scales * length_scale,
        relative_standard_deviation=0.04,
    )
    assert scaled.probe_scale_ratios == pytest.approx(reference.probe_scale_ratios)
    assert scaled.fisher_matrix == pytest.approx(reference.fisher_matrix, rel=2.0e-14)
    assert scaled.condition_number == pytest.approx(
        reference.condition_number,
        rel=2.0e-14,
    )


def test_custom_rank_tolerance_can_declare_practical_rank_loss() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [0.01, 0.02, 0.03],
        relative_standard_deviation=0.05,
        rank_relative_tolerance=0.02,
    )
    assert diagnostics.rank == 1
    assert diagnostics.null_direction is not None


def test_returned_arrays_are_read_only() -> None:
    diagnostics = gaussian_multiscale_fisher_information(
        1.0,
        1.0,
        [0.0, 1.0, 3.0],
        relative_standard_deviation=0.05,
    )
    for array in (
        diagnostics.predicted_variance,
        diagnostics.probe_scale_ratios,
        diagnostics.jacobian,
        diagnostics.observation_covariance,
        diagnostics.fisher_matrix,
        diagnostics.singular_values,
        diagnostics.parameter_covariance,
    ):
        assert array is not None
        assert array.flags.writeable is False


def test_invalid_model_and_scale_inputs_are_rejected() -> None:
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
    with pytest.raises(ValueError, match="finite"):
        gaussian_multiscale_variance(1.0, 1.0, [math.nan])


def test_exactly_one_uncertainty_specification_is_required() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        gaussian_multiscale_fisher_information(1.0, 1.0, [0.0, 1.0])
    with pytest.raises(ValueError, match="exactly one"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            relative_standard_deviation=0.1,
            observation_standard_deviations=[0.1, 0.1],
        )


def test_invalid_standard_deviations_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            observation_standard_deviations=[0.1],
        )
    with pytest.raises(ValueError, match="positive"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            observation_standard_deviations=[0.1, 0.0],
        )
    with pytest.raises(ValueError, match="relative_standard_deviation"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            relative_standard_deviation=-0.1,
        )


def test_invalid_observation_covariance_is_rejected() -> None:
    scales = [0.0, 1.0]
    with pytest.raises(ValueError, match="shape"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            scales,
            observation_covariance=np.eye(3),
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


def test_invalid_rank_tolerance_is_rejected() -> None:
    with pytest.raises(ValueError, match="rank_relative_tolerance"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            relative_standard_deviation=0.1,
            rank_relative_tolerance=0.0,
        )
    with pytest.raises(ValueError, match="less than one"):
        gaussian_multiscale_fisher_information(
            1.0,
            1.0,
            [0.0, 1.0],
            relative_standard_deviation=0.1,
            rank_relative_tolerance=1.0,
        )
