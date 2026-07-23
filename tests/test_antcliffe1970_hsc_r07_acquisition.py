from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/hansen/antcliffe1970_hsc_r07_source_metadata.csv"
README_PATH = ROOT / "data/hansen/antcliffe1970_hsc_r07_README.md"
SOURCE_GRAPH_PATH = ROOT / "data/hansen/hansen_1982_source_graph.csv"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_exact_public_identity_and_unavailable_full_text_boundary() -> None:
    rows = _csv(METADATA_PATH)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "ANTCLIFFE1970_HSC_R07"
    assert row["hansen_graph_id"] == "HSC_R07"
    assert row["publication_year"] == "1970"
    assert row["author"] == "G. A. Antcliffe"
    assert row["title"] == "Effective Mass and Spin Splitting in Hg1-xCdxTe"
    assert row["container"] == "Physical Review B"
    assert row["volume"] == "2"
    assert row["issue"] == "2"
    assert row["starting_page"] == "345"
    assert row["publication_date"] == "1970-07-15"
    assert row["doi"] == "10.1103/PhysRevB.2.345"
    assert row["publisher_metadata_status"] == "verified_from_aps_issue_metadata"
    assert row["full_text_status"] == "not_available_in_user_file_library_or_repository"
    assert row["source_file_library_name"] == ""
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


def test_unresolved_primary_fields_remain_unresolved() -> None:
    row = _csv(METADATA_PATH)[0]
    unresolved_fields = [
        "primary_observable_status",
        "specimen_registry_status",
        "composition_provenance_status",
        "temperature_range_status",
        "magnetic_field_geometry_status",
        "direct_observations_status",
    ]
    for field in unresolved_fields:
        assert row[field] == "unresolved_primary_full_text_required"
    assert row["page_range_status"] == (
        "starting_page_verified_end_page_unresolved_without_full_text"
    )
    assert row["numerical_reconstruction_status"] == (
        "blocked_primary_full_text_required"
    )


def test_hansen_graph_identity_is_preserved_without_added_specificity() -> None:
    rows = {row["graph_id"]: row for row in _csv(SOURCE_GRAPH_PATH)}
    row = rows["HSC_R07"]
    assert row["citation_as_printed"] == (
        "G. A. Antcliffe, Phys. Rev. B 2, 345 (1970)"
    )
    assert row["role_in_hansen"] == "fitted_data"
    assert row["measurement_group"] == "magneto_optical_unspecified_in_hansen"
    assert row["gap_observable"] == "magneto_optical_gap"
    assert row["composition_method_stated_by_hansen"] == "not_stated_in_hansen"
    assert row["temperature_series_mapping"] == "unresolved"


def test_secondary_context_is_not_promoted_to_primary_data() -> None:
    row = _csv(METADATA_PATH)[0]
    assert row["secondary_context_status"] == (
        "secondary_citations_available_not_authorized_for_reconstruction"
    )
    notes = row["notes"]
    for source in ["Weiler 1977", "Groves 1971", "Chu 1991", "Hansen 1982"]:
        assert source in notes
    assert "Do not infer specimens" in notes


def test_readme_states_fail_closed_acquisition_result() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    required = [
        "HSC_R07 numerical reconstruction = blocked",
        "direct observation ledger = absent",
        "The terminal page is not asserted",
        "These are secondary or later cross-source context",
        "None of those fields is populated from inference",
        "does not reconstruct numerical observations",
    ]
    for phrase in required:
        assert phrase in text


def test_no_inferred_antcliffe_numerical_products_exist() -> None:
    forbidden = [
        ROOT / "data/hansen/antcliffe1970_hsc_r07_digitized.csv",
        ROOT / "data/hansen/antcliffe1970_hsc_r07_gap_points.csv",
        ROOT / "data/hansen/antcliffe1970_hsc_r07_specimens.csv",
        ROOT / "data/hansen/antcliffe1970_hsc_r07_band_parameters.csv",
        ROOT / "data/hansen/antcliffe1970_hsc_r07_secondary_reconstruction.csv",
    ]
    assert all(not path.exists() for path in forbidden)
