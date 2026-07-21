from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import zipfile

import pytest

BUNDLE_ENV = "SST_BUNDLE_DIR"
FORBIDDEN = ("Terence Fisher", "Brooks Photonics", "Florida, USA", "Kajin-0")


def _bundle() -> Path:
    value = os.environ.get(BUNDLE_ENV)
    if not value:
        pytest.skip(f"{BUNDLE_ENV} is not set")
    path = Path(value).resolve()
    if not path.is_dir():
        pytest.fail(f"compiled bundle directory does not exist: {path}")
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pdf_text(path: Path) -> str:
    completed = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        pytest.fail(f"pdftotext failed for {path}: {completed.stderr}")
    return completed.stdout


def _page_count(path: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        pytest.fail(f"pdfinfo failed for {path}: {completed.stderr}")
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, flags=re.MULTILINE)
    if not match:
        pytest.fail(f"page count not found in pdfinfo output for {path}")
    return int(match.group(1))


def test_named_and_anonymous_review_pdfs_compile() -> None:
    bundle = _bundle()
    named = bundle / "manuscript_named.pdf"
    anonymous = bundle / "manuscript_anonymous.pdf"
    assert named.stat().st_size > 100_000
    assert anonymous.stat().st_size > 100_000
    named_pages = _page_count(named)
    anonymous_pages = _page_count(anonymous)
    assert named_pages >= 15
    assert anonymous_pages >= 15
    assert abs(named_pages - anonymous_pages) <= 2


def test_compiled_pdf_identity_boundary() -> None:
    bundle = _bundle()
    named_text = _pdf_text(bundle / "manuscript_named.pdf")
    anonymous_text = _pdf_text(bundle / "manuscript_anonymous.pdf")
    assert "Terence Fisher" in named_text
    assert "Brooks Photonics" in named_text
    for token in FORBIDDEN:
        assert token not in anonymous_text
    assert "From latent bandgap to measured edge in HgCdTe" in anonymous_text
    assert "Data availability" in anonymous_text


def test_compiled_bundle_has_seven_vector_figures() -> None:
    bundle = _bundle()
    figures = sorted((bundle / "figures").glob("figure*.pdf"))
    assert len(figures) == 7
    for figure in figures:
        assert figure.stat().st_size > 2_000
        assert _page_count(figure) == 1


def test_source_archives_are_complete_and_separated() -> None:
    bundle = _bundle()
    named_zip = bundle / "sst_named_source.zip"
    anonymous_zip = bundle / "sst_anonymous_source.zip"
    with zipfile.ZipFile(named_zip) as archive:
        named_members = set(archive.namelist())
    with zipfile.ZipFile(anonymous_zip) as archive:
        anonymous_members = set(archive.namelist())
        for member in anonymous_members:
            if member.endswith((".tex", ".txt", ".bib")):
                text = archive.read(member).decode("utf-8", errors="replace")
                for token in FORBIDDEN:
                    assert token not in text

    expected_figures = {f"figures/figure{index}.pdf" for index in range(1, 8)}
    actual_named_figures = {
        member for member in named_members if member.startswith("figures/") and member.endswith(".pdf")
    }
    actual_anonymous_figures = {
        member for member in anonymous_members if member.startswith("figures/") and member.endswith(".pdf")
    }
    assert len(actual_named_figures) == 7
    assert actual_named_figures == actual_anonymous_figures
    assert "manuscript_named.tex" in named_members
    assert "manuscript_named.pdf" in named_members
    assert "manuscript_anonymous.tex" in anonymous_members
    assert "manuscript_anonymous.pdf" in anonymous_members
    assert "manuscript_named.tex" not in anonymous_members
    assert "manuscript_named.pdf" not in anonymous_members
    assert not expected_figures & named_members  # descriptive names are intentionally retained


def test_compiled_manifest_hashes_and_counts() -> None:
    bundle = _bundle()
    with (bundle / "submission_manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    assert manifest["compiled"] is True
    assert manifest["figure_count"] == 7
    assert manifest["table_count"] == 3
    assert manifest["verified_reference_count"] == 15
    assert manifest["cited_reference_count"] == 15
    assert manifest["archive_doi_issued"] is False
    paths = {entry["path"] for entry in manifest["files"]}
    assert "manuscript_named.pdf" in paths
    assert "manuscript_anonymous.pdf" in paths
    assert "sst_named_source.zip" in paths
    assert "sst_anonymous_source.zip" in paths
    for entry in manifest["files"]:
        path = bundle / entry["path"]
        assert path.is_file()
        assert path.stat().st_size == entry["bytes"]
        assert _sha256(path) == entry["sha256"]


def test_latex_logs_have_no_fatal_or_missing_reference_warnings() -> None:
    bundle = _bundle()
    for stem in ("manuscript_named", "manuscript_anonymous"):
        log = (bundle / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
        assert "Fatal error" not in log
        assert "Emergency stop" not in log
        assert "Undefined control sequence" not in log
        assert "There were undefined references" not in log
        assert "Citation" not in log or "undefined" not in log.lower()
