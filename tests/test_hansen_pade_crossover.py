from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tools.analyze_hansen_pade_crossover import (
    HANSEN_SLOPE_MEV_PER_K,
    analyze,
    hansen_pade_gap_ev,
    hansen_static_gap_ev,
    pade_thermal_shape_mev,
    published_seiler_gap_ev,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/seiler1990_figure7_digitized.csv"


def test_candidate_is_zero_anchored_and_flat_at_zero_temperature() -> None:
    composition = 0.259
    tau = 18.0

    assert pade_thermal_shape_mev(np.asarray([0.0]), composition, tau)[0] == 0.0
    assert hansen_pade_gap_ev(composition, 0.0, tau) == pytest.approx(
        hansen_static_gap_ev(composition), abs=1e-15
    )

    small = np.asarray([1.0e-5, 2.0e-5])
    values = pade_thermal_shape_mev(small, composition, tau)
    numerical_slope = float((values[1] - values[0]) / (small[1] - small[0]))
    assert abs(numerical_slope) < 1e-10


def test_candidate_recovers_hansen_high_temperature_slope() -> None:
    composition = 0.239
    tau = 25.0
    temperature = 1.0e7
    expected_slope = HANSEN_SLOPE_MEV_PER_K * (1.0 - 2.0 * composition)
    value = float(
        pade_thermal_shape_mev(
            np.asarray([temperature]), composition, tau
        )[0]
    )

    assert value / temperature == pytest.approx(expected_slope, rel=1e-11)


def test_full_equations_return_finite_broadcast_values() -> None:
    composition = np.asarray([0.239, 0.259, 0.300])
    temperature = np.asarray([5.0, 50.0, 150.0])

    candidate = hansen_pade_gap_ev(composition, temperature, 20.0)
    published = published_seiler_gap_ev(composition, temperature)

    assert np.asarray(candidate).shape == composition.shape
    assert np.asarray(published).shape == composition.shape
    assert np.all(np.isfinite(candidate))
    assert np.all(np.isfinite(published))


def test_analysis_is_deterministic_and_leakage_safe() -> None:
    first = analyze(DATA)
    second = analyze(DATA)

    assert first["candidate_equation"] == second["candidate_equation"]
    assert first["pooled_heldout_shape_metrics"] == second[
        "pooled_heldout_shape_metrics"
    ]
    assert first["parameter_stability"] == second["parameter_stability"]

    absolute = first["independent_composition_absolute_test"]
    assert absolute["heldout_sample"] == 3
    assert absolute["training_samples_for_tau"] == [1, 2]
    assert absolute["composition_x"] == pytest.approx(0.259)
    assert absolute["composition_sigma_x"] == pytest.approx(0.0015)
    assert absolute["tau_k"] > 0.0

    for model, metrics in absolute["metrics"].items():
        assert model in {"hansen_linear", "published_seiler", "fixed_slope_pade"}
        assert metrics["count"] == 9
        assert np.isfinite(metrics["rmse_mev"])


def test_promotion_decision_is_fully_gate_driven() -> None:
    result = analyze(DATA)
    checks = result["promotion_checks"]

    assert set(checks) == {
        "shape_rmse_improves_over_hansen_by_20_percent",
        "shape_rmse_within_20_percent_of_two_parameter_seiler",
        "crossover_stable_within_factor_two",
        "absolute_sample3_beats_hansen",
        "absolute_sample3_not_worse_than_published_seiler_by_more_than_1mev",
    }
    assert all(isinstance(value, bool) for value in checks.values())
    assert result["decision"]["all_promotion_checks_pass"] is all(checks.values())
    assert result["decision"]["candidate_promoted_to_repository_model"] is False


def test_invalid_tau_fails_closed() -> None:
    with pytest.raises(ValueError, match="tau_k"):
        pade_thermal_shape_mev(np.asarray([10.0]), 0.25, 0.0)
