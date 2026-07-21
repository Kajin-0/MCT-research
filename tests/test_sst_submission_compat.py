from __future__ import annotations

from pathlib import Path

from tools.build_sst_submission_bundle_compat import build

ROOT = Path(__file__).resolve().parents[1]


def test_portable_preamble_and_bibliography(tmp_path: Path) -> None:
    output = tmp_path / "bundle"
    build(ROOT, output, compile_pdf=False, commit_sha="compat-test")

    named = (output / "manuscript_named.tex").read_text(encoding="utf-8")
    references = (output / "references.tex").read_text(encoding="utf-8")

    assert "\\pdfminorversion=7" in named
    assert "\\usepackage{lmodern}" in named
    assert "\\usepackage{mathptmx}" not in named
    assert "\\hbar" in named

    assert "Åström" in references
    assert "Flatté" in references
    assert "Möllmann" in references
    assert "\\textbackslash{}AA" not in references


def test_portable_entry_point_remains_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build(ROOT, first, compile_pdf=False, commit_sha="compat-test")
    build(ROOT, second, compile_pdf=False, commit_sha="compat-test")

    for relative in (
        "manuscript_named.tex",
        "manuscript_anonymous.tex",
        "references.tex",
        "references.bib",
        "sst_named_source.zip",
        "sst_anonymous_source.zip",
        "submission_manifest.json",
    ):
        assert (first / relative).read_bytes() == (second / relative).read_bytes()
