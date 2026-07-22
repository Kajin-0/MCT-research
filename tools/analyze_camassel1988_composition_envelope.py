#!/usr/bin/env python3
"""Bounded Camassel 1988 composition-accuracy evaluation without refitting."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import numpy as np

try:
    from mct_research import (
        hansen_gap_ev,
        laurenti_gap_ev,
        provisional_hansen_pade_gap_ev,
    )
except ModuleNotFoundError:  # pragma: no cover - direct source-tree fallback
    from src.mct_research.gap_models import (
        hansen_gap_ev,
        laurenti_gap_ev,
        provisional_hansen_pade_gap_ev,
    )

Model = Callable[[float, float], float]
MODELS: dict[str, Model] = {
    "hansen_1982": hansen_gap_ev,
    "laurenti_1990": laurenti_gap_ev,
    "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
}
GRID_POINTS = 20001


def _read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def _hansen_domain_status(x: float) -> str:
    if np.isclose(x, 1.0):
        return "cdte_endpoint"
    if x <= 0.6:
        return "within_declared_composition_evidence"
    if x <= 0.625:
        return "near_boundary_extrapolation"
    return "conjectural_high_x_extrapolation"


def _model_status(model_name: str, x: float) -> str:
    if model_name == "laurenti_1990":
        return "source_lineage_dependent_not_heldout"
    if model_name == "provisional_hansen_pade":
        return (
            "provisional_thermal_reparameterization_inherits_hansen_static_law;"
            + _hansen_domain_status(x)
        )
    return _hansen_domain_status(x)


def _metrics(values: list[float]) -> dict[str, float]:
    data = np.asarray(values, dtype=float)
    return {
        "count": int(data.size),
        "mean_signed_mev": float(np.mean(data)),
        "mae_mev": float(np.mean(np.abs(data))),
        "rmse_mev": float(np.sqrt(np.mean(data**2))),
        "maximum_absolute_mev": float(np.max(np.abs(data))),
    }


def _evaluate_record(
    observation: dict[str, str],
    specimen: dict[str, str],
    model_name: str,
    model: Model,
) -> dict[str, Any]:
    x = float(specimen["composition_x"])
    accuracy = float(specimen["composition_accuracy_x"])
    temperature = float(observation["temperature_k"])
    observed = float(observation["tabulated_gap_ev"])
    lower_x = max(0.0, x - accuracy)
    upper_x = min(1.0, x + accuracy)
    grid = np.linspace(lower_x, upper_x, GRID_POINTS)
    predictions = np.asarray(model(grid, temperature), dtype=float)
    residuals_mev = 1000.0 * (observed - predictions)
    prediction_min = float(np.min(predictions))
    prediction_max = float(np.max(predictions))
    residual_min = float(np.min(residuals_mev))
    residual_max = float(np.max(residuals_mev))
    zero_reachable = residual_min <= 0.0 <= residual_max
    minimum_absolute = 0.0 if zero_reachable else float(np.min(np.abs(residuals_mev)))
    nominal_prediction = float(model(x, temperature))
    nominal_residual = 1000.0 * (observed - nominal_prediction)
    return {
        "observation_id": observation["observation_id"],
        "specimen_id": observation["specimen_id"],
        "composition_group_id": observation["composition_group_id"],
        "modality": observation["modality"],
        "measurement_class": observation["measurement_class"],
        "temperature_k": temperature,
        "composition_x_reported": x,
        "composition_accuracy_x": accuracy,
        "composition_interval_lower": lower_x,
        "composition_interval_upper": upper_x,
        "composition_interval_interpretation": (
            "deterministic_source_accuracy_envelope_not_probability_distribution"
        ),
        "observed_gap_ev": observed,
        "model": model_name,
        "model_domain_status": _model_status(model_name, x),
        "nominal_prediction_ev": nominal_prediction,
        "nominal_residual_mev": nominal_residual,
        "prediction_interval_min_ev": prediction_min,
        "prediction_interval_max_ev": prediction_max,
        "residual_interval_min_mev": residual_min,
        "residual_interval_max_mev": residual_max,
        "minimum_absolute_residual_mev": minimum_absolute,
        "zero_residual_reachable": bool(zero_reachable),
        "fitted_parameters": 0,
    }


def analyze(
    specimens_path: str | Path,
    observations_path: str | Path,
) -> dict[str, Any]:
    specimens = {row["specimen_id"]: row for row in _read_rows(specimens_path)}
    observations = _read_rows(observations_path)
    if len(specimens) != 11:
        raise ValueError("expected 11 Camassel specimens")
    if len(observations) != 13:
        raise ValueError("expected 13 Camassel observations")

    records: list[dict[str, Any]] = []
    for observation in observations:
        specimen = specimens[observation["specimen_id"]]
        if observation["composition_group_id"] != specimen["specimen_id"]:
            raise ValueError("composition group must match canonical specimen identity")
        for model_name, model in MODELS.items():
            records.append(_evaluate_record(observation, specimen, model_name, model))

    residuals_by_model: dict[str, list[float]] = defaultdict(list)
    residuals_by_model_modality: dict[tuple[str, str], list[float]] = defaultdict(list)
    compatible_by_model: dict[str, int] = defaultdict(int)
    for record in records:
        model_name = record["model"]
        residual = float(record["nominal_residual_mev"])
        residuals_by_model[model_name].append(residual)
        residuals_by_model_modality[(model_name, record["modality"])].append(residual)
        compatible_by_model[model_name] += int(record["zero_residual_reachable"])

    summaries: dict[str, Any] = {}
    for model_name in MODELS:
        summaries[model_name] = {
            "all_observations_descriptive_only": _metrics(
                residuals_by_model[model_name]
            ),
            "by_modality_descriptive_only": {
                modality: _metrics(
                    residuals_by_model_modality[(model_name, modality)]
                )
                for modality in ("reflectivity", "absorption_derivative")
            },
            "zero_residual_reachable_count": compatible_by_model[model_name],
            "observation_count": len(observations),
        }

    by_specimen: dict[str, list[dict[str, str]]] = defaultdict(list)
    for observation in observations:
        by_specimen[observation["specimen_id"]].append(observation)
    modality_differences: list[dict[str, Any]] = []
    for specimen_id, specimen_observations in by_specimen.items():
        if len(specimen_observations) != 2:
            continue
        values = {
            row["modality"]: float(row["tabulated_gap_ev"])
            for row in specimen_observations
        }
        if set(values) != {"reflectivity", "absorption_derivative"}:
            raise ValueError("dual-modality specimen has unexpected observation classes")
        signed = 1000.0 * (
            values["reflectivity"] - values["absorption_derivative"]
        )
        modality_differences.append(
            {
                "specimen_id": specimen_id,
                "composition_x_reported": float(
                    specimens[specimen_id]["composition_x"]
                ),
                "reflectivity_minus_absorption_mev": signed,
                "absolute_difference_mev": abs(signed),
                "independent_specimen_count": 1,
            }
        )

    focus_ids = {
        "camassel1988_mct68_absorption": "x_0p50",
        "camassel1988_mct67_absorption": "x_0p55",
    }
    within_domain_focus: dict[str, Any] = {}
    for observation_id, label in focus_ids.items():
        per_model = {
            record["model"]: {
                "nominal_residual_mev": record["nominal_residual_mev"],
                "minimum_absolute_residual_mev": record[
                    "minimum_absolute_residual_mev"
                ],
                "residual_interval_min_mev": record["residual_interval_min_mev"],
                "residual_interval_max_mev": record["residual_interval_max_mev"],
                "zero_residual_reachable": record["zero_residual_reachable"],
                "model_domain_status": record["model_domain_status"],
            }
            for record in records
            if record["observation_id"] == observation_id
        }
        within_domain_focus[label] = per_model

    return {
        "schema_version": "1.0",
        "analysis": (
            "Camassel 1988 deterministic composition-accuracy envelope "
            "without parameter fitting"
        ),
        "source": {
            "doi": "10.1103/PhysRevB.38.3948",
            "temperature_k": 2.0,
            "composition_accuracy_x": 0.005,
            "composition_accuracy_interpretation": (
                "source_reported_standard_accuracy_used_as_deterministic_"
                "sensitivity_envelope_not_gaussian_sigma"
            ),
            "pointwise_energy_covariance": "not_reported",
        },
        "model_lineage": {
            "hansen_1982": "external_source_check_with_domain_limits",
            "laurenti_1990": "camassel_lineage_dependent_not_heldout",
            "provisional_hansen_pade": (
                "diagnostic_only_inherits_hansen_zero_temperature_composition_law"
            ),
        },
        "fitted_parameter_count": 0,
        "records": records,
        "summaries": summaries,
        "same_specimen_modality_differences": modality_differences,
        "hansen_within_domain_focus": within_domain_focus,
        "scientific_decision": {
            "hansen_incompatible_at_x_0p50_across_envelope": not within_domain_focus[
                "x_0p50"
            ]["hansen_1982"]["zero_residual_reachable"],
            "hansen_incompatible_at_x_0p55_across_envelope": not within_domain_focus[
                "x_0p55"
            ]["hansen_1982"]["zero_residual_reachable"],
            "provisional_thermal_term_repairs_static_discrepancy": False,
            "laurenti_independently_validated": False,
            "measurement_classes_poolable_without_observation_model": False,
            "production_equation_authorized": False,
            "manuscript_authorized": False,
        },
        "claim_boundary": [
            (
                "The x=0.50 and x=0.55 Camassel absorption-derived excitonic "
                "gaps are external observations inside Hansen's stated fitted "
                "composition range."
            ),
            (
                "The incompatibility is conditioned on the Camassel excitonic-gap "
                "definition and the deterministic x +/- 0.005 sensitivity envelope."
            ),
            (
                "Laurenti is descriptively closer but belongs to the Camassel "
                "experimental lineage and is not held out."
            ),
            (
                "The provisional Hansen-Pade thermal term is negligible at 2 K "
                "and inherits the Hansen static composition discrepancy."
            ),
            (
                "No probability distribution, p-value, chi-square, source offset, "
                "composition shift, or fitted parameter is introduced."
            ),
        ],
    }


def quantize_for_serialization(value: Any, digits: int = 9) -> Any:
    """Return a deterministic JSON/CSV representation at scientific precision."""
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return value
    if isinstance(value, float):
        return round(value, digits)
    if isinstance(value, list):
        return [quantize_for_serialization(item, digits) for item in value]
    if isinstance(value, dict):
        return {
            key: quantize_for_serialization(item, digits)
            for key, item in value.items()
        }
    raise TypeError(f"unsupported serialization type: {type(value)!r}")


def _write_csv(path: str | Path, records: list[dict[str, Any]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = quantize_for_serialization(records)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(serialized[0]))
        writer.writeheader()
        writer.writerows(serialized)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--specimens-csv",
        default="data/experimental/camassel1988_specimens.csv",
    )
    parser.add_argument(
        "--observations-csv",
        default="data/experimental/camassel1988_table1_observations.csv",
    )
    parser.add_argument("--output-json")
    parser.add_argument("--output-csv")
    args = parser.parse_args()
    result = analyze(args.specimens_csv, args.observations_csv)
    serialized = quantize_for_serialization(result)
    text = json.dumps(serialized, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    if args.output_csv:
        _write_csv(args.output_csv, result["records"])
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
