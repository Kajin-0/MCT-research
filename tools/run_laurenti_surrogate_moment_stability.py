#!/usr/bin/env python3
"""Test thermal-moment stability in the two-scale Laurenti surrogate study.

The target is the Laurenti published equation, not experimental observations. The study
asks whether combinations of fitted oscillator amplitudes and temperatures are more stable
than the selected oscillator temperatures themselves.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from tools.run_laurenti_surrogate_compression import (
    make_surrogate_data,
    select_on_training_data,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    ROOT
    / "data"
    / "validation"
    / "laurenti_surrogate_thermal_moment_stability.csv"
)
EVALUATION_COMPOSITIONS = np.array([0.0, 0.2, 0.5, 0.8, 1.0])


def laurenti_high_temperature_slope_ev_per_k(x: float) -> float:
    """Return the exact high-temperature slope of Laurenti's thermal term."""

    amplitude = 6.3 - 15.47 * x + 5.92 * x**2
    return 1.0e-4 * amplitude


def oscillator_amplitude_coefficients(fit) -> np.ndarray:
    """Return one polynomial coefficient row per oscillator."""

    specification = fit.specification
    degree_count = specification.amplitude_degree + 1
    offset = specification.static_degree + 1
    rows = []
    for _ in specification.oscillator_temperatures_k:
        rows.append(fit.coefficients[offset : offset + degree_count])
        offset += degree_count
    return np.asarray(rows, dtype=float)


def evaluate_amplitudes(coefficients: np.ndarray, x: float) -> np.ndarray:
    powers = x ** np.arange(coefficients.shape[1], dtype=float)
    return coefficients @ powers


def run_study() -> list[dict[str, float | str]]:
    data = make_surrogate_data()
    holdouts = {
        "low_T_le_40K": data.temperature_k <= 40.0,
        "mid_40K_to_200K": (data.temperature_k > 40.0)
        & (data.temperature_k <= 200.0),
        "high_T_gt_200K": data.temperature_k > 200.0,
    }

    rows: list[dict[str, float | str]] = []
    for fold_name, holdout in holdouts.items():
        selected = select_on_training_data(data.subset(~holdout), 2)
        training_rmse, training_max, condition, scales, fit = selected
        amplitude_coefficients = oscillator_amplitude_coefficients(fit)
        theta = np.asarray(scales, dtype=float)

        for composition in EVALUATION_COMPOSITIONS:
            amplitudes = evaluate_amplitudes(amplitude_coefficients, float(composition))
            mu_minus_one = float(np.sum(amplitudes / theta))
            mu_zero = float(np.sum(amplitudes))
            mu_one = float(np.sum(amplitudes * theta))
            high_temperature_slope = 2.0 * mu_minus_one
            target_slope = laurenti_high_temperature_slope_ev_per_k(
                float(composition)
            )
            rows.append(
                {
                    "fold": fold_name,
                    "theta_1_k": float(theta[0]),
                    "theta_2_k": float(theta[1]),
                    "training_rmse_mev": float(training_rmse),
                    "training_max_abs_mev": float(training_max),
                    "training_condition_number": float(condition),
                    "x": float(composition),
                    "amplitude_1_ev": float(amplitudes[0]),
                    "amplitude_2_ev": float(amplitudes[1]),
                    "mu_minus_one_ev_per_k": mu_minus_one,
                    "mu_zero_ev": mu_zero,
                    "mu_one_ev_k": mu_one,
                    "high_temperature_slope_mev_per_k": 1000.0
                    * high_temperature_slope,
                    "laurenti_target_slope_mev_per_k": 1000.0 * target_slope,
                    "slope_error_mev_per_k": 1000.0
                    * (high_temperature_slope - target_slope),
                    "high_temperature_constant_mev": -1000.0 * mu_zero,
                    "inverse_temperature_coefficient_mev_k": 1000.0
                    * mu_one
                    / 6.0,
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
            f"{row['fold']:18s} x={row['x']:.1f} "
            f"theta=({row['theta_1_k']:.0f},{row['theta_2_k']:.0f}) K "
            f"slope={row['high_temperature_slope_mev_per_k']:.6f} meV/K "
            f"target={row['laurenti_target_slope_mev_per_k']:.6f} meV/K"
        )


if __name__ == "__main__":
    main()
