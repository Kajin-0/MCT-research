#!/usr/bin/env python3
"""Screen historical HgCdTe equations against the Guldner transition series."""
from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable
from pathlib import Path

from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import (
    chu_1983_gap_ev,
    schmit_stelzer_1969_gap_ev,
    seiler_1990_gap_ev,
    weiler_1977_gap_ev,
    wiley_dexter_1969_gap_ev,
)

Model = Callable[[float, float], float]
MODELS: dict[str, Model] = {
    "schmit_stelzer_1969": schmit_stelzer_1969_gap_ev,
    "wiley_dexter_1969": wiley_dexter_1969_gap_ev,
    "weiler_1977": weiler_1977_gap_ev,
    "hansen_1982": hansen_gap_ev,
    "seiler_1990": seiler_1990_gap_ev,
    "laurenti_reconstructed": laurenti_gap_ev,
    "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    "chu_1983": chu_1983_gap_ev,
}


def load_series(path: str | Path) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported Guldner series schema")
    if data.get("data_status") != (
        "secondary exact transcription with primary-figure consistency screen"
    ):
        raise ValueError("Guldner series promotion boundary changed")
    if len(data.get("rows", [])) != 12:
        raise ValueError("Guldner series must contain 12 attributed rows")
    return data


def root_at_temperature(model: Model, temperature_k: float) -> float:
    left, right = 0.0, 0.4
    f_left = model(left, temperature_k)
    f_right = model(right, temperature_k)
    if f_left * f_right > 0:
        raise ValueError("zero crossing is not bracketed")
    for _ in range(160):
        midpoint = 0.5 * (left + right)
        f_midpoint = model(midpoint, temperature_k)
        if f_left * f_midpoint <= 0:
            right = midpoint
            f_right = f_midpoint
        else:
            left = midpoint
            f_left = f_midpoint
    return 0.5 * (left + right)


def metrics(values: list[float]) -> dict[str, float]:
    return {
        "count": len(values),
        "mae_meV": 1000 * sum(abs(value) for value in values) / len(values),
        "rmse_meV": 1000
        * math.sqrt(sum(value * value for value in values) / len(values)),
        "bias_meV": 1000 * sum(values) / len(values),
        "max_abs_meV": 1000 * max(abs(value) for value in values),
    }


def crossing_status(value: float, lower: float, upper: float) -> str:
    if lower <= value <= upper:
        return "inside_reported_transition_interval"
    if value < lower:
        return "below_reported_transition_interval"
    return "above_reported_transition_interval"


def analyze(series_path: str | Path) -> dict[str, object]:
    series = load_series(series_path)
    temperature = float(series["temperature_K"])
    rows = series["rows"]
    transition = series["primary_transition_composition"]
    lower = float(transition["value"]) - float(transition["sigma"])
    upper = float(transition["value"]) + float(transition["sigma"])

    comparisons: dict[str, dict[str, float | str]] = {}
    for name, model in MODELS.items():
        residuals = [
            model(float(row["x"]), temperature) - float(row["gap_eV"])
            for row in rows
        ]
        zero = root_at_temperature(model, temperature)
        comparisons[name] = {
            **metrics(residuals),
            "critical_composition": zero,
            "critical_composition_status": crossing_status(zero, lower, upper),
        }

    mae_rank = sorted(comparisons, key=lambda name: comparisons[name]["mae_meV"])
    inside = [
        name
        for name, item in comparisons.items()
        if item["critical_composition_status"]
        == "inside_reported_transition_interval"
    ]
    outside = [name for name in comparisons if name not in inside]
    hansen_pade_difference = abs(
        float(comparisons["hansen_1982"]["mae_meV"])
        - float(comparisons["provisional_hansen_pade"]["mae_meV"])
    )

    return {
        "schema_version": "1.0",
        "analysis": "Guldner low-temperature transition-series screen",
        "temperature_K": temperature,
        "row_count": len(rows),
        "data_status": series["data_status"],
        "reported_transition_interval": [lower, upper],
        "model_comparisons": comparisons,
        "mae_rank": mae_rank,
        "decision": {
            "lowest_mae_model": mae_rank[0],
            "lowest_mae_meV": comparisons[mae_rank[0]]["mae_meV"],
            "hansen_pade_mae_difference_meV": hansen_pade_difference,
            "transition_interval_satisfied_models": inside,
            "transition_interval_rejected_models": outside,
            "hansen_over_pade_ranking_authorized": False,
            "strict_material_law_ranking_authorized": False,
            "primary_exact_point_promotion_authorized": False,
            "new_universal_gap_refit_authorized": False,
            "reason": (
                "The secondary exact transcription, primary figure screen, and "
                "reported transition composition can reject inconsistent low-"
                "temperature crossings. Pointwise composition uncertainties and a "
                "primary numerical table remain unavailable, while Hansen and the "
                "provisional Pade form differ by less than one tenth of a meV in "
                "series MAE."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.series_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
