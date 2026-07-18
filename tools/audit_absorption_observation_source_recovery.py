#!/usr/bin/env python3
"""Audit modern HgCdTe absorption sources by scientific use case."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

OBSERVATION_STATUSES = {"authorized", "conditional", "blocked", "review_only"}
STATIC_STATUSES = {"authorized", "conditional", "blocked", "screen_only"}
CURVE_STATUSES = {"machine_readable", "figure_only", "not_recovered"}


def yes(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def load_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("absorption source ledger is empty")
    if len({row["source_id"] for row in rows}) != len(rows):
        raise ValueError("source_id values must be unique")
    return rows


def audit(source_path: str | Path, manifest_path: str | Path) -> dict[str, object]:
    rows = load_rows(source_path)
    with Path(manifest_path).open(newline="", encoding="utf-8") as stream:
        figures = list(csv.DictReader(stream))
    if not figures:
        raise ValueError("digitization manifest is empty")

    sources: list[dict[str, object]] = []
    for row in rows:
        observation_status = row["observation_model_authority_status"].strip().lower()
        static_status = row["static_gap_fit_authority_status"].strip().lower()
        curve_status = row["raw_absorption_data_status"].strip().lower()
        if observation_status not in OBSERVATION_STATUSES:
            raise ValueError(f"invalid observation status for {row['source_id']}")
        if static_status not in STATIC_STATUSES:
            raise ValueError(f"invalid static status for {row['source_id']}")
        if curve_status not in CURVE_STATUSES:
            raise ValueError(f"invalid curve status for {row['source_id']}")

        full_text = yes(row["full_text_recovered"])
        machine_readable = yes(row["machine_readable_curve_recovered"])
        measurement_definition = yes(row["measurement_definition_recovered"])
        temperature = yes(row["temperature_metadata_recovered"])
        independent_composition = yes(row["independent_composition_method_recovered"])
        point_uncertainty = False

        complete_observation_authority = all(
            (full_text, machine_readable, measurement_definition, temperature)
        )
        complete_static_authority = all(
            (
                complete_observation_authority,
                independent_composition,
                point_uncertainty,
            )
        )
        if observation_status == "authorized" and not complete_observation_authority:
            raise ValueError(
                f"{row['source_id']} is observation-authorized without complete evidence"
            )
        if static_status == "authorized" and not complete_static_authority:
            raise ValueError(
                f"{row['source_id']} is static-authorized without complete evidence"
            )

        sources.append(
            {
                "source_id": row["source_id"],
                "doi": row["doi"],
                "source_role": row["source_role"],
                "observation_status": observation_status,
                "static_status": static_status,
                "curve_status": curve_status,
                "full_text_recovered": full_text,
                "machine_readable_curve_recovered": machine_readable,
                "cross_method_same_specimen": yes(row["cross_method_same_specimen"]),
                "carrier_type_recovered": yes(row["carrier_type_recovered"]),
                "carrier_density_recovered": yes(row["carrier_density_recovered"]),
                "independent_composition_method_recovered": independent_composition,
                "bandgap_fit_dependency": row["bandgap_fit_dependency"],
                "complete_observation_authority": complete_observation_authority,
                "complete_static_authority": complete_static_authority,
            }
        )

    manifest_sources = {row["source_id"] for row in figures}
    known_sources = {item["source_id"] for item in sources}
    unknown_manifest_sources = manifest_sources.difference(known_sources)
    if unknown_manifest_sources:
        raise ValueError(
            f"manifest references unknown sources: {sorted(unknown_manifest_sources)}"
        )

    conditional = [
        item for item in sources if item["observation_status"] == "conditional"
    ]
    blocked = [item for item in sources if item["observation_status"] == "blocked"]
    review_only = [
        item for item in sources if item["observation_status"] == "review_only"
    ]
    authorized = [
        item for item in sources if item["observation_status"] == "authorized"
    ]
    static_authorized = [
        item for item in sources if item["static_status"] == "authorized"
    ]
    cross_method = [item for item in sources if item["cross_method_same_specimen"]]
    carrier_complete = [
        item
        for item in sources
        if item["carrier_type_recovered"] and item["carrier_density_recovered"]
    ]
    digitization_ready = [
        row
        for row in figures
        if yes(row["source_page_image_archived"])
        and yes(row["axis_calibration_archived"])
    ]

    return {
        "schema_version": "1.0",
        "analysis": "modern primary HgCdTe absorption evidence audit",
        "source_count": len(sources),
        "observation_authorized_count": len(authorized),
        "observation_conditional_count": len(conditional),
        "observation_blocked_count": len(blocked),
        "observation_review_only_count": len(review_only),
        "static_gap_authorized_count": len(static_authorized),
        "cross_method_source_count": len(cross_method),
        "carrier_complete_source_count": len(carrier_complete),
        "figure_manifest_count": len(figures),
        "digitization_ready_figure_count": len(digitization_ready),
        "sources": sources,
        "decision": {
            "observation_model_research_authorized": len(conditional) >= 2,
            "production_observation_model_authorized": len(authorized) >= 2,
            "new_static_gap_refit_authorized": len(static_authorized) >= 2,
            "figure_digitization_authorized_now": len(digitization_ready) > 0,
            "retain_measurement_class_separation": True,
            "reason": (
                "Modern primary studies support absorption-model and mechanism work, "
                "but no machine-readable curve archive with independent composition "
                "and uncertainty supports a universal static gap refit."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources-csv", required=True)
    parser.add_argument("--manifest-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.sources_csv, args.manifest_csv)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
