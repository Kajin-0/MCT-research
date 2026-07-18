#!/usr/bin/env python3
"""Screen the provisional Hansen-Pade law on historical low-temperature data.

The screen is intentionally secondary. Many legacy compositions in Seiler Table 2
were not independently audited, and the present-work measurements are reported
over 2-10 K rather than at one exact temperature.  The purpose is to detect
catastrophic extrapolation and expose the remaining static-composition error, not
to refit the provisional thermal coefficients.
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
from tools.analyze_hansen_pade_crossover import published_seiler_gap_ev
from tools.analyze_seiler1990_heldout_shape import _metrics


def _temperature_k(value: str) -> float:
    text = value.strip()
    if "-" in text:
        lower, upper = (float(piece) for piece in text.split("-", maxsplit=1))
        return 0.5 * (lower + upper)
    return float(text)


def _load(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for index, row in enumerate(csv.DictReader(stream)):
            records.append(
                {
                    "index": index,
                    "composition_x": float(row["composition_x"]),
                    "temperature_k": _temperature_k(row["temperature_k_or_range"]),
                    "reported_temperature": row["temperature_k_or_range"],
                    "gap_mev": float(row["gap_mev"]),
                    "present_work": row["present_work"].strip().lower() == "true",
                    "sample_number": row["sample_number"].strip() or None,
                    "composition_provenance_status": row[
                        "composition_provenance_status"
                    ],
                    "measurement_class": row["measurement_class"],
                    "reference_group": row["reference_group"],
                }
            )
    if not records:
        raise ValueError("historical screen contains no records")
    return records


def _evaluate_subset(
    records: list[dict[str, Any]],
    models: dict[str, Callable[[float, float], float]],
) -> dict[str, Any]:
    residuals: dict[str, list[float]] = {name: [] for name in models}
    point_records: list[dict[str, Any]] = []
    for record in records:
        predictions: dict[str, float] = {}
        for name, model in models.items():
            prediction_mev = 1000.0 * float(
                model(record["composition_x"], record["temperature_k"])
            )
            predictions[name] = prediction_mev
            residuals[name].append(record["gap_mev"] - prediction_mev)
        point_records.append({**record, "predicted_gap_mev": predictions})
    return {
        "count": len(records),
        "metrics": {
            name: _metrics(np.asarray(values, dtype=float))
            for name, values in residuals.items()
        },
        "records": point_records,
    }


def analyze(path: str | Path) -> dict[str, Any]:
    records = _load(path)
    models: dict[str, Callable[[float, float], float]] = {
        "hansen": lambda x, temperature: float(hansen_gap_ev(x, temperature)),
        "published_seiler": lambda x, temperature: float(
            published_seiler_gap_ev(x, temperature)
        ),
        "laurenti": lambda x, temperature: float(laurenti_gap_ev(x, temperature)),
        "provisional_hansen_pade": lambda x, temperature: float(
            provisional_hansen_pade_gap_ev(x, temperature)
        ),
    }
    independent = [
        record
        for record in records
        if record["composition_provenance_status"]
        == "wet_chemistry_tied_independent"
    ]
    legacy = [record for record in records if not record["present_work"]]
    all_result = _evaluate_subset(records, models)
    independent_result = _evaluate_subset(independent, models)
    legacy_result = _evaluate_subset(legacy, models)

    all_metrics = all_result["metrics"]
    independent_metrics = independent_result["metrics"]
    checks = {
        "all_rows_rmse_within_5_percent_of_hansen": all_metrics[
            "provisional_hansen_pade"
        ]["rmse_mev"]
        <= 1.05 * all_metrics["hansen"]["rmse_mev"],
        "all_rows_mae_improves_over_hansen": all_metrics[
            "provisional_hansen_pade"
        ]["mae_mev"]
        < all_metrics["hansen"]["mae_mev"],
        "all_rows_rmse_beats_published_seiler": all_metrics[
            "provisional_hansen_pade"
        ]["rmse_mev"]
        < all_metrics["published_seiler"]["rmse_mev"],
        "all_rows_rmse_beats_laurenti": all_metrics[
            "provisional_hansen_pade"
        ]["rmse_mev"]
        < all_metrics["laurenti"]["rmse_mev"],
        "independent_low_temperature_rmse_not_worse_than_hansen_by_more_than_0p5mev": independent_metrics[
            "provisional_hansen_pade"
        ]["rmse_mev"]
        <= independent_metrics["hansen"]["rmse_mev"] + 0.5,
    }

    return {
        "schema_version": "1.0",
        "analysis": "provisional Hansen-Pade historical low-temperature screen",
        "temperature_policy": "numeric temperatures used directly; 2-10 K ranges evaluated at 6 K midpoint",
        "all_rows": all_result,
        "independently_composed_present_samples": independent_result,
        "legacy_compositions_not_audited_by_seiler": legacy_result,
        "screen_checks": checks,
        "decision": {
            "historical_screen_passed": all(checks.values()),
            "provisional_status_retained": all(checks.values()),
            "production_equation_authorized": False,
            "static_composition_law_is_controlling_limitation": True,
            "interpretation": (
                "The provisional thermal law does not catastrophically degrade the broader "
                "low-temperature table and improves overall MAE, but its RMSE remains close "
                "to Hansen and the independently composed sample-4 residual exposes the "
                "remaining zero-temperature composition-law limitation."
            ),
        },
        "claim_boundary": [
            "Most legacy compositions were not audited in the Seiler source.",
            "Present-work data reported over 2-10 K are evaluated at the 6 K midpoint.",
            "The screen does not refit alpha or tau.",
            "This screen cannot validate novelty or a universal static composition law."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv",
    )
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.input_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
