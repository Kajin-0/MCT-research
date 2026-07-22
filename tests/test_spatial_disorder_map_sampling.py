from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder import (
    GaussianCovariance,
    GaussianKernel,
    gaussian_gaussian_effective_variance,
)
from mct_research.spatial_disorder_map_sampling import (
    gaussian_filtered_cross_covariance,
    gaussian_map_covariance_matrix,
    gaussian_map_sampling_diagnostics,
    gaussian_regular_grid_sampling_diagnostics,
    regular_grid_positions,
)


def test_zero_separation_recovers_filtered_variance() -> None:
    covariance = GaussianCovariance(2.5e-5, [[4.0, 0.6], [0.6, 2.0]])
    kernel = GaussianKernel([[0.5, 0.1], [0.1, 0.8]])
    value = gaussian_filtered_cross_covariance(
        covariance, kernel, kernel, [0.0, 0.0]
    )
    assert value == pytest.approx(
        gaussian_gaussian_effective_variance(covariance, kernel), rel=3.0e-15
    )


def test_point_probe_and_exchange_symmetry() -> None:
    covariance = GaussianCovariance.isotropic(0.01, 3.0, 2)
    point = GaussianKernel.isotropic(0.0, 2)
    displacement = np.array([1.2, -0.7])
    assert gaussian_filtered_cross_covariance(
        covariance, point, point, displacement
    ) == pytest.approx(covariance.covariance(displacement), rel=3.0e-15)

    left = GaussianKernel(np.diag([0.2, 0.8]))
    right = GaussianKernel([[0.7, 0.1], [0.1, 0.4]])
    forward = gaussian_filtered_cross_covariance(
        covariance, left, right, displacement
    )
    reverse = gaussian_filtered_cross_covariance(
        covariance, right, left, -displacement
    )
    assert forward == pytest.approx(reverse, rel=3.0e-15)


def test_cross_covariance_is_rotation_invariant() -> None:
    angle = 0.61
    rotation = np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    )
    material = np.array([[4.0, 0.4], [0.4, 1.5]])
    left = np.array([[0.3, 0.05], [0.05, 0.8]])
    right = np.array([[0.9, -0.08], [-0.08, 0.4]])
    displacement = np.array([1.3, -0.6])
    original = gaussian_filtered_cross_covariance(
        GaussianCovariance(0.01, material),
        GaussianKernel(left),
        GaussianKernel(right),
        displacement,
    )
    rotated = gaussian_filtered_cross_covariance(
        GaussianCovariance(0.01, rotation @ material @ rotation.T),
        GaussianKernel(rotation @ left @ rotation.T),
        GaussianKernel(rotation @ right @ rotation.T),
        rotation @ displacement,
    )
    assert rotated == pytest.approx(original, rel=2.0e-14)


def test_mixed_kernel_map_covariance_is_symmetric_psd() -> None:
    covariance = GaussianCovariance.isotropic(0.01, 2.0, 2)
    positions = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    kernels = [
        GaussianKernel.isotropic(scale, 2) for scale in (0.0, 0.5, 1.0, 1.5)
    ]
    matrix = gaussian_map_covariance_matrix(covariance, positions, kernels)
    assert np.allclose(matrix, matrix.T, rtol=0.0, atol=1.0e-15)
    assert float(np.min(np.linalg.eigvalsh(matrix))) > -1.0e-14
    assert matrix[3, 3] < matrix[2, 2] < matrix[1, 1] < matrix[0, 0]


def test_independent_map_recovers_classical_results() -> None:
    count, marginal = 17, 3.2
    result = gaussian_map_sampling_diagnostics(np.eye(count) * marginal)
    assert result.map_mean_variance == pytest.approx(marginal / count)
    assert result.map_mean_effective_sample_count == pytest.approx(count)
    assert result.naive_sample_variance_expectation == pytest.approx(marginal)
    assert result.naive_sample_variance_relative_bias == pytest.approx(0.0)
    assert result.naive_sample_variance_variance == pytest.approx(
        2.0 * marginal**2 / (count - 1)
    )
    assert result.variance_effective_degrees_of_freedom == pytest.approx(count - 1)


def test_dense_hundred_pixel_reference() -> None:
    covariance = GaussianCovariance.isotropic(0.005**2, 2.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 2)
    _, result = gaussian_regular_grid_sampling_diagnostics(
        covariance, kernel, (10, 10), 0.5
    )
    assert result.nominal_sample_count == 100
    assert result.average_marginal_variance == pytest.approx(
        1.6666666666666667e-5
    )
    assert result.map_mean_effective_sample_count == pytest.approx(
        1.7377128548163472, rel=2.0e-13
    )
    assert (
        result.naive_sample_variance_expectation / result.average_marginal_variance
        == pytest.approx(0.4288191214959078, rel=2.0e-13)
    )
    assert result.variance_effective_degrees_of_freedom == pytest.approx(
        3.4783258588131654, rel=2.0e-13
    )


def test_spacing_restores_independent_information() -> None:
    covariance = GaussianCovariance.isotropic(0.005**2, 2.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 2)
    results = [
        gaussian_regular_grid_sampling_diagnostics(
            covariance, kernel, (10, 10), spacing
        )[1]
        for spacing in (0.5, 1.0, 2.0, 4.0, 8.0)
    ]
    assert all(
        left.map_mean_effective_sample_count < right.map_mean_effective_sample_count
        for left, right in zip(results, results[1:])
    )
    assert all(
        left.variance_effective_degrees_of_freedom
        < right.variance_effective_degrees_of_freedom
        for left, right in zip(results, results[1:])
    )
    assert abs(results[-1].naive_sample_variance_relative_bias) < 2.0e-4
    assert results[-1].map_mean_effective_sample_count > 98.0


def test_fixed_field_of_view_oversampling_adds_negligible_information() -> None:
    covariance = GaussianCovariance.isotropic(0.005**2, 2.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 2)
    coarse = gaussian_regular_grid_sampling_diagnostics(
        covariance, kernel, (10, 10), 0.5
    )[1]
    fine = gaussian_regular_grid_sampling_diagnostics(
        covariance, kernel, (20, 20), 0.25
    )[1]
    assert (coarse.nominal_sample_count, fine.nominal_sample_count) == (100, 400)
    assert (
        fine.map_mean_effective_sample_count
        / coarse.map_mean_effective_sample_count
        < 1.004
    )
    assert abs(
        fine.naive_sample_variance_relative_bias
        - coarse.naive_sample_variance_relative_bias
    ) < 0.003


def test_unit_translation_and_permutation_invariance() -> None:
    covariance = GaussianCovariance.isotropic(0.01, 2.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 2)
    positions = regular_grid_positions((4, 5), [0.7, 1.1], origin=[2.0, -3.0])
    reference = gaussian_map_covariance_matrix(covariance, positions, kernel)

    scale = 1000.0
    transformed = gaussian_map_covariance_matrix(
        GaussianCovariance.isotropic(0.01, 2.0 * scale, 2),
        np.asarray(positions) * scale + np.array([7.0, -11.0]),
        GaussianKernel.isotropic(scale, 2),
    )
    assert np.allclose(transformed, reference, rtol=2.0e-14, atol=1.0e-16)

    permutation = np.array(
        [7, 0, 12, 3, 18, 5, 11, 2, 19, 1, 8, 14, 6, 10, 15, 4, 9, 13, 16, 17]
    )
    left = gaussian_map_sampling_diagnostics(reference)
    right = gaussian_map_sampling_diagnostics(
        reference[np.ix_(permutation, permutation)]
    )
    assert right.map_mean_variance == pytest.approx(
        left.map_mean_variance, rel=2.0e-14
    )
    assert right.naive_sample_variance_expectation == pytest.approx(
        left.naive_sample_variance_expectation, rel=2.0e-14
    )
    assert right.naive_sample_variance_variance == pytest.approx(
        left.naive_sample_variance_variance, rel=2.0e-14
    )


def test_quadratic_form_moments_match_monte_carlo() -> None:
    covariance = GaussianCovariance.isotropic(1.0, 2.0, 2)
    kernel = GaussianKernel.isotropic(0.8, 2)
    positions = regular_grid_positions((4, 4), 1.0)
    matrix = np.asarray(
        gaussian_map_covariance_matrix(covariance, positions, kernel)
    )
    exact = gaussian_map_sampling_diagnostics(matrix)

    generator = np.random.default_rng(20260722)
    samples = generator.multivariate_normal(
        np.zeros(matrix.shape[0]), matrix, size=50000, method="cholesky"
    )
    means = np.mean(samples, axis=1)
    variances = np.var(samples, axis=1, ddof=1)
    assert np.var(means, ddof=1) == pytest.approx(
        exact.map_mean_variance, rel=0.025
    )
    assert np.mean(variances) == pytest.approx(
        exact.naive_sample_variance_expectation, rel=0.015
    )
    assert np.var(variances, ddof=1) == pytest.approx(
        exact.naive_sample_variance_variance, rel=0.04
    )


@pytest.mark.parametrize(
    "operation",
    [
        lambda: regular_grid_positions((), 1.0),
        lambda: regular_grid_positions((2, 2), 0.0),
        lambda: gaussian_map_sampling_diagnostics(np.eye(1)),
        lambda: gaussian_map_sampling_diagnostics(
            np.array([[1.0, 2.0], [2.0, 1.0]])
        ),
        lambda: gaussian_filtered_cross_covariance(
            GaussianCovariance.isotropic(1.0, 1.0, 2),
            GaussianKernel.isotropic(1.0, 2),
            GaussianKernel.isotropic(1.0, 3),
            [0.0, 0.0],
        ),
        lambda: gaussian_map_covariance_matrix(
            GaussianCovariance.isotropic(1.0, 1.0, 2),
            [[0.0, 0.0], [1.0, 0.0]],
            [GaussianKernel.isotropic(1.0, 2)],
        ),
    ],
)
def test_invalid_inputs_are_rejected(operation) -> None:
    with pytest.raises((TypeError, ValueError)):
        operation()
