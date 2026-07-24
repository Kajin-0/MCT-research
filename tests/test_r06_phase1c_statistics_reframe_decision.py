import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = ROOT / "configs" / "transport_noise" / "statistics_reframe_decision.json"


def load_decision() -> dict:
    return json.loads(DECISION_PATH.read_text(encoding="utf-8"))


def test_decision_is_explicit_reframe_with_material_prediction_block():
    decision = load_decision()
    assert decision["decision"] == "reframe"
    assert decision["phase_1_direction"] == (
        "proceed_with_reframed_architecture_and_material_prediction_block"
    )


def test_primary_source_identities_and_dois_are_pinned():
    sources = load_decision()["source_status"]
    assert sources["madarasz_szmulowicz_mcbath_1985"]["doi"] == "10.1063/1.335685"
    assert sources["madarasz_szmulowicz_1985"]["doi"] == "10.1063/1.335868"
    assert sources["seiler_lowney_littler_yoon_1991"]["doi"] == "10.1557/PROC-216-59"
    assert sources["lowney_seiler_littler_yoon_1992"]["doi"] == "10.1063/1.351371"
    assert sources["hansen_schmit_1983"]["doi"] == "10.1063/1.332153"


def test_historic_implementations_remain_unauthorized():
    sources = load_decision()["source_status"]
    for key in (
        "madarasz_szmulowicz_mcbath_1985",
        "madarasz_szmulowicz_1985",
        "seiler_lowney_littler_yoon_1991",
        "lowney_seiler_littler_yoon_1992",
    ):
        assert sources[key]["implementation_authorized"] is False


def test_authorized_scope_contains_interface_but_not_material_prediction():
    decision = load_decision()
    authorized = set(decision["authorized_now"])
    prohibited = set(decision["not_authorized"])
    assert "model-agnostic carrier density and compressibility interface" in authorized
    assert "thermodynamic generalized-Einstein identity checks" in authorized
    assert "material-accurate HgCdTe density or susceptibility prediction" in prohibited
    assert "production detector coupling to an unvalidated statistics closure" in prohibited


def test_both_future_closure_paths_have_validation_requirements():
    paths = {entry["path"]: entry["requirements"] for entry in load_decision()["future_closure_paths"]}
    assert set(paths) == {"source_exact_recovery", "project_defined_kane_closure"}
    assert "three primary numerical reference points" in paths["source_exact_recovery"]
    assert "three independent numerical validation points" in paths["project_defined_kane_closure"]
    assert "explicit distinction from historic implementations" in paths["project_defined_kane_closure"]
