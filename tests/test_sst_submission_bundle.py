from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

from tools.build_sst_submission_bundle import build

ROOT = Path(__file__).resolve().parents[1]
METADATA = (
    ROOT
    / "manuscript"
    / "distributional_band_edge"
    / "journal_submission"
    / "submission_metadata.json"
)
REFERENCES = (
    ROOT / "manuscript" / "distributional_band_edge" / "references_verified.json"
)
ANCHORS = (
    ROOT
    / "manuscript"
    / "distributional_band_edge"
    / "journal_submission"
    / "citation_anchors.json"
)


def _load(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_submission_metadata_preserves_known_and_unknown_fields() -> None:
    metadata = _load(METADATA)
    assert metadata["schema_version"] == "1.0"
    assert metadata["program_issue"] == 193
    assert metadata["journal"] == "Semiconductor Science and Technology"
    assert metadata["article_type"] == "Paper"
    assert metadata["default_review_variant"] == "double_anonymous"

    author = metadata["author"]
    assert author["name"] == "Terence Fisher"
    assert author["affiliation"] == "Brooks Photonics"
    assert author["location"] == "Florida, USA"
    assert author["correspondence_email"] is None
    assert author["orcid"] is None
    assert author["full_postal_address"] is None
    assert metadata["archive"]["doi"] is None
    assert metadata["funding"]["status"] == "requires_author_confirmation"


def test_citation_anchor_manifest_covers_every_verified_reference() -> None:
    references = _load(REFERENCES)["references"]
    anchors = _load(ANCHORS)
    reference_keys = {reference["key"] for reference in references}
    cited = set()
    needles = []
    for anchor in anchors["anchors"]:
        needles.append(anchor["needle"])
        cited.update(anchor.get("citation_keys", []))
        cited.update(anchor.get("append_citation_keys", []))
    assert cited == reference_keys
    assert len(needles) == len(set(needles))
    assert anchors["requirements"]["every_anchor_must_match_exactly_once"] is True
    assert anchors["requirements"]["every_verified_reference_must_be_cited"] is True


def test_source_bundle_is_deterministic_and_anonymous_safe(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    manifest_first = build(ROOT, first, compile_pdf=False, commit_sha="test-sha")
    manifest_second = build(ROOT, second, compile_pdf=False, commit_sha="test-sha")

    assert manifest_first["compiled"] is False
    assert manifest_first["verified_reference_count"] == 15
    assert manifest_first["cited_reference_count"] == 15
    assert manifest_first["figure_count"] == 7
    assert manifest_first["table_count"] == 3
    assert manifest_first["archive_doi_issued"] is False
    assert manifest_first["unresolved_submission_blockers"]

    deterministic_files = (
        "manuscript_named.tex",
        "manuscript_anonymous.tex",
        "references.tex",
        "references.bib",
        "cover_letter_named.txt",
        "submission_README.txt",
        "unresolved_metadata.json",
        "sst_named_source.zip",
        "sst_anonymous_source.zip",
        "submission_manifest.json",
    )
    for relative in deterministic_files:
        assert (first / relative).is_file()
        assert _sha256(first / relative) == _sha256(second / relative)

    named = (first / "manuscript_named.tex").read_text(encoding="utf-8")
    anonymous = (first / "manuscript_anonymous.tex").read_text(encoding="utf-8")
    assert "Terence Fisher" in named
    assert "Brooks Photonics" in named
    assert "Florida, USA" in named
    for token in ("Terence Fisher", "Brooks Photonics", "Florida, USA", "Kajin-0"):
        assert token not in anonymous

    assert "\\cite{bellman_astrom_1970,yates_evans_chappell_2009,eisenberg_hayashi_2014}" in named
    assert "\\cite{chang_2006,chang_2007}" in named
    assert "\\cite{chu_mi_tang_1991,ivanov_omskii_2009}" in named
    assert named.count("\\begin{figure}") == 7
    assert named.count("\\begin{longtable}") >= 3
    assert "Funding statement requires final author confirmation" in named
    assert "CORRESPONDENCE_EMAIL_PENDING" in (first / "cover_letter_named.txt").read_text(encoding="utf-8")

    with zipfile.ZipFile(first / "sst_anonymous_source.zip") as archive:
        members = set(archive.namelist())
        assert "manuscript_anonymous.tex" in members
        assert "manuscript_named.tex" not in members
        for member in members:
            if member.endswith((".tex", ".txt", ".bib")):
                text = archive.read(member).decode("utf-8", errors="replace")
                for token in ("Terence Fisher", "Brooks Photonics", "Florida, USA", "Kajin-0"):
                    assert token not in text


def test_reference_outputs_retain_all_dois(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    build(ROOT, output, compile_pdf=False, commit_sha="test-sha")
    references = _load(REFERENCES)["references"]
    tex = (output / "references.tex").read_text(encoding="utf-8")
    bib = (output / "references.bib").read_text(encoding="utf-8")
    for reference in references:
        assert f"\\bibitem{{{reference['key']}}}" in tex
        assert reference["doi"] in tex
        assert f"@article{{{reference['key']}," in bib or f"@misc{{{reference['key']}," in bib
        assert reference["doi"] in bib


def test_manifest_hashes_match_generated_files(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    build(ROOT, output, compile_pdf=False, commit_sha="test-sha")
    manifest = _load(output / "submission_manifest.json")
    assert manifest["commit_sha"] == "test-sha"
    for entry in manifest["files"]:
        path = output / entry["path"]
        assert path.is_file()
        assert path.stat().st_size == entry["bytes"]
        assert _sha256(path) == entry["sha256"]
        assert " " not in entry["path"]


def test_archive_placeholder_is_never_represented_as_issued(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    build(ROOT, output, compile_pdf=False, commit_sha="test-sha")
    readme = (output / "submission_README.txt").read_text(encoding="utf-8")
    unresolved = _load(output / "unresolved_metadata.json")
    assert "not an issued DOI" in readme
    assert unresolved["archive_doi_issued"] is False
    assert unresolved["submission_ready"] is False
