from __future__ import annotations

import pytest

from tools.audit_two_level_gap_design_minimum import analyze


def test_exhaustive_design_audit_is_deterministic() -> None:
    assert analyze() == analyze()


def test_all_two_level_subsets_are_enumerated() -> None:
    rows = {entry["specimen_count"]: entry for entry in analyze()["subset_summary"]}

    assert rows[3]["candidate_subset_count"] == 56
    assert rows[4]["candidate_subset_count"] == 70
    assert rows[5]["candidate_subset_count"] == 56
    assert rows[6]["candidate_subset_count"] == 28
    assert rows[7]["candidate_subset_count"] == 8
    assert rows[8]["candidate_subset_count"] == 1

    assert rows[3]["full_rank_subset_count"] == 24
    assert rows[4]["full_rank_subset_count"] == 62
    assert rows[5]["full_rank_subset_count"] == 56
    assert rows[6]["full_rank_subset_count"] == 28
    assert rows[7]["full_rank_subset_count"] == 8
    assert rows[8]["full_rank_subset_count"] == 1


def test_no_smaller_subset_meets_all_audit_grade_thresholds() -> None:
    result = analyze()
    rows = {entry["specimen_count"]: entry for entry in result["subset_summary"]}

    assert all(rows[count]["audit_grade_subset_count"] == 0 for count in range(3, 8))
    assert rows[8]["audit_grade_subset_count"] == 1
    assert rows[7]["residual_degrees_of_freedom_if_full_rank"] == 9
    assert rows[7]["minimum_maximum_leverage_among_full_rank"] == pytest.approx(
        0.6120689655172413, abs=1e-12
    )
    assert rows[6]["minimum_maximum_leverage_among_full_rank"] == pytest.approx(
        0.5833333333333333, abs=1e-12
    )

    decision = result["decision"]
    assert decision["smallest_audit_grade_specimen_count"] == 8
    assert decision["eight_specimen_full_factorial_is_minimum_in_candidate_family"] is True
    assert decision["eight_specimen_design_is_unique_qualifier"] is True
    assert decision["smaller_design_authorized"] is False


def test_full_factorial_has_expected_optimal_metrics() -> None:
    row = analyze()["subset_summary"][-1]
    assert row["specimen_count"] == 8
    assert row["minimum_condition_number_among_full_rank"] == pytest.approx(
        2.6180339887498953, abs=1e-12
    )
    assert row["minimum_maximum_leverage_among_full_rank"] == pytest.approx(
        0.4375, abs=1e-12
    )
    assert row["maximum_information_determinant_among_full_rank"] == pytest.approx(
        65536.0, abs=1e-8
    )
