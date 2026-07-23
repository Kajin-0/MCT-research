from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_PATH = ROOT / "manuscript" / "r04" / "manuscript_architecture.md"
CLAIM_LEDGER_PATH = ROOT / "manuscript" / "r04" / "claim_ledger.json"
FIGURE_PLAN_PATH = ROOT / "manuscript" / "r04" / "figure_plan.json"
ABSTRACT_PLAN_PATH = ROOT / "manuscript" / "r04" / "abstract_plan.json"
DECISION_PATH = (
    ROOT
    / "research"
    / "decision_records"
    / "2026-07-23-r04-manuscript-architecture.md"
)
AUTHORIZATION_PATH = ROOT / "data" / "validation" / "r04_manuscript_authorization_review.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_architecture_deliverables_exist() -> None:
    for path in (
        ARCHITECTURE_PATH,
        CLAIM_LEDGER_PATH,
        FIGURE_PLAN_PATH,
        ABSTRACT_PLAN_PATH,
        DECISION_PATH,
        AUTHORIZATION_PATH,
    ):
        assert path.is_file(), path


def test_architecture_decision_and_authorization_are_consistent() -> None:
    architecture = ARCHITECTURE_PATH.read_text(encoding="utf-8")
    decision = DECISION_PATH.read_text(encoding="utf-8")
    authorization = load(AUTHORIZATION_PATH)

    assert authorization["decision"] == "AUTHORIZE_RESTRICTED_MANUSCRIPT"
    assert authorization["authorization"]["restricted_manuscript_drafting"] is True
    assert authorization["authorization"]["submission"] is False
    assert "ARCHITECTURE_READY_FOR_DRAFTING" in architecture
    assert "ARCHITECTURE_READY_FOR_DRAFTING" in decision
    assert "submission                                       not authorized" in decision
    assert "final pre-submission claim audit                 required" in decision


def test_claim_ledger_has_required_schema_and_classes() -> None:
    ledger = load(CLAIM_LEDGER_PATH)
    claims = ledger["claims"]

    assert ledger["program"] == "R04"
    assert ledger["issue"] == 330
    assert ledger["final_claim_audit_required_before_submission"] is True
    assert len(claims) == 15
    assert len({claim["claim_id"] for claim in claims}) == len(claims)

    required_fields = {
        "claim_id",
        "claim_text",
        "claim_class",
        "supporting_theorem_result_source",
        "main_text_location",
        "figure_table_support",
        "scope_conditions",
        "unsupported_stronger_version",
        "required_citation_class",
        "final_claim_audit_status",
    }
    required_classes = {
        "established_mathematics",
        "established_prior_art",
        "candidate_integrated_R04_contribution",
        "synthetic_design_consequence",
        "restricted_cross_material_demonstration",
        "explicit_limitation",
    }

    for claim in claims:
        assert set(claim) == required_fields
        assert claim["supporting_theorem_result_source"]
        assert claim["scope_conditions"]
        assert claim["unsupported_stronger_version"]
        assert claim["final_claim_audit_status"] == "required"

    assert required_classes <= {claim["claim_class"] for claim in claims}


def test_claim_ledger_preserves_prior_art_and_blocked_inferences() -> None:
    claims = {claim["claim_id"]: claim for claim in load(CLAIM_LEDGER_PATH)["claims"]}

    assert claims["R04-C01"]["claim_class"] == "established_prior_art"
    assert "predate R04" in claims["R04-C01"]["claim_text"]
    assert "R04 invented" in claims["R04-C01"]["unsupported_stronger_version"]

    assert claims["R04-C12"]["claim_class"] == "restricted_cross_material_demonstration"
    assert "CdSeTe" in claims["R04-C12"]["claim_text"]
    assert "validates HgCdTe" in claims["R04-C12"]["unsupported_stronger_version"]

    assert claims["R04-C14"]["claim_class"] == "explicit_limitation"
    assert "public source-native HgCdTe" in claims["R04-C14"]["claim_text"]
    assert "No suitable HgCdTe data exist anywhere" in claims["R04-C14"][
        "unsupported_stronger_version"
    ]

    assert claims["R04-C15"]["claim_class"] == "explicit_limitation"
    assert "no specimen-specific HgCdTe" in claims["R04-C15"]["claim_text"]


def test_figure_plan_has_exactly_four_main_figures_and_no_new_science() -> None:
    plan = load(FIGURE_PLAN_PATH)
    figures = plan["figures"]

    assert plan["main_figure_ceiling"] == 4
    assert plan["new_scientific_calculations_authorized"] is False
    assert len(figures) == 4
    assert [figure["figure"] for figure in figures] == [1, 2, 3, 4]
    assert len(figures[0]["panels"]) == 3
    assert len(figures[1]["panels"]) == 4
    assert len(figures[2]["panels"]) == 4
    assert len(figures[3]["panels"]) == 4

    required_panel_fields = {
        "panel",
        "short_title",
        "source_module_or_result",
        "plotted_variables_and_units",
        "evidence_type",
        "caption_level_claim",
        "prohibited_interpretation",
        "new_scientific_calculation_required",
        "rendering_action",
    }
    panel_ids: list[str] = []
    for figure in figures:
        for panel in figure["panels"]:
            assert set(panel) == required_panel_fields
            assert panel["new_scientific_calculation_required"] is False
            assert panel["source_module_or_result"]
            assert panel["prohibited_interpretation"]
            panel_ids.append(panel["panel"])
    assert len(panel_ids) == len(set(panel_ids))


def test_real_data_figure_is_explicitly_restricted() -> None:
    figure4 = load(FIGURE_PLAN_PATH)["figures"][3]
    assert figure4["figure"] == 4
    text = " ".join(json.dumps(figure4).split())

    assert "CdSeTe" in text
    assert "PL peak wavelength" in text
    assert "11.24 percent" in text
    assert "not independent family validation" in text
    assert "not the CdSeTe or HgCdTe material covariance law" in text
    assert "unknown native sample-plane kernel" in text


def test_abstract_plan_has_exactly_six_functions_and_mandatory_limits() -> None:
    plan = load(ABSTRACT_PLAN_PATH)
    function_keys = [
        "problem",
        "method",
        "analytical_result",
        "real_map_demonstration",
        "limitation",
        "practical_consequence",
    ]

    assert [key for key in plan if key in function_keys] == function_keys
    assert len([key for key in plan if key in function_keys]) == 6
    for key in function_keys:
        assert set(plan[key]) == {"function", "required_terms", "prohibited_terms"}
        assert plan[key]["function"]
        assert plan[key]["required_terms"]
        assert plan[key]["prohibited_terms"]

    real_map = " ".join(plan["real_map_demonstration"]["required_terms"])
    limitation = " ".join(plan["limitation"]["required_terms"])
    assert "cross-material method demonstration" in real_map
    assert "numerical scales from one raster are dependent" in real_map
    assert "HgCdTe external validation remains blocked" in limitation
    assert "no physical correlation length is reported" in limitation
    assert "no covariance-family identification" in limitation


def test_architecture_contains_all_required_sections_and_drafting_order() -> None:
    text = ARCHITECTURE_PATH.read_text(encoding="utf-8")

    required_headings = [
        "## Abstract",
        "## 1. Introduction and prior-art boundary",
        "## 2. Measurement model and kernel-filtered covariance",
        "## 3. Recoverability and absolute scale calibration",
        "## 4. Three-scale family closure and misspecification",
        "## 5. Finite-map information and same-raster covariance",
        "## 6. Restricted CdSeTe real-map demonstration",
        "## 7. Measurement-design consequences",
        "## 8. Limitations",
        "## 9. Discussion and conclusion",
        "## Appendices and supplementary placement",
        "## Citation-role map",
        "## Drafting order",
    ]
    for heading in required_headings:
        assert heading in text

    assert text.index("measurement model") < text.index("introduction", text.index("## Drafting order"))
    assert "abstract last" in text
    assert "No fifth main figure is authorized" in text
    assert "full section drafting under the architecture    authorized" in DECISION_PATH.read_text(
        encoding="utf-8"
    )


def test_canonical_json_formatting() -> None:
    for path in (CLAIM_LEDGER_PATH, FIGURE_PLAN_PATH, ABSTRACT_PLAN_PATH):
        raw = path.read_text(encoding="utf-8")
        assert raw == json.dumps(json.loads(raw), indent=2) + "\n"
