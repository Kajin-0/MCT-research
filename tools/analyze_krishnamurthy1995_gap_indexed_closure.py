#!/usr/bin/env python3
"""Test the Table II claim that c and m* are directly proportional to Eg.

This is a narrow historical-theory reproduction. The predeclared training range is
1-100 K and the held-out prediction range is 150-300 K. Linear functions of the
printed gap are used only as diagnostics of the paper's stated gap-indexed
interpolation claim; they are not proposed as new HgCdTe material models.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


def _load(path: str | Path) -> dict[str, np.ndarray]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 21:
        raise ValueError("expected the 21-row Krishnamurthy Table II transcription")
    names = {
        "temperature_k": "temperature_k",
        "gap_ev": "gap_mev",
        "gamma": "gamma_reported",
        "c_ev": "c_ev",
        "mass_ratio": "effective_mass_ratio_to_m0",
    }
    data = {
        key: np.asarray([float(row[column]) for row in rows], dtype=float)
        for key, column in names.items()
    }
    data["gap_ev"] *= 1.0e-3
    if not np.all(np.isfinite(np.column_stack(tuple(data.values())))):
        raise ValueError("Table II contains non-finite values")
    if not np.all(np.diff(data["temperature_k"]) > 0.0):
        raise ValueError("temperatures must increase strictly")
    return data


def _fit_affine(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    design = np.column_stack([np.ones(x.size), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    return float(intercept), float(slope)


def _metrics(fractional_error: np.ndarray) -> dict[str, float]:
    return {
        "mean_signed_fractional_error": float(np.mean(fractional_error)),
        "mean_absolute_fractional_error": float(np.mean(np.abs(fractional_error))),
        "rms_fractional_error": float(np.sqrt(np.mean(fractional_error**2))),
        "maximum_absolute_fractional_error": float(np.max(np.abs(fractional_error))),
    }


def analyze(path: str | Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    data = _load(path)
    temperature = data["temperature_k"]
    gap = data["gap_ev"]
    gamma = data["gamma"]
    c_ev = data["c_ev"]
    mass_ratio = data["mass_ratio"]

    robust = temperature <= 300.0
    train = temperature <= 100.0
    heldout = (temperature > 100.0) & (temperature <= 300.0)
    high_temperature = temperature > 300.0

    strict_gap_ratio = gap / gap[0]
    strict_c_ratio = c_ev / c_ev[0]
    strict_c_fractional_error = strict_gap_ratio / strict_c_ratio - 1.0
    strict_mass_fractional_error = strict_gap_ratio / mass_ratio - 1.0
    c_over_gap = c_ev / gap

    c_intercept, c_slope = _fit_affine(gap[train], c_ev[train])
    gamma_intercept, gamma_slope = _fit_affine(gap[train], gamma[train])
    c_prediction = c_intercept + c_slope * gap
    gamma_prediction = gamma_intercept + gamma_slope * gap
    mass_prediction = (c_prediction / gamma_prediction) / (
        c_prediction[0] / gamma_prediction[0]
    )

    c_fractional_error = c_prediction / c_ev - 1.0
    gamma_fractional_error = gamma_prediction / gamma - 1.0
    mass_fractional_error = mass_prediction / mass_ratio - 1.0

    rows: list[dict[str, Any]] = []
    for index in range(temperature.size):
        if train[index]:
            scope = "train_1_100k"
        elif heldout[index]:
            scope = "heldout_150_300k"
        else:
            scope = "high_temperature_extrapolation"
        rows.append(
            {
                "temperature_k": float(temperature[index]),
                "gap_ev": float(gap[index]),
                "scope": scope,
                "c_reported_ev": float(c_ev[index]),
                "c_gap_indexed_ev": float(c_prediction[index]),
                "c_error_mev": float(1.0e3 * (c_prediction[index] - c_ev[index])),
                "c_fractional_error": float(c_fractional_error[index]),
                "gamma_reported": float(gamma[index]),
                "gamma_gap_indexed": float(gamma_prediction[index]),
                "gamma_fractional_error": float(gamma_fractional_error[index]),
                "mass_ratio_reported": float(mass_ratio[index]),
                "mass_ratio_gap_indexed": float(mass_prediction[index]),
                "mass_ratio_fractional_error": float(mass_fractional_error[index]),
                "strict_gap_ratio": float(strict_gap_ratio[index]),
                "strict_c_ratio_reported": float(strict_c_ratio[index]),
            }
        )

    heldout_c_error_mev = 1.0e3 * (c_prediction[heldout] - c_ev[heldout])
    heldout_gamma_error = gamma_prediction[heldout] - gamma[heldout]
    near_turnover = (temperature == 10.0) | (temperature == 20.0)

    summary: dict[str, Any] = {
        "analysis": "Krishnamurthy 1995 Table II gap-indexed closure",
        "source_kind": "historical_calculated_HPTB_plus_valence_force_field_data",
        "experimental_validation": False,
        "paper_claim_tested": (
            "m* and c are directly proportional to the gap; gamma and c can be "
            "interpolated for any positive gap"
        ),
        "strict_direct_proportionality_1_300k": {
            "c_over_gap_fractional_change_1_to_300k": float(
                c_over_gap[temperature == 300.0][0] / c_over_gap[0] - 1.0
            ),
            "c_ratio_from_gap_ratio": _metrics(strict_c_fractional_error[robust]),
            "mass_ratio_from_gap_ratio": _metrics(
                strict_mass_fractional_error[robust]
            ),
            "decision": "strict_mathematical_proportionality_not_supported",
        },
        "predeclared_split": {
            "training_temperature_k": [1.0, 100.0],
            "heldout_temperatures_k": [150.0, 200.0, 250.0, 300.0],
            "high_temperature_extrapolation_k": [350.0, 600.0],
        },
        "gap_indexed_affine_diagnostic": {
            "c_of_gap": {
                "intercept_ev": c_intercept,
                "slope": c_slope,
                "heldout_maximum_absolute_error_mev": float(
                    np.max(np.abs(heldout_c_error_mev))
                ),
                "heldout_rms_error_mev": float(
                    np.sqrt(np.mean(heldout_c_error_mev**2))
                ),
                "heldout_fractional_metrics": _metrics(
                    c_fractional_error[heldout]
                ),
            },
            "gamma_of_gap": {
                "intercept_reported_units": gamma_intercept,
                "slope_reported_units_per_ev": gamma_slope,
                "heldout_maximum_absolute_error": float(
                    np.max(np.abs(heldout_gamma_error))
                ),
                "heldout_rms_error": float(
                    np.sqrt(np.mean(heldout_gamma_error**2))
                ),
                "heldout_fractional_metrics": _metrics(
                    gamma_fractional_error[heldout]
                ),
            },
            "reconstructed_mass_ratio": {
                "heldout_fractional_metrics": _metrics(
                    mass_fractional_error[heldout]
                ),
                "decision": (
                    "gap_indexed_interpolation_supported_below_300k_at_few_percent"
                ),
            },
        },
        "low_temperature_turnover_identifiability": {
            "temperature_pair_k": [10.0, 20.0],
            "gap_difference_mev": float(
                1.0e3 * np.diff(gap[near_turnover])[0]
            ),
            "c_difference_mev": float(
                1.0e3 * np.diff(c_ev[near_turnover])[0]
            ),
            "gamma_difference": float(np.diff(gamma[near_turnover])[0]),
            "resolved_independent_temperature_effect": False,
            "reason": (
                "the near-degenerate-gap differences are at the printed-rounding "
                "and historical model-accuracy floor"
            ),
        },
        "high_temperature_stop": {
            "maximum_c_fractional_error_350_600k": float(
                np.max(np.abs(c_fractional_error[high_temperature]))
            ),
            "maximum_gamma_fractional_error_350_600k": float(
                np.max(np.abs(gamma_fractional_error[high_temperature]))
            ),
            "maximum_mass_fractional_error_350_600k": float(
                np.max(np.abs(mass_fractional_error[high_temperature]))
            ),
            "decision": (
                "do_not_extrapolate_the_low_temperature_gap_indexed_diagnostic_above_300k"
            ),
        },
        "scientific_decision": (
            "Read the paper's direct-proportionality language qualitatively, not "
            "literally. Table II supports smooth gap-indexed interpolation of c, "
            "gamma, and their mass ratio below 300 K without resolving an "
            "additional independent temperature variable."
        ),
        "limitations": [
            "The source is historical calculated data, not experiment.",
            "The affine relations are diagnostics of one table, not new material laws.",
            "The split contains only four held-out temperatures from one calculation.",
            "Printed values have no datum-level uncertainty and are rounded.",
            "The absolute convention of gamma remains intentionally uninferred.",
        ],
        "falsification_criteria": [
            "Unrounded values that produce more than 5 percent held-out mass error below 300 K would reject the gap-indexed closure.",
            "Independent calculations at matched gap but different temperature that differ beyond uncertainty would resolve an explicit temperature variable.",
            "Experimental velocity or mass data with more than 5 percent residual after gap indexing would strengthen non-gap temperature renormalization.",
        ],
    }
    return rows, summary


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
        default="data/theory/krishnamurthy1995_hg078cd022_table2.csv",
    )
    parser.add_argument("--output-csv")
    parser.add_argument("--summary-json")
    args = parser.parse_args()

    rows, summary = analyze(args.input_csv)
    if args.output_csv:
        _write_csv(args.output_csv, rows)
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
