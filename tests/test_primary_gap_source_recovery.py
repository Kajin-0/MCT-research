from __future__ import annotations

from pathlib import Path

from tools.audit_primary_gap_source_recovery import audit

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/evidence/hgcdte_primary_gap_source_recovery.csv"


def test_primary_source_recovery_audit_is_fail_closed() -> None:
    result = audit(LEDGER)
    assert result["source_count"] == 9
    assert result["primary_source_count"] == 8
    assert result["authorized_primary_fit_source_count"] == 0
    assert result["conditional_primary_source_count"] == 2
    assert result["blocked_primary_source_count"] == 6
    assert result["screen_only_source_count"] == 1
    assert result["decision"]["new_static_refit_authorized"] is False
    assert result["decision"]["secondary_table_is_fit_authority"] is False
    assert result["decision"]["abstract_formula_is_point_level_evidence"] is False


def test_seiler_and_orlita_are_conditional_primary_evidence() -> None:
    result = audit(LEDGER)
    statuses = {item["source_id"]: item["status"] for item in result["sources"]}
    assert statuses["seiler_lowney_littler_yoon_jvst"] == "conditional"
    assert statuses["orlita2014_graded_mbe"] == "conditional"
    assert statuses["chu_sher_table_4_4_secondary"] == "screen_only"
    for source_id in (
        "chu_mi_tang_infrared_physics",
        "chu_mi_tang_jap",
        "scott_jap",
        "schmit_stelzer_jap",
        "hansen_schmit_casselman_jap",
        "chu_xu_tang_apl",
    ):
        assert statuses[source_id] == "blocked"


def test_orlita_is_incomplete_despite_primary_full_text() -> None:
    result = audit(LEDGER)
    orlita = next(
        item for item in result["sources"] if item["source_id"] == "orlita2014_graded_mbe"
    )
    assert orlita["status"] == "conditional"
    assert orlita["requirements"] == {
        "full_text_recovered": "true",
        "point_level_gap_data_recovered": "true",
        "composition_method_recovered": "true",
        "point_uncertainties_recovered": "false",
        "measurement_definition_recovered": "true",
    }
    assert orlita["complete_primary_evidence"] is False


def test_no_blocked_source_has_complete_primary_evidence() -> None:
    result = audit(LEDGER)
    blocked = [item for item in result["sources"] if item["status"] == "blocked"]
    assert blocked
    assert all(item["complete_primary_evidence"] is False for item in blocked)
