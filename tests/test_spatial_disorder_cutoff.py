from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_cutoff import (
    LateralCutoffComparison,
    LateralResponseCurves,
    lateral_gaussian_gap_response_curves,
    lateral_gaussian_gap_response_cutoff,
)


def test_response_curves_obey_jensen_ordering_over_energy_grid() -> None:
    energy = np.linspace(0.075, 0.145, 141)
    curves = lateral_gaussian_gap_response_curves(
        energy,
        mean_gap_ev=0.105,
        gap_sigma_ev=0.006,
        thickness_cm=0.012,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1800.0,
        quadrature_order=256,
    )

    assert isinstance(curves, LateralResponseCurves)
    assert np.all(
        curves.transmission_averaged_response
        <= curves.mean_absorption_closure_response + 1.0e-12
    )
    assert np.all(curves.closure_response_excess >= 0.0)
    assert np.max(curves.closure_response_excess) > 1.0e-3


def test_zero_disorder_response_curves_and_cutoffs_are_identical() -> None:
    energy = np.linspace(0.09, 0.14, 51)
    curves = lateral_gaussian_gap_response_curves(
        energy,
        mean_gap_ev=0.10,
        gap_sigma_ev=0.0,
        thickness_cm=0.01,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1000.0,
    )
    assert curves.transmission_averaged_response == pytest.approx(
        curves.mean_absorption_closure_response,
        rel=1.0e-14,
        abs=1.0e-14,
    )

    cutoff = lateral_gaussian_gap_response_cutoff(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.0,
        thickness_cm=0.01,
        lower_energy_ev=0.10,
        upper_energy_ev=0.13,
        target_response=0.5,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1000.0,
        absolute_tolerance_ev=1.0e-12,
    )
    assert cutoff.transmission_averaged_energy_ev == pytest.approx(
        cutoff.mean_absorption_closure_energy_ev,
        abs=2.0e-12,
    )
    assert cutoff.energy_shift_ev == pytest.approx(0.0, abs=2.0e-12)
    assert cutoff.wavelength_shift_um == pytest.approx(0.0, abs=1.0e-8)


def test_exact_step_edge_target_returns_true_cutoff_at_mean_gap() -> None:
    mean_gap = 0.10
    sigma_gap = 0.005
    amplitude = 200.0
    thickness = 0.02
    target = 0.5 * (1.0 - math.exp(-amplitude * thickness))

    cutoff = lateral_gaussian_gap_response_cutoff(
        mean_gap_ev=mean_gap,
        gap_sigma_ev=sigma_gap,
        thickness_cm=thickness,
        lower_energy_ev=0.08,
        upper_energy_ev=0.12,
        target_response=target,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
        absolute_tolerance_ev=1.0e-12,
        response_tolerance=1.0e-14,
    )

    assert isinstance(cutoff, LateralCutoffComparison)
    assert cutoff.transmission_averaged_energy_ev == pytest.approx(
        mean_gap,
        abs=1.0e-15,
    )
    assert cutoff.mean_absorption_closure_energy_ev < mean_gap
    assert cutoff.energy_shift_ev > 0.0
    assert cutoff.wavelength_shift_um < 0.0
    assert cutoff.transmission_iterations == 1


def test_cutoff_energy_and_wavelength_ordering() -> None:
    cutoff = lateral_gaussian_gap_response_cutoff(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.006,
        thickness_cm=0.015,
        lower_energy_ev=0.07,
        upper_energy_ev=0.14,
        target_response=0.35,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=300.0,
        absolute_tolerance_ev=1.0e-11,
    )
    assert (
        cutoff.transmission_averaged_energy_ev
        >= cutoff.mean_absorption_closure_energy_ev
    )
    assert (
        cutoff.transmission_averaged_wavelength_um
        <= cutoff.mean_absorption_closure_wavelength_um
    )
    assert cutoff.energy_shift_ev >= 0.0
    assert cutoff.wavelength_shift_um <= 0.0


def test_thin_sample_cutoff_shift_converges_toward_zero() -> None:
    common = dict(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        lower_energy_ev=0.06,
        upper_energy_ev=0.14,
        target_response=0.02,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=1000.0,
        absolute_tolerance_ev=1.0e-11,
    )
    thinner = lateral_gaussian_gap_response_cutoff(
        thickness_cm=5.0e-5,
        **common,
    )
    thin = lateral_gaussian_gap_response_cutoff(
        thickness_cm=1.0e-4,
        **common,
    )
    thick = lateral_gaussian_gap_response_cutoff(
        thickness_cm=1.0e-2,
        **common,
    )

    assert thinner.energy_shift_ev < thin.energy_shift_ev < thick.energy_shift_ev
    assert (
        abs(thinner.wavelength_shift_um)
        < abs(thin.wavelength_shift_um)
        < abs(thick.wavelength_shift_um)
    )


def test_bisection_reports_residuals_and_tolerance_metadata() -> None:
    cutoff = lateral_gaussian_gap_response_cutoff(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.004,
        thickness_cm=0.01,
        lower_energy_ev=0.07,
        upper_energy_ev=0.14,
        target_response=0.25,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=250.0,
        absolute_tolerance_ev=1.0e-12,
        response_tolerance=1.0e-12,
        max_iterations=128,
    )

    assert abs(cutoff.transmission_response_residual) <= 2.0e-10
    assert abs(cutoff.mean_absorption_response_residual) <= 2.0e-10
    assert cutoff.transmission_iterations <= 128
    assert cutoff.mean_absorption_iterations <= 128
    assert cutoff.lower_energy_ev == 0.07
    assert cutoff.upper_energy_ev == 0.14
    assert cutoff.absolute_tolerance_ev == 1.0e-12
    assert cutoff.response_tolerance == 1.0e-12


def test_response_curve_shapes_and_read_only_outputs() -> None:
    scalar = lateral_gaussian_gap_response_curves(
        0.10,
        0.10,
        0.005,
        0.01,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=100.0,
    )
    energy = np.array([[0.09, 0.10], [0.11, 0.12]])
    matrix = lateral_gaussian_gap_response_curves(
        energy,
        0.10,
        0.005,
        0.01,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=100.0,
    )

    assert scalar.transmission_averaged_response.shape == ()
    assert matrix.transmission_averaged_response.shape == energy.shape
    for array in (
        matrix.transmission_averaged_response,
        matrix.mean_absorption_closure_response,
        matrix.closure_response_excess,
    ):
        assert array.flags.writeable is False


def test_target_must_be_bracketed_by_both_response_curves() -> None:
    common = dict(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        thickness_cm=0.01,
        target_response=0.20,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=100.0,
    )
    with pytest.raises(ValueError, match="lower bracket"):
        lateral_gaussian_gap_response_cutoff(
            lower_energy_ev=0.11,
            upper_energy_ev=0.14,
            **common,
        )
    with pytest.raises(ValueError, match="upper bracket"):
        lateral_gaussian_gap_response_cutoff(
            lower_energy_ev=0.06,
            upper_energy_ev=0.09,
            **common,
        )


def test_invalid_target_bracket_and_solver_controls_are_rejected() -> None:
    base = dict(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        thickness_cm=0.01,
        lower_energy_ev=0.07,
        upper_energy_ev=0.14,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=100.0,
    )
    with pytest.raises(ValueError, match="target_response"):
        lateral_gaussian_gap_response_cutoff(target_response=1.0, **base)
    with pytest.raises(ValueError, match="lower_energy_ev"):
        lateral_gaussian_gap_response_cutoff(
            target_response=0.2,
            **{**base, "lower_energy_ev": 0.0},
        )
    with pytest.raises(ValueError, match="upper_energy_ev"):
        lateral_gaussian_gap_response_cutoff(
            target_response=0.2,
            **{**base, "upper_energy_ev": 0.06},
        )
    with pytest.raises(ValueError, match="absolute_tolerance_ev"):
        lateral_gaussian_gap_response_cutoff(
            target_response=0.2,
            **{**base, "absolute_tolerance_ev": 0.1},
        )
    with pytest.raises(ValueError, match="response_tolerance"):
        lateral_gaussian_gap_response_cutoff(
            target_response=0.2,
            **{**base, "response_tolerance": 1.0},
        )
    with pytest.raises(ValueError, match="max_iterations"):
        lateral_gaussian_gap_response_cutoff(
            target_response=0.2,
            **{**base, "max_iterations": True},
        )


def test_invalid_local_model_and_quadrature_inputs_propagate() -> None:
    common = dict(
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        thickness_cm=0.01,
        lower_energy_ev=0.07,
        upper_energy_ev=0.14,
        target_response=0.2,
    )
    with pytest.raises(ValueError, match="gap_sigma_ev"):
        lateral_gaussian_gap_response_cutoff(
            **{**common, "gap_sigma_ev": -0.005}
        )
    with pytest.raises(ValueError, match="exponent"):
        lateral_gaussian_gap_response_cutoff(
            **common,
            exponent=-0.5,
        )
    with pytest.raises(ValueError, match="amplitude"):
        lateral_gaussian_gap_response_cutoff(
            **common,
            amplitude_cm_inverse_ev_power=-1.0,
        )
    with pytest.raises(ValueError, match="quadrature_order"):
        lateral_gaussian_gap_response_cutoff(
            **common,
            quadrature_order=16,
        )
