#!/usr/bin/env python3
"""Audit whether available cross-source data support a new HgCdTe static gap law.

The audit deliberately separates model screening from fit authority.  Eight
room-temperature points transcribed from Chu and Sher Table 4.4 are useful as an
external source screen, but their primary composition metrology and point
uncertainties have not been recovered.  Three Seiler low-temperature samples
have independently reported wet-chemistry compositions.  Candidate corrections
are fit only as diagnostics and must improve both sources before they can be
considered universal.
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
        "mean_signed_mev": float(residual.mean()),
        "mae_mev": float(np.mean(np.abs(residual))),
        "rmse_mev": float(np.sqrt(np.mean(residual**2))),
        "maximum_absolute_mev": float(np.max(np.abs(residual))),
    }


def load_chu_table(path: str | Path) -> list[dict[str, Any]]:
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
                    "claim_boundary": row["claim_boundary"],
                }
            )
    if len(records) != 8:
        raise ValueError("expected eight Chu-Sher Table 4.4 records")
    return records


def load_independent_seiler(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["composition_provenance_status"] != "wet_chemistry_tied_independent":
                continue
            records.append(
                {
                    "sample_number": int(row["sample_number"]),
                    "composition_x": float(row["composition_x"]),
                    "composition_sigma_x": float(row["composition_sigma_x"]),
                    "gap_ev": 1.0e-3 * float(row["gap_mev"]),
                    "gap_sigma_ev": 1.0e-3 * float(row["gap_sigma_mev"]),
                    "temperature_k": 6.0,
                    "reported_temperature_range_k": row["temperature_k_or_range"],
                }
            )
    if {record["sample_number"] for record in records} != {3, 4, 5}:
        raise ValueError("expected independently composed Seiler samples 3, 4 and 5")
    return records


def model_metrics(
    records: list[dict[str, Any]],
    model: Callable[[np.ndarray, np.ndarray], np.ndarray | float],
) -> dict[str, float]:
    x = np.asarray([record["composition_x"] for record in records], dtype=float)
    temperature = np.asarray(
        [record["temperature_k"] for record in records], dtype=float
    )
    observed = np.asarray([record["gap_ev"] for record in records], dtype=float)
    predicted = np.asarray(model(x, temperature), dtype=float)
    return metrics(1000.0 * (observed - predicted))


def invert_composition(
    gap_ev: float,
    temperature_k: float,
    model: Callable[[float, float], float],
    *,
    lower: float = 0.0,
    upper: float = 0.8,
) -> float:
    left = float(lower)
    right = float(upper)
    f_left = float(model(left, temperature_k)) - gap_ev
    f_right = float(model(right, temperature_k)) - gap_ev
    if f_left == 0.0:
        return left
    if f_right == 0.0:
        return right
    if np.signbit(f_left) == np.signbit(f_right):
        raise ValueError("gap does not bracket a composition root")
    for _ in range(256):
        midpoint = 0.5 * (left + right)
        f_midpoint = float(model(midpoint, temperature_k)) - gap_ev
        if abs(f_midpoint) < 1.0e-14 or right - left < 1.0e-13:
            return midpoint
        if np.signbit(f_midpoint) == np.signbit(f_left):
            left = midpoint
            f_left = f_midpoint
        else:
            right = midpoint
    raise RuntimeError("composition inversion did not converge")


def correction_basis(name: str, x: np.ndarray) -> np.ndarray:
    composition = np.asarray(x, dtype=float)
    if name == "constant":
        return np.column_stack((np.ones_like(composition),))
    if name == "affine":
        return np.column_stack((np.ones_like(composition), composition))
    if name == "quadratic":
        return np.column_stack(
            (np.ones_like(composition), composition, composition**2)
        )
    if name == "endpoint_one":
        return np.column_stack((composition * (1.0 - composition),))
    if name == "endpoint_two":
        return np.column_stack(
            (
                composition * (1.0 - composition),
                composition**2 * (1.0 - composition),
            )
        )
    raise ValueError(f"unknown correction basis {name}")


def fit_correction(
    basis_name: str,
    x: np.ndarray,
    residual_ev: np.ndarray,
) -> np.ndarray:
    design = correction_basis(basis_name, x)
    return np.linalg.lstsq(design, residual_ev, rcond=None)[0]


def corrected_prediction(
    basis_name: str,
    coefficients: np.ndarray,
    x: np.ndarray,
    temperature: np.ndarray,
) -> np.ndarray:
    return np.asarray(provisional_hansen_pade_gap_ev(x, temperature), dtype=float) + (
        correction_basis(basis_name, x) @ coefficients
    )


def analyze(chu_path: str | Path, seiler_path: str | Path) -> dict[str, Any]:
    chu_records = load_chu_table(chu_path)
    seiler_records = load_independent_seiler(seiler_path)
    models: dict[str, Callable[[np.ndarray, np.ndarray], np.ndarray | float]] = {
        "hansen": hansen_gap_ev,
        "chu_1983": chu_1983_gap_ev,
        "laurenti": laurenti_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    }
    source_screen = {
        "chu_secondary_room_temperature": {
            name: model_metrics(chu_records, model) for name, model in models.items()
        },
        "seiler_independent_low_temperature": {
            name: model_metrics(seiler_records, model) for name, model in models.items()
        },
    }

    chu_x = np.asarray([record["composition_x"] for record in chu_records])
    chu_temperature = np.asarray([record["temperature_k"] for record in chu_records])
    chu_gap = np.asarray([record["gap_ev"] for record in chu_records])
    provisional_chu = np.asarray(
        provisional_hansen_pade_gap_ev(chu_x, chu_temperature), dtype=float
    )
    chu_residual = chu_gap - provisional_chu

    seiler_x = np.asarray([record["composition_x"] for record in seiler_records])
    seiler_temperature = np.asarray(
        [record["temperature_k"] for record in seiler_records]
    )
    seiler_gap = np.asarray([record["gap_ev"] for record in seiler_records])
    provisional_seiler = np.asarray(
        provisional_hansen_pade_gap_ev(seiler_x, seiler_temperature), dtype=float
    )
    provisional_seiler_rmse = metrics(1000.0 * (seiler_gap - provisional_seiler))[
        "rmse_mev"
    ]

    correction_results: dict[str, Any] = {}
    universal_candidates: list[str] = []
    for basis_name in (
        "constant",
        "affine",
        "quadratic",
        "endpoint_one",
        "endpoint_two",
    ):
        coefficients = fit_correction(basis_name, chu_x, chu_residual)
        room_prediction = corrected_prediction(
            basis_name, coefficients, chu_x, chu_temperature
        )
        room_metrics = metrics(1000.0 * (chu_gap - room_prediction))

        loo_residuals: list[float] = []
        for heldout in range(len(chu_x)):
            mask = np.arange(len(chu_x)) != heldout
            fold_coefficients = fit_correction(
                basis_name, chu_x[mask], chu_residual[mask]
            )
            prediction = corrected_prediction(
                basis_name,
                fold_coefficients,
                np.asarray([chu_x[heldout]]),
                np.asarray([chu_temperature[heldout]]),
            )[0]
            loo_residuals.append(1000.0 * (chu_gap[heldout] - prediction))
        loo_metrics = metrics(np.asarray(loo_residuals))

        seiler_prediction = corrected_prediction(
            basis_name, coefficients, seiler_x, seiler_temperature
        )
        seiler_metrics = metrics(1000.0 * (seiler_gap - seiler_prediction))
        improves_room = loo_metrics["rmse_mev"] < 0.5 * source_screen[
            "chu_secondary_room_temperature"
        ]["provisional_hansen_pade"]["rmse_mev"]
        transfers_to_seiler = seiler_metrics["rmse_mev"] <= min(
            provisional_seiler_rmse + 0.5,
            source_screen["seiler_independent_low_temperature"]["hansen"][
                "rmse_mev"
            ]
            + 0.5,
        )
        if improves_room and transfers_to_seiler:
            universal_candidates.append(basis_name)
        correction_results[basis_name] = {
            "coefficients_ev": coefficients.tolist(),
            "chu_training_metrics": room_metrics,
            "chu_leave_one_composition_out_metrics": loo_metrics,
            "seiler_independent_transfer_metrics": seiler_metrics,
            "improves_chu_secondary_room_screen": improves_room,
            "transfers_to_independent_seiler": transfers_to_seiler,
            "universal_candidate": improves_room and transfers_to_seiler,
        }

    inferred_x = np.asarray(
        [
            invert_composition(
                record["gap_ev"],
                record["temperature_k"],
                lambda composition, temperature: float(
                    provisional_hansen_pade_gap_ev(composition, temperature)
                ),
            )
            for record in chu_records
        ]
    )
    mapping_design = np.column_stack((np.ones_like(chu_x), chu_x))
    mapping_coefficients = np.linalg.lstsq(mapping_design, inferred_x, rcond=None)[0]
    mapped_chu_x = mapping_design @ mapping_coefficients
    mapped_chu_prediction = np.asarray(
        provisional_hansen_pade_gap_ev(mapped_chu_x, chu_temperature), dtype=float
    )
    mapped_seiler_x = (
        mapping_coefficients[0] + mapping_coefficients[1] * seiler_x
    )
    mapped_seiler_prediction = np.asarray(
        provisional_hansen_pade_gap_ev(mapped_seiler_x, seiler_temperature), dtype=float
    )
    mapping_result = {
        "x_effective_equals_intercept_plus_slope_times_reported_x": {
            "intercept": float(mapping_coefficients[0]),
            "slope": float(mapping_coefficients[1]),
        },
        "inferred_effective_compositions": inferred_x.tolist(),
        "effective_minus_reported_x": (inferred_x - chu_x).tolist(),
        "affine_mapping_rms_composition_residual": float(
            np.sqrt(np.mean((inferred_x - mapped_chu_x) ** 2))
        ),
        "chu_room_metrics_after_mapping": metrics(
            1000.0 * (chu_gap - mapped_chu_prediction)
        ),
        "seiler_low_temperature_metrics_after_mapping": metrics(
            1000.0 * (seiler_gap - mapped_seiler_prediction)
        ),
        "mapping_transfers_to_seiler": metrics(
            1000.0 * (seiler_gap - mapped_seiler_prediction)
        )["rmse_mev"]
        <= provisional_seiler_rmse + 0.5,
    }

    data_checks = {
        "chu_point_table_recovered_from_primary_article": False,
        "chu_point_uncertainties_available": False,
        "chu_composition_metrology_recovered": False,
        "at_least_one_minimal_static_correction_transfers_across_sources": bool(
            universal_candidates
        ),
        "affine_composition_mapping_transfers_across_sources": bool(
            mapping_result["mapping_transfers_to_seiler"]
        ),
        "two_sources_are_mutually_consistent_under_one_named_formula": False,
    }

    return {
        "schema_version": "1.0",
        "analysis": "cross-source static HgCdTe composition-law audit",
        "source_screen": source_screen,
        "diagnostic_static_corrections_fit_to_secondary_chu_table": correction_results,
        "diagnostic_composition_scale_mapping": mapping_result,
        "universal_static_correction_candidates": universal_candidates,
        "data_sufficiency_checks": data_checks,
        "decision": {
            "new_static_composition_polynomial_authorized": False,
            "provisional_thermal_kernel_retained": True,
            "chu_1983_retained_as_historical_comparator": True,
            "source_specific_composition_calibration_is_plausible": True,
            "cross_source_static_law_is_identified": False,
            "next_required_evidence": [
                "primary point-level Chu 1991 absorption gaps with composition method and uncertainty",
                "an additional independently composed low-temperature x-Eg series",
                "or new specimen-level composition and gap measurements on a common metrology scale",
            ],
            "interpretation": (
                "The secondary Chu room-temperature table strongly prefers Chu's own "
                "source-specific formula and can be fit by simple energy corrections or an "
                "affine composition remapping, but none transfers to independently composed "
                "Seiler samples. The available evidence does not identify a universal "
                "replacement for the Hansen zero-temperature composition polynomial."
            ),
        },
        "claim_boundary": [
            "The Chu room-temperature points are transcribed from a 2008 secondary table.",
            "The primary point table, composition method and point uncertainties were not recovered.",
            "Diagnostic corrections are not promoted models.",
            "The Seiler low-temperature set contains only three independently composed points.",
            "Cross-source inconsistency may reflect composition calibration, optical-gap definition, sample physics, or formula error."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chu-csv",
        default="data/experimental/chu_sher_2008_table4_4_room_temperature_gap.csv",
    )
    parser.add_argument(
        "--seiler-csv",
        default="data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv",
    )
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.chu_csv, args.seiler_csv)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
