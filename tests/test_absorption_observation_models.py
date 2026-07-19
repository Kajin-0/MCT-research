from __future__ import annotations

import pytest

from tools.benchmark_absorption_observation_models import (
    analyze,
    analyze_scenario,
    moazzami_parameters,
)


def test_moazzami_reference_parameters() -> None:
    coefficient_k, exponent_n = moazzami_parameters(0.21, 80.0)
    assert coefficient_k == pytest.approx(5066.531, abs=1e-9)
    assert exponent_n == pytest.approx(0.7025951, abs=1e-10)

    coefficient_k, exponent_n = moazzami_parameters(0.31, 300.0)
    assert coefficient_k == pytest.approx(48814.103, abs=1e-9)
    assert exponent_n == pytest.approx(0.7761787, abs=1e-10)


def test_correct_fractional_power_recovers_its_latent_edge() -> None:
    result = analyze()
    for scenario in result["scenarios"]:
        fit = scenario["moazzami_truth_fits"]["free"]
        assert abs(fit["edge_bias_mev"]) <= 0.05
        expected = scenario["moazzami_parameters"]["n"]
        assert fit["exponent"] == pytest.approx(expected, abs=0.003)


def test_wrong_model_and_thresholds_generate_multi_mev_bias() -> None:
    result = analyze()
    linear_biases = [
        abs(row["moazzami_truth_fits"]["linear_1p0"]["edge_bias_mev"])
        for row in result["scenarios"]
    ]
    nonparabolic_free_biases = [
        abs(row["chang_inspired_truth_fits"]["free"]["edge_bias_mev"])
        for row in result["scenarios"]
    ]
    threshold_biases = [
        row["chang_inspired_threshold_bias_mev"]["1500"]
        for row in result["scenarios"]
    ]
    threshold_spreads = [
        row["threshold_spread_600_to_2000_mev"]
        for row in result["scenarios"]
    ]

    assert max(linear_biases) >= 4.5
    assert max(nonparabolic_free_biases) >= 10.0
    assert min(threshold_biases) >= 8.0
    assert min(threshold_spreads) >= 15.0


def test_nominal_scenario_values_are_deterministic() -> None:
    result = analyze_scenario(0.21, 80.0)
    assert result["latent_gap_ev"] == pytest.approx(0.101413416007612, abs=1e-14)
    assert result["moazzami_truth_fits"]["free"]["edge_bias_mev"] == pytest.approx(
        -0.005, abs=1e-9
    )
    assert result["moazzami_truth_fits"]["linear_1p0"][
        "edge_bias_mev"
    ] == pytest.approx(-8.1075, abs=1e-8)
    assert result["chang_inspired_truth_fits"]["free"][
        "edge_bias_mev"
    ] == pytest.approx(-11.3625, abs=1e-8)
    assert result["chang_inspired_threshold_bias_mev"]["1500"] == pytest.approx(
        9.2088066524, abs=1e-7
    )


def test_sensitivity_and_decision_remain_fail_closed() -> None:
    result = analyze()
    sensitivity = result["sensitivity"]
    decision = result["decision"]

    assert sensitivity["case_count"] == 36
    assert sensitivity["threshold_bias_aggregates"]["1500"][
        "median_mev"
    ] >= 8.0
    assert all(result["validation_checks"].values())
    assert decision["measurement_definition_can_generate_multi_mev_edge_bias"] is True
    assert decision["production_observation_correction_authorized"] is False
    assert decision["static_gap_refit_authorized"] is False
    assert "edge-model uncertainty envelope" in decision["required_reporting"]
