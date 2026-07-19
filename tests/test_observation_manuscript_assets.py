from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.build_observation_model_manuscript_assets import build

ROOT = Path(__file__).resolve().parents[1]


def _row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as stream:
        return sum(1 for _ in csv.DictReader(stream))


def test_manuscript_asset_bundle_is_complete(tmp_path: Path) -> None:
    summary = build(ROOT, tmp_path)
    expected = {
        "figure1_spectrum_models.svg",
        "figure2_edge_candidates.svg",
        "figure3_material_residual_envelopes.svg",
        "manuscript_asset_summary.json",
        "table1_specimen_provenance.csv",
        "table2_candidate_definitions.csv",
        "table3_edge_ensemble.csv",
        "table4_material_model_comparison.csv",
        "table5_claim_boundaries.csv",
    }
    assert {path.name for path in tmp_path.iterdir()} == expected
    assert summary["decision"]["published_seiler_comparator_included"] is True
    assert summary["decision"]["strict_material_model_ranking_authorized"] is False


def test_manuscript_tables_preserve_expected_record_counts(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    assert _row_count(tmp_path / "table1_specimen_provenance.csv") == 2
    assert _row_count(tmp_path / "table2_candidate_definitions.csv") == 4
    assert _row_count(tmp_path / "table3_edge_ensemble.csv") == 28
    assert _row_count(tmp_path / "table4_material_model_comparison.csv") == 8
    assert _row_count(tmp_path / "table5_claim_boundaries.csv") == 4


def test_svg_and_summary_outputs_are_machine_readable(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    for name in (
        "figure1_spectrum_models.svg",
        "figure2_edge_candidates.svg",
        "figure3_material_residual_envelopes.svg",
    ):
        text = (tmp_path / name).read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "<title>" in text
        assert "not selected" in text or "observation" in text.lower()
    summary = json.loads(
        (tmp_path / "manuscript_asset_summary.json").read_text(encoding="utf-8")
    )
    assert summary["digitization_decision"][
        "all_model_candidate_shifts_below_1mev"
    ] is True
