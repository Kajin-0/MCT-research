"""Source-conditioned validation gates for anchored published absorption tails.

This module composes the finite-window pixel-space diagnostic from
``published_tail_recoverability`` with a source-reported Urbach energy and an
independent-gap-anchor status. It is a publication-figure recoverability tool,
not a specimen-disorder inversion.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, log10

from .published_tail_recoverability import (
    critical_upper_standardized_energy,
    gaussian_power_tail_pixel_recoverability,
)


@dataclass(frozen=True)
class AnchoredTailTrace:
    """Recoverability result for one source-conditioned absorption trace."""

    source_identifier: str
    scenario_identifier: str
    urbach_energy_ev: float
    absorption_min_cm_inverse: float
    absorption_max_cm_inverse: float
    dynamic_range_decades: float
    trace_energy_span_ev: float
    panel_energy_span_ev: float
    panel_width_px: float
    trace_horizontal_span_px: float
    panel_log_absorption_span_decades: float
    panel_height_px: float
    trace_vertical_span_px: float
    upper_standardized_energy: float
    maximum_orthogonal_departure_px: float
    rms_orthogonal_departure_px: float
    center_uncertainty_px: float
    departure_to_uncertainty_ratio: float
    one_uncertainty_resolvable: bool
    three_uncertainty_resolvable: bool
    critical_upper_z_one_uncertainty: float | None
    critical_upper_z_three_uncertainty: float | None
    numeric_gap_anchor_available: bool
    numeric_gap_anchor_uncertainty_available: bool
    digitization_authorized: bool
    decision: str


def _finite_positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def urbach_trace_energy_span_ev(
    urbach_energy_ev: float,
    absorption_min_cm_inverse: float,
    absorption_max_cm_inverse: float,
) -> float:
    """Return ``Delta E = W ln(alpha_max/alpha_min)`` in electronvolts."""
    width = _finite_positive("urbach_energy_ev", urbach_energy_ev)
    lower = _finite_positive("absorption_min_cm_inverse", absorption_min_cm_inverse)
    upper = _finite_positive("absorption_max_cm_inverse", absorption_max_cm_inverse)
    if upper <= lower:
        raise ValueError("absorption_max_cm_inverse must exceed the minimum")
    return width * log(upper / lower)


def source_conditioned_anchored_trace(
    *,
    source_identifier: str,
    scenario_identifier: str,
    urbach_energy_ev: float,
    absorption_min_cm_inverse: float,
    absorption_max_cm_inverse: float,
    panel_energy_span_ev: float,
    panel_width_px: float,
    panel_log_absorption_span_decades: float,
    panel_height_px: float,
    center_uncertainty_px: float,
    numeric_gap_anchor_available: bool,
    numeric_gap_anchor_uncertainty_available: bool,
    upper_standardized_energy: float = 0.0,
    exponent: float = 0.5,
    sample_count: int = 401,
    quadrature_order: int = 256,
    standard_deviation_limit: float = 10.0,
) -> AnchoredTailTrace:
    """Evaluate one declared source trace and issue a pre-digitization decision.

    ``urbach_energy_ev`` only maps a source-reported exponential interval into
    horizontal plot pixels. It is not identified with ``sigma_G``.
    """
    lower_alpha = _finite_positive(
        "absorption_min_cm_inverse", absorption_min_cm_inverse
    )
    upper_alpha = _finite_positive(
        "absorption_max_cm_inverse", absorption_max_cm_inverse
    )
    if upper_alpha <= lower_alpha:
        raise ValueError("absorption_max_cm_inverse must exceed the minimum")
    energy_span = _finite_positive("panel_energy_span_ev", panel_energy_span_ev)
    width_px = _finite_positive("panel_width_px", panel_width_px)
    panel_decades = _finite_positive(
        "panel_log_absorption_span_decades", panel_log_absorption_span_decades
    )
    height_px = _finite_positive("panel_height_px", panel_height_px)
    uncertainty = _finite_positive("center_uncertainty_px", center_uncertainty_px)
    upper_z = float(upper_standardized_energy)
    if not isfinite(upper_z) or upper_z > 0.0:
        raise ValueError("upper_standardized_energy must be finite and <= 0")

    dynamic_range = log10(upper_alpha / lower_alpha)
    trace_energy_span = urbach_trace_energy_span_ev(
        urbach_energy_ev,
        lower_alpha,
        upper_alpha,
    )
    horizontal_span = width_px * trace_energy_span / energy_span
    vertical_span = height_px * dynamic_range / panel_decades
    recovery = gaussian_power_tail_pixel_recoverability(
        upper_z,
        dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    critical_one = critical_upper_standardized_energy(
        dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        significance=1.0,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    critical_three = critical_upper_standardized_energy(
        dynamic_range,
        horizontal_span,
        vertical_span,
        uncertainty,
        significance=3.0,
        exponent=exponent,
        sample_count=sample_count,
        quadrature_order=quadrature_order,
        standard_deviation_limit=standard_deviation_limit,
    )
    anchor_value = bool(numeric_gap_anchor_available)
    anchor_uncertainty = bool(numeric_gap_anchor_uncertainty_available)
    authorized = bool(
        recovery.three_sigma_resolvable and anchor_value and anchor_uncertainty
    )
    if authorized:
        decision = "digitization_authorized"
    elif not recovery.three_sigma_resolvable:
        decision = "figure_resolution_limited"
    elif not anchor_value:
        decision = "numeric_gap_anchor_missing"
    else:
        decision = "gap_anchor_uncertainty_missing"

    return AnchoredTailTrace(
        source_identifier=str(source_identifier),
        scenario_identifier=str(scenario_identifier),
        urbach_energy_ev=float(urbach_energy_ev),
        absorption_min_cm_inverse=lower_alpha,
        absorption_max_cm_inverse=upper_alpha,
        dynamic_range_decades=dynamic_range,
        trace_energy_span_ev=trace_energy_span,
        panel_energy_span_ev=energy_span,
        panel_width_px=width_px,
        trace_horizontal_span_px=horizontal_span,
        panel_log_absorption_span_decades=panel_decades,
        panel_height_px=height_px,
        trace_vertical_span_px=vertical_span,
        upper_standardized_energy=upper_z,
        maximum_orthogonal_departure_px=recovery.maximum_orthogonal_departure_px,
        rms_orthogonal_departure_px=recovery.rms_orthogonal_departure_px,
        center_uncertainty_px=uncertainty,
        departure_to_uncertainty_ratio=recovery.departure_to_uncertainty_ratio,
        one_uncertainty_resolvable=recovery.one_sigma_resolvable,
        three_uncertainty_resolvable=recovery.three_sigma_resolvable,
        critical_upper_z_one_uncertainty=critical_one,
        critical_upper_z_three_uncertainty=critical_three,
        numeric_gap_anchor_available=anchor_value,
        numeric_gap_anchor_uncertainty_available=anchor_uncertainty,
        digitization_authorized=authorized,
        decision=decision,
    )


def chang_reference_traces() -> tuple[AnchoredTailTrace, ...]:
    """Return the four declared Chang 2004/2006 audit scenarios."""
    common = {
        "urbach_energy_ev": 0.014,
        "center_uncertainty_px": 6.0,
        "numeric_gap_anchor_available": False,
        "numeric_gap_anchor_uncertainty_available": False,
        "upper_standardized_energy": 0.0,
    }
    return (
        source_conditioned_anchored_trace(
            source_identifier="Chang et al. 2004 Figure 2(c)",
            scenario_identifier="optimistic_broad_tail",
            absorption_min_cm_inverse=100.0,
            absorption_max_cm_inverse=4000.0,
            panel_energy_span_ev=0.30,
            panel_width_px=590.0,
            panel_log_absorption_span_decades=2.0,
            panel_height_px=478.0,
            **common,
        ),
        source_conditioned_anchored_trace(
            source_identifier="Chang et al. 2004 Figure 2(c)",
            scenario_identifier="representative_tail",
            absorption_min_cm_inverse=100.0,
            absorption_max_cm_inverse=1000.0,
            panel_energy_span_ev=0.30,
            panel_width_px=590.0,
            panel_log_absorption_span_decades=2.0,
            panel_height_px=478.0,
            **common,
        ),
        source_conditioned_anchored_trace(
            source_identifier="Chang et al. 2006 Figure 2",
            scenario_identifier="optimistic_broad_tail",
            absorption_min_cm_inverse=200.0,
            absorption_max_cm_inverse=4000.0,
            panel_energy_span_ev=0.50,
            panel_width_px=649.0,
            panel_log_absorption_span_decades=2.0,
            panel_height_px=520.0,
            **common,
        ),
        source_conditioned_anchored_trace(
            source_identifier="Chang et al. 2006 Figure 2",
            scenario_identifier="representative_tail",
            absorption_min_cm_inverse=200.0,
            absorption_max_cm_inverse=2000.0,
            panel_energy_span_ev=0.50,
            panel_width_px=649.0,
            panel_log_absorption_span_decades=2.0,
            panel_height_px=520.0,
            **common,
        ),
    )
