#!/usr/bin/env python3
"""Generate the deterministic Aliev 1970 HSC_R12 primary-source audit."""
from __future__ import annotations

import csv
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hansen"

def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def d(value: str) -> Decimal:
    return Decimal(value)

def main() -> None:
    source = read_csv("aliev1970_hsc_r12_source_metadata.csv")
    groups = read_csv("aliev1970_composition_groups.csv")
    table = read_csv("aliev1970_table1_effective_mass.csv")
    relations = read_csv("aliev1970_relations.csv")
    assumptions = read_csv("aliev1970_model_assumptions.csv")
    candidates = read_csv("aliev1970_hansen_ingestion_candidates.csv")

    composition_counts = Counter(row["composition_x"] for row in table)
    distinct_gaps = {
        row["composition_x"]: row["gap_eV"]
        for row in table
    }

    gap_relation_residuals = []
    band_edge_residuals = []
    for row in table:
        x = d(row["composition_x"])
        listed_gap = d(row["gap_eV"])
        equation_gap = Decimal("-0.3") + Decimal("0.0005") * Decimal("300") + (
            Decimal("1.91") - Decimal("0.001") * Decimal("300")
        ) * x
        gap_relation_residuals.append(abs(listed_gap - equation_gap))

        ep = Decimal("18") + Decimal("3") * x
        theoretical = Decimal(1) / (
            Decimal(1) + Decimal(2) * ep / (Decimal(3) * abs(listed_gap))
        )
        listed_band_edge = d(row["band_edge_mass_theory_m0"])
        band_edge_residuals.append(abs(listed_band_edge - theoretical))

    report = {
        "schema_version": 1,
        "source_id": source[0]["source_id"],
        "hansen_graph_id": source[0]["hansen_graph_id"],
        "source_pdf_sha256": source[0]["source_pdf_sha256"],
        "source_pdf_page_count": int(source[0]["source_pdf_page_count"]),
        "measurement_class": source[0]["primary_measurement_class"],
        "temperature_k": int(source[0]["temperature_k"]),
        "table1": {
            "row_count": len(table),
            "composition_group_count": len(groups),
            "composition_row_counts": dict(sorted(composition_counts.items())),
            "distinct_gap_values_by_x": dict(sorted(distinct_gaps.items())),
            "carrier_density_min_cm3": min(row["carrier_density_cm3"] for row in table),
            "carrier_density_max_cm3": max(row["carrier_density_cm3"] for row in table),
            "gap_provenance_values": sorted({row["gap_provenance"] for row in table}),
        },
        "relations": {
            "count": len(relations),
            "ids": [row["relation_id"] for row in relations],
            "equation3_status": next(
                row["status"] for row in relations if row["relation_id"] == "AL70_EQ3"
            ),
            "equation4_status": next(
                row["status"] for row in relations if row["relation_id"] == "AL70_EQ4"
            ),
        },
        "assumptions": {
            "count": len(assumptions),
            "ids": [row["assumption_id"] for row in assumptions],
        },
        "hansen_candidates": {
            "count": len(candidates),
            "numeric_count": sum(bool(row["gap_eV"]) for row in candidates),
            "independent_gap_observation_count": sum(
                row["independent_gap_observation"].lower() == "true"
                for row in candidates
            ),
            "ids": [row["candidate_id"] for row in candidates],
        },
        "deterministic_checks": {
            "max_abs_table_gap_minus_equation3_eV": format(max(gap_relation_residuals), "f"),
            "max_abs_theoretical_band_edge_mass_residual_m0": format(max(band_edge_residuals), "f"),
            "all_table_rows_at_300_k": all(row["temperature_k"] == "300" for row in table),
            "x_010_row_count": composition_counts["0.10"],
            "source_binary_committed": source[0]["source_binary_committed"] == "true",
            "figure_digitization_performed": source[0]["figure_digitization_performed"] == "true",
        },
        "controlling_decision": (
            "primary_source_recovered_thermomagnetic_effective_mass_table_reconstructed_"
            "gap_values_are_adopted_wiley_dexter_equation_inputs_"
            "hansen_marker_mapping_unresolved"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
