from __future__ import annotations

import csv
from pathlib import Path

from tools.build_observation_model_irpt_submission_tables import TABLE_FILENAMES, build

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript/observation_model_uncertainty"
FROZEN = SOURCE / "irpt/tables"


def _csv_count(name: str) -> int:
    with (SOURCE / name).open(newline="", encoding="utf-8") as stream:
        return sum(1 for _ in csv.DictReader(stream))


def _built(tmp_path: Path) -> dict[str, str]:
    build(ROOT, tmp_path)
    return {
        name: (tmp_path / name).read_text(encoding="utf-8")
        for name in TABLE_FILENAMES
    }


def test_irpt_table_bundle_is_deterministic(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    build(ROOT, first)
    build(ROOT, second)
    assert {path.name for path in first.iterdir()} == set(TABLE_FILENAMES)
    for name in TABLE_FILENAMES:
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_irpt_tables_preserve_records_and_layout(tmp_path: Path) -> None:
    tables = _built(tmp_path)
    t1, t2, t3, t4, t5 = (tables[name] for name in TABLE_FILENAMES)

    assert _csv_count("table1_specimen_provenance.csv") == 2
    assert t1.count("Moazzami 2005, Fig.~6") == 2
    assert t1.count("density not reported") == 2
    assert t1.count(r"\textemdash{}") == 2
    assert r"\begin{tabularx}{\textwidth}" in t1

    assert _csv_count("table2_candidate_definitions.csv") == 4
    assert t2.count("fractional power") == 2
    assert "Chu 1994 Kane region" in t2
    assert "First interpolated" in t2

    assert _csv_count("table3_edge_ensemble.csv") == 28
    assert t3.count(" & fit & ") == 12
    assert t3.count(" & threshold & ") == 16
    assert t3.count(" & yes & ") == 3
    assert r"\begin{landscape}" in t3
    assert r"\scriptsize" in t3
    assert r"\renewcommand{\arraystretch}{0.95}" in t3
    assert r"\setlength{\tabcolsep}{3pt}" in t3
    assert "Closest comparator" in t3
    assert "fixed thresh-" not in t3

    assert _csv_count("table4_material_model_comparison.csv") == 8
    assert t4.count(" & no ") == 8
    assert r"\begin{tabularx}{\textwidth}" in t4

    assert _csv_count("table5_claim_boundaries.csv") == 4
    assert "not authorized" in t5


def test_irpt_tables_preserve_claim_boundaries_and_labels(tmp_path: Path) -> None:
    tables = _built(tmp_path)
    assert "Boundary-limited candidates" in tables[TABLE_FILENAMES[2]]
    assert "Strict material-law ranking is not authorized" in tables[TABLE_FILENAMES[3]]
    assert "one corrected or production edge exists" in tables[TABLE_FILENAMES[4]]
    assert "complete candidate ensemble must be reported" in tables[TABLE_FILENAMES[4]]

    labels = (
        r"\label{tab:specimen-provenance}",
        r"\label{tab:candidate-definitions}",
        r"\label{tab:edge-ensemble}",
        r"\label{tab:model-comparison}",
        r"\label{tab:claim-boundaries}",
    )
    for name, label in zip(TABLE_FILENAMES, labels, strict=True):
        assert label in tables[name]


def test_frozen_irpt_tables_match_a_fresh_rebuild(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    assert {path.name for path in FROZEN.iterdir()} == set(TABLE_FILENAMES)
    for name in TABLE_FILENAMES:
        assert (FROZEN / name).read_bytes() == (tmp_path / name).read_bytes()
