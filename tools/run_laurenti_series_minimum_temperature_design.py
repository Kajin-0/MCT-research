#!/usr/bin/env python3
"""Find the minimum temperature needed to separate Hansen and Laurenti shapes.

The observable is a within-specimen thermal shift relative to 2 K. The study is an
experiment/digitization design calculation, not a comparison with extracted observations.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from mct_research.gap_models import hansen_gap_ev, laurenti_gap_ev

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    ROOT
    / "data"
    / "validation"
    / "laurenti_series_minimum_discrimination_temperature.csv"
)
DIRECT_SERIES_X = (0.500, 0.550, 0.620, 0.710, 0.805, 0.925, 0.955, 0.970)
REFERENCE_TEMPERATURE_K = 2.0
EDGE_SIGMA_MEV = 3.0
COMPOSITION_SIGMA = 0.003
DIGITIZATION_SIGMA_MEV = (0.0, 1.0, 2.0, 3.0, 5.0)
TARGET_Z = 3.0


def thermal_shape_separation_ev(
    x: float,
    temperature_k: float,
    *,
    reference_temperature_k: float = REFERENCE_TEMPERATURE_K,
) -> float:
    """Return Laurenti-minus-Hansen within-specimen thermal shift."""

    laurenti_shift = float(laurenti_gap_ev(x, temperature_k)) - float(
        laurenti_gap_ev(x, reference_temperature_k)
    )
    hansen_shift = float(hansen_gap_ev(x, temperature_k)) - float(
        hansen_gap_ev(x, reference_temperature_k)
    )
    return laurenti_shift - hansen_shift


def separation_composition_derivative_ev_per_x(
    x: float,
    temperature_k: float,
    *,
    step: float = 1.0e-5,
) -> float:
    if not 0.0 < step < min(x, 1.0 - x):
        raise ValueError("finite-difference step must remain inside the alloy interval")
    return (
        thermal_shape_separation_ev(x + step, temperature_k)
        - thermal_shape_separation_ev(x - step, temperature_k)
    ) / (2.0 * step)


def discrimination_components(
    x: float,
    temperature_k: float,
    *,
    digitization_sigma_mev: float,
    edge_sigma_mev: float = EDGE_SIGMA_MEV,
    composition_sigma: float = COMPOSITION_SIGMA,
) -> dict[str, float]:
    if digitization_sigma_mev < 0.0 or edge_sigma_mev < 0.0:
        raise ValueError("uncertainties must be non-negative")
    if composition_sigma < 0.0:
        raise ValueError("composition_sigma must be non-negative")

    separation_mev = 1000.0 * abs(
        thermal_shape_separation_ev(x, temperature_k)
    )
    composition_component_mev = (
        1000.0
        * abs(separation_composition_derivative_ev_per_x(x, temperature_k))
        * composition_sigma
    )
    point_component_mev = np.sqrt(
        2.0 * (edge_sigma_mev**2 + digitization_sigma_mev**2)
    )
    total_sigma_mev = float(
        np.sqrt(point_component_mev**2 + composition_component_mev**2)
    )
    z_score = separation_mev / total_sigma_mev if total_sigma_mev > 0.0 else np.inf
    return {
        "separation_mev": float(separation_mev),
        "point_pair_sigma_mev": float(point_component_mev),
        "composition_sigma_mev": float(composition_component_mev),
        "total_sigma_mev": total_sigma_mev,
        "z_score": float(z_score),
    }


def minimum_discriminating_temperature_k(
    x: float,
    *,
    digitization_sigma_mev: float,
    target_z: float = TARGET_Z,
    minimum_temperature_k: int = 3,
    maximum_temperature_k: int = 300,
) -> int | None:
    if target_z <= 0.0:
        raise ValueError("target_z must be positive")
    for temperature_k in range(minimum_temperature_k, maximum_temperature_k + 1):
        components = discrimination_components(
            x,
            float(temperature_k),
            digitization_sigma_mev=digitization_sigma_mev,
        )
        if components["z_score"] >= target_z:
            return temperature_k
    return None


def run_study() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for digitization_sigma_mev in DIGITIZATION_SIGMA_MEV:
        for x in DIRECT_SERIES_X:
            threshold = minimum_discriminating_temperature_k(
                x,
                digitization_sigma_mev=digitization_sigma_mev,
            )
            at_300 = discrimination_components(
                x,
                300.0,
                digitization_sigma_mev=digitization_sigma_mev,
            )
            if threshold is None:
                threshold_components = {
                    "separation_mev": np.nan,
                    "point_pair_sigma_mev": np.nan,
                    "composition_sigma_mev": np.nan,
                    "total_sigma_mev": np.nan,
                    "z_score": np.nan,
                }
            else:
                threshold_components = discrimination_components(
                    x,
                    float(threshold),
                    digitization_sigma_mev=digitization_sigma_mev,
                )
            rows.append(
                {
                    "x": x,
                    "reference_temperature_k": REFERENCE_TEMPERATURE_K,
                    "edge_sigma_per_point_mev": EDGE_SIGMA_MEV,
                    "digitization_sigma_per_point_mev": digitization_sigma_mev,
                    "composition_sigma": COMPOSITION_SIGMA,
                    "target_z": TARGET_Z,
                    "minimum_temperature_k": (
                        "not_reached_by_300K" if threshold is None else threshold
                    ),
                    "threshold_separation_mev": threshold_components[
                        "separation_mev"
                    ],
                    "threshold_total_sigma_mev": threshold_components[
                        "total_sigma_mev"
                    ],
                    "threshold_z_score": threshold_components["z_score"],
                    "separation_at_300k_mev": at_300["separation_mev"],
                    "composition_sigma_at_300k_mev": at_300[
                        "composition_sigma_mev"
                    ],
                    "total_sigma_at_300k_mev": at_300["total_sigma_mev"],
                    "z_score_at_300k": at_300["z_score"],
                }
            )
    return rows


def main() -> None:
    rows = run_study()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"digit={float(row['digitization_sigma_per_point_mev']):g} meV "
            f"x={float(row['x']):.3f} "
            f"Tmin={row['minimum_temperature_k']} "
            f"z300={float(row['z_score_at_300k']):.2f}"
        )


if __name__ == "__main__":
    main()
