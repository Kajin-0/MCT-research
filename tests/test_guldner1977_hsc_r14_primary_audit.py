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


def test_source_identity_hash_and_author_correction() -> None:
    row = read_csv("guldner1977_hsc_r14_source_metadata.csv")[0]
    assert row["source_pdf_sha256"] == "e460fcc11e7627b1a3ec7346483bf88494b18e4fb69272b2af7e6ab61da3ef5b"
    assert row["source_pdf_page_count"] == "13"
    assert "A. Mycielski" in row["authors"]
    assert "M. Grynberg" not in row["authors"]
    assert row["primary_measurement_class"] == "interband_and_intraband_magnetotransmission"


def test_five_composition_groups_preserve_precision() -> None:
    rows = read_csv("guldner1977_specimen_groups.csv")
    assert len(rows) == 5
    assert [row["composition_x"] for row in rows] == ["0.010", "0.025", "0.050", "0.105", "0.115"]
    assert rows[0]["composition_qualifier"] == "mixed_exact_and_approximate_printing"
    assert rows[3]["composition_qualifier"] == "approximate"
    assert all(row["composition_method"] == "not_reported" for row in rows)


def test_printed_interaction_gap_candidates_are_complete() -> None:
    rows = read_csv("guldner1977_interaction_gap_candidates.csv")
    assert len(rows) == 5
    assert {row["interaction_gap_meV"] for row in rows} == {"-285", "-261", "-207", "-110", "-90"}
    assert all(row["gap_sign"] == "negative" for row in rows)
    assert all(row["source_native_gap_determination"] == "true" for row in rows)
    assert all(row["raw_observable"] == "false" for row in rows)
    assert all(row["printed_gap_uncertainty_meV"] == "" for row in rows)


def test_acceptors_are_not_intrinsic_gap_records() -> None:
    rows = read_csv("guldner1977_acceptor_states.csv")
    assert len(rows) == 3
    assert {row["acceptor_label"] for row in rows} == {"A0", "A1"}
    assert all(row["intrinsic_gap_evidence"] == "false" for row in rows)
    x0115 = next(row for row in rows if row["record_id"] == "G77_A1_X0115")
    assert x0115["binding_energy_meV"] == "5.5"
    assert x0115["binding_energy_uncertainty_meV"] == "0.5"


def test_band_parameter_uncertainty_semantics() -> None:
    rows = {row["parameter_id"]: row for row in read_csv("guldner1977_band_parameter_constraints.csv")}
    assert rows["G77_P_DELTA"]["value"] == "1"
    assert rows["G77_P_GAMMA1"]["value"] == "4.5"
    assert rows["G77_P_GAMMA1"]["uncertainty"] == "1.5"
    assert rows["G77_P_KAPPA"]["value"] == "-1"
    assert rows["G77_P_MHH"]["value"] == "0.4"
    assert rows["G77_P_MHH"]["uncertainty"] == "0.1"


def test_part_ii_relations_are_cross_references_only() -> None:
    rows = read_csv("guldner1977_hsc_r14_cross_source_links.csv")
    assert len(rows) == 2
    assert {row["target_graph_id"] for row in rows} == {"HSC_R15"}
    assert all(row["status"] == "cross_reference_only_not_reconstructed" for row in rows)
    assert any("Figure 11" in row["notes"] for row in rows)


def test_hansen_candidates_are_not_assignments() -> None:
    rows = read_csv("guldner1977_hansen_ingestion_candidates.csv")
    assert len(rows) == 5
    assert all(row["source_native_gap_determination"] == "true" for row in rows)
    assert all(row["hansen_assignment_resolved"] == "false" for row in rows)


def test_readme_enforces_core_boundaries() -> None:
    text = (DATA / "guldner1977_hsc_r14_README.md").read_text(encoding="utf-8")
    assert "A. Mycielski" in text
    assert "Acceptor binding energies are not intrinsic bandgaps" in text
    assert "not present in the HSC_R14 article" in text
    assert "assign Hansen markers by plot proximity" in text


def test_source_graph_classification_and_author_are_corrected() -> None:
    rows = read_csv("hansen_1982_source_graph.csv")
    row = next(row for row in rows if row["graph_id"] == "HSC_R14")
    assert "A. Mycielski" in row["citation_as_printed"]
    assert row["measurement_group"] == "interband_and_intraband_magnetotransmission"
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    row15 = next(row for row in rows if row["graph_id"] == "HSC_R15")
    assert "A. Mycielski" in row15["citation_as_printed"]


def test_canonical_audit_regenerates_byte_identically() -> None:
    expected = (ROOT / "data" / "validation" / "guldner1977_hsc_r14_audit.json").read_bytes()
    actual = subprocess.check_output([sys.executable, str(ROOT / "tools" / "audit_guldner1977_hsc_r14.py")], cwd=ROOT)
    assert actual == expected
    report = json.loads(actual)
    assert report["interaction_gap_candidates"]["count"] == 5
    assert report["interaction_gap_candidates"]["source_native_gap_determination_count"] == 5
    assert report["interaction_gap_candidates"]["raw_observable_count"] == 0
    assert report["acceptor_states"]["intrinsic_gap_evidence_count"] == 0
    assert report["cross_source_links"]["all_cross_reference_only"] is True
    assert report["controlling_decision"].endswith("hansen_marker_mapping_unresolved")
