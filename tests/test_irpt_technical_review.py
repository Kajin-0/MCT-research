from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IRPT = ROOT / "manuscript/observation_model_uncertainty/irpt"
METHODS = (IRPT / "sections/02_methods.tex").read_text(encoding="utf-8")
RESULTS = (IRPT / "sections/03_results.tex").read_text(encoding="utf-8")
DISCUSSION = (IRPT / "sections/04_discussion.tex").read_text(encoding="utf-8")
LIMITATIONS = (IRPT / "sections/05_limitations.tex").read_text(encoding="utf-8")
CONCLUSIONS = (IRPT / "sections/06_conclusions.tex").read_text(encoding="utf-8")


def test_all_material_comparators_are_defined_explicitly() -> None:
    for label in ("eq:hansen", "eq:seiler", "eq:laurenti", "eq:provisional"):
        assert rf"\label{{{label}}}" in METHODS
    assert "signed zone-centre gap in electronvolts" in METHODS
    assert "original coefficient covariance and validity limits were not reconstructed" in METHODS


def test_observation_equation_preserves_residual_method_uncertainty() -> None:
    assert "calibrated magneto-optical gap estimate" in METHODS
    assert r"\epsilon=\epsilon_{\mathrm{abs}}-\epsilon_{\mathrm{MO}}" in METHODS
    assert "residual method and measurement uncertainty remains" in METHODS


def test_chu_units_and_source_domain_are_explicit() -> None:
    assert r"$\beta$ in eV$^{-1}$" in METHODS
    assert r"$T$ in kelvin" in METHODS
    assert r"0.170\leq x\leq0.443" in METHODS
    assert r"77\leq T\leq300" in METHODS


def test_design_temperature_and_factorial_scope_are_consistent() -> None:
    combined = "\n".join((METHODS, RESULTS, LIMITATIONS, CONCLUSIONS))
    assert "target 6~K" in combined
    assert "300~K" in combined
    assert "complete factorial" in combined or "complete-factorial" in combined
    assert "not a universal optimal-design proof" in METHODS


def test_absorption_observation_terminology_does_not_claim_intrinsic_state() -> None:
    combined = "\n".join((METHODS, RESULTS, DISCUSSION, CONCLUSIONS))
    assert "intrinsic-absorption" not in combined
    assert "absorption-derived" in combined
