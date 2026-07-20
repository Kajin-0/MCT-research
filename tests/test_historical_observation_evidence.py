from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.audit_historical_observation_evidence import audit

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/evidence/hgcdte_historical_observation_evidence.json"
CHANG = ROOT / "data/evidence/hgcdte_historical_observation_chang2004.json"


def test_bounded_inventory_includes_chang2004_extension() -> None:
    result = audit(PACKAGE)
    assert result["source_count"] == 8
    assert result["specimen_group_count"] == 14
    assert result["explicit_observation_count"] == 11
    assert result["expanded_observation_count"] == 67
    assert result["schmit_table_iii_count"] == 56
    assert result["sign_constraint_count"] == 2
    assert result["chang2004_urbach_record_count"] == 6
    assert result["same_point_pairing_count"] == 1


def test_measurement_classes_remain_separate() -> None:
    counts = audit(PACKAGE)["measurement_class_counts"]
    assert counts == {
        "combined_resonance_fit": 1,
        "detector_half_peak_cutoff": 56,
        "gap_sign_or_crossing_constraint": 2,
        "magnetoreflectance_fit": 2,
        "urbach_dynamic_electron_phonon_component": 3,
        "urbach_static_disorder_component": 3,
    }


def test_value_status_inventory_preserves_exact_chang_table_rows() -> None:
    assert audit(PACKAGE)["value_status_counts"] == {
        "exact_reported_value": 2,
        "exact_table": 62,
        "note_added_in_proof": 1,
        "sign_constraint": 2,
    }


def test_no_universal_static_refit_is_authorized() -> None:
    result = audit(PACKAGE)
    assert result["universal_static_fit_authorized"] is False
    assert result["decision"]["new_universal_gap_refit_authorized"] is False
    assert result["decision"]["pool_measurement_classes_by_default"] is False


def test_schmit_values_remain_detector_cutoffs() -> None:
    result = audit(PACKAGE)
    assert result["measurement_class_counts"]["detector_half_peak_cutoff"] == 56


def test_wiley_mccombe_lineage_and_carrier_metadata_are_preserved() -> None:
    result = audit(PACKAGE)
    assert result["shared_wiley_mccombe_lineage_preserved"] is True


def test_groves_sign_change_is_not_replaced_by_point_estimates() -> None:
    result = audit(PACKAGE)
    assert result["value_status_counts"]["sign_constraint"] == 2


def test_chang2004_table_i_transcription_is_exact() -> None:
    extension = json.loads(CHANG.read_text(encoding="utf-8"))
    rows = {row["observation_id"]: row for row in extension["observations"]}
    expected = {
        "chang2004_x040_urbach_A": (0.0190, 0.0002),
        "chang2004_x040_urbach_B": (0.0012, 0.0001),
        "chang2004_x030_urbach_A": (0.0112, 0.0003),
        "chang2004_x030_urbach_B": (0.0008, 0.0001),
        "chang2004_x021_urbach_A": (0.0124, 0.0005),
        "chang2004_x021_urbach_B": (0.00067, 0.00027),
    }
    assert set(rows) == set(expected)
    for observation_id, (value, sigma) in expected.items():
        row = rows[observation_id]
        assert row["reported_value_eV"] == pytest.approx(value, abs=1e-12)
        assert row["reported_sigma_eV"] == pytest.approx(sigma, abs=1e-12)
        assert row["value_status"] == "exact_table"
        assert row["temperature_K"] is None
        assert row["quantity"].startswith("urbach_width_")


def test_chang2004_composition_uncertainty_is_not_invented() -> None:
    extension = json.loads(CHANG.read_text(encoding="utf-8"))
    assert [row["composition_nominal"] for row in extension["specimens"]] == [
        0.4,
        0.3,
        0.21,
    ]
    assert all(row["composition_sigma"] is None for row in extension["specimens"])
    assert all(
        row["composition_sigma"] is None for row in extension["observations"]
    )


def test_chang2004_pairing_is_documented_but_offset_is_unidentified() -> None:
    result = audit(PACKAGE)
    assert result["chang2004_same_point_pairing_documented"] is True
    assert result["chang2004_numeric_method_offset_identified"] is False
    assert result["decision"]["chang2004_urbach_components_authorized"] is True
    assert result["decision"]["chang2004_numeric_pair_offset_authorized"] is False

    pairing = json.loads(CHANG.read_text(encoding="utf-8"))["same_point_pairing"]
    assert pairing["paired_temperatures_K"] == [77, 293]
    assert pairing["specimen_composition_identified"] is False
    assert pairing["numerical_paired_gap_table_reported"] is False
    assert pairing["photoconductive_edge_operator_complete"] is False


def test_chang2004_asset_is_hash_bound_without_committing_source_pdf() -> None:
    extension = json.loads(CHANG.read_text(encoding="utf-8"))
    source = extension["source"]
    assert source["input_asset_sha256"] == (
        "de5dba52fa075fe197dbd182c00ef22ee620f0ad571e82e78f6b2a2698181424"
    )
    assert source["copyrighted_source_committed"] == "false"
    assert audit(PACKAGE)["copyrighted_source_files_committed"] is False
