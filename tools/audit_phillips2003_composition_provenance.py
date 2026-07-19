#!/usr/bin/env python3
"""Audit the composition provenance in Phillips et al. 2003."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_fields(path: str | Path) -> dict[str, dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("provenance table is empty")
    if len({row["field"] for row in rows}) != len(rows):
        raise ValueError("provenance fields must be unique")
    return {row["field"]: row for row in rows}


def number(fields: dict[str, dict[str, str]], name: str) -> float:
    if name not in fields:
        raise ValueError(f"missing field {name}")
    return float(fields[name]["value"])


def text(fields: dict[str, dict[str, str]], name: str) -> str:
    if name not in fields:
        raise ValueError(f"missing field {name}")
    return fields[name]["value"]


def audit(provenance_path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    fields = load_fields(provenance_path)
    with Path(manifest_path).open(newline="", encoding="utf-8") as stream:
        figures = list(csv.DictReader(stream))
    if len(figures) != 4:
        raise ValueError("expected four figure records")

    mean_alpha = number(fields, "mean_absorption_coefficient")
    sigma_alpha = number(fields, "absorption_standard_deviation")
    reported_percent = number(fields, "reported_absorption_relative_variation")
    calculated_percent = 100.0 * sigma_alpha / mean_alpha
    x_sigma = number(fields, "extracted_composition_standard_deviation")
    x_resolution = number(fields, "equivalent_composition_resolution")
    resolution_ratio = x_sigma / x_resolution
    x_mean = number(fields, "extracted_composition_mean")
    nominal_x = number(fields, "nominal_composition_x")

    exact_full_text = text(fields, "full_text_recovered").lower() == "true"
    independent = text(fields, "independent_composition_metrology").lower() == "true"
    static_authority = text(fields, "static_gap_fit_authority")
    observation_authority = text(fields, "observation_uniformity_authority")
    all_digitization_blocked = all(
        row["digitization_status"].startswith("blocked") for row in figures
    )
    any_page_archived = any(
        row["source_page_image_archived_in_repo"].lower() == "true"
        for row in figures
    )
    any_calibration_archived = any(
        row["axis_calibration_archived"].lower() == "true" for row in figures
    )

    checks = {
        "primary_full_text_recovered": exact_full_text,
        "reported_relative_variation_reproduced": abs(calculated_percent - reported_percent)
        <= 0.05,
        "composition_is_absorption_derived": fields[
            "extracted_composition_mean"
        ]["provenance"]
        == "derived_from_absorption_threshold",
        "composition_metrology_is_not_independent": independent is False,
        "static_fit_authority_is_blocked": static_authority == "blocked",
        "observation_uniformity_is_conditional": observation_authority == "conditional",
        "derived_spread_is_below_one_resolution_increment": resolution_ratio < 1.0,
        "figure_digitization_remains_blocked": all_digitization_blocked
        and not any_page_archived
        and not any_calibration_archived,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"Phillips 2003 provenance audit failed: {failed}")

    return {
        "schema_version": "1.0",
        "analysis": "Phillips 2003 spectromicroscopy composition provenance audit",
        "source": {
            "doi": text(fields, "doi"),
            "stable_repository_handle": text(fields, "stable_repository_handle"),
            "full_text_recovered": exact_full_text,
        },
        "sample_and_measurement": {
            "growth_method": text(fields, "growth_method"),
            "substrate": text(fields, "substrate"),
            "in_situ_growth_control": text(fields, "in_situ_growth_control"),
            "nominal_composition_x": nominal_x,
            "layer_thickness_um": number(fields, "layer_thickness"),
            "beam_diameter_um": number(fields, "beam_diameter"),
            "spatial_step_um": number(fields, "spatial_step"),
            "area_scan_point_count": int(number(fields, "area_scan_point_count")),
        },
        "absorption_uniformity": {
            "wavenumber_cm1": number(fields, "absorption_map_wavenumber"),
            "mean_alpha_cm1": mean_alpha,
            "sigma_alpha_cm1": sigma_alpha,
            "calculated_relative_sigma_percent": calculated_percent,
            "reported_relative_sigma_percent": reported_percent,
        },
        "derived_composition": {
            "threshold_cm1": number(fields, "composition_extraction_threshold"),
            "reference_relations": text(fields, "composition_reference_relations"),
            "mean_x": x_mean,
            "sigma_x": x_sigma,
            "nominal_minus_derived_mean_x": nominal_x - x_mean,
            "spectrometer_resolution_cm1": number(fields, "spectrometer_resolution"),
            "equivalent_x_resolution": x_resolution,
            "sigma_to_resolution_ratio": resolution_ratio,
            "independent_composition_metrology": independent,
        },
        "confounders": text(fields, "confounders").split("; "),
        "figure_recovery": {
            "figure_record_count": len(figures),
            "source_page_image_archived_in_repo": any_page_archived,
            "axis_calibration_archived": any_calibration_archived,
            "digitization_authorized": False,
        },
        "validation_checks": checks,
        "decision": {
            "observation_uniformity_research_authorized": True,
            "derived_x_is_independent_static_gap_evidence": False,
            "reported_sigma_x_is_independent_composition_uncertainty": False,
            "static_gap_refit_authorized": False,
            "figure_digitization_authorized": False,
            "reason": (
                "The reported composition is derived from an absorption threshold and "
                "empirical gap-composition relations. Its spread is below one stated "
                "spectrometer-equivalent composition increment and is confounded by "
                "thickness, reflections, absorption variation, and drift."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance-csv", required=True)
    parser.add_argument("--manifest-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.provenance_csv, args.manifest_csv)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
