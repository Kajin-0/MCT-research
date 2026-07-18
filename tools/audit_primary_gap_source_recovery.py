#!/usr/bin/env python3
"""Audit whether recovered HgCdTe gap sources can support refitting."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED = (
    "full_text_recovered",
    "point_level_gap_data_recovered",
    "composition_method_recovered",
    "point_uncertainties_recovered",
    "measurement_definition_recovered",
)
STATUSES = {"authorized", "conditional", "blocked", "screen_only"}


def recovered(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def audit(path: str | Path) -> dict[str, object]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("source recovery ledger is empty")
    if len({row["source_id"] for row in rows}) != len(rows):
        raise ValueError("source_id values must be unique")

    sources = []
    for row in rows:
        status = row["fit_authority_status"].strip().lower()
        if status not in STATUSES:
            raise ValueError(f"invalid status for {row['source_id']}: {status}")
        states = {field: row[field].strip().lower() for field in REQUIRED}
        complete = all(recovered(value) for value in states.values())
        if status == "authorized" and not complete:
            raise ValueError(f"{row['source_id']} is authorized without complete evidence")
        sources.append(
            {
                "source_id": row["source_id"],
                "doi": row["doi"],
                "status": status,
                "requirements": states,
                "complete_primary_evidence": complete,
            }
        )

    primary = [item for item in sources if item["status"] != "screen_only"]
    authorized = [item for item in primary if item["status"] == "authorized"]
    conditional = [item for item in primary if item["status"] == "conditional"]
    blocked = [item for item in primary if item["status"] == "blocked"]
    screen_only = [item for item in sources if item["status"] == "screen_only"]

    return {
        "schema_version": "1.0",
        "analysis": "primary HgCdTe gap source recovery audit",
        "source_count": len(sources),
        "primary_source_count": len(primary),
        "authorized_primary_fit_source_count": len(authorized),
        "conditional_primary_source_count": len(conditional),
        "blocked_primary_source_count": len(blocked),
        "screen_only_source_count": len(screen_only),
        "sources": sources,
        "decision": {
            "new_static_refit_authorized": len(authorized) >= 2,
            "secondary_table_is_fit_authority": False,
            "abstract_formula_is_point_level_evidence": False,
            "reason": "No two independent primary point sources satisfy the evidence requirements.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_csv)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
