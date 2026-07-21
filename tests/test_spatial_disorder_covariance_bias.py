from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_covariance_bias import (
    fit_gaussian_log_variance_surrogate,
    gaussian_family_inverse_bias,
    gaussian_pairwise_parameter_drift,
    matern_family_gaussian_inverse_bias,
)
from mct_research.spatial_disorder_covariance_families import (
    gaussian_reference_variance,
    matern_gaussian_probe_variance_2d,
)


BROAD_SCALES = np.array([0.0, 0.5, 2.0, 8.0, 20.0])


def test_exact_gaussian_data_have_no_pairwise_drift_or_global_bias() -> None:
    diagnostics = gaussian_family_inverse_bias(
        0.01,
        2.0,
        BROAD_SCALES,
    )
    assert diagnostics.pairwise_drift.point_variance_spread_ratio == pytest.approx(
        1.0, rel=1.0e-13
    )
    assert diagnostics.pairwise_drift.correlation_length_spread_ratio == pytest.approx(
        1.0, rel=1.0e-13
    )
    assert diagnostics.point_variance_bias_ratio == pytest.approx(
        1.0, rel=5.0e-12
    )
    assert diagnostics.correlation_length_bias_ratio == pytest.approx(
        1.0, rel=5.0e-12
    )
    assert diagnostics.global_surrogate.rms_log_error < 5.0e-12
    assert (
        diagnostics.global_surrogate.maximum_absolute_relative_variance_error
        < 5.0e-12
    )


def test_non_gaussian_pairwise_drift_orders_with_matern_smoothness() -> None:
    diagnostics = {
        smoothness: matern_family_gaussian_inverse_bias(
            0.01,
            2.0,
            BROAD_SCALES,
            smoothness,
        )
        for smoothness in (0.5, 1.5, 2.5)
    }
    assert (
        diagnostics[0.5].pairwise_drift.correlation_length_spread_ratio
        > diagnostics[1.5].pairwise_drift.correlation_length_spread_ratio
        > diagnostics[2.5].pairwise_drift.correlation_length_spread_ratio
        > 1.0
    )
    assert (
        diagnostics[0.5].pairwise_drift.point_variance_spread_ratio
        > diagnostics[1.5].pairwise_drift.point_variance_spread_ratio
        > diagnostics[2.5].pairwise_drift.point_variance_spread_ratio
        > 1.0
    )


def test_global_surrogate_bias_orders_with_matern_smoothness() -> None:
    diagnostics = {
        smoothness: matern_family_gaussian_inverse_bias(
            0.01,
            2.0,
            BROAD_SCALES,
            smoothness,
        )
        for smoothness in (0.5, 1.5, 2.5)
    }
    assert (
        diagnostics[0.5].global_surrogate.rms_log_error
        > diagnostics[1.5].global_surrogate.rms_log_error
        > diagnostics[2.5].global_surrogate.rms_log_error
        > 0.0
    )
    assert diagnostics[0.5].point_variance_bias_ratio == pytest.approx(
        0.8351085397306751, rel=3.0e-11
    )
    assert diagnostics[0.5].correlation_length_bias_ratio == pytest.approx(
        1.0406401414252207, rel=3.0e-11
    )
    assert diagnostics[0.5].pairwise_drift.correlation_length_spread_ratio == pytest.approx(
        3.418125791274161, rel=3.0e-11
    )


def test_three_scale_design_exposes_fitting_convention_dependence() -> None:
    scales = np.array([0.25, 1.0, 4.0])
    diagnostics = matern_family_gaussian_inverse_bias(
        0.01,
        2.0,
        scales,
        0.5,
    )
    assert diagnostics.pairwise_drift.point_variance_spread_ratio > 1.3
    assert diagnostics.pairwise_drift.correlation_length_spread_ratio > 1.5
    assert diagnostics.point_variance_bias_ratio == pytest.approx(
        0.7594677130319091, rel=3.0e-11
    )
    assert diagnostics.global_surrogate.maximum_absolute_relative_variance_error == pytest.approx(
        0.14315129656512116, rel=3.0e-11
    )


def test_amplitude_and_length_unit_invariance() -> None:
    base = matern_family_gaussian_inverse_bias(
        0.01,
        2.0,
        BROAD_SCALES,
        1.5,
    )
    rescaled = matern_family_gaussian_inverse_bias(
        2.5e4,
        2.0e-6,
        BROAD_SCALES * 1.0e-6,
        1.5,
    )
    assert rescaled.point_variance_bias_ratio == pytest.approx(
        base.point_variance_bias_ratio, rel=3.0e-12
    )
    assert rescaled.correlation_length_bias_ratio == pytest.approx(
        base.correlation_length_bias_ratio, rel=3.0e-12
    )
    assert rescaled.pairwise_drift.point_variance_spread_ratio == pytest.approx(
        base.pairwise_drift.point_variance_spread_ratio, rel=3.0e-12
    )
    assert rescaled.pairwise_drift.correlation_length_spread_ratio == pytest.approx(
        base.pairwise_drift.correlation_length_spread_ratio, rel=3.0e-12
    )
    assert rescaled.global_surrogate.rms_log_error == pytest.approx(
        base.global_surrogate.rms_log_error, rel=3.0e-12
    )


def test_weighting_changes_the_reported_global_surrogate() -> None:
    values = matern_gaussian_probe_variance_2d(
        0.01,
        2.0,
        BROAD_SCALES,
        0.5,
    )
    equal = fit_gaussian_log_variance_surrogate(BROAD_SCALES, values)
    point_weighted = fit_gaussian_log_variance_surrogate(
        BROAD_SCALES,
        values,
        weights=[10.0, 1.0, 1.0, 1.0, 1.0],
    )
    assert point_weighted.fitted_point_variance > equal.fitted_point_variance
    assert point_weighted.fitted_correlation_length != pytest.approx(
        equal.fitted_correlation_length, rel=1.0e-3
    )


def test_outputs_are_immutable() -> None:
    diagnostics = matern_family_gaussian_inverse_bias(
        0.01,
        2.0,
        BROAD_SCALES,
        1.5,
    )
    arrays = (
        diagnostics.probe_sigmas,
        diagnostics.true_filtered_variances,
        diagnostics.pairwise_drift.pair_indices,
        diagnostics.pairwise_drift.point_variances,
        diagnostics.pairwise_drift.correlation_lengths,
        diagnostics.global_surrogate.normalized_weights,
        diagnostics.global_surrogate.fitted_variances,
        diagnostics.global_surrogate.log_residuals,
    )
    assert all(not array.flags.writeable for array in arrays)


def test_pairwise_helper_reuses_existing_exact_recovery() -> None:
    values = gaussian_reference_variance(0.017, 1.8, [0.0, 0.2, 0.9, 2.7])
    drift = gaussian_pairwise_parameter_drift(
        [0.0, 0.2, 0.9, 2.7],
        values,
    )
    assert drift.point_variances == pytest.approx(
        np.full(6, 0.017), rel=5.0e-14
    )
    assert drift.correlation_lengths == pytest.approx(
        np.full(6, 1.8), rel=5.0e-14
    )


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        gaussian_pairwise_parameter_drift([1.0], [1.0])
    with pytest.raises(ValueError, match="distinct"):
        gaussian_pairwise_parameter_drift([1.0, 1.0], [1.0, 0.5])
    with pytest.raises(ValueError, match="positive"):
        fit_gaussian_log_variance_surrogate([0.0, 1.0], [1.0, 0.0])
    with pytest.raises(ValueError, match="weights"):
        fit_gaussian_log_variance_surrogate(
            [0.0, 1.0, 2.0],
            [1.0, 0.5, 0.3],
            weights=[1.0, 1.0],
        )
    with pytest.raises(ValueError, match="smoothness"):
        matern_family_gaussian_inverse_bias(
            1.0,
            1.0,
            [0.0, 1.0, 2.0],
            1.0,
        )
    with pytest.raises(ValueError, match="maximum_iterations"):
        fit_gaussian_log_variance_surrogate(
            [0.0, 1.0],
            [1.0, 0.5],
            maximum_iterations=0,
        )
    with pytest.raises(ValueError, match="finite and positive"):
        gaussian_family_inverse_bias(math.inf, 1.0, [0.0, 1.0])
