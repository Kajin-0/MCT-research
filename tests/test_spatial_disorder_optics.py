from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_optics import (
    LateralTransmissionObservation,
    gaussian_gap_averaged_log_transmission,
    lateral_gaussian_gap_transmission_observation,
)


def test_zero_disorder_reduces_to_local_beer_lambert_law() -> None:
    energy = np.array([0.08, 0.10, 0.12, 0.16])
    mean_gap = 0.10
    amplitude = 800.0
    exponent = 0.5
    thickness = 0.015
    expected_absorption = amplitude * np.maximum(energy - mean_gap, 0.0) ** exponent

    observation = lateral_gaussian_gap_transmission_observation(
        energy,
        mean_gap,
        0.0,
        thickness,
        exponent=exponent,
        amplitude_cm_inverse_ev_power=amplitude,
    )

    assert observation.mean_absorption_cm_inverse == pytest.approx(
        expected_absorption, rel=1.0e-14
    )
    assert observation.log_averaged_transmission == pytest.approx(
        -thickness * expected_absorption, rel=1.0e-14
    )
    assert observation.transmission_effective_absorption_cm_inverse == pytest.approx(
        expected_absorption, rel=1.0e-14
    )
    assert observation.jensen_gap_cm_inverse == pytest.approx(
        np.zeros_like(energy), abs=1.0e-14
    )


def test_zero_amplitude_is_fully_transparent() -> None:
    observation = lateral_gaussian_gap_transmission_observation(
        np.linspace(0.08, 0.14, 11),
        0.10,
        0.004,
        0.02,
        amplitude_cm_inverse_ev_power=0.0,
    )
    assert observation.mean_absorption_cm_inverse == pytest.approx(0.0)
    assert observation.log_averaged_transmission == pytest.approx(0.0)
    assert observation.averaged_transmission == pytest.approx(1.0)
    assert observation.transmission_effective_absorption_cm_inverse == pytest.approx(0.0)
    assert observation.relative_closure_error == pytest.approx(0.0)


def test_step_edge_at_mean_gap_matches_exact_mixture() -> None:
    amplitude = 120.0
    thickness = 0.035
    observation = lateral_gaussian_gap_transmission_observation(
        np.asarray([0.10]),
        mean_gap_ev=0.10,
        gap_sigma_ev=0.006,
        thickness_cm=thickness,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
    )
    expected_transmission = 0.5 * (1.0 + math.exp(-amplitude * thickness))
    expected_log_transmission = math.log(expected_transmission)

    assert observation.mean_absorption_cm_inverse[0] == pytest.approx(
        amplitude / 2.0, rel=1.0e-15
    )
    assert observation.averaged_transmission[0] == pytest.approx(
        expected_transmission, rel=1.0e-15
    )
    assert observation.log_averaged_transmission[0] == pytest.approx(
        expected_log_transmission, rel=1.0e-15
    )
    assert observation.transmission_effective_absorption_cm_inverse[0] == pytest.approx(
        -expected_log_transmission / thickness, rel=1.0e-15
    )


def test_jensen_inequality_holds_over_energy_grid() -> None:
    energy = np.linspace(0.075, 0.145, 181)
    thickness = 0.012
    observation = lateral_gaussian_gap_transmission_observation(
        energy,
        mean_gap_ev=0.105,
        gap_sigma_ev=0.006,
        thickness_cm=thickness,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1800.0,
        quadrature_order=256,
    )

    assert np.all(
        observation.transmission_effective_absorption_cm_inverse
        <= observation.mean_absorption_cm_inverse + 1.0e-8
    )
    assert np.all(observation.jensen_gap_cm_inverse >= 0.0)
    arithmetic_beer_lambert = np.exp(
        -thickness * observation.mean_absorption_cm_inverse
    )
    assert np.all(
        observation.averaged_transmission >= arithmetic_beer_lambert - 1.0e-12
    )
    assert np.max(observation.jensen_gap_cm_inverse) > 1.0


def test_thin_sample_effective_absorption_converges_to_mean() -> None:
    amplitude = 100.0
    thickness = 1.0e-8
    observation = lateral_gaussian_gap_transmission_observation(
        np.asarray([0.10]),
        0.10,
        0.005,
        thickness,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
    )
    assert observation.transmission_effective_absorption_cm_inverse[0] == pytest.approx(
        amplitude / 2.0, rel=3.0e-7
    )


def test_optically_thick_log_transmission_remains_authoritative() -> None:
    amplitude = 1000.0
    thickness = 100.0
    all_absorbing_log_transmission = gaussian_gap_averaged_log_transmission(
        np.asarray([0.30]),
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        thickness_cm=thickness,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
    )
    observation = lateral_gaussian_gap_transmission_observation(
        np.asarray([0.30]),
        0.10,
        0.005,
        thickness,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=amplitude,
    )

    assert all_absorbing_log_transmission[0] == pytest.approx(-100000.0)
    assert observation.log_averaged_transmission[0] == pytest.approx(-100000.0)
    assert observation.averaged_transmission[0] == 0.0
    assert observation.transmission_effective_absorption_cm_inverse[0] == pytest.approx(
        amplitude
    )


def test_closure_error_increases_with_thickness_for_declared_step_case() -> None:
    common = dict(
        photon_energy_ev=np.asarray([0.10]),
        mean_gap_ev=0.10,
        gap_sigma_ev=0.005,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=200.0,
    )
    thin = lateral_gaussian_gap_transmission_observation(
        thickness_cm=1.0e-4, **common
    )
    thick = lateral_gaussian_gap_transmission_observation(
        thickness_cm=0.05, **common
    )
    assert thick.relative_closure_error[0] > thin.relative_closure_error[0]
    assert thick.jensen_gap_cm_inverse[0] > thin.jensen_gap_cm_inverse[0]


def test_scalar_and_multidimensional_shapes_are_preserved() -> None:
    scalar = lateral_gaussian_gap_transmission_observation(
        0.11,
        0.10,
        0.004,
        0.01,
        amplitude_cm_inverse_ev_power=900.0,
    )
    matrix_energy = np.array([[0.09, 0.10], [0.11, 0.12]])
    matrix = lateral_gaussian_gap_transmission_observation(
        matrix_energy,
        0.10,
        0.004,
        0.01,
        amplitude_cm_inverse_ev_power=900.0,
    )

    assert scalar.mean_absorption_cm_inverse.shape == ()
    assert scalar.log_averaged_transmission.shape == ()
    assert matrix.mean_absorption_cm_inverse.shape == matrix_energy.shape
    assert matrix.log_averaged_transmission.shape == matrix_energy.shape
    assert matrix.relative_closure_error.shape == matrix_energy.shape


def test_square_root_quadrature_shows_consistent_algebraic_convergence() -> None:
    energy = np.linspace(0.08, 0.14, 31)
    common = dict(
        photon_energy_ev=energy,
        mean_gap_ev=0.105,
        gap_sigma_ev=0.005,
        thickness_cm=0.015,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1600.0,
    )
    coarse = lateral_gaussian_gap_transmission_observation(
        quadrature_order=64, **common
    )
    medium = lateral_gaussian_gap_transmission_observation(
        quadrature_order=128, **common
    )
    fine = lateral_gaussian_gap_transmission_observation(
        quadrature_order=256, **common
    )

    coarse_log_change = float(
        np.max(
            np.abs(
                coarse.log_averaged_transmission
                - medium.log_averaged_transmission
            )
        )
    )
    fine_log_change = float(
        np.max(
            np.abs(
                medium.log_averaged_transmission
                - fine.log_averaged_transmission
            )
        )
    )
    coarse_absorption_change = float(
        np.max(
            np.abs(
                coarse.mean_absorption_cm_inverse
                - medium.mean_absorption_cm_inverse
            )
        )
    )
    fine_absorption_change = float(
        np.max(
            np.abs(
                medium.mean_absorption_cm_inverse
                - fine.mean_absorption_cm_inverse
            )
        )
    )

    # The square-root threshold has an endpoint derivative singularity, so
    # Gauss--Legendre convergence is algebraic rather than spectral. Doubling
    # order must materially reduce the observed successive difference.
    assert fine_log_change < 0.35 * coarse_log_change
    assert fine_absorption_change < 0.35 * coarse_absorption_change
    assert fine_log_change < 2.1e-6


def test_observation_arrays_are_read_only() -> None:
    observation = lateral_gaussian_gap_transmission_observation(
        np.linspace(0.09, 0.12, 5),
        0.10,
        0.004,
        0.01,
    )
    assert isinstance(observation, LateralTransmissionObservation)
    for array in (
        observation.mean_absorption_cm_inverse,
        observation.log_averaged_transmission,
        observation.averaged_transmission,
        observation.transmission_effective_absorption_cm_inverse,
        observation.jensen_gap_cm_inverse,
        observation.relative_closure_error,
    ):
        assert array.flags.writeable is False


def test_invalid_energy_gap_and_material_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="photon_energy_ev"):
        gaussian_gap_averaged_log_transmission(
            [0.1, math.nan], 0.1, 0.01, 0.01
        )
    with pytest.raises(ValueError, match="mean_gap_ev"):
        gaussian_gap_averaged_log_transmission(0.1, math.inf, 0.01, 0.01)
    with pytest.raises(ValueError, match="gap_sigma_ev"):
        gaussian_gap_averaged_log_transmission(0.1, 0.1, -0.01, 0.01)
    with pytest.raises(ValueError, match="thickness_cm"):
        gaussian_gap_averaged_log_transmission(0.1, 0.1, 0.01, 0.0)
    with pytest.raises(ValueError, match="exponent"):
        gaussian_gap_averaged_log_transmission(
            0.1, 0.1, 0.01, 0.01, exponent=-0.5
        )
    with pytest.raises(ValueError, match="amplitude"):
        gaussian_gap_averaged_log_transmission(
            0.1,
            0.1,
            0.01,
            0.01,
            amplitude_cm_inverse_ev_power=-1.0,
        )


def test_invalid_quadrature_and_truncation_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="quadrature_order"):
        gaussian_gap_averaged_log_transmission(
            0.1, 0.1, 0.01, 0.01, quadrature_order=31
        )
    with pytest.raises(ValueError, match="quadrature_order"):
        gaussian_gap_averaged_log_transmission(
            0.1, 0.1, 0.01, 0.01, quadrature_order=True
        )
    with pytest.raises(ValueError, match="standard_deviation_limit"):
        gaussian_gap_averaged_log_transmission(
            0.1,
            0.1,
            0.01,
            0.01,
            standard_deviation_limit=0.0,
        )
