from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tools.analyze_two_parameter_hansen_pade import (
    analyze,
    two_parameter_gap_ev,
)
from tools.analyze_hansen_pade_crossover import hansen_static_gap_ev

ROOT = Path(__file__).resolve().parents[1]
FIGURE7 = ROOT / "data/experimental/seiler1990_figure7_digitized.csv"
LOW_T = ROOT / "data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv"


def test_equation_is_zero_anchored_and_has_declared_high_temperature_slope() -> None:
    x = 0.259
    alpha_mev_per_k = 0.593
    tau_k = 18.0

    assert two_parameter_gap_ev(x, 0.0, alpha_mev_per_k, tau_k) == pytest.approx(
        hansen_static_gap_ev(x), abs=1e-15
    )
    temperature = 1.0e7
    thermal_mev = 1000.0 * (
        two_parameter_gap_ev(x, temperature, alpha_mev_per_k, tau_k)
        - hansen_static_gap_ev(x)
    )
    assert thermal_mev / temperature == pytest.approx(
        alpha_mev_per_k * (1.0 - 2.0 * x), rel=1e-11
    )


def test_equation_broadcasts_and_remains_finite() -> None:
    x = np.asarray([0.239, 0.259, 0.300])
    temperature = np.asarray([5.0, 50.0, 150.0])
    values = two_parameter_gap_ev(x, temperature, 0.593, 18.0)

    assert np.asarray(values).shape == x.shape
    assert np.all(np.isfinite(values))


def test_analysis_is_deterministic_and_reports_all_validation_layers() -> None:
    first = analyze(FIGURE7, LOW_T)
    second = analyze(FIGURE7, LOW_T)

    assert first["all_specimen_shape_fit"] == second["all_specimen_shape_fit"]
    assert first["fold_parameter_stability"] == second["fold_parameter_stability"]
    assert first["promotion_checks"] == second["promotion_checks"]

    fit = first["all_specimen_shape_fit"]
    assert fit["alpha_mev_per_k"] > 0.0
    assert fit["tau_k"] > 0.0

    absolute = first["independent_composition_absolute_test"]
    assert absolute["heldout_sample"] == 3
    assert absolute["training_samples"] == [1, 2]
    assert absolute["composition_x"] == pytest.approx(0.259)
    assert absolute["composition_sigma_x"] == pytest.approx(0.0015)

    low_temperature = first["independent_low_temperature_composition_check"]
    assert len(low_temperature["records"]) == 3
    assert {
        int(record["sample_number"]) for record in low_temperature["records"]
    } == {3, 4, 5}


def test_promotion_is_gate_driven_but_not_production_authorization() -> None:
    result = analyze(FIGURE7, LOW_T)
    checks = result["promotion_checks"]

    assert set(checks) == {
        "shape_rmse_within_10_percent_of_trained_seiler",
        "shape_rmse_beats_published_seiler",
        "alpha_stable_within_5_percent",
        "tau_stable_within_factor_two",
        "absolute_sample3_beats_hansen",
        "absolute_sample3_beats_published_seiler",
        "low_temperature_nominal_rmse_not_worse_than_hansen_by_more_than_0p5mev",
    }
    assert all(isinstance(value, bool) for value in checks.values())
    assert result["decision"]["all_promotion_checks_pass"] is all(checks.values())
    assert result["decision"]["leading_analytical_candidate"] is all(
        checks.values()
    )
    assert result["decision"]["production_equation_authorized"] is False


def test_nonpositive_tau_fails_closed() -> None:
    with pytest.raises(ValueError, match="tau_k"):
        two_parameter_gap_ev(0.25, 10.0, 0.593, 0.0)
