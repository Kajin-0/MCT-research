from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.tail_curvature import (
    GaussianPowerTailAsymptotic,
    GaussianPowerTailDiagnostics,
    gaussian_power_deep_tail_asymptotic,
    gaussian_power_tail_diagnostics,
)


def normal_cdf(value: np.ndarray) -> np.ndarray:
    return np.asarray(
        [0.5 * (1.0 + math.erf(float(item) / math.sqrt(2.0))) for item in value]
    )


def normal_density(value: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * value**2) / math.sqrt(2.0 * math.pi)


def test_public_types_and_functions() -> None:
    assert GaussianPowerTailDiagnostics.__name__ == "GaussianPowerTailDiagnostics"
    assert GaussianPowerTailAsymptotic.__name__ == "GaussianPowerTailAsymptotic"
    assert callable(gaussian_power_tail_diagnostics)
    assert callable(gaussian_power_deep_tail_asymptotic)


def test_step_edge_matches_closed_gaussian_cdf_derivatives() -> None:
    mean_gap = 0.100
    sigma_gap = 0.012
    amplitude = 2.5
    z = np.asarray([-4.0, -2.0, -1.0, 0.0])
    energy = mean_gap + sigma_gap * z
    cdf = normal_cdf(z)
    density = normal_density(z)
    inverse_mills = density / cdf

    result = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
        quadrature_order=512,
    )

    np.testing.assert_allclose(result.absorption_cm_inverse, amplitude * cdf, rtol=2e-10)
    np.testing.assert_allclose(
        result.dimensionless_log_slope,
        inverse_mills,
        rtol=2e-9,
    )
    np.testing.assert_allclose(
        result.dimensionless_log_curvature,
        -z * inverse_mills - inverse_mills**2,
        rtol=2e-8,
        atol=2e-10,
    )


def test_linear_edge_matches_closed_gaussian_moment_derivatives() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    z = np.asarray([-4.0, -2.0, -1.0, 0.0])
    energy = mean_gap + sigma_gap * z
    cdf = normal_cdf(z)
    density = normal_density(z)
    moment = z * cdf + density
    first = cdf
    second = density

    result = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=1.0,
        quadrature_order=512,
    )

    np.testing.assert_allclose(
        result.absorption_cm_inverse,
        sigma_gap * moment,
        rtol=2e-9,
        atol=1e-18,
    )
    np.testing.assert_allclose(
        result.dimensionless_log_slope,
        first / moment,
        rtol=2e-8,
    )
    np.testing.assert_allclose(
        result.dimensionless_log_curvature,
        second / moment - (first / moment) ** 2,
        rtol=3e-7,
        atol=2e-9,
    )


def test_quadratic_edge_matches_closed_gaussian_moment_derivatives() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    z = np.asarray([-4.0, -2.0, -1.0, 0.0])
    energy = mean_gap + sigma_gap * z
    cdf = normal_cdf(z)
    density = normal_density(z)
    moment_1 = z * cdf + density
    moment_2 = (z**2 + 1.0) * cdf + z * density
    first = 2.0 * moment_1
    second = 2.0 * cdf

    result = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=2.0,
        quadrature_order=512,
    )

    np.testing.assert_allclose(
        result.absorption_cm_inverse,
        sigma_gap**2 * moment_2,
        rtol=3e-8,
        atol=1e-20,
    )
    np.testing.assert_allclose(
        result.dimensionless_log_slope,
        first / moment_2,
        rtol=3e-7,
    )
    np.testing.assert_allclose(
        result.dimensionless_log_curvature,
        second / moment_2 - (first / moment_2) ** 2,
        rtol=2e-6,
        atol=2e-8,
    )


def test_herrmann_square_root_differential_diagnostics_converge() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    z = np.linspace(-6.0, 0.0, 61)
    energy = mean_gap + sigma_gap * z

    coarse = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        quadrature_order=256,
    )
    fine = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        quadrature_order=512,
    )

    np.testing.assert_allclose(
        coarse.dimensionless_log_slope,
        fine.dimensionless_log_slope,
        rtol=2e-6,
    )
    np.testing.assert_allclose(
        coarse.dimensionless_log_curvature,
        fine.dimensionless_log_curvature,
        rtol=2e-5,
        atol=2e-7,
    )


def test_log_tail_is_concave_and_local_tail_energy_is_monotone() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    energy = mean_gap + sigma_gap * np.linspace(-6.0, 0.0, 121)

    result = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        quadrature_order=512,
    )

    assert np.max(result.dimensionless_log_curvature) < -0.5
    assert np.all(np.diff(result.dimensionless_log_slope) < 0.0)
    assert np.all(np.diff(result.dimensionless_local_tail_energy) > 0.0)
    assert not result.local_tail_energy_ev.flags.writeable


def test_deep_tail_approaches_gaussian_curvature_not_exponential_curvature() -> None:
    z = np.asarray([-8.0])
    exact = gaussian_power_tail_diagnostics(
        z,
        0.0,
        1.0,
        exponent=0.5,
        quadrature_order=512,
    )
    asymptotic = gaussian_power_deep_tail_asymptotic(z, exponent=0.5)

    assert exact.dimensionless_log_curvature[0] == pytest.approx(-1.0, abs=0.025)
    assert exact.dimensionless_log_curvature[0] != pytest.approx(0.0, abs=0.1)
    assert exact.dimensionless_log_slope[0] == pytest.approx(
        asymptotic.dimensionless_log_slope[0], rel=1.0e-3
    )
    assert exact.dimensionless_log_curvature[0] == pytest.approx(
        asymptotic.dimensionless_log_curvature[0], abs=3.0e-3
    )
    assert exact.absorption_cm_inverse[0] == pytest.approx(
        asymptotic.dimensionless_absorption_shape[0], rel=0.03
    )


def test_consistent_energy_rescaling_preserves_dimensionless_diagnostics() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    exponent = 0.5
    amplitude = 3.0
    z = np.linspace(-5.0, 0.0, 31)
    energy = mean_gap + sigma_gap * z

    base = gaussian_power_tail_diagnostics(
        energy,
        mean_gap,
        sigma_gap,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude,
        quadrature_order=512,
    )

    scale = 1000.0
    rescaled = gaussian_power_tail_diagnostics(
        energy * scale,
        mean_gap * scale,
        sigma_gap * scale,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude / scale**exponent,
        quadrature_order=512,
    )

    np.testing.assert_allclose(
        rescaled.absorption_cm_inverse,
        base.absorption_cm_inverse,
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        rescaled.dimensionless_log_slope,
        base.dimensionless_log_slope,
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        rescaled.dimensionless_log_curvature,
        base.dimensionless_log_curvature,
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        rescaled.log_slope_ev_inverse,
        base.log_slope_ev_inverse / scale,
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        rescaled.local_tail_energy_ev,
        base.local_tail_energy_ev * scale,
        rtol=1e-12,
    )
    np.testing.assert_allclose(
        rescaled.log_curvature_ev_inverse_squared,
        base.log_curvature_ev_inverse_squared / scale**2,
        rtol=1e-12,
    )


def test_input_validation() -> None:
    with pytest.raises(ValueError, match="gap_sigma_ev"):
        gaussian_power_tail_diagnostics([-0.1], 0.0, 0.0)
    with pytest.raises(ValueError, match="exponent"):
        gaussian_power_tail_diagnostics([-0.1], 0.0, 1.0, exponent=-0.5)
    with pytest.raises(ValueError, match="<= mean_gap_ev"):
        gaussian_power_tail_diagnostics([0.1], 0.0, 1.0)
    with pytest.raises(ValueError, match="standard_deviation_limit"):
        gaussian_power_tail_diagnostics([-10.0], 0.0, 1.0)
    with pytest.raises(ValueError, match="< 0"):
        gaussian_power_deep_tail_asymptotic([0.0])
