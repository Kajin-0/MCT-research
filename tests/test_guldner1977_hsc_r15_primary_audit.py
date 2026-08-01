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


def test_source_identity_and_binary_provenance_are_complete() -> None:
    row = read_csv("guldner1977_hsc_r15_source_metadata.csv")[0]
    assert row["doi"] == "10.1002/pssb.2220820115"
    assert row["source_pdf_page_count"] == "10"
    assert row["source_pdf_sha256"] == "85bdf09852eb02747158a80f7854d202a69a48d98c9c571a396f8a4cd51c8704"
    assert row["source_pdf_sha256_status"] == "materialized_conversation_attachment"
    assert row["source_file_library_id"] == "file_000000006f0881fda163c0e4ae6a72c3"
    assert row["source_binary_committed"] == "false"
    assert "A. Mycielski" in row["authors"]


def test_five_printed_composition_gap_groups_preserve_precision() -> None:
    rows = read_csv("guldner1977_hsc_r15_specimen_groups.csv")
    assert len(rows) == 5
    assert [row["composition_x"] for row in rows] == [
        "0.250",
        "0.215",
        "0.280",
        "0.150",
        "0.185",
    ]
    assert rows[0]["composition_qualifier"] == "approximate"
    assert rows[1]["composition_qualifier"] == "approximate"
    assert rows[2]["composition_qualifier"] == "exact_as_printed"
    assert rows[3]["composition_qualifier"] == "approximate"
    assert all(row["physical_specimen_count_status"] == "unresolved" for row in rows)


def test_printed_interaction_gap_candidates_cross_zero() -> None:
    rows = read_csv("guldner1977_hsc_r15_interaction_gap_candidates.csv")
    assert len(rows) == 5
    assert {row["interaction_gap_meV"] for row in rows} == {"-30", "35", "86", "161", "208"}
    assert sum(row["gap_sign"] == "negative" for row in rows) == 1
    assert sum(row["gap_sign"] == "positive" for row in rows) == 4
    assert all(row["source_native_gap_determination"] == "true" for row in rows)
    assert all(row["raw_observable"] == "false" for row in rows)
    assert all(row["printed_gap_uncertainty_meV"] == "" for row in rows)
    assert all(row["figure_digitized"] == "false" for row in rows)


def test_critical_composition_is_not_promoted_to_pointwise_uncertainty() -> None:
    figures = {row["figure_id"]: row for row in read_csv("guldner1977_hsc_r15_figure_evidence.csv")}
    fig11 = figures["G77II_FIG11"]
    assert fig11["reported_relation"] == "epsilon0_of_x_is_linear"
    assert fig11["printed_scalar_result"] == "x0=0.165+/-0.005"
    assert fig11["coordinates_digitized"] == "false"
    groups = read_csv("guldner1977_hsc_r15_specimen_groups.csv")
    assert all(row["composition_uncertainty"] == "" for row in groups)


def test_representative_and_global_band_parameters_are_separated() -> None:
    rows = read_csv("guldner1977_hsc_r15_band_parameter_constraints.csv")
    global_rows = {row["parameter_id"]: row for row in rows if row["scope"] == "global"}
    fit_rows = [row for row in rows if row["scope"] == "representative_fit"]
    assert global_rows["G77II_P_DELTA"]["value"] == "1"
    assert global_rows["G77II_P_GAMMA1"]["uncertainty"] == "1.5"
    assert global_rows["G77II_P_KAPPA"]["value"] == "-1"
    assert global_rows["G77II_P_MHH"]["value"] == "0.4"
    assert len(fit_rows) == 12
    assert {row["composition_x"] for row in fit_rows} == {"0.250", "0.215", "0.280"}


def test_polaron_anomalies_are_not_intrinsic_gap_records() -> None:
    rows = read_csv("guldner1977_hsc_r15_polaron_anomalies.csv")
    assert len(rows) == 3
    assert {row["phonon_energy_meV"] for row in rows} == {"17", "19.5"}
    critical = next(row for row in rows if row["record_id"] == "G77II_POL_195_SIGMA_MINUS")
    assert critical["critical_field_kG"] == "29.5"
    assert all(row["intrinsic_gap_evidence"] == "false" for row in rows)
    assert all(row["quantitative_model_complete"] == "false" for row in rows)


def test_calculated_figures_are_not_raw_measurements() -> None:
    rows = {row["figure_id"]: row for row in read_csv("guldner1977_hsc_r15_figure_evidence.csv")}
    assert rows["G77II_FIG12"]["authorized_use"] == "qualitative_non_linear_parameter_trend"
    assert rows["G77II_FIG13"]["prohibited_use"] == "raw_effective_mass_measurement_claim"
    assert rows["G77II_FIG14"]["prohibited_use"] == "raw_Lande_factor_measurement_claim"
    assert all(row["coordinates_digitized"] == "false" for row in rows.values())


def test_part_i_linkage_prevents_double_counting() -> None:
    rows = read_csv("guldner1977_hsc_r15_part_i_links.csv")
    assert len(rows) == 3
    assert {row["target_graph_id"] for row in rows} == {"HSC_R14"}
    assert all(row["same_specimen_established"] == "false" for row in rows)
    assert all(row["double_counting_allowed"] == "false" for row in rows)


def test_hansen_candidates_are_not_assignments_or_validation() -> None:
    rows = read_csv("guldner1977_hsc_r15_hansen_ingestion_candidates.csv")
    assert len(rows) == 5
    assert all(row["source_native_gap_determination"] == "true" for row in rows)
    assert all(row["hansen_assignment_resolved"] == "false" for row in rows)
    assert all(row["independent_validation"] == "false" for row in rows)


def test_source_graph_is_updated_without_overclaim() -> None:
    rows = read_csv("hansen_1982_source_graph.csv")
    row = next(row for row in rows if row["graph_id"] == "HSC_R15")
    assert row["measurement_group"] == "interband_magnetoabsorption"
    assert row["composition_method_stated_by_hansen"] == "density measurements and electron microprobe"
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    assert "SHA256 85bdf09852eb02747158a80f7854d202a69a48d98c9c571a396f8a4cd51c8704" in row["notes"]
    assert "Hansen marker mapping remain unresolved" in row["notes"]


def test_readme_enforces_core_boundaries() -> None:
    text = (DATA / "guldner1977_hsc_r15_README.md").read_text(encoding="utf-8")
    assert "85bdf09852eb02747158a80f7854d202a69a48d98c9c571a396f8a4cd51c8704" in text
    assert "Figure 11 is not digitized" in text
    assert "polaron energies or splittings as intrinsic gaps" in text
    assert "assign Hansen markers by plot proximity" in text


def test_canonical_audit_regenerates_byte_identically() -> None:
    expected = (ROOT / "data" / "validation" / "guldner1977_hsc_r15_audit.json").read_bytes()
    actual = subprocess.check_output(
        [sys.executable, str(ROOT / "tools" / "audit_guldner1977_hsc_r15.py")],
        cwd=ROOT,
    )
    assert actual == expected
    report = json.loads(actual)
    assert report["completion_status"] == "PRIMARY_SOURCE_AUDIT_PROVENANCE_COMPLETE"
    assert report["interaction_gap_candidates"]["count"] == 5
    assert report["interaction_gap_candidates"]["signed_transition_bracket_present"] is True
    assert report["critical_composition"]["value"] == "0.165"
    assert report["polaron_anomalies"]["intrinsic_gap_evidence_count"] == 0
    assert report["part_i_links"]["double_counting_authorized_count"] == 0
    assert report["hansen_candidates"]["resolved_assignment_count"] == 0
    assert report["deterministic_checks"]["source_hash_materialized"] is True
    assert report["deterministic_checks"]["source_hash_matches_expected"] is True
    assert report["deterministic_checks"]["source_hash_status_is_materialized"] is True
