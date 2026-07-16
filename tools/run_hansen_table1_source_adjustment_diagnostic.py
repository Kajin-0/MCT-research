#!/usr/bin/env python3
"""Diagnose source-offset versus composition-shift confounding in Hansen Table I.

This study uses only the 16 numerical cutoff points printed in Hansen et al.
Table I. It does not treat those in-sample data as external validation.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

from mct_research.gap_models import hansen_gap_ev, laurenti_gap_ev

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "hansen" / "measurements.csv"
METRICS_PATH = (
    ROOT
    / "data"
    / "validation"
    / "hansen_table1_source_adjustment_models.csv"
)
IDENTIFIABILITY_PATH = (
    ROOT
    / "data"
    / "validation"
    / "hansen_table1_source_adjustment_identifiability.csv"
)


@dataclass(frozen=True)
class Observation:
    source: str
    x: float
    temperature_k: float
    gap_ev: float


@dataclass(frozen=True)
class Metrics:
    mae_mev: float
    rmse_mev: float
    max_abs_error_mev: float
    sse_mev2: float


def load_table1(path: Path = INPUT_PATH) -> list[Observation]:
    observations: list[Observation] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            source_id = row["source_id"]
            if source_id == "HSC1982_TABLE1_TOBIN":
                source = "Tobin"
            elif source_id == "HSC1982_TABLE1_RAWE":
                source = "Rawe"
            else:
                continue
            observations.append(
                Observation(
                    source=source,
                    x=float(row["x_reported"]),
                    temperature_k=float(row["temperature_k"]),
                    gap_ev=float(row["gap_ev"]),
                )
            )
    if len(observations) != 16:
        raise RuntimeError(f"expected 16 Hansen Table I points, found {len(observations)}")
    return observations


def hansen_dx(x: float, temperature_k: float) -> float:
    """Analytical composition derivative of the Hansen equation, eV/x."""

    a = 5.35e-4
    return 1.930 - 1.620 * x + 2.496 * x**2 - 2.0 * a * temperature_k


def laurenti_dx(x: float, temperature_k: float) -> float:
    """Analytical composition derivative of the Laurenti equation, eV/x."""

    amplitude = 6.3 - 15.47 * x + 5.92 * x**2
    amplitude_dx = -15.47 + 11.84 * x
    scale = 11.0 + 67.7 * x
    scale_dx = 67.7
    denominator = temperature_k + scale
    static_dx = 1.777 + 0.264 * x
    thermal_dx = (
        1.0e-4
        * temperature_k**2
        * (amplitude_dx * denominator - amplitude * scale_dx)
        / denominator**2
    )
    return static_dx + thermal_dx


def gap_metrics(residual_ev: np.ndarray) -> Metrics:
    residual_mev = 1000.0 * np.asarray(residual_ev, dtype=float)
    return Metrics(
        mae_mev=float(np.mean(np.abs(residual_mev))),
        rmse_mev=float(np.sqrt(np.mean(residual_mev**2))),
        max_abs_error_mev=float(np.max(np.abs(residual_mev))),
        sse_mev2=float(np.sum(residual_mev**2)),
    )


def _bounded_minimize(
    objective: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    tolerance: float = 1.0e-13,
    max_iterations: int = 512,
) -> float:
    """Golden-section minimization on a finite scalar interval."""

    if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
        raise ValueError("bounds must be finite and strictly ordered")
    ratio = 0.5 * (np.sqrt(5.0) - 1.0)
    left = float(lower)
    right = float(upper)
    c = right - ratio * (right - left)
    d = left + ratio * (right - left)
    fc = float(objective(c))
    fd = float(objective(d))
    for _ in range(max_iterations):
        if right - left <= tolerance:
            return 0.5 * (left + right)
        if fc <= fd:
            right = d
            d = c
            fd = fc
            c = right - ratio * (right - left)
            fc = float(objective(c))
        else:
            left = c
            c = d
            fc = fd
            d = left + ratio * (right - left)
            fd = float(objective(d))
    raise RuntimeError("bounded minimization did not converge")


def _arrays(
    observations: list[Observation],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    source = np.asarray([item.source for item in observations], dtype=object)
    x = np.asarray([item.x for item in observations], dtype=float)
    temperature = np.asarray([item.temperature_k for item in observations], dtype=float)
    observed = np.asarray([item.gap_ev for item in observations], dtype=float)
    return source, x, temperature, observed


def evaluate_adjustments(
    observations: list[Observation],
    model: Callable[[np.ndarray, np.ndarray], float | np.ndarray],
) -> dict[str, object]:
    source, x, temperature, observed = _arrays(observations)
    nominal = np.asarray(model(x, temperature), dtype=float)

    energy_offsets: dict[str, float] = {}
    energy_prediction = nominal.copy()
    for name in ("Tobin", "Rawe"):
        mask = source == name
        offset = float(np.mean(observed[mask] - nominal[mask]))
        energy_offsets[name] = offset
        energy_prediction[mask] += offset

    composition_shifts: dict[str, float] = {}
    composition_prediction = np.empty_like(observed)
    for name in ("Tobin", "Rawe"):
        mask = source == name
        source_x = x[mask]
        source_t = temperature[mask]
        source_y = observed[mask]

        def objective(delta_x: float) -> float:
            prediction = np.asarray(model(source_x + delta_x, source_t), dtype=float)
            return float(np.sum((source_y - prediction) ** 2))

        delta_x = _bounded_minimize(objective, -0.01, 0.01)
        composition_shifts[name] = delta_x
        composition_prediction[mask] = np.asarray(
            model(source_x + delta_x, source_t), dtype=float
        )

    return {
        "none": {
            "metrics": gap_metrics(observed - nominal),
            "energy_offsets": {},
            "composition_shifts": {},
        },
        "source_energy_offsets": {
            "metrics": gap_metrics(observed - energy_prediction),
            "energy_offsets": energy_offsets,
            "composition_shifts": {},
        },
        "source_composition_shifts": {
            "metrics": gap_metrics(observed - composition_prediction),
            "energy_offsets": {},
            "composition_shifts": composition_shifts,
        },
    }


def source_identifiability(
    observations: list[Observation],
    derivative: Callable[[float, float], float],
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for name in ("Tobin", "Rawe"):
        subset = [item for item in observations if item.source == name]
        x = np.asarray([item.x for item in subset], dtype=float)
        slopes = np.asarray(
            [derivative(item.x, item.temperature_k) for item in subset], dtype=float
        )

        # Parameterization: b is measured in meV and dx in 0.001 composition.
        # Both columns therefore express their effect in eV on comparable scales.
        design = np.column_stack(
            [np.full(slopes.size, 1.0e-3), slopes * 1.0e-3]
        )
        covariance_shape = np.linalg.inv(design.T @ design)
        correlation = float(
            covariance_shape[0, 1]
            / np.sqrt(covariance_shape[0, 0] * covariance_shape[1, 1])
        )
        rows.append(
            {
                "source": name,
                "n_points": int(x.size),
                "x_min": float(np.min(x)),
                "x_max": float(np.max(x)),
                "derivative_min_ev_per_x": float(np.min(slopes)),
                "derivative_max_ev_per_x": float(np.max(slopes)),
                "derivative_relative_span": float(
                    (np.max(slopes) - np.min(slopes)) / np.mean(slopes)
                ),
                "condition_number_scaled": float(np.linalg.cond(design)),
                "covariance_correlation_b_dx": correlation,
            }
        )
    return rows


def run_study() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    observations = load_table1()
    models = {
        "Hansen": (hansen_gap_ev, hansen_dx),
        "Laurenti": (laurenti_gap_ev, laurenti_dx),
    }

    metric_rows: list[dict[str, object]] = []
    identifiability_rows: list[dict[str, object]] = []
    for model_name, (model, derivative) in models.items():
        adjustments = evaluate_adjustments(observations, model)
        for adjustment_name, result in adjustments.items():
            metrics = result["metrics"]
            assert isinstance(metrics, Metrics)
            energy_offsets = result["energy_offsets"]
            composition_shifts = result["composition_shifts"]
            assert isinstance(energy_offsets, dict)
            assert isinstance(composition_shifts, dict)
            metric_rows.append(
                {
                    "model": model_name,
                    "adjustment": adjustment_name,
                    "fitted_parameter_count": 0 if adjustment_name == "none" else 2,
                    "mae_mev": metrics.mae_mev,
                    "rmse_mev": metrics.rmse_mev,
                    "max_abs_error_mev": metrics.max_abs_error_mev,
                    "sse_mev2": metrics.sse_mev2,
                    "tobin_energy_offset_mev": 1000.0
                    * float(energy_offsets.get("Tobin", np.nan)),
                    "rawe_energy_offset_mev": 1000.0
                    * float(energy_offsets.get("Rawe", np.nan)),
                    "tobin_delta_x": float(composition_shifts.get("Tobin", np.nan)),
                    "rawe_delta_x": float(composition_shifts.get("Rawe", np.nan)),
                }
            )
        for row in source_identifiability(observations, derivative):
            identifiability_rows.append({"model": model_name, **row})

    return metric_rows, identifiability_rows


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    metric_rows, identifiability_rows = run_study()
    _write_rows(METRICS_PATH, metric_rows)
    _write_rows(IDENTIFIABILITY_PATH, identifiability_rows)

    for row in metric_rows:
        print(
            f"{row['model']:8s} {row['adjustment']:28s} "
            f"MAE={row['mae_mev']:.3f} meV "
            f"RMSE={row['rmse_mev']:.3f} meV"
        )
    for row in identifiability_rows:
        print(
            f"{row['model']:8s} {row['source']:5s} "
            f"condition={row['condition_number_scaled']:.1f} "
            f"corr={row['covariance_correlation_b_dx']:.9f}"
        )


if __name__ == "__main__":
    main()
