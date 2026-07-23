from __future__ import annotations

from pathlib import Path

from mct_research.r01_temperature_benchmark_eligibility import (
    DECISION,
    build_reference,
    sha256_file,
)

ROOT = Path(__file__).resolve().parents[1]


def _reference():
    return build_reference(ROOT)


def test_source_inventory_and_counts_are_exact() -> None:
    result = _reference()
    assert result["program"] == "R01"
    assert result["parent_issue"] == 8
    assert result["issue"] == 320
    assert result["summary"] == {
        "source_count": 4,
        "row_count": 167,
        "temperature_series_specimen_count": 21,
        "exact_measurement_class_count": 4,
        "maximum_sources_in_one_exact_class": 1,
    }
    assert [source["source_id"] for source in result["sources"]] == [
        "chu_mi_tang_1991",
        "schmit_stelzer1969",
        "scott1969",
        "seiler1990",
    ]


def test_every_counted_source_passes_e1() -> None:
    result = _reference()
    assert result["gates"]["E1_all_in_scope_sources_eligible"] is True
    assert all(source["e1_eligible"] for source in result["sources"])
    assert all(not source["e1_failures"] for source in result["sources"])
    assert all(source["eligible_for_intercept_profiled_shape"] for source in result["sources"])


def test_exact_measurement_classes_are_not_pooled() -> None:
    result = _reference()
    classes = result["measurement_classes"]
    assert len(classes) == 4
    assert all(record["source_count"] == 1 for record in classes)
    assert all(
        record["source_held_out_ranking_authorized"] is False
        for record in classes
    )
    assert result["observation_boundary"]["exact_measurement_class_matching_required"] is True
    assert result["observation_boundary"]["cross_class_pooling_authorized"] is False


def test_source_specific_observation_boundaries_are_preserved() -> None:
    result = _reference()
    sources = {source["source_id"]: source for source in result["sources"]}
    assert sources["seiler1990"]["measurement_class"] == (
        "two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap"
    )
    assert sources["seiler1990"]["absolute_gap_eligible_specimen_count"] == 1
    assert sources["chu_mi_tang_1991"]["measurement_class"] == (
        "absorption_turning_point_edge"
    )
    assert sources["chu_mi_tang_1991"]["eligible_for_absolute_gap_ranking"] is False
    assert sources["scott1969"]["signed_gap_eligible"] is False
    assert sources["scott1969"]["intrinsic_gap_eligible_without_observation_operator"] is False
    assert sources["schmit_stelzer1969"]["signed_gap_eligible"] is False
    assert sources["schmit_stelzer1969"]["intrinsic_gap_eligible_without_observation_operator"] is False


def test_canonical_file_hashes_match_repository_bytes() -> None:
    for source in _reference()["sources"]:
        for record in source["canonical_files"]:
            assert record["sha256"] == sha256_file(ROOT / record["path"])


def test_fail_closed_decision_and_advancement_gates() -> None:
    result = _reference()
    assert result["decision"] == DECISION
    assert result["gates"] == {
        "E1_all_in_scope_sources_eligible": True,
        "E2_any_exact_class_source_holdout_authorized": False,
        "E3_any_exact_class_absolute_ranking_authorized": False,
        "E4_universal_model_advancement_authorized": False,
    }
    assert all(
        source["eligible_for_source_holdout"] is False
        for source in result["sources"]
    )


def test_audit_performs_no_fit_or_nuisance_correction() -> None:
    boundary = _reference()["observation_boundary"]
    assert boundary["model_coefficients_fitted"] == 0
    assert boundary["source_offsets_fitted"] == 0
    assert boundary["composition_shifts_fitted"] == 0
    assert boundary["observation_operator_inference_authorized"] is False
    assert boundary["deterministic_bounds_recast_as_gaussian_sigma"] is False
