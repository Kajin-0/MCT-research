#!/usr/bin/env python3
"""Use Browder 1972 as a morphology-limited CdTe expansion bridge.

The official publisher HTML Table I is primary experimental data for hot-pressed
microcrystalline CdTe (Irtran 6), not single-crystal CdTe. Results from this
script are sensitivity diagnostics and cannot close the CdTe execution gate.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from tools.analyze_cdte_lattice_source_chain import (
    SMITH_ALPHA_1E8,
    SMITH_T_K,
    alpha_williams,
    lattice_a,
)

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "experimental"
    / "browder1972_cdte_irtran6_alpha.csv"
)


def load_browder() -> tuple[np.ndarray, np.ndarray]:
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    temperature = np.asarray([float(row["temperature_k"]) for row in rows])
    alpha = np.asarray([float(row["alpha_1e6_per_k"]) for row in rows]) * 1.0e-6
    return temperature, alpha


def integrate(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.trapezoid(y, x))


def smith_integral_to(stop_k: float) -> float:
    low_zero_to_two = -170.0e-12 * 2.0**4 / 4.0
    mask = SMITH_T_K <= stop_k
    return low_zero_to_two + integrate(SMITH_T_K[mask], SMITH_ALPHA_1E8[mask] * 1.0e-8)


def grid_with_endpoints(
    source_temperature: np.ndarray,
    start_k: float,
    stop_k: float,
) -> np.ndarray:
    internal = source_temperature[
        (source_temperature > start_k) & (source_temperature < stop_k)
    ]
    return np.unique(np.concatenate(([start_k], internal, [stop_k])))


def analyze() -> dict[str, object]:
    browder_t, browder_alpha = load_browder()
    anchor_temperature_k = 293.15
    anchor_a = float(lattice_a(20.0))
    williams_alpha = float(alpha_williams(20.0))

    full_grid = grid_with_endpoints(browder_t, 10.0, anchor_temperature_k)
    full_alpha = np.interp(full_grid, browder_t, browder_alpha)
    full_integral = smith_integral_to(10.0) + integrate(full_grid, full_alpha)
    full_a0 = anchor_a * math.exp(-full_integral)

    hybrid_grid = grid_with_endpoints(browder_t, 85.0, anchor_temperature_k)
    hybrid_alpha = np.interp(hybrid_grid, browder_t, browder_alpha)
    smith_to_85 = smith_integral_to(85.0)
    hybrid_integral = smith_to_85 + integrate(hybrid_grid, hybrid_alpha)
    hybrid_a0 = anchor_a * math.exp(-hybrid_integral)

    smith_alpha_85 = float(
        SMITH_ALPHA_1E8[np.where(SMITH_T_K == 85.0)[0][0]] * 1.0e-8
    )
    browder_alpha_85 = float(np.interp(85.0, browder_t, browder_alpha))
    browder_alpha_anchor = float(
        np.interp(anchor_temperature_k, browder_t, browder_alpha)
    )
    correction_85 = smith_alpha_85 - browder_alpha_85
    correction_anchor = williams_alpha - browder_alpha_anchor
    correction = correction_85 + (
        (correction_anchor - correction_85)
        * (hybrid_grid - 85.0)
        / (anchor_temperature_k - 85.0)
    )
    adjusted_integral = smith_to_85 + integrate(
        hybrid_grid, hybrid_alpha + correction
    )
    adjusted_a0 = anchor_a * math.exp(-adjusted_integral)

    overlap_t = np.asarray([10.0, 15.0, 20.0, 30.0, 75.0, 85.0, 283.0])
    smith_overlap = np.asarray(
        [
            SMITH_ALPHA_1E8[np.where(SMITH_T_K == value)[0][0]] * 1.0e-8
            for value in overlap_t
        ]
    )
    browder_overlap = np.interp(overlap_t, browder_t, browder_alpha)
    overlap_delta = browder_overlap - smith_overlap

    linear_bridge_integral = smith_to_85
    alpha_283 = float(
        SMITH_ALPHA_1E8[np.where(SMITH_T_K == 283.0)[0][0]] * 1.0e-8
    )
    linear_bridge_integral += 0.5 * (smith_alpha_85 + alpha_283) * (283.0 - 85.0)
    linear_bridge_integral += 0.5 * (alpha_283 + williams_alpha) * (
        anchor_temperature_k - 283.0
    )
    linear_bridge_a0 = anchor_a * math.exp(-linear_bridge_integral)

    table_rounding_alpha = 0.005e-6
    rounding_a_bound = anchor_a * table_rounding_alpha * (
        anchor_temperature_k - 10.0
    )

    if len(browder_t) != 25:
        raise RuntimeError("Browder Table I transcription must contain 25 CdTe rows")
    if not np.all(np.diff(browder_t) > 0.0):
        raise RuntimeError("Browder temperatures are not strictly increasing")
    if abs(adjusted_a0 - hybrid_a0) > 0.0002:
        raise RuntimeError("endpoint adjustment unexpectedly large")
    if np.max(np.abs(overlap_delta)) < 0.8e-6:
        raise RuntimeError("morphology/source discrepancy was not detected")

    return {
        "status": "morphology_limited_bridge_sensitivity_only",
        "source": {
            "citation": "Browder and Ballard, Applied Optics 11, 841-843 (1972)",
            "doi": "10.1364/AO.11.000841",
            "source_location": "official Optica HTML Table I",
            "material": "microcrystalline hot-pressed CdTe Irtran 6",
            "method": "three-terminal capacitance-type dilatometer",
            "temperature_range_k": [10.0, 300.0],
            "row_count": int(len(browder_t)),
        },
        "overlap_with_smith_white_single_crystal": {
            "temperatures_k": overlap_t.tolist(),
            "browder_minus_smith_alpha_1e6_per_k": (
                overlap_delta * 1.0e6
            ).tolist(),
            "rms_difference_1e6_per_k": float(
                np.sqrt(np.mean(overlap_delta**2)) * 1.0e6
            ),
            "maximum_absolute_difference_1e6_per_k": float(
                np.max(np.abs(overlap_delta)) * 1.0e6
            ),
            "difference_at_283k_1e6_per_k": float(overlap_delta[-1] * 1.0e6),
        },
        "zero_k_sensitivity": {
            "williams_anchor_a_at_293_15_k": anchor_a,
            "smith_below_10_then_browder_a0_a": full_a0,
            "smith_through_85_then_browder_a0_a": hybrid_a0,
            "endpoint_adjusted_browder_shape_a0_a": adjusted_a0,
            "linear_bridge_previous_a0_a": linear_bridge_a0,
            "adjusted_shape_minus_linear_bridge_a": adjusted_a0
            - linear_bridge_a0,
            "table_rounding_only_a_bound": rounding_a_bound,
        },
        "decision": (
            "Browder Table I removes the unconstrained numerical bridge but transfers "
            "a microcrystalline Irtran-6 curve into a single-crystal problem. It is an "
            "informative shape sensitivity test, not a validated geometry input. Keep "
            "ready_for_execution false until the Greenough-Palmer single-crystal curve "
            "or an equivalent primary 90-293 K dataset is acquired."
        ),
    }


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
