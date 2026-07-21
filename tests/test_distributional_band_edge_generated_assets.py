from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

from tools.build_distributional_band_edge_manuscript_assets import (
    FIGURE_FILES,
    TABLE_FILES,
    build,
)

ROOT = Path(__file__).resolve().parents[1]


def test_distributional_asset_builder_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    summary_first = build(ROOT, first)
    summary_second = build(ROOT, second)

    expected = sorted([*FIGURE_FILES, *TABLE_FILES])
    assert summary_first["generated_files"] == expected
    assert summary_second["generated_files"] == expected
    assert summary_first["figure_count"] == 7
    assert summary_first["table_count"] == 3
    assert summary_first["external_material_validation"] is False

    generated = [*expected, "distributional_band_edge_asset_summary.json"]
    for name in generated:
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_generated_svgs_are_parseable_and_preserve_claim_boundaries(
    tmp_path: Path,
) -> None:
    output = tmp_path / "generated"
    build(ROOT, output)

    ids: set[str] = set()
    for name in FIGURE_FILES:
        path = output / name
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")
        title = root.find("{http://www.w3.org/2000/svg}title")
        metadata = root.find("{http://www.w3.org/2000/svg}metadata")
        assert title is not None and title.text
        assert metadata is not None and metadata.text
        payload = json.loads(metadata.text)
        assert payload["claim_ids"]
        assert payload["generated_from_commit"]
        assert name not in ids
        ids.add(name)

    combined = "\n".join((output / name).read_text(encoding="utf-8") for name in FIGURE_FILES)
    assert "NOT MATERIAL VALIDATION" in combined
    assert "NOT A SPECIMEN FIT" in combined
    assert "cm^-1" in combined
    assert "meV" in combined
    assert "rank" in combined.lower()


def test_generated_tables_and_summary_match_contract(tmp_path: Path) -> None:
    output = tmp_path / "generated"
    build(ROOT, output)

    theorem = (output / TABLE_FILES[0]).read_text(encoding="utf-8")
    quantitative = (output / TABLE_FILES[1]).read_text(encoding="utf-8")
    provenance = (output / TABLE_FILES[2]).read_text(encoding="utf-8")
    assert "Theorem 3" in theorem
    assert "rank(J) <= 3" in theorem
    assert "147.323 meV" in quantitative
    assert "25.0803 K" in quantitative
    for index in range(1, 24):
        assert f"C{index:02d}" in provenance

    summary = json.loads(
        (output / "distributional_band_edge_asset_summary.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(summary["source_records"]) == 5
    assert summary["external_material_validation"] is False
    assert "specimen-level validation" in summary["claim_boundary"]


def test_regenerated_headline_labels_are_present(tmp_path: Path) -> None:
    output = tmp_path / "generated"
    build(ROOT, output)

    figure3 = (output / "figure3_herrmann_tail_nonuniqueness.svg").read_text(
        encoding="utf-8"
    )
    figure4 = (output / "figure4_chang_cutoff_rank.svg").read_text(
        encoding="utf-8"
    )
    figure5 = (output / "figure5_carrier_filling.svg").read_text(
        encoding="utf-8"
    )
    figure6 = (output / "figure6_unified_structural_rank.svg").read_text(
        encoding="utf-8"
    )
    assert "60.1%" in figure3
    assert "-16.636 meV" in figure4
    assert "147.323 meV" in figure5
    assert "max |difference|" in figure6
    assert "(Delta, -Delta, 0, -1, +1)" in figure6
