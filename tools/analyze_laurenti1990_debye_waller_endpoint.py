#!/usr/bin/env python3
"""Quantify Laurenti 1990's Debye-Waller endpoint sign test.

The paper fits the measured endpoint gaps with

    Eg(T) = Eg(0) + a T^2 / (b + T)

and separately reports 0-300 K band-edge shifts from a temperature-dependent
empirical-pseudopotential Debye-Waller treatment. The signed gap shift is

    Delta Eg = Delta Ec - Delta Ev.

This script compares those two quantities for CdTe and HgTe. It reproduces a
historical model falsification; it is not experimental validation of a modern
Fan-plus-Debye-Waller calculation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def _load(path: str | Path) -> list[dict[str, Any]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if {row["material"] for row in rows} != {"CdTe", "HgTe"}:
        raise ValueError("expected exactly the CdTe and HgTe endpoint rows")
    result: list[dict[str, Any]] = []
    numeric = (
        "temperature_k",
        "varshni_a_ev_per_k",
        "varshni_b_k",
        "conduction_edge_shift_mev",
        "valence_edge_shift_mev",
        "a_rounding_half_unit_ev_per_k",
        "b_rounding_half_unit_k",
        "edge_rounding_half_unit_mev",
    )
    for row in rows:
        parsed: dict[str, Any] = {"material": row["material"]}
        parsed.update({name: float(row[name]) for name in numeric})
        parsed["source_definition"] = row["source_definition"]
        result.append(parsed)
    return result


def _varshni_shift_mev(a: float, b: float, temperature_k: float) -> float:
    return 1.0e3 * a * temperature_k**2 / (b + temperature_k)


def _interval(values: list[float]) -> list[float]:
    return [float(min(values)), float(max(values))]


def analyze(path: str | Path) -> dict[str, Any]:
    materials: dict[str, Any] = {}
    for row in _load(path):
        temperature = row["temperature_k"]
        empirical = _varshni_shift_mev(
            row["varshni_a_ev_per_k"],
            row["varshni_b_k"],
            temperature,
        )
        debye_waller = (
            row["conduction_edge_shift_mev"]
            - row["valence_edge_shift_mev"]
        )
        residual = debye_waller - empirical

        a0 = row["varshni_a_ev_per_k"]
        b0 = row["varshni_b_k"]
        da = row["a_rounding_half_unit_ev_per_k"]
        db = row["b_rounding_half_unit_k"]
        empirical_corners = [
            _varshni_shift_mev(a, b, temperature)
            for a in (a0 - da, a0 + da)
            for b in (b0 - db, b0 + db)
        ]
        empirical_interval = _interval(empirical_corners)

        edge_half = row["edge_rounding_half_unit_mev"]
        debye_waller_interval = [
            debye_waller - 2.0 * edge_half,
            debye_waller + 2.0 * edge_half,
        ]
        residual_interval = [
            debye_waller_interval[0] - empirical_interval[1],
            debye_waller_interval[1] - empirical_interval[0],
        ]

        materials[row["material"]] = {
            "temperature_k": temperature,
            "empirical_endpoint_gap_shift_mev": empirical,
            "debye_waller_conduction_shift_mev": row[
                "conduction_edge_shift_mev"
            ],
            "debye_waller_valence_shift_mev": row[
                "valence_edge_shift_mev"
            ],
            "debye_waller_gap_shift_mev": debye_waller,
            "residual_debye_waller_minus_empirical_mev": residual,
            "same_sign": (debye_waller > 0.0) == (empirical > 0.0),
            "absolute_magnitude_ratio": abs(debye_waller) / abs(empirical),
            "printed_rounding_empirical_interval_mev": empirical_interval,
            "printed_rounding_debye_waller_interval_mev": debye_waller_interval,
            "printed_rounding_residual_interval_mev": residual_interval,
        }

    cdte = materials["CdTe"]
    hgte = materials["HgTe"]
    endpoint_sign_reversal_empirical = (
        cdte["empirical_endpoint_gap_shift_mev"]
        * hgte["empirical_endpoint_gap_shift_mev"]
        < 0.0
    )
    endpoint_sign_reversal_debye_waller = (
        cdte["debye_waller_gap_shift_mev"]
        * hgte["debye_waller_gap_shift_mev"]
        < 0.0
    )

    return {
        "analysis": "Laurenti 1990 Debye-Waller endpoint falsification",
        "source_kind": "historical_empirical_endpoint_fits_plus_historical_model",
        "experimental_validation_of_modern_theory": False,
        "equations": {
            "empirical_endpoint": "Delta Eg=a*T^2/(b+T)",
            "signed_gap_shift": "Delta Eg=Delta Ec-Delta Ev",
        },
        "materials": materials,
        "endpoint_topology": {
            "empirical_endpoint_sign_reversal": endpoint_sign_reversal_empirical,
            "debye_waller_endpoint_sign_reversal": endpoint_sign_reversal_debye_waller,
        },
        "decision": (
            "The temperature-dependent-form-factor Debye-Waller treatment is "
            "falsified as an endpoint-complete thermal-gap model: it overstates "
            "the CdTe magnitude and predicts the wrong HgTe sign."
        ),
        "claim_boundary": [
            "This does not isolate modern Fan and Debye-Waller terms.",
            "This does not validate any current first-principles implementation.",
            "The source edge shifts and coefficients are printed rounded values.",
            "The result concerns binary endpoints, not alloy interpolation.",
        ],
        "computational_consequence": (
            "A future CdTe/HgTe workflow must retain both Fan-like and "
            "Debye-Waller-like contributions and validate signed endpoint shifts; "
            "static composition accuracy does not establish thermal transferability."
        ),
        "falsification_criteria": [
            "A primary-source recheck showing different endpoint edge shifts invalidates the transcription.",
            "An independently complete historical term omitted from this comparison would narrow the claim to the isolated form-factor contribution.",
            "A modern calculation is successful only if its total signed endpoint shifts agree within a declared uncertainty budget.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/theory/laurenti1990_debye_waller_endpoint_inputs.csv",
    )
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    summary = analyze(args.input_csv)
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
