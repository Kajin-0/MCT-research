#!/usr/bin/env python3
"""Generate the deterministic Guldner 1977 HSC_R14 primary-source audit."""
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
    source = read_csv("guldner1977_hsc_r14_source_metadata.csv")[0]
    groups = read_csv("guldner1977_specimen_groups.csv")
    gaps = read_csv("guldner1977_interaction_gap_candidates.csv")
    acceptors = read_csv("guldner1977_acceptor_states.csv")
    parameters = read_csv("guldner1977_band_parameter_constraints.csv")
    assumptions = read_csv("guldner1977_model_assumptions.csv")
    links = read_csv("guldner1977_hsc_r14_cross_source_links.csv")
    candidates = read_csv("guldner1977_hansen_ingestion_candidates.csv")

    gap_values = [dec(row["interaction_gap_meV"]) for row in gaps]
    report = {
        "schema_version": 1,
        "source_id": source["source_id"],
        "hansen_graph_id": source["hansen_graph_id"],
        "source_pdf_sha256": source["source_pdf_sha256"],
        "source_pdf_page_count": int(source["source_pdf_page_count"]),
        "measurement_class": source["primary_measurement_class"],
        "specimen_groups": {
            "count": len(groups),
            "composition_values": [row["composition_x"] for row in groups],
            "composition_method": source["composition_method"],
            "physical_specimen_count_resolved": all(row["physical_specimen_count_status"] != "unresolved" for row in groups),
        },
        "interaction_gap_candidates": {
            "count": len(gaps),
            "values_meV_by_x": {row["composition_x"]: row["interaction_gap_meV"] for row in gaps},
            "minimum_meV": format(min(gap_values), "f"),
            "maximum_meV": format(max(gap_values), "f"),
            "all_negative": all(value < 0 for value in gap_values),
            "source_native_gap_determination_count": sum(row["source_native_gap_determination"] == "true" for row in gaps),
            "raw_observable_count": sum(row["raw_observable"] == "true" for row in gaps),
            "reported_pointwise_uncertainty_count": sum(bool(row["printed_gap_uncertainty_meV"]) for row in gaps),
        },
        "acceptor_states": {
            "count": len(acceptors),
            "labels": sorted({row["acceptor_label"] for row in acceptors}),
            "intrinsic_gap_evidence_count": sum(row["intrinsic_gap_evidence"] == "true" for row in acceptors),
        },
        "band_parameter_constraints": {
            "count": len(parameters),
            "ids": [row["parameter_id"] for row in parameters],
        },
        "model_assumptions": {
            "count": len(assumptions),
            "ids": [row["assumption_id"] for row in assumptions],
        },
        "cross_source_links": {
            "count": len(links),
            "target_graph_ids": sorted({row["target_graph_id"] for row in links}),
            "all_cross_reference_only": all(row["status"] == "cross_reference_only_not_reconstructed" for row in links),
        },
        "hansen_candidates": {
            "count": len(candidates),
            "all_source_native": all(row["source_native_gap_determination"] == "true" for row in candidates),
            "resolved_assignment_count": sum(row["hansen_assignment_resolved"] == "true" for row in candidates),
        },
        "deterministic_checks": {
            "source_binary_committed": source["source_binary_committed"] == "true",
            "figure_digitization_performed": source["figure_digitization_performed"] == "true",
            "pointwise_covariance": source["pointwise_covariance"],
            "part_ii_relation_reconstructed": any(row["status"] != "cross_reference_only_not_reconstructed" for row in links),
            "acceptors_separated_from_intrinsic_gap": all(row["intrinsic_gap_evidence"] == "false" for row in acceptors),
        },
        "controlling_decision": "primary_source_recovered_semimetallic_magnetotransmission_gap_candidates_reconstructed_part_ii_relation_and_hansen_marker_mapping_unresolved",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
