from __future__ import annotations

from pathlib import Path

from tools.audit_historical_observation_evidence import audit

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/evidence/hgcdte_historical_observation_evidence.json"


def test_first_tranche_has_exact_bounded_inventory() -> None:
    result = audit(PACKAGE)
    assert result["source_count"] == 7
    assert result["specimen_group_count"] == 11
    assert result["explicit_observation_count"] == 5
    assert result["expanded_observation_count"] == 61
    assert result["schmit_table_iii_count"] == 56
    assert result["sign_constraint_count"] == 2


def test_measurement_classes_remain_separate() -> None:
    counts = audit(PACKAGE)["measurement_class_counts"]
    assert counts == {
        "combined_resonance_fit": 1,
        "detector_half_peak_cutoff": 56,
        "gap_sign_or_crossing_constraint": 2,
        "magnetoreflectance_fit": 2,
    }


def test_no_universal_static_refit_is_authorized() -> None:
    result = audit(PACKAGE)
    assert result["universal_static_fit_authorized"] is False
    assert result["decision"]["new_universal_gap_refit_authorized"] is False
    assert result["decision"]["pool_measurement_classes_by_default"] is False


def test_schmit_values_remain_detector_cutoffs() -> None:
    result = audit(PACKAGE)
    assert result["measurement_class_counts"]["detector_half_peak_cutoff"] == 56
    assert result["value_status_counts"]["exact_table"] == 56


def test_wiley_mccombe_lineage_and_carrier_metadata_are_preserved() -> None:
    result = audit(PACKAGE)
    assert result["shared_wiley_mccombe_lineage_preserved"] is True


def test_groves_sign_change_is_not_replaced_by_point_estimates() -> None:
    result = audit(PACKAGE)
    assert result["value_status_counts"]["sign_constraint"] == 2


def test_copyrighted_primary_pdfs_are_not_committed() -> None:
    result = audit(PACKAGE)
    assert result["copyrighted_source_files_committed"] is False
