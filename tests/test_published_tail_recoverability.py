from __future__ import annotations

import math

import pytest

from mct_research.published_tail_recoverability import (
    GaussianTailWindowStraightness,
    PublishedFigureTraceRecoverability,
    SourceConditionedTrace,
    critical_upper_standardized_energy,
    finkman_modified_urbach_trace_span_ev,
    gaussian_power_tail_pixel_recoverability,
    gaussian_power_tail_window_straightness,
    source_conditioned_finkman_trace,
)


def test_public_result_types_and_functions() -> None:
    assert GaussianTailWindowStraightness.__name__ == "GaussianTailWindowStraightness"
    assert PublishedFigureTraceRecoverability.__name__ == (
        "PublishedFigureTraceRecoverability"
    )
    assert SourceConditionedTrace.__name__ == "SourceConditionedTrace"
    assert callable(gaussian_power_tail_window_straightness)
    assert callable(gaussian_power_tail_pixel_recoverability)
    assert callable(critical_upper_standardized_energy)
    assert callable(finkman_modified_urbach_trace_span_ev)
    assert callable(source_conditioned_finkman_trace)


def test_fixed_dynamic_range_becomes_arbitrarily_straight_deeper_in_tail() -> None:
    dynamic_range = math.log10(1000.0 / 5.0)
    near = gaussian_power_tail_window_straightness(
        -2.0,
        dynamic_range,
        sample_count=161,
        quadrature_order=256,
    )
    middle = gaussian_power_tail_window_straightness(
        -4.0,
        dynamic_range,
        sample_count=161,
        quadrature_order=256,
    )
    deep = gaussian_power_tail_window_straightness(
        -6.0,
        dynamic_range,
        sample_count=161,
        quadrature_order=256,
    )

    assert near.maximum_vertical_residual_decades > (
        middle.maximum_vertical_residual_decades
    )
    assert middle.maximum_vertical_residual_decades > (
        deep.maximum_vertical_residual_decades
    )
    assert near.maximum_horizontal_residual_fraction > (
        middle.maximum_horizontal_residual_fraction
    )
    assert middle.maximum_horizontal_residual_fraction > (
        deep.maximum_horizontal_residual_fraction
    )
    assert deep.lower_standardized_energy < deep.upper_standardized_energy


def test_deep_tail_straightness_has_inverse_square_scaling() -> None:
    dynamic_range = math.log10(1000.0 / 5.0)
    at_six = gaussian_power_tail_window_straightness(
        -6.0,
        dynamic_range,
        sample_count=161,
        quadrature_order=256,
    )
    at_eight = gaussian_power_tail_window_straightness(
        -8.0,
        dynamic_range,
        sample_count=161,
        quadrature_order=256,
        standard_deviation_limit=12.0,
    )

    scaled_six = 6.0**2 * at_six.maximum_horizontal_residual_fraction
    scaled_eight = 8.0**2 * at_eight.maximum_horizontal_residual_fraction
    assert scaled_eight == pytest.approx(scaled_six, rel=0.20)


def test_finkman_1984_high_temperature_panel_reference() -> None:
    trace = source_conditioned_finkman_trace(
        source_identifier="Finkman-Schacham-1984-Fig4-300K",
        composition=0.29,
        temperature_k=300.0,
        absorption_min_cm_inverse=5.0,
        absorption_max_cm_inverse=1000.0,
        panel_energy_min_ev=0.20,
        panel_energy_max_ev=0.30,
        panel_width_px=545.0,
        panel_absorption_min_cm_inverse=5.0,
        panel_absorption_max_cm_inverse=1000.0,
        panel_height_px=562.0,
        marker_center_uncertainty_px=6.0,
        sample_count=161,
        quadrature_order=256,
    )

    assert trace.trace_energy_span_ev == pytest.approx(0.0480119, rel=2.0e-5)
    assert trace.trace_horizontal_span_px == pytest.approx(261.665, rel=2.0e-4)
    assert trace.trace_vertical_span_px == pytest.approx(562.0)
    assert trace.departure_at_mean_gap_px == pytest.approx(25.7, rel=0.025)
    assert trace.critical_upper_z_one_sigma == pytest.approx(-3.19, abs=0.08)
    assert trace.critical_upper_z_three_sigma == pytest.approx(-0.73, abs=0.08)


def test_finkman_low_temperature_trace_fails_conservative_three_sigma_gate() -> None:
    trace = source_conditioned_finkman_trace(
        source_identifier="Finkman-Schacham-1984-Fig4-85K",
        composition=0.29,
        temperature_k=85.0,
        absorption_min_cm_inverse=5.0,
        absorption_max_cm_inverse=1000.0,
        panel_energy_min_ev=0.20,
        panel_energy_max_ev=0.30,
        panel_width_px=545.0,
        panel_absorption_min_cm_inverse=5.0,
        panel_absorption_max_cm_inverse=1000.0,
        panel_height_px=562.0,
        marker_center_uncertainty_px=6.0,
        sample_count=161,
        quadrature_order=256,
    )

    assert trace.trace_horizontal_span_px == pytest.approx(114.35, rel=0.002)
    assert trace.departure_at_mean_gap_px == pytest.approx(12.2, rel=0.03)
    assert trace.critical_upper_z_one_sigma == pytest.approx(-1.46, abs=0.10)
    assert trace.critical_upper_z_three_sigma is None


def test_finkman_1979_high_temperature_panel_reference() -> None:
    trace = source_conditioned_finkman_trace(
        source_identifier="Finkman-Nemirovsky-1979-Fig3-300K",
        composition=0.205,
        temperature_k=300.0,
        absorption_min_cm_inverse=20.0,
        absorption_max_cm_inverse=1000.0,
        panel_energy_min_ev=0.08,
        panel_energy_max_ev=0.18,
        panel_width_px=848.0,
        panel_absorption_min_cm_inverse=5.0,
        panel_absorption_max_cm_inverse=2000.0,
        panel_height_px=982.0,
        marker_center_uncertainty_px=6.0,
        sample_count=161,
        quadrature_order=256,
    )

    assert trace.trace_energy_span_ev == pytest.approx(0.0379503, rel=2.0e-5)
    assert trace.trace_horizontal_span_px == pytest.approx(321.818, rel=2.0e-4)
    assert trace.trace_vertical_span_px == pytest.approx(641.1, rel=0.002)
    assert trace.departure_at_mean_gap_px == pytest.approx(26.5, rel=0.03)
    assert trace.critical_upper_z_one_sigma == pytest.approx(-3.04, abs=0.08)
    assert trace.critical_upper_z_three_sigma == pytest.approx(-0.73, abs=0.08)


def test_pixel_departure_is_below_marker_uncertainty_for_deep_window() -> None:
    result = gaussian_power_tail_pixel_recoverability(
        -6.0,
        math.log10(1000.0 / 5.0),
        trace_horizontal_span_px=261.665,
        trace_vertical_span_px=562.0,
        center_uncertainty_px=6.0,
        sample_count=161,
        quadrature_order=256,
    )

    assert result.maximum_orthogonal_departure_px == pytest.approx(2.38, rel=0.04)
    assert result.departure_to_uncertainty_ratio < 0.5
    assert not result.one_sigma_resolvable
    assert not result.three_sigma_resolvable


def test_input_validation() -> None:
    dynamic_range = math.log10(1000.0 / 5.0)
    with pytest.raises(ValueError, match="<= 0"):
        gaussian_power_tail_window_straightness(0.1, dynamic_range)
    with pytest.raises(ValueError, match="positive"):
        gaussian_power_tail_window_straightness(-2.0, 0.0)
    with pytest.raises(ValueError, match="sample_count"):
        gaussian_power_tail_window_straightness(-2.0, dynamic_range, sample_count=17)
    with pytest.raises(ValueError, match="composition"):
        finkman_modified_urbach_trace_span_ev(1.2, 300.0, 5.0, 1000.0)
    with pytest.raises(ValueError, match="exceed"):
        finkman_modified_urbach_trace_span_ev(0.29, 300.0, 1000.0, 5.0)
