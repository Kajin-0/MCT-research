from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "manuscript" / "r04" / "manuscript_architecture.md"
CLAIMS = ROOT / "manuscript" / "r04" / "claim_ledger.json"
FIGURES = ROOT / "manuscript" / "r04" / "figure_plan.json"
ABSTRACT = ROOT / "manuscript" / "r04" / "abstract_plan.json"
DECISION = (
    ROOT
    / "research"
    / "decision_records"
    / "2026-07-23-r04-manuscript-architecture.md"
)
AUTHORIZATION = ROOT / "data" / "validation" / "r04_manuscript_authorization_review.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_deliverables_and_controlling_decisions() -> None:
    for path in (ARCHITECTURE, CLAIMS, FIGURES, ABSTRACT, DECISION, AUTHORIZATION):
        assert path.is_file(), path

    authorization = load(AUTHORIZATION)
    assert authorization["decision"] == "AUTHORIZE_RESTRICTED_MANUSCRIPT"
    assert authorization["authorization"]["restricted_manuscript_drafting"] is True
    assert authorization["authorization"]["submission"] is False
    assert "ARCHITECTURE_READY_FOR_DRAFTING" in compact(ARCHITECTURE)
    assert "ARCHITECTURE_READY_FOR_DRAFTING" in compact(DECISION)
    assert "submission not authorized" in compact(DECISION)


def test_claim_ledger_schema_classes_and_boundaries() -> None:
    ledger = load(CLAIMS)
    claims = ledger["claims"]
    required_classes = {
        "established_mathematics",
        "established_prior_art",
        "candidate_integrated_R04_contribution",
        "synthetic_design_consequence",
        "restricted_cross_material_demonstration",
        "explicit_limitation",
    }
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

    assert ledger["issue"] == 330
    assert ledger["final_claim_audit_required_before_submission"] is True
    assert len(claims) == 15
    assert len({claim["claim_id"] for claim in claims}) == 15
    assert required_classes <= {claim["claim_class"] for claim in claims}

    for claim in claims:
        assert set(claim) == required_fields
        assert claim["supporting_theorem_result_source"]
        assert claim["scope_conditions"]
        assert claim["unsupported_stronger_version"]
        assert claim["final_claim_audit_status"] == "required"

    indexed = {claim["claim_id"]: claim for claim in claims}
    assert indexed["R04-C01"]["claim_class"] == "established_prior_art"
    assert "R04 invented" in indexed["R04-C01"]["unsupported_stronger_version"]
    assert indexed["R04-C12"]["claim_class"] == "restricted_cross_material_demonstration"
    assert "validates HgCdTe" in indexed["R04-C12"]["unsupported_stronger_version"]
    assert indexed["R04-C14"]["claim_class"] == "explicit_limitation"
    assert "No suitable HgCdTe data exist anywhere" in indexed["R04-C14"][
        "unsupported_stronger_version"
    ]


def test_four_figure_ceiling_and_panel_contracts() -> None:
    plan = load(FIGURES)
    figures = plan["figures"]
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

    assert plan["main_figure_ceiling"] == 4
    assert plan["new_scientific_calculations_authorized"] is False
    assert [figure["figure"] for figure in figures] == [1, 2, 3, 4]
    assert [len(figure["panels"]) for figure in figures] == [3, 4, 4, 4]

    panel_ids: list[str] = []
    for figure in figures:
        for panel in figure["panels"]:
            assert set(panel) == required_panel_fields
            assert panel["source_module_or_result"]
            assert panel["prohibited_interpretation"]
            assert panel["new_scientific_calculation_required"] is False
            panel_ids.append(panel["panel"])
    assert len(panel_ids) == len(set(panel_ids))

    real_map_text = json.dumps(figures[3], ensure_ascii=False)
    assert "CdSeTe" in real_map_text
    assert "11.24 percent" in real_map_text
    assert "not independent family validation" in real_map_text
    assert "material covariance law" in real_map_text
    assert "native sample-plane kernel" in real_map_text


def test_abstract_has_exactly_six_functions_and_explicit_limits() -> None:
    plan = load(ABSTRACT)
    function_keys = [
        "problem",
        "method",
        "analytical_result",
        "real_map_demonstration",
        "limitation",
        "practical_consequence",
    ]

    assert [key for key in plan if key in function_keys] == function_keys
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


def test_architecture_sections_scope_and_drafting_order() -> None:
    text = ARCHITECTURE.read_text(encoding="utf-8")
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

    drafting = text[text.index("## Drafting order") :]
    assert drafting.index("measurement model") < drafting.index("introduction")
    assert "abstract last" in drafting
    assert "main figures" in text
    assert "4" in text[text.index("## Main-text ceiling") : text.index("---", text.index("## Main-text ceiling"))]
    assert "full section drafting under the architecture authorized" in compact(DECISION)


def test_json_files_are_canonical_utf8() -> None:
    for path in (CLAIMS, FIGURES, ABSTRACT):
        raw = path.read_text(encoding="utf-8")
        assert raw == json.dumps(json.loads(raw), indent=2, ensure_ascii=False) + "\n"
