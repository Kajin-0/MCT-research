from __future__ import annotations

import numpy as np
import pytest

from mct_research.analytical_benchmark import (
    GapBenchmarkData,
    OscillatorBasisSpec,
    bose_occupation_basis,
    coefficient_constraint,
    combine_constraints,
    endpoint_constraints,
    fit_linear_gap_model,
    leave_one_group_out,
    named_holdout_cross_validation,
    oscillator_design_matrix,
    residual_metrics,
)


def _composition_temperature_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    compositions = np.array([0.2, 0.4, 0.6, 0.8])
    temperatures = np.array([0.0, 10.0, 30.0, 60.0, 100.0, 180.0, 300.0])
    x = np.repeat(compositions, temperatures.size)
    temperature = np.tile(temperatures, compositions.size)
    groups = np.repeat(["s1", "s2", "s3", "s4"], temperatures.size)
    return x, temperature, groups


def test_bose_basis_has_correct_zero_temperature_limit() -> None:
    values = bose_occupation_basis(100.0, np.array([0.0, 50.0, 100.0]))
    assert values[0] == 0.0
    assert values[1] == pytest.approx(2.0 / np.expm1(2.0))
    assert values[2] == pytest.approx(2.0 / np.expm1(1.0))


def test_one_oscillator_exact_recovery() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=2,
        amplitude_degree=1,
        oscillator_temperatures_k=(150.0,),
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    expected = np.array([-0.30, 1.80, -0.20, 0.04, -0.08])
    gap = matrix @ expected
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=0.001,
        group=groups,
    )

    result = fit_linear_gap_model(data, specification)

    np.testing.assert_allclose(result.coefficients, expected, atol=1.0e-12)
    assert result.metrics.rmse_mev < 1.0e-8
    assert result.design_rank == expected.size
    assert result.free_parameter_count == expected.size
    assert result.condition_number > 1.0


def test_two_signed_oscillators_recover_turnover() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=1,
        amplitude_degree=0,
        oscillator_temperatures_k=(20.0, 200.0),
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    expected = np.array([-0.20, 1.50, -0.01, 0.20])
    gap = matrix @ expected
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=0.001,
        group=groups,
    )

    result = fit_linear_gap_model(data, specification)
    predicted = np.asarray(result.predict(0.4, temperature[:7]))

    np.testing.assert_allclose(result.coefficients, expected, atol=1.0e-12)
    assert np.argmin(predicted) not in (0, predicted.size - 1)
    assert predicted[-1] > predicted[np.argmin(predicted)]


def test_endpoint_constraints_hold_and_remove_covariance_directions() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=2,
        amplitude_degree=1,
        oscillator_temperatures_k=(150.0,),
    )
    matrix, labels = oscillator_design_matrix(specification, x, temperature)
    expected = np.array([-0.30, 1.80, -0.20, 0.04, -0.08])
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        matrix @ expected,
        sigma_ev=0.001,
        group=groups,
    )
    endpoints = endpoint_constraints(specification, {0.0: -0.30, 1.0: 1.30})
    amplitude_sum = coefficient_constraint(
        labels,
        {
            "osc0_theta150K_x0": 1.0,
            "osc0_theta150K_x1": 1.0,
        },
        -0.04,
    )
    constraints = combine_constraints(
        endpoints,
        amplitude_sum,
        parameter_count=len(labels),
    )
    assert constraints is not None

    result = fit_linear_gap_model(data, specification, constraints=constraints)

    np.testing.assert_allclose(
        constraints.matrix @ result.coefficients,
        constraints.values,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        constraints.matrix @ result.covariance_known_sigma,
        0.0,
        atol=1.0e-15,
    )
    assert result.free_parameter_count == len(labels) - 3


def test_hansen_temperature_relation_can_be_imposed_by_name() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=3,
        quasiharmonic_degree=1,
    )
    matrix, labels = oscillator_design_matrix(specification, x, temperature)
    expected = np.array([-0.302, 1.93, -0.81, 0.832, 5.35e-4, -1.07e-3])
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        matrix @ expected,
        sigma_ev=0.001,
        group=groups,
    )
    relation = coefficient_constraint(
        labels,
        {"qh_T_x0": 2.0, "qh_T_x1": 1.0},
    )

    result = fit_linear_gap_model(data, specification, constraints=relation)

    np.testing.assert_allclose(result.coefficients, expected, atol=1.0e-12)
    assert 2.0 * result.coefficients[-2] + result.coefficients[-1] == pytest.approx(
        0.0,
        abs=1.0e-14,
    )


def test_leave_one_group_out_never_splits_a_specimen() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=1,
        amplitude_degree=0,
        oscillator_temperatures_k=(120.0,),
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    expected = np.array([-0.25, 1.60, 0.03])
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        matrix @ expected,
        sigma_ev=0.001,
        group=groups,
    )

    result = leave_one_group_out(data, specification)

    np.testing.assert_allclose(result.predictions_ev, data.gap_ev, atol=1.0e-12)
    assert result.metrics.rmse_mev < 1.0e-8
    assert len(result.folds) == 4
    for fold in result.folds:
        held_groups = np.unique(data.group[fold.held_out_indices])
        assert held_groups.tolist() == [fold.name]


def test_named_holdouts_support_temperature_range_splits() -> None:
    x, temperature, groups = _composition_temperature_grid()
    specification = OscillatorBasisSpec(
        static_degree=1,
        amplitude_degree=0,
        oscillator_temperatures_k=(120.0,),
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    data = GapBenchmarkData.from_arrays(
        x,
        temperature,
        matrix @ np.array([-0.25, 1.60, 0.03]),
        sigma_ev=0.001,
        group=groups,
    )
    low = temperature <= 60.0
    high = ~low

    result = named_holdout_cross_validation(
        data,
        specification,
        {"low_temperature": low, "high_temperature": high},
    )

    np.testing.assert_allclose(result.predictions_ev, data.gap_ev, atol=1.0e-12)
    assert {fold.name for fold in result.folds} == {
        "low_temperature",
        "high_temperature",
    }


def test_rank_deficiency_and_invalid_inputs_fail_closed() -> None:
    specification = OscillatorBasisSpec(
        static_degree=1,
        amplitude_degree=0,
        oscillator_temperatures_k=(100.0,),
    )
    data = GapBenchmarkData.from_arrays(
        np.full(5, 0.2),
        np.array([0.0, 20.0, 50.0, 100.0, 200.0]),
        np.linspace(0.0, 0.1, 5),
        sigma_ev=0.001,
        group=["one"] * 5,
    )
    with pytest.raises(np.linalg.LinAlgError, match="rank deficient"):
        fit_linear_gap_model(data, specification)
    with pytest.raises(ValueError, match="positive"):
        OscillatorBasisSpec(1, oscillator_temperatures_k=(0.0,))
    with pytest.raises(ValueError, match="strictly positive"):
        GapBenchmarkData.from_arrays([0.2], [77.0], [0.1], sigma_ev=[0.0])


def test_residual_metrics_are_reported_in_mev() -> None:
    metrics = residual_metrics(
        [0.100, 0.110],
        [0.099, 0.112],
        sigma_ev=[0.001, 0.002],
    )
    assert metrics.mean_signed_mev == pytest.approx(-0.5)
    assert metrics.mae_mev == pytest.approx(1.5)
    assert metrics.rmse_mev == pytest.approx(np.sqrt(2.5))
    assert metrics.max_abs_mev == pytest.approx(2.0)
    assert metrics.weighted_mae_mev == pytest.approx(1.2)
