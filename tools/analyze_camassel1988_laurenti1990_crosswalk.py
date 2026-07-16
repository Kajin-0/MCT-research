#!/usr/bin/env python3
"""Validate the Camassel 1988 to Laurenti 1990 Cd-rich specimen crosswalk.

The analysis is deliberately narrow. It checks specimen identity, growth-method
classification, exciton-to-gap arithmetic, and the scale of composition uncertainty.
It does not digitize Laurenti Figure 2 or treat the model-corrected gap as a raw
quasiparticle measurement.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


EXPECTED = {
    0.970: ("MCT 83", "LPE", 1.5315, 9.0, 1.5405),
    0.955: ("bulk reference", "THM", 1.4992, 8.7, 1.5079),
    0.925: ("MCT 51", "LPE", 1.4416, 8.2, 1.4498),
}


def load_rows(path: str | Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
    if len(rows) != 3:
        raise ValueError("expected exactly three priority Cd-rich crosswalk rows")
    return rows


def analyze(path: str | Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = load_rows(path)
    derived: list[dict[str, Any]] = []

    for row in rows:
        x = float(row["laurenti_composition_x"])
        if x not in EXPECTED:
            raise ValueError(f"unexpected composition {x}")
        sample, growth, transition_ev, binding_mev, gap_ev = EXPECTED[x]
        if row["camassel_sample_id"] != sample:
            raise ValueError(f"wrong sample identity at x={x}")
        if row["growth_method"] != growth:
            raise ValueError(f"wrong growth method at x={x}")

        reported_transition = float(row["transverse_exciton_energy_ev"])
        reported_binding = float(row["exciton_binding_energy_mev"])
        reported_gap = float(row["derived_interband_gap_ev"])
        closure_gap = reported_transition + reported_binding * 1.0e-3
        closure_residual_mev = 1.0e3 * (reported_gap - closure_gap)

        if abs(reported_transition - transition_ev) > 1.0e-12:
            raise ValueError(f"transition transcription mismatch at x={x}")
        if abs(reported_binding - binding_mev) > 1.0e-12:
            raise ValueError(f"binding transcription mismatch at x={x}")
        if abs(reported_gap - gap_ev) > 1.0e-12:
            raise ValueError(f"gap transcription mismatch at x={x}")

        sigma_x = float(row["composition_sigma_x"])
        composition_energy_scale_mev = sigma_x * 100.0 * 20.0
        derived.append(
            {
                "composition_x": x,
                "sample_id": sample,
                "growth_method": growth,
                "gap_closure_residual_mev": closure_residual_mev,
                "composition_sigma_x": sigma_x,
                "composition_energy_scale_mev": composition_energy_scale_mev,
                "laurenti_extraction_accuracy_upper_bound_mev": 3.0,
                "composition_to_extraction_scale_ratio": (
                    composition_energy_scale_mev / 3.0
                ),
            }
        )

    growth_counts: dict[str, int] = {}
    for row in derived:
        growth_counts[row["growth_method"]] = growth_counts.get(
            row["growth_method"], 0
        ) + 1

    summary: dict[str, Any] = {
        "analysis": "Camassel 1988 to Laurenti 1990 Cd-rich specimen crosswalk",
        "source_kind": "primary_experiment_with_model_corrected_exciton_gap",
        "priority_compositions": [0.970, 0.955, 0.925],
        "specimen_identity_resolved": True,
        "growth_method_counts": growth_counts,
        "all_gap_closure_residuals_below_microelectronvolt": all(
            abs(row["gap_closure_residual_mev"]) < 1.0e-6 for row in derived
        ),
        "composition_energy_scale_mev": 10.0,
        "laurenti_reported_extraction_accuracy_upper_bound_mev": 3.0,
        "composition_uncertainty_dominates_extraction_accuracy": True,
        "corrected_task_wording": (
            "Cd-rich Laurenti series at x=0.970, 0.955, and 0.925; "
            "the x=0.955 specimen is a bulk THM reference, not LPE"
        ),
        "scientific_decision": (
            "The three priority Laurenti curves have specimen-level 2 K anchors and "
            "shared composition uncertainty. They must not be pooled as an all-LPE "
            "series, and the reported interband gaps remain exciton-model corrected."
        ),
        "limitations": [
            "Laurenti states that the same sample series was reused but does not print the sample IDs again in Figure 2.",
            "The transverse exciton energies are experimental; the interband gaps add theoretical exciton binding energies.",
            "The +/-0.005 composition uncertainty is the Camassel Table I standard accuracy and is shared across temperatures for each specimen.",
            "No Figure 2 points have been digitized in this task.",
        ],
        "falsification_criteria": [
            "A primary specimen ledger contradicting the sample identities or growth methods would invalidate the crosswalk.",
            "A later source showing that Laurenti replaced specimens between the two papers would invalidate shared-specimen covariance.",
        ],
    }
    return derived, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        default="data/experimental/camassel1988_laurenti1990_cd_rich_crosswalk.csv",
    )
    parser.add_argument("--summary-json")
    args = parser.parse_args()

    rows, summary = analyze(args.input_csv)
    payload = {"rows": rows, "summary": summary}
    if args.summary_json:
        output = Path(args.summary_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
