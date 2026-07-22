from __future__ import annotations

import pytest

from mct_research.anchored_tail_validation import (
    chang_reference_traces,
    source_conditioned_anchored_trace,
    urbach_trace_energy_span_ev,
)


def test_urbach_trace_energy_span_is_exact() -> None:
    result = urbach_trace_energy_span_ev(0.014, 100.0, 4000.0)
    assert result == pytest.approx(0.05164431235759511, rel=1.0e-13)


def test_urbach_trace_energy_span_rejects_invalid_ranges() -> None:
    with pytest.raises(ValueError):
        urbach_trace_energy_span_ev(0.0, 100.0, 4000.0)
    with pytest.raises(ValueError):
        urbach_trace_energy_span_ev(0.014, 100.0, 100.0)


def test_chang_reference_headlines() -> None:
    traces = chang_reference_traces()
    assert len(traces) == 4
    expected = [
        (1.6020599913279625, 101.56714763660372, 382.89233792738304, 8.787073423694324),
        (1.0, 63.3978428937694, 239.0, 4.10185254309304),
        (1.3010299956639813, 54.438446875023125, 338.2677988726351, 4.260853700384435),
        (1.0, 41.842576309887804, 260.0, 2.769321138608292),
    ]
    for trace, values in zip(traces, expected, strict=True):
        dynamic_range, horizontal, vertical, departure = values
        assert trace.dynamic_range_decades == pytest.approx(dynamic_range, rel=1.0e-12)
        assert trace.trace_horizontal_span_px == pytest.approx(horizontal, rel=1.0e-12)
        assert trace.trace_vertical_span_px == pytest.approx(vertical, rel=1.0e-12)
        assert trace.maximum_orthogonal_departure_px == pytest.approx(
            departure, rel=1.0e-10
        )
        assert not trace.three_uncertainty_resolvable
        assert not trace.digitization_authorized
        assert trace.decision == "figure_resolution_limited"


def test_only_optimistic_chang_2004_case_crosses_one_uncertainty() -> None:
    traces = chang_reference_traces()
    assert traces[0].one_uncertainty_resolvable
    assert traces[0].critical_upper_z_one_uncertainty == pytest.approx(
        -0.7132787037156341, rel=1.0e-9
    )
    assert traces[0].critical_upper_z_three_uncertainty is None
    for trace in traces[1:]:
        assert not trace.one_uncertainty_resolvable
        assert trace.critical_upper_z_one_uncertainty is None
        assert trace.critical_upper_z_three_uncertainty is None


def test_departure_decreases_when_window_moves_deeper() -> None:
    at_gap = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="at_gap",
        urbach_energy_ev=0.014,
        absorption_min_cm_inverse=100.0,
        absorption_max_cm_inverse=4000.0,
        panel_energy_span_ev=0.30,
        panel_width_px=590.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=478.0,
        center_uncertainty_px=6.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=True,
        upper_standardized_energy=0.0,
    )
    deep = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="deep",
        urbach_energy_ev=0.014,
        absorption_min_cm_inverse=100.0,
        absorption_max_cm_inverse=4000.0,
        panel_energy_span_ev=0.30,
        panel_width_px=590.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=478.0,
        center_uncertainty_px=6.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=True,
        upper_standardized_energy=-1.0,
    )
    assert deep.maximum_orthogonal_departure_px < at_gap.maximum_orthogonal_departure_px


def test_common_energy_unit_rescaling_is_invariant() -> None:
    base = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="ev",
        urbach_energy_ev=0.014,
        absorption_min_cm_inverse=100.0,
        absorption_max_cm_inverse=4000.0,
        panel_energy_span_ev=0.30,
        panel_width_px=590.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=478.0,
        center_uncertainty_px=6.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=True,
    )
    rescaled = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="mev",
        urbach_energy_ev=14.0,
        absorption_min_cm_inverse=1.0e4,
        absorption_max_cm_inverse=4.0e5,
        panel_energy_span_ev=300.0,
        panel_width_px=590.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=478.0,
        center_uncertainty_px=6.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=True,
    )
    assert rescaled.dynamic_range_decades == pytest.approx(base.dynamic_range_decades)
    assert rescaled.trace_horizontal_span_px == pytest.approx(base.trace_horizontal_span_px)
    assert rescaled.trace_vertical_span_px == pytest.approx(base.trace_vertical_span_px)
    assert rescaled.maximum_orthogonal_departure_px == pytest.approx(
        base.maximum_orthogonal_departure_px, rel=1.0e-12
    )


def test_authorization_requires_resolution_and_anchor_covariance() -> None:
    resolved = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="high_resolution",
        urbach_energy_ev=0.014,
        absorption_min_cm_inverse=100.0,
        absorption_max_cm_inverse=4000.0,
        panel_energy_span_ev=0.30,
        panel_width_px=5900.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=4780.0,
        center_uncertainty_px=1.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=True,
    )
    assert resolved.three_uncertainty_resolvable
    assert resolved.digitization_authorized
    assert resolved.decision == "digitization_authorized"

    no_uncertainty = source_conditioned_anchored_trace(
        source_identifier="controlled",
        scenario_identifier="anchor_without_covariance",
        urbach_energy_ev=0.014,
        absorption_min_cm_inverse=100.0,
        absorption_max_cm_inverse=4000.0,
        panel_energy_span_ev=0.30,
        panel_width_px=5900.0,
        panel_log_absorption_span_decades=2.0,
        panel_height_px=4780.0,
        center_uncertainty_px=1.0,
        numeric_gap_anchor_available=True,
        numeric_gap_anchor_uncertainty_available=False,
    )
    assert no_uncertainty.three_uncertainty_resolvable
    assert not no_uncertainty.digitization_authorized
    assert no_uncertainty.decision == "gap_anchor_uncertainty_missing"
