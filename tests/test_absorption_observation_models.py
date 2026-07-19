from __future__ import annotations

import pytest

from tools.benchmark_absorption_observation_models import analyze, analyze_scenario, moazzami_parameters


def test_moazzami_reference_parameters() -> None:
    k_value, exponent = moazzami_parameters(0.21, 80.0)
    assert k_value == pytest.approx(5066.531, abs=1e-9)
    assert exponent == pytest.approx(0.7025951, abs=1e-10)
    k_value, exponent = moazzami_parameters(0.31, 300.0)
    assert k_value == pytest.approx(48814.103, abs=1e-9)
    assert exponent == pytest.approx(0.7761787, abs=1e-10)


def test_correct_fractional_power_recovers_its_latent_edge() -> None:
    for scenario in analyze()["scenarios"]:
        fit = scenario["moazzami_truth_fits"]["free"]
        assert abs(fit["edge_bias_mev"]) <= 0.05
        assert fit["exponent"] == pytest.approx(
            scenario["moazzami_parameters"]["n"], abs=0.003
        )


def test_wrong_models_and_thresholds_generate_multi_mev_bias() -> None:
    scenarios = analyze()["scenarios"]
    assert max(
        abs(row["moazzami_truth_fits"]["linear_1p0"]["edge_bias_mev"])
        for row in scenarios
    ) >= 4.5
    assert max(
        abs(row["chang_inspired_truth_fits"]["free"]["edge_bias_mev"])
        for row in scenarios
    ) >= 10.0
    assert min(
        row["chang_inspired_threshold_bias_mev"]["1500"] for row in scenarios
    ) >= 8.0
    assert min(row["threshold_spread_600_to_2000_mev"] for row in scenarios) >= 15.0


def test_nominal_scenario_is_stable_at_declared_resolution() -> None:
    result = analyze_scenario(0.21, 80.0)
    assert result["latent_gap_ev"] == pytest.approx(0.101413416007612, abs=1e-14)
    assert result["moazzami_truth_fits"]["free"]["edge_bias_mev"] == pytest.approx(
        0.00375, abs=1e-6
    )
    assert result["moazzami_truth_fits"]["linear_1p0"]["edge_bias_mev"] == pytest.approx(
        -8.09875, abs=1e-5
    )
    assert result["chang_inspired_truth_fits"]["free"]["edge_bias_mev"] == pytest.approx(
        -11.3625, abs=1e-5
    )
    assert result["chang_inspired_threshold_bias_mev"]["1500"] == pytest.approx(
        9.2088066524, abs=1e-7
    )


def test_sensitivity_and_decision_remain_fail_closed() -> None:
    result = analyze()
    assert result["sensitivity"]["case_count"] == 36
    assert result["sensitivity"]["threshold_bias_aggregates"]["1500"]["median_mev"] >= 8.0
    assert all(result["validation_checks"].values())
    assert result["decision"]["measurement_definition_can_generate_multi_mev_edge_bias"] is True
    assert result["decision"]["production_observation_correction_authorized"] is False
    assert result["decision"]["static_gap_refit_authorized"] is False
