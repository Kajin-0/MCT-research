from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hansen"

def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def test_source_metadata_and_measurement_class() -> None:
    row = read_csv("dornhaus1977_hsc_r13_source_metadata.csv")[0]
    assert row["source_pdf_sha256"] == "245d79984caf798916820e36d8afc0f0f9d54d8961a9da443d1491c3885c3200"
    assert row["source_pdf_page_count"] == "5"
    assert row["primary_measurement_class"] == "extreme_quantum_limit_transverse_magnetotransport"
    assert row["source_binary_committed"] == "false"

def test_all_nine_table1_samples_are_preserved() -> None:
    rows = read_csv("dornhaus1977_table1_samples.csv")
    assert len(rows) == 9
    assert [row["sample_number"] for row in rows] == [str(i) for i in range(1, 10)]
    assert sum(row["composition_x"] == "0.200" for row in rows) == 5

def test_printed_composition_uncertainties_are_not_broadened() -> None:
    rows = read_csv("dornhaus1977_table1_samples.csv")
    observed = {row["sample_id"]: row["composition_uncertainty_x"] for row in rows if row["composition_uncertainty_x"]}
    assert observed == {"DN77_S1": "0.005", "DN77_S4": "0.005", "DN77_S7": "0.005", "DN77_S8": "0.005"}

def test_powerlaw_intervals_and_temperature_splits() -> None:
    rows = read_csv("dornhaus1977_powerlaw_ranges.csv")
    assert len(rows) == 13
    assert min(float(row["alpha"]) for row in rows) == 1.0
    assert max(float(row["alpha"]) for row in rows) == 2.3
    low = {(row["sample_id"], row["temperature_k"]) for row in rows if float(row["temperature_k"]) < 4.2}
    assert low == {("DN77_S5", "1.5"), ("DN77_S8", "1.43")}

def test_4p2k_alpha_range_is_distinct_from_abstract_summary() -> None:
    rows = [row for row in read_csv("dornhaus1977_powerlaw_ranges.csv") if row["temperature_k"] == "4.2"]
    assert min(float(row["alpha"]) for row in rows) == 1.0
    assert max(float(row["alpha"]) for row in rows) == 2.0

def test_gap_parameters_are_five_unique_nonobservations() -> None:
    rows = read_csv("dornhaus1977_band_parameters.csv")
    assert len(rows) == 5
    assert {row["gap_eV"] for row in rows} == {"0.014", "0.0245", "0.047", "0.070", "0.096"}
    assert all(row["independent_gap_observation"] == "false" for row in rows)
    assert all(row["evidence_layer"] == "source_tabulated_transport_model_parameter" for row in rows)

def test_hansen_candidates_do_not_duplicate_x020_rows() -> None:
    rows = read_csv("dornhaus1977_hansen_ingestion_candidates.csv")
    assert len(rows) == 5
    x020 = [row for row in rows if row["composition_x"] == "0.200"]
    assert len(x020) == 1
    assert x020[0]["table1_sample_numbers"] == "4;5;6;7;9"
    assert all(row["independent_gap_observation"] == "false" for row in rows)

def test_source_graph_is_corrected_from_magneto_optical() -> None:
    rows = read_csv("hansen_1982_source_graph.csv")
    row = next(row for row in rows if row["graph_id"] == "HSC_R13")
    assert row["measurement_group"] == "extreme_quantum_limit_transverse_magnetotransport"
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    assert "not direct" in row["gap_observable"]

def test_readme_preserves_prohibited_interpretations() -> None:
    text = (DATA / "dornhaus1977_hsc_r13_README.md").read_text(encoding="utf-8")
    assert "not raw magnetoresistance observations" in text
    assert "no exact power law was found" in text
    assert "count the repeated `x=0.20`" in text
    assert "assign Hansen markers by plot proximity" in text

def test_canonical_audit_regenerates_byte_identically() -> None:
    expected = (ROOT / "data" / "validation" / "dornhaus1977_hsc_r13_audit.json").read_bytes()
    actual = subprocess.check_output([sys.executable, str(ROOT / "tools" / "audit_dornhaus1977_hsc_r13.py")], cwd=ROOT)
    assert actual == expected
    report = json.loads(actual)
    assert report["table1"]["sample_count"] == 9
    assert report["power_law_ranges"]["record_count"] == 13
    assert report["band_parameters"]["independent_gap_observation_count"] == 0
    assert report["controlling_decision"].endswith("hansen_marker_mapping_unresolved")
