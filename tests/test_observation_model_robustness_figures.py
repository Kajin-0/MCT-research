from pathlib import Path

from tools.build_observation_model_robustness_figures import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "manuscript/observation_model_uncertainty"
REFERENCE = ROOT / "data/validation/moazzami2005_model_robustness_reference.json"
FIGURE_NAMES = {
    "figure6_relative_fitted_intercepts.svg",
    "figure7_robustness_scales.svg",
    "figure8_model_residual_compatibility.svg",
}


def test_robustness_figures_are_deterministic_and_frozen(tmp_path: Path) -> None:
    result = build(REFERENCE, tmp_path)
    assert set(result) == FIGURE_NAMES
    for name in sorted(FIGURE_NAMES):
        generated = tmp_path / name
        text = generated.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "<title>" in text
        assert generated.read_bytes() == (FROZEN / name).read_bytes()


def test_robustness_figures_do_not_restore_superseded_feature_marker(
    tmp_path: Path,
) -> None:
    build(REFERENCE, tmp_path)
    for name in FIGURE_NAMES:
        text = (tmp_path / name).read_text(encoding="utf-8").lower()
        assert "reversal core" not in text
        assert "equation ranking" not in text
