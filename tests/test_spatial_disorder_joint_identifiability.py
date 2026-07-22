from __future__ import annotations

import numpy as np
import pytest

from mct_research.spatial_disorder_instrument import CompositeInstrumentKernel
from mct_research.spatial_disorder_joint_identifiability import (
    ObservationOperatorSpecification,
    evaluate_observation_operator,
    joint_identifiability_screen,
)


POINT_VARIANCE = 2.5e-5
LATERAL_XI = 2.0
DEPTH_XI = 2.0
KERNELS = (
    CompositeInstrumentKernel(0.2, 0.2, 0.4, 0.4, 0.5, 10.0),
    CompositeInstrumentKernel(1.0, 1.0, 2.0, 2.0, 0.5, 10.0),
    CompositeInstrumentKernel(4.0, 4.0, 8.0, 8.0, 0.5, 10.0),
)
INSTRUMENT_LOG_SD = np.array([0.05, 0.05, 0.01, 0.01, 0.10, 0.05])
INSTRUMENT_COVARIANCE = np.diag(INSTRUMENT_LOG_SD**2)
OBSERVATION_LOG_SD = np.array([0.03, 0.03, 0.03])


def _screen(
    specification: ObservationOperatorSpecification | None = None,
):
    return joint_identifiability_screen(
        point_variance=POINT_VARIANCE,
        lateral_correlation_length=LATERAL_XI,
        depth_correlation_length=DEPTH_XI,
        kernels=KERNELS,
        instrument_parameter_log_covariance=INSTRUMENT_COVARIANCE,
        observation_log_standard_deviations=OBSERVATION_LOG_SD,
        observation_specification=specification,
        threshold_distance=3.0,
        depth_quadrature_order=128,
    )


def test_gaussian_truth_is_self_consistent_under_both_fit_conventions() -> None:
    screen = _screen()
    gaussian = [item for item in screen.results if item.true_family == "gaussian"]
    assert {item.fitting_convention for item in gaussian} == {
        "log_variance",
        "reciprocal_variance",
    }
    for item in gaussian:
        assert item.fitted_variances == pytest.approx(
            item.true_variances,
            rel=5.0e-12,
            abs=1.0e-18,
        )
        assert item.full_envelope.distance < 1.0e-8
        assert item.decision == "observation_limited"


def test_uncertainty_stages_cannot_increase_mahalanobis_separation() -> None:
    screen = _screen()
    for item in screen.results:
        stages = [
            item.observation_only.distance,
            item.calibration_added.distance,
            item.kernel_shape_added.distance,
            item.full_envelope.distance,
        ]
        assert stages == sorted(stages, reverse=True)


def test_shared_instrument_calibration_creates_cross_scale_covariance() -> None:
    screen = _screen()
    covariance = screen.instrument_log_variance_covariance
    assert covariance.shape == (3, 3)
    assert np.all(np.diag(covariance) > 0.0)
    assert np.max(np.abs(covariance - np.diag(np.diag(covariance)))) > 1.0e-5
    assert np.linalg.eigvalsh(covariance).min() >= -1.0e-14


def test_kernel_shape_systematic_is_scale_dependent() -> None:
    screen = _screen()
    shifts = screen.kernel_shape_log_shifts
    assert shifts.shape == (3,)
    assert np.all(shifts < 0.0)
    assert abs(shifts[-1]) > abs(shifts[0])
    assert np.max(np.abs(shifts)) > 0.008


def test_rougher_matern_family_is_more_separable_in_direct_variance_space() -> None:
    screen = _screen()
    for convention in ("log_variance", "reciprocal_variance"):
        by_family = {
            item.true_family: item.full_envelope.distance
            for item in screen.results
            if item.fitting_convention == convention
        }
        assert (
            by_family["matern_0.5"]
            > by_family["matern_1.5"]
            > by_family["matern_2.5"]
            > 0.0
        )


def test_fit_conventions_produce_distinct_misspecified_parameters() -> None:
    screen = _screen()
    exponential = [
        item for item in screen.results if item.true_family == "matern_0.5"
    ]
    assert len(exponential) == 2
    assert exponential[0].fitted_point_variance != pytest.approx(
        exponential[1].fitted_point_variance,
        rel=1.0e-4,
    )
    assert exponential[0].fitted_correlation_length != pytest.approx(
        exponential[1].fitted_correlation_length,
        rel=1.0e-4,
    )


def test_direct_variance_and_gap_standard_deviation_have_exact_sensitivities() -> None:
    variances = np.array([1.0e-6, 4.0e-6, 9.0e-6])
    direct = evaluate_observation_operator(
        variances,
        ObservationOperatorSpecification(kind="log_variance"),
    )
    gap = evaluate_observation_operator(
        variances,
        ObservationOperatorSpecification(
            kind="log_gap_standard_deviation",
            gap_slope_ev_per_fraction=1.2,
        ),
    )
    assert direct.log_variance_sensitivities == pytest.approx(np.ones(3))
    assert gap.log_variance_sensitivities == pytest.approx(np.full(3, 0.5))
    assert direct.closure_log_shifts == pytest.approx(np.zeros(3))
    assert gap.closure_log_shifts == pytest.approx(np.zeros(3))


def test_transmission_operator_obeys_jensen_shift_sign() -> None:
    specification = ObservationOperatorSpecification(
        kind="log_transmission_effective_absorption",
        gap_slope_ev_per_fraction=1.2,
        mean_gap_ev=0.10,
        optical_thickness_cm=0.012,
        photon_energy_ev=0.115,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1800.0,
        quadrature_order=128,
    )
    evaluation = evaluate_observation_operator(
        np.array([1.0e-5, 2.0e-5, 3.0e-5]),
        specification,
    )
    assert np.all(np.isfinite(evaluation.log_observables))
    assert np.all(evaluation.log_variance_sensitivities < 0.0)
    assert np.all(evaluation.closure_log_shifts >= 0.0)
    assert np.max(evaluation.closure_log_shifts) > 1.0e-4


def test_cutoff_operator_obeys_energy_ordering_shift_sign() -> None:
    specification = ObservationOperatorSpecification(
        kind="log_cutoff_energy",
        gap_slope_ev_per_fraction=1.2,
        mean_gap_ev=0.10,
        optical_thickness_cm=0.015,
        target_response=0.35,
        lower_energy_ev=0.07,
        upper_energy_ev=0.14,
        exponent=0.0,
        amplitude_cm_inverse_ev_power=300.0,
        quadrature_order=128,
        absolute_tolerance_ev=1.0e-10,
    )
    evaluation = evaluate_observation_operator(
        np.array([1.0e-5, 2.0e-5, 3.0e-5]),
        specification,
    )
    assert np.all(np.isfinite(evaluation.log_observables))
    assert np.all(evaluation.closure_log_shifts <= 0.0)
    assert np.min(evaluation.closure_log_shifts) < -1.0e-4


def test_nonlinear_transmission_screen_adds_operator_uncertainty() -> None:
    specification = ObservationOperatorSpecification(
        kind="log_transmission_effective_absorption",
        gap_slope_ev_per_fraction=1.2,
        mean_gap_ev=0.10,
        optical_thickness_cm=0.012,
        photon_energy_ev=0.115,
        exponent=0.5,
        amplitude_cm_inverse_ev_power=1800.0,
        quadrature_order=96,
    )
    screen = _screen(specification)
    assert any(
        item.full_envelope.distance < item.kernel_shape_added.distance
        for item in screen.results
        if item.true_family != "gaussian"
    )


def test_length_unit_invariance_of_variance_space_screen() -> None:
    base = _screen()
    scale = 1.0e-6
    rescaled_kernels = tuple(
        CompositeInstrumentKernel(
            item.psf_sigma_x * scale,
            item.psf_sigma_y * scale,
            item.pixel_width_x * scale,
            item.pixel_width_y * scale,
            item.attenuation_coefficient / scale,
            item.thickness * scale,
            item.side,
        )
        for item in KERNELS
    )
    rescaled = joint_identifiability_screen(
        point_variance=POINT_VARIANCE,
        lateral_correlation_length=LATERAL_XI * scale,
        depth_correlation_length=DEPTH_XI * scale,
        kernels=rescaled_kernels,
        instrument_parameter_log_covariance=INSTRUMENT_COVARIANCE,
        observation_log_standard_deviations=OBSERVATION_LOG_SD,
        threshold_distance=3.0,
        depth_quadrature_order=128,
    )
    assert rescaled.kernel_shape_log_shifts == pytest.approx(
        base.kernel_shape_log_shifts,
        rel=5.0e-11,
        abs=5.0e-13,
    )
    for first, second in zip(base.results, rescaled.results, strict=True):
        assert second.full_envelope.distance == pytest.approx(
            first.full_envelope.distance,
            rel=5.0e-10,
            abs=5.0e-12,
        )


def test_input_kernel_order_is_normalized_by_equivalent_scale() -> None:
    base = _screen()
    permutation = [2, 0, 1]
    permuted = joint_identifiability_screen(
        point_variance=POINT_VARIANCE,
        lateral_correlation_length=LATERAL_XI,
        depth_correlation_length=DEPTH_XI,
        kernels=tuple(KERNELS[index] for index in permutation),
        instrument_parameter_log_covariance=INSTRUMENT_COVARIANCE,
        observation_log_standard_deviations=OBSERVATION_LOG_SD[permutation],
        depth_quadrature_order=128,
    )
    assert permuted.equivalent_probe_sigmas == pytest.approx(
        base.equivalent_probe_sigmas
    )
    for first, second in zip(base.results, permuted.results, strict=True):
        assert second.full_envelope.distance == pytest.approx(
            first.full_envelope.distance,
            rel=3.0e-12,
        )


def test_outputs_are_immutable() -> None:
    screen = _screen()
    arrays = [
        screen.equivalent_probe_sigmas,
        screen.depth_ratios,
        screen.exact_gaussian_variances,
        screen.reduced_gaussian_variances,
        screen.kernel_shape_log_shifts,
        screen.instrument_log_sensitivity,
        screen.instrument_log_variance_covariance,
        screen.observation_log_standard_deviations,
    ]
    for result in screen.results:
        arrays.extend(
            [
                result.true_variances,
                result.fitted_variances,
                result.true_log_observables,
                result.fitted_log_observables,
                result.log_observable_residuals,
                result.full_envelope.covariance,
            ]
        )
    assert all(not array.flags.writeable for array in arrays)


@pytest.mark.parametrize(
    "operation, message",
    [
        (
            lambda: joint_identifiability_screen(
                point_variance=POINT_VARIANCE,
                lateral_correlation_length=LATERAL_XI,
                depth_correlation_length=DEPTH_XI,
                kernels=KERNELS[:2],
                instrument_parameter_log_covariance=INSTRUMENT_COVARIANCE,
                observation_log_standard_deviations=OBSERVATION_LOG_SD[:2],
            ),
            "at least three",
        ),
        (
            lambda: joint_identifiability_screen(
                point_variance=POINT_VARIANCE,
                lateral_correlation_length=LATERAL_XI,
                depth_correlation_length=DEPTH_XI,
                kernels=(
                    CompositeInstrumentKernel(1.0, 2.0, 2.0, 2.0, 0.5, 10.0),
                    KERNELS[1],
                    KERNELS[2],
                ),
                instrument_parameter_log_covariance=INSTRUMENT_COVARIANCE,
                observation_log_standard_deviations=OBSERVATION_LOG_SD,
            ),
            "isotropic",
        ),
        (
            lambda: joint_identifiability_screen(
                point_variance=POINT_VARIANCE,
                lateral_correlation_length=LATERAL_XI,
                depth_correlation_length=DEPTH_XI,
                kernels=KERNELS,
                instrument_parameter_log_covariance=np.eye(5),
                observation_log_standard_deviations=OBSERVATION_LOG_SD,
            ),
            "shape",
        ),
        (
            lambda: evaluate_observation_operator(
                [1.0, -1.0],
                ObservationOperatorSpecification(),
            ),
            "positive",
        ),
    ],
)
def test_invalid_inputs_are_rejected(operation, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        operation()
