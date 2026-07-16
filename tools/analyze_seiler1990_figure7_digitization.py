#!/usr/bin/env python3
"""Audit the calibrated direct-marker digitization of Seiler 1990 Figure 7."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Callable


def _load(path: str | Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 34:
        raise ValueError("expected 34 direct Figure 7 markers")
    return rows


def _hansen_shape_mev(x: float, temperature_k: float) -> float:
    return 0.535 * (1.0 - 2.0 * x) * temperature_k


def _seiler_shape_mev(x: float, temperature_k: float) -> float:
    numerator = -1822.0 + temperature_k**3
    denominator = 255.2 + temperature_k**2
    return 0.535 * (1.0 - 2.0 * x) * numerator / denominator


def _metrics(values: list[float]) -> dict[str, float]:
    return {
        "mean_signed_mev": sum(values) / len(values),
        "mae_mev": sum(abs(value) for value in values) / len(values),
        "rmse_mev": math.sqrt(sum(value * value for value in values) / len(values)),
        "maximum_absolute_mev": max(abs(value) for value in values),
    }


def _shape_residuals(
    samples: dict[int, list[dict[str, str]]],
    shape: Callable[[float, float], float],
) -> tuple[list[float], dict[int, dict[str, Any]]]:
    pooled: list[float] = []
    per_sample: dict[int, dict[str, Any]] = {}
    for sample_number, rows in sorted(samples.items()):
        composition = float(rows[0]["composition_x_reported"])
        temperatures = [float(row["temperature_k_digitized"]) for row in rows]
        gaps = [float(row["gap_mev_digitized"]) for row in rows]
        shape_values = [shape(composition, temperature) for temperature in temperatures]
        offset = sum(gap - value for gap, value in zip(gaps, shape_values, strict=True)) / len(rows)
        residuals = [
            gap - (offset + value)
            for gap, value in zip(gaps, shape_values, strict=True)
        ]
        pooled.extend(residuals)
        per_sample[sample_number] = {
            "point_count": len(rows),
            "composition_x_reported": composition,
            "fitted_specimen_offset_mev": offset,
            **_metrics(residuals),
        }
    return pooled, per_sample


def analyze(path: str | Path) -> dict[str, Any]:
    rows = _load(path)
    samples: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        sample_number = int(row["sample_number"])
        samples.setdefault(sample_number, []).append(row)

        x_left = float(row["x_axis_left_px"])
        x_right = float(row["x_axis_right_px"])
        y_top = float(row["y_axis_top_px"])
        y_bottom = float(row["y_axis_bottom_px"])
        x_min = float(row["x_axis_min_k"])
        x_max = float(row["x_axis_max_k"])
        y_min = float(row["y_axis_min_mev"])
        y_max = float(row["y_axis_max_mev"])
        pixel_x = float(row["marker_center_x_px"])
        pixel_y = float(row["marker_center_y_px"])

        reproduced_temperature = x_min + (pixel_x - x_left) * (x_max - x_min) / (x_right - x_left)
        reproduced_gap = y_max - (pixel_y - y_top) * (y_max - y_min) / (y_bottom - y_top)
        if abs(reproduced_temperature - float(row["temperature_k_digitized"])) > 1.0e-6:
            raise ValueError("temperature calibration does not reproduce committed value")
        if abs(reproduced_gap - float(row["gap_mev_digitized"])) > 1.0e-6:
            raise ValueError("gap calibration does not reproduce committed value")

    for sample_rows in samples.values():
        sample_rows.sort(key=lambda row: float(row["temperature_k_digitized"]))

    hansen_residuals, hansen_by_sample = _shape_residuals(samples, _hansen_shape_mev)
    seiler_residuals, seiler_by_sample = _shape_residuals(samples, _seiler_shape_mev)
    hansen_metrics = _metrics(hansen_residuals)
    seiler_metrics = _metrics(seiler_residuals)

    plateau_checks: list[dict[str, float | int]] = []
    for sample_number, sample_rows in sorted(samples.items()):
        first = sample_rows[0]
        near_ten = min(
            sample_rows,
            key=lambda row: abs(float(row["temperature_k_digitized"]) - 10.0),
        )
        composition = float(first["composition_x_reported"])
        delta_temperature = (
            float(near_ten["temperature_k_digitized"])
            - float(first["temperature_k_digitized"])
        )
        observed_change = (
            float(near_ten["gap_mev_digitized"])
            - float(first["gap_mev_digitized"])
        )
        hansen_change = _hansen_shape_mev(composition, delta_temperature)
        plateau_checks.append(
            {
                "sample_number": sample_number,
                "start_temperature_k": float(first["temperature_k_digitized"]),
                "near_10k_temperature_k": float(near_ten["temperature_k_digitized"]),
                "observed_gap_change_mev": observed_change,
                "hansen_linear_change_mev": hansen_change,
                "observed_minus_hansen_mev": observed_change - hansen_change,
            }
        )

    return {
        "analysis": "Seiler 1990 Figure 7 calibrated direct-marker digitization",
        "source_kind": "experimental_TPMA_gap_inferred_with_modified_Pidgeon_Brown_model",
        "total_marker_count": len(rows),
        "marker_count_by_sample": {
            str(sample_number): len(sample_rows)
            for sample_number, sample_rows in sorted(samples.items())
        },
        "composition_admissibility": {
            "sample_1": "cutoff-derived composition; shape use only",
            "sample_2": "composition assigned using HSC; shape use only",
            "sample_3": "wet-chemistry-tied composition; independently composition calibrated",
        },
        "digitization": {
            "marker_center_half_width_px": 2.0,
            "temperature_half_width_k_by_panel": {
                panel: float(next(row["temperature_digitization_half_width_k"] for row in rows if row["panel"] == panel))
                for panel in ("a", "b", "c")
            },
            "gap_half_width_mev_by_panel": {
                panel: float(next(row["gap_digitization_half_width_mev"] for row in rows if row["panel"] == panel))
                for panel in ("a", "b", "c")
            },
            "visual_overlay_check": "all 34 Hough-detected centers checked against the 400-dpi render",
        },
        "specimen_offset_shape_comparison": {
            "hansen_linear_temperature_shape": {
                "pooled": hansen_metrics,
                "per_sample": hansen_by_sample,
            },
            "seiler_published_nonlinear_shape": {
                "pooled": seiler_metrics,
                "per_sample": seiler_by_sample,
            },
            "pooled_rmse_fractional_reduction": (
                1.0 - seiler_metrics["rmse_mev"] / hansen_metrics["rmse_mev"]
            ),
            "decision": (
                "the digitized markers reproduce the reported nonlinear shape, "
                "but this is an in-sample comparison because Seiler fitted the "
                "published nonlinear relation to these specimens"
            ),
        },
        "approximately_5_to_10k_plateau_checks": plateau_checks,
        "scientific_decision": (
            "Figure 7 is now available as a direct experimental marker ledger. "
            "It supports a low-temperature plateau and nonlinear thermal shape, "
            "but it cannot independently validate Seiler over Hansen or identify "
            "a microscopic phonon scale."
        ),
        "limitations": [
            "Figure 7 does not report pointwise experimental gap uncertainties.",
            "The solid curves are fitted relations and were not digitized as data.",
            "Sample 2 composition is equation-assigned and cannot validate a composition law.",
            "Sample 1 composition is cutoff-derived and is not independent composition calibration.",
            "The TPMA gap remains model inferred rather than a raw optical-edge observable.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/seiler1990_figure7_digitized.csv",
    )
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    summary = analyze(args.input_csv)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
