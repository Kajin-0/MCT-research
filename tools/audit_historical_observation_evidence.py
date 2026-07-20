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
    "urbach_static_disorder_component",
    "urbach_dynamic_electron_phonon_component",
}
VALUE_STATUSES = {
    "exact_table",
    "exact_reported_value",
    "sign_constraint",
    "note_added_in_proof",
}
RELATIONS = {"eq", "lt", "gt", "approx"}

CHANG_SOURCE_ID = "chang_badano_et_al_2004"
CHANG_LINEAGE_ID = "uic_mbe_near_edge_2004"
CHANG_ASSET_SHA256 = (
    "de5dba52fa075fe197dbd182c00ef22ee620f0ad571e82e78f6b2a2698181424"
)
CHANG_EXPECTED = {
    "chang2004_x040_urbach_A": (
        "chang2004_x040", 0.40, "urbach_static_disorder_component",
        "urbach_width_static_component", 0.0190, 0.0002,
    ),
    "chang2004_x040_urbach_B": (
        "chang2004_x040", 0.40, "urbach_dynamic_electron_phonon_component",
        "urbach_width_dynamic_component", 0.0012, 0.0001,
    ),
    "chang2004_x030_urbach_A": (
        "chang2004_x030", 0.30, "urbach_static_disorder_component",
        "urbach_width_static_component", 0.0112, 0.0003,
    ),
    "chang2004_x030_urbach_B": (
        "chang2004_x030", 0.30, "urbach_dynamic_electron_phonon_component",
        "urbach_width_dynamic_component", 0.0008, 0.0001,
    ),
    "chang2004_x021_urbach_A": (
        "chang2004_x021", 0.21, "urbach_static_disorder_component",
        "urbach_width_static_component", 0.0124, 0.0005,
    ),
    "chang2004_x021_urbach_B": (
        "chang2004_x021", 0.21, "urbach_dynamic_electron_phonon_component",
        "urbach_width_dynamic_component", 0.00067, 0.00027,
    ),
}


def load_package(path: str | Path) -> dict[str, object]:
    package_path = Path(path)
    data = json.loads(package_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported historical observation schema")
    includes = data.get("includes")
    if includes is None:
        data.setdefault("same_point_pairings", [])
        return data

    required = {"sources", "specimens", "records", "schmit_contract"}
    optional = {"chang2004"}
    inventory = set(includes)
    if not required.issubset(inventory) or not inventory.issubset(required | optional):
        raise ValueError("historical observation include inventory is incomplete or unsupported")

    parent = package_path.parent
    result: dict[str, object] = {
        "schema_version": data["schema_version"],
        "analysis": data["analysis"],
        "sources": json.loads((parent / includes["sources"]).read_text(encoding="utf-8")),
        "specimen_groups": json.loads(
            (parent / includes["specimens"]).read_text(encoding="utf-8")
        ),
        "observations": json.loads(
            (parent / includes["records"]).read_text(encoding="utf-8")
        ),
        "schmit_observation_contract": json.loads(
            (parent / includes["schmit_contract"]).read_text(encoding="utf-8")
        ),
        "same_point_pairings": [],
    }
    if "chang2004" in includes:
        extension = json.loads(
            (parent / includes["chang2004"]).read_text(encoding="utf-8")
        )
        if extension.get("schema_version") != "1.0":
            raise ValueError("unsupported Chang 2004 extension schema")
        result["sources"].append(extension["source"])
        result["specimen_groups"].extend(extension["specimens"])
        result["observations"].extend(extension["observations"])
        result["same_point_pairings"].append(extension["same_point_pairing"])
    return result


def _require_close(actual: object, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1e-12
    ):
        raise ValueError(f"Chang 2004 {field} changed: {actual!r} != {expected!r}")


def audit(package_path: str | Path) -> dict[str, object]:
    package = load_package(package_path)
    sources = package["sources"]
    specimens = package["specimen_groups"]
    observations = package["observations"]
    contract = package["schmit_observation_contract"]
    pairings = package.get("same_point_pairings", [])

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
            raise ValueError(
                f"{source['source_id']} attempts to commit copyrighted source content"
            )
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
            raise ValueError(
                f"point observation has inequality relation in {row['observation_id']}"
            )

        class_counts[row["measurement_class"]] = (
            class_counts.get(row["measurement_class"], 0) + 1
        )
        status_counts[row["value_status"]] = status_counts.get(row["value_status"], 0) + 1

    schmit_groups = [
        row for row in specimens if row["specimen_id"].startswith("schmit_detector_")
    ]
    schmit_count = 0
    for group in schmit_groups:
        if group["source_lineage_id"] != contract["source_lineage_id"]:
            raise ValueError(f"Schmit lineage mismatch in {group['specimen_id']}")
        if group["composition_nominal"] == group["composition_adjusted"]:
            raise ValueError(
                f"fit-adjusted composition was not preserved in {group['specimen_id']}"
            )
        for temperature, wavelength_um, energy_eV in group["points"]:
            schmit_count += 1
            if abs(1.24 / wavelength_um - energy_eV) > 6e-4:
                raise ValueError(
                    f"cutoff-energy conversion mismatch in {group['specimen_id']} "
                    f"at {temperature} K"
                )
    if len(schmit_groups) != 8 or schmit_count != 56:
        raise ValueError("Schmit-Stelzer Table III inventory is incomplete")

    mccombe = [
        row for row in observations if row["observation_id"] == "mccombe1970_sample4_gap"
    ]
    if len(mccombe) != 1:
        raise ValueError("McCombe sample-4 gap record missing")
    mccombe_row = mccombe[0]
    mccombe_specimen = specimen_by_id[mccombe_row["specimen_id"]]
    if mccombe_row["source_lineage_id"] != "wiley_mccombe_sample4":
        raise ValueError("McCombe/Wiley shared lineage was not preserved")
    if not math.isclose(
        mccombe_specimen["carrier_density_cm3"], 9e14, rel_tol=0.0, abs_tol=1.0
    ):
        raise ValueError("McCombe carrier density metadata changed")

    sign_rows = [row for row in observations if row["value_status"] == "sign_constraint"]
    if {(row["temperature_K"], row["relation"]) for row in sign_rows} != {
        (4, "lt"),
        (77, "gt"),
    }:
        raise ValueError("Groves same-specimen sign constraints are incomplete")

    chang_source = source_by_id.get(CHANG_SOURCE_ID)
    if chang_source is None:
        raise ValueError("Chang 2004 source record missing")
    if chang_source["source_lineage_id"] != CHANG_LINEAGE_ID:
        raise ValueError("Chang 2004 source lineage changed")
    if chang_source["input_asset_sha256"] != CHANG_ASSET_SHA256:
        raise ValueError("Chang 2004 source asset hash changed")

    chang_specimen_ids = {
        row["specimen_id"]
        for row in specimens
        if row["source_lineage_id"] == CHANG_LINEAGE_ID
    }
    if chang_specimen_ids != {"chang2004_x040", "chang2004_x030", "chang2004_x021"}:
        raise ValueError("Chang 2004 specimen inventory is incomplete")

    chang_rows = [row for row in observations if row["source_id"] == CHANG_SOURCE_ID]
    if {row["observation_id"] for row in chang_rows} != set(CHANG_EXPECTED):
        raise ValueError("Chang 2004 Table I observation inventory changed")
    for row in chang_rows:
        specimen_id, composition, measurement_class, quantity, value, sigma = (
            CHANG_EXPECTED[row["observation_id"]]
        )
        if row["specimen_id"] != specimen_id:
            raise ValueError(f"Chang specimen changed in {row['observation_id']}")
        _require_close(
            row["composition_reported"], composition,
            f"{row['observation_id']} composition",
        )
        if row["composition_sigma"] is not None:
            raise ValueError(
                f"Chang composition uncertainty was invented in {row['observation_id']}"
            )
        if row["measurement_class"] != measurement_class or row["quantity"] != quantity:
            raise ValueError(f"Chang observation class changed in {row['observation_id']}")
        _require_close(row["reported_value_eV"], value, f"{row['observation_id']} value")
        _require_close(row["reported_sigma_eV"], sigma, f"{row['observation_id']} sigma")
        if (
            row["value_status"] != "exact_table"
            or row["relation"] != "eq"
            or row["temperature_K"] is not None
        ):
            raise ValueError(f"Chang Table I semantics changed in {row['observation_id']}")

    if len(pairings) != 1:
        raise ValueError("Chang 2004 same-point pairing metadata missing")
    pairing = pairings[0]
    required_pairing = {
        "source_id": CHANG_SOURCE_ID,
        "source_lineage_id": CHANG_LINEAGE_ID,
        "same_point_pairing_documented": True,
        "simultaneous_measurement_documented": True,
        "paired_modalities": [
            "absorption_coefficient",
            "photoconductive_quantum_efficiency",
        ],
        "paired_temperatures_K": [77, 293],
        "specimen_composition_identified": False,
        "numerical_paired_gap_table_reported": False,
        "photoconductive_edge_operator_complete": False,
        "paired_numeric_method_offset_identified": False,
    }
    for field, expected in required_pairing.items():
        if pairing.get(field) != expected:
            raise ValueError(f"Chang pairing field {field} changed")

    static_authorized = [
        row
        for row in sources
        if row["static_gap_fit_authority_status"]
        not in {"blocked", "conditional_endpoint"}
    ]
    expanded_observation_count = schmit_count + len(observations)
    expanded_class_counts = dict(class_counts)
    expanded_class_counts[contract["measurement_class"]] = schmit_count
    expanded_status_counts = dict(status_counts)
    expanded_status_counts[contract["value_status"]] = (
        expanded_status_counts.get(contract["value_status"], 0) + schmit_count
    )

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
        "chang2004_urbach_record_count": len(chang_rows),
        "same_point_pairing_count": len(pairings),
        "chang2004_same_point_pairing_documented": True,
        "chang2004_numeric_method_offset_identified": False,
        "shared_wiley_mccombe_lineage_preserved": True,
        "copyrighted_source_files_committed": False,
        "universal_static_fit_authorized": len(static_authorized) > 0,
        "decision": {
            "historical_observation_integration_authorized": True,
            "new_universal_gap_refit_authorized": False,
            "pool_measurement_classes_by_default": False,
            "digitized_curve_use_in_this_tranche": False,
            "chang2004_urbach_components_authorized": True,
            "chang2004_numeric_pair_offset_authorized": False,
            "reason": (
                "The exact Chang 2004 Table I Urbach components can be preserved as "
                "observation-model parameters, and the source documents simultaneous "
                "same-point absorption and photoconductive measurement. The publication "
                "does not identify the Figure 1 specimen composition, report a paired "
                "numeric gap table, or specify a complete photoconductive edge operator, "
                "so no numerical method offset or universal correction is identified."
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
