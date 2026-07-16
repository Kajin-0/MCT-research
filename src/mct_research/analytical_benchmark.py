"""Linear, fixed-scale analytical benchmark models for HgCdTe gaps.

This module intentionally separates two tasks:

1. nonlinear model selection, such as choosing oscillator temperatures;
2. linear coefficient estimation conditional on a declared model specification.

Oscillator temperatures must therefore be fixed before calling the fitter, or selected
inside a properly nested training loop. The module does not infer experimental
validity from synthetic recovery.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
_EPS: Final[float] = np.finfo(float).eps


@dataclass(frozen=True)
class GapBenchmarkData:
    """One-dimensional benchmark observations.

    ``group`` should identify the specimen or another leakage-safe unit. Repeated
    temperatures from the same specimen must share one group label.
    """

    x: FloatArray
    temperature_k: FloatArray
    gap_ev: FloatArray
    sigma_ev: FloatArray
    group: NDArray[np.str_]

    @classmethod
    def from_arrays(
        cls,
        x: ArrayLike,
        temperature_k: ArrayLike,
        gap_ev: ArrayLike,
        *,
        sigma_ev: ArrayLike | None = None,
        group: Sequence[object] | None = None,
    ) -> "GapBenchmarkData":
        composition = np.asarray(x, dtype=float)
        temperature = np.asarray(temperature_k, dtype=float)
        gap = np.asarray(gap_ev, dtype=float)
        composition, temperature, gap = np.broadcast_arrays(
            composition, temperature, gap
        )
        if composition.ndim != 1:
            raise ValueError("benchmark arrays must be one-dimensional")
        if composition.size == 0:
            raise ValueError("benchmark data must contain at least one observation")
        if not (
            np.all(np.isfinite(composition))
            and np.all(np.isfinite(temperature))
            and np.all(np.isfinite(gap))
        ):
            raise ValueError("benchmark values must be finite")
        if np.any((composition < 0.0) | (composition > 1.0)):
            raise ValueError("Cd mole fraction x must lie in [0, 1]")
        if np.any(temperature < 0.0):
            raise ValueError("temperature must be non-negative")

        if sigma_ev is None:
            sigma = np.ones(composition.shape, dtype=float)
        else:
            sigma = np.asarray(sigma_ev, dtype=float)
            sigma = np.broadcast_to(sigma, composition.shape).astype(float, copy=True)
            if not np.all(np.isfinite(sigma)) or np.any(sigma <= 0.0):
                raise ValueError("sigma_ev must be finite and strictly positive")

        if group is None:
            labels = np.asarray(
                [f"observation_{index}" for index in range(composition.size)],
                dtype=str,
            )
        else:
            labels = np.asarray([str(value) for value in group], dtype=str)
            if labels.shape != composition.shape:
                raise ValueError("group must have one label per observation")
            if np.any(labels == ""):
                raise ValueError("group labels must be non-empty")

        return cls(
            x=composition.astype(float, copy=True),
            temperature_k=temperature.astype(float, copy=True),
            gap_ev=gap.astype(float, copy=True),
            sigma_ev=sigma,
            group=labels,
        )

    def subset(self, mask: ArrayLike) -> "GapBenchmarkData":
        selected = np.asarray(mask, dtype=bool)
        if selected.shape != self.x.shape:
            raise ValueError("subset mask has the wrong shape")
        if not np.any(selected):
            raise ValueError("subset cannot be empty")
        return GapBenchmarkData(
            x=self.x[selected].copy(),
            temperature_k=self.temperature_k[selected].copy(),
            gap_ev=self.gap_ev[selected].copy(),
            sigma_ev=self.sigma_ev[selected].copy(),
            group=self.group[selected].copy(),
        )


@dataclass(frozen=True)
class OscillatorBasisSpec:
    """Linear coefficient model with fixed oscillator temperatures.

    The model is

    ``P_static(x) + sum_j P_j(x) b(theta_j, T) + T P_qh(x)``,

    where ``b(theta,T)=2/(exp(theta/T)-1)`` and the optional final term is only a
    benchmark nuisance basis. It is not, by itself, a quasiharmonic derivation.
    """

    static_degree: int
    amplitude_degree: int = 0
    oscillator_temperatures_k: tuple[float, ...] = ()
    quasiharmonic_degree: int | None = None

    def __post_init__(self) -> None:
        if self.static_degree < 0:
            raise ValueError("static_degree must be non-negative")
        if self.amplitude_degree < 0:
            raise ValueError("amplitude_degree must be non-negative")
        if self.quasiharmonic_degree is not None and self.quasiharmonic_degree < 0:
            raise ValueError("quasiharmonic_degree must be non-negative or None")
        temperatures = tuple(float(value) for value in self.oscillator_temperatures_k)
        if any(not np.isfinite(value) or value <= 0.0 for value in temperatures):
            raise ValueError("oscillator temperatures must be finite and positive")
        if len(set(temperatures)) != len(temperatures):
            raise ValueError("oscillator temperatures must be distinct")
        object.__setattr__(self, "oscillator_temperatures_k", temperatures)


@dataclass(frozen=True)
class LinearEqualityConstraints:
    matrix: FloatArray
    values: FloatArray

    @classmethod
    def from_arrays(
        cls,
        matrix: ArrayLike,
        values: ArrayLike,
        *,
        parameter_count: int,
    ) -> "LinearEqualityConstraints":
        constraint_matrix = np.asarray(matrix, dtype=float)
        constraint_values = np.asarray(values, dtype=float)
        if constraint_matrix.ndim == 1:
            constraint_matrix = constraint_matrix.reshape(1, -1)
        if constraint_values.ndim == 0:
            constraint_values = constraint_values.reshape(1)
        if constraint_matrix.ndim != 2 or constraint_values.ndim != 1:
            raise ValueError(
                "constraint matrix and values must be two- and one-dimensional"
            )
        if constraint_matrix.shape != (constraint_values.size, parameter_count):
            raise ValueError("constraint dimensions do not match the parameter count")
        if not (
            np.all(np.isfinite(constraint_matrix))
            and np.all(np.isfinite(constraint_values))
        ):
            raise ValueError("constraints must be finite")
        return cls(constraint_matrix.copy(), constraint_values.copy())


@dataclass(frozen=True)
class ResidualMetrics:
    count: int
    mean_signed_mev: float
    mae_mev: float
    rmse_mev: float
    max_abs_mev: float
    weighted_mean_signed_mev: float
    weighted_mae_mev: float
    weighted_rmse_mev: float


@dataclass(frozen=True)
class LinearGapFit:
    specification: OscillatorBasisSpec
    parameter_labels: tuple[str, ...]
    coefficients: FloatArray
    covariance_known_sigma: FloatArray
    covariance_scaled: FloatArray
    correlation_scaled: FloatArray
    standard_errors_scaled: FloatArray
    fitted_gap_ev: FloatArray
    residual_ev: FloatArray
    metrics: ResidualMetrics
    free_parameter_count: int
    design_rank: int
    singular_values: FloatArray
    condition_number: float
    chi_square: float
    degrees_of_freedom: int
    reduced_chi_square: float

    def predict(self, x: ArrayLike, temperature_k: ArrayLike) -> float | FloatArray:
        matrix, _ = oscillator_design_matrix(self.specification, x, temperature_k)
        values = matrix @ self.coefficients
        scalar_input = (
            np.asarray(x).ndim == 0 and np.asarray(temperature_k).ndim == 0
        )
        return float(values[0]) if values.size == 1 and scalar_input else values


@dataclass(frozen=True)
class HoldoutFold:
    name: str
    held_out_indices: NDArray[np.int64]
    prediction_ev: FloatArray
    metrics: ResidualMetrics
    fit: LinearGapFit


@dataclass(frozen=True)
class CrossValidationResult:
    predictions_ev: FloatArray
    residual_ev: FloatArray
    metrics: ResidualMetrics
    folds: tuple[HoldoutFold, ...]


def bose_occupation_basis(
    theta_k: float,
    temperature_k: ArrayLike,
) -> float | FloatArray:
    """Return ``coth(theta/(2T))-1 = 2/(exp(theta/T)-1)``.

    The value at zero temperature is defined by its limit, zero.
    """

    theta = float(theta_k)
    if not np.isfinite(theta) or theta <= 0.0:
        raise ValueError("theta_k must be finite and positive")
    temperature = np.asarray(temperature_k, dtype=float)
    if not np.all(np.isfinite(temperature)) or np.any(temperature < 0.0):
        raise ValueError("temperature must be finite and non-negative")

    result = np.zeros_like(temperature, dtype=float)
    positive = temperature > 0.0
    ratio = np.empty_like(temperature, dtype=float)
    ratio[positive] = theta / temperature[positive]
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        result[positive] = 2.0 / np.expm1(ratio[positive])
    result[~np.isfinite(result)] = 0.0
    return float(result) if result.ndim == 0 else result


def oscillator_design_matrix(
    specification: OscillatorBasisSpec,
    x: ArrayLike,
    temperature_k: ArrayLike,
) -> tuple[FloatArray, tuple[str, ...]]:
    composition = np.asarray(x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    composition, temperature = np.broadcast_arrays(composition, temperature)
    if not (
        np.all(np.isfinite(composition)) and np.all(np.isfinite(temperature))
    ):
        raise ValueError("composition and temperature must be finite")
    if np.any((composition < 0.0) | (composition > 1.0)):
        raise ValueError("Cd mole fraction x must lie in [0, 1]")
    if np.any(temperature < 0.0):
        raise ValueError("temperature must be non-negative")

    flat_x = composition.ravel()
    flat_temperature = temperature.ravel()
    columns: list[FloatArray] = []
    labels: list[str] = []

    for degree in range(specification.static_degree + 1):
        columns.append(flat_x**degree)
        labels.append(f"static_x{degree}")

    for oscillator_index, theta in enumerate(
        specification.oscillator_temperatures_k
    ):
        thermal = np.asarray(
            bose_occupation_basis(theta, flat_temperature), dtype=float
        )
        for degree in range(specification.amplitude_degree + 1):
            columns.append(thermal * flat_x**degree)
            labels.append(f"osc{oscillator_index}_theta{theta:g}K_x{degree}")

    if specification.quasiharmonic_degree is not None:
        for degree in range(specification.quasiharmonic_degree + 1):
            columns.append(flat_temperature * flat_x**degree)
            labels.append(f"qh_T_x{degree}")

    return np.column_stack(columns), tuple(labels)


def endpoint_constraints(
    specification: OscillatorBasisSpec,
    endpoint_gap_ev: Mapping[float, float],
) -> LinearEqualityConstraints:
    """Constrain declared zero-temperature endpoint or interior compositions."""

    if not endpoint_gap_ev:
        raise ValueError("at least one endpoint constraint is required")
    compositions = np.asarray(list(endpoint_gap_ev.keys()), dtype=float)
    values = np.asarray(list(endpoint_gap_ev.values()), dtype=float)
    matrix, labels = oscillator_design_matrix(specification, compositions, 0.0)
    return LinearEqualityConstraints.from_arrays(
        matrix, values, parameter_count=len(labels)
    )


def coefficient_constraint(
    parameter_labels: Sequence[str],
    terms: Mapping[str, float],
    value: float = 0.0,
) -> LinearEqualityConstraints:
    """Build one equality row from named coefficient weights."""

    labels = tuple(parameter_labels)
    if not terms:
        raise ValueError("at least one named coefficient is required")
    row = np.zeros(len(labels), dtype=float)
    for name, coefficient in terms.items():
        try:
            index = labels.index(name)
        except ValueError as error:
            raise ValueError(f"unknown parameter label: {name}") from error
        row[index] = float(coefficient)
    return LinearEqualityConstraints.from_arrays(
        row, value, parameter_count=len(labels)
    )


def combine_constraints(
    *constraints: LinearEqualityConstraints,
    parameter_count: int,
) -> LinearEqualityConstraints | None:
    if not constraints:
        return None
    for constraint in constraints:
        if constraint.matrix.shape[1] != parameter_count:
            raise ValueError("constraint parameter counts do not match")
    return LinearEqualityConstraints(
        matrix=np.vstack([constraint.matrix for constraint in constraints]),
        values=np.concatenate([constraint.values for constraint in constraints]),
    )


def residual_metrics(
    observed_ev: ArrayLike,
    predicted_ev: ArrayLike,
    *,
    sigma_ev: ArrayLike | None = None,
) -> ResidualMetrics:
    observed = np.asarray(observed_ev, dtype=float)
    predicted = np.asarray(predicted_ev, dtype=float)
    observed, predicted = np.broadcast_arrays(observed, predicted)
    if observed.size == 0 or not (
        np.all(np.isfinite(observed)) and np.all(np.isfinite(predicted))
    ):
        raise ValueError("metric inputs must be non-empty and finite")
    residual_mev = 1000.0 * (observed.ravel() - predicted.ravel())

    if sigma_ev is None:
        weights = np.ones(residual_mev.shape, dtype=float)
    else:
        sigma = np.asarray(sigma_ev, dtype=float)
        sigma = np.broadcast_to(sigma, observed.shape).ravel()
        if not np.all(np.isfinite(sigma)) or np.any(sigma <= 0.0):
            raise ValueError("sigma_ev must be finite and strictly positive")
        weights = 1.0 / sigma**2
    normalized_weights = weights / np.sum(weights)

    return ResidualMetrics(
        count=residual_mev.size,
        mean_signed_mev=float(np.mean(residual_mev)),
        mae_mev=float(np.mean(np.abs(residual_mev))),
        rmse_mev=float(np.sqrt(np.mean(residual_mev**2))),
        max_abs_mev=float(np.max(np.abs(residual_mev))),
        weighted_mean_signed_mev=float(np.sum(normalized_weights * residual_mev)),
        weighted_mae_mev=float(np.sum(normalized_weights * np.abs(residual_mev))),
        weighted_rmse_mev=float(
            np.sqrt(np.sum(normalized_weights * residual_mev**2))
        ),
    )


def _constraint_parameterization(
    parameter_count: int,
    constraints: LinearEqualityConstraints | None,
) -> tuple[FloatArray, FloatArray]:
    if constraints is None:
        return np.zeros(parameter_count, dtype=float), np.eye(parameter_count)

    matrix = constraints.matrix
    values = constraints.values
    if matrix.shape[1] != parameter_count:
        raise ValueError("constraints have the wrong parameter count")

    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    tolerance = (
        max(matrix.shape) * _EPS * singular_values[0]
        if singular_values.size and singular_values[0] > 0.0
        else 0.0
    )
    rank = int(np.sum(singular_values > tolerance))
    particular = np.linalg.lstsq(matrix, values, rcond=None)[0]
    residual = matrix @ particular - values
    scale = max(1.0, float(np.linalg.norm(values)))
    if np.linalg.norm(residual) > 1.0e-10 * scale:
        raise ValueError("equality constraints are inconsistent")
    null_space = vh[rank:].T.copy()
    return particular, null_space


def fit_linear_gap_model(
    data: GapBenchmarkData,
    specification: OscillatorBasisSpec,
    *,
    constraints: LinearEqualityConstraints | None = None,
) -> LinearGapFit:
    matrix, labels = oscillator_design_matrix(
        specification, data.x, data.temperature_k
    )
    parameter_count = matrix.shape[1]
    particular, null_space = _constraint_parameterization(
        parameter_count, constraints
    )
    free_count = null_space.shape[1]

    weighted_matrix = matrix / data.sigma_ev[:, None]
    weighted_target = data.gap_ev / data.sigma_ev
    shifted_target = weighted_target - weighted_matrix @ particular
    reduced_matrix = weighted_matrix @ null_space

    if free_count:
        singular_values = np.linalg.svd(reduced_matrix, compute_uv=False)
        tolerance = (
            max(reduced_matrix.shape) * _EPS * singular_values[0]
            if singular_values.size and singular_values[0] > 0.0
            else 0.0
        )
        rank = int(np.sum(singular_values > tolerance))
        if rank < free_count:
            raise np.linalg.LinAlgError(
                "weighted design is rank deficient for the free parameters"
            )
        reduced_coefficients = np.linalg.lstsq(
            reduced_matrix, shifted_target, rcond=None
        )[0]
        coefficients = particular + null_space @ reduced_coefficients
        normal_inverse = np.linalg.inv(reduced_matrix.T @ reduced_matrix)
        covariance_known = null_space @ normal_inverse @ null_space.T
        condition_number = float(singular_values[0] / singular_values[-1])
    else:
        singular_values = np.empty(0, dtype=float)
        rank = 0
        coefficients = particular
        covariance_known = np.zeros(
            (parameter_count, parameter_count), dtype=float
        )
        condition_number = 1.0

    fitted = matrix @ coefficients
    residual = data.gap_ev - fitted
    normalized_residual = residual / data.sigma_ev
    chi_square = float(normalized_residual @ normalized_residual)
    degrees_of_freedom = data.gap_ev.size - free_count
    reduced_chi_square = (
        chi_square / degrees_of_freedom
        if degrees_of_freedom > 0
        else float("nan")
    )
    covariance_scale = (
        reduced_chi_square if np.isfinite(reduced_chi_square) else 1.0
    )
    covariance_scaled = covariance_known * covariance_scale
    standard_errors = np.sqrt(np.clip(np.diag(covariance_scaled), 0.0, None))
    denominator = np.outer(standard_errors, standard_errors)
    correlation = np.divide(
        covariance_scaled,
        denominator,
        out=np.zeros_like(covariance_scaled),
        where=denominator > 0.0,
    )
    positive_error = standard_errors > 0.0
    correlation[np.diag_indices_from(correlation)] = positive_error.astype(float)

    return LinearGapFit(
        specification=specification,
        parameter_labels=labels,
        coefficients=coefficients,
        covariance_known_sigma=covariance_known,
        covariance_scaled=covariance_scaled,
        correlation_scaled=correlation,
        standard_errors_scaled=standard_errors,
        fitted_gap_ev=fitted,
        residual_ev=residual,
        metrics=residual_metrics(data.gap_ev, fitted, sigma_ev=data.sigma_ev),
        free_parameter_count=free_count,
        design_rank=rank,
        singular_values=singular_values,
        condition_number=condition_number,
        chi_square=chi_square,
        degrees_of_freedom=degrees_of_freedom,
        reduced_chi_square=reduced_chi_square,
    )


def named_holdout_cross_validation(
    data: GapBenchmarkData,
    specification: OscillatorBasisSpec,
    holdouts: Mapping[str, ArrayLike],
    *,
    constraints: LinearEqualityConstraints | None = None,
    require_partition: bool = True,
) -> CrossValidationResult:
    """Fit on each mask complement and predict its held-out observations."""

    if not holdouts:
        raise ValueError("at least one holdout mask is required")
    predictions = np.full(data.gap_ev.shape, np.nan, dtype=float)
    assigned = np.zeros(data.gap_ev.shape, dtype=int)
    folds: list[HoldoutFold] = []

    for name, raw_mask in holdouts.items():
        holdout = np.asarray(raw_mask, dtype=bool)
        if holdout.shape != data.gap_ev.shape:
            raise ValueError(f"holdout {name!r} has the wrong shape")
        if not np.any(holdout) or np.all(holdout):
            raise ValueError(f"holdout {name!r} must select some but not all points")
        fit = fit_linear_gap_model(
            data.subset(~holdout), specification, constraints=constraints
        )
        matrix, _ = oscillator_design_matrix(
            specification, data.x[holdout], data.temperature_k[holdout]
        )
        prediction = matrix @ fit.coefficients
        indices = np.flatnonzero(holdout)
        predictions[indices] = prediction
        assigned[indices] += 1
        folds.append(
            HoldoutFold(
                name=str(name),
                held_out_indices=indices.astype(np.int64),
                prediction_ev=prediction,
                metrics=residual_metrics(
                    data.gap_ev[holdout],
                    prediction,
                    sigma_ev=data.sigma_ev[holdout],
                ),
                fit=fit,
            )
        )

    if np.any(assigned > 1):
        raise ValueError("holdout masks overlap")
    if require_partition and np.any(assigned != 1):
        raise ValueError("holdout masks must form a complete partition")
    evaluated = assigned == 1
    if not np.any(evaluated):
        raise ValueError("no observations were evaluated")

    residual = np.full(data.gap_ev.shape, np.nan, dtype=float)
    residual[evaluated] = data.gap_ev[evaluated] - predictions[evaluated]
    return CrossValidationResult(
        predictions_ev=predictions,
        residual_ev=residual,
        metrics=residual_metrics(
            data.gap_ev[evaluated],
            predictions[evaluated],
            sigma_ev=data.sigma_ev[evaluated],
        ),
        folds=tuple(folds),
    )


def leave_one_group_out(
    data: GapBenchmarkData,
    specification: OscillatorBasisSpec,
    *,
    constraints: LinearEqualityConstraints | None = None,
) -> CrossValidationResult:
    groups = np.unique(data.group)
    if groups.size < 2:
        raise ValueError("leave-one-group-out requires at least two groups")
    holdouts = {str(group): data.group == group for group in groups}
    return named_holdout_cross_validation(
        data,
        specification,
        holdouts,
        constraints=constraints,
        require_partition=True,
    )
