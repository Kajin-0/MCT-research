from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_instrument import (
    CompositeInstrumentKernel,
    composite_instrument_effective_variance,
    composite_instrument_log_sensitivity,
    gaussian_psf_rectangular_pixel_axis_ratio,
    gaussian_psf_rectangular_pixel_axis_ratio_quadrature,
    moment_matched_gaussian_axis_ratio,
    propagate_composite_instrument_calibration,
)
from mct_research.spatial_disorder_theorems import (
    top_hat_gaussian_effective_variance_1d,
)


@pytest.mark.parametrize(
    "correlation_length, psf_sigma, pixel_width",
    [
        (0.2, 0.0, 0.0),
        (0.2, 0.5, 0.0),
        (0.2, 0.0, 1.0),
        (1.0, 0.3, 2.0),
        (2.0, 2.0, 5.0),
        (10.0, 0.1, 30.0),
    ],
)
def test_axis_formula_matches_independent_triangular_quadrature(
    correlation_length: float,
    psf_sigma: float,
    pixel_width: float,
) -> None:
    exact = gaussian_psf_rectangular_pixel_axis_ratio(
        correlation_length,
        psf_sigma,
        pixel_width,
    )
    numerical = gaussian_psf_rectangular_pixel_axis_ratio_quadrature(
        correlation_length,
        psf_sigma,
        pixel_width,
        quadrature_order=160,
    )
    assert exact == pytest.approx(numerical, rel=2.0e-13, abs=2.0e-15)


def test_axis_formula_recovers_declared_limits() -> None:
    xi = 1.7
    sigma = 0.8
    width = 2.3
    gaussian_only = gaussian_psf_rectangular_pixel_axis_ratio(xi, sigma, 0.0)
    assert gaussian_only == pytest.approx(
        xi / math.sqrt(xi**2 + 2.0 * sigma**2), rel=2.0e-15
    )

    pixel_only = gaussian_psf_rectangular_pixel_axis_ratio(xi, 0.0, width)
    assert pixel_only == pytest.approx(
        top_hat_gaussian_effective_variance_1d(1.0, xi, width),
        rel=2.0e-15,
    )
    assert gaussian_psf_rectangular_pixel_axis_ratio(xi, 0.0, 0.0) == 1.0


def test_moment_matched_gaussian_is_second_moment_not_exact_shape() -> None:
    xi = 2.0
    sigma = 2.0
    width = 5.0
    exact = gaussian_psf_rectangular_pixel_axis_ratio(xi, sigma, width)
    approximation = moment_matched_gaussian_axis_ratio(xi, sigma, width)
    assert exact == pytest.approx(0.49466379334485655, rel=3.0e-14)
    assert approximation == pytest.approx(0.4974160033738069, rel=3.0e-14)
    assert approximation / exact - 1.0 == pytest.approx(
        0.00556379922278194, rel=3.0e-13
    )


def test_reference_composite_kernel_factorization() -> None:
    kernel = CompositeInstrumentKernel(
        psf_sigma_x=2.0,
        psf_sigma_y=2.0,
        pixel_width_x=5.0,
        pixel_width_y=5.0,
        attenuation_coefficient=0.5,
        thickness=10.0,
    )
    result = composite_instrument_effective_variance(
        0.01,
        [2.0, 2.0, 2.0],
        kernel,
        depth_quadrature_order=160,
    )
    assert result.lateral_ratio_x == pytest.approx(
        0.49466379334485655, rel=3.0e-14
    )
    assert result.lateral_ratio_y == pytest.approx(
        0.49466379334485655, rel=3.0e-14
    )
    assert result.depth_ratio == pytest.approx(
        0.6644455179635949, rel=3.0e-13
    )
    assert result.exact_variance_ratio == pytest.approx(
        result.lateral_ratio_x * result.lateral_ratio_y * result.depth_ratio,
        rel=2.0e-15,
    )
    assert result.exact_variance_ratio == pytest.approx(
        0.16258468104950405, rel=3.0e-13
    )
    assert result.effective_variance == pytest.approx(
        0.0016258468104950405, rel=3.0e-13
    )
    assert result.equivalent_gaussian_relative_error == pytest.approx(
        0.011158554307354906, rel=3.0e-12
    )


def test_pixel_dominated_regime_exceeds_one_percent_equivalent_gaussian_error() -> None:
    kernel = CompositeInstrumentKernel(
        psf_sigma_x=3.8,
        psf_sigma_y=3.8,
        pixel_width_x=44.2,
        pixel_width_y=44.2,
        attenuation_coefficient=0.5,
        thickness=10.0,
    )
    result = composite_instrument_effective_variance(
        1.0,
        [5.0, 5.0, 2.0],
        kernel,
        depth_quadrature_order=128,
    )
    assert result.equivalent_gaussian_relative_error == pytest.approx(
        0.08876457091123835, rel=3.0e-12
    )
    assert result.equivalent_gaussian_relative_error > 0.08


def test_front_back_reflection_leaves_stationary_depth_variance_unchanged() -> None:
    front = CompositeInstrumentKernel(1.0, 2.0, 3.0, 4.0, 0.7, 8.0, "front")
    back = CompositeInstrumentKernel(1.0, 2.0, 3.0, 4.0, 0.7, 8.0, "back")
    front_result = composite_instrument_effective_variance(
        1.0, [1.5, 2.5, 0.8], front, depth_quadrature_order=128
    )
    back_result = composite_instrument_effective_variance(
        1.0, [1.5, 2.5, 0.8], back, depth_quadrature_order=128
    )
    assert back_result.exact_variance_ratio == pytest.approx(
        front_result.exact_variance_ratio, rel=3.0e-14
    )


def test_length_unit_invariance() -> None:
    kernel = CompositeInstrumentKernel(2.0, 3.0, 5.0, 7.0, 0.4, 9.0)
    base = composite_instrument_effective_variance(
        1.0, [1.5, 2.5, 0.8], kernel, depth_quadrature_order=128
    )
    scale = 1.0e-6
    rescaled_kernel = CompositeInstrumentKernel(
        2.0 * scale,
        3.0 * scale,
        5.0 * scale,
        7.0 * scale,
        0.4 / scale,
        9.0 * scale,
    )
    rescaled = composite_instrument_effective_variance(
        7.0,
        np.array([1.5, 2.5, 0.8]) * scale,
        rescaled_kernel,
        depth_quadrature_order=128,
    )
    assert rescaled.exact_variance_ratio == pytest.approx(
        base.exact_variance_ratio, rel=3.0e-13
    )
    assert rescaled.equivalent_gaussian_relative_error == pytest.approx(
        base.equivalent_gaussian_relative_error, rel=3.0e-13
    )
    assert rescaled.effective_variance == pytest.approx(
        7.0 * base.effective_variance, rel=3.0e-13
    )


def test_reference_log_sensitivity_and_step_convergence() -> None:
    kernel = CompositeInstrumentKernel(2.0, 2.0, 5.0, 5.0, 0.5, 10.0)
    sensitivity = composite_instrument_log_sensitivity(
        [2.0, 2.0, 2.0],
        kernel,
        log_step=1.0e-5,
        depth_quadrature_order=128,
    )
    tighter = composite_instrument_log_sensitivity(
        [2.0, 2.0, 2.0],
        kernel,
        log_step=5.0e-6,
        depth_quadrature_order=128,
    )
    assert sensitivity == pytest.approx(
        [
            -0.483396366392163,
            -0.483396366392163,
            -0.274905438590433,
            -0.274905438590433,
            0.408999755963757,
            -0.06542850963287,
        ],
        rel=3.0e-9,
        abs=3.0e-10,
    )
    assert tighter == pytest.approx(sensitivity, rel=3.0e-8, abs=3.0e-9)


def test_independent_calibration_uncertainty_propagation() -> None:
    kernel = CompositeInstrumentKernel(2.0, 2.0, 5.0, 5.0, 0.5, 10.0)
    log_standard_deviations = np.array([0.05, 0.05, 0.01, 0.01, 0.10, 0.05])
    result = propagate_composite_instrument_calibration(
        [2.0, 2.0, 2.0],
        kernel,
        np.diag(log_standard_deviations**2),
        log_step=1.0e-5,
        depth_quadrature_order=128,
    )
    assert result.parameter_names == CompositeInstrumentKernel.log_parameter_names
    assert result.log_variance_standard_deviation == pytest.approx(
        0.05354423535417187, rel=3.0e-8
    )
    assert result.first_order_relative_standard_deviation == pytest.approx(
        result.log_variance_standard_deviation
    )
    assert result.lognormal_relative_standard_deviation == pytest.approx(
        0.05358263591832234, rel=3.0e-8
    )


def test_correlated_calibration_covariance_is_used() -> None:
    kernel = CompositeInstrumentKernel(1.0, 1.0, 2.0, 2.0, 0.8, 6.0)
    standard_deviations = np.array([0.04, 0.04, 0.01, 0.01, 0.05, 0.03])
    covariance = np.diag(standard_deviations**2)
    covariance[0, 1] = covariance[1, 0] = 0.75 * standard_deviations[0] * standard_deviations[1]
    independent = propagate_composite_instrument_calibration(
        [1.2, 1.2, 0.7],
        kernel,
        np.diag(standard_deviations**2),
    )
    correlated = propagate_composite_instrument_calibration(
        [1.2, 1.2, 0.7],
        kernel,
        covariance,
    )
    assert correlated.log_variance_standard_deviation > independent.log_variance_standard_deviation


def test_outputs_are_immutable() -> None:
    kernel = CompositeInstrumentKernel(1.0, 2.0, 3.0, 4.0, 0.6, 7.0)
    result = composite_instrument_effective_variance(1.0, [1.0, 2.0, 3.0], kernel)
    propagated = propagate_composite_instrument_calibration(
        [1.0, 2.0, 3.0],
        kernel,
        np.eye(6) * 1.0e-4,
    )
    assert not result.correlation_lengths.flags.writeable
    assert not propagated.log_sensitivity.flags.writeable
    assert not propagated.parameter_log_covariance.flags.writeable


@pytest.mark.parametrize(
    "operation, message",
    [
        (
            lambda: CompositeInstrumentKernel(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            "psf_sigma_x",
        ),
        (
            lambda: CompositeInstrumentKernel(1.0, 1.0, 1.0, 1.0, 0.0, 1.0),
            "attenuation_coefficient",
        ),
        (
            lambda: CompositeInstrumentKernel(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "left"),
            "side",
        ),
        (
            lambda: gaussian_psf_rectangular_pixel_axis_ratio(0.0, 1.0, 1.0),
            "correlation_length",
        ),
        (
            lambda: composite_instrument_effective_variance(
                1.0,
                [1.0, 2.0],
                CompositeInstrumentKernel(1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            ),
            "shape",
        ),
        (
            lambda: propagate_composite_instrument_calibration(
                [1.0, 1.0, 1.0],
                CompositeInstrumentKernel(1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                np.eye(5),
            ),
            "shape",
        ),
        (
            lambda: propagate_composite_instrument_calibration(
                [1.0, 1.0, 1.0],
                CompositeInstrumentKernel(1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                -np.eye(6),
            ),
            "positive semidefinite",
        ),
        (
            lambda: composite_instrument_log_sensitivity(
                [1.0, 1.0, 1.0],
                CompositeInstrumentKernel(0.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            ),
            "positive",
        ),
    ],
)
def test_invalid_inputs(operation, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        operation()
