from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_calibration import (
    common_log_scale_basis,
    common_probe_scale_calibration_information,
    gaussian_probe_scale_calibration_information,
    independent_log_scale_basis,
    independent_probe_scale_calibration_information,
)
from mct_research.spatial_disorder_inference import gaussian_multiscale_variance


def test_common_scale_covariance_identity_is_exact() -> None:
    tau = 0.08
    diagnostics = common_probe_scale_calibration_information(
        0.03,
        1.4,
        [0.2, 0.7, 2.0, 6.0],
        calibration_log_standard_deviation=tau,
        relative_standard_deviation=0.04,
    )
    base_covariance = np.asarray(diagnostics.base_diagnostics.parameter_covariance)
    calibrated_covariance = np.asarray(diagnostics.parameter_covariance)
    expected = base_covariance + np.array([[0.0, 0.0], [0.0, tau**2]])

    assert diagnostics.rank == 2
    assert calibrated_covariance == pytest.approx(expected, rel=3.0e-12, abs=2.0e-15)
    assert calibrated_covariance[0, 0] == pytest.approx(
        base_covariance[0, 0], rel=3.0e-12
    )
    assert calibrated_covariance[0, 1] == pytest.approx(
        base_covariance[0, 1], rel=3.0e-12
    )
    assert diagnostics.standard_deviation_inflation[0] == pytest.approx(1.0)
    assert diagnostics.standard_deviation_inflation[1] > 1.0


def test_uncalibrated_common_scale_makes_log_xi_unidentifiable() -> None:
    diagnostics = common_probe_scale_calibration_information(
        0.03,
        1.4,
        [0.2, 0.7, 2.0, 6.0],
        calibration_log_standard_deviation=None,
        relative_standard_deviation=0.04,
    )

    assert diagnostics.rank == 1
    assert math.isinf(diagnostics.condition_number)
    assert diagnostics.parameter_covariance is None
    assert diagnostics.standard_deviation_inflation is None
    assert diagnostics.null_direction == pytest.approx([0.0, 1.0], abs=2.0e-14)
    assert diagnostics.marginalized_fisher_matrix[0, 1] == pytest.approx(
        0.0, abs=2.0e-12
    )
    assert diagnostics.marginalized_fisher_matrix[1, 1] == pytest.approx(
        0.0, abs=2.0e-12
    )


def test_nuisance_jacobian_matches_stable_finite_differences() -> None:
    point_variance = 0.021
    correlation_length = 1.7
    scales = np.array([0.15, 0.45, 1.2, 3.5, 8.0])
    centered_log_scale = np.log(scales) - np.mean(np.log(scales))
    basis = np.column_stack((np.ones(scales.size), centered_log_scale))
    diagnostics = gaussian_probe_scale_calibration_information(
        point_variance,
        correlation_length,
        scales,
        basis,
        relative_standard_deviation=0.05,
        calibration_prior_standard_deviations=[0.03, 0.02],
    )

    step = 1.0e-5
    numerical_columns = []
    for column in range(basis.shape[1]):
        offset = step * basis[:, column]
        plus = gaussian_multiscale_variance(
            point_variance,
            correlation_length,
            scales * np.exp(offset),
        )
        minus = gaussian_multiscale_variance(
            point_variance,
            correlation_length,
            scales * np.exp(-offset),
        )
        numerical_columns.append((plus - minus) / (2.0 * step))
    numerical = np.column_stack(numerical_columns)

    assert diagnostics.nuisance_jacobian == pytest.approx(
        numerical, rel=2.0e-9, abs=2.0e-14
    )
    assert diagnostics.probe_log_jacobian == pytest.approx(
        -diagnostics.base_diagnostics.jacobian[:, 1], rel=1.0e-15
    )


def test_schur_complement_matches_direct_joint_inverse() -> None:
    scales = np.array([0.25, 0.6, 1.4, 3.2, 7.0])
    basis = np.column_stack(
        (
            np.ones(scales.size),
            np.linspace(-1.0, 1.0, scales.size),
        )
    )
    prior_covariance = np.array([[0.04**2, 0.25 * 0.04 * 0.02],
                                 [0.25 * 0.04 * 0.02, 0.02**2]])
    diagnostics = gaussian_probe_scale_calibration_information(
        0.04,
        1.6,
        scales,
        basis,
        relative_standard_deviation=0.03,
        calibration_prior_covariance=prior_covariance,
        calibration_mode="common_plus_tilt",
    )

    joint_inverse = np.linalg.inv(np.asarray(diagnostics.joint_fisher_matrix))
    direct_physical_covariance = joint_inverse[:2, :2]

    assert diagnostics.rank == 2
    assert diagnostics.parameter_covariance == pytest.approx(
        direct_physical_covariance, rel=2.0e-11, abs=2.0e-14
    )
    assert np.linalg.inv(np.asarray(diagnostics.marginalized_fisher_matrix)) == pytest.approx(
        direct_physical_covariance, rel=2.0e-11, abs=2.0e-14
    )
    assert diagnostics.calibration_mode == "common_plus_tilt"


def test_prior_precision_interface_matches_covariance_interface() -> None:
    scales = [0.2, 0.8, 2.5, 7.0]
    basis = np.column_stack((np.ones(4), [-1.0, -0.3, 0.4, 1.0]))
    covariance = np.array([[0.05**2, 0.0003], [0.0003, 0.03**2]])
    precision = np.linalg.inv(covariance)

    by_covariance = gaussian_probe_scale_calibration_information(
        0.02,
        1.2,
        scales,
        basis,
        relative_standard_deviation=0.04,
        calibration_prior_covariance=covariance,
    )
    by_precision = gaussian_probe_scale_calibration_information(
        0.02,
        1.2,
        scales,
        basis,
        relative_standard_deviation=0.04,
        calibration_prior_precision=precision,
    )

    assert by_covariance.nuisance_prior_precision == pytest.approx(
        by_precision.nuisance_prior_precision, rel=2.0e-14
    )
    assert by_covariance.marginalized_fisher_matrix == pytest.approx(
        by_precision.marginalized_fisher_matrix, rel=2.0e-13
    )
    assert by_covariance.parameter_covariance == pytest.approx(
        by_precision.parameter_covariance, rel=2.0e-13
    )


def test_independent_scale_errors_inflate_both_physical_uncertainties() -> None:
    diagnostics = independent_probe_scale_calibration_information(
        0.02,
        1.5,
        [0.15, 0.5, 1.5, 4.5, 12.0],
        calibration_log_standard_deviations=[0.02] * 5,
        relative_standard_deviation=0.03,
    )

    assert diagnostics.nuisance_dimension == 5
    assert diagnostics.rank == 2
    assert np.all(np.asarray(diagnostics.standard_deviation_inflation) >= 1.0)
    assert diagnostics.standard_deviation_inflation[0] > 1.0
    assert diagnostics.standard_deviation_inflation[1] > 1.0


def test_basis_constructors_and_outputs_are_immutable() -> None:
    common = common_log_scale_basis(4)
    independent = independent_log_scale_basis(4)
    assert common.shape == (4, 1)
    assert independent.shape == (4, 4)
    assert not common.flags.writeable
    assert not independent.flags.writeable

    diagnostics = common_probe_scale_calibration_information(
        0.02,
        1.0,
        [0.2, 0.7, 2.0],
        calibration_log_standard_deviation=0.03,
        relative_standard_deviation=0.04,
    )
    arrays = (
        diagnostics.calibration_basis,
        diagnostics.probe_log_jacobian,
        diagnostics.nuisance_jacobian,
        diagnostics.nuisance_prior_precision,
        diagnostics.joint_fisher_matrix,
        diagnostics.nuisance_fisher_matrix,
        diagnostics.marginalized_fisher_matrix,
        diagnostics.singular_values,
        diagnostics.parameter_covariance,
        diagnostics.standard_deviation_inflation,
    )
    assert all(array is not None and not array.flags.writeable for array in arrays)


@pytest.mark.parametrize(
    "operation, message",
    [
        (lambda: common_log_scale_basis(0), "positive integer"),
        (lambda: independent_log_scale_basis(True), "positive integer"),
        (
            lambda: gaussian_probe_scale_calibration_information(
                1.0,
                1.0,
                [0.2, 1.0],
                [[1.0], [1.0], [1.0]],
                relative_standard_deviation=0.1,
            ),
            "shape",
        ),
        (
            lambda: gaussian_probe_scale_calibration_information(
                1.0,
                1.0,
                [0.2, 1.0],
                [[1.0], [1.0]],
                relative_standard_deviation=0.1,
                calibration_prior_standard_deviations=[0.1],
                calibration_prior_covariance=[[0.01]],
            ),
            "at most one",
        ),
        (
            lambda: gaussian_probe_scale_calibration_information(
                1.0,
                1.0,
                [0.2, 1.0],
                [[1.0], [1.0]],
                relative_standard_deviation=0.1,
                calibration_prior_covariance=[[0.0]],
            ),
            "positive definite",
        ),
        (
            lambda: gaussian_probe_scale_calibration_information(
                1.0,
                1.0,
                [0.2, 1.0],
                [[1.0], [1.0]],
                relative_standard_deviation=0.1,
                calibration_prior_precision=[[-1.0]],
            ),
            "positive semidefinite",
        ),
        (
            lambda: common_probe_scale_calibration_information(
                1.0,
                1.0,
                [0.2, 1.0],
                calibration_log_standard_deviation=0.0,
                relative_standard_deviation=0.1,
            ),
            "finite and positive",
        ),
    ],
)
def test_invalid_inputs(operation, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        operation()
