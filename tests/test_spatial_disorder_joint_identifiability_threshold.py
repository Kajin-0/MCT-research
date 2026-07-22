from __future__ import annotations

import numpy as np

from mct_research.spatial_disorder_instrument import CompositeInstrumentKernel
from mct_research.spatial_disorder_joint_identifiability import (
    joint_identifiability_screen,
)


def test_near_threshold_design_is_flagged_as_convention_sensitive() -> None:
    kernels = (
        CompositeInstrumentKernel(0.2, 0.2, 0.4, 0.4, 0.5, 10.0),
        CompositeInstrumentKernel(1.0, 1.0, 2.0, 2.0, 0.5, 10.0),
        CompositeInstrumentKernel(4.0, 4.0, 8.0, 8.0, 0.5, 10.0),
    )
    instrument_log_sd = np.array([0.05, 0.05, 0.01, 0.01, 0.10, 0.05])
    screen = joint_identifiability_screen(
        point_variance=2.5e-5,
        lateral_correlation_length=2.0,
        depth_correlation_length=2.0,
        kernels=kernels,
        instrument_parameter_log_covariance=np.diag(
            instrument_log_sd**2
        ),
        observation_log_standard_deviations=[0.03, 0.03, 0.03],
        threshold_distance=6.195,
        depth_quadrature_order=128,
    )

    assert screen.convention_sensitive_families == ("matern_0.5",)
    exponential = {
        item.fitting_convention: item
        for item in screen.results
        if item.true_family == "matern_0.5"
    }
    assert (
        exponential["log_variance"].decision
        == "kernel_shape_limited"
    )
    assert (
        exponential["reciprocal_variance"].decision
        == "resolved_under_full_envelope"
    )
