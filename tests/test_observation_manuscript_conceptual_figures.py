from __future__ import annotations

import json
from pathlib import Path

from tools.build_observation_model_conceptual_figures import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "manuscript/observation_model_uncertainty"
FIGURE_NAMES = {
    "figure4_identifiability.svg",
    "figure5_paired_acquisition_design.svg",
}


def test_conceptual_figure_bundle_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build(first)
    build(second)
    assert {path.name for path in first.iterdir()} == {
        *FIGURE_NAMES,
        "conceptual_figure_summary.json",
    }
    for name in FIGURE_NAMES | {"conceptual_figure_summary.json"}:
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_identifiability_figure_preserves_the_observation_equation(tmp_path: Path) -> None:
    build(tmp_path)
    text = (tmp_path / "figure4_identifiability.svg").read_text(encoding="utf-8")
    assert "yMO = Eg(x,T)" in text
    assert "yabs = Eg +" in text
    assert "Delta" not in text
    assert "same specimen" in text
    assert "universal correction" in text


def test_acquisition_figure_reads_the_validated_design_oracle(tmp_path: Path) -> None:
    build(tmp_path)
    text = (tmp_path / "figure5_paired_acquisition_design.svg").read_text(
        encoding="utf-8"
    )
    assert "rank  5/5" in text
    assert "observations/block  16" in text
    assert "residual DOF  11" in text
    assert "condition number  2.618" in text
    assert "max leverage  0.4375" in text
    for specimen in range(1, 9):
        assert text.count(f">S{specimen}<") == 2


def test_conceptual_summary_preserves_claim_boundaries(tmp_path: Path) -> None:
    summary = build(tmp_path)
    assert summary["new_empirical_model_introduced"] is False
    assert summary["universal_correction_authorized"] is False
    persisted = json.loads(
        (tmp_path / "conceptual_figure_summary.json").read_text(encoding="utf-8")
    )
    assert persisted == summary
