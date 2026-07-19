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


def test_irpt_table_bundle_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build(ROOT, first)
    build(ROOT, second)
    assert {path.name for path in first.iterdir()} == set(TABLE_FILENAMES)
    for name in TABLE_FILENAMES:
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_irpt_tables_preserve_frozen_record_counts(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    table1 = (tmp_path / TABLE_FILENAMES[0]).read_text(encoding="utf-8")
    table2 = (tmp_path / TABLE_FILENAMES[1]).read_text(encoding="utf-8")
    table3 = (tmp_path / TABLE_FILENAMES[2]).read_text(encoding="utf-8")
    table4 = (tmp_path / TABLE_FILENAMES[3]).read_text(encoding="utf-8")
    table5 = (tmp_path / TABLE_FILENAMES[4]).read_text(encoding="utf-8")

    assert _csv_count("table1_specimen_provenance.csv") == 2
    assert table1.count("Moazzami 2005, Fig.~6") == 2
    assert table1.count("density not reported") == 2

    assert _csv_count("table2_candidate_definitions.csv") == 4
    assert table2.count(" \\\") == 5  # one header plus four records

    assert _csv_count("table3_edge_ensemble.csv") == 28
    assert table3.count(" & fit & ") == 12
    assert table3.count(" & threshold & ") == 16
    assert table3.count(" & yes & ") == 3

    assert _csv_count("table4_material_model_comparison.csv") == 8
    assert table4.count(" & no \\\") == 8

    assert _csv_count("table5_claim_boundaries.csv") == 4
    assert "not authorized" in table5


def test_irpt_tables_use_width_constrained_layouts(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    table1 = (tmp_path / TABLE_FILENAMES[0]).read_text(encoding="utf-8")
    table3 = (tmp_path / TABLE_FILENAMES[2]).read_text(encoding="utf-8")
    table4 = (tmp_path / TABLE_FILENAMES[3]).read_text(encoding="utf-8")

    assert r"\begin{tabularx}{\textwidth}" in table1
    assert r"\begin{tabularx}{\textwidth}" in table4
    assert r"\footnotesize" in table3
    assert r"\setlength{\tabcolsep}{1.5pt}" in table3
    assert "Closest comparator" in table3
    assert "fixed thresh-" not in table3


def test_irpt_tables_preserve_claim_boundaries(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    edge_table = (tmp_path / "table3_edge_ensemble.tex").read_text(encoding="utf-8")
    model_table = (tmp_path / "table4_material_model_comparison.tex").read_text(
        encoding="utf-8"
    )
    claim_table = (tmp_path / "table5_claim_boundaries.tex").read_text(
        encoding="utf-8"
    )

    assert "Boundary-limited candidates" in edge_table
    assert "Strict material-law ranking is not authorized" in model_table
    assert "one corrected or production edge exists" in claim_table
    assert "not authorized" in claim_table
    assert "complete candidate ensemble must be reported" in claim_table


def test_irpt_table_labels_match_manuscript_inputs(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    expected_labels = {
        "table1_specimen_provenance.tex": r"\label{tab:specimen-provenance}",
        "table2_candidate_definitions.tex": r"\label{tab:candidate-definitions}",
        "table3_edge_ensemble.tex": r"\label{tab:edge-ensemble}",
        "table4_material_model_comparison.tex": r"\label{tab:model-comparison}",
        "table5_claim_boundaries.tex": r"\label{tab:claim-boundaries}",
    }
    for name, label in expected_labels.items():
        assert label in (tmp_path / name).read_text(encoding="utf-8")


def test_frozen_irpt_tables_match_a_fresh_rebuild(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    assert {path.name for path in FROZEN.iterdir()} == set(TABLE_FILENAMES)
    for name in TABLE_FILENAMES:
        assert (FROZEN / name).read_bytes() == (tmp_path / name).read_bytes()
