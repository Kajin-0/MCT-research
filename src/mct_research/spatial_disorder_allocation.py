"""Optimal repeat allocation for multiscale spatial-disorder measurements.

The declared local model is the isotropic two-dimensional Gaussian benchmark

``V(s) = A / (1 + 2 s**2 / xi**2)``.

Each scale is measured with an independent mean whose relative standard
deviation is ``single_repeat_relative_standard_deviation / sqrt(n_i)``.  Under
this log-homoscedastic model, the Fisher rows for ``(log A, log xi)`` are
proportional to ``(1, g_i)`` with

``g_i = 4 (s_i/xi)**2 / (1 + 2 (s_i/xi)**2)``.

The module proves and implements the endpoint D-optimal allocation, quantifies
integer and unequal-allocation losses, and constructs a three-scale Pareto
tradeoff between Gaussian-parameter precision and covariance-family
falsification.  It reuses the established R04 covariance-family and calibration
APIs and does not define a new covariance model.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, isfinite
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_calibration import gaussian_common_probe_scale_calibration
from .spatial_disorder_covariance_families import (
    SUPPORTED_MATERN_SMOOTHNESS,
    gaussian_three_scale_falsification,
    matern_gaussian_probe_variance_2d,
)
from .spatial_disorder_inference import (
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_variance,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]
IntArray = NDArray[np.int64]


def _positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _read_only_float(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _read_only_int(value: ArrayLike) -> IntArray:
    result = np.array(value, dtype=np.int64, copy=True)
    result.setflags(write=False)
    return result


def _validated_scales_and_repeats(
    probe_sigmas: ArrayLike,
    repeats: ArrayLike,
    *,
    minimum_count: int = 2,
) -> tuple[FloatArray, IntArray]:
    scales = np.asarray(probe_sigmas, dtype=float)
    counts_raw = np.asarray(repeats)
    if scales.ndim != 1 or scales.size < minimum_count:
        raise ValueError(f"at least {minimum_count} probe scales are required")
    if counts_raw.ndim != 1 or counts_raw.shape != scales.shape:
        raise ValueError("repeats must match probe_sigmas")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    if np.unique(scales).size != scales.size:
        raise ValueError("probe_sigmas must be distinct")
    if not np.issubdtype(counts_raw.dtype, np.integer):
        if not np.all(np.isfinite(counts_raw)) or not np.all(
            counts_raw == np.floor(counts_raw)
        ):
            raise ValueError("repeats must contain integers")
    counts = np.asarray(counts_raw, dtype=np.int64)
    if np.any(counts <= 0):
        raise ValueError("every declared scale must receive at least one repeat")
    return _read_only_float(scales), _read_only_int(counts)


def gaussian_log_correlation_sensitivity(
    probe_sigmas: ArrayLike,
    correlation_length: float,
) -> FloatArray:
    r"""Return ``d log(V) / d log(xi)`` for the 2D Gaussian benchmark.

    .. math::

       g(s/\xi)=\frac{4(s/\xi)^2}{1+2(s/\xi)^2}.
    """

    xi = _positive_scalar("correlation_length", correlation_length)
    scales = np.asarray(probe_sigmas, dtype=float)
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("probe_sigmas must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    ratio_squared = (scales / xi) ** 2
    return _read_only_float(4.0 * ratio_squared / (1.0 + 2.0 * ratio_squared))


@dataclass(frozen=True)
class GaussianAllocationDiagnostics:
    """Parameter-information diagnostics for one repeat allocation."""

    probe_sigmas: FloatArray
    repeats: IntArray
    total_repeats: int
    predicted_variances: FloatArray
    log_correlation_sensitivities: FloatArray
    weighted_mean_sensitivity: float
    weighted_sensitivity_sum_of_squares: float
    fisher_matrix: FloatMatrix
    fisher_determinant: float
    endpoint_optimal_fisher_determinant: float
    d_efficiency: float
    parameter_covariance_relative_scale: FloatMatrix
    parameter_covariance_absolute_scale: FloatMatrix | None
    log_point_variance_standard_deviation: float
    log_correlation_length_relative_standard_deviation: float
    log_correlation_length_absolute_standard_deviation: float | None
    parameter_correlation: float
    fisher_condition_number: float
    common_log_scale_standard_deviation: float | None


@dataclass(frozen=True)
class ThreeScaleAllocationDiagnostics:
    """Three-scale precision and covariance-family-falsification diagnostics."""

    allocation: GaussianAllocationDiagnostics
    matern_smoothness: FloatArray
    standardized_family_residuals: FloatArray
    worst_case_absolute_standardized_residual: float
    mean_absolute_standardized_residual: float
    pareto_optimal: bool


@dataclass(frozen=True)
class ThreeScaleOptimizationResult:
    """Deterministic constrained three-scale allocation result."""

    probe_sigmas: FloatArray
    total_repeats: int
    minimum_middle_repeats: int
    minimum_d_efficiency: float
    recommended: ThreeScaleAllocationDiagnostics
    pareto_front: tuple[ThreeScaleAllocationDiagnostics, ...]
    all_designs: tuple[ThreeScaleAllocationDiagnostics, ...]


def _endpoint_integer_counts(total_repeats: int) -> tuple[int, int]:
    if isinstance(total_repeats, bool) or int(total_repeats) != total_repeats:
        raise ValueError("total_repeats must be an integer")
    total = int(total_repeats)
    if total < 2:
        raise ValueError("total_repeats must be at least two")
    lower = total // 2
    return lower, total - lower


def endpoint_d_optimal_allocation(total_repeats: int) -> IntArray:
    """Return the integer D-optimal allocation on two endpoint scales.

    Continuous D-optimality assigns equal weight to both endpoint
    sensitivities.  Integer allocation therefore differs by at most one repeat.
    """

    lower, upper = _endpoint_integer_counts(total_repeats)
    return _read_only_int([lower, upper])


def endpoint_integer_d_efficiency(total_repeats: int) -> float:
    """Return the determinant efficiency caused only by integer rounding."""

    lower, upper = _endpoint_integer_counts(total_repeats)
    total = lower + upper
    return float(4.0 * lower * upper / (total * total))


def gaussian_allocation_diagnostics(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    repeats: ArrayLike,
    *,
    single_repeat_relative_standard_deviation: float,
    common_log_scale_standard_deviation: float | None = None,
) -> GaussianAllocationDiagnostics:
    """Return exact local Fisher diagnostics for a repeat allocation.

    For homoscedastic relative errors, the Fisher determinant satisfies

    ``det(F) = N * sum_i n_i (g_i-g_bar)**2 / sigma_y**4``.

    The D-efficiency is measured against the equal-weight endpoint design over
    the minimum and maximum declared scales with the same integer budget.
    """

    variance = _positive_scalar("point_variance", point_variance)
    xi = _positive_scalar("correlation_length", correlation_length)
    relative = _positive_scalar(
        "single_repeat_relative_standard_deviation",
        single_repeat_relative_standard_deviation,
    )
    scales, counts = _validated_scales_and_repeats(probe_sigmas, repeats)
    total = int(np.sum(counts))
    predicted = gaussian_multiscale_variance(variance, xi, scales)
    observation_standard_deviations = (
        relative * np.asarray(predicted) / np.sqrt(np.asarray(counts, dtype=float))
    )
    fisher_diagnostics = gaussian_multiscale_fisher_information(
        variance,
        xi,
        scales,
        observation_standard_deviations=observation_standard_deviations,
    )
    if fisher_diagnostics.rank != 2 or fisher_diagnostics.parameter_covariance is None:
        raise ValueError("allocation does not identify both Gaussian parameters")

    sensitivities = gaussian_log_correlation_sensitivity(scales, xi)
    weighted_mean = float(np.dot(counts, sensitivities) / total)
    weighted_sum_of_squares = float(
        np.dot(counts, (np.asarray(sensitivities) - weighted_mean) ** 2)
    )
    determinant_identity = total * weighted_sum_of_squares / relative**4
    fisher_matrix = np.asarray(fisher_diagnostics.fisher_matrix)
    determinant = float(np.linalg.det(fisher_matrix))
    if not np.isclose(determinant, determinant_identity, rtol=3.0e-12, atol=1.0e-13):
        raise ArithmeticError("Fisher determinant disagrees with weighted-variance identity")

    endpoint_counts = endpoint_d_optimal_allocation(total)
    endpoint_sensitivities = gaussian_log_correlation_sensitivity(
        [float(np.min(scales)), float(np.max(scales))],
        xi,
    )
    sensitivity_span = float(endpoint_sensitivities[1] - endpoint_sensitivities[0])
    endpoint_determinant = float(
        endpoint_counts[0]
        * endpoint_counts[1]
        * sensitivity_span**2
        / relative**4
    )
    d_efficiency = determinant / endpoint_determinant
    if d_efficiency > 1.0 and d_efficiency < 1.0 + 5.0e-12:
        d_efficiency = 1.0
    if not 0.0 < d_efficiency <= 1.0:
        raise ArithmeticError("D-efficiency left its physical interval")

    relative_covariance = np.asarray(fisher_diagnostics.parameter_covariance)
    absolute_covariance: FloatMatrix | None
    absolute_log_xi_std: float | None
    common_scale_std: float | None
    if common_log_scale_standard_deviation is None:
        absolute_covariance = None
        absolute_log_xi_std = None
        common_scale_std = None
    else:
        common_scale_std = _positive_scalar(
            "common_log_scale_standard_deviation",
            common_log_scale_standard_deviation,
        )
        calibrated = gaussian_common_probe_scale_calibration(
            variance,
            xi,
            scales,
            log_scale_standard_deviation=common_scale_std,
            observation_standard_deviations=observation_standard_deviations,
        )
        if calibrated.rank != 2 or calibrated.parameter_covariance is None:
            raise ValueError("calibrated allocation does not identify both parameters")
        absolute_covariance = np.asarray(calibrated.parameter_covariance)
        expected = np.array(relative_covariance, copy=True)
        expected[1, 1] += common_scale_std**2
        if not np.allclose(
            absolute_covariance,
            expected,
            rtol=5.0e-11,
            atol=5.0e-13,
        ):
            raise ArithmeticError("common calibration floor identity failed")
        absolute_log_xi_std = float(np.sqrt(absolute_covariance[1, 1]))

    return GaussianAllocationDiagnostics(
        probe_sigmas=_read_only_float(scales),
        repeats=_read_only_int(counts),
        total_repeats=total,
        predicted_variances=_read_only_float(predicted),
        log_correlation_sensitivities=_read_only_float(sensitivities),
        weighted_mean_sensitivity=weighted_mean,
        weighted_sensitivity_sum_of_squares=weighted_sum_of_squares,
        fisher_matrix=_read_only_float(fisher_matrix),
        fisher_determinant=determinant,
        endpoint_optimal_fisher_determinant=endpoint_determinant,
        d_efficiency=float(d_efficiency),
        parameter_covariance_relative_scale=_read_only_float(relative_covariance),
        parameter_covariance_absolute_scale=(
            None if absolute_covariance is None else _read_only_float(absolute_covariance)
        ),
        log_point_variance_standard_deviation=float(
            np.sqrt(relative_covariance[0, 0])
        ),
        log_correlation_length_relative_standard_deviation=float(
            np.sqrt(relative_covariance[1, 1])
        ),
        log_correlation_length_absolute_standard_deviation=absolute_log_xi_std,
        parameter_correlation=float(fisher_diagnostics.parameter_correlation),
        fisher_condition_number=float(fisher_diagnostics.condition_number),
        common_log_scale_standard_deviation=common_scale_std,
    )


def _family_residuals(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: FloatArray,
    repeats: IntArray,
    relative_standard_deviation: float,
    smoothness_values: Iterable[float],
) -> tuple[FloatArray, FloatArray]:
    smoothness = np.asarray(tuple(smoothness_values), dtype=float)
    if smoothness.ndim != 1 or smoothness.size == 0:
        raise ValueError("matern_smoothness_values must be non-empty")
    residuals = []
    for value in smoothness:
        variances = matern_gaussian_probe_variance_2d(
            point_variance,
            correlation_length,
            probe_sigmas,
            float(value),
        )
        standard_deviations = (
            relative_standard_deviation
            * np.asarray(variances)
            / np.sqrt(np.asarray(repeats, dtype=float))
        )
        diagnostic = gaussian_three_scale_falsification(
            probe_sigmas,
            variances,
            variance_standard_deviations=standard_deviations,
        )
        if diagnostic.standardized_reciprocal_residual is None:
            raise ArithmeticError("three-scale residual standardization failed")
        residuals.append(float(diagnostic.standardized_reciprocal_residual))
    return _read_only_float(smoothness), _read_only_float(residuals)


def _mark_pareto_front(
    designs: list[ThreeScaleAllocationDiagnostics],
) -> tuple[ThreeScaleAllocationDiagnostics, ...]:
    flags = []
    for index, design in enumerate(designs):
        dominated = False
        for other_index, other in enumerate(designs):
            if index == other_index:
                continue
            no_worse = (
                other.allocation.d_efficiency >= design.allocation.d_efficiency
                and other.worst_case_absolute_standardized_residual
                >= design.worst_case_absolute_standardized_residual
            )
            strictly_better = (
                other.allocation.d_efficiency > design.allocation.d_efficiency
                or other.worst_case_absolute_standardized_residual
                > design.worst_case_absolute_standardized_residual
            )
            if no_worse and strictly_better:
                dominated = True
                break
        flags.append(not dominated)

    marked = []
    for design, flag in zip(designs, flags, strict=True):
        marked.append(
            ThreeScaleAllocationDiagnostics(
                allocation=design.allocation,
                matern_smoothness=design.matern_smoothness,
                standardized_family_residuals=design.standardized_family_residuals,
                worst_case_absolute_standardized_residual=(
                    design.worst_case_absolute_standardized_residual
                ),
                mean_absolute_standardized_residual=(
                    design.mean_absolute_standardized_residual
                ),
                pareto_optimal=flag,
            )
        )
    return tuple(marked)


def optimize_three_scale_allocation(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    total_repeats: int,
    *,
    single_repeat_relative_standard_deviation: float,
    minimum_middle_repeats: int = 1,
    minimum_d_efficiency: float = 0.8,
    common_log_scale_standard_deviation: float | None = None,
    matern_smoothness_values: Iterable[float] = SUPPORTED_MATERN_SMOOTHNESS,
) -> ThreeScaleOptimizationResult:
    """Optimize a three-scale precision/falsification compromise.

    Every scale receives at least one repeat and the middle scale receives at
    least ``minimum_middle_repeats``.  Among allocations meeting the declared
    D-efficiency floor, the recommendation maximizes the minimum absolute
    standardized residual over the selected Matérn alternatives.  Ties prefer
    higher D-efficiency and then lexicographically smaller repeat vectors.
    """

    variance = _positive_scalar("point_variance", point_variance)
    xi = _positive_scalar("correlation_length", correlation_length)
    relative = _positive_scalar(
        "single_repeat_relative_standard_deviation",
        single_repeat_relative_standard_deviation,
    )
    scales = np.asarray(probe_sigmas, dtype=float)
    if scales.shape != (3,) or not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must contain exactly three finite non-negative scales")
    if np.unique(scales).size != 3 or not np.all(np.diff(scales) > 0.0):
        raise ValueError("probe_sigmas must be strictly increasing")
    if isinstance(total_repeats, bool) or int(total_repeats) != total_repeats:
        raise ValueError("total_repeats must be an integer")
    total = int(total_repeats)
    if isinstance(minimum_middle_repeats, bool) or int(minimum_middle_repeats) != minimum_middle_repeats:
        raise ValueError("minimum_middle_repeats must be an integer")
    minimum_middle = int(minimum_middle_repeats)
    if minimum_middle < 1 or total < minimum_middle + 2:
        raise ValueError("budget is insufficient for the minimum three-scale allocation")
    efficiency_floor = float(minimum_d_efficiency)
    if not isfinite(efficiency_floor) or not 0.0 < efficiency_floor <= 1.0:
        raise ValueError("minimum_d_efficiency must lie in (0, 1]")

    unmarked: list[ThreeScaleAllocationDiagnostics] = []
    for middle in range(minimum_middle, total - 1):
        remaining = total - middle
        for lower in range(1, remaining):
            upper = remaining - lower
            counts = np.array([lower, middle, upper], dtype=np.int64)
            allocation = gaussian_allocation_diagnostics(
                variance,
                xi,
                scales,
                counts,
                single_repeat_relative_standard_deviation=relative,
                common_log_scale_standard_deviation=(
                    common_log_scale_standard_deviation
                ),
            )
            smoothness, residuals = _family_residuals(
                variance,
                xi,
                _read_only_float(scales),
                _read_only_int(counts),
                relative,
                matern_smoothness_values,
            )
            absolute = np.abs(np.asarray(residuals))
            unmarked.append(
                ThreeScaleAllocationDiagnostics(
                    allocation=allocation,
                    matern_smoothness=smoothness,
                    standardized_family_residuals=residuals,
                    worst_case_absolute_standardized_residual=float(np.min(absolute)),
                    mean_absolute_standardized_residual=float(np.mean(absolute)),
                    pareto_optimal=False,
                )
            )

    designs = _mark_pareto_front(unmarked)
    feasible = [
        design
        for design in designs
        if design.allocation.d_efficiency + 1.0e-14 >= efficiency_floor
    ]
    if not feasible:
        raise ValueError("no three-scale allocation meets the D-efficiency floor")
    recommended = max(
        feasible,
        key=lambda design: (
            design.worst_case_absolute_standardized_residual,
            design.allocation.d_efficiency,
            tuple(-int(value) for value in design.allocation.repeats),
        ),
    )
    pareto = tuple(
        sorted(
            (design for design in designs if design.pareto_optimal),
            key=lambda design: (
                design.allocation.d_efficiency,
                design.worst_case_absolute_standardized_residual,
                tuple(int(value) for value in design.allocation.repeats),
            ),
        )
    )
    all_sorted = tuple(
        sorted(
            designs,
            key=lambda design: tuple(int(value) for value in design.allocation.repeats),
        )
    )
    return ThreeScaleOptimizationResult(
        probe_sigmas=_read_only_float(scales),
        total_repeats=total,
        minimum_middle_repeats=minimum_middle,
        minimum_d_efficiency=efficiency_floor,
        recommended=recommended,
        pareto_front=pareto,
        all_designs=all_sorted,
    )
