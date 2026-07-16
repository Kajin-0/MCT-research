#!/usr/bin/env python3
"""Leave-one-specimen-out test of Seiler 1990 low-temperature shape.

The fit uses only the direct Figure 7 markers committed by PR #57. One
additive energy offset is profiled for every specimen. The test therefore
addresses thermal shape, not absolute composition-law accuracy.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

PUBLISHED_A_K3 = -1822.0
PUBLISHED_B_K2 = 255.2
B_PROFILE_MIN_K2 = 1.0
B_PROFILE_MAX_K2 = 5000.0


def _load(path: str | Path) -> dict[int, dict[str, Any]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 34:
        raise ValueError("expected the 34-marker Figure 7 ledger")
    samples: dict[int, dict[str, Any]] = {}
    for row in rows:
        sample = int(row["sample_number"])
        record = samples.setdefault(
            sample,
            {
                "composition_x": float(row["composition_x_reported"]),
                "temperature_k": [],
                "gap_mev": [],
            },
        )
        if record["composition_x"] != float(row["composition_x_reported"]):
            raise ValueError("composition changed within one specimen")
        record["temperature_k"].append(float(row["temperature_k_digitized"]))
        record["gap_mev"].append(float(row["gap_mev_digitized"]))
    if sorted(samples) != [1, 2, 3]:
        raise ValueError("expected specimens 1, 2, and 3")
    for record in samples.values():
        order = np.argsort(record["temperature_k"])
        record["temperature_k"] = np.asarray(record["temperature_k"], dtype=float)[order]
        record["gap_mev"] = np.asarray(record["gap_mev"], dtype=float)[order]
    return samples


def _scale(composition_x: float) -> float:
    return 0.535 * (1.0 - 2.0 * composition_x)


def _seiler_shape(
    temperature_k: np.ndarray,
    composition_x: float,
    a_k3: float,
    b_k2: float,
) -> np.ndarray:
    return _scale(composition_x) * (
        a_k3 + temperature_k**3
    ) / (b_k2 + temperature_k**2)


def _hansen_shape(temperature_k: np.ndarray, composition_x: float) -> np.ndarray:
    return _scale(composition_x) * temperature_k


def _quadratic_shape(
    temperature_k: np.ndarray,
    composition_x: float,
    p1: float,
    p2_per_k: float,
) -> np.ndarray:
    return _scale(composition_x) * (
        p1 * temperature_k + p2_per_k * temperature_k**2
    )


def _offset_residuals(gap_mev: np.ndarray, shape_mev: np.ndarray) -> tuple[float, np.ndarray]:
    offset = float(np.mean(gap_mev - shape_mev))
    return offset, gap_mev - (offset + shape_mev)


def _metrics(residuals: np.ndarray) -> dict[str, float]:
    return {
        "mean_signed_mev": float(np.mean(residuals)),
        "mae_mev": float(np.mean(np.abs(residuals))),
        "rmse_mev": float(np.sqrt(np.mean(residuals**2))),
        "maximum_absolute_mev": float(np.max(np.abs(residuals))),
    }


def _solve_seiler_at_b(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...], log_b: float
) -> tuple[float, float, float, dict[int, float]]:
    b_k2 = float(np.exp(log_b))
    design_rows: list[list[float]] = []
    target: list[float] = []
    for sample in train_ids:
        record = samples[sample]
        temperature = record["temperature_k"]
        gap = record["gap_mev"]
        scale = _scale(record["composition_x"])
        denominator = b_k2 + temperature**2
        fixed = scale * temperature**3 / denominator
        a_column = scale / denominator
        for coefficient, value in zip(a_column, gap - fixed, strict=True):
            design_rows.append(
                [float(coefficient)]
                + [1.0 if candidate == sample else 0.0 for candidate in train_ids]
            )
            target.append(float(value))
    design = np.asarray(design_rows, dtype=float)
    response = np.asarray(target, dtype=float)
    coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
    residuals = response - design @ coefficients
    offsets = {
        sample: float(coefficients[index + 1])
        for index, sample in enumerate(train_ids)
    }
    return (
        float(residuals @ residuals),
        b_k2,
        float(coefficients[0]),
        offsets,
    )


def _fit_seiler_family(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...]
) -> dict[str, Any]:
    log_min = math.log(B_PROFILE_MIN_K2)
    log_max = math.log(B_PROFILE_MAX_K2)
    grid = np.linspace(log_min, log_max, 2001)
    grid_sse = np.asarray(
        [_solve_seiler_at_b(samples, train_ids, float(value))[0] for value in grid]
    )
    best = int(np.argmin(grid_sse))
    lower = float(grid[max(0, best - 2)])
    upper = float(grid[min(grid.size - 1, best + 2)])

    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    left = upper - (upper - lower) / golden_ratio
    right = lower + (upper - lower) / golden_ratio
    left_sse = _solve_seiler_at_b(samples, train_ids, left)[0]
    right_sse = _solve_seiler_at_b(samples, train_ids, right)[0]
    for _ in range(160):
        if left_sse < right_sse:
            upper, right, right_sse = right, left, left_sse
            left = upper - (upper - lower) / golden_ratio
            left_sse = _solve_seiler_at_b(samples, train_ids, left)[0]
        else:
            lower, left, left_sse = left, right, right_sse
            right = lower + (upper - lower) / golden_ratio
            right_sse = _solve_seiler_at_b(samples, train_ids, right)[0]

    sse, b_k2, a_k3, offsets = _solve_seiler_at_b(
        samples, train_ids, 0.5 * (lower + upper)
    )
    return {
        "a_k3": a_k3,
        "b_k2": b_k2,
        "training_sse_mev2": sse,
        "training_offsets_mev": offsets,
    }


def _fit_scaled_quadratic(
    samples: dict[int, dict[str, Any]], train_ids: tuple[int, ...]
) -> dict[str, Any]:
    design_rows: list[list[float]] = []
    target: list[float] = []
    for sample in train_ids:
        record = samples[sample]
        scale = _scale(record["composition_x"])
        for temperature, gap in zip(
            record["temperature_k"], record["gap_mev"], strict=True
        ):
            design_rows.append(
                [scale * temperature, scale * temperature**2]
                + [1.0 if candidate == sample else 0.0 for candidate in train_ids]
            )
            target.append(float(gap))
    design = np.asarray(design_rows, dtype=float)
    response = np.asarray(target, dtype=float)
    coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
    residuals = response - design @ coefficients
    return {
        "p1": float(coefficients[0]),
        "p2_per_k": float(coefficients[1]),
        "training_sse_mev2": float(residuals @ residuals),
    }


def _normalized_jacobian_diagnostics(
    samples: dict[int, dict[str, Any]],
    train_ids: tuple[int, ...],
    a_k3: float,
    b_k2: float,
) -> dict[str, float]:
    def profiled_residuals(a_value: float, b_value: float) -> np.ndarray:
        values: list[float] = []
        for sample in train_ids:
            record = samples[sample]
            shape = _seiler_shape(
                record["temperature_k"], record["composition_x"], a_value, b_value
            )
            _, residuals = _offset_residuals(record["gap_mev"], shape)
            values.extend(residuals.tolist())
        return np.asarray(values, dtype=float)

    step_a = max(1.0e-3, abs(a_k3) * 1.0e-5)
    step_b = max(1.0e-6, b_k2 * 1.0e-5)
    jacobian_a = (
        profiled_residuals(a_k3 + step_a, b_k2)
        - profiled_residuals(a_k3 - step_a, b_k2)
    ) / (2.0 * step_a)
    jacobian_b = (
        profiled_residuals(a_k3, b_k2 + step_b)
        - profiled_residuals(a_k3, b_k2 - step_b)
    ) / (2.0 * step_b)
    norm_a = float(np.linalg.norm(jacobian_a))
    norm_b = float(np.linalg.norm(jacobian_b))
    correlation = float(jacobian_a @ jacobian_b / (norm_a * norm_b))
    normalized = np.column_stack([jacobian_a / norm_a, jacobian_b / norm_b])
    singular_values = np.linalg.svd(normalized, compute_uv=False)
    return {
        "normalized_jacobian_column_correlation": correlation,
        "normalized_jacobian_condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
    }


def analyze(path: str | Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    samples = _load(path)
    fold_rows: list[dict[str, Any]] = []
    pooled: dict[str, list[float]] = {
        "hansen_fixed_linear": [],
        "published_seiler": [],
        "trained_seiler_family": [],
        "trained_scaled_quadratic": [],
    }

    for heldout in sorted(samples):
        train_ids = tuple(sample for sample in sorted(samples) if sample != heldout)
        seiler_fit = _fit_seiler_family(samples, train_ids)
        quadratic_fit = _fit_scaled_quadratic(samples, train_ids)
        diagnostics = _normalized_jacobian_diagnostics(
            samples,
            train_ids,
            seiler_fit["a_k3"],
            seiler_fit["b_k2"],
        )
        record = samples[heldout]
        models = {
            "hansen_fixed_linear": _hansen_shape(
                record["temperature_k"], record["composition_x"]
            ),
            "published_seiler": _seiler_shape(
                record["temperature_k"],
                record["composition_x"],
                PUBLISHED_A_K3,
                PUBLISHED_B_K2,
            ),
            "trained_seiler_family": _seiler_shape(
                record["temperature_k"],
                record["composition_x"],
                seiler_fit["a_k3"],
                seiler_fit["b_k2"],
            ),
            "trained_scaled_quadratic": _quadratic_shape(
                record["temperature_k"],
                record["composition_x"],
                quadratic_fit["p1"],
                quadratic_fit["p2_per_k"],
            ),
        }
        for model_name, shape in models.items():
            offset, residuals = _offset_residuals(record["gap_mev"], shape)
            pooled[model_name].extend(residuals.tolist())
            row: dict[str, Any] = {
                "heldout_sample": heldout,
                "training_samples": "+".join(str(value) for value in train_ids),
                "model": model_name,
                "heldout_point_count": int(residuals.size),
                "heldout_offset_mev": offset,
                **_metrics(residuals),
                "trained_a_k3": "",
                "trained_b_k2": "",
                "trained_quadratic_p1": "",
                "trained_quadratic_p2_per_k": "",
                "normalized_jacobian_column_correlation": "",
                "normalized_jacobian_condition_number": "",
            }
            if model_name == "trained_seiler_family":
                row.update(
                    {
                        "trained_a_k3": seiler_fit["a_k3"],
                        "trained_b_k2": seiler_fit["b_k2"],
                        **diagnostics,
                    }
                )
            if model_name == "trained_scaled_quadratic":
                row.update(
                    {
                        "trained_quadratic_p1": quadratic_fit["p1"],
                        "trained_quadratic_p2_per_k": quadratic_fit["p2_per_k"],
                    }
                )
            fold_rows.append(row)

    pooled_metrics = {
        model: _metrics(np.asarray(values, dtype=float))
        for model, values in pooled.items()
    }
    trained_rows = [
        row for row in fold_rows if row["model"] == "trained_seiler_family"
    ]
    absolute_a = np.asarray([abs(float(row["trained_a_k3"])) for row in trained_rows])
    b_values = np.asarray([float(row["trained_b_k2"]) for row in trained_rows])
    summary = {
        "analysis": "Seiler 1990 leave-one-specimen-out thermal-shape transfer",
        "measurement_class": "two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap",
        "validation_unit": "specimen",
        "specimen_offsets_profiled": True,
        "pooled_heldout_metrics": pooled_metrics,
        "heldout_rmse_reduction_vs_hansen": float(
            1.0
            - pooled_metrics["trained_seiler_family"]["rmse_mev"]
            / pooled_metrics["hansen_fixed_linear"]["rmse_mev"]
        ),
        "heldout_rmse_reduction_vs_scaled_quadratic": float(
            1.0
            - pooled_metrics["trained_seiler_family"]["rmse_mev"]
            / pooled_metrics["trained_scaled_quadratic"]["rmse_mev"]
        ),
        "trained_parameter_stability": {
            "published_a_k3": PUBLISHED_A_K3,
            "published_b_k2": PUBLISHED_B_K2,
            "fold_a_k3": [float(row["trained_a_k3"]) for row in trained_rows],
            "fold_b_k2": [float(row["trained_b_k2"]) for row in trained_rows],
            "absolute_a_max_to_min_ratio": float(np.max(absolute_a) / np.min(absolute_a)),
            "b_max_to_min_ratio": float(np.max(b_values) / np.min(b_values)),
            "jacobian_correlation_range": [
                float(min(row["normalized_jacobian_column_correlation"] for row in trained_rows)),
                float(max(row["normalized_jacobian_column_correlation"] for row in trained_rows)),
            ],
            "decision": (
                "the rational family transfers, but A and B are correlated and "
                "not individually identified under specimen offsets"
            ),
        },
        "scientific_decision": (
            "A nonlinear low-temperature shape transfers across held-out specimens "
            "and materially outperforms Hansen's fixed linear shape. The data do "
            "not identify the individual Seiler A and B parameters or a microscopic scale."
        ),
        "claim_boundary": [
            "Only three specimens are available, so every fold trains on two specimens.",
            "Samples 1 and 2 do not have independently calibrated compositions.",
            "One held-out additive energy offset is fitted; this is a shape test, not absolute-gap prediction.",
            "The scaled quadratic comparator shows that generic smooth curvature also transfers reasonably well.",
            "No pointwise experimental covariance is available for Figure 7.",
        ],
    }
    return fold_rows, summary


def _write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/seiler1990_figure7_digitized.csv",
    )
    parser.add_argument("--output-csv")
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    rows, summary = analyze(args.input_csv)
    if args.output_csv:
        _write_csv(args.output_csv, rows)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
