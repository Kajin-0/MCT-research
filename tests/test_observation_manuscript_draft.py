from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuscript/observation_model_uncertainty"
DRAFT = MANUSCRIPT_DIR / "manuscript_draft.md"


def _rows(name: str) -> list[dict[str, str]]:
    with (MANUSCRIPT_DIR / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_manuscript_has_complete_submission_structure() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    for heading in (
        "## Abstract",
        "## 1. Introduction",
        "## 2. Observation model and methods",
        "## 3. Results",
        "## 4. Discussion",
        "## 5. Limitations",
        "## 6. Conclusions",
        "## Data and code availability",
        "## Figure captions",
        "## Table captions",
        "## References requiring final bibliography formatting",
    ):
        assert heading in text
    for figure in range(1, 6):
        assert f"**Figure {figure}.**" in text
    for table in range(1, 6):
        assert f"**Table {table}.**" in text


def test_manuscript_numbers_are_tied_to_frozen_tables() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    edges: dict[str, list[float]] = defaultdict(list)
    fitted_coordinate_shifts: list[float] = []
    for row in _rows("table3_edge_ensemble.csv"):
        if row["observation_class"] == "fitted_absorption_model":
            edges[row["specimen_id"]].append(float(row["edge_mev"]))
            fitted_coordinate_shifts.append(
                float(row["digitization_coordinate_shift_mev"])
            )
    spans = sorted(max(values) - min(values) for values in edges.values())
    assert f"{spans[0]:.3f}" in text
    assert f"{spans[1]:.3f}" in text
    assert f"{max(fitted_coordinate_shifts):.3f}" in text

    predictions: dict[str, dict[str, float]] = defaultdict(dict)
    for row in _rows("table4_material_model_comparison.csv"):
        predictions[row["specimen_id"]][row["model_id"]] = float(
            row["prediction_mev"]
        )
    separations = sorted(
        abs(values["hansen"] - values["published_seiler"])
        for values in predictions.values()
    )
    assert f"{separations[0]:.3f}" in text
    assert f"{separations[1]:.3f}" in text


def test_manuscript_preserves_claim_boundaries() -> None:
    text = DRAFT.read_text(encoding="utf-8").lower()
    required = (
        "no single fitted edge is selected.",
        "does not establish a preferred universal hgcdte gap equation",
        "do not support a universal absorption correction",
        "no candidate is promoted as the corrected or production edge",
        "not a universal optimal-design proof",
        "specimen-level composition uncertainty is unreported",
    )
    for statement in required:
        assert statement in text
    assert "universal replacement for hansen is demonstrated" not in text
    assert "production-ready edge" not in text


def test_unverified_bibliography_is_explicitly_marked() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    assert "Verify complete primary citation" in text
    assert "Complete primary metadata" in text
    assert "only after exact source verification" in text
