from __future__ import annotations

import itertools

import numpy as np
import pytest

from mct_research.spatial_disorder_allocation import (
    endpoint_d_optimal_allocation,
    endpoint_integer_d_efficiency,
    gaussian_allocation_diagnostics,
    gaussian_log_correlation_sensitivity,
    optimize_three_scale_allocation,
)


def test_endpoint_integer_allocation_maximizes_two_scale_determinant() -> None:
    for total in range(2, 31):
        selected = endpoint_d_optimal_allocation(total)
        selected_product = int(selected[0] * selected[1])
        all_products = [lower * (total - lower) for lower in range(1, total)]
        assert selected_product == max(all_products)
        assert abs(int(selected[0]) - int(selected[1])) <= 1
        assert endpoint_integer_d_efficiency(total) == pytest.approx(
            4.0 * selected_product / total**2
        )


def test_log_sensitivity_has_correct_limits_and_monotonicity() -> None:
    values = gaussian_log_correlation_sensitivity(
        [0.0, 1.0e-6, 0.1, 1.0, 10.0, 1.0e6],
        1.0,
    )
    assert values[0] == 0.0
    assert np.all(np.diff(values) > 0.0)
    assert values[-1] == pytest.approx(2.0, rel=1.0e-12)


def test_weighted_variance_fisher_identity_and_permutation_invariance() -> None:
    scales = np.array([0.1, 1.0, 2.0])
    repeats = np.array([11, 7, 12])
    reference = gaussian_allocation_diagnostics(
        0.01,
        1.0,
        scales,
        repeats,
        single_repeat_relative_standard_deviation=0.03,
    )
    expected_determinant = (
        reference.total_repeats
        * reference.weighted_sensitivity_sum_of_squares
        / 0.03**4
    )
    assert reference.fisher_determinant == pytest.approx(
        expected_determinant,
        rel=3.0e-12,
    )

    for permutation in itertools.permutations(range(3)):
        permuted = gaussian_allocation_diagnostics(
            0.01,
            1.0,
            scales[list(permutation)],
            repeats[list(permutation)],
            single_repeat_relative_standard_deviation=0.03,
        )
        assert permuted.fisher_matrix == pytest.approx(reference.fisher_matrix)
        assert permuted.fisher_determinant == pytest.approx(
            reference.fisher_determinant
        )
        assert permuted.d_efficiency == pytest.approx(reference.d_efficiency)
        assert permuted.parameter_covariance_relative_scale == pytest.approx(
            reference.parameter_covariance_relative_scale
        )


def test_endpoint_design_has_unit_d_efficiency_and_unequal_loss() -> None:
    for total in (10, 11, 30, 31):
        optimal_counts = endpoint_d_optimal_allocation(total)
        optimal = gaussian_allocation_diagnostics(
            0.01,
            2.0,
            [0.2, 20.0],
            optimal_counts,
            single_repeat_relative_standard_deviation=0.04,
        )
        assert optimal.d_efficiency == pytest.approx(1.0, abs=2.0e-14)

    unequal = gaussian_allocation_diagnostics(
        0.01,
        2.0,
        [0.2, 20.0],
        [3, 27],
        single_repeat_relative_standard_deviation=0.04,
    )
    assert unequal.d_efficiency == pytest.approx(4.0 * 3.0 * 27.0 / 30.0**2)


def test_common_scale_calibration_adds_only_absolute_length_floor() -> None:
    relative = gaussian_allocation_diagnostics(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        [11, 7, 12],
        single_repeat_relative_standard_deviation=0.03,
    )
    calibrated = gaussian_allocation_diagnostics(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        [11, 7, 12],
        single_repeat_relative_standard_deviation=0.03,
        common_log_scale_standard_deviation=0.05,
    )
    assert calibrated.parameter_covariance_absolute_scale is not None
    expected = np.array(relative.parameter_covariance_relative_scale, copy=True)
    expected[1, 1] += 0.05**2
    assert calibrated.parameter_covariance_absolute_scale == pytest.approx(
        expected,
        rel=5.0e-11,
        abs=5.0e-13,
    )
    assert calibrated.log_point_variance_standard_deviation == pytest.approx(
        relative.log_point_variance_standard_deviation
    )
    assert (
        calibrated.log_correlation_length_absolute_standard_deviation
        > calibrated.log_correlation_length_relative_standard_deviation
    )


@pytest.mark.parametrize(
    ("total", "expected_repeats", "expected_efficiency", "expected_worst_z"),
    [
        (12, (5, 3, 4), 0.8082031519902514, 2.4024189856907174),
        (30, (11, 7, 12), 0.8006806489908984, 3.7816460279252246),
        (60, (24, 15, 21), 0.8045022330261747, 5.403954866662064),
    ],
)
def test_three_scale_optimizer_reproduces_controlled_designs(
    total: int,
    expected_repeats: tuple[int, int, int],
    expected_efficiency: float,
    expected_worst_z: float,
) -> None:
    result = optimize_three_scale_allocation(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        total,
        single_repeat_relative_standard_deviation=0.03,
        minimum_middle_repeats=1,
        minimum_d_efficiency=0.8,
        common_log_scale_standard_deviation=0.02,
    )
    recommended = result.recommended
    assert tuple(int(value) for value in recommended.allocation.repeats) == expected_repeats
    assert recommended.allocation.d_efficiency == pytest.approx(
        expected_efficiency,
        rel=3.0e-12,
    )
    assert recommended.worst_case_absolute_standardized_residual == pytest.approx(
        expected_worst_z,
        rel=3.0e-11,
    )
    assert recommended.pareto_optimal
    assert recommended.allocation.parameter_covariance_absolute_scale is not None
    assert len(result.pareto_front) > 1
    assert all(design.pareto_optimal for design in result.pareto_front)
    assert all(
        design.allocation.d_efficiency + 1.0e-14 >= 0.8
        for design in [recommended]
    )


def test_optimizer_is_invariant_to_common_length_unit_change() -> None:
    first = optimize_three_scale_allocation(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        30,
        single_repeat_relative_standard_deviation=0.03,
        minimum_d_efficiency=0.8,
    )
    second = optimize_three_scale_allocation(
        0.01,
        1000.0,
        [100.0, 1000.0, 2000.0],
        30,
        single_repeat_relative_standard_deviation=0.03,
        minimum_d_efficiency=0.8,
    )
    assert second.recommended.allocation.repeats == pytest.approx(
        first.recommended.allocation.repeats
    )
    assert second.recommended.allocation.d_efficiency == pytest.approx(
        first.recommended.allocation.d_efficiency
    )
    assert second.recommended.standardized_family_residuals == pytest.approx(
        first.recommended.standardized_family_residuals,
        rel=2.0e-12,
    )


def test_efficiency_floor_controls_precision_family_tradeoff() -> None:
    strict = optimize_three_scale_allocation(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        30,
        single_repeat_relative_standard_deviation=0.03,
        minimum_d_efficiency=0.9,
    )
    permissive = optimize_three_scale_allocation(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        30,
        single_repeat_relative_standard_deviation=0.03,
        minimum_d_efficiency=0.6,
    )
    assert strict.recommended.allocation.d_efficiency >= 0.9
    assert permissive.recommended.allocation.d_efficiency >= 0.6
    assert (
        permissive.recommended.worst_case_absolute_standardized_residual
        >= strict.recommended.worst_case_absolute_standardized_residual
    )


@pytest.mark.parametrize(
    "operation",
    [
        lambda: endpoint_d_optimal_allocation(1),
        lambda: endpoint_d_optimal_allocation(2.5),
        lambda: gaussian_log_correlation_sensitivity([], 1.0),
        lambda: gaussian_log_correlation_sensitivity([1.0], 0.0),
        lambda: gaussian_allocation_diagnostics(
            0.01,
            1.0,
            [0.1, 1.0],
            [1, 0],
            single_repeat_relative_standard_deviation=0.03,
        ),
        lambda: gaussian_allocation_diagnostics(
            0.01,
            1.0,
            [0.1, 0.1],
            [1, 1],
            single_repeat_relative_standard_deviation=0.03,
        ),
        lambda: optimize_three_scale_allocation(
            0.01,
            1.0,
            [0.1, 1.0, 2.0],
            2,
            single_repeat_relative_standard_deviation=0.03,
        ),
        lambda: optimize_three_scale_allocation(
            0.01,
            1.0,
            [0.1, 1.0, 2.0],
            30,
            single_repeat_relative_standard_deviation=0.03,
            minimum_d_efficiency=1.1,
        ),
    ],
)
def test_invalid_inputs(operation) -> None:
    with pytest.raises(ValueError):
        operation()
