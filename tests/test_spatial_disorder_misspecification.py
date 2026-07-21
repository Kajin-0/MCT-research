from __future__ import annotations

import math

import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss

from mct_research.spatial_disorder_misspecification import (
    SUPPORTED_COVARIANCE_FAMILIES,
    _quadrature_attenuation,
    covariance_family_misspecification_diagnostics,
    exponential_gaussian_probe_attenuation,
    fit_gaussian_surrogate_log_variance,
    gaussian_probe_filtered_variance_family,
    normalized_radial_covariance,
    pairwise_gaussian_inversions,
    three_scale_gaussian_closure,
)


def test_supported_families_share_point_value_and_integral_area() -> None:
    nodes, weights = leggauss(256)
    radius = 15.0 * (nodes + 1.0)
    radial_weights = 15.0 * weights

    for family in SUPPORTED_COVARIANCE_FAMILIES:
        at_origin = normalized_radial_covariance(family, [0.0])
        area = 2.0 * math.pi * np.dot(
            radial_weights,
            radius * normalized_radial_covariance(family, radius),
        )
        assert at_origin == pytest.approx([1.0], abs=0.0)
        assert area == pytest.approx(2.0 * math.pi, rel=4.0e-12)


def test_gaussian_filtered_variance_matches_exact_rational_form() -> None:
    point_variance = 0.017
    correlation_length = 1.8
    scales = np.array([0.0, 0.2, 0.9, 2.7, 8.0])
    result = gaussian_probe_filtered_variance_family(
        "gaussian",
        point_variance,
        correlation_length,
        scales,
    )
    expected = point_variance / (
        1.0 + 2.0 * scales**2 / correlation_length**2
    )
    assert result == pytest.approx(expected, rel=2.0e-15)


def test_exponential_quadrature_matches_exact_expression() -> None:
    for ratio in (0.01, 0.1, 0.3, 1.0, 3.0, 8.0):
        exact = exponential_gaussian_probe_attenuation(ratio)
        quadrature = _quadrature_attenuation(
            "exponential",
            ratio,
            quadrature_order=64,
            integration_limit=10.0,
        )
        assert quadrature == pytest.approx(exact, rel=2.0e-12, abs=2.0e-15)

    assert exponential_gaussian_probe_attenuation(100.0) == pytest.approx(
        4.999250187434405e-5,
        rel=2.0e-15,
    )


def test_matern_quadrature_is_converged() -> None:
    for family in ("matern32", "matern52"):
        low = gaussian_probe_filtered_variance_family(
            family,
            1.0,
            1.0,
            [0.1, 1.0, 3.0, 8.0],
            quadrature_order=64,
        )
        high = gaussian_probe_filtered_variance_family(
            family,
            1.0,
            1.0,
            [0.1, 1.0, 3.0, 8.0],
            quadrature_order=96,
        )
        assert low == pytest.approx(high, rel=3.0e-13, abs=3.0e-16)


def test_three_scale_closure_is_exact_for_gaussian_family() -> None:
    scales = np.array([0.25, 1.0, 4.0])
    values = gaussian_probe_filtered_variance_family(
        "gaussian", 0.01, 2.0, scales
    )
    closure = three_scale_gaussian_closure(scales, values)
    assert closure.signed_reciprocal_residual == pytest.approx(
        0.0, abs=2.0e-13
    )
    assert closure.normalized_reciprocal_residual == pytest.approx(
        0.0, abs=2.0e-15
    )


@pytest.mark.parametrize(
    ("family", "minimum_residual"),
    [
        ("exponential", 0.03),
        ("matern32", 0.01),
        ("matern52", 0.005),
    ],
)
def test_three_scale_closure_detects_non_gaussian_families(
    family: str,
    minimum_residual: float,
) -> None:
    diagnostics = covariance_family_misspecification_diagnostics(
        family,
        0.01,
        2.0,
        [0.25, 1.0, 4.0],
    )
    assert diagnostics.maximum_absolute_three_scale_residual > minimum_residual
    assert diagnostics.pairwise_inversions.correlation_length_spread_ratio > 1.1
    assert diagnostics.gaussian_surrogate.maximum_relative_error > 0.03


def test_two_scale_pairs_are_consistent_only_for_exact_gaussian_data() -> None:
    scales = [0.0, 0.5, 2.0, 8.0, 20.0]
    gaussian_values = gaussian_probe_filtered_variance_family(
        "gaussian", 0.01, 2.0, scales
    )
    gaussian_pairs = pairwise_gaussian_inversions(scales, gaussian_values)
    assert gaussian_pairs.point_variances == pytest.approx(
        np.full(10, 0.01), rel=3.0e-14
    )
    assert gaussian_pairs.correlation_lengths == pytest.approx(
        np.full(10, 2.0), rel=3.0e-14
    )

    exponential_values = gaussian_probe_filtered_variance_family(
        "exponential", 0.01, 2.0, scales
    )
    exponential_pairs = pairwise_gaussian_inversions(
        scales, exponential_values
    )
    assert exponential_pairs.point_variance_spread_ratio > 1.2
    assert exponential_pairs.correlation_length_spread_ratio > 3.0


def test_best_gaussian_surrogate_recovers_exact_family() -> None:
    scales = [0.0, 0.5, 2.0, 8.0, 20.0]
    values = gaussian_probe_filtered_variance_family(
        "gaussian", 0.01, 2.0, scales
    )
    fit = fit_gaussian_surrogate_log_variance(scales, values)
    assert fit.point_variance == pytest.approx(0.01, rel=5.0e-12)
    assert fit.correlation_length == pytest.approx(2.0, rel=5.0e-12)
    assert fit.rms_log_error < 5.0e-12
    assert fit.maximum_relative_error < 5.0e-12


def test_family_smoothness_orders_gaussian_surrogate_error() -> None:
    scales = [0.0, 0.5, 2.0, 8.0, 20.0]
    diagnostics = {
        family: covariance_family_misspecification_diagnostics(
            family, 0.01, 2.0, scales
        )
        for family in ("exponential", "matern32", "matern52")
    }
    assert (
        diagnostics["exponential"].gaussian_surrogate.rms_log_error
        > diagnostics["matern32"].gaussian_surrogate.rms_log_error
        > diagnostics["matern52"].gaussian_surrogate.rms_log_error
        > 0.0
    )
    assert (
        diagnostics["exponential"].maximum_absolute_three_scale_residual
        > diagnostics["matern32"].maximum_absolute_three_scale_residual
        > diagnostics["matern52"].maximum_absolute_three_scale_residual
        > 0.0
    )


def test_amplitude_and_length_unit_invariance() -> None:
    base = covariance_family_misspecification_diagnostics(
        "matern32",
        0.01,
        2.0,
        [0.0, 0.5, 2.0, 8.0, 20.0],
    )
    rescaled = covariance_family_misspecification_diagnostics(
        "matern32",
        2.5e4,
        2.0e-6,
        np.array([0.0, 0.5, 2.0, 8.0, 20.0]) * 1.0e-6,
    )
    assert rescaled.point_variance_bias_ratio == pytest.approx(
        base.point_variance_bias_ratio, rel=3.0e-12
    )
    assert rescaled.correlation_length_bias_ratio == pytest.approx(
        base.correlation_length_bias_ratio, rel=3.0e-12
    )
    assert rescaled.maximum_absolute_three_scale_residual == pytest.approx(
        base.maximum_absolute_three_scale_residual, rel=3.0e-12
    )
    assert rescaled.gaussian_surrogate.rms_log_error == pytest.approx(
        base.gaussian_surrogate.rms_log_error, rel=3.0e-12
    )


def test_weighted_fit_and_immutable_outputs() -> None:
    scales = np.array([0.0, 0.5, 2.0, 8.0, 20.0])
    values = gaussian_probe_filtered_variance_family(
        "exponential", 0.01, 2.0, scales
    )
    equal = fit_gaussian_surrogate_log_variance(scales, values)
    weighted = fit_gaussian_surrogate_log_variance(
        scales,
        values,
        weights=[10.0, 1.0, 1.0, 1.0, 1.0],
    )
    assert weighted.point_variance > equal.point_variance
    assert not values.flags.writeable
    assert not equal.predicted_variance.flags.writeable
    assert not equal.log_residuals.flags.writeable

    diagnostics = covariance_family_misspecification_diagnostics(
        "exponential", 0.01, 2.0, scales
    )
    assert not diagnostics.probe_sigmas.flags.writeable
    assert not diagnostics.true_filtered_variance.flags.writeable
    assert not diagnostics.all_three_scale_indices.flags.writeable
    assert not diagnostics.normalized_three_scale_residuals.flags.writeable
    assert not diagnostics.pairwise_inversions.pair_indices.flags.writeable


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="family"):
        normalized_radial_covariance("unknown", [0.0])
    with pytest.raises(ValueError, match="non-negative"):
        normalized_radial_covariance("gaussian", [-1.0])
    with pytest.raises(ValueError, match="point_variance"):
        gaussian_probe_filtered_variance_family("gaussian", 0.0, 1.0, [1.0])
    with pytest.raises(ValueError, match="correlation_length"):
        gaussian_probe_filtered_variance_family(
            "gaussian", 1.0, math.inf, [1.0]
        )
    with pytest.raises(ValueError, match="strictly increasing"):
        three_scale_gaussian_closure(
            [0.0, 1.0, 1.0], [1.0, 0.5, 0.4]
        )
    with pytest.raises(ValueError, match="exactly three"):
        three_scale_gaussian_closure(
            [0.0, 1.0, 2.0, 3.0],
            [1.0, 0.5, 0.3, 0.2],
        )
    with pytest.raises(ValueError, match="shape"):
        fit_gaussian_surrogate_log_variance(
            [0.0, 1.0, 2.0],
            [1.0, 0.5, 0.3],
            weights=[1.0, 1.0],
        )
    with pytest.raises(ValueError, match="at least 16"):
        gaussian_probe_filtered_variance_family(
            "matern32",
            1.0,
            1.0,
            [1.0],
            quadrature_order=8,
        )
