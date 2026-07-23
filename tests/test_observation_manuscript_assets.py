from __future__ import annotations

import csv
from hashlib import sha256
import json
from pathlib import Path

from tools.build_observation_model_manuscript_assets import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "manuscript/observation_model_uncertainty"
ASSET_NAMES = {
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
FROZEN_ASSET_NAMES = ASSET_NAMES | {
    "figure4_identifiability.svg",
    "figure5_paired_acquisition_design.svg",
    "figure6_relative_fitted_intercepts.svg",
    "figure7_robustness_scales.svg",
    "figure8_model_residual_compatibility.svg",
    "conceptual_figure_summary.json",
}


def _row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as stream:
        return sum(1 for _ in csv.DictReader(stream))


def test_manuscript_asset_bundle_is_complete(tmp_path: Path) -> None:
    summary = build(ROOT, tmp_path)
    assert {path.name for path in tmp_path.iterdir()} == ASSET_NAMES
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


def test_frozen_manuscript_assets_match_a_fresh_rebuild(tmp_path: Path) -> None:
    build(ROOT, tmp_path)
    for name in sorted(ASSET_NAMES):
        assert (FROZEN / name).read_bytes() == (tmp_path / name).read_bytes()


def test_frozen_asset_hash_manifest_matches_committed_bytes() -> None:
    manifest: dict[str, str] = {}
    for line in (FROZEN / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    assert set(manifest) == FROZEN_ASSET_NAMES
    for name, expected in manifest.items():
        assert sha256((FROZEN / name).read_bytes()).hexdigest() == expected
