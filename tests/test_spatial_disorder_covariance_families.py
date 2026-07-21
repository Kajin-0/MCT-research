from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_covariance_families import (
    SUPPORTED_MATERN_SMOOTHNESS,
    gaussian_reciprocal_linearity_fit,
    gaussian_reference_variance,
    gaussian_three_scale_falsification,
    matern_gaussian_probe_attenuation_2d,
    matern_gaussian_probe_variance_2d,
    matern_half_integer_correlation,
)


def _simpson(function, lower: float, upper: float, intervals: int = 30000) -> float:
    if intervals % 2:
        raise ValueError("intervals must be even")
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * i) for i in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * i) for i in range(2, intervals, 2))
    return total * step / 3.0


def _matern_polynomial(z: float, smoothness: float) -> float:
    if smoothness == 0.5:
        return 1.0
    if smoothness == 1.5:
        return 1.0 + z
    return 1.0 + z + z * z / 3.0


def _independent_radial_attenuation(ratio: float, smoothness: float) -> float:
    rho = math.sqrt(2.0 * smoothness) * ratio
    integrand = lambda z: (
        z
        * _matern_polynomial(z, smoothness)
        * math.exp(-z - z * z / (4.0 * rho * rho))
        / (2.0 * rho * rho)
    )
    return _simpson(integrand, 0.0, 35.0)


@pytest.mark.parametrize("smoothness", SUPPORTED_MATERN_SMOOTHNESS)
def test_half_integer_correlation_is_normalized_and_monotone(smoothness: float) -> None:
    distances = np.array([0.0, 0.2, 1.0, 3.0])
    values = matern_half_integer_correlation(distances, 1.0, smoothness)
    assert values[0] == pytest.approx(1.0)
    assert np.all(np.diff(values) < 0.0)
    assert not values.flags.writeable


def test_half_integer_correlation_known_polynomials() -> None:
    distance = np.array([0.4, 1.2])
    exponential = np.exp(-distance)
    assert matern_half_integer_correlation(distance, 1.0, 0.5) == pytest.approx(
        exponential
    )

    z_3 = math.sqrt(3.0) * distance
    assert matern_half_integer_correlation(distance, 1.0, 1.5) == pytest.approx(
        (1.0 + z_3) * np.exp(-z_3)
    )

    z_5 = math.sqrt(5.0) * distance
    assert matern_half_integer_correlation(distance, 1.0, 2.5) == pytest.approx(
        (1.0 + z_5 + z_5**2 / 3.0) * np.exp(-z_5)
    )


@pytest.mark.parametrize("smoothness", SUPPORTED_MATERN_SMOOTHNESS)
@pytest.mark.parametrize("ratio", [0.15, 0.7, 2.0, 5.0])
def test_matern_probe_attenuation_matches_independent_radial_quadrature(
    smoothness: float,
    ratio: float,
) -> None:
    obtained = matern_gaussian_probe_attenuation_2d(
        ratio,
        1.0,
        smoothness,
    )
    expected = _independent_radial_attenuation(ratio, smoothness)
    assert obtained == pytest.approx(expected, rel=3.0e-10, abs=3.0e-13)


@pytest.mark.parametrize("smoothness", SUPPORTED_MATERN_SMOOTHNESS)
def test_point_and_large_probe_limits(smoothness: float) -> None:
    assert matern_gaussian_probe_attenuation_2d(
        0.0, 2.0, smoothness
    ) == pytest.approx(1.0)

    ratio = 100.0
    attenuation = matern_gaussian_probe_attenuation_2d(
        ratio,
        1.0,
        smoothness,
    )
    # Under the standard sqrt(2 nu)/ell Matérn parameterization, every supported
    # family has the same leading inverse-area coefficient.
    assert 2.0 * ratio**2 * attenuation == pytest.approx(1.0, rel=4.0e-4)


def test_gaussian_reciprocal_curvature_is_zero() -> None:
    scales = np.array([0.5, 5.0, 10.0])
    values = gaussian_reference_variance(2.5e-5, 5.0, scales)
    result = gaussian_three_scale_falsification(scales, values)

    assert result.reciprocal_second_divided_difference == pytest.approx(
        0.0, abs=2.0e-8
    )
    # Reciprocal values are O(1e5), so this absolute residual is still at the
    # binary64 interpolation floor and corresponds to zero relative variance error.
    assert result.reciprocal_middle_residual == pytest.approx(0.0, abs=2.0e-10)
    assert result.middle_relative_prediction_error == pytest.approx(
        0.0, abs=2.0e-15
    )
    assert result.endpoint_fitted_point_variance == pytest.approx(2.5e-5)
    assert result.endpoint_fitted_correlation_length == pytest.approx(5.0)


@pytest.mark.parametrize(
    "smoothness, expected_relative_error, expected_standardized_residual",
    [
        (0.5, 0.17481782804557172, 4.119513842708676),
        (1.5, 0.08086470140958815, 2.0123485823984772),
        (2.5, 0.05206533772268234, 1.319071250152875),
    ],
)
def test_matern_three_scale_reference(
    smoothness: float,
    expected_relative_error: float,
    expected_standardized_residual: float,
) -> None:
    scales = np.array([0.5, 5.0, 10.0])
    values = matern_gaussian_probe_variance_2d(
        1.0,
        5.0,
        scales,
        smoothness,
    )
    standard_deviations = 0.03 * values
    result = gaussian_three_scale_falsification(
        scales,
        values,
        variance_standard_deviations=standard_deviations,
    )

    assert result.middle_relative_prediction_error == pytest.approx(
        expected_relative_error, rel=3.0e-12
    )
    assert result.standardized_reciprocal_residual == pytest.approx(
        expected_standardized_residual, rel=3.0e-12
    )
    assert result.reciprocal_second_divided_difference != pytest.approx(
        0.0, abs=1.0e-12
    )


def test_weighted_reciprocal_fit_recovers_exact_gaussian_parameters() -> None:
    scales = np.array([0.0, 0.3, 1.2, 3.0, 8.0])
    point_variance = 0.017
    correlation_length = 1.8
    values = gaussian_reference_variance(point_variance, correlation_length, scales)
    result = gaussian_reciprocal_linearity_fit(
        scales,
        values,
        variance_standard_deviations=0.02 * values,
    )

    assert result.fitted_point_variance == pytest.approx(
        point_variance, rel=3.0e-14
    )
    assert result.fitted_correlation_length == pytest.approx(
        correlation_length, rel=3.0e-14
    )
    assert result.maximum_absolute_relative_variance_residual < 3.0e-14
    assert result.chi_square == pytest.approx(0.0, abs=2.0e-25)
    assert result.degrees_of_freedom == 3
    assert result.reduced_chi_square == pytest.approx(0.0, abs=1.0e-25)
    assert result.coefficient_covariance is not None


def test_two_scales_fit_exactly_but_three_scales_test_family() -> None:
    scales = np.array([0.5, 5.0, 10.0])
    values = matern_gaussian_probe_variance_2d(1.0, 5.0, scales, 0.5)

    two_scale = gaussian_reciprocal_linearity_fit(
        scales[[0, 2]],
        values[[0, 2]],
    )
    assert two_scale.degrees_of_freedom == 0
    assert two_scale.maximum_absolute_relative_variance_residual < 3.0e-15

    three_scale = gaussian_reciprocal_linearity_fit(scales, values)
    assert three_scale.degrees_of_freedom == 1
    assert three_scale.maximum_absolute_relative_variance_residual > 0.05


def test_scaling_and_length_unit_invariance() -> None:
    scales = np.array([0.5, 5.0, 10.0])
    base = matern_gaussian_probe_variance_2d(1.0, 5.0, scales, 1.5)
    rescaled = matern_gaussian_probe_variance_2d(
        7.0,
        5.0e-6,
        scales * 1.0e-6,
        1.5,
    )
    assert rescaled == pytest.approx(7.0 * base, rel=3.0e-14)

    base_test = gaussian_three_scale_falsification(scales, base)
    rescaled_test = gaussian_three_scale_falsification(
        scales * 1.0e-6,
        7.0 * base,
    )
    assert rescaled_test.middle_relative_prediction_error == pytest.approx(
        base_test.middle_relative_prediction_error,
        rel=3.0e-14,
    )


@pytest.mark.parametrize(
    "operation, message",
    [
        (
            lambda: matern_half_integer_correlation([0.0], 1.0, 1.0),
            "smoothness",
        ),
        (
            lambda: matern_half_integer_correlation([-1.0], 1.0, 0.5),
            "distance",
        ),
        (
            lambda: matern_gaussian_probe_attenuation_2d(-1.0, 1.0, 0.5),
            "probe_sigma",
        ),
        (
            lambda: matern_gaussian_probe_attenuation_2d(
                1.0, 1.0, 0.5, quadrature_order=8
            ),
            "quadrature_order",
        ),
        (
            lambda: gaussian_three_scale_falsification(
                [1.0, 1.0, 2.0], [1.0, 0.8, 0.5]
            ),
            "distinct",
        ),
        (
            lambda: gaussian_reciprocal_linearity_fit(
                [1.0, 2.0], [1.0, 1.2]
            ),
            "positive Gaussian parameters",
        ),
    ],
)
def test_invalid_inputs(operation, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        operation()
