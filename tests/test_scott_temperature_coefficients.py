from __future__ import annotations

from pathlib import Path

import pytest

from mct_research.scott_temperature_coefficients import (
    HANSEN_B0_EV_PER_K,
    HANSEN_B1_EV_PER_K_PER_X,
    SUBSET_COMPOSITIONS,
    analyze_subset,
    build_reference,
    fit_independent_slopes,
    fit_shared_composition_slope,
    group_points,
    leave_one_specimen_out,
    linearized_box_sensitivity,
    load_scott_points,
    select_compositions,
    source_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/experimental/scott1969_figure2_digitized.csv"


def _points():
    return load_scott_points(SOURCE)


def _slopes_by_composition(points):
    groups = group_points(points)
    slopes = fit_independent_slopes(points)
    return {
        groups[label][0].composition_x: slopes[label]
        for label in groups
    }


def test_source_contract_and_specimen_counts() -> None:
    points = _points()
    groups = group_points(points)
    assert len(points) == 70
    assert len(groups) == 9
    assert sorted(len(series) for series in groups.values()) == [6, 7, 8, 8, 8, 8, 8, 8, 9]
    assert all(point.energy_half_width_ev == 0.0047 for point in points)
    assert all(point.temperature_half_width_k == 1.75 for point in points)


def test_independent_specimen_slopes_match_centered_coordinates() -> None:
    slopes = _slopes_by_composition(_points())
    assert slopes[0.23] == pytest.approx(3.250202919e-4, abs=1e-13)
    assert slopes[0.35] == pytest.approx(1.611972379e-4, abs=1e-13)
    assert slopes[0.46] == pytest.approx(4.267729535e-5, abs=1e-13)
    assert slopes[0.61] == pytest.approx(-7.646551428e-5, abs=1e-13)


def test_full_shared_slope_is_close_to_but_not_fixed_to_hansen() -> None:
    fit = fit_shared_composition_slope(_points())
    assert fit["rank"] == 2
    assert fit["b0_ev_per_k"] == pytest.approx(5.497835425e-4, abs=1e-13)
    assert fit["b1_ev_per_k_per_x"] == pytest.approx(-1.076209537e-3, abs=1e-13)
    assert fit["b0_ev_per_k"] != HANSEN_B0_EV_PER_K
    assert fit["b1_ev_per_k_per_x"] != HANSEN_B1_EV_PER_K_PER_X


def test_declared_subsets_are_exact() -> None:
    points = _points()
    expected_counts = {
        "full_9_specimens": (9, 70),
        "exclude_source_flagged_x_0p25_0p385_0p53": (6, 49),
        "exclude_x_0p61_outside_scott_equation_range": (8, 62),
        "core_unflagged_within_range": (5, 41),
        "exclude_endpoint_x_0p23_0p61": (7, 54),
    }
    for name, compositions in SUBSET_COMPOSITIONS.items():
        selected = select_compositions(points, compositions)
        assert len(group_points(selected)) == expected_counts[name][0]
        assert len(selected) == expected_counts[name][1]


def test_core_neither_shared_nor_hansen_model_is_box_feasible() -> None:
    core = select_compositions(
        _points(), SUBSET_COMPOSITIONS["core_unflagged_within_range"]
    )
    result = analyze_subset(core)
    s1 = result["S1_shared_linear_composition_slope"]
    sh = result["SH_hansen_fixed_slope"]
    assert s1["b0_ev_per_k"] == pytest.approx(6.038727338e-4, abs=1e-13)
    assert s1["b1_ev_per_k_per_x"] == pytest.approx(-1.235286852e-3, abs=1e-13)
    assert s1["metrics"]["maximum_normalized_box_residual"] == pytest.approx(
        1.418088513, abs=1e-9
    )
    assert sh["metrics"]["maximum_normalized_box_residual"] == pytest.approx(
        1.820916077, abs=1e-9
    )
    assert s1["metrics"]["box_feasible"] is False
    assert sh["metrics"]["box_feasible"] is False


def test_core_leave_one_specimen_out_fails_closed_for_both_models() -> None:
    core = select_compositions(
        _points(), SUBSET_COMPOSITIONS["core_unflagged_within_range"]
    )
    s1 = leave_one_specimen_out(core, model="S1")
    sh = leave_one_specimen_out(core, model="SH")
    assert s1["all_held_out_specimens_box_feasible"] is False
    assert sh["all_held_out_specimens_box_feasible"] is False
    assert s1["maximum_held_out_normalized_box_residual"] == pytest.approx(
        1.628014211, abs=1e-9
    )
    assert sh["maximum_held_out_normalized_box_residual"] == pytest.approx(
        1.820916077, abs=1e-9
    )


def test_linearized_box_sensitivity_contains_hansen_coefficients() -> None:
    core = select_compositions(
        _points(), SUBSET_COMPOSITIONS["core_unflagged_within_range"]
    )
    sensitivity = linearized_box_sensitivity(core)
    assert sensitivity["probabilistic_interpretation"] is False
    assert sensitivity["hansen_coefficients_inside_componentwise_envelope"] is True
    assert sensitivity["lower"]["b0_ev_per_k"] == pytest.approx(
        3.914851145e-4, abs=1e-13
    )
    assert sensitivity["upper"]["b0_ev_per_k"] == pytest.approx(
        8.162603531e-4, abs=1e-13
    )
    assert sensitivity["lower"]["b1_ev_per_k_per_x"] == pytest.approx(
        -1.809474839e-3, abs=1e-13
    )
    assert sensitivity["upper"]["b1_ev_per_k_per_x"] == pytest.approx(
        -6.610988646e-4, abs=1e-13
    )


def test_controlling_decision_is_non_identifiable_at_figure_precision() -> None:
    points = _points()
    reference = build_reference(points, source_csv_sha256=source_sha256(SOURCE))
    assert reference["decision"]["decision"] == "non_identifiable_at_figure_precision"
    assert reference["decision"]["gates"] == {
        "S1_core_box_feasible": False,
        "S1_core_leave_one_specimen_out_box_feasible": False,
        "SH_core_box_feasible": False,
        "SH_core_leave_one_specimen_out_box_feasible": False,
        "hansen_monotone_residual_sign_pattern": False,
        "hansen_coefficients_outside_S1_linearized_box_envelope": False,
    }


def test_analysis_never_changes_observation_class() -> None:
    reference = build_reference(_points(), source_csv_sha256=source_sha256(SOURCE))
    boundary = reference["observation_boundary"]
    assert boundary["signed_gap_eligible"] is False
    assert boundary["intrinsic_gap_eligible_without_observation_operator"] is False
    assert boundary["pointwise_experimental_covariance"] == "not_reported"
    assert boundary["coordinate_half_widths_are_gaussian_sigma"] is False
