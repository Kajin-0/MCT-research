"""Deterministic eligibility audit for specimen-level R01 temperature benchmarks.

The audit inventories repository-native source ledgers and groups them only by
exact operational measurement class.  It does not evaluate a gap equation,
fit coefficients, infer an observation operator, or convert deterministic
source/digitization bounds into Gaussian covariance.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ISSUE = 320
DECISION = "class_specific_single_source_benchmarks_only"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _file_record(root: Path, relative_path: str) -> dict[str, str]:
    path = root / relative_path
    if not path.is_file():
        raise FileNotFoundError(relative_path)
    return {"path": relative_path, "sha256": sha256_file(path)}


def _unique(rows: list[dict[str, str]], field: str) -> set[str]:
    values = {row[field] for row in rows}
    if "" in values:
        raise ValueError(f"empty {field} value")
    return values


def _audit_seiler(root: Path) -> dict[str, Any]:
    figure_path = "data/experimental/seiler1990_figure7_digitized.csv"
    specimen_path = "data/experimental/seiler1990_specimens.csv"
    rows = _read_csv(root / figure_path)
    specimens = _read_csv(root / specimen_path)
    measurement_classes = _unique(rows, "measurement_class")
    sample_numbers = _unique(rows, "sample_number")
    if len(rows) != 34 or sample_numbers != {"1", "2", "3"}:
        raise ValueError("unexpected Seiler Figure 7 ledger structure")
    if measurement_classes != {
        "two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap"
    }:
        raise ValueError("unexpected Seiler measurement class")
    independently_composed_temperature_series = sum(
        int(row["figure7_marker_count"]) > 0
        and row["composition_independent_for_composition_law"] == "true"
        for row in specimens
    )
    source_hashes = _unique(rows, "source_pdf_sha256")
    if len(source_hashes) != 1:
        raise ValueError("Seiler Figure 7 must bind to one source PDF")
    return {
        "source_id": "seiler1990",
        "canonical_files": [
            _file_record(root, figure_path),
            _file_record(root, specimen_path),
        ],
        "source_asset_sha256": next(iter(source_hashes)),
        "source_native_or_auditable_status": "auditable_direct_marker_digitization",
        "row_count": len(rows),
        "specimen_count": len(sample_numbers),
        "temperature_series_specimen_count": len(sample_numbers),
        "independently_composed_temperature_series_count": (
            independently_composed_temperature_series
        ),
        "measurement_class": next(iter(measurement_classes)),
        "signed_gap_eligible": None,
        "intrinsic_gap_eligible_without_observation_operator": True,
        "composition_provenance": (
            "sample_3_independent_wet_chemistry_tied_value; samples_1_2_"
            "cutoff_or_HSC_conditioned"
        ),
        "energy_uncertainty_semantics": (
            "Figure_7_digitization_half_widths_are_coordinate_bounds; "
            "pointwise_experimental_covariance_not_reported"
        ),
        "temperature_uncertainty_semantics": (
            "source_approximately_plus_minus_0p2_K_article_level; "
            "digitization_bounds_separate"
        ),
        "source_lineage_dependencies": [
            "published_Seiler_relation_derived_from_same_source",
            "provisional_Hansen_Pade_primarily_trained_on_Seiler_Figure_7",
        ],
        "eligible_for_intercept_profiled_shape": True,
        "eligible_for_absolute_gap_ranking": True,
        "absolute_gap_eligible_specimen_count": 1,
        "e1_failures": [],
    }


def _audit_chu(root: Path) -> dict[str, Any]:
    relative_path = "data/evidence/hgcdte_chu_1991_turning_point_series.json"
    payload = json.loads((root / relative_path).read_text(encoding="utf-8"))
    rows = payload["temperature_series"]["rows"]
    if len(rows) != 7:
        raise ValueError("unexpected Chu temperature-series row count")
    temperatures = [float(row["temperature_K"]) for row in rows]
    if len(set(temperatures)) != len(temperatures):
        raise ValueError("Chu temperatures must be unique within the specimen")
    measurement_class = payload["measurement_class"]
    if measurement_class != "absorption_turning_point_edge":
        raise ValueError("unexpected Chu measurement class")
    return {
        "source_id": "chu_mi_tang_1991",
        "canonical_files": [_file_record(root, relative_path)],
        "source_asset_sha256": payload["source"]["input_asset_sha256"],
        "source_native_or_auditable_status": "source_printed_figure_labels",
        "row_count": len(rows),
        "specimen_count": 1,
        "temperature_series_specimen_count": 1,
        "independently_composed_temperature_series_count": 1,
        "measurement_class": measurement_class,
        "signed_gap_eligible": None,
        "intrinsic_gap_eligible_without_observation_operator": False,
        "composition_provenance": payload["composition_method"],
        "energy_uncertainty_semantics": (
            "printed_label_rounding_half_width_0p5_meV_not_experimental_sigma"
        ),
        "temperature_uncertainty_semantics": "printed_temperature_labels",
        "source_lineage_dependencies": [
            "Chu_1983_equation_same_source_family",
        ],
        "eligible_for_intercept_profiled_shape": True,
        "eligible_for_absolute_gap_ranking": False,
        "absolute_gap_eligible_specimen_count": 0,
        "e1_failures": [],
    }


def _audit_scott(root: Path) -> dict[str, Any]:
    data_path = "data/experimental/scott1969_figure2_digitized.csv"
    readme_path = "data/experimental/scott1969_figure2_extraction_README.md"
    rows = _read_csv(root / data_path)
    groups = _unique(rows, "shared_specimen_group")
    classes = _unique(rows, "measurement_class")
    if len(rows) != 70 or len(groups) != 9:
        raise ValueError("unexpected Scott Figure 2 ledger structure")
    if classes != {"fixed_absorption_optical_edge_alpha_500_cm_inverse"}:
        raise ValueError("unexpected Scott measurement class")
    if _unique(rows, "signed_gap_eligible") != {"false"}:
        raise ValueError("Scott rows must remain non-signed")
    if _unique(rows, "intrinsic_gap_eligible_without_observation_operator") != {
        "false"
    }:
        raise ValueError("Scott rows must remain observation-operator dependent")
    readme = (root / readme_path).read_text(encoding="utf-8")
    match = re.search(r"source PDF SHA256\s+([0-9a-f]{64})", readme)
    if match is None:
        raise ValueError("Scott source PDF hash missing from extraction record")
    return {
        "source_id": "scott1969",
        "canonical_files": [
            _file_record(root, data_path),
            _file_record(root, readme_path),
        ],
        "source_asset_sha256": match.group(1),
        "source_native_or_auditable_status": "auditable_direct_marker_digitization",
        "row_count": len(rows),
        "specimen_count": len(groups),
        "temperature_series_specimen_count": len(groups),
        "independently_composed_temperature_series_count": len(groups),
        "measurement_class": next(iter(classes)),
        "signed_gap_eligible": False,
        "intrinsic_gap_eligible_without_observation_operator": False,
        "composition_provenance": (
            "density_measured_plus_minus_0p005_with_microprobe_spatial_audit"
        ),
        "energy_uncertainty_semantics": (
            "plus_minus_4p7_meV_digitization_bound; "
            "pointwise_experimental_covariance_not_reported"
        ),
        "temperature_uncertainty_semantics": (
            "plus_minus_1p75_K_digitization_bound_not_sigma"
        ),
        "source_lineage_dependencies": [
            "Scott_1969_equation_same_source",
            "Hansen_1982_fitted_source_HSC_R02",
        ],
        "eligible_for_intercept_profiled_shape": True,
        "eligible_for_absolute_gap_ranking": False,
        "absolute_gap_eligible_specimen_count": 0,
        "e1_failures": [],
    }


def _audit_schmit(root: Path) -> dict[str, Any]:
    observation_path = "data/experimental/schmit1969_table3_cutoff_observations.csv"
    specimen_path = "data/experimental/schmit1969_specimens.csv"
    rows = _read_csv(root / observation_path)
    specimens = _read_csv(root / specimen_path)
    specimen_ids = _unique(rows, "specimen_id")
    classes = _unique(rows, "measurement_class")
    if len(rows) != 56 or len(specimen_ids) != 8 or len(specimens) != 8:
        raise ValueError("unexpected Schmit Table III ledger structure")
    if classes != {"detector_half_peak_spectral_response_cutoff"}:
        raise ValueError("unexpected Schmit measurement class")
    if _unique(rows, "signed_gap_eligible") != {"false"}:
        raise ValueError("Schmit rows must remain non-signed")
    if _unique(rows, "intrinsic_gap_eligible_without_observation_operator") != {
        "false"
    }:
        raise ValueError("Schmit rows must remain observation-operator dependent")
    return {
        "source_id": "schmit_stelzer1969",
        "canonical_files": [
            _file_record(root, observation_path),
            _file_record(root, specimen_path),
        ],
        "source_asset_sha256": None,
        "source_native_or_auditable_status": "source_native_printed_table",
        "row_count": len(rows),
        "specimen_count": len(specimen_ids),
        "temperature_series_specimen_count": len(specimen_ids),
        "independently_composed_temperature_series_count": len(specimen_ids),
        "measurement_class": next(iter(classes)),
        "signed_gap_eligible": False,
        "intrinsic_gap_eligible_without_observation_operator": False,
        "composition_provenance": (
            "nominal_density_and_microprobe_values_are_measured; "
            "fit_adjusted_compositions_are_not_independent"
        ),
        "energy_uncertainty_semantics": (
            "source_level_better_than_1_percent_not_pointwise_sigma; "
            "pointwise_covariance_not_reported"
        ),
        "temperature_uncertainty_semantics": (
            "plus_minus_0p5_K_control_stability_separate_from_"
            "better_than_10_K_absolute_accuracy; neither_is_pointwise_sigma"
        ),
        "source_lineage_dependencies": [
            "Schmit_Stelzer_1969_equation_same_source",
            "Hansen_1982_fitted_source_HSC_R01",
        ],
        "eligible_for_intercept_profiled_shape": True,
        "eligible_for_absolute_gap_ranking": False,
        "absolute_gap_eligible_specimen_count": 0,
        "e1_failures": [],
    }


def build_reference(root: Path) -> dict[str, Any]:
    sources = [
        _audit_seiler(root),
        _audit_chu(root),
        _audit_scott(root),
        _audit_schmit(root),
    ]
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in sources:
        source["e1_eligible"] = not source["e1_failures"]
        by_class[source["measurement_class"]].append(source)

    class_records: list[dict[str, Any]] = []
    for measurement_class in sorted(by_class):
        members = by_class[measurement_class]
        eligible_members = [member for member in members if member["e1_eligible"]]
        source_holdout_authorized = len(eligible_members) >= 2
        absolute_sources = [
            member for member in eligible_members
            if member["eligible_for_absolute_gap_ranking"]
        ]
        absolute_ranking_authorized = (
            source_holdout_authorized and len(absolute_sources) >= 2
        )
        class_records.append(
            {
                "measurement_class": measurement_class,
                "source_ids": sorted(member["source_id"] for member in members),
                "source_count": len(members),
                "e1_eligible_source_count": len(eligible_members),
                "absolute_gap_eligible_source_count": len(absolute_sources),
                "source_held_out_ranking_authorized": source_holdout_authorized,
                "absolute_material_gap_ranking_authorized": (
                    absolute_ranking_authorized
                ),
                "blocking_reasons": [] if source_holdout_authorized else [
                    "fewer_than_two_independent_sources_in_exact_measurement_class"
                ],
            }
        )

    class_by_name = {
        record["measurement_class"]: record for record in class_records
    }
    for source in sources:
        class_record = class_by_name[source["measurement_class"]]
        source["eligible_for_source_holdout"] = class_record[
            "source_held_out_ranking_authorized"
        ]
        source["exclusion_reasons"] = (
            [] if source["eligible_for_source_holdout"] else [
                "no_second_independent_source_with_same_exact_measurement_class"
            ]
        )

    e2 = any(
        record["source_held_out_ranking_authorized"] for record in class_records
    )
    e3 = any(
        record["absolute_material_gap_ranking_authorized"]
        for record in class_records
    )
    e4 = e2 and e3
    decision = (
        "source_held_out_class_benchmark_authorized"
        if e2
        else DECISION
    )
    return {
        "schema_version": "1.0",
        "program": "R01",
        "parent_issue": 8,
        "issue": ISSUE,
        "decision": decision,
        "observation_boundary": {
            "exact_measurement_class_matching_required": True,
            "cross_class_pooling_authorized": False,
            "observation_operator_inference_authorized": False,
            "model_coefficients_fitted": 0,
            "source_offsets_fitted": 0,
            "composition_shifts_fitted": 0,
            "deterministic_bounds_recast_as_gaussian_sigma": False,
        },
        "gates": {
            "E1_all_in_scope_sources_eligible": all(
                source["e1_eligible"] for source in sources
            ),
            "E2_any_exact_class_source_holdout_authorized": e2,
            "E3_any_exact_class_absolute_ranking_authorized": e3,
            "E4_universal_model_advancement_authorized": e4,
        },
        "summary": {
            "source_count": len(sources),
            "row_count": sum(source["row_count"] for source in sources),
            "temperature_series_specimen_count": sum(
                source["temperature_series_specimen_count"] for source in sources
            ),
            "exact_measurement_class_count": len(class_records),
            "maximum_sources_in_one_exact_class": max(
                record["source_count"] for record in class_records
            ),
        },
        "sources": sorted(sources, key=lambda source: source["source_id"]),
        "measurement_classes": class_records,
        "context_only_exclusions": [
            {
                "source_id": "camassel1988",
                "reason": "low_temperature_composition_anchors_not_specimen_temperature_series",
            },
            {
                "source_id": "finkman_nemirovsky1979",
                "reason": "no_committed_specimen_temperature_point_ledger",
            },
            {
                "source_id": "laurenti1990_figure2",
                "reason": "direct_experimental_temperature_series_not_available_as_calibrated_ledger",
            },
            {
                "source_id": "blue1964",
                "reason": "room_temperature_context_and_non_signed_theory_conditioned_parameter",
            },
            {
                "source_id": "groves1967",
                "reason": "endpoint_and_sign_constraints_not_multi_temperature_specimen_series",
            },
        ],
        "claim_boundary": {
            "authorized": [
                "class_specific_single_source_shape_or_forward_evaluations",
                "source_bounded_eligibility_reporting",
            ],
            "not_authorized": [
                "source_held_out_model_ranking",
                "pooled_cross_class_ranking",
                "new_gap_law_coefficients",
                "universal_HgCdTe_equation",
                "manuscript_authorization",
            ],
        },
    }
