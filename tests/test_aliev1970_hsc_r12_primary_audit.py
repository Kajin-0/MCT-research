from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hansen"

def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def test_primary_source_identity_and_hash() -> None:
    rows = read_csv("aliev1970_hsc_r12_source_metadata.csv")
    assert len(rows) == 1
    row = rows[0]
    assert row["hansen_graph_id"] == "HSC_R12"
    assert row["title"] == "Electron Effective Mass in the Hg1-xCdxTe System"
    assert row["source_pdf_sha256"] == "be08dc3f926a42f7549b1a7734337fd72701cbcec3d3759373eed772006e44bf"
    assert row["source_pdf_page_count"] == "4"
    assert row["source_binary_committed"] == "false"

def test_measurement_is_thermomagnetic_not_optical() -> None:
    row = read_csv("aliev1970_hsc_r12_source_metadata.csv")[0]
    assert row["primary_measurement_class"] == "strong_field_thermomagnetic_transport"
    assert "No direct gap observable" in row["primary_gap_observable"]

def test_table1_is_complete() -> None:
    rows = read_csv("aliev1970_table1_effective_mass.csv")
    assert len(rows) == 11
    assert all(row["temperature_k"] == "300" for row in rows)
    counts = Counter(row["composition_x"] for row in rows)
    assert counts == Counter({"0.10": 7, "0.05": 1, "0.14": 1, "0.15": 1, "0.20": 1})

def test_table_gap_column_is_equation3_input() -> None:
    rows = read_csv("aliev1970_table1_effective_mass.csv")
    for row in rows:
        x = Decimal(row["composition_x"])
        expected = Decimal("-0.3") + Decimal("0.0005") * Decimal("300") + (
            Decimal("1.91") - Decimal("0.001") * Decimal("300")
        ) * x
        listed = Decimal(row["gap_eV"])
        assert abs(listed - expected) <= Decimal("0.0055")
        assert row["gap_provenance"] == "Equation_3_empirical_input_not_independent_measurement"

def test_theoretical_band_edge_mass_matches_equation2_k_zero() -> None:
    rows = read_csv("aliev1970_table1_effective_mass.csv")
    for row in rows:
        x = Decimal(row["composition_x"])
        gap = abs(Decimal(row["gap_eV"]))
        ep = Decimal("18") + Decimal("3") * x
        expected = Decimal(1) / (Decimal(1) + Decimal(2) * ep / (Decimal(3) * gap))
        listed = Decimal(row["band_edge_mass_theory_m0"])
        assert abs(listed - expected) <= Decimal("0.00034")

def test_relations_preserve_wiley_dexter_lineage() -> None:
    rows = {row["relation_id"]: row for row in read_csv("aliev1970_relations.csv")}
    assert rows["AL70_EQ3"]["status"] == "adopted_input_not_independent_result"
    assert "Wiley and Dexter" in rows["AL70_EQ3"]["source_lineage"]
    assert rows["AL70_EQ4"]["status"] == "adopted_input_not_independent_result"

def test_no_candidate_is_independent_gap_evidence() -> None:
    rows = read_csv("aliev1970_hansen_ingestion_candidates.csv")
    assert len(rows) == 6
    assert all(row["independent_gap_observation"] == "false" for row in rows)
    assert sum(bool(row["gap_eV"]) for row in rows) == 5

def test_readme_preserves_scientific_boundary() -> None:
    text = (DATA / "aliev1970_hsc_r12_README.md").read_text(encoding="utf-8")
    assert "not independent measurements" in text
    assert "lineage duplication" in text
    assert "cannot independently validate Hansen" in text
    assert "do not create repeated gap evidence" in (
        ROOT / "research/programs/empirical_bandgap/state_updates/2026-07-24-aliev1970-hsc-r12-primary-audit.md"
    ).read_text(encoding="utf-8")

def test_source_graph_is_corrected() -> None:
    rows = {row["graph_id"]: row for row in read_csv("hansen_1982_source_graph.csv")}
    row = rows["HSC_R12"]
    assert row["measurement_group"] == "strong_field_thermomagnetic_transport"
    assert row["temperature_series_mapping"] == "unresolved_equation3_values_vs_effective_mass_records"
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    assert "Wiley-Dexter" in row["notes"]

def test_audit_regenerates_byte_identically() -> None:
    generated = subprocess.check_output(
        [sys.executable, str(ROOT / "tools/audit_aliev1970_hsc_r12.py")],
        text=True,
    )
    committed = (ROOT / "data/validation/aliev1970_hsc_r12_audit.json").read_text(encoding="utf-8")
    assert generated == committed
    report = json.loads(generated)
    assert report["table1"]["row_count"] == 11
    assert report["hansen_candidates"]["independent_gap_observation_count"] == 0
