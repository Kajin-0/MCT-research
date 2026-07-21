from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_calibration import (
    gaussian_common_probe_scale_calibration,
    gaussian_multiscale_fisher_with_probe_uncertainty,
    gaussian_probe_log_jacobian,
)
from mct_research.spatial_disorder_inference import (
    gaussian_multiscale_log_jacobian,
    gaussian_multiscale_variance,
)


POINT_VARIANCE = 0.01
CORRELATION_LENGTH = 2.0
SCALES = np.array([0.0, 0.4, 2.0, 10.0])
RELATIVE_NOISE = 0.05


def test_probe_log_jacobian_matches_stable_central_differences() -> None:
    analytical = gaussian_probe_log_jacobian(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
    )
    numerical = np.zeros(SCALES.size)
    step = 1.0e-5
    for index, scale in enumerate(SCALES):
        if scale == 0.0:
            continue
        upper = SCALES.copy()
        lower = SCALES.copy()
        upper[index] *= math.exp(step)
        lower[index] *= math.exp(-step)
        numerical[index] = (
            gaussian_multiscale_variance(
                POINT_VARIANCE,
                CORRELATION_LENGTH,
                upper,
            )[index]
            - gaussian_multiscale_variance(
                POINT_VARIANCE,
                CORRELATION_LENGTH,
                lower,
            )[index]
        ) / (2.0 * step)

    assert analytical == pytest.approx(numerical, rel=1.0e-9, abs=1.0e-14)


def test_common_scale_mode_is_exactly_opposite_log_correlation_column() -> None:
    scale_jacobian = gaussian_probe_log_jacobian(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
    )
    physics_jacobian = gaussian_multiscale_log_jacobian(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
    )
    assert scale_jacobian == pytest.approx(
        -physics_jacobian[:, 1],
        rel=2.0e-15,
        abs=1.0e-18,
    )


def test_common_calibration_adds_exact_log_length_variance() -> None:
    calibration_std = 0.02
    diagnostics = gaussian_common_probe_scale_calibration(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        log_scale_standard_deviation=calibration_std,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    assert diagnostics.base_parameter_covariance is not None
    assert diagnostics.parameter_covariance is not None

    expected = np.asarray(diagnostics.base_parameter_covariance).copy()
    expected[1, 1] += calibration_std**2
    assert diagnostics.parameter_covariance == pytest.approx(
        expected,
        rel=5.0e-14,
        abs=5.0e-18,
    )
    assert diagnostics.parameter_covariance[0, 0] == pytest.approx(
        diagnostics.base_parameter_covariance[0, 0],
        rel=5.0e-14,
    )
    assert diagnostics.parameter_covariance[0, 1] == pytest.approx(
        diagnostics.base_parameter_covariance[0, 1],
        rel=5.0e-14,
    )


def test_general_nuisance_basis_matches_direct_block_calculation() -> None:
    basis = np.array(
        [
            [1.0, 0.0],
            [1.0, 0.5],
            [1.0, -0.25],
            [1.0, 1.0],
        ]
    )
    nuisance_covariance = np.array(
        [
            [4.0e-4, 5.0e-5],
            [5.0e-5, 9.0e-4],
        ]
    )
    diagnostics = gaussian_multiscale_fisher_with_probe_uncertainty(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        nuisance_basis=basis,
        nuisance_covariance=nuisance_covariance,
        relative_standard_deviation=RELATIVE_NOISE,
    )

    observation_precision = np.linalg.inv(
        np.asarray(diagnostics.observation_covariance)
    )
    physics = np.asarray(diagnostics.physics_jacobian)
    nuisance = np.asarray(diagnostics.nuisance_jacobian)
    physics_block = physics.T @ observation_precision @ physics
    cross_block = physics.T @ observation_precision @ nuisance
    nuisance_block = (
        nuisance.T @ observation_precision @ nuisance
        + np.linalg.inv(nuisance_covariance)
    )
    direct = physics_block - cross_block @ np.linalg.solve(
        nuisance_block,
        cross_block.T,
    )
    direct = 0.5 * (direct + direct.T)

    assert diagnostics.marginalized_fisher_matrix == pytest.approx(
        direct,
        rel=2.0e-13,
        abs=2.0e-12,
    )
    assert diagnostics.parameter_covariance is not None
    augmented_covariance = np.linalg.inv(
        np.asarray(diagnostics.augmented_fisher_matrix)
    )
    assert diagnostics.parameter_covariance == pytest.approx(
        augmented_covariance[:2, :2],
        rel=2.0e-13,
        abs=2.0e-16,
    )


def test_weak_common_calibration_prior_recovers_rank_deficiency() -> None:
    diagnostics = gaussian_common_probe_scale_calibration(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        log_scale_standard_deviation=1.0e6,
        relative_standard_deviation=RELATIVE_NOISE,
        rank_relative_tolerance=1.0e-6,
    )
    assert diagnostics.rank == 1
    assert math.isinf(diagnostics.condition_number)
    assert diagnostics.parameter_covariance is None
    assert diagnostics.parameter_standard_deviation_inflation is None


def test_independent_scale_errors_degrade_both_parameters() -> None:
    calibration_std = 0.02
    diagnostics = gaussian_multiscale_fisher_with_probe_uncertainty(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        nuisance_basis=np.eye(SCALES.size),
        nuisance_covariance=np.eye(SCALES.size) * calibration_std**2,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    assert diagnostics.parameter_standard_deviation_inflation is not None
    assert diagnostics.parameter_standard_deviation_inflation[0] > 1.0
    assert diagnostics.parameter_standard_deviation_inflation[1] > 1.0
    assert diagnostics.parameter_standard_deviation_inflation == pytest.approx(
        [1.0072853255206649, 1.1328944237548817],
        rel=2.0e-13,
    )


def test_common_calibration_is_length_unit_invariant() -> None:
    reference = gaussian_common_probe_scale_calibration(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        log_scale_standard_deviation=0.03,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    length_unit = 1.0e-6
    rescaled = gaussian_common_probe_scale_calibration(
        POINT_VARIANCE,
        CORRELATION_LENGTH * length_unit,
        SCALES * length_unit,
        log_scale_standard_deviation=0.03,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    assert rescaled.probe_scale_ratios == pytest.approx(
        reference.probe_scale_ratios,
        rel=2.0e-15,
    )
    assert rescaled.marginalized_fisher_matrix == pytest.approx(
        reference.marginalized_fisher_matrix,
        rel=2.0e-14,
    )
    assert rescaled.parameter_covariance == pytest.approx(
        reference.parameter_covariance,
        rel=3.0e-14,
    )


def test_outputs_are_immutable() -> None:
    diagnostics = gaussian_common_probe_scale_calibration(
        POINT_VARIANCE,
        CORRELATION_LENGTH,
        SCALES,
        log_scale_standard_deviation=0.02,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    arrays = (
        diagnostics.predicted_variance,
        diagnostics.probe_scale_ratios,
        diagnostics.physics_jacobian,
        diagnostics.probe_log_jacobian,
        diagnostics.nuisance_basis,
        diagnostics.nuisance_jacobian,
        diagnostics.observation_covariance,
        diagnostics.nuisance_covariance,
        diagnostics.augmented_fisher_matrix,
        diagnostics.marginalized_fisher_matrix,
        diagnostics.singular_values,
        diagnostics.base_parameter_covariance,
        diagnostics.parameter_covariance,
        diagnostics.parameter_standard_deviation_inflation,
    )
    assert all(array is not None and not array.flags.writeable for array in arrays)


def test_invalid_calibration_inputs() -> None:
    kwargs = dict(
        point_variance=POINT_VARIANCE,
        correlation_length=CORRELATION_LENGTH,
        probe_sigmas=SCALES,
        relative_standard_deviation=RELATIVE_NOISE,
    )
    with pytest.raises(ValueError, match="log_scale_standard_deviation"):
        gaussian_common_probe_scale_calibration(
            **kwargs,
            log_scale_standard_deviation=0.0,
        )
    with pytest.raises(ValueError, match="nuisance_basis"):
        gaussian_multiscale_fisher_with_probe_uncertainty(
            **kwargs,
            nuisance_basis=np.ones((3, 1)),
            nuisance_covariance=[[1.0]],
        )
    with pytest.raises(ValueError, match="symmetric"):
        gaussian_multiscale_fisher_with_probe_uncertainty(
            **kwargs,
            nuisance_basis=np.ones((4, 2)),
            nuisance_covariance=[[1.0, 0.2], [0.1, 1.0]],
        )
    with pytest.raises(ValueError, match="positive definite"):
        gaussian_multiscale_fisher_with_probe_uncertainty(
            **kwargs,
            nuisance_basis=np.ones((4, 2)),
            nuisance_covariance=[[1.0, 1.0], [1.0, 1.0]],
        )
    with pytest.raises(ValueError, match="exactly one"):
        gaussian_multiscale_fisher_with_probe_uncertainty(
            POINT_VARIANCE,
            CORRELATION_LENGTH,
            SCALES,
            nuisance_basis=np.ones((4, 1)),
            nuisance_covariance=[[1.0]],
        )
