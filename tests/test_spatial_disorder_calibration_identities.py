from __future__ import annotations

import numpy as np
import pytest

from mct_research.spatial_disorder_calibration import (
    common_probe_scale_calibration_information,
)


@pytest.mark.parametrize("tau", [1.0e-4, 0.01, 0.1, 0.5])
def test_common_calibration_covariance_increment_for_multiple_priors(tau: float) -> None:
    diagnostics = common_probe_scale_calibration_information(
        0.03,
        1.4,
        [0.0, 0.2, 0.7, 2.0, 6.0],
        calibration_log_standard_deviation=tau,
        relative_standard_deviation=0.04,
    )
    exact = np.asarray(diagnostics.base_diagnostics.parameter_covariance)
    calibrated = np.asarray(diagnostics.parameter_covariance)
    expected_increment = np.array([[0.0, 0.0], [0.0, tau**2]])

    assert calibrated - exact == pytest.approx(
        expected_increment,
        rel=2.0e-10,
        abs=max(2.0e-15, 2.0e-13 * tau**2),
    )


def test_common_calibration_result_is_invariant_to_length_units() -> None:
    kwargs = dict(
        point_variance=0.02,
        calibration_log_standard_deviation=0.03,
        relative_standard_deviation=0.05,
    )
    reference = common_probe_scale_calibration_information(
        correlation_length=1.7,
        probe_sigmas=[0.1, 0.5, 1.7, 5.0],
        **kwargs,
    )
    rescaled = common_probe_scale_calibration_information(
        correlation_length=1.7e-6,
        probe_sigmas=[0.1e-6, 0.5e-6, 1.7e-6, 5.0e-6],
        **kwargs,
    )

    assert rescaled.base_diagnostics.predicted_variance == pytest.approx(
        reference.base_diagnostics.predicted_variance,
        rel=2.0e-14,
    )
    assert rescaled.marginalized_fisher_matrix == pytest.approx(
        reference.marginalized_fisher_matrix,
        rel=2.0e-13,
    )
    assert rescaled.parameter_covariance == pytest.approx(
        reference.parameter_covariance,
        rel=2.0e-13,
    )


def test_common_calibration_prior_does_not_change_log_amplitude_variance() -> None:
    weak = common_probe_scale_calibration_information(
        0.05,
        2.0,
        [0.15, 0.8, 2.0, 8.0],
        calibration_log_standard_deviation=0.01,
        relative_standard_deviation=0.03,
    )
    loose = common_probe_scale_calibration_information(
        0.05,
        2.0,
        [0.15, 0.8, 2.0, 8.0],
        calibration_log_standard_deviation=0.3,
        relative_standard_deviation=0.03,
    )

    assert loose.parameter_covariance[0, 0] == pytest.approx(
        weak.parameter_covariance[0, 0],
        rel=2.0e-11,
    )
    assert loose.parameter_covariance[0, 1] == pytest.approx(
        weak.parameter_covariance[0, 1],
        rel=2.0e-11,
    )
    assert loose.parameter_covariance[1, 1] - weak.parameter_covariance[1, 1] == pytest.approx(
        0.3**2 - 0.01**2,
        rel=2.0e-11,
    )
