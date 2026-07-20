#!/usr/bin/env python3
"""Audit the recovered Herrmann 1992/1993 HgCdTe model chain."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median
from typing import Any

EXPECTED_ROWS = [
    [0.140, 300, 70, 24.0, 10.6, 12.0, 2000, 698, 12],
    [0.222, 80, 119, 2.9, 2.0, 1.4, 480, 508, 13],
    [0.230, 80, 132, 4.4, 1.5, 2.2, 1040, 656, 4],
    [0.290, 85, 228, 4.2, 2.3, 2.1, 840, 843, 3],
    [0.290, 245, 264, 4.0, 10.4, 2.0, 1120, 678, 6],
    [0.320, 300, 317, 19.0, 10.6, 9.8, 2030, 1577, 9],
    [0.344, 300, 350, 8.3, 9.7, 4.2, 1060, 1078, 14],
    [0.480, 80, 531, 9.4, 6.0, 4.8, 1000, 1994, 6],
]
EXPECTED_COMPONENTS = {
    "urbach_branch": "complete",
    "tail_temperature_relation": "form_complete_parameters_source_specific",
    "band_filling_factor": "incomplete_symbolic_approximation",
    "transition_continuity": "conditional_on_missing_definitions",
}
REQUIRED_DEPENDENCY_TERMS = {
    "Anderson 1980",
    "Anderson 1977",
    "Herrmann 1992",
    "BFF_lh",
    "quasi-Fermi",
    "Kane",
}
ASSET_SHA256 = "f7c470601fef398239d574134f61282bef4848984e6d0178e79ba3137a53c56d"


def _close(actual: Any, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Herrmann readiness schema")

    sources = {row["source_id"]: row for row in payload["sources"]}
    if set(sources) != {"herrmann_1992", "herrmann_1993"}:
        raise ValueError("Herrmann source inventory changed")
    if sources["herrmann_1992"]["full_text_recovered"] is not False:
        raise ValueError("Herrmann 1992 full text was not recovered in this tranche")
    if sources["herrmann_1993"]["full_text_recovered"] is not True:
        raise ValueError("Herrmann 1993 companion full text is required")
    if sources["herrmann_1993"]["input_asset_sha256"] != ASSET_SHA256:
        raise ValueError("Herrmann 1993 asset hash changed")
    if any(row["copyrighted_source_committed"] is not False for row in sources.values()):
        raise ValueError("copyrighted source content may not be committed")

    components = {
        row["id"]: row["status"] for row in payload["explicit_components"]
    }
    if components != EXPECTED_COMPONENTS:
        raise ValueError("Herrmann component-readiness inventory changed")
    dependencies = payload["missing_dependencies"]
    if not isinstance(dependencies, list) or len(dependencies) < 6:
        raise ValueError("Herrmann missing-dependency inventory is incomplete")
    joined_dependencies = "\n".join(str(value) for value in dependencies)
    for term in REQUIRED_DEPENDENCY_TERMS:
        if term not in joined_dependencies:
            raise ValueError(f"Herrmann missing dependency not preserved: {term}")

    semantics = payload["table_i_semantics"]
    if semantics["status"] != "exact_secondary_model_validation_table":
        raise ValueError("Herrmann Table I status changed")
    if semantics["row_count"] != 8 or semantics["independent_specimen_gap_evidence"]:
        raise ValueError("Herrmann Table I evidence authority changed")
    if semantics["universal_gap_fit_authorized"]:
        raise ValueError("Herrmann Table I cannot authorize a universal gap fit")

    rows = payload["table_i_rows"]
    if len(rows) != len(EXPECTED_ROWS):
        raise ValueError("Herrmann Table I row count changed")
    for row_index, (row, expected) in enumerate(zip(rows, EXPECTED_ROWS, strict=True)):
        if len(row) != 9:
            raise ValueError(f"Herrmann Table I row {row_index + 1} has wrong width")
        for column_index, (actual, target) in enumerate(zip(row, expected, strict=True)):
            _close(actual, target, f"Table I row {row_index + 1} column {column_index + 1}")

    transition_errors = [float(row[5]) - float(row[4]) for row in rows]
    transition_absolute_errors = [abs(value) for value in transition_errors]
    absorption_ratios = [float(row[7]) / float(row[6]) for row in rows]
    geometric_mean_ratio = math.exp(
        sum(math.log(value) for value in absorption_ratios) / len(absorption_ratios)
    )
    maximum_factor_error = max(
        max(absorption_ratios), 1.0 / min(absorption_ratios)
    )

    decision = payload["decision"]
    expected_decision = {
        "complete_model_reconstructable": False,
        "implementation_authorized": False,
        "exact_transition_table_diagnostics_authorized": True,
        "universal_gap_fit_authorized": False,
        "hybrid_substitution_authorized": False,
    }
    for field, expected in expected_decision.items():
        if decision.get(field) is not expected:
            raise ValueError(f"Herrmann decision field {field} changed")

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "source_count": len(sources),
        "table_i_row_count": len(rows),
        "explicit_component_count": len(components),
        "missing_dependency_count": len(dependencies),
        "transition_offset_signed_mean_error_meV": sum(transition_errors) / len(rows),
        "transition_offset_mean_absolute_error_meV": (
            sum(transition_absolute_errors) / len(rows)
        ),
        "transition_offset_median_absolute_error_meV": median(
            transition_absolute_errors
        ),
        "transition_offset_maximum_absolute_error_meV": max(
            transition_absolute_errors
        ),
        "transition_absorption_median_calculated_to_measured_ratio": median(
            absorption_ratios
        ),
        "transition_absorption_geometric_mean_calculated_to_measured_ratio": (
            geometric_mean_ratio
        ),
        "transition_absorption_maximum_factor_error": maximum_factor_error,
        "copyrighted_source_files_committed": False,
        "decision": decision,
        "claim_boundary": (
            "The exact transition table can be audited as secondary model-validation "
            "evidence. The recovered source chain does not define a complete executable "
            "model, so implementation and universal gap fitting remain blocked."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
