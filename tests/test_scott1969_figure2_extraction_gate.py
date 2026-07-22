from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "data/experimental/scott1969_figure2_extraction_gate.csv"
README_PATH = ROOT / "data/experimental/scott1969_figure2_extraction_README.md"
DIGITIZED_PATH = ROOT / "data/experimental/scott1969_figure2_digitized.csv"
CALIBRATION_PATH = ROOT / "data/experimental/scott1969_figure2_calibration.csv"


def _rows() -> dict[str, dict[str, str]]:
    with GATE_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["record_id"]: row for row in csv.DictReader(handle)}


def test_gate_contains_exact_figure_roles() -> None:
    rows = _rows()
    assert set(rows) == {"SCOTT69_F2", "SCOTT69_F5"}
    assert rows["SCOTT69_F2"]["role"] == "direct_marker_source"
    assert rows["SCOTT69_F5"]["role"] == "provenance_cross_check_only"
    assert rows["SCOTT69_F5"]["status"] == "rejected_as_independent_dataset"


def test_fixed_alpha_observation_class_is_preserved() -> None:
    rows = _rows()
    for row in rows.values():
        assert row["measurement_class"] == (
            "fixed_absorption_optical_edge_alpha_500_cm_inverse"
        )
        assert row["signed_gap_eligible"] == "false"
        assert row["intrinsic_gap_eligible_without_observation_operator"] == "false"


def test_numerical_extraction_remains_fail_closed_without_page_asset() -> None:
    rows = _rows()
    assert rows["SCOTT69_F2"]["page_asset_status"] == (
        "available_in_user_file_library_not_materialized"
    )
    assert rows["SCOTT69_F2"]["numerical_rows_authorized"] == "false"
    assert not DIGITIZED_PATH.exists()
    assert not CALIBRATION_PATH.exists()


def test_readme_requires_pixel_and_digest_provenance() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    required = {
        "page-image SHA256",
        "rendering tool and version",
        "pixel_half_width_x",
        "temperature_extraction_half_width_k",
        "pointwise_experimental_covariance",
        "Figure 5 independent numerical dataset      rejected",
    }
    missing = sorted(item for item in required if item not in text)
    assert not missing, f"missing extraction-governance statements: {missing}"


def test_readme_prohibits_equation_and_figure5_pseudodata() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "sample an Equation (3) curve as data" in text
    assert "add Figure 5 markers as independent observations" in text
    assert "replace a density-measured composition with a fit-required value" in text
    assert "absence of `scott1969_figure2_digitized.csv` is the correct fail-closed state" in text


def test_source_uncertainty_is_not_recast_as_pointwise_covariance() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "Coordinate-extraction bounds are not source measurement covariance" in text
    assert "`1-2 mole % CdTe`" in text
    assert "`+/-0.01 eV`" in text
