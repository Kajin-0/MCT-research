from __future__ import annotations

import pytest

from tools.run_laurenti_series_minimum_temperature_design import (
    DIRECT_SERIES_X,
    discrimination_components,
    minimum_discriminating_temperature_k,
    run_study,
    separation_composition_derivative_ev_per_x,
    thermal_shape_separation_ev,
)


def test_shape_separation_reference_and_room_temperature_values() -> None:
    for x in DIRECT_SERIES_X:
        assert thermal_shape_separation_ev(x, 2.0) == pytest.approx(0.0, abs=1.0e-15)

    assert 1000.0 * thermal_shape_separation_ev(0.500, 300.0) == pytest.approx(
        1.17403945755, abs=1.0e-9
    )
    assert 1000.0 * thermal_shape_separation_ev(0.970, 300.0) == pytest.approx(
        74.9550826043, abs=1.0e-9
    )


def test_composition_derivative_is_step_stable() -> None:
    for x in (0.710, 0.805, 0.925, 0.970):
        coarse = separation_composition_derivative_ev_per_x(x, 150.0, step=1.0e-5)
        fine = separation_composition_derivative_ev_per_x(x, 150.0, step=5.0e-6)
        assert coarse == pytest.approx(fine, rel=0.0, abs=2.0e-9)


def test_nominal_minimum_temperature_thresholds() -> None:
    expected = {
        0.500: None,
        0.550: None,
        0.620: None,
        0.710: 119,
        0.805: 63,
        0.925: 39,
        0.955: 36,
        0.970: 34,
    }
    for x, threshold in expected.items():
        assert minimum_discriminating_temperature_k(
            x, digitization_sigma_mev=0.0
        ) == threshold

        if threshold is not None:
            at_threshold = discrimination_components(
                x, float(threshold), digitization_sigma_mev=0.0
            )
            before = discrimination_components(
                x, float(threshold - 1), digitization_sigma_mev=0.0
            )
            assert at_threshold["z_score"] >= 3.0
            assert before["z_score"] < 3.0


def test_digitization_uncertainty_delays_but_does_not_erase_high_cd_decision() -> None:
    expected_at_five_mev = {
        0.710: None,
        0.805: 156,
        0.925: 87,
        0.955: 78,
        0.970: 74,
    }
    for x, threshold in expected_at_five_mev.items():
        assert minimum_discriminating_temperature_k(
            x, digitization_sigma_mev=5.0
        ) == threshold

    assert minimum_discriminating_temperature_k(
        0.970, digitization_sigma_mev=5.0
    ) < 90


def test_study_grid_and_null_control() -> None:
    rows = run_study()
    assert len(rows) == 40

    nominal = {
        float(row["x"]): row
        for row in rows
        if float(row["digitization_sigma_per_point_mev"]) == 0.0
    }
    assert float(nominal[0.500]["z_score_at_300k"]) < 0.3
    assert float(nominal[0.620]["z_score_at_300k"]) < 3.0
    assert float(nominal[0.710]["z_score_at_300k"]) > 5.0
    assert float(nominal[0.970]["composition_sigma_at_300k_mev"]) < 0.72
