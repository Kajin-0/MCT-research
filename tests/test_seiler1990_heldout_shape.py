from pathlib import Path

from tools.analyze_seiler1990_heldout_shape import analyze

DATA = Path("data/experimental/seiler1990_figure7_digitized.csv")


def test_fold_structure() -> None:
    rows, summary = analyze(DATA)
    assert len(rows) == 12
    assert summary["validation_unit"] == "specimen"


def test_heldout_improvement() -> None:
    _, summary = analyze(DATA)
    metrics = summary["pooled_heldout_metrics"]
    assert metrics["trained_seiler_family"]["rmse_mev"] < metrics["hansen_fixed_linear"]["rmse_mev"]
    assert metrics["trained_seiler_family"]["rmse_mev"] < metrics["trained_scaled_quadratic"]["rmse_mev"]
    assert metrics["trained_seiler_family"]["maximum_absolute_mev"] < 2.0
