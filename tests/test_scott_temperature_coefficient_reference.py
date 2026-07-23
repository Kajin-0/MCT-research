from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/experimental/scott1969_figure2_digitized.csv"
REFERENCE = ROOT / "data/validation/scott1969_temperature_coefficient_test.json"
BUILDER = ROOT / "tools/build_scott_temperature_coefficient_reference.py"


def _reference() -> dict:
    return json.loads(REFERENCE.read_text(encoding="utf-8"))


def test_committed_reference_regenerates_exactly(tmp_path: Path) -> None:
    regenerated = tmp_path / "scott-temperature-coefficient.json"
    subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--source",
            str(SOURCE),
            "--output",
            str(regenerated),
        ],
        cwd=ROOT,
        check=True,
    )
    assert regenerated.read_bytes() == REFERENCE.read_bytes()


def test_reference_is_bound_to_merged_scott_ledger() -> None:
    result = _reference()
    assert result["schema_version"] == "1.0"
    assert result["program"] == "R01"
    assert result["issue"] == 312
    assert result["source"] == {
        "path": "data/experimental/scott1969_figure2_digitized.csv",
        "row_count": 70,
        "sha256": "6fd672cb9469d16d0dce2dc4657af99391e1652b79a2e59cd4661d03bdebc851",
        "specimen_count": 9,
    }


def test_full_fit_is_numerically_near_hansen_but_not_a_pass() -> None:
    result = _reference()
    full = result["subset_analyses"]["full_9_specimens"]
    assert full["S1"]["b0_ev_per_k"] == pytest.approx(
        5.49783543e-4, abs=5e-13
    )
    assert full["S1"]["b1_ev_per_k_per_x"] == pytest.approx(
        -1.076209537e-3, abs=5e-13
    )
    assert full["S1"]["metrics"]["box_feasible"] is False
    assert full["SH"]["metrics"]["box_feasible"] is False


def test_core_gate_fails_for_shared_and_hansen_slopes() -> None:
    result = _reference()
    core = result["subset_analyses"]["core_unflagged_within_range"]
    assert core["compositions_x"] == [0.23, 0.31, 0.35, 0.405, 0.46]
    assert core["S1"]["metrics"]["maximum_normalized_box_residual"] == pytest.approx(
        1.418088512811, abs=5e-13
    )
    assert core["SH"]["metrics"]["maximum_normalized_box_residual"] == pytest.approx(
        1.82091607736, abs=5e-13
    )
    assert core["S1"]["metrics"]["box_feasible"] is False
    assert core["SH"]["metrics"]["box_feasible"] is False


def test_core_held_out_prediction_fails_for_both_models() -> None:
    result = _reference()
    held_out = result["leave_one_specimen_out"]["core_unflagged_within_range"]
    assert held_out["S1"]["all_held_out_specimens_box_feasible"] is False
    assert held_out["SH"]["all_held_out_specimens_box_feasible"] is False
    assert held_out["S1"]["maximum_held_out_normalized_box_residual"] == pytest.approx(
        1.628014211258, abs=5e-13
    )
    assert held_out["SH"]["maximum_held_out_normalized_box_residual"] == pytest.approx(
        1.82091607736, abs=5e-13
    )


def test_hansen_remains_inside_nonprobabilistic_box_sensitivity() -> None:
    result = _reference()
    sensitivity = result["linearized_box_sensitivity"][
        "core_unflagged_within_range"
    ]
    assert sensitivity["probabilistic_interpretation"] is False
    assert sensitivity["hansen_coefficients_inside_componentwise_envelope"] is True
    assert sensitivity["lower"]["b0_ev_per_k"] == pytest.approx(
        3.91485115e-4, abs=5e-13
    )
    assert sensitivity["upper"]["b0_ev_per_k"] == pytest.approx(
        8.16260353e-4, abs=5e-13
    )
    assert sensitivity["lower"]["b1_ev_per_k_per_x"] == pytest.approx(
        -1.809474839e-3, abs=5e-13
    )
    assert sensitivity["upper"]["b1_ev_per_k_per_x"] == pytest.approx(
        -6.61098865e-4, abs=5e-13
    )


def test_final_decision_and_observation_boundary_are_fail_closed() -> None:
    result = _reference()
    assert result["decision"]["decision"] == "non_identifiable_at_figure_precision"
    assert result["decision"]["gates"] == {
        "S1_core_box_feasible": False,
        "S1_core_leave_one_specimen_out_box_feasible": False,
        "SH_core_box_feasible": False,
        "SH_core_leave_one_specimen_out_box_feasible": False,
        "hansen_coefficients_outside_S1_linearized_box_envelope": False,
        "hansen_monotone_residual_sign_pattern": False,
    }
    boundary = result["observation_boundary"]
    assert boundary["signed_gap_eligible"] is False
    assert boundary["intrinsic_gap_eligible_without_observation_operator"] is False
    assert boundary["coordinate_half_widths_are_gaussian_sigma"] is False
    assert boundary["pointwise_experimental_covariance"] == "not_reported"
