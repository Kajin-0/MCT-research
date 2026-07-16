#!/usr/bin/env python3
"""Analyze the directly digitized Cd-rich Laurenti Figure 2 series.

The task is deliberately narrow. It tests temperature *shape* after anchoring each
specimen to its Camassel 2 K gap. It does not refit a global HgCdTe equation and
it does not pool other measurement classes.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Callable

import numpy as np


def laurenti_gap_ev(x: float, temperature_k: float) -> float:
    static = -0.303 * (1.0 - x) + 1.606 * x - 0.132 * x * (1.0 - x)
    numerator = (
        6.3 * (1.0 - x) - 3.25 * x - 5.92 * x * (1.0 - x)
    ) * 1.0e-4 * temperature_k**2
    denominator = 11.0 * (1.0 - x) + 78.7 * x + temperature_k
    return static + numerator / denominator


def hansen_gap_ev(x: float, temperature_k: float) -> float:
    return (
        -0.302
        + 1.93 * x
        - 0.81 * x**2
        + 0.832 * x**3
        + 5.35e-4 * (1.0 - 2.0 * x) * temperature_k
    )


def _load(path: str | Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 21:
        raise ValueError("expected 3 anchors and 18 Figure 2 markers")
    return rows


def _metrics(residual_mev: np.ndarray) -> dict[str, float]:
    return {
        "mean_signed_mev": float(np.mean(residual_mev)),
        "mean_absolute_mev": float(np.mean(np.abs(residual_mev))),
        "rms_mev": float(np.sqrt(np.mean(residual_mev**2))),
        "maximum_absolute_mev": float(np.max(np.abs(residual_mev))),
    }


def _bounded_composition_metrics(
    model: Callable[[float, float], float],
    temperature_k: np.ndarray,
    measured_shift_mev: np.ndarray,
    nominal_x: float,
    half_width_x: float,
) -> dict[str, float]:
    candidates = np.linspace(nominal_x - half_width_x, nominal_x + half_width_x, 2001)
    best: tuple[float, float, np.ndarray] | None = None
    for x_value in candidates:
        predicted = np.asarray(
            [
                1.0e3 * (model(x_value, t) - model(x_value, 2.0))
                for t in temperature_k
            ],
            dtype=float,
        )
        residual = measured_shift_mev - predicted
        rms = float(np.sqrt(np.mean(residual**2)))
        if best is None or rms < best[0]:
            best = (rms, float(x_value), residual)
    assert best is not None
    return {
        "best_composition_x": best[1],
        "composition_shift": best[1] - nominal_x,
        **_metrics(best[2]),
    }


def analyze(path: str | Path) -> dict[str, object]:
    rows = _load(path)
    anchors: dict[str, float] = {}
    specimen_meta: dict[str, dict[str, float | str]] = {}
    markers: list[dict[str, float | str]] = []

    for row in rows:
        sample = row["sample_id"]
        if row["point_kind"] == "two_kelvin_anchor":
            anchors[sample] = float(row["gap_ev"])
            specimen_meta[sample] = {
                "composition_x": float(row["composition_x"]),
                "composition_sigma_x": float(row["composition_sigma_x"]),
                "growth_method": row["growth_method"],
            }
        elif row["point_kind"] == "digitized_full_square":
            markers.append(
                {
                    "sample_id": sample,
                    "composition_x": float(row["composition_x"]),
                    "temperature_k": float(row["temperature_k"]),
                    "gap_ev": float(row["gap_ev"]),
                    "shift_from_2k_mev": float(row["shift_from_2k_mev"]),
                    "marker_center_x_px": float(row["marker_center_x_px"]),
                    "marker_center_y_px": float(row["marker_center_y_px"]),
                }
            )
        else:
            raise ValueError(f"unexpected point kind: {row['point_kind']}")

    if set(anchors) != {"MCT83", "bulk_reference", "MCT51"}:
        raise ValueError("unexpected specimen set")
    if len(markers) != 18:
        raise ValueError("expected 18 digitized markers")

    model_results: dict[str, object] = {}
    model_functions = {
        "Laurenti_1990_equation_7": laurenti_gap_ev,
        "Hansen_1982_linear_temperature_extrapolation": hansen_gap_ev,
    }

    for model_name, model in model_functions.items():
        pooled_residuals: list[float] = []
        bounded_pooled_residuals: list[float] = []
        specimens: dict[str, object] = {}
        for sample in anchors:
            sample_rows = [row for row in markers if row["sample_id"] == sample]
            temperature = np.asarray([float(row["temperature_k"]) for row in sample_rows])
            measured = np.asarray([float(row["shift_from_2k_mev"]) for row in sample_rows])
            x_value = float(specimen_meta[sample]["composition_x"])
            sigma_x = float(specimen_meta[sample]["composition_sigma_x"])
            predicted = np.asarray(
                [1.0e3 * (model(x_value, t) - model(x_value, 2.0)) for t in temperature]
            )
            residual = measured - predicted
            pooled_residuals.extend(residual.tolist())

            bounded = _bounded_composition_metrics(
                model,
                temperature,
                measured,
                x_value,
                sigma_x,
            )
            bounded_prediction = np.asarray(
                [
                    1.0e3
                    * (
                        model(float(bounded["best_composition_x"]), t)
                        - model(float(bounded["best_composition_x"]), 2.0)
                    )
                    for t in temperature
                ]
            )
            bounded_pooled_residuals.extend((measured - bounded_prediction).tolist())

            endpoint_index = int(np.argmax(temperature))
            specimens[sample] = {
                **specimen_meta[sample],
                "marker_count": len(sample_rows),
                "nominal_composition_metrics": _metrics(residual),
                "bounded_composition_metrics": bounded,
                "highest_temperature_k": float(temperature[endpoint_index]),
                "observed_endpoint_shift_mev": float(measured[endpoint_index]),
                "predicted_endpoint_shift_mev": float(predicted[endpoint_index]),
                "endpoint_residual_mev": float(residual[endpoint_index]),
            }

        model_results[model_name] = {
            "nominal_composition_pooled_metrics": _metrics(
                np.asarray(pooled_residuals, dtype=float)
            ),
            "bounded_composition_pooled_metrics": _metrics(
                np.asarray(bounded_pooled_residuals, dtype=float)
            ),
            "specimens": specimens,
        }

    endpoint_rows = []
    for sample in anchors:
        sample_rows = [row for row in markers if row["sample_id"] == sample]
        endpoint_rows.append(max(sample_rows, key=lambda row: float(row["temperature_k"])))
    endpoint_shifts = np.asarray(
        [float(row["shift_from_2k_mev"]) for row in endpoint_rows], dtype=float
    )

    laurenti_rms = float(
        model_results["Laurenti_1990_equation_7"][
            "nominal_composition_pooled_metrics"
        ]["rms_mev"]
    )
    hansen_rms = float(
        model_results["Hansen_1982_linear_temperature_extrapolation"][
            "nominal_composition_pooled_metrics"
        ]["rms_mev"]
    )

    first_marker = next(row for row in rows if row["point_kind"] == "digitized_full_square")
    summary: dict[str, object] = {
        "analysis": "Laurenti 1990 Figure 2 Cd-rich direct-marker reproduction",
        "source_kind": "digitized_experimental_plus_excitonic_model_corrected_interband_gap",
        "source_pdf_sha256": first_marker["source_pdf_sha256"],
        "page_image_sha256": first_marker["page_image_sha256"],
        "specimen_count": 3,
        "digitized_marker_count": 18,
        "measurement_class": "derivative_absorption_fit_with_3D_direct_allowed_exciton_theory",
        "axis_and_marker_uncertainty": {
            "temperature_digitization_half_width_k": float(
                first_marker["temperature_digitization_half_width_k"]
            ),
            "gap_digitization_half_width_mev": float(
                first_marker["gap_digitization_half_width_mev"]
            ),
            "paper_stated_edge_extraction_accuracy_upper_bound_mev": 3.0,
            "composition_sigma_x": 0.005,
        },
        "observed_near_300k_shift_mev": {
            "mean": float(np.mean(endpoint_shifts)),
            "population_standard_deviation": float(np.std(endpoint_shifts)),
            "range": float(np.max(endpoint_shifts) - np.min(endpoint_shifts)),
            "values": {
                str(row["sample_id"]): float(row["shift_from_2k_mev"])
                for row in endpoint_rows
            },
        },
        "model_results": model_results,
        "rms_ratio_hansen_to_laurenti": hansen_rms / laurenti_rms,
        "scientific_decision": (
            "The three Cd-rich specimens show an approximately 70-73 meV gap "
            "decrease from 2 K to 300 K. Laurenti equation 7 reproduces these "
            "same fitting data at digitization-scale residuals, while extrapolating "
            "the Hansen linear temperature term to x=0.925-0.970 overpredicts the "
            "magnitude by roughly a factor of two and remains grossly inconsistent "
            "after allowing the full reported composition uncertainty."
        ),
        "claim_boundary": [
            "This is not independent validation of Laurenti equation 7 because these specimens contributed to its fit.",
            "The result rejects Cd-rich extrapolation of Hansen's temperature term; it does not challenge Hansen within its intended mercury-rich detector range.",
            "The x=0.955 specimen is a THM bulk reference, while x=0.970 and 0.925 are LPE specimens.",
            "The gaps are obtained from excitonic spectral fits and are not raw quasiparticle-gap measurements.",
            "The data do not identify a microscopic phonon mechanism or unique oscillator parameters.",
        ],
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/laurenti1990_figure2_cd_rich_digitized.csv",
    )
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    summary = analyze(args.input_csv)
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
