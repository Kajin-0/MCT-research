from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder import (
    GaussianCovariance,
    GaussianKernel,
    GaussianTwoScaleInversion,
    gaussian_gaussian_effective_variance,
    isotropic_gaussian_effective_variance,
    two_scale_gaussian_inversion,
)


def _rotation(angle_rad: float) -> np.ndarray:
    cosine = math.cos(angle_rad)
    sine = math.sin(angle_rad)
    return np.array([[cosine, -sine], [sine, cosine]], dtype=float)


@pytest.mark.parametrize("dimension", [1, 2, 3])
def test_isotropic_determinant_identity_matches_closed_form(dimension: int) -> None:
    variance = 0.0037
    correlation_length = 1.8
    probe_sigma = 0.65
    covariance = GaussianCovariance.isotropic(
        variance,
        correlation_length,
        dimension,
    )
    kernel = GaussianKernel.isotropic(probe_sigma, dimension)

    exact = gaussian_gaussian_effective_variance(covariance, kernel)
    closed = isotropic_gaussian_effective_variance(
        variance,
        correlation_length,
        probe_sigma,
        dimension=dimension,
    )

    assert exact == pytest.approx(closed, rel=1.0e-14)


def test_anisotropic_rotated_tensors_match_direct_determinants() -> None:
    covariance_rotation = _rotation(0.37)
    kernel_rotation = _rotation(-0.61)
    correlation_matrix = (
        covariance_rotation
        @ np.diag([0.8**2, 3.1**2])
        @ covariance_rotation.T
    )
    kernel_matrix = (
        kernel_rotation @ np.diag([0.15**2, 1.2**2]) @ kernel_rotation.T
    )
    covariance = GaussianCovariance(0.012, correlation_matrix)
    kernel = GaussianKernel(kernel_matrix)

    result = gaussian_gaussian_effective_variance(covariance, kernel)
    expected = 0.012 * math.sqrt(
        np.linalg.det(correlation_matrix)
        / np.linalg.det(correlation_matrix + 2.0 * kernel_matrix)
    )

    assert result == pytest.approx(expected, rel=1.0e-14)


def test_common_coordinate_rotation_leaves_effective_variance_invariant() -> None:
    correlation_matrix = np.diag([0.5**2, 2.0**2, 5.0**2])
    kernel_matrix = np.diag([0.2**2, 0.7**2, 1.4**2])
    covariance = GaussianCovariance(0.004, correlation_matrix)
    kernel = GaussianKernel(kernel_matrix)

    angle = 0.43
    rotation = np.array(
        [
            [math.cos(angle), -math.sin(angle), 0.0],
            [math.sin(angle), math.cos(angle), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    rotated_covariance = GaussianCovariance(
        0.004,
        rotation @ correlation_matrix @ rotation.T,
    )
    rotated_kernel = GaussianKernel(rotation @ kernel_matrix @ rotation.T)

    assert gaussian_gaussian_effective_variance(
        rotated_covariance,
        rotated_kernel,
    ) == pytest.approx(
        gaussian_gaussian_effective_variance(covariance, kernel),
        rel=1.0e-14,
    )


def test_point_probe_returns_point_variance() -> None:
    covariance = GaussianCovariance.isotropic(0.0025, 1.7, 2)
    point_kernel = GaussianKernel.isotropic(0.0, 2)

    assert gaussian_gaussian_effective_variance(
        covariance,
        point_kernel,
    ) == pytest.approx(0.0025, rel=1.0e-15)
    assert isotropic_gaussian_effective_variance(0.0025, 1.7, 0.0) == 0.0025


def test_large_correlation_length_approaches_point_variance() -> None:
    variance = 0.007
    result = isotropic_gaussian_effective_variance(
        variance,
        1.0e9,
        2.0,
        dimension=2,
    )
    assert result == pytest.approx(variance, rel=1.0e-15)


def test_large_probe_two_dimensional_asymptote() -> None:
    variance = 0.008
    correlation_length = 0.7
    probe_sigma = 1.0e5
    result = isotropic_gaussian_effective_variance(
        variance,
        correlation_length,
        probe_sigma,
        dimension=2,
    )
    scaled = result * 2.0 * probe_sigma**2 / (
        variance * correlation_length**2
    )
    assert scaled == pytest.approx(1.0, rel=1.0e-10)


def test_uniform_length_rescaling_leaves_effective_variance_invariant() -> None:
    correlation_matrix = np.array([[2.0, 0.3], [0.3, 0.8]], dtype=float)
    kernel_matrix = np.array([[0.4, -0.05], [-0.05, 0.2]], dtype=float)
    covariance = GaussianCovariance(0.01, correlation_matrix)
    kernel = GaussianKernel(kernel_matrix)
    reference = gaussian_gaussian_effective_variance(covariance, kernel)

    length_scale = 1.0e-6
    scaled = gaussian_gaussian_effective_variance(
        GaussianCovariance(0.01, correlation_matrix * length_scale**2),
        GaussianKernel(kernel_matrix * length_scale**2),
    )

    assert scaled == pytest.approx(reference, rel=1.0e-14)


def test_covariance_evaluation_uses_declared_gaussian_convention() -> None:
    covariance = GaussianCovariance.isotropic(0.02, 3.0, 2)
    assert covariance.covariance([0.0, 0.0]) == pytest.approx(0.02)
    assert covariance.covariance([3.0, 0.0]) == pytest.approx(
        0.02 * math.exp(-0.5)
    )


@pytest.mark.parametrize(
    ("point_variance", "correlation_length", "probe_sigma_1", "probe_sigma_2"),
    [
        (0.003, 0.25, 0.0, 0.4),
        (0.02, 1.7, 0.3, 2.2),
        (1.0e-6, 8.0, 1.5, 11.0),
        (0.4, 50.0, 0.1, 9.0),
    ],
)
def test_two_scale_inversion_recovers_parameters(
    point_variance: float,
    correlation_length: float,
    probe_sigma_1: float,
    probe_sigma_2: float,
) -> None:
    variance_1 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        probe_sigma_1,
    )
    variance_2 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        probe_sigma_2,
    )

    result = two_scale_gaussian_inversion(
        variance_1,
        variance_2,
        probe_sigma_1,
        probe_sigma_2,
    )

    assert isinstance(result, GaussianTwoScaleInversion)
    assert result.point_variance == pytest.approx(point_variance, rel=2.0e-12)
    assert result.correlation_length == pytest.approx(
        correlation_length,
        rel=2.0e-12,
    )


def test_two_scale_inversion_is_order_invariant() -> None:
    point_variance = 0.013
    correlation_length = 2.4
    scale_1 = 0.5
    scale_2 = 3.0
    variance_1 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_1,
    )
    variance_2 = isotropic_gaussian_effective_variance(
        point_variance,
        correlation_length,
        scale_2,
    )

    forward = two_scale_gaussian_inversion(
        variance_1,
        variance_2,
        scale_1,
        scale_2,
    )
    reverse = two_scale_gaussian_inversion(
        variance_2,
        variance_1,
        scale_2,
        scale_1,
    )

    assert reverse.point_variance == pytest.approx(forward.point_variance)
    assert reverse.correlation_length == pytest.approx(forward.correlation_length)


def test_invalid_scalar_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="variance"):
        GaussianCovariance.isotropic(0.0, 1.0, 2)
    with pytest.raises(ValueError, match="correlation_length"):
        GaussianCovariance.isotropic(1.0, 0.0, 2)
    with pytest.raises(ValueError, match="probe_sigma"):
        GaussianKernel.isotropic(-1.0, 2)
    with pytest.raises(ValueError, match="dimension"):
        GaussianKernel.isotropic(1.0, True)
    with pytest.raises(ValueError, match="point_variance"):
        isotropic_gaussian_effective_variance(-1.0, 1.0, 1.0)


def test_invalid_covariance_tensors_are_rejected() -> None:
    with pytest.raises(ValueError, match="square"):
        GaussianCovariance(1.0, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    with pytest.raises(ValueError, match="symmetric"):
        GaussianCovariance(1.0, [[1.0, 0.2], [0.1, 1.0]])
    with pytest.raises(ValueError, match="positive definite"):
        GaussianCovariance(1.0, [[1.0, 0.0], [0.0, 0.0]])
    with pytest.raises(ValueError, match="positive definite"):
        GaussianCovariance(1.0, [[1.0, 2.0], [2.0, 1.0]])


def test_invalid_kernel_tensors_are_rejected() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        GaussianKernel([[1.0, 0.2], [0.0, 1.0]])
    with pytest.raises(ValueError, match="positive semidefinite"):
        GaussianKernel([[1.0, 0.0], [0.0, -0.1]])


def test_mismatched_dimensions_and_wrong_types_are_rejected() -> None:
    covariance = GaussianCovariance.isotropic(1.0, 1.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 3)
    with pytest.raises(ValueError, match="dimensions"):
        gaussian_gaussian_effective_variance(covariance, kernel)
    with pytest.raises(TypeError, match="GaussianCovariance"):
        gaussian_gaussian_effective_variance(object(), GaussianKernel.isotropic(1.0, 2))  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="GaussianKernel"):
        gaussian_gaussian_effective_variance(covariance, object())  # type: ignore[arg-type]


def test_displacement_validation() -> None:
    covariance = GaussianCovariance.isotropic(1.0, 1.0, 2)
    with pytest.raises(ValueError, match="shape"):
        covariance.covariance([1.0])
    with pytest.raises(ValueError, match="finite"):
        covariance.covariance([1.0, math.inf])


def test_equal_probe_sizes_and_equal_variances_are_degenerate() -> None:
    with pytest.raises(ValueError, match="distinct"):
        two_scale_gaussian_inversion(0.8, 0.7, 1.0, 1.0)
    with pytest.raises(ValueError, match="degenerate"):
        two_scale_gaussian_inversion(0.8, 0.8, 1.0, 2.0)


def test_nonmonotone_two_scale_data_are_rejected() -> None:
    with pytest.raises(ValueError, match="decrease"):
        two_scale_gaussian_inversion(0.5, 0.7, 1.0, 2.0)


def test_impossibly_steep_two_scale_data_are_rejected() -> None:
    with pytest.raises(ValueError, match="point variance"):
        two_scale_gaussian_inversion(1.0, 0.1, 1.0, 2.0)
