#!/usr/bin/env python3
"""Generate the deterministic Dornhaus 1977 HSC_R13 primary-source audit."""
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

def dec(value: str) -> Decimal:
    return Decimal(value)

def main() -> None:
    source = read_csv("dornhaus1977_hsc_r13_source_metadata.csv")
    samples = read_csv("dornhaus1977_table1_samples.csv")
    ranges = read_csv("dornhaus1977_powerlaw_ranges.csv")
    parameters = read_csv("dornhaus1977_band_parameters.csv")
    assumptions = read_csv("dornhaus1977_model_assumptions.csv")
    candidates = read_csv("dornhaus1977_hansen_ingestion_candidates.csv")

    composition_counts = Counter(row["composition_x"] for row in samples)
    uncertainty_samples = [row["sample_id"] for row in samples if row["composition_uncertainty_x"]]
    alpha_all = [dec(row["alpha"]) for row in ranges]
    alpha_4p2 = [dec(row["alpha"]) for row in ranges if row["temperature_k"] == "4.2"]
    low_temperature_samples = sorted({row["sample_id"] for row in ranges if dec(row["temperature_k"]) < Decimal("4.2")})

    q = Decimal("1.602176634e-19")
    mobility_relative_residuals = []
    for row in samples:
        if not row["hall_mobility_10_m2_per_v_s_at_b0_4p2k"]:
            continue
        density = dec(row["carrier_density_1e20_m_minus3_at_b0_4p2k"]) * Decimal("1e20")
        resistivity = dec(row["resistivity_1e_minus5_ohm_m_at_b0_4p2k"]) * Decimal("1e-5")
        mobility = dec(row["hall_mobility_10_m2_per_v_s_at_b0_4p2k"]) * Decimal("10")
        calculated = Decimal(1) / (q * density * resistivity)
        mobility_relative_residuals.append(abs(calculated - mobility) / mobility)

    report = {
        "schema_version": 1,
        "source_id": source[0]["source_id"],
        "hansen_graph_id": source[0]["hansen_graph_id"],
        "source_pdf_sha256": source[0]["source_pdf_sha256"],
        "source_pdf_page_count": int(source[0]["source_pdf_page_count"]),
        "measurement_class": source[0]["primary_measurement_class"],
        "table1": {
            "sample_count": len(samples),
            "composition_group_count": len(composition_counts),
            "composition_sample_counts": dict(sorted(composition_counts.items())),
            "printed_composition_uncertainty_samples": uncertainty_samples,
            "carrier_density_min_1e20_m_minus3": format(min(dec(row["carrier_density_1e20_m_minus3_at_b0_4p2k"]) for row in samples), "f"),
            "carrier_density_max_1e20_m_minus3": format(max(dec(row["carrier_density_1e20_m_minus3_at_b0_4p2k"]) for row in samples), "f"),
        },
        "power_law_ranges": {
            "record_count": len(ranges),
            "alpha_min_all": format(min(alpha_all), "f"),
            "alpha_max_all": format(max(alpha_all), "f"),
            "alpha_min_4p2k": format(min(alpha_4p2), "f"),
            "alpha_max_4p2k": format(max(alpha_4p2), "f"),
            "low_temperature_samples": low_temperature_samples,
        },
        "band_parameters": {
            "unique_composition_count": len(parameters),
            "gap_values_eV_by_x": {row["composition_x"]: row["gap_eV"] for row in parameters},
            "independent_gap_observation_count": sum(row["independent_gap_observation"].lower() == "true" for row in parameters),
        },
        "assumptions": {"count": len(assumptions), "ids": [row["assumption_id"] for row in assumptions]},
        "hansen_candidates": {
            "count": len(candidates),
            "independent_gap_observation_count": sum(row["independent_gap_observation"].lower() == "true" for row in candidates),
            "ids": [row["candidate_id"] for row in candidates],
        },
        "deterministic_checks": {
            "x_020_sample_count": composition_counts["0.200"],
            "max_hall_mobility_relative_residual": format(max(mobility_relative_residuals), ".12f"),
            "source_binary_committed": source[0]["source_binary_committed"] == "true",
            "figure_digitization_performed": source[0]["figure_digitization_performed"] == "true",
            "all_candidates_nonindependent": all(row["independent_gap_observation"].lower() == "false" for row in candidates),
        },
        "controlling_decision": "primary_source_recovered_extreme_quantum_limit_magnetotransport_table_reconstructed_gap_parameters_not_direct_observations_hansen_marker_mapping_unresolved",
    }
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
