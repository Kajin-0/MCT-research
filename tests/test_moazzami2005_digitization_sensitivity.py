from pathlib import Path

from tools.audit_moazzami2005_digitization_sensitivity import audit

ROOT = Path(__file__).resolve().parents[1]


def test_model_candidates_survive_declared_digitization_bounds() -> None:
    result = audit(ROOT)
    decision = result["decision"]
    assert decision["all_model_candidate_shifts_below_1mev"] is True
    assert decision["maximum_model_candidate_shift_mev"] < 1.0
    assert decision["model_family_conclusion_survives_digitization_bounds"] is True


def test_thresholds_through_4000_remain_below_the_5mev_gate() -> None:
    result = audit(ROOT)
    decision = result["decision"]
    assert decision["all_thresholds_through_4000cm1_below_5mev"] is True
    assert decision["calibration_sensitive_threshold_candidates"] == [
        "threshold_5000_cm-1"
    ]
    assert decision["threshold_5000_requires_separate_caution"] is True


def test_exact_point_counts_and_corner_count_are_preserved() -> None:
    result = audit(ROOT)
    assert [item["point_count"] for item in result["specimens"]] == [125, 115]
    assert [item["corner_count"] for item in result["specimens"]] == [4, 4]
