from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from tools.build_distributional_band_edge_manuscript_assets import (
    FIGURE_FILES,
    TABLE_FILES,
    build,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def generated_assets(tmp_path_factory: pytest.TempPathFactory) -> Path:
    output = tmp_path_factory.mktemp("distributional-assets")
    build(ROOT, output)
    return output


def test_distributional_asset_builder_is_deterministic(
    generated_assets: Path,
    tmp_path: Path,
) -> None:
    second = tmp_path / "second"
    summary_first = json.loads(
        (
            generated_assets / "distributional_band_edge_asset_summary.json"
        ).read_text(encoding="utf-8")
    )
    summary_second = build(ROOT, second)

    expected = sorted([*FIGURE_FILES, *TABLE_FILES])
    assert summary_first["generated_files"] == expected
    assert summary_second["generated_files"] == expected
    assert summary_first["figure_count"] == 7
    assert summary_first["table_count"] == 3
    assert summary_first["external_material_validation"] is False

    generated = [*expected, "distributional_band_edge_asset_summary.json"]
    for name in generated:
        assert (generated_assets / name).read_bytes() == (second / name).read_bytes()


def test_generated_svgs_are_parseable_and_preserve_claim_boundaries(
    generated_assets: Path,
) -> None:
    ids: set[str] = set()
    for name in FIGURE_FILES:
        path = generated_assets / name
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

    combined = "\n".join(
        (generated_assets / name).read_text(encoding="utf-8")
        for name in FIGURE_FILES
    )
    assert "NOT MATERIAL VALIDATION" in combined
    assert "NOT A SPECIMEN FIT" in combined
    assert "cm^-1" in combined
    assert "meV" in combined
    assert "rank" in combined.lower()


def test_generated_tables_and_summary_match_contract(
    generated_assets: Path,
) -> None:
    theorem = (generated_assets / TABLE_FILES[0]).read_text(encoding="utf-8")
    quantitative = (generated_assets / TABLE_FILES[1]).read_text(encoding="utf-8")
    provenance = (generated_assets / TABLE_FILES[2]).read_text(encoding="utf-8")
    assert "Theorem 3" in theorem
    assert "rank(J) <= 3" in theorem
    assert "147.323 meV" in quantitative
    assert "25.0803 K" in quantitative
    for index in range(1, 24):
        assert f"C{index:02d}" in provenance

    summary = json.loads(
        (
            generated_assets / "distributional_band_edge_asset_summary.json"
        ).read_text(encoding="utf-8")
    )
    assert len(summary["source_records"]) == 5
    assert summary["external_material_validation"] is False
    assert "specimen-level validation" in summary["claim_boundary"]


def test_regenerated_headline_labels_are_present(
    generated_assets: Path,
) -> None:
    figure3 = (
        generated_assets / "figure3_herrmann_tail_nonuniqueness.svg"
    ).read_text(encoding="utf-8")
    figure4 = (
        generated_assets / "figure4_chang_cutoff_rank.svg"
    ).read_text(encoding="utf-8")
    figure5 = (
        generated_assets / "figure5_carrier_filling.svg"
    ).read_text(encoding="utf-8")
    figure6 = (
        generated_assets / "figure6_unified_structural_rank.svg"
    ).read_text(encoding="utf-8")
    assert "60.1%" in figure3
    assert "-16.636 meV" in figure4
    assert "147.323 meV" in figure5
    assert "max |difference|" in figure6
    assert "(Delta, -Delta, 0, -1, +1)" in figure6
