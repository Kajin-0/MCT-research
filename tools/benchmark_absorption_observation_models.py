#!/usr/bin/env python3
"""Benchmark HgCdTe edge bias caused by observation-model choices.

This is a formula-level synthetic benchmark. It does not fit or diagnose a
specific specimen. The reference scenarios use the repository's provisional gap
only to define a latent edge around which published absorption-model structures
are compared.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.gap_models import provisional_hansen_pade_gap_ev

SCENARIOS = ((0.21, 80.0), (0.31, 80.0), (0.21, 300.0), (0.31, 300.0))
THRESHOLDS_CM1 = (600.0, 1000.0, 1200.0, 1500.0, 2000.0)
FIT_MIN_CM1 = 600.0
FIT_MAX_CM1 = 5000.0


def moazzami_parameters(composition_x: float, temperature_k: float) -> tuple[float, float]:
    """Return the published Moazzami 2005 K and n coefficients."""

    x = float(composition_x)
    t = float(temperature_k)
    coefficient_k = (
        -20060.0
        + 115750.0 * x
        + 32.43 * t
        - 64170.0 * x**2
        + 0.43231 * t**2
        - 101.92 * x * t
    )
    exponent_n = 0.74487 - 0.44513 * x + (0.000799 - 0.000757 * x) * t
    if coefficient_k <= 0.0 or exponent_n <= 0.0:
        raise ValueError("scenario lies outside the positive Moazzami parameter domain")
    return coefficient_k, exponent_n


def moazzami_absorption_cm1(
    energy_ev: np.ndarray,
    composition_x: float,
    temperature_k: float,
    gap_ev: float,
) -> np.ndarray:
    """Return the published fractional-power above-gap form in cm^-1."""

    energy = np.asarray(energy_ev, dtype=float)
    coefficient_k, exponent_n = moazzami_parameters(composition_x, temperature_k)
    excess = np.maximum(energy - float(gap_ev), 0.0)
    return coefficient_k * excess**exponent_n / energy


def chang_inspired_absorption_cm1(
    energy_ev: np.ndarray,
    gap_ev: float,
    *,
    nonparabolic_scale_ev: float = 0.103,
    urbach_energy_ev: float = 0.006,
    edge_absorption_cm1: float = 400.0,
    target_absorption_cm1: float = 4000.0,
    target_excess_energy_ev: float = 0.100,
) -> np.ndarray:
    """Return a smooth Urbach plus hyperbolic nonparabolic reference curve.

    The structure is source-inspired rather than a coefficient reproduction of a
    specific sample. The intrinsic part combines heavy- and light-hole-like
    hyperbolic terms, then is normalized at one declared excess energy.
    """

    energy = np.asarray(energy_ev, dtype=float)
    gap = float(gap_ev)
    scale = float(nonparabolic_scale_ev)
    excess = np.maximum(energy - gap, 0.0)

    heavy = (excess + scale) * np.sqrt(
        np.maximum((excess + scale) ** 2 - scale**2, 0.0)
    )
    split_scale = 2.0 * scale
    light = 0.125 * (excess + split_scale) * np.sqrt(
        np.maximum((excess + split_scale) ** 2 - split_scale**2, 0.0)
    )
    raw_intrinsic = (heavy + light) / energy

    target_excess = float(target_excess_energy_ev)
    target_energy = gap + target_excess
    target_heavy = (target_excess + scale) * np.sqrt(
        (target_excess + scale) ** 2 - scale**2
    )
    target_light = 0.125 * (target_excess + split_scale) * np.sqrt(
        (target_excess + split_scale) ** 2 - split_scale**2
    )
    target_raw = (target_heavy + target_light) / target_energy
    intrinsic = float(target_absorption_cm1) * raw_intrinsic / target_raw

    urbach = float(edge_absorption_cm1) * np.exp(
        np.clip((energy - gap) / float(urbach_energy_ev), -50.0, 50.0)
    )
    blend = 1.0 / (
        1.0 + np.exp(np.clip(-(energy - gap) / 0.0005, -50.0, 50.0))
    )
    return (1.0 - blend) * urbach + blend * (
        float(edge_absorption_cm1) + intrinsic
    )


def threshold_edge_ev(
    energy_ev: np.ndarray, absorption_cm1: np.ndarray, threshold_cm1: float
) -> float:
    """Interpolate the first energy at which absorption reaches a threshold."""

    energy = np.asarray(energy_ev, dtype=float)
    absorption = np.asarray(absorption_cm1, dtype=float)
    indices = np.flatnonzero(absorption >= float(threshold_cm1))
    if indices.size == 0:
        raise ValueError("threshold is not crossed")
    index = int(indices[0])
    if index == 0:
        return float(energy[0])
    e0, e1 = energy[index - 1], energy[index]
    a0, a1 = absorption[index - 1], absorption[index]
    fraction = (float(threshold_cm1) - a0) / (a1 - a0)
    return float(e0 + fraction * (e1 - e0))


def fit_fractional_power_edge(
    energy_ev: np.ndarray,
    absorption_cm1: np.ndarray,
    *,
    edge_bounds_ev: tuple[float, float],
    fixed_exponent: float | None = None,
    grid_points: int = 4001,
) -> dict[str, float]:
    """Fit alpha=A*(E-Eg)^p/E by deterministic edge grid search."""

    energy = np.asarray(energy_ev, dtype=float)
    absorption = np.asarray(absorption_cm1, dtype=float)
    if energy.size < 3 or energy.shape != absorption.shape:
        raise ValueError("fit arrays must have equal length and at least three points")
    if np.any(absorption <= 0.0):
        raise ValueError("fit absorption must be positive")

    target = np.log(absorption * energy)
    best: tuple[float, float, float, float] | None = None
    for edge in np.linspace(edge_bounds_ev[0], edge_bounds_ev[1], grid_points):
        excess = energy - edge
        if np.any(excess <= 0.0):
            continue
        predictor = np.log(excess)
        if fixed_exponent is None:
            design = np.column_stack((np.ones_like(predictor), predictor))
            log_amplitude, exponent = np.linalg.lstsq(design, target, rcond=None)[0]
            if not 0.2 <= exponent <= 1.5:
                continue
        else:
            exponent = float(fixed_exponent)
            log_amplitude = float(np.mean(target - exponent * predictor))
        predicted = log_amplitude + exponent * predictor
        mean_square = float(np.mean((target - predicted) ** 2))
        if best is None or mean_square < best[0]:
            best = (mean_square, float(edge), float(np.exp(log_amplitude)), float(exponent))
    if best is None:
        raise RuntimeError("no valid edge candidate")
    return {
        "log_mean_square_error": best[0],
        "edge_ev": best[1],
        "amplitude": best[2],
        "exponent": best[3],
    }


def fit_summary(
    energy: np.ndarray,
    absorption: np.ndarray,
    gap_ev: float,
) -> dict[str, dict[str, float]]:
    mask = (absorption >= FIT_MIN_CM1) & (absorption <= FIT_MAX_CM1)
    fit_energy = energy[mask]
    fit_absorption = absorption[mask]
    if fit_energy.size < 20:
        raise ValueError("insufficient points in the declared fit window")
    output: dict[str, dict[str, float]] = {}
    for name, exponent in (("free", None), ("parabolic_0p5", 0.5), ("linear_1p0", 1.0)):
        result = fit_fractional_power_edge(
            fit_energy,
            fit_absorption,
            edge_bounds_ev=(gap_ev - 0.030, gap_ev + 0.005),
            fixed_exponent=exponent,
        )
        result["edge_bias_mev"] = 1000.0 * (result["edge_ev"] - gap_ev)
        output[name] = result
    return output


def analyze_scenario(composition_x: float, temperature_k: float) -> dict[str, Any]:
    gap_ev = float(provisional_hansen_pade_gap_ev(composition_x, temperature_k))
    energy = np.linspace(gap_ev - 0.040, gap_ev + 0.150, 5001)
    coefficient_k, exponent_n = moazzami_parameters(composition_x, temperature_k)

    moazzami = moazzami_absorption_cm1(
        energy, composition_x, temperature_k, gap_ev
    )
    chang_reference = chang_inspired_absorption_cm1(energy, gap_ev)
    threshold_bias = {
        str(int(threshold)): 1000.0
        * (threshold_edge_ev(energy, chang_reference, threshold) - gap_ev)
        for threshold in THRESHOLDS_CM1
    }

    return {
        "composition_x": composition_x,
        "temperature_k": temperature_k,
        "latent_gap_ev": gap_ev,
        "moazzami_parameters": {"K": coefficient_k, "n": exponent_n},
        "moazzami_truth_fits": fit_summary(energy, moazzami, gap_ev),
        "chang_inspired_truth_fits": fit_summary(energy, chang_reference, gap_ev),
        "chang_inspired_threshold_bias_mev": threshold_bias,
        "threshold_spread_600_to_2000_mev": (
            threshold_bias["2000"] - threshold_bias["600"]
        ),
    }


def sensitivity_summary() -> dict[str, Any]:
    rows: list[dict[str, float]] = []
    for composition_x, temperature_k in SCENARIOS:
        gap_ev = float(provisional_hansen_pade_gap_ev(composition_x, temperature_k))
        energy = np.linspace(gap_ev - 0.040, gap_ev + 0.150, 5001)
        for urbach_mev in (4.0, 6.0, 10.0):
            for edge_absorption in (200.0, 400.0, 800.0):
                curve = chang_inspired_absorption_cm1(
                    energy,
                    gap_ev,
                    urbach_energy_ev=urbach_mev / 1000.0,
                    edge_absorption_cm1=edge_absorption,
                )
                row = {
                    "composition_x": composition_x,
                    "temperature_k": temperature_k,
                    "urbach_energy_mev": urbach_mev,
                    "edge_absorption_cm1": edge_absorption,
                }
                for threshold in (1000.0, 1500.0, 2000.0):
                    row[f"bias_{int(threshold)}_mev"] = 1000.0 * (
                        threshold_edge_ev(energy, curve, threshold) - gap_ev
                    )
                rows.append(row)

    aggregates: dict[str, dict[str, float]] = {}
    for threshold in (1000, 1500, 2000):
        values = np.asarray([row[f"bias_{threshold}_mev"] for row in rows])
        aggregates[str(threshold)] = {
            "minimum_mev": float(np.min(values)),
            "median_mev": float(np.median(values)),
            "maximum_mev": float(np.max(values)),
        }
    return {"case_count": len(rows), "threshold_bias_aggregates": aggregates}


def analyze() -> dict[str, Any]:
    scenarios = [analyze_scenario(x, t) for x, t in SCENARIOS]
    moazzami_free_biases = [
        abs(row["moazzami_truth_fits"]["free"]["edge_bias_mev"])
        for row in scenarios
    ]
    moazzami_linear_biases = [
        abs(row["moazzami_truth_fits"]["linear_1p0"]["edge_bias_mev"])
        for row in scenarios
    ]
    chang_free_biases = [
        abs(row["chang_inspired_truth_fits"]["free"]["edge_bias_mev"])
        for row in scenarios
    ]
    nominal_1500 = [
        row["chang_inspired_threshold_bias_mev"]["1500"] for row in scenarios
    ]
    threshold_spreads = [row["threshold_spread_600_to_2000_mev"] for row in scenarios]
    chu_mean_residual_mev = 9.039188186513025
    sensitivity = sensitivity_summary()

    checks = {
        "correct_fractional_power_recovers_edge_within_0p05_mev": max(
            moazzami_free_biases
        )
        <= 0.05,
        "wrong_linear_exponent_produces_at_least_4p5_mev_bias": max(
            moazzami_linear_biases
        )
        >= 4.5,
        "free_power_law_misses_nonparabolic_reference_by_at_least_10_mev": max(
            chang_free_biases
        )
        >= 10.0,
        "nominal_1500_threshold_bias_is_at_least_8_mev_in_all_scenarios": min(
            nominal_1500
        )
        >= 8.0,
        "threshold_choice_600_to_2000_spans_at_least_15_mev": min(
            threshold_spreads
        )
        >= 15.0,
        "sensitivity_median_1500_bias_overlaps_multi_mev_regime": sensitivity[
            "threshold_bias_aggregates"
        ]["1500"]["median_mev"]
        >= 8.0,
    }

    return {
        "schema_version": "1.0",
        "analysis": "formula-level HgCdTe absorption observation-model benchmark",
        "claim_boundary": (
            "Synthetic formula comparison only; no specimen diagnosis or production "
            "edge correction is authorized."
        ),
        "source_model_provenance": {
            "moazzami_fractional_power_doi": "10.1007/s11664-005-0019-3",
            "chang_nonparabolic_urbach_doi": "10.1063/1.2245220",
        },
        "fit_window_cm1": [FIT_MIN_CM1, FIT_MAX_CM1],
        "scenarios": scenarios,
        "sensitivity": sensitivity,
        "comparison_to_existing_cross_source_residual": {
            "chu_mean_signed_residual_mev": chu_mean_residual_mev,
            "nominal_1500_threshold_bias_minimum_mev": min(nominal_1500),
            "nominal_1500_threshold_bias_maximum_mev": max(nominal_1500),
            "interpretation": (
                "The synthetic threshold bias has the same positive sign and multi-meV "
                "scale as the observed cross-source discrepancy, but does not identify "
                "its cause."
            ),
        },
        "validation_checks": checks,
        "decision": {
            "measurement_definition_can_generate_multi_mev_edge_bias": all(
                checks.values()
            ),
            "production_observation_correction_authorized": False,
            "static_gap_refit_authorized": False,
            "required_reporting": [
                "measurement model",
                "fit window",
                "absorption threshold",
                "carrier state",
                "tail model",
                "edge-model uncertainty envelope",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze()
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
