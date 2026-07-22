"""Build the controlled R03 published-tail recoverability validation record."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from math import log10
from pathlib import Path
from typing import Any

from mct_research.published_tail_recoverability import (
    gaussian_power_tail_window_straightness,
    source_conditioned_finkman_trace,
)


REFERENCE_DECIMAL_PLACES = 12


def _stable_reference_value(value: Any) -> Any:
    """Quantize floating outputs above platform-level LAPACK variation."""

    if isinstance(value, float):
        return round(value, REFERENCE_DECIMAL_PLACES)
    if isinstance(value, dict):
        return {key: _stable_reference_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_stable_reference_value(item) for item in value]
    return value


def _straightness_case(upper_z: float) -> dict[str, float]:
    kwargs: dict[str, float] = {}
    if upper_z <= -8.0:
        kwargs["standard_deviation_limit"] = 12.0
    result = gaussian_power_tail_window_straightness(
        upper_z,
        log10(1000.0 / 5.0),
        sample_count=161,
        quadrature_order=256,
        **kwargs,
    )
    return {
        "upper_standardized_energy": result.upper_standardized_energy,
        "lower_standardized_energy": result.lower_standardized_energy,
        "maximum_vertical_residual_decades": (
            result.maximum_vertical_residual_decades
        ),
        "rms_vertical_residual_decades": result.rms_vertical_residual_decades,
        "maximum_horizontal_residual_fraction": (
            result.maximum_horizontal_residual_fraction
        ),
        "rms_horizontal_residual_fraction": result.rms_horizontal_residual_fraction,
    }


def _source_cases() -> list[dict[str, object]]:
    definitions = [
        {
            "source_identifier": "finkman_schacham_1984_fig4_85k",
            "composition": 0.29,
            "temperature_k": 85.0,
            "absorption_min_cm_inverse": 5.0,
            "absorption_max_cm_inverse": 1000.0,
            "panel_energy_min_ev": 0.20,
            "panel_energy_max_ev": 0.30,
            "panel_width_px": 545.0,
            "panel_absorption_min_cm_inverse": 5.0,
            "panel_absorption_max_cm_inverse": 1000.0,
            "panel_height_px": 562.0,
        },
        {
            "source_identifier": "finkman_schacham_1984_fig4_300k",
            "composition": 0.29,
            "temperature_k": 300.0,
            "absorption_min_cm_inverse": 5.0,
            "absorption_max_cm_inverse": 1000.0,
            "panel_energy_min_ev": 0.20,
            "panel_energy_max_ev": 0.30,
            "panel_width_px": 545.0,
            "panel_absorption_min_cm_inverse": 5.0,
            "panel_absorption_max_cm_inverse": 1000.0,
            "panel_height_px": 562.0,
        },
        {
            "source_identifier": "finkman_nemirovsky_1979_fig3_80k",
            "composition": 0.205,
            "temperature_k": 80.0,
            "absorption_min_cm_inverse": 20.0,
            "absorption_max_cm_inverse": 1000.0,
            "panel_energy_min_ev": 0.08,
            "panel_energy_max_ev": 0.18,
            "panel_width_px": 848.0,
            "panel_absorption_min_cm_inverse": 5.0,
            "panel_absorption_max_cm_inverse": 2000.0,
            "panel_height_px": 982.0,
        },
        {
            "source_identifier": "finkman_nemirovsky_1979_fig3_300k",
            "composition": 0.205,
            "temperature_k": 300.0,
            "absorption_min_cm_inverse": 20.0,
            "absorption_max_cm_inverse": 1000.0,
            "panel_energy_min_ev": 0.08,
            "panel_energy_max_ev": 0.18,
            "panel_width_px": 848.0,
            "panel_absorption_min_cm_inverse": 5.0,
            "panel_absorption_max_cm_inverse": 2000.0,
            "panel_height_px": 982.0,
        },
    ]
    cases: list[dict[str, object]] = []
    for definition in definitions:
        result = source_conditioned_finkman_trace(
            **definition,
            marker_center_uncertainty_px=6.0,
            sample_count=161,
            quadrature_order=256,
        )
        cases.append(asdict(result))
    return cases


def build_reference() -> dict[str, object]:
    """Return the immutable source-conditioned recoverability record."""

    record = {
        "schema_version": "1.0",
        "portfolio_contribution": "R03",
        "issue": 235,
        "status": (
            "source_conditioned_published_figure_recoverability_"
            "not_material_validation"
        ),
        "numerical_precision": {
            "decimal_places": REFERENCE_DECIMAL_PLACES,
            "reason": "exclude platform-level SVD and least-squares roundoff",
        },
        "model": {
            "absorption": "alpha_p(E)=A*sigma_G^p*F_p(z)",
            "standardized_energy": "z=(E-mu_G)/sigma_G",
            "dynamic_range": "R=log10(alpha_max/alpha_min)",
            "figure_residual": (
                "maximum total-least-squares orthogonal departure in "
                "audit-render pixels"
            ),
        },
        "finite_window_result": {
            "statement": (
                "for fixed finite R, best-straight-line residual tends to zero "
                "as z_upper tends to minus infinity"
            ),
            "asymptotic_scaling": "O(abs(z_upper)^-2)",
            "consequence": (
                "tail straightness alone cannot falsify the Gaussian-power "
                "model without an independent gap-location or "
                "intrinsic-amplitude constraint"
            ),
            "finkman_1984_dynamic_range_decades": log10(1000.0 / 5.0),
            "straightness_grid": [
                _straightness_case(value) for value in (0.0, -2.0, -4.0, -6.0, -8.0)
            ],
        },
        "source_panel_assumptions": {
            "render_dpi": 300,
            "marker_center_uncertainty_scenario_px": 6.0,
            "finkman_1984_fig4": {
                "energy_range_ev": [0.2, 0.3],
                "panel_width_px": 545.0,
                "absorption_range_cm_inverse": [5.0, 1000.0],
                "panel_height_px": 562.0,
            },
            "finkman_1979_fig3": {
                "energy_range_ev": [0.08, 0.18],
                "panel_width_px": 848.0,
                "absorption_range_cm_inverse": [5.0, 2000.0],
                "panel_height_px": 982.0,
                "fitted_absorption_range_cm_inverse": [20.0, 1000.0],
            },
        },
        "source_conditioned_traces": _source_cases(),
        "decision": {
            "manual_digitization_authorized": False,
            "reason": (
                "no independent standardized window-location anchor is available; "
                "low-temperature traces fail the conservative three-sigma panel "
                "gate even at z_upper=0, while high-temperature traces require "
                "the upper window to lie within about 0.72 sigma_G below the "
                "latent mean gap for a six-pixel three-sigma threshold"
            ),
            "next_required_evidence": (
                "independent above-gap or mean-gap anchor with uncertainty, or "
                "numerical source data with measurement covariance"
            ),
        },
        "claim_boundaries": [
            (
                "panel pixels and marker-center uncertainty are declared audit "
                "scenarios, not source measurement covariance"
            ),
            (
                "modified-Urbach trace spans are source-conditioned empirical "
                "slopes, not Gaussian-disorder parameters"
            ),
            "negative logarithmic curvature does not identify composition disorder",
            "Ariel 1995 d2(alpha)/dE2 is not d2(log(alpha))/dE2",
            (
                "no manuscript or material-validation claim follows from "
                "synthetic recoverability"
            ),
        ],
    }
    return _stable_reference_value(record)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/validation/published_tail_curvature_recoverability.json"),
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build_reference(), indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
