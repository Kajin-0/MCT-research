from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/hansen/weiler1981_hsc_r04_source_metadata.csv"
PROVENANCE_PATH = ROOT / "data/hansen/weiler1981_hsc_r04_composition_provenance.csv"
README_PATH = ROOT / "data/hansen/weiler1981_hsc_r04_README.md"
EXISTING_EVIDENCE_PATH = ROOT / "data/evidence/guldner_weiler_1977_magneto_core.json"
SOURCE_GRAPH_PATH = ROOT / "data/hansen/hansen_1982_source_graph.csv"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_exact_chapter_identity_and_unavailable_full_text_boundary() -> None:
    rows = _csv(METADATA_PATH)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "WEILER1981_HSC_R04"
    assert row["hansen_graph_id"] == "HSC_R04"
    assert row["publication_year"] == "1981"
    assert row["title"] == "Magnetooptical Properties of Hg1-xCdxTe Alloys"
    assert row["container"] == "Semiconductors and Semimetals"
    assert row["volume"] == "16"
    assert row["pages"] == "119-191"
    assert row["doi"] == "10.1016/S0080-8784(08)60130-1"
    assert row["publisher_metadata_status"] == "verified_from_publisher_metadata"
    assert row["full_text_status"] == "not_available_in_user_file_library_or_repository"
    assert row["source_file_library_name"] == ""
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


def test_chapter_scope_does_not_claim_specimen_mapping() -> None:
    row = _csv(METADATA_PATH)[0]
    assert row["relationship_to_weiler1977"] == (
        "likely_review_lineage_not_specimen_identity_proof"
    )
    assert row["numerical_chapter_data_status"] == "unresolved_full_text_required"
    assert row["temperature_series_mapping_status"] == "unresolved"
    assert row["specimen_identity_mapping_status"] == "unresolved"
    assert "Do not infer chapter tables" in row["notes"]


def test_existing_weiler_1977_evidence_is_linked_without_duplication() -> None:
    row = _csv(METADATA_PATH)[0]
    assert row["existing_evidence_record"] == (
        "data/evidence/guldner_weiler_1977_magneto_core.json"
    )
    evidence = json.loads(EXISTING_EVIDENCE_PATH.read_text(encoding="utf-8"))
    weiler_sources = [
        source for source in evidence["sources"] if source["source_id"] == "weiler_1977"
    ]
    assert len(weiler_sources) == 1
    source = weiler_sources[0]
    assert source["doi"] == "10.1103/PhysRevB.16.3603"
    assert source["primary_full_text_recovered"] is True


def test_three_composition_provenance_layers_are_distinct() -> None:
    rows = {row["provenance_id"]: row for row in _csv(PROVENANCE_PATH)}
    assert set(rows) == {
        "WEILER1977_PUBLISHED",
        "MICKLETHWAITE_PRIVATE",
        "REINE_PRIVATE",
    }

    published = rows["WEILER1977_PUBLISHED"]
    assert published["source_layer"] == "Weiler_1977_primary_paper"
    assert published["per_specimen_values_available"] == "true"
    assert published["synthetic_reconstruction_authorized"] == "false"

    micklethwaite = rows["MICKLETHWAITE_PRIVATE"]
    assert micklethwaite["used_by_hansen"] == "true"
    assert micklethwaite["measurement_or_assignment_method"] == "transmission_cutoff"
    assert micklethwaite["per_specimen_values_available"] == "false"
    assert micklethwaite["numerical_shift_min_x"] == ""
    assert micklethwaite["numerical_shift_max_x"] == ""
    assert micklethwaite["synthetic_reconstruction_authorized"] == "false"

    reine = rows["REINE_PRIVATE"]
    assert reine["used_by_hansen"] == "false"
    assert reine["measurement_or_assignment_method"] == "density"
    assert reine["per_specimen_values_available"] == "false"
    assert float(reine["numerical_shift_min_x"]) == 0.01
    assert float(reine["numerical_shift_max_x"]) == 0.035
    assert reine["synthetic_reconstruction_authorized"] == "false"


def test_hansen_graph_preserves_hsc_r04_private_provenance_statement() -> None:
    rows = {row["graph_id"]: row for row in _csv(SOURCE_GRAPH_PATH)}
    row = rows["HSC_R04"]
    assert row["role_in_hansen"] == "fitted_data"
    assert row["measurement_group"] == "magneto_reflectance"
    assert "Micklethwaite" in row["composition_method_stated_by_hansen"]
    assert "+0.01 to +0.035" in row["composition_method_stated_by_hansen"]
    assert row["temperature_series_mapping"] == "unresolved"


def test_readme_states_fail_closed_numerical_boundary() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    required = [
        "HSC_R04 numerical reconstruction = blocked",
        "private composition reconstruction = not authorized",
        "1977-to-1981 specimen identity = unresolved",
        "The reported Reine shift range is not a transformation rule",
        "does not establish chapter-level numerical data",
    ]
    for phrase in required:
        assert phrase in text


def test_no_synthetic_private_composition_products_exist() -> None:
    forbidden = [
        ROOT / "data/hansen/weiler1981_micklethwaite_reconstructed.csv",
        ROOT / "data/hansen/weiler1981_reine_shifted_compositions.csv",
        ROOT / "data/hansen/weiler1981_hsc_r04_digitized.csv",
        ROOT / "data/hansen/weiler1981_hsc_r04_gap_points.csv",
    ]
    assert all(not path.exists() for path in forbidden)
