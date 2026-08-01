#!/usr/bin/env python3
"""Generate the deterministic Guldner 1977 HSC_R15 primary-source audit."""
from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hansen"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def dec(value: str) -> Decimal:
    return Decimal(value)


def main() -> None:
    source = read_csv("guldner1977_hsc_r15_source_metadata.csv")[0]
    groups = read_csv("guldner1977_hsc_r15_specimen_groups.csv")
    gaps = read_csv("guldner1977_hsc_r15_interaction_gap_candidates.csv")
    parameters = read_csv("guldner1977_hsc_r15_band_parameter_constraints.csv")
    polarons = read_csv("guldner1977_hsc_r15_polaron_anomalies.csv")
    figures = read_csv("guldner1977_hsc_r15_figure_evidence.csv")
    links = read_csv("guldner1977_hsc_r15_part_i_links.csv")
    candidates = read_csv("guldner1977_hsc_r15_hansen_ingestion_candidates.csv")

    gap_values = [dec(row["interaction_gap_meV"]) for row in gaps]
    fig11 = next(row for row in figures if row["figure_id"] == "G77II_FIG11")
    report = {
        "schema_version": 1,
        "source_id": source["source_id"],
        "hansen_graph_id": source["hansen_graph_id"],
        "source_pdf_sha256": source["source_pdf_sha256"],
        "source_pdf_sha256_status": source["source_pdf_sha256_status"],
        "source_file_library_id": source["source_file_library_id"],
        "source_pdf_page_count": int(source["source_pdf_page_count"]),
        "measurement_class": source["primary_measurement_class"],
        "specimen_groups": {
            "count": len(groups),
            "composition_values": [row["composition_x"] for row in groups],
            "composition_method": source["composition_method"],
            "physical_specimen_count_resolved": all(
                row["physical_specimen_count_status"] != "unresolved" for row in groups
            ),
            "part_i_linkage_resolved": all(
                row["part_i_linkage_status"] == "established" for row in groups
            ),
        },
        "interaction_gap_candidates": {
            "count": len(gaps),
            "values_meV_by_x": {
                row["composition_x"]: row["interaction_gap_meV"] for row in gaps
            },
            "minimum_meV": format(min(gap_values), "f"),
            "maximum_meV": format(max(gap_values), "f"),
            "negative_count": sum(value < 0 for value in gap_values),
            "positive_count": sum(value > 0 for value in gap_values),
            "signed_transition_bracket_present": any(value < 0 for value in gap_values)
            and any(value > 0 for value in gap_values),
            "source_native_gap_determination_count": sum(
                row["source_native_gap_determination"] == "true" for row in gaps
            ),
            "raw_observable_count": sum(row["raw_observable"] == "true" for row in gaps),
            "reported_pointwise_uncertainty_count": sum(
                bool(row["printed_gap_uncertainty_meV"]) for row in gaps
            ),
        },
        "critical_composition": {
            "value": "0.165",
            "uncertainty": "0.005",
            "temperature_k": "4.2",
            "reported_relation": fig11["reported_relation"],
            "figure_coordinates_digitized": fig11["coordinates_digitized"] == "true",
        },
        "band_parameter_constraints": {
            "count": len(parameters),
            "global_count": sum(row["scope"] == "global" for row in parameters),
            "representative_fit_count": sum(
                row["scope"] == "representative_fit" for row in parameters
            ),
            "ids": [row["parameter_id"] for row in parameters],
        },
        "polaron_anomalies": {
            "count": len(polarons),
            "phonon_energies_meV": sorted(
                {row["phonon_energy_meV"] for row in polarons}, key=Decimal
            ),
            "intrinsic_gap_evidence_count": sum(
                row["intrinsic_gap_evidence"] == "true" for row in polarons
            ),
            "quantitatively_complete_count": sum(
                row["quantitative_model_complete"] == "true" for row in polarons
            ),
        },
        "figure_evidence": {
            "count": len(figures),
            "ids": [row["figure_id"] for row in figures],
            "digitized_count": sum(row["coordinates_digitized"] == "true" for row in figures),
        },
        "part_i_links": {
            "count": len(links),
            "target_graph_ids": sorted({row["target_graph_id"] for row in links}),
            "same_specimen_established_count": sum(
                row["same_specimen_established"] == "true" for row in links
            ),
            "double_counting_authorized_count": sum(
                row["double_counting_allowed"] == "true" for row in links
            ),
        },
        "hansen_candidates": {
            "count": len(candidates),
            "all_source_native": all(
                row["source_native_gap_determination"] == "true" for row in candidates
            ),
            "resolved_assignment_count": sum(
                row["hansen_assignment_resolved"] == "true" for row in candidates
            ),
            "independent_validation_count": sum(
                row["independent_validation"] == "true" for row in candidates
            ),
        },
        "deterministic_checks": {
            "source_binary_committed": source["source_binary_committed"] == "true",
            "source_hash_materialized": bool(source["source_pdf_sha256"]),
            "source_hash_matches_expected": source["source_pdf_sha256"]
            == "85bdf09852eb02747158a80f7854d202a69a48d98c9c571a396f8a4cd51c8704",
            "source_hash_status_is_materialized": source["source_pdf_sha256_status"]
            == "materialized_conversation_attachment",
            "figure_digitization_performed": source["figure_digitization_performed"] == "true",
            "pointwise_covariance": source["pointwise_covariance"],
            "polaron_anomalies_separated_from_intrinsic_gap": all(
                row["intrinsic_gap_evidence"] == "false" for row in polarons
            ),
            "part_i_double_counting_prohibited": all(
                row["double_counting_allowed"] == "false" for row in links
            ),
        },
        "completion_status": "PRIMARY_SOURCE_AUDIT_PROVENANCE_COMPLETE",
        "controlling_decision": "primary_source_recovered_semiconducting_transition_interaction_gap_candidates_and_x0_reconstructed_hansen_marker_mapping_unresolved",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
