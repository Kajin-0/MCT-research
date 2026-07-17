#!/usr/bin/env python3
"""Reject an endpoint- and critical-composition-constrained thermal surrogate."""
import csv
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LAURENTI = ROOT / "data/experimental/laurenti1990_figure2_cd_rich_digitized.csv"
SEILER = ROOT / "data/experimental/seiler1990_figure7_digitized.csv"


def xc():
    roots = np.roots([5.92, -15.47, 6.3])
    return float(next(root.real for root in roots if abs(root.imag) < 1e-12 and 0 < root.real < 1))


def laurenti(x, temperature):
    return 1e-4 * (6.3 - 15.47*x + 5.92*x*x) * temperature**2 / (11 + 67.7*x + temperature)


def surrogate(x, temperature):
    critical = xc()
    hg = laurenti(0.0, temperature)
    cd = laurenti(1.0, temperature)
    bowing = ((1-critical)*hg + critical*cd) / (critical*(1-critical))
    return (1-x)*hg + x*cd - bowing*x*(1-x)


def metrics(residual):
    residual = np.asarray(residual, float)
    return {
        "rmse_mev": float(np.sqrt(np.mean(residual**2))),
        "mean_absolute_error_mev": float(np.mean(np.abs(residual))),
        "maximum_absolute_error_mev": float(np.max(np.abs(residual))),
    }


def cd_rich_scores():
    with LAURENTI.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["point_kind"] == "digitized_full_square"]
    if len(rows) != 18:
        raise RuntimeError("expected 18 Laurenti markers")
    observed = np.array([float(row["shift_from_2k_mev"]) for row in rows])
    exact = np.array([1000*(laurenti(float(row["composition_x"]), float(row["temperature_k"])) - laurenti(float(row["composition_x"]), 2.0)) for row in rows])
    reduced = np.array([1000*(surrogate(float(row["composition_x"]), float(row["temperature_k"])) - surrogate(float(row["composition_x"]), 2.0)) for row in rows])
    return {"laurenti_equation7": metrics(exact-observed), "endpoint_critical_surrogate": metrics(reduced-observed)}


def seiler_scores():
    with SEILER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 34:
        raise RuntimeError("expected 34 Seiler markers")
    residuals = {"hansen_linear": [], "laurenti_equation7": [], "endpoint_critical_surrogate": []}
    for sample in (1, 2, 3):
        subset = [row for row in rows if int(row["sample_number"]) == sample]
        x = float(subset[0]["composition_x_reported"])
        temperature = np.array([float(row["temperature_k_digitized"]) for row in subset])
        observed = np.array([float(row["gap_mev_digitized"]) for row in subset])
        predictions = {
            "hansen_linear": 1000*5.35e-4*(1-2*x)*temperature,
            "laurenti_equation7": np.array([1000*laurenti(x, value) for value in temperature]),
            "endpoint_critical_surrogate": np.array([1000*surrogate(x, value) for value in temperature]),
        }
        for name, prediction in predictions.items():
            offset = np.mean(observed-prediction)
            residuals[name].extend(prediction+offset-observed)
    return {name: metrics(values) for name, values in residuals.items()}


def surface_score():
    maximum = 0.0
    sum_square = 0.0
    count = 0
    for temperature in np.linspace(0, 500, 1001):
        residual = 1000*np.array([surrogate(x, temperature)-laurenti(x, temperature) for x in np.linspace(0, 1, 1001)])
        maximum = max(maximum, float(np.max(np.abs(residual))))
        sum_square += float(residual @ residual)
        count += residual.size
    return {"maximum_absolute_difference_mev": maximum, "rms_difference_mev": float(np.sqrt(sum_square/count))}


def analyze():
    surface = surface_score()
    cd_rich = cd_rich_scores()
    seiler = seiler_scores()
    if cd_rich["endpoint_critical_surrogate"]["rmse_mev"] <= cd_rich["laurenti_equation7"]["rmse_mev"]:
        raise RuntimeError("surrogate unexpectedly improved Laurenti fitting data")
    if seiler["endpoint_critical_surrogate"]["rmse_mev"] <= seiler["hansen_linear"]["rmse_mev"]:
        raise RuntimeError("surrogate unexpectedly improved Seiler shapes")
    return {
        "analysis": "endpoint-critical thermal surrogate rejection",
        "critical_composition": xc(),
        "surface_equivalence_to_laurenti": surface,
        "direct_cd_rich_marker_scores": cd_rich,
        "seiler_profiled_offset_shape_scores": seiler,
        "decision": "Endpoint signs and the zero-shift composition constrain composition architecture but do not define a predictive temperature kernel. Reject the surrogate.",
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2, sort_keys=True))
