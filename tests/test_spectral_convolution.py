from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spectral_convolution import (
    fit_exponential_absorption_tail,
    gaussian_gap_convolved_power_absorption,
    herrmann_gap_sigma_ev,
    normalized_gaussian_gap_convolved_power_absorption,
)


def normal_cdf(value: np.ndarray) -> np.ndarray:
    return np.asarray(
        [0.5 * (1.0 + math.erf(float(item) / math.sqrt(2.0))) for item in value]
    )


def normal_density(value: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * value**2) / math.sqrt(2.0 * math.pi)


def test_herrmann_source_scale_conversion() -> None:
    assert herrmann_gap_sigma_ev(0.008) == pytest.approx(
        math.sqrt(2.0) * 0.008
    )
    assert herrmann_gap_sigma_ev(0.0) == 0.0
    with pytest.raises(ValueError, match="non-negative"):
        herrmann_gap_sigma_ev(-0.001)


def test_linear_power_edge_matches_closed_gaussian_moment() -> None:
    mean_gap = 0.100
    sigma_gap = 0.012
    energy = mean_gap + sigma_gap * np.asarray([-3.0, -1.0, 0.0, 1.0, 3.0])
    z = (energy - mean_gap) / sigma_gap
    expected = (energy - mean_gap) * normal_cdf(z) + sigma_gap * normal_density(z)

    calculated = gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=1.0,
        quadrature_order=512,
    )

    # The integrand has a moving kink at G=E, so deterministic Gaussian
    # quadrature converges algebraically rather than spectrally at the deepest
    # tail points.  This tolerance is verified against the exact closed form.
    np.testing.assert_allclose(calculated, expected, rtol=3.0e-4, atol=2.0e-9)


def test_quadratic_power_edge_matches_closed_gaussian_moment() -> None:
    mean_gap = 0.100
    sigma_gap = 0.012
    energy = mean_gap + sigma_gap * np.asarray([-3.0, -1.0, 0.0, 1.0, 3.0])
    delta = energy - mean_gap
    z = delta / sigma_gap
    expected = (
        (delta**2 + sigma_gap**2) * normal_cdf(z)
        + delta * sigma_gap * normal_density(z)
    )

    calculated = gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=2.0,
        quadrature_order=512,
    )

    np.testing.assert_allclose(calculated, expected, rtol=1.0e-4, atol=2.0e-10)


def test_square_root_spectrum_is_quadrature_converged_in_fit_region() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    energy = mean_gap + sigma_gap * np.linspace(-3.5, -0.5, 301)
    coarse = normalized_gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        quadrature_order=256,
    )
    fine = normalized_gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        quadrature_order=512,
    )

    np.testing.assert_allclose(coarse, fine, rtol=4.0e-3, atol=2.0e-3)


def test_deterministic_gap_limit() -> None:
    energy = np.asarray([0.09, 0.10, 0.11])
    square_root = gaussian_gap_convolved_power_absorption(
        energy,
        0.10,
        0.0,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=2.0,
    )
    np.testing.assert_allclose(square_root, [0.0, 0.0, 0.2])

    step = gaussian_gap_convolved_power_absorption(
        energy,
        0.10,
        0.0,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=3.0,
    )
    np.testing.assert_allclose(step, [0.0, 3.0, 3.0])


def test_normalization_at_mean_gap() -> None:
    mean_gap = 0.100
    sigma_gap = 0.010
    absorption = normalized_gaussian_gap_convolved_power_absorption(
        np.asarray([mean_gap - sigma_gap, mean_gap, mean_gap + sigma_gap]),
        mean_gap,
        sigma_gap,
        exponent=0.5,
        absorption_at_mean_gap_cm_inverse=1000.0,
        quadrature_order=512,
    )
    assert absorption[1] == pytest.approx(1000.0, rel=1.0e-12)
    assert absorption[0] < absorption[1] < absorption[2]


def test_herrmann_square_root_reproduction_gives_half_s_tail() -> None:
    source_s = 0.008
    sigma_gap = herrmann_gap_sigma_ev(source_s)
    mean_gap = 0.100
    energy = mean_gap + sigma_gap * np.linspace(-5.0, 1.0, 6001)
    absorption = normalized_gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        absorption_at_mean_gap_cm_inverse=1000.0,
        quadrature_order=512,
    )
    fit = fit_exponential_absorption_tail(
        energy,
        absorption,
        absorption_bounds_cm_inverse=(1.0, 100.0),
        maximum_energy_ev=mean_gap,
    )

    assert fit.tail_energy_ev / source_s == pytest.approx(0.505, rel=0.012)
    assert fit.r_squared > 0.995
    assert fit.point_count > 100


def test_fit_window_changes_inferred_tail_energy_despite_high_r_squared() -> None:
    source_s = 0.008
    sigma_gap = herrmann_gap_sigma_ev(source_s)
    mean_gap = 0.100
    energy = mean_gap + sigma_gap * np.linspace(-5.0, 1.0, 6001)
    absorption = normalized_gaussian_gap_convolved_power_absorption(
        energy,
        mean_gap,
        sigma_gap,
        exponent=0.5,
        absorption_at_mean_gap_cm_inverse=1000.0,
        quadrature_order=512,
    )
    source_window = fit_exponential_absorption_tail(
        energy,
        absorption,
        absorption_bounds_cm_inverse=(1.0, 100.0),
        maximum_energy_ev=mean_gap,
    )
    upper_window = fit_exponential_absorption_tail(
        energy,
        absorption,
        absorption_bounds_cm_inverse=(100.0, 500.0),
        maximum_energy_ev=mean_gap,
    )

    assert source_window.r_squared > 0.995
    assert upper_window.r_squared > 0.997
    assert upper_window.tail_energy_ev / source_window.tail_energy_ev > 1.55


def test_intrinsic_exponent_is_weakly_identified_by_source_tail_window() -> None:
    source_s = 0.008
    sigma_gap = herrmann_gap_sigma_ev(source_s)
    mean_gap = 0.100
    energy = mean_gap + sigma_gap * np.linspace(-5.0, 1.0, 6001)
    ratios: list[float] = []

    for exponent in (0.5, 1.0, 2.0):
        absorption = normalized_gaussian_gap_convolved_power_absorption(
            energy,
            mean_gap,
            sigma_gap,
            exponent=exponent,
            absorption_at_mean_gap_cm_inverse=1000.0,
            quadrature_order=512,
        )
        fit = fit_exponential_absorption_tail(
            energy,
            absorption,
            absorption_bounds_cm_inverse=(1.0, 100.0),
            maximum_energy_ev=mean_gap,
        )
        assert fit.r_squared > 0.995
        ratios.append(fit.tail_energy_ev / source_s)

    assert max(ratios) - min(ratios) < 0.025


def test_tail_fit_and_operator_input_validation() -> None:
    with pytest.raises(ValueError, match="gap_sigma_ev"):
        gaussian_gap_convolved_power_absorption([0.1], 0.1, -0.001)
    with pytest.raises(ValueError, match="exponent"):
        gaussian_gap_convolved_power_absorption([0.1], 0.1, 0.001, exponent=-0.5)
    with pytest.raises(ValueError, match="quadrature_order"):
        gaussian_gap_convolved_power_absorption(
            [0.1], 0.1, 0.001, quadrature_order=16
        )
    with pytest.raises(ValueError, match="strictly increasing"):
        fit_exponential_absorption_tail(
            [0.1, 0.1],
            [1.0, 10.0],
        )
    with pytest.raises(ValueError, match="too few points"):
        fit_exponential_absorption_tail(
            [0.09, 0.10, 0.11],
            [0.1, 1.0, 10.0],
        )
