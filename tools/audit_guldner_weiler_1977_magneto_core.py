#!/usr/bin/env python3
"""Fail-closed audit for the Guldner-Weiler 1977 magneto-optical core."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

EXPECTED_DOIS = {
    "guldner_1977_part_i": "10.1002/pssb.2220810225",
    "guldner_1977_part_ii": "10.1002/pssb.2220820115",
    "weiler_1977": "10.1103/PhysRevB.16.3603",
}

EXPECTED_ANCHORS = [
    (0.025, -261.0),
    (0.050, -207.0),
    (0.115, -90.0),
    (0.150, -30.0),
    (0.185, 35.0),
    (0.250, 161.0),
    (0.280, 208.0),
]

EXPECTED_DECISION = {
    "primary_magneto_optical_source_recovery": True,
    "exact_guldner_primary_anchors_authorized": True,
    "full_guldner_figure_11_series_authorized": False,
    "weiler_per_specimen_figure_points_authorized": False,
    "independent_laboratory_qualitative_comparison_authorized": True,
    "few_meV_quantitative_cross_lab_ranking_authorized": False,
    "composition_uncertainty_dominates_gap_fit_precision": True,
    "default_cross_modality_pooling_authorized": False,
    "universal_material_law_fit_authorized": False,
    "copyrighted_source_content_committed": False,
}


def _require_close(actual: Any, expected: float, field: str, tolerance: float = 1.0e-12) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=tolerance
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def weiler_dEg_dx_eV_per_x(temperature_K: float) -> float:
    temperature = float(temperature_K)
    if not math.isfinite(temperature):
        raise ValueError("temperature_K must be finite")
    if temperature not in (24.0, 91.0):
        raise ValueError("Weiler uncertainty audit is restricted to 24 K and 91 K")
    return 1.88 - 0.001 * temperature


def composition_energy_scale_meV(temperature_K: float, sigma_x: float) -> float:
    sigma = float(sigma_x)
    if not math.isfinite(sigma) or sigma <= 0.0:
        raise ValueError("sigma_x must be finite and positive")
    if sigma not in (0.005, 0.006, 0.015):
        raise ValueError("sigma_x is outside the source-declared audit set")
    return 1000.0 * weiler_dEg_dx_eV_per_x(temperature_K) * sigma


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Guldner-Weiler evidence schema")

    sources = payload.get("sources")
    if not isinstance(sources, list) or len(sources) != 3:
        raise ValueError("primary source inventory changed")
    observed_dois = {source["source_id"]: source["doi"] for source in sources}
    if observed_dois != EXPECTED_DOIS:
        raise ValueError("primary DOI inventory changed")
    if any(source.get("primary_full_text_recovered") is not True for source in sources):
        raise ValueError("all three primary full texts must remain recovered")
    if any(source.get("copyrighted_source_committed") is not False for source in sources):
        raise ValueError("copyrighted source content may not be committed")

    guldner = payload["guldner"]
    _require_close(guldner["temperature_K"], 4.2, "Guldner temperature")
    if guldner.get("measurement_class") != "magneto_interband_fit":
        raise ValueError("Guldner observation class changed")
    if guldner.get("composition_method") != ["density", "electron_microprobe"]:
        raise ValueError("Guldner composition provenance changed")
    if guldner.get("specimen_level_composition_uncertainty_reported") is not False:
        raise ValueError("unreported Guldner specimen sigma_x may not be invented")
    if guldner["model"].get("interaction_gap_is_model_conditioned") is not True:
        raise ValueError("Guldner interaction gaps must remain model conditioned")
    if guldner["full_figure_11_series"].get("numeric_ingestion_authorized") is not False:
        raise ValueError("Guldner Figure 11 points require a separate digitization gate")
    crossing = guldner["zero_gap_crossing"]
    _require_close(crossing["composition_x"], 0.165, "zero-gap composition")
    _require_close(crossing["composition_sigma"], 0.005, "zero-gap composition sigma")

    anchors = guldner.get("exact_primary_anchors")
    if not isinstance(anchors, list) or len(anchors) != len(EXPECTED_ANCHORS):
        raise ValueError("Guldner exact-anchor inventory changed")
    observed_anchors = [
        (float(row["composition_x"]), float(row["interaction_gap_meV"]))
        for row in anchors
    ]
    if observed_anchors != EXPECTED_ANCHORS:
        raise ValueError("Guldner exact anchors changed")
    if any(not str(row.get("value_status", "")).startswith("exact_") for row in anchors):
        raise ValueError("all authorized Guldner anchors must be exact text or caption values")

    weiler = payload["weiler"]
    if weiler.get("measurement_class") != "magnetoreflectance_fit":
        raise ValueError("Weiler observation class changed")
    if weiler.get("sample_count") != 10:
        raise ValueError("Weiler sample count changed")
    if weiler.get("temperatures_K") != [24.0, 91.0]:
        raise ValueError("Weiler temperature inventory changed")
    _require_close(weiler["gap_fit_uncertainty_meV_approx"], 3.0, "Weiler gap uncertainty")
    if weiler["per_specimen_gap_series"].get("numeric_ingestion_authorized") is not False:
        raise ValueError("Weiler per-specimen figure points require digitization audit")
    example = weiler["exact_example"]
    _require_close(example["composition_x"], 0.213, "Weiler example composition")
    _require_close(example["composition_sigma"], 0.006, "Weiler example sigma_x")
    cut_on = weiler["composition_provenance"]["room_temperature_transmission_cut_on"]
    if cut_on.get("independent_material_gap_validation") is not False:
        raise ValueError("transmission-derived composition cannot become independent gap validation")
    if weiler["interband_intraband_discrepancy"].get("model_observable_class_discrepancy") is not True:
        raise ValueError("Weiler interband/intraband discrepancy classification changed")

    if payload.get("decision") != EXPECTED_DECISION:
        raise ValueError("Guldner-Weiler decision changed")

    uncertainty_rows: list[dict[str, float]] = []
    fit_sigma = float(weiler["gap_fit_uncertainty_meV_approx"])
    for temperature in (24.0, 91.0):
        slope = weiler_dEg_dx_eV_per_x(temperature)
        for sigma_x in (0.005, 0.006, 0.015):
            energy_scale = composition_energy_scale_meV(temperature, sigma_x)
            uncertainty_rows.append(
                {
                    "temperature_K": temperature,
                    "dEg_dx_eV_per_x": slope,
                    "sigma_x": sigma_x,
                    "composition_energy_scale_meV": energy_scale,
                    "ratio_to_gap_fit_sigma": energy_scale / fit_sigma,
                }
            )

    minimum_composition_scale = min(
        row["composition_energy_scale_meV"] for row in uncertainty_rows
    )
    if minimum_composition_scale <= fit_sigma:
        raise ValueError("composition uncertainty no longer dominates fit precision")

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "primary_source_count": len(sources),
        "independent_laboratory_lineage_count": len(
            {source["source_lineage_id"] for source in sources}
        ),
        "guldner_exact_anchor_count": len(anchors),
        "guldner_zero_gap_crossing": crossing,
        "weiler_exact_example": example,
        "weiler_gap_fit_uncertainty_meV_approx": fit_sigma,
        "weiler_uncertainty_rows": uncertainty_rows,
        "minimum_composition_energy_scale_meV": minimum_composition_scale,
        "maximum_composition_energy_scale_meV": max(
            row["composition_energy_scale_meV"] for row in uncertainty_rows
        ),
        "minimum_ratio_to_gap_fit_sigma": min(
            row["ratio_to_gap_fit_sigma"] for row in uncertainty_rows
        ),
        "maximum_ratio_to_gap_fit_sigma": max(
            row["ratio_to_gap_fit_sigma"] for row in uncertainty_rows
        ),
        "interband_intraband_discrepancy_meV_approx": weiler[
            "interband_intraband_discrepancy"
        ]["maximum_energy_meV_approx"],
        "decision": payload["decision"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        Path(args.output_json).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
