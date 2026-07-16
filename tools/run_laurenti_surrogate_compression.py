#!/usr/bin/env python3
"""Screen fixed-scale oscillator models against the Laurenti equation.

This study samples an established analytical equation, not experimental observations.
It measures representational capacity and conditioning only.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from dataclasses import asdict

import numpy as np

from mct_research import (
    GapBenchmarkData,
    OscillatorBasisSpec,
    fit_linear_gap_model,
    laurenti_gap_ev,
    oscillator_design_matrix,
    residual_metrics,
)

CANDIDATE_THETA_K = (
    5.0,
    10.0,
    15.0,
    20.0,
    30.0,
    40.0,
    60.0,
    80.0,
    120.0,
    160.0,
    240.0,
    320.0,
    480.0,
)
COMPOSITIONS = np.linspace(0.0, 1.0, 21)
TEMPERATURES_K = np.array(
    [0.0, 2.0, 5.0, 10.0, 20.0, 40.0, 77.0, 100.0, 150.0, 200.0, 300.0, 400.0, 500.0]
)


def make_surrogate_data() -> GapBenchmarkData:
    x = np.repeat(COMPOSITIONS, TEMPERATURES_K.size)
    temperature = np.tile(TEMPERATURES_K, COMPOSITIONS.size)
    gap = np.asarray(laurenti_gap_ev(x, temperature), dtype=float)
    groups = np.repeat(
        [f"x={composition:.2f}" for composition in COMPOSITIONS],
        TEMPERATURES_K.size,
    )
    return GapBenchmarkData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=np.ones_like(gap),
        group=groups,
    )


def candidate_scales(oscillator_count: int) -> list[tuple[float, ...]]:
    if oscillator_count == 1:
        return [(theta,) for theta in CANDIDATE_THETA_K]
    if oscillator_count == 2:
        return list(itertools.combinations(CANDIDATE_THETA_K, 2))
    raise ValueError("oscillator_count must be one or two")


def select_on_training_data(
    data: GapBenchmarkData,
    oscillator_count: int,
):
    candidates = []
    for scales in candidate_scales(oscillator_count):
        specification = OscillatorBasisSpec(
            static_degree=2,
            amplitude_degree=2,
            oscillator_temperatures_k=scales,
        )
        fit = fit_linear_gap_model(data, specification)
        candidates.append(
            (
                fit.metrics.rmse_mev,
                fit.metrics.max_abs_mev,
                fit.condition_number,
                scales,
                fit,
            )
        )
    return min(candidates, key=lambda item: item[:3])


def predict_fold(
    data: GapBenchmarkData,
    holdout: np.ndarray,
    oscillator_count: int,
) -> tuple[np.ndarray, dict[str, object]]:
    selected = select_on_training_data(data.subset(~holdout), oscillator_count)
    training_rmse, training_max, condition, scales, fit = selected
    matrix, _ = oscillator_design_matrix(
        fit.specification,
        data.x[holdout],
        data.temperature_k[holdout],
    )
    prediction = matrix @ fit.coefficients
    metrics = residual_metrics(data.gap_ev[holdout], prediction)
    record = {
        "selected_theta_k": list(scales),
        "training_rmse_mev": training_rmse,
        "training_max_abs_mev": training_max,
        "training_condition_number": condition,
        "holdout_metrics": asdict(metrics),
    }
    return prediction, record


def composition_holdout(
    data: GapBenchmarkData,
    oscillator_count: int,
) -> dict[str, object]:
    predictions = np.full(data.gap_ev.shape, np.nan)
    folds: dict[str, object] = {}
    for group in np.unique(data.group):
        holdout = data.group == group
        prediction, record = predict_fold(data, holdout, oscillator_count)
        predictions[holdout] = prediction
        folds[str(group)] = record
    metrics = residual_metrics(data.gap_ev, predictions)
    selections = Counter(
        tuple(record["selected_theta_k"]) for record in folds.values()
    )
    return {
        "aggregate_metrics": asdict(metrics),
        "selection_counts": {
            "+".join(f"{value:g}" for value in scales): count
            for scales, count in sorted(selections.items())
        },
        "max_training_condition_number": max(
            record["training_condition_number"] for record in folds.values()
        ),
        "folds": folds,
    }


def temperature_holdout(
    data: GapBenchmarkData,
    oscillator_count: int,
) -> dict[str, object]:
    masks = {
        "low_T_le_40K": data.temperature_k <= 40.0,
        "mid_40K_to_200K": (data.temperature_k > 40.0)
        & (data.temperature_k <= 200.0),
        "high_T_gt_200K": data.temperature_k > 200.0,
    }
    predictions = np.full(data.gap_ev.shape, np.nan)
    folds: dict[str, object] = {}
    for name, holdout in masks.items():
        prediction, record = predict_fold(data, holdout, oscillator_count)
        predictions[holdout] = prediction
        folds[name] = record
    metrics = residual_metrics(data.gap_ev, predictions)
    return {
        "aggregate_metrics": asdict(metrics),
        "max_training_condition_number": max(
            record["training_condition_number"] for record in folds.values()
        ),
        "folds": folds,
    }


def run_study() -> dict[str, object]:
    data = make_surrogate_data()
    models = {}
    for oscillator_count, name in (
        (1, "one_fixed_scale_oscillator"),
        (2, "two_fixed_scale_oscillators"),
    ):
        models[name] = {
            "leave_one_composition_out": composition_holdout(
                data, oscillator_count
            ),
            "held_out_temperature_ranges": temperature_holdout(
                data, oscillator_count
            ),
        }
    return {
        "study_class": "analytical_surrogate_compression_not_experimental_validation",
        "target": "Laurenti_1990_published_equation",
        "composition_grid": COMPOSITIONS.tolist(),
        "temperature_grid_k": TEMPERATURES_K.tolist(),
        "candidate_theta_k": list(CANDIDATE_THETA_K),
        "static_degree": 2,
        "amplitude_degree": 2,
        "selection_rule": "minimum_training_RMSE_then_max_error_then_condition_number",
        "models": models,
    }


def main() -> None:
    print(json.dumps(run_study(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
