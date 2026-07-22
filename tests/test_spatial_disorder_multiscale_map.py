from __future__ import annotations

import numpy as np
import pytest

from mct_research.spatial_disorder import GaussianCovariance
from mct_research.spatial_disorder_map_sampling import (
    gaussian_map_sampling_diagnostics,
    regular_grid_positions,
)
from mct_research.spatial_disorder_multiscale_map import (
    gaussian_multiscale_map_covariance_blocks,
    gaussian_multiscale_map_fisher_comparison,
    gaussian_multiscale_map_variance_statistics,
)

POINT_VARIANCE = 0.005**2
CORRELATION_LENGTH = 2.0
PROBE_SIGMAS = np.array([0.23094, 1.15470, 4.61880])


def _controlled_result(shape=(10, 10), spacing=0.5):
    covariance = GaussianCovariance.isotropic(
        POINT_VARIANCE, CORRELATION_LENGTH, 2
    )
    positions = regular_grid_positions(shape, spacing)
    blocks = gaussian_multiscale_map_covariance_blocks(
        covariance, positions, PROBE_SIGMAS
    )
    statistics = gaussian_multiscale_map_variance_statistics(
        blocks, PROBE_SIGMAS
    )
    comparison = gaussian_multiscale_map_fisher_comparison(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        PROBE_SIGMAS,
        statistics.delta_log_variance_covariance,
        nominal_pixel_count=statistics.nominal_pixel_count,
    )
    return blocks, statistics, comparison


def test_diagonal_recovers_single_scale_map_quadratic_form_moments() -> None:
    blocks, statistics, _ = _controlled_result()
    for index in range(PROBE_SIGMAS.size):
        single = gaussian_map_sampling_diagnostics(blocks[index, index])
        assert statistics.expected_naive_variances[index] == pytest.approx(
            single.naive_sample_variance_expectation, rel=3.0e-14
        )
        assert statistics.raw_variance_estimator_covariance[index, index] == pytest.approx(
            single.naive_sample_variance_variance, rel=3.0e-14
        )
        assert statistics.moment_matched_effective_degrees_of_freedom[index] == pytest.approx(
            single.variance_effective_degrees_of_freedom, rel=3.0e-14
        )


def test_controlled_dense_raster_reference() -> None:
    _, statistics, comparison = _controlled_result()
    assert statistics.nominal_pixel_count == 100
    assert statistics.deterministic_bias_factors == pytest.approx(
        [0.52805134, 0.40194623, 0.08300702], rel=3.0e-8
    )
    assert statistics.delta_log_variance_standard_deviations == pytest.approx(
        [0.69489827, 0.77465168, 0.95528224], rel=3.0e-8
    )
    assert statistics.delta_log_variance_correlation[0, 1] == pytest.approx(
        0.94595396, rel=3.0e-8
    )
    assert statistics.delta_log_variance_correlation[0, 2] == pytest.approx(
        0.18004355, rel=3.0e-8
    )
    assert statistics.delta_log_variance_correlation[1, 2] == pytest.approx(
        0.28842180, rel=3.0e-8
    )
    assert comparison.parameter_standard_deviation_inflation == pytest.approx(
        [4.43971118, 2.86773360], rel=3.0e-8
    )
    assert comparison.parameter_covariance_determinant_inflation == pytest.approx(
        404.68548880, rel=3.0e-8
    )


def test_bias_correction_leaves_log_covariance_invariant() -> None:
    _, statistics, _ = _controlled_result()
    reconstructed = statistics.bias_corrected_estimator_covariance / np.outer(
        statistics.marginal_filtered_variances,
        statistics.marginal_filtered_variances,
    )
    assert np.allclose(
        reconstructed,
        statistics.delta_log_variance_covariance,
        rtol=3.0e-14,
        atol=1.0e-15,
    )


def test_same_raster_cross_covariance_matches_monte_carlo() -> None:
    covariance = GaussianCovariance.isotropic(1.0, 2.0, 2)
    scales = np.array([0.4, 1.2, 3.5])
    positions = regular_grid_positions((4, 4), 1.0)
    blocks = gaussian_multiscale_map_covariance_blocks(
        covariance, positions, scales
    )
    exact = gaussian_multiscale_map_variance_statistics(blocks, scales)
    full_covariance = np.block(
        [
            [np.asarray(blocks[row, column]) for column in range(scales.size)]
            for row in range(scales.size)
        ]
    )
    generator = np.random.default_rng(20260722)
    samples = generator.multivariate_normal(
        np.zeros(full_covariance.shape[0]),
        full_covariance,
        size=60000,
        method="cholesky",
    )
    pixel_count = positions.shape[0]
    map_variances = np.column_stack(
        [
            np.var(
                samples[:, index * pixel_count : (index + 1) * pixel_count],
                axis=1,
                ddof=1,
            )
            for index in range(scales.size)
        ]
    )
    empirical_mean = np.mean(map_variances, axis=0)
    empirical_covariance = np.cov(map_variances, rowvar=False, ddof=1)
    assert empirical_mean == pytest.approx(
        exact.expected_naive_variances, rel=0.015
    )
    assert empirical_covariance == pytest.approx(
        exact.raw_variance_estimator_covariance, rel=0.04
    )


def test_fixed_field_of_view_oversampling_does_not_create_information() -> None:
    _, coarse_statistics, coarse_comparison = _controlled_result((10, 10), 0.5)
    _, fine_statistics, fine_comparison = _controlled_result((20, 20), 0.25)
    assert (coarse_statistics.nominal_pixel_count, fine_statistics.nominal_pixel_count) == (
        100,
        400,
    )
    coarse_full_sd = np.sqrt(np.diag(coarse_comparison.full_parameter_covariance))
    fine_full_sd = np.sqrt(np.diag(fine_comparison.full_parameter_covariance))
    assert fine_full_sd[1] / coarse_full_sd[1] > 0.995
    assert fine_full_sd[0] / coarse_full_sd[0] > 0.995

    coarse_nominal_sd = np.sqrt(
        np.diag(coarse_comparison.nominal_independent_pixel_parameter_covariance)
    )
    fine_nominal_sd = np.sqrt(
        np.diag(fine_comparison.nominal_independent_pixel_parameter_covariance)
    )
    assert fine_nominal_sd[1] / coarse_nominal_sd[1] == pytest.approx(
        np.sqrt(99.0 / 399.0), rel=3.0e-14
    )
    assert (
        fine_comparison.parameter_covariance_determinant_inflation
        / coarse_comparison.parameter_covariance_determinant_inflation
        > 15.0
    )


def test_scale_reordering_is_covariant() -> None:
    covariance = GaussianCovariance.isotropic(
        POINT_VARIANCE, CORRELATION_LENGTH, 2
    )
    positions = regular_grid_positions((6, 5), 0.8)
    order = np.array([2, 0, 1])
    original_blocks = gaussian_multiscale_map_covariance_blocks(
        covariance, positions, PROBE_SIGMAS
    )
    original = gaussian_multiscale_map_variance_statistics(
        original_blocks, PROBE_SIGMAS
    )
    reordered_scales = PROBE_SIGMAS[order]
    reordered_blocks = gaussian_multiscale_map_covariance_blocks(
        covariance, positions, reordered_scales
    )
    reordered = gaussian_multiscale_map_variance_statistics(
        reordered_blocks, reordered_scales
    )
    assert reordered.expected_naive_variances == pytest.approx(
        original.expected_naive_variances[order], rel=3.0e-14
    )
    assert reordered.delta_log_variance_covariance == pytest.approx(
        original.delta_log_variance_covariance[np.ix_(order, order)],
        rel=3.0e-14,
    )


def test_length_unit_translation_and_map_permutation_invariance() -> None:
    covariance = GaussianCovariance.isotropic(
        POINT_VARIANCE, CORRELATION_LENGTH, 2
    )
    positions = regular_grid_positions((4, 5), [0.7, 1.1], origin=[2.0, -3.0])
    reference_blocks = gaussian_multiscale_map_covariance_blocks(
        covariance, positions, PROBE_SIGMAS
    )
    reference = gaussian_multiscale_map_variance_statistics(
        reference_blocks, PROBE_SIGMAS
    )

    unit = 1000.0
    transformed_positions = np.asarray(positions) * unit + np.array([11.0, -7.0])
    transformed_blocks = gaussian_multiscale_map_covariance_blocks(
        GaussianCovariance.isotropic(
            POINT_VARIANCE, CORRELATION_LENGTH * unit, 2
        ),
        transformed_positions,
        PROBE_SIGMAS * unit,
    )
    transformed = gaussian_multiscale_map_variance_statistics(
        transformed_blocks, PROBE_SIGMAS * unit
    )
    assert transformed.delta_log_variance_covariance == pytest.approx(
        reference.delta_log_variance_covariance, rel=3.0e-14
    )

    permutation = np.array(
        [7, 0, 12, 3, 18, 5, 11, 2, 19, 1, 8, 14, 6, 10, 15, 4, 9, 13, 16, 17]
    )
    permuted_blocks = reference_blocks[:, :, permutation][:, :, :, permutation]
    permuted = gaussian_multiscale_map_variance_statistics(
        permuted_blocks, PROBE_SIGMAS
    )
    assert permuted.expected_naive_variances == pytest.approx(
        reference.expected_naive_variances, rel=3.0e-14
    )
    assert permuted.delta_log_variance_covariance == pytest.approx(
        reference.delta_log_variance_covariance, rel=3.0e-14
    )


@pytest.mark.parametrize(
    "operation",
    [
        lambda: gaussian_multiscale_map_covariance_blocks(
            GaussianCovariance.isotropic(1.0, 1.0, 2),
            [[0.0, 0.0]],
            [0.5, 1.0],
        ),
        lambda: gaussian_multiscale_map_covariance_blocks(
            GaussianCovariance.isotropic(1.0, 1.0, 2),
            [[0.0, 0.0], [1.0, 0.0]],
            [0.5, 0.5],
        ),
        lambda: gaussian_multiscale_map_variance_statistics(
            np.zeros((2, 2, 1, 1)), [0.5, 1.0]
        ),
        lambda: gaussian_multiscale_map_fisher_comparison(
            1.0,
            1.0,
            [0.5, 1.0],
            np.eye(2),
            nominal_pixel_count=1,
        ),
    ],
)
def test_invalid_inputs_are_rejected(operation) -> None:
    with pytest.raises((TypeError, ValueError)):
        operation()
