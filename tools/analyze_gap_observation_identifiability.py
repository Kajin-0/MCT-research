#!/usr/bin/env python3
"""Test whether cross-source HgCdTe gap disagreement identifies an observation operator.

The audit is deliberately diagnostic. It asks whether the secondary Chu-attributed
room-temperature gaps can be reconciled with the provisional latent-gap model by a
mechanism that is both sign-compatible and identifiable from the available metadata.
It does not fit or promote a new material band-gap law.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.gap_models import provisional_hansen_pade_gap_ev


def _metrics(values: np.ndarray) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {
        "mean_signed_mev": float(np.mean(array)),
        "mae_mev": float(np.mean(np.abs(array))),
        "rmse_mev": float(np.sqrt(np.mean(array**2))),
        "maximum_absolute_mev": float(np.max(np.abs(array))),
    }


def _load_chu(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            records.append(
                {
                    "composition_x": float(row["composition_x"]),
                    "gap_ev": float(row["gap_ev"]),
                    "alpha_at_gap_cm1": float(row["alpha_at_gap_cm1"]),
                    "temperature_k": float(row["temperature_k"]),
                    "composition_provenance_status": row[
                        "composition_provenance_status"
                    ],
                    "uncertainty_status": row["uncertainty_status"],
                }
            )
    if len(records) != 8:
        raise ValueError("expected eight Chu-attributed room-temperature records")
    return records


def _load_mechanisms(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        records = list(csv.DictReader(stream))
    expected = {
        "hg_vacancy_absorption_edge",
        "absorption_edge_extraction_method",
        "burstein_moss_band_filling",
        "chu_intrinsic_absorption_fit",
    }
    if {row["mechanism"] for row in records} != expected:
        raise ValueError("observation-mechanism ledger is incomplete")
    return records


def _linear_fit(features: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    design = np.column_stack((np.ones(target.size), np.asarray(features, dtype=float)))
    coefficients = np.linalg.lstsq(design, target, rcond=None)[0]
    residual = target - design @ coefficients
    return coefficients, residual


def _leave_one_out(features: np.ndarray, target: np.ndarray) -> np.ndarray:
    matrix = np.asarray(features, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    residuals: list[float] = []
    for heldout in range(target.size):
        mask = np.arange(target.size) != heldout
        coefficients, _ = _linear_fit(matrix[mask], target[mask])
        prediction = np.concatenate(([1.0], matrix[heldout])) @ coefficients
        residuals.append(float(target[heldout] - prediction))
    return np.asarray(residuals, dtype=float)


def analyze(chu_path: str | Path, mechanism_path: str | Path) -> dict[str, Any]:
    records = _load_chu(chu_path)
    mechanisms = _load_mechanisms(mechanism_path)

    composition = np.asarray([row["composition_x"] for row in records], dtype=float)
    temperature = np.asarray([row["temperature_k"] for row in records], dtype=float)
    observed = np.asarray([row["gap_ev"] for row in records], dtype=float)
    alpha_at_gap = np.asarray(
        [row["alpha_at_gap_cm1"] for row in records], dtype=float
    )
    predicted = np.asarray(
        provisional_hansen_pade_gap_ev(composition, temperature), dtype=float
    )
    residual_mev = 1000.0 * (observed - predicted)

    centered_rmse = float(np.sqrt(np.mean((residual_mev - residual_mev.mean()) ** 2)))
    x_alpha_correlation = float(np.corrcoef(composition, alpha_at_gap)[0, 1])
    variance_inflation_factor = float(1.0 / (1.0 - x_alpha_correlation**2))

    normalized = np.column_stack(
        (
            (composition - composition.mean()) / composition.std(),
            (alpha_at_gap - alpha_at_gap.mean()) / alpha_at_gap.std(),
        )
    )
    normalized_condition_number = float(np.linalg.cond(normalized))

    predictor_results: dict[str, Any] = {}
    for name, features in {
        "composition_x": composition.reshape(-1, 1),
        "alpha_at_gap_cm1": alpha_at_gap.reshape(-1, 1),
        "composition_x_plus_alpha_at_gap": np.column_stack(
            (composition, alpha_at_gap)
        ),
    }.items():
        coefficients, training_residual = _linear_fit(features, residual_mev)
        heldout_residual = _leave_one_out(features, residual_mev)
        predictor_results[name] = {
            "coefficients": coefficients.tolist(),
            "training_metrics": _metrics(training_residual),
            "leave_one_out_metrics": _metrics(heldout_residual),
        }

    positive_count = int(np.sum(residual_mev > 0.0))
    negative_count = int(np.sum(residual_mev < 0.0))
    residual_sign_is_predominantly_positive = positive_count >= 6

    mechanism_assessments = {
        "hg_vacancy_absorption_edge": {
            "literature_shift_direction": "negative",
            "literature_scale_mev": [9.0, 12.0],
            "observed_residual_direction": "predominantly_positive",
            "sign_compatible": not residual_sign_is_predominantly_positive,
            "identified": False,
            "decision": (
                "reject as an explanation of the signed Chu discrepancy; the cited "
                "vacancy mechanism lowers the apparent absorption edge"
            ),
        },
        "absorption_edge_extraction_method": {
            "reported_method_scatter_upper_mev": 2.0,
            "constant_offset_removed_rmse_mev": centered_rmse,
            "maximum_observed_residual_mev": float(np.max(np.abs(residual_mev))),
            "magnitude_sufficient": centered_rmse <= 2.0,
            "identified": False,
            "decision": (
                "the <=2 meV method scatter reported in the cited study is too small "
                "to explain the remaining composition-dependent discrepancy"
            ),
        },
        "burstein_moss_band_filling": {
            "literature_shift_direction": "positive",
            "sign_compatible": residual_sign_is_predominantly_positive,
            "sample_carrier_density_available": False,
            "sample_carrier_type_available": False,
            "identified": False,
            "decision": (
                "retain as a plausible observation operator, but do not estimate a "
                "shift without sample-level carrier statistics"
            ),
        },
        "source_specific_composition_or_fit_definition": {
            "sign_compatible": True,
            "identified": False,
            "decision": (
                "composition, alpha_at_gap and source are confounded in the eight-point "
                "secondary table"
            ),
        },
    }

    identification_checks = {
        "primary_chu_point_table_available": False,
        "pointwise_gap_uncertainty_available": False,
        "sample_carrier_statistics_available": False,
        "composition_and_alpha_at_gap_are_separable": variance_inflation_factor < 5.0,
        "vacancy_shift_sign_matches": mechanism_assessments[
            "hg_vacancy_absorption_edge"
        ]["sign_compatible"],
        "extraction_method_scale_is_sufficient": mechanism_assessments[
            "absorption_edge_extraction_method"
        ]["magnitude_sufficient"],
        "burstein_moss_is_quantitatively_testable": False,
    }

    return {
        "schema_version": "1.0",
        "analysis": "HgCdTe gap observation-operator identifiability audit",
        "source_residual_definition": "observed_gap_minus_provisional_latent_gap",
        "source_residuals": {
            "composition_x": composition.tolist(),
            "alpha_at_gap_cm1": alpha_at_gap.tolist(),
            "residual_mev": residual_mev.tolist(),
            "metrics": _metrics(residual_mev),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "constant_offset_removed_rmse_mev": centered_rmse,
            "correlation_with_composition_x": float(
                np.corrcoef(residual_mev, composition)[0, 1]
            ),
            "correlation_with_alpha_at_gap": float(
                np.corrcoef(residual_mev, alpha_at_gap)[0, 1]
            ),
        },
        "confounding_diagnostics": {
            "composition_alpha_at_gap_correlation": x_alpha_correlation,
            "variance_inflation_factor": variance_inflation_factor,
            "normalized_two_predictor_condition_number": normalized_condition_number,
            "interpretation": (
                "The secondary table changes composition and alpha_at_gap together; "
                "their separate observation-operator contributions are not identified."
            ),
        },
        "diagnostic_predictors": predictor_results,
        "mechanism_ledger": mechanisms,
        "mechanism_assessments": mechanism_assessments,
        "identification_checks": identification_checks,
        "decision": {
            "universal_material_law_change_authorized": False,
            "production_observation_operator_identified": False,
            "hg_vacancy_explanation_rejected_by_sign": True,
            "burstein_moss_retained_as_plausible_but_unidentified": True,
            "measurement_class_metadata_must_be_preserved": True,
            "next_required_evidence": [
                "sample-level carrier density and carrier type for the Chu absorption specimens",
                "primary absorption-fit definition and covariance for each reported gap",
                "composition measurements on the same specimens independent of a gap formula",
                "paired magneto-optical and absorption measurements on common material",
            ],
        },
        "claim_boundary": [
            "The Chu point table is a secondary transcription.",
            "The mechanism ledger records literature directions and scales, not sample diagnoses.",
            "Correlation with composition or alpha_at_gap does not identify causation.",
            "No defect concentration or carrier density is available for the eight Chu points.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chu-csv",
        default="data/experimental/chu_sher_2008_table4_4_room_temperature_gap.csv",
    )
    parser.add_argument(
        "--mechanism-csv",
        default="data/evidence/hgcdte_gap_observation_mechanisms.csv",
    )
    parser.add_argument("--output-json")
    args = parser.parse_args()

    result = analyze(args.chu_csv, args.mechanism_csv)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
