from __future__ import annotations

import math

import numpy as np
import pytest

from mct_research.spatial_disorder_cutoff import (
    lateral_gaussian_gap_response_cutoff,
)
from mct_research.spatial_disorder_design import (
    MultiscaleCutoffPrediction,
    MultiscaleGapWidthPrediction,
    multiscale_gaussian_gap_cutoff_prediction,
    multiscale_gaussian_gap_width,
)


def test_exact_gap_width_formula_and_point_probe_limit() -> None:
    prediction = multiscale_gaussian_gap_width(
        point_composition_variance=4.0e-6,
        correlation_length=2.0,
        gap_slope_ev_per_fraction=-1.5,
        probe_sigmas=[0.0, 2.0, 6.0],
    )

    assert isinstance(prediction, MultiscaleGapWidthPrediction)
    expected_variance = 4.0e-6 / np.array([1.0, 3.0, 19.0])
    assert prediction.effective_composition_variance == pytest.approx(
        expected_variance,
        rel=1.0e-14,
    )
    assert prediction.effective_composition_standard_deviation == pytest.approx(
        np.sqrt(expected_variance),
        rel=1.0e-14,
    )
    assert prediction.effective_gap_standard_deviation_ev == pytest.approx(
        1.5 * np.sqrt(expected_variance),
        rel=1.0e-14,
    )
    assert prediction.effective_composition_variance[0] == 4.0e-6
    assert prediction.effective_gap_standard_deviation_ev[0] == pytest.approx(0.003)


def test_large_probe_asymptote() -> None:
    point_variance = 9.0e-6
    correlation = 0.7
    slope = 1.8
    scale = 1.0e6
    prediction = multiscale_gaussian_gap_width(
        point_composition_variance=point_variance,
        correlation_length=correlation,
        gap_slope_ev_per_fraction=slope,
        probe_sigmas=scale,
    )

    variance_scaled = (
        float(prediction.effective_composition_variance)
        * 2.0
        * scale**2
        / (point_variance * correlation**2)
    )
    gap_scaled = (
        float(prediction.effective_gap_standard_deviation_ev)
        * math.sqrt(2.0)
        * scale
        / (abs(slope) * math.sqrt(point_variance) * correlation)
    )
    assert variance_scaled == pytest.approx(1.0, rel=1.0e-12)
    assert gap_scaled == pytest.approx(1.0, rel=1.0e-12)


def test_effective_variance_and_gap_width_decrease_with_sorted_probe_scale() -> None:
    prediction = multiscale_gaussian_gap_width(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=2.0,
        probe_sigmas=np.geomspace(1.0e-3, 1.0e3, 15),
    )
    assert np.all(np.diff(prediction.effective_composition_variance) < 0.0)
    assert np.all(np.diff(prediction.effective_gap_standard_deviation_ev) < 0.0)


def test_gap_width_scaling_and_length_unit_invariance() -> None:
    scales = np.array([0.0, 0.2, 1.0, 5.0])
    reference = multiscale_gaussian_gap_width(
        point_composition_variance=4.0e-6,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.5,
        probe_sigmas=scales,
    )
    composition_scaled = multiscale_gaussian_gap_width(
        point_composition_variance=9.0 * 4.0e-6,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.5,
        probe_sigmas=scales,
    )
    slope_scaled = multiscale_gaussian_gap_width(
        point_composition_variance=4.0e-6,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=-4.5,
        probe_sigmas=scales,
    )
    length_scale = 1.0e-6
    unit_scaled = multiscale_gaussian_gap_width(
        point_composition_variance=4.0e-6,
        correlation_length=length_scale,
        gap_slope_ev_per_fraction=1.5,
        probe_sigmas=scales * length_scale,
    )

    assert composition_scaled.effective_gap_standard_deviation_ev == pytest.approx(
        3.0 * reference.effective_gap_standard_deviation_ev,
        rel=2.0e-14,
    )
    assert slope_scaled.effective_gap_standard_deviation_ev == pytest.approx(
        3.0 * reference.effective_gap_standard_deviation_ev,
        rel=2.0e-14,
    )
    assert unit_scaled.probe_scale_ratios == pytest.approx(
        reference.probe_scale_ratios,
        rel=2.0e-14,
    )
    assert unit_scaled.effective_gap_standard_deviation_ev == pytest.approx(
        reference.effective_gap_standard_deviation_ev,
        rel=2.0e-14,
    )


def _cutoff_kwargs() -> dict[str, float | int]:
    return {
        "mean_gap_ev": 0.10,
        "thickness_cm": 0.02,
        "lower_energy_ev": 0.06,
        "upper_energy_ev": 0.14,
        "target_response": 0.30,
        "exponent": 0.0,
        "amplitude_cm_inverse_ev_power": 200.0,
        "absolute_tolerance_ev": 1.0e-11,
        "response_tolerance": 1.0e-12,
        "max_iterations": 128,
    }


def test_end_to_end_cutoffs_equal_direct_per_scale_calls() -> None:
    scales = np.array([0.0, 0.5, 2.0, 8.0])
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.2,
        gap_slope_ev_per_fraction=1.6,
        probe_sigmas=scales,
        **_cutoff_kwargs(),
    )

    assert isinstance(prediction, MultiscaleCutoffPrediction)
    for index, gap_sigma in enumerate(
        prediction.gap_width.effective_gap_standard_deviation_ev
    ):
        direct = lateral_gaussian_gap_response_cutoff(
            gap_sigma_ev=float(gap_sigma),
            **_cutoff_kwargs(),
        )
        assert prediction.transmission_averaged_energy_ev[index] == direct.transmission_averaged_energy_ev
        assert prediction.mean_absorption_closure_energy_ev[index] == direct.mean_absorption_closure_energy_ev
        assert prediction.energy_shift_ev[index] == direct.energy_shift_ev
        assert prediction.transmission_averaged_wavelength_um[index] == direct.transmission_averaged_wavelength_um
        assert prediction.wavelength_shift_um[index] == direct.wavelength_shift_um
        assert prediction.transmission_iterations[index] == direct.transmission_iterations


def test_large_probe_cutoffs_converge_to_deterministic_gap_result() -> None:
    common = _cutoff_kwargs()
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.5,
        probe_sigmas=1.0e9,
        **common,
    )
    deterministic = lateral_gaussian_gap_response_cutoff(
        gap_sigma_ev=0.0,
        **common,
    )

    assert float(prediction.transmission_averaged_energy_ev) == pytest.approx(
        deterministic.transmission_averaged_energy_ev,
        abs=2.0e-10,
    )
    assert float(prediction.mean_absorption_closure_energy_ev) == pytest.approx(
        deterministic.mean_absorption_closure_energy_ev,
        abs=2.0e-10,
    )
    assert float(prediction.energy_shift_ev) == pytest.approx(0.0, abs=3.0e-10)


def test_declared_step_edge_cutoff_shift_decreases_with_probe_scale() -> None:
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.5,
        probe_sigmas=[0.0, 0.5, 2.0, 8.0],
        **_cutoff_kwargs(),
    )

    assert np.all(np.diff(prediction.energy_shift_ev) < 0.0)
    assert np.all(np.diff(np.abs(prediction.wavelength_shift_um)) < 0.0)
    ratios = prediction.energy_shift_ev / prediction.gap_width.effective_gap_standard_deviation_ev
    assert ratios == pytest.approx(np.full(4, ratios[0]), rel=2.0e-8)


def test_unsorted_probe_order_is_preserved() -> None:
    scales = np.array([3.0, 0.0, 1.0, 0.2])
    width = multiscale_gaussian_gap_width(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.0,
        probe_sigmas=scales,
    )
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.0,
        probe_sigmas=scales,
        **_cutoff_kwargs(),
    )

    assert width.probe_sigmas == pytest.approx(scales)
    assert prediction.gap_width.probe_sigmas == pytest.approx(scales)
    assert np.argmax(prediction.gap_width.effective_gap_standard_deviation_ev) == 1


def test_scalar_input_preserves_scalar_shapes_and_arrays_are_read_only() -> None:
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.0,
        probe_sigmas=0.5,
        **_cutoff_kwargs(),
    )

    arrays = (
        prediction.gap_width.probe_sigmas,
        prediction.gap_width.effective_composition_variance,
        prediction.gap_width.effective_gap_standard_deviation_ev,
        prediction.transmission_averaged_energy_ev,
        prediction.mean_absorption_closure_energy_ev,
        prediction.energy_shift_ev,
        prediction.transmission_iterations,
    )
    assert all(array.shape == () for array in arrays)
    assert all(not array.flags.writeable for array in arrays)


def test_zero_gap_slope_produces_deterministic_cutoffs_at_every_scale() -> None:
    prediction = multiscale_gaussian_gap_cutoff_prediction(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=0.0,
        probe_sigmas=[0.0, 1.0, 10.0],
        **_cutoff_kwargs(),
    )
    assert prediction.gap_width.effective_gap_standard_deviation_ev == pytest.approx(0.0)
    assert prediction.energy_shift_ev == pytest.approx(0.0, abs=2.0e-10)
    assert prediction.transmission_averaged_energy_ev == pytest.approx(
        np.full(3, prediction.transmission_averaged_energy_ev[0]),
        abs=2.0e-10,
    )


def test_invalid_width_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="point_composition_variance"):
        multiscale_gaussian_gap_width(
            point_composition_variance=0.0,
            correlation_length=1.0,
            gap_slope_ev_per_fraction=1.0,
            probe_sigmas=[0.0],
        )
    with pytest.raises(ValueError, match="correlation_length"):
        multiscale_gaussian_gap_width(
            point_composition_variance=1.0,
            correlation_length=-1.0,
            gap_slope_ev_per_fraction=1.0,
            probe_sigmas=[0.0],
        )
    with pytest.raises(ValueError, match="gap_slope"):
        multiscale_gaussian_gap_width(
            point_composition_variance=1.0,
            correlation_length=1.0,
            gap_slope_ev_per_fraction=math.nan,
            probe_sigmas=[0.0],
        )
    with pytest.raises(ValueError, match="one-dimensional"):
        multiscale_gaussian_gap_width(
            point_composition_variance=1.0,
            correlation_length=1.0,
            gap_slope_ev_per_fraction=1.0,
            probe_sigmas=[[0.0, 1.0]],
        )
    with pytest.raises(ValueError, match="empty"):
        multiscale_gaussian_gap_width(
            point_composition_variance=1.0,
            correlation_length=1.0,
            gap_slope_ev_per_fraction=1.0,
            probe_sigmas=[],
        )
    with pytest.raises(ValueError, match="non-negative"):
        multiscale_gaussian_gap_width(
            point_composition_variance=1.0,
            correlation_length=1.0,
            gap_slope_ev_per_fraction=1.0,
            probe_sigmas=[-1.0],
        )


def test_invalid_cutoff_controls_propagate() -> None:
    base = dict(
        point_composition_variance=1.0e-5,
        correlation_length=1.0,
        gap_slope_ev_per_fraction=1.0,
        probe_sigmas=[0.0, 1.0],
        **_cutoff_kwargs(),
    )
    with pytest.raises(ValueError, match="upper_energy_ev"):
        multiscale_gaussian_gap_cutoff_prediction(
            **{**base, "upper_energy_ev": 0.05}
        )
    with pytest.raises(ValueError, match="target_response"):
        multiscale_gaussian_gap_cutoff_prediction(
            **{**base, "target_response": 1.0}
        )
    with pytest.raises(ValueError, match="exponent"):
        multiscale_gaussian_gap_cutoff_prediction(
            **{**base, "exponent": -0.5}
        )
    with pytest.raises(ValueError, match="quadrature_order"):
        multiscale_gaussian_gap_cutoff_prediction(
            **{**base, "quadrature_order": 16}
        )
