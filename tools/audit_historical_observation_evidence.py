#!/usr/bin/env python3
"""Fail-closed audit for historical HgCdTe observation evidence."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

SOURCE_STATUSES = {"conditional", "supporting_provenance", "mechanism_only"}
STATIC_STATUSES = {"blocked", "conditional_endpoint"}
MEASUREMENT_CLASSES = {
    "detector_half_peak_cutoff",
    "combined_resonance_fit",
    "gap_sign_or_crossing_constraint",
    "magnetoreflectance_fit",
}
VALUE_STATUSES = {"exact_table", "exact_reported_value", "sign_constraint", "note_added_in_proof"}
RELATIONS = {"eq", "lt", "gt", "approx"}


def load_package(path: str | Path) -> dict[str, object]:
    package_path = Path(path)
    data = json.loads(package_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported historical observation schema")
    includes = data.get("includes")
    if includes is None:
        return data
    required = {"sources", "specimens", "records", "schmit_contract"}
    if set(includes) != required:
        raise ValueError("historical observation include inventory is incomplete")
    parent = package_path.parent
    return {
        "schema_version": data["schema_version"],
        "analysis": data["analysis"],
        "sources": json.loads((parent / includes["sources"]).read_text(encoding="utf-8")),
        "specimen_groups": json.loads((parent / includes["specimens"]).read_text(encoding="utf-8")),
        "observations": json.loads((parent / includes["records"]).read_text(encoding="utf-8")),
        "schmit_observation_contract": json.loads(
            (parent / includes["schmit_contract"]).read_text(encoding="utf-8")
        ),
    }


def audit(package_path: str | Path) -> dict[str, object]:
    package = load_package(package_path)
    sources = package["sources"]
    specimens = package["specimen_groups"]
    observations = package["observations"]
    contract = package["schmit_observation_contract"]

    source_ids = [row["source_id"] for row in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("source_id values must be unique")
    specimen_ids = [row["specimen_id"] for row in specimens]
    if len(specimen_ids) != len(set(specimen_ids)):
        raise ValueError("specimen_id values must be unique")
    observation_ids = [row["observation_id"] for row in observations]
    if len(observation_ids) != len(set(observation_ids)):
        raise ValueError("observation_id values must be unique")

    source_by_id = {row["source_id"]: row for row in sources}
    specimen_by_id = {row["specimen_id"]: row for row in specimens}
    for source in sources:
        if source["primary_source"] != "true":
            raise ValueError(f"{source['source_id']} is not a primary source")
        if source["full_text_recovered"] != "true":
            raise ValueError(f"{source['source_id']} lacks recovered full text")
        if source["copyrighted_source_committed"] != "false":
            raise ValueError(f"{source['source_id']} attempts to commit copyrighted source content")
        if len(source["input_asset_sha256"]) != 64:
            raise ValueError(f"{source['source_id']} lacks a SHA-256 input binding")
        if source["observation_authority_status"] not in SOURCE_STATUSES:
            raise ValueError(f"invalid observation authority for {source['source_id']}")
        if source["static_gap_fit_authority_status"] not in STATIC_STATUSES:
            raise ValueError(f"invalid static authority for {source['source_id']}")

    class_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for row in observations:
        if row["source_id"] not in source_by_id:
            raise ValueError(f"unknown source_id in {row['observation_id']}")
        if row["specimen_id"] not in specimen_by_id:
            raise ValueError(f"unknown specimen_id in {row['observation_id']}")
        source = source_by_id[row["source_id"]]
        specimen = specimen_by_id[row["specimen_id"]]
        if row["source_lineage_id"] != source["source_lineage_id"]:
            raise ValueError(f"source lineage mismatch in {row['observation_id']}")
        if row["source_lineage_id"] != specimen["source_lineage_id"]:
            raise ValueError(f"specimen lineage mismatch in {row['observation_id']}")
        if row["input_asset_sha256"] != source["input_asset_sha256"]:
            raise ValueError(f"asset hash mismatch in {row['observation_id']}")
        if row["measurement_class"] not in MEASUREMENT_CLASSES:
            raise ValueError(f"invalid measurement class in {row['observation_id']}")
        if row["value_status"] not in VALUE_STATUSES:
            raise ValueError(f"invalid value status in {row['observation_id']}")
        if row["relation"] not in RELATIONS:
            raise ValueError(f"invalid relation in {row['observation_id']}")
        if row["value_status"] == "sign_constraint":
            if row["relation"] not in {"lt", "gt"} or row["reported_value_eV"] != 0.0:
                raise ValueError(f"invalid sign constraint in {row['observation_id']}")
        elif row["relation"] not in {"eq", "approx"}:
            raise ValueError(f"point observation has inequality relation in {row['observation_id']}")

        class_counts[row["measurement_class"]] = class_counts.get(row["measurement_class"], 0) + 1
        status_counts[row["value_status"]] = status_counts.get(row["value_status"], 0) + 1

    schmit_groups = [row for row in specimens if row["specimen_id"].startswith("schmit_detector_")]
    schmit_count = 0
    for group in schmit_groups:
        if group["source_lineage_id"] != contract["source_lineage_id"]:
            raise ValueError(f"Schmit lineage mismatch in {group['specimen_id']}")
        if group["composition_nominal"] == group["composition_adjusted"]:
            raise ValueError(f"fit-adjusted composition was not preserved in {group['specimen_id']}")
        for temperature, wavelength_um, energy_eV in group["points"]:
            schmit_count += 1
            if abs(1.24 / wavelength_um - energy_eV) > 6e-4:
                raise ValueError(
                    f"cutoff-energy conversion mismatch in {group['specimen_id']} at {temperature} K"
                )
    if len(schmit_groups) != 8 or schmit_count != 56:
        raise ValueError("Schmit-Stelzer Table III inventory is incomplete")

    mccombe = [row for row in observations if row["observation_id"] == "mccombe1970_sample4_gap"]
    if len(mccombe) != 1:
        raise ValueError("McCombe sample-4 gap record missing")
    mccombe_row = mccombe[0]
    mccombe_specimen = specimen_by_id[mccombe_row["specimen_id"]]
    if mccombe_row["source_lineage_id"] != "wiley_mccombe_sample4":
        raise ValueError("McCombe/Wiley shared lineage was not preserved")
    if not math.isclose(mccombe_specimen["carrier_density_cm3"], 9e14, rel_tol=0.0, abs_tol=1.0):
        raise ValueError("McCombe carrier density metadata changed")

    sign_rows = [row for row in observations if row["value_status"] == "sign_constraint"]
    if {(row["temperature_K"], row["relation"]) for row in sign_rows} != {(4, "lt"), (77, "gt")}:
        raise ValueError("Groves same-specimen sign constraints are incomplete")

    static_authorized = [
        row for row in sources
        if row["static_gap_fit_authority_status"] not in {"blocked", "conditional_endpoint"}
    ]
    expanded_observation_count = schmit_count + len(observations)
    expanded_class_counts = dict(class_counts)
    expanded_class_counts[contract["measurement_class"]] = schmit_count
    expanded_status_counts = dict(status_counts)
    expanded_status_counts[contract["value_status"]] = schmit_count

    return {
        "schema_version": package["schema_version"],
        "analysis": package["analysis"],
        "source_count": len(sources),
        "specimen_group_count": len(specimens),
        "explicit_observation_count": len(observations),
        "expanded_observation_count": expanded_observation_count,
        "measurement_class_counts": dict(sorted(expanded_class_counts.items())),
        "value_status_counts": dict(sorted(expanded_status_counts.items())),
        "schmit_table_iii_count": schmit_count,
        "sign_constraint_count": len(sign_rows),
        "shared_wiley_mccombe_lineage_preserved": True,
        "copyrighted_source_files_committed": False,
        "universal_static_fit_authorized": len(static_authorized) > 0,
        "decision": {
            "historical_observation_integration_authorized": True,
            "new_universal_gap_refit_authorized": False,
            "pool_measurement_classes_by_default": False,
            "digitized_curve_use_in_this_tranche": False,
            "reason": (
                "The recovered primary sources support exact detector-cutoff, resonance, "
                "magnetoreflectance, and sign-constraint records. Their observation operators, "
                "source lineages, composition limits, and model conditioning remain distinct."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.package_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
