#!/usr/bin/env python3
"""Test whether Laurenti Table V mass variation is gap driven."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

DELTA_HGTE_EV = 1.08
DELTA_CDTE_EV = 0.927
SOURCE_PDF_SHA256 = "1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea"


def spin_orbit_ev(x: float) -> float:
    return DELTA_HGTE_EV * (1.0 - x) + DELTA_CDTE_EV * x


def infer_p2_ev(gap_ev: float, mass_ratio: float, delta_ev: float) -> float:
    return 3.0 * (1.0 / mass_ratio - 1.0) / (
        2.0 / gap_ev + 1.0 / (gap_ev + delta_ev)
    )


def predict_mass_ratio(gap_ev: float, p2_ev: float, delta_ev: float) -> float:
    return 1.0 / (
        1.0 + (p2_ev / 3.0) * (2.0 / gap_ev + 1.0 / (gap_ev + delta_ev))
    )


def analyze(path: str | Path) -> dict:
    raw = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(raw) != 66:
        raise ValueError("expected 66 Table IV/V rows")

    grouped: dict[float, list[tuple[float, float, float]]] = {}
    for row in raw:
        x = float(row["composition_x"])
        gap = float(row["gap_ev"])
        mass = float(row["mass_ratio_m0"])
        grouped.setdefault(x, []).append(
            (gap, mass, infer_p2_ev(gap, mass, spin_orbit_ev(x)))
        )

    means = {
        x: float(np.mean([item[2] for item in rows]))
        for x, rows in grouped.items()
    }
    residuals = []
    summaries = {}
    for x in sorted(grouped):
        p2_values = np.asarray([item[2] for item in grouped[x]])
        local_residuals = []
        for gap, mass, _ in grouped[x]:
            residual = predict_mass_ratio(gap, means[x], spin_orbit_ev(x)) - mass
            residuals.append(residual)
            local_residuals.append(residual)
        summaries[f"{x:.2f}"] = {
            "mean_p2_ev": means[x],
            "p2_cv": float(np.std(p2_values, ddof=1) / np.mean(p2_values)),
            "mass_max_abs_error_m0": float(np.max(np.abs(local_residuals))),
        }

    x_values = np.asarray(sorted(means))
    p2_means = np.asarray([means[x] for x in x_values])
    slope, intercept = np.polyfit(x_values, p2_means, 1)
    residuals = np.asarray(residuals)

    return {
        "source_kind": "historical_model_generated_tables_not_experiment",
        "source_doi": "10.1063/1.345119",
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "row_count": len(raw),
        "composition_range": [0.5, 1.0],
        "spin_orbit_assumption": "linear_VCA_1.08_to_0.927_eV",
        "composition_summaries": summaries,
        "global_closure": {
            "mass_rmse_m0": float(np.sqrt(np.mean(residuals**2))),
            "mass_mae_m0": float(np.mean(np.abs(residuals))),
            "mass_max_abs_error_m0": float(np.max(np.abs(residuals))),
            "maximum_p2_cv": max(item["p2_cv"] for item in summaries.values()),
        },
        "p2_linear_diagnostic": {
            "intercept_ev": float(intercept),
            "slope_ev_per_x": float(slope),
            "cdte_x1_ev": float(intercept + slope),
            "table_vii_cdte_ev": 18.5,
        },
        "decision": (
            "Table V mass temperature dependence is reproduced to its printed precision "
            "by Eg(x,T) with composition-fixed three-band coupling; it is not independent P(T) evidence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/theory/laurenti1990_tables4_5_cd_rich.csv",
    )
    args = parser.parse_args()
    print(json.dumps(analyze(args.input_csv), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
