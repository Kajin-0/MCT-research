#!/usr/bin/env python3
"""Compare provenance-separated historical HgCdTe constraints with gap equations."""
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
)

Model = Callable[[float, float], float]
MODELS: dict[str, Model] = {
    "schmit_stelzer_1969": schmit_stelzer_1969_gap_ev,
    "hansen_1982": hansen_gap_ev,
    "seiler_1990": seiler_1990_gap_ev,
    "laurenti_reconstructed": laurenti_gap_ev,
    "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    "chu_1983": chu_1983_gap_ev,
}
INDEPENDENT_CUTOFF_COMPARATORS = tuple(
    name for name in MODELS if name != "schmit_stelzer_1969"
)


def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _root_for_target(
    model: Model,
    temperature_k: float,
    target_ev: float,
    lower: float = 0.0,
    upper: float = 0.4,
) -> float | None:
    left, right = float(lower), float(upper)
    f_left = model(left, temperature_k) - target_ev
    f_right = model(right, temperature_k) - target_ev
    if f_left == 0:
        return left
    if f_right == 0:
        return right
    if f_left * f_right > 0:
        return None
    for _ in range(128):
        midpoint = 0.5 * (left + right)
        f_midpoint = model(midpoint, temperature_k) - target_ev
        if abs(f_midpoint) < 1e-14:
            return midpoint
        if f_left * f_midpoint <= 0:
            right = midpoint
            f_right = f_midpoint
        else:
            left = midpoint
            f_left = f_midpoint
    return 0.5 * (left + right)


def _metrics(residuals_ev: list[float]) -> dict[str, float]:
    count = len(residuals_ev)
    return {
        "count": count,
        "mae_meV": 1000 * sum(abs(value) for value in residuals_ev) / count,
        "rmse_meV": 1000
        * math.sqrt(sum(value * value for value in residuals_ev) / count),
        "bias_meV": 1000 * sum(residuals_ev) / count,
        "max_abs_meV": 1000 * max(abs(value) for value in residuals_ev),
    }


def _sign_interval_status(values_ev: tuple[float, float], relation: str) -> str:
    if relation == "lt":
        hits = [value < 0 for value in values_ev]
    elif relation == "gt":
        hits = [value > 0 for value in values_ev]
    else:
        raise ValueError("sign relation must be lt or gt")
    if all(hits):
        return "satisfied_entire_interval"
    if not any(hits):
        return "violated_entire_interval"
    return "ambiguous_within_composition_interval"


def analyze(specimens_path: str | Path, records_path: str | Path) -> dict[str, object]:
    specimens = load_json(specimens_path)
    records = load_json(records_path)

    schmit_specimens = [
        row
        for row in specimens
        if row["specimen_id"].startswith("schmit_detector_")
    ]
    cutoff: dict[str, dict[str, dict[str, float]]] = {}
    for x_mode, key in (
        ("nominal", "composition_nominal"),
        ("adjusted", "composition_adjusted"),
    ):
        model_residuals = {name: [] for name in MODELS}
        for specimen in schmit_specimens:
            composition = float(specimen[key])
            for temperature_k, _wavelength_um, reported_ev in specimen["points"]:
                for name, model in MODELS.items():
                    model_residuals[name].append(
                        model(composition, float(temperature_k)) - float(reported_ev)
                    )
        cutoff[x_mode] = {
            name: _metrics(values) for name, values in model_residuals.items()
        }

    sign_results = []
    for row in records:
        if row["value_status"] != "sign_constraint":
            continue
        composition = float(row["composition_reported"])
        sigma = float(row["composition_sigma"])
        lower = max(0.0, composition - sigma)
        upper = min(1.0, composition + sigma)
        by_model = {}
        for name, model in MODELS.items():
            endpoint_values = (
                model(lower, float(row["temperature_K"])),
                model(upper, float(row["temperature_K"])),
            )
            by_model[name] = {
                "gap_at_lower_x_meV": 1000 * endpoint_values[0],
                "gap_at_upper_x_meV": 1000 * endpoint_values[1],
                "critical_composition": _root_for_target(
                    model, float(row["temperature_K"]), 0.0
                ),
                "status": _sign_interval_status(endpoint_values, row["relation"]),
            }
        sign_results.append(
            {
                "observation_id": row["observation_id"],
                "temperature_K": row["temperature_K"],
                "relation": row["relation"],
                "composition_interval": [lower, upper],
                "models": by_model,
            }
        )

    point_results = []
    for row in records:
        if row["relation"] not in {"eq", "approx"}:
            continue
        by_model = {}
        composition = float(row["composition_reported"])
        temperature = float(row["temperature_K"])
        target = float(row["reported_value_eV"])
        for name, model in MODELS.items():
            prediction = model(composition, temperature)
            required_composition = _root_for_target(model, temperature, target)
            step = 1e-5
            upper_x = min(1.0, composition + step)
            lower_x = max(0.0, composition - step)
            derivative = (
                model(upper_x, temperature) - model(lower_x, temperature)
            ) / (upper_x - lower_x)
            by_model[name] = {
                "prediction_meV": 1000 * prediction,
                "residual_meV": 1000 * (prediction - target),
                "required_composition": required_composition,
                "required_composition_shift": (
                    None
                    if required_composition is None
                    else required_composition - composition
                ),
                "dEg_dx_eV_per_x": derivative,
            }
        point_results.append(
            {
                "observation_id": row["observation_id"],
                "measurement_class": row["measurement_class"],
                "reported_value_meV": 1000 * target,
                "reported_sigma_meV": (
                    None
                    if row["reported_sigma_eV"] is None
                    else 1000 * float(row["reported_sigma_eV"])
                ),
                "temperature_K": temperature,
                "composition_reported": composition,
                "models": by_model,
            }
        )

    adjusted_rank = sorted(
        cutoff["adjusted"],
        key=lambda name: cutoff["adjusted"][name]["mae_meV"],
    )
    independent_rank = sorted(
        INDEPENDENT_CUTOFF_COMPARATORS,
        key=lambda name: cutoff["adjusted"][name]["mae_meV"],
    )
    sign_4k = next(item for item in sign_results if item["temperature_K"] == 4)
    mccombe = next(
        item
        for item in point_results
        if item["observation_id"] == "mccombe1970_sample4_gap"
    )
    hgte_30k = next(
        item
        for item in point_results
        if item["observation_id"] == "groves1967_hgte_gap_30K"
    )
    minimum_mccombe = min(
        mccombe["models"],
        key=lambda name: abs(mccombe["models"][name]["residual_meV"]),
    )
    minimum_hgte = min(
        hgte_30k["models"],
        key=lambda name: abs(hgte_30k["models"][name]["residual_meV"]),
    )

    return {
        "schema_version": "1.0",
        "analysis": "historical HgCdTe exact-constraint comparison",
        "model_names": list(MODELS),
        "schmit_cutoff_comparison": cutoff,
        "schmit_adjusted_mae_rank": adjusted_rank,
        "schmit_adjusted_independent_comparator_rank": independent_rank,
        "sign_constraints": sign_results,
        "point_constraints": point_results,
        "decision": {
            "schmit_own_equation_best_on_fit_adjusted_cutoffs": (
                adjusted_rank[0] == "schmit_stelzer_1969"
            ),
            "schmit_ranking_is_independent_validation": False,
            "best_independent_adjusted_cutoff_comparator": independent_rank[0],
            "groves_4K_definite_violations": [
                name
                for name, item in sign_4k["models"].items()
                if item["status"] == "violated_entire_interval"
            ],
            "groves_4K_composition_ambiguous": [
                name
                for name, item in sign_4k["models"].items()
                if item["status"] == "ambiguous_within_composition_interval"
            ],
            "mccombe_all_models_overpredict_at_reported_x": all(
                item["residual_meV"] > 0
                for item in mccombe["models"].values()
            ),
            "mccombe_smallest_absolute_residual_model": minimum_mccombe,
            "mccombe_smallest_absolute_residual_meV": abs(
                mccombe["models"][minimum_mccombe]["residual_meV"]
            ),
            "hgte_30K_smallest_absolute_residual_model": minimum_hgte,
            "strict_global_model_ranking_authorized": False,
            "new_universal_gap_refit_authorized": False,
            "reason": (
                "The exact constraints discriminate some historical formulas and "
                "observation classes, but composition uncertainty, fit-adjusted x "
                "values, model-conditioned magneto-optical extraction, and "
                "incompatible measurement operators prevent a global material-law "
                "ranking."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens-json", required=True)
    parser.add_argument("--records-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.specimens_json, args.records_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
