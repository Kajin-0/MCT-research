#!/usr/bin/env python3
"""Audit the precision of Laurenti's temperature-independent composition.

The exact root of the printed empirical equation is separated from what the
reported experimental and coefficient precision can identify. This does not
refit Figure 2 or propose a new HgCdTe material law.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any, Callable

import numpy as np

A_HGTE = 6.3
A_CDTE = -3.25
A_BOWING = -5.92
B_HGTE_K = 11.0
B_CDTE_K = 78.7
SOURCE_PDF_SHA256 = (
    "1e6a8805c6b2dae538b52dff4da40e4b9f10c2e8e204438c9d5917aa819fecea"
)


def thermal_numerator(
    x: float,
    a_hgte: float = A_HGTE,
    a_cdte: float = A_CDTE,
    a_bowing: float = A_BOWING,
) -> float:
    return a_hgte * (1.0 - x) + a_cdte * x + a_bowing * x * (1.0 - x)


def thermal_denominator(x: float, temperature_k: float) -> float:
    return B_HGTE_K * (1.0 - x) + B_CDTE_K * x + temperature_k


def thermal_shift_ev(x: float, temperature_k: float) -> float:
    return (
        1.0e-4
        * thermal_numerator(x)
        * temperature_k**2
        / thermal_denominator(x, temperature_k)
    )


def physical_root(
    a_hgte: float = A_HGTE,
    a_cdte: float = A_CDTE,
    a_bowing: float = A_BOWING,
) -> tuple[float, float]:
    coefficients = [-a_bowing, -a_hgte + a_cdte + a_bowing, a_hgte]
    roots = sorted(
        float(value.real)
        for value in np.roots(coefficients)
        if abs(value.imag) < 1.0e-12
    )
    physical = [value for value in roots if 0.0 <= value <= 1.0]
    if len(physical) != 1:
        raise ValueError("expected exactly one physical composition root")
    return physical[0], next(value for value in roots if value not in physical)


def printed_rounding_interval() -> tuple[float, float]:
    """Stress the root by half a unit in each printed last decimal place."""
    roots = []
    for a_hgte, a_cdte, a_bowing in itertools.product(
        [6.25, 6.35],
        [-3.255, -3.245],
        [-5.925, -5.915],
    ):
        roots.append(physical_root(a_hgte, a_cdte, a_bowing)[0])
    return min(roots), max(roots)


def central_derivative(
    function: Callable[[float], float], value: float, step: float = 1.0e-6
) -> float:
    return float((function(value + step) - function(value - step)) / (2.0 * step))


def analyze() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root, other_root = physical_root()
    rounding_min, rounding_max = printed_rounding_interval()
    slope_300 = central_derivative(
        lambda composition: thermal_shift_ev(composition, 300.0), root
    )

    rows: list[dict[str, Any]] = []
    temperatures = [0.0, 100.0, 200.0, 300.0, 500.0]
    compositions = [
        (0.500, "illustrated_positive_side"),
        (root, "printed_equation_root"),
        (0.505, "reported_rounded_value"),
        (0.550, "illustrated_negative_side"),
    ]
    for composition, label in compositions:
        for temperature in temperatures:
            rows.append(
                {
                    "composition_x": composition,
                    "composition_label": label,
                    "temperature_k": temperature,
                    "thermal_numerator_reported_units": thermal_numerator(composition),
                    "thermal_denominator_k": thermal_denominator(
                        composition, temperature
                    ),
                    "thermal_shift_mev": 1.0e3
                    * thermal_shift_ev(composition, temperature),
                }
            )

    summary: dict[str, Any] = {
        "analysis": (
            "Laurenti 1990 temperature-independent-composition precision audit"
        ),
        "source_doi": "10.1063/1.345119",
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "printed_thermal_numerator": "6.3(1-x)-3.25x-5.92x(1-x)",
        "root_from_printed_coefficients": root,
        "other_algebraic_root": other_root,
        "reported_rounded_composition": 0.505,
        "rounding_difference": 0.505 - root,
        "denominator_positive_for_domain": True,
        "temperature_independence_in_model": (
            "exact_when_thermal_numerator_is_zero"
        ),
        "printed_coefficient_rounding_stress": {
            "assumption": "half_unit_in_last_printed_decimal_place",
            "root_min": rounding_min,
            "root_max": rounding_max,
            "interval_width": rounding_max - rounding_min,
        },
        "experimental_resolution_audit": {
            "reported_edge_accuracy_mev": 3.0,
            "reported_specimen_composition_accuracy": 0.005,
            "thermal_shift_slope_at_300k_ev_per_x": slope_300,
            "shift_for_plus_or_minus_0p005_at_300k_mev": (
                abs(slope_300) * 0.005 * 1.0e3
            ),
            "single_edge_3mev_equivalent_composition_resolution": (
                0.003 / abs(slope_300)
            ),
            "independent_two_edge_3mev_each_equivalent_composition_resolution": (
                np.sqrt(2.0) * 0.003 / abs(slope_300)
            ),
        },
        "illustrated_300k_shifts_mev": {
            "x_0p500": 1.0e3 * thermal_shift_ev(0.500, 300.0),
            "x_0p505": 1.0e3 * thermal_shift_ev(0.505, 300.0),
            "x_0p550": 1.0e3 * thermal_shift_ev(0.550, 300.0),
        },
        "scientific_decision": (
            "x=0.505 is the rounded root of the printed global empirical fit. "
            "The paper brackets the sign reversal experimentally near x=0.5, "
            "but does not resolve the critical composition to three decimal places."
        ),
        "limitations": [
            "No covariance or uncertainty is reported for the fitted thermal coefficients.",
            "The x=0.500 and x=0.550 spectra bracket the sign reversal but are not a dense local composition scan.",
            "The edge values are excitonic-model-corrected absorption edges, not raw quasiparticle gaps.",
            "The coefficient-rounding interval is a formatting sensitivity, not a statistical confidence interval.",
        ],
    }
    return rows, summary


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv")
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    rows, summary = analyze()
    if args.output_csv:
        write_csv(args.output_csv, rows)
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
