from __future__ import annotations

from pathlib import Path

from tools.audit_absorption_observation_source_recovery import audit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data/evidence/hgcdte_absorption_observation_source_recovery.csv"
MANIFEST = ROOT / "data/evidence/hgcdte_absorption_figure_digitization_manifest.csv"


def test_modern_absorption_sources_have_separate_authority_classes() -> None:
    result = audit(SOURCES, MANIFEST)
    assert result["source_count"] == 5
    assert result["observation_authorized_count"] == 0
    assert result["observation_conditional_count"] == 2
    assert result["observation_blocked_count"] == 2
    assert result["observation_review_only_count"] == 1
    assert result["static_gap_authorized_count"] == 0


def test_observation_research_is_authorized_but_production_is_not() -> None:
    decision = audit(SOURCES, MANIFEST)["decision"]
    assert decision["observation_model_research_authorized"] is True
    assert decision["production_observation_model_authorized"] is False
    assert decision["new_static_gap_refit_authorized"] is False
    assert decision["retain_measurement_class_separation"] is True


def test_digitization_remains_blocked_without_archived_source_images() -> None:
    result = audit(SOURCES, MANIFEST)
    assert result["figure_manifest_count"] == 7
    assert result["digitization_ready_figure_count"] == 0
    assert result["decision"]["figure_digitization_authorized_now"] is False


def test_moazzami_cross_method_evidence_is_preserved() -> None:
    result = audit(SOURCES, MANIFEST)
    by_id = {item["source_id"]: item for item in result["sources"]}
    source = by_id["moazzami_phillips_lee_et_al_2005"]
    assert source["observation_status"] == "conditional"
    assert source["cross_method_same_specimen"] is True
    assert source["bandgap_fit_dependency"] == (
        "Hansen_Eg_inserted_into_final_absorption_model"
    )
    assert source["static_status"] == "blocked"


def test_chang_carrier_metadata_does_not_make_static_fit_authority() -> None:
    result = audit(SOURCES, MANIFEST)
    by_id = {item["source_id"]: item for item in result["sources"]}
    source = by_id["chang_grein_sivananthan_flatte_2006"]
    assert source["carrier_type_recovered"] is True
    assert source["carrier_density_recovered"] is True
    assert source["independent_composition_method_recovered"] is False
    assert source["complete_static_authority"] is False
