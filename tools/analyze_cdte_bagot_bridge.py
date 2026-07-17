#!/usr/bin/env python3
"""Audit the Bogucki/Bagot analytic CdTe thermal-expansion bridge."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

if __package__:
    from .analyze_cdte_browder_bridge import analyze as analyze_browder
    from .analyze_cdte_lattice_source_chain import (
        SMITH_ALPHA_1E8,
        SMITH_T_K,
        alpha_williams,
        lattice_a,
    )
else:
    from analyze_cdte_browder_bridge import analyze as analyze_browder
    from analyze_cdte_lattice_source_chain import (
        SMITH_ALPHA_1E8,
        SMITH_T_K,
        alpha_williams,
        lattice_a,
    )


def alpha_bagot_fit(temperature_k: np.ndarray | float, coefficients: list[dict]) -> np.ndarray:
    temperature = np.asarray(temperature_k, dtype=float)
    result = np.zeros_like(temperature)
    positive = temperature > 0.0
    t = temperature[positive]
    for item in coefficients:
        s = float(item["s_k"])
        g = float(item["g_reported"])
        x = s / t
        factor = np.empty_like(x)
        moderate = np.abs(x) < 50.0
        factor[moderate] = 1.0 / (4.0 * np.sinh(x[moderate] / 2.0) ** 2)
        factor[~moderate] = np.exp(-np.abs(x[~moderate]))
        result[positive] += g * (s / t) ** 2 * factor
    return result * 1.0e-8


def analyze(source_json: str | Path) -> dict[str, object]:
    source = json.loads(Path(source_json).read_text(encoding="utf-8"))
    coefficients = source["coefficients"]

    # Smith and White identify the 57.5 K and 65 K rows as literature
    # values reprinted for context rather than their direct CdTe measurements.
    direct_mask = (
        ~np.isin(SMITH_T_K, np.asarray([57.5, 65.0]))
        & (SMITH_T_K >= 2.0)
        & (SMITH_T_K <= 283.0)
    )
    direct_t = SMITH_T_K[direct_mask]
    direct_alpha = SMITH_ALPHA_1E8[direct_mask] * 1.0e-8
    fitted_direct = alpha_bagot_fit(direct_t, coefficients)
    direct_difference = fitted_direct - direct_alpha

    grid = np.linspace(0.0, 293.15, 200001)
    integral = float(np.trapezoid(alpha_bagot_fit(grid, coefficients), grid))
    anchor = float(lattice_a(20.0))
    a0 = anchor * math.exp(-integral)

    alpha_283 = float(alpha_bagot_fit(283.0, coefficients))
    alpha_293 = float(alpha_bagot_fit(293.15, coefficients))
    smith_283 = float(
        SMITH_ALPHA_1E8[SMITH_T_K == 283.0][0] * 1.0e-8
    )
    williams_293 = float(alpha_williams(20.0))
    browder = analyze_browder()
    browder_adjusted_a0 = float(browder["adjusted_bridge"]["a0_a"])
    previous_linear_a0 = 6.477028

    spread = abs(a0 - browder_adjusted_a0)
    midpoint = 0.5 * (a0 + browder_adjusted_a0)
    anchor_bound = 0.000579
    conservative_bound = anchor_bound + 0.5 * spread
    lattice_fraction = conservative_bound / midpoint
    volume_fraction = 3.0 * lattice_fraction

    result = {
        "schema_version": "1.0",
        "status": "secondary_bagot_bridge_diagnostic_not_execution_authorized",
        "source": source["source"],
        "underlying_primary_source": source["underlying_cdte_data_source"],
        "formula": source["formula"],
        "coefficients": coefficients,
        "smith_white_direct_overlap": {
            "row_count": int(direct_t.size),
            "temperature_range_k": [float(direct_t.min()), float(direct_t.max())],
            "rms_alpha_difference_1e6_per_k": float(
                np.sqrt(np.mean(direct_difference**2)) * 1.0e6
            ),
            "maximum_absolute_alpha_difference_1e6_per_k": float(
                np.max(np.abs(direct_difference)) * 1.0e6
            ),
            "bagot_fit_alpha_283_1e6_per_k": alpha_283 * 1.0e6,
            "smith_white_alpha_283_1e6_per_k": smith_283 * 1.0e6,
        },
        "williams_anchor_cross_check": {
            "bagot_fit_alpha_293_15_1e6_per_k": alpha_293 * 1.0e6,
            "williams_alpha_293_15_1e6_per_k": williams_293 * 1.0e6,
            "difference_1e6_per_k": (alpha_293 - williams_293) * 1.0e6,
        },
        "zero_temperature_diagnostic": {
            "integral_0_293_15": integral,
            "williams_anchor_angstrom": anchor,
            "a0_angstrom": a0,
            "adjusted_browder_a0_angstrom": browder_adjusted_a0,
            "bagot_minus_browder_angstrom": a0 - browder_adjusted_a0,
            "previous_linear_bridge_a0_angstrom": previous_linear_a0,
            "bagot_minus_previous_linear_angstrom": a0 - previous_linear_a0,
        },
        "two_model_planning_envelope": {
            "midpoint_angstrom": midpoint,
            "model_half_spread_angstrom": 0.5 * spread,
            "williams_anchor_bound_angstrom": anchor_bound,
            "conservative_sum_bound_angstrom": conservative_bound,
            "conservative_lattice_fraction": lattice_fraction,
            "first_order_volume_fraction": volume_fraction,
            "fraction_of_half_percent_volume_bracket": volume_fraction / 0.005,
            "authorization": "sensitivity_diagnostic_only",
        },
        "decision": {
            "bridge_plausibility_supported": True,
            "execution_bridge_authorized": False,
            "reason": (
                "The secondary Bagot fit agrees closely with direct Smith-White data "
                "and with the morphology-adjusted Browder bridge, but the underlying "
                "primary Bagot article and measurement uncertainty are not acquired. "
                "The two-model envelope is suitable for A0 sensitivity planning, not "
                "for execution provenance."
            ),
            "next_gate": (
                "Acquire and hash Bagot 1993 or Greenough-Palmer 1973. Prefer the "
                "single-crystal Greenough curve for morphology-consistent execution; "
                "use Bagot primary data as an independent full-range cross-check."
            ),
        },
        "claim_boundary": source["claim_boundary"],
    }

    if not (6.4762 < a0 < 6.4767):
        raise RuntimeError("unexpected Bagot bridge a0")
    if result["smith_white_direct_overlap"]["rms_alpha_difference_1e6_per_k"] > 0.3:
        raise RuntimeError("Bagot fit does not reproduce Smith-White adequately")
    if result["decision"]["execution_bridge_authorized"]:
        raise RuntimeError("secondary bridge must remain fail closed")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-json",
        default="data/cdte_lattice/bogucki2022_bagot_cdte_expansion_fit.json",
    )
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.source_json)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output_json:
        Path(args.output_json).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
