#!/usr/bin/env python3
"""Enumerate two-level paired-gap designs and prove the declared minimum.

The candidate family is the complete 2^3 factorial over coded composition,
carrier state and vacancy state. Every subset containing three through eight
specimens is evaluated with the same rank, condition-number, residual-degree and
maximum-leverage thresholds used by the acquisition design oracle.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

from tools.design_minimum_gap_identifiability_dataset import (
    _audit_grade_factorial,
    _matrix_diagnostics,
    design_matrix,
)


def analyze() -> dict[str, Any]:
    full_factorial = _audit_grade_factorial()
    rows: list[dict[str, Any]] = []
    qualifying: list[dict[str, Any]] = []

    for specimen_count in range(3, len(full_factorial) + 1):
        full_rank_diagnostics: list[dict[str, Any]] = []
        audit_grade_diagnostics: list[dict[str, Any]] = []
        for indices in itertools.combinations(range(len(full_factorial)), specimen_count):
            subset = [full_factorial[index] for index in indices]
            matrix, _ = design_matrix(subset)
            diagnostics = _matrix_diagnostics(matrix)
            if diagnostics["full_parameter_identification"]:
                full_rank_diagnostics.append(diagnostics)
            if diagnostics["audit_grade"]:
                audit_grade_diagnostics.append(diagnostics)
                qualifying.append(
                    {
                        "specimen_count": specimen_count,
                        "specimen_ids": [entry.specimen_id for entry in subset],
                        "diagnostics": diagnostics,
                    }
                )

        row: dict[str, Any] = {
            "specimen_count": specimen_count,
            "candidate_subset_count": math.comb(len(full_factorial), specimen_count),
            "full_rank_subset_count": len(full_rank_diagnostics),
            "audit_grade_subset_count": len(audit_grade_diagnostics),
            "minimum_condition_number_among_full_rank": None,
            "minimum_maximum_leverage_among_full_rank": None,
            "maximum_information_determinant_among_full_rank": None,
            "residual_degrees_of_freedom_if_full_rank": 2 * specimen_count - 5,
        }
        if full_rank_diagnostics:
            row.update(
                {
                    "minimum_condition_number_among_full_rank": min(
                        entry["condition_number"] for entry in full_rank_diagnostics
                    ),
                    "minimum_maximum_leverage_among_full_rank": min(
                        entry["maximum_leverage"] for entry in full_rank_diagnostics
                    ),
                    "maximum_information_determinant_among_full_rank": max(
                        entry["information_determinant"]
                        for entry in full_rank_diagnostics
                    ),
                }
            )
        rows.append(row)

    smallest = min(
        (entry["specimen_count"] for entry in qualifying),
        default=None,
    )
    return {
        "schema_version": "1.0",
        "analysis": "exhaustive minimum audit-grade two-level paired-gap design",
        "candidate_family": (
            "all specimen subsets of the 2^3 coded composition x carrier x vacancy factorial"
        ),
        "audit_grade_thresholds": {
            "full_parameter_rank": 5,
            "maximum_condition_number": 5.0,
            "minimum_residual_degrees_of_freedom": 8,
            "maximum_leverage": 0.5,
        },
        "subset_summary": rows,
        "qualifying_designs": qualifying,
        "decision": {
            "smallest_audit_grade_specimen_count": smallest,
            "eight_specimen_full_factorial_is_minimum_in_candidate_family": smallest
            == 8,
            "eight_specimen_design_is_unique_qualifier": len(qualifying) == 1,
            "smaller_design_authorized": False,
        },
        "claim_boundary": [
            "The minimum is proven only within the declared two-level 2^3 candidate family.",
            "The audit-grade thresholds are design criteria, not universal statistical laws.",
            "Alternative continuous or multilevel optimal designs may achieve different tradeoffs.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
