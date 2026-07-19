#!/usr/bin/env python3
"""Audit the fixed real-spectrum set for the HgCdTe observation-model manuscript."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED_COLUMNS = {
    "spectrum_id",
    "source_id",
    "doi",
    "figure_id",
    "pdf_page_zero_based",
    "evidence_class",
    "composition_x",
    "temperature_k",
    "measurement_modality",
    "same_specimen_cross_method",
    "carrier_type",
    "carrier_density_cm3",
    "composition_method_status",
    "thickness_status",
    "source_full_text_status",
    "figure_locator_status",
    "source_image_archived",
    "axis_calibration_archived",
    "machine_readable_points_recovered",
    "chu_1994_domain_eligible",
    "manuscript_role",
    "analysis_status",
    "notes",
}


def yes(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def load_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("selection CSV has no header")
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(f"selection CSV is missing columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("selection CSV is empty")
    identifiers = [row["spectrum_id"].strip() for row in rows]
    if any(not identifier for identifier in identifiers):
        raise ValueError("every row requires a spectrum_id")
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("spectrum_id values must be unique")
    return rows


def audit(path: str | Path) -> dict[str, object]:
    rows = load_rows(path)
    normalized: list[dict[str, object]] = []

    for row in rows:
        spectrum_id = row["spectrum_id"].strip()
        evidence_class = row["evidence_class"].strip().lower()
        if evidence_class != "primary":
            raise ValueError(f"{spectrum_id} is not primary evidence")

        composition = float(row["composition_x"])
        temperature = float(row["temperature_k"])
        if not 0.0 <= composition <= 1.0:
            raise ValueError(f"invalid composition for {spectrum_id}")
        if temperature <= 0.0:
            raise ValueError(f"invalid temperature for {spectrum_id}")
        if not row["doi"].strip() or not row["figure_id"].strip():
            raise ValueError(f"missing source locator for {spectrum_id}")
        if row["source_full_text_status"].strip() != "author_posted_full_text":
            raise ValueError(f"{spectrum_id} does not have recovered primary full text")
        if not row["figure_locator_status"].strip():
            raise ValueError(f"{spectrum_id} has no figure locator status")

        image_archived = yes(row["source_image_archived"])
        calibration_archived = yes(row["axis_calibration_archived"])
        points_recovered = yes(row["machine_readable_points_recovered"])
        if points_recovered and not (image_archived and calibration_archived):
            raise ValueError(
                f"{spectrum_id} reports points without source image and calibration"
            )

        normalized.append(
            {
                "spectrum_id": spectrum_id,
                "source_id": row["source_id"].strip(),
                "doi": row["doi"].strip(),
                "figure_id": row["figure_id"].strip(),
                "composition_x": composition,
                "temperature_k": temperature,
                "measurement_modality": row["measurement_modality"].strip(),
                "same_specimen_cross_method": yes(
                    row["same_specimen_cross_method"]
                ),
                "carrier_metadata_complete": (
                    row["carrier_type"].strip() != "not_reported"
                    and row["carrier_density_cm3"].strip() != "not_reported"
                ),
                "source_image_archived": image_archived,
                "axis_calibration_archived": calibration_archived,
                "machine_readable_points_recovered": points_recovered,
                "chu_1994_domain_eligible": yes(
                    row["chu_1994_domain_eligible"]
                ),
                "manuscript_role": row["manuscript_role"].strip(),
                "analysis_status": row["analysis_status"].strip(),
            }
        )

    temperatures = [float(row["temperature_k"]) for row in normalized]
    compositions = sorted({float(row["composition_x"]) for row in normalized})
    source_ids = sorted({str(row["source_id"]) for row in normalized})
    low_temperature = [row for row in normalized if float(row["temperature_k"]) <= 100.0]
    room_temperature = [row for row in normalized if float(row["temperature_k"]) >= 250.0]
    cross_method = [row for row in normalized if row["same_specimen_cross_method"]]
    chu_eligible = [row for row in normalized if row["chu_1994_domain_eligible"]]
    digitization_ready = [
        row
        for row in normalized
        if row["source_image_archived"] and row["axis_calibration_archived"]
    ]
    analysis_ready = [row for row in normalized if row["machine_readable_points_recovered"]]

    selection_gates = {
        "at_least_two_primary_spectra": len(normalized) >= 2,
        "low_temperature_coverage": bool(low_temperature),
        "near_room_temperature_coverage": bool(room_temperature),
        "at_least_two_compositions": len(compositions) >= 2,
        "same_specimen_cross_method_case": bool(cross_method),
        "chu_1994_domain_case": bool(chu_eligible),
        "at_least_two_independent_sources": len(source_ids) >= 2,
    }

    return {
        "schema_version": "1.0",
        "analysis": "HgCdTe manuscript absorption-spectrum selection audit",
        "spectrum_count": len(normalized),
        "source_count": len(source_ids),
        "source_ids": source_ids,
        "composition_values": compositions,
        "temperature_range_k": [min(temperatures), max(temperatures)],
        "low_temperature_spectrum_count": len(low_temperature),
        "near_room_temperature_spectrum_count": len(room_temperature),
        "cross_method_spectrum_count": len(cross_method),
        "chu_1994_domain_spectrum_count": len(chu_eligible),
        "digitization_ready_spectrum_count": len(digitization_ready),
        "machine_readable_spectrum_count": len(analysis_ready),
        "selection_gates": selection_gates,
        "selection_gate_passed": all(selection_gates.values()),
        "analysis_authorized_now": len(analysis_ready) >= 2,
        "next_blocker": (
            "Archive exact source page images and axis calibrations, then recover "
            "machine-readable points for at least two selected spectra."
        ),
        "spectra": normalized,
        "claim_boundary": (
            "This audit selects manuscript-critical primary spectra. It does not "
            "digitize copyrighted figures, infer missing metadata, select a corrected "
            "gap, or authorize a material-law refit."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.selection_csv)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
