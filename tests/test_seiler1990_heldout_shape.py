from pathlib import Path

from tools.analyze_seiler1990_heldout_shape import analyze

DATA = Path("data/experimental/seiler1990_figure7_digitized.csv")


def test_fold_structure() -> None:
    rows, summary = analyze(DATA)
    assert len(rows) == 12
    assert summary["validation_unit"] == "specimen"
