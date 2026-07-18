#!/usr/bin/env python3
"""Audit primary Teppe 2016 HgCdTe gap points under both reported compositions.

The paper reports Sample A as x=0.175 in the main text/figures and x=0.170 in
Methods.  This tool preserves both hypotheses and fails closed on universal
model promotion when the discrepancy reverses the model ranking.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Callable

import numpy as np

from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import chu_1983_gap_ev


def metrics(residual_mev: np.ndarray) -> dict[str, float]:
    residual = np.asarray(residual_mev, dtype=float)
    return {
        "mean_signed_mev": float(np.mean(residual)),
        "mae_mev": float(np.mean(np.abs(residual))),
        "rmse_mev": float(np.sqrt(np.mean(residual**2))),
        "maximum_absolute_mev": float(np.max(np.abs(residual))),
    }


def load_points(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            rows.append(
                {
                    "sample": row["sample"],
                    "temperature_k": float(row["temperature_k"]),
                    "gap_ev": float(row["gap_ev"]),
                    "gap_sigma_ev": float(row["gap_sigma_ev"]) if row["gap_sigma_ev"] else None,
                    "composition_figure": float(row["composition_figure"]),
                    "composition_methods": float(row["composition_methods"]),
                    "provenance_status": row["provenance_status"],
                }
            )
    if len(rows) != 5 or sum(row["sample"] == "A" for row in rows) != 4:
        raise ValueError("expected four Sample A points and one Sample B point")
    return rows


def evaluate(
    rows: list[dict[str, Any]],
    model: Callable[[np.ndarray, np.ndarray], np.ndarray | float],
    composition_field: str,
) -> dict[str, float]:
    x = np.asarray([row[composition_field] for row in rows], dtype=float)
    t = np.asarray([row["temperature_k"] for row in rows], dtype=float)
    observed = np.asarray([row["gap_ev"] for row in rows], dtype=float)
    predicted = np.asarray(model(x, t), dtype=float)
    return metrics(1000.0 * (observed - predicted))


def best_sample_a_composition(
    rows: list[dict[str, Any]],
    model: Callable[[np.ndarray, np.ndarray], np.ndarray | float],
) -> dict[str, float]:
    sample = [row for row in rows if row["sample"] == "A"]
    t = np.asarray([row["temperature_k"] for row in sample], dtype=float)
    observed = np.asarray([row["gap_ev"] for row in sample], dtype=float)
    grid = np.linspace(0.16, 0.185, 25001)
    prediction = np.asarray(model(grid[:, None], t[None, :]), dtype=float)
    rmse = np.sqrt(np.mean((observed[None, :] - prediction) ** 2, axis=1))
    index = int(np.argmin(rmse))
    residual = 1000.0 * (observed - prediction[index])
    return {
        "best_composition_x": float(grid[index]),
        "rmse_mev": float(rmse[index] * 1000.0),
        "residuals_mev": residual.tolist(),
    }


def analyze(path: str | Path) -> dict[str, Any]:
    rows = load_points(path)
    models: dict[str, Callable[[np.ndarray, np.ndarray], np.ndarray | float]] = {
        "hansen": hansen_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
        "laurenti": laurenti_gap_ev,
        "chu_1983": chu_1983_gap_ev,
    }
    hypotheses: dict[str, Any] = {}
    winners: dict[str, str] = {}
    for label, field in (
        ("figure_and_main_text_x_0p175", "composition_figure"),
        ("methods_x_0p170", "composition_methods"),
    ):
        result = {name: evaluate(rows, model, field) for name, model in models.items()}
        hypotheses[label] = result
        winners[label] = min(result, key=lambda name: result[name]["rmse_mev"])

    fitted = {
        name: best_sample_a_composition(rows, model) for name, model in models.items()
    }
    ranking_reverses = len(set(winners.values())) > 1
    return {
        "source": {
            "doi": "10.1038/ncomms12576",
            "point_count": len(rows),
            "sample_a_composition_main_text_and_figures": 0.175,
            "sample_a_composition_methods": 0.170,
            "composition_conflict_delta_x": 0.005,
            "measurement_class": "magneto_optical_zero_field_intercept",
        },
        "reported_composition_hypotheses": hypotheses,
        "winner_by_hypothesis": winners,
        "sample_a_profiled_composition": fitted,
        "decision": {
            "model_ranking_reverses_across_reported_compositions": ranking_reverses,
            "strict_universal_model_promotion_authorized": False,
            "provisional_hansen_pade_retained_for_seiler_regime_only": True,
            "provisional_hansen_pade_global_leading_claim_withdrawn": True,
            "teppe_series_admitted_as_primary_benchmark": True,
            "next_required_evidence": "resolve Sample A composition from author/source records or independent metrology",
        },
        "claim_boundary": (
            "Exact point labels are primary, but the source contains an internal "
            "0.005 composition inconsistency that reverses the aggregate model ranking."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.input_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
