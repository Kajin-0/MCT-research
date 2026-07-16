"""First-order composition-uncertainty propagation for HgCdTe gap benchmarks.

The implementation is deliberately narrower than a full latent-composition model.
It linearizes each analytical model about the reported composition and propagates
Gaussian composition uncertainty through the analytic derivative ``dE/dx``.
Repeated temperatures from one specimen can share one correlated composition
perturbation through the existing leakage-safe ``group`` label.

No source offset, free composition shift, or experimental-validity claim is
introduced by this module.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final, Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .analytical_benchmark import (
    GapBenchmarkData,
    LinearEqualityConstraints,
    LinearGapFit,
    OscillatorBasisSpec,
    ResidualMetrics,
    fit_linear_gap_model,
    oscillator_design_matrix,
    residual_metrics,
)

FloatArray = NDArray[np.float64]
_EPS: Final[float] = np.finfo(float).eps
CompositionMode = Literal["independent", "shared_group"]


@dataclass(frozen=True)
class CompositionAwareGapData:
    """Benchmark observations with composition and provenance metadata.

    ``sigma_x`` is one standard uncertainty in Cd mole fraction. In
    ``shared_group`` mode, all observations with one group label must represent
    one specimen and therefore carry the same reported ``x`` and ``sigma_x``.

    ``measurement_class`` is intentionally explicit. Mixed classes are rejected
    by default by the fitter so optical, electrical, ellipsometric, or other gap
    observables are not pooled accidentally.
    """

    benchmark: GapBenchmarkData
    sigma_x: FloatArray
    source: NDArray[np.str_]
    measurement_class: NDArray[np.str_]

    def __post_init__(self) -> None:
        shape = self.benchmark.x.shape
        sigma_x = np.asarray(self.sigma_x, dtype=float)
        if sigma_x.shape != shape:
            raise ValueError("sigma_x must have one value per observation")
        if not np.all(np.isfinite(sigma_x)) or np.any(sigma_x < 0.0):
            raise ValueError("sigma_x must be finite and non-negative")

        source = np.asarray(self.source, dtype=str)
        measurement_class = np.asarray(self.measurement_class, dtype=str)
        if source.shape != shape:
            raise ValueError("source must have one label per observation")
        if measurement_class.shape != shape:
            raise ValueError(
                "measurement_class must have one label per observation"
            )
        if np.any(source == "") or np.any(measurement_class == ""):
            raise ValueError("source and measurement_class labels must be non-empty")

        object.__setattr__(self, "sigma_x", sigma_x.astype(float, copy=True))
        object.__setattr__(self, "source", source.copy())
        object.__setattr__(self, "measurement_class", measurement_class.copy())

    @classmethod
    def from_arrays(
        cls,
        x: ArrayLike,
        temperature_k: ArrayLike,
        gap_ev: ArrayLike,
        *,
        sigma_ev: ArrayLike | None = None,
        sigma_x: ArrayLike | None = None,
        group: Sequence[object] | None = None,
        source: Sequence[object] | None = None,
        measurement_class: Sequence[object] | None = None,
    ) -> "CompositionAwareGapData":
        benchmark = GapBenchmarkData.from_arrays(
            x,
            temperature_k,
            gap_ev,
            sigma_ev=sigma_ev,
            group=group,
        )
        shape = benchmark.x.shape

        if sigma_x is None:
            composition_sigma = np.zeros(shape, dtype=float)
        else:
            composition_sigma = np.asarray(sigma_x, dtype=float)
            composition_sigma = np.broadcast_to(
                composition_sigma, shape
            ).astype(float, copy=True)

        def labels(
            values: Sequence[object] | None,
            *,
            default: str,
            name: str,
        ) -> NDArray[np.str_]:
            if values is None:
                return np.full(shape, default, dtype=str)
            result = np.asarray([str(value) for value in values], dtype=str)
            if result.shape != shape:
                raise ValueError(f"{name} must have one label per observation")
            return result

        return cls(
            benchmark=benchmark,
            sigma_x=composition_sigma,
            source=labels(source, default="unspecified_source", name="source"),
            measurement_class=labels(
                measurement_class,
                default="unspecified_measurement_class",
                name="measurement_class",
            ),
        )

    @property
    def x(self) -> FloatArray:
        return self.benchmark.x

    @property
    def temperature_k(self) -> FloatArray:
        return self.benchmark.temperature_k

    @property
    def gap_ev(self) -> FloatArray:
        return self.benchmark.gap_ev

    @property
    def sigma_ev(self) -> FloatArray:
        return self.benchmark.sigma_ev

    @property
    def group(self) -> NDArray[np.str_]:
        return self.benchmark.group

    def subset(self, mask: ArrayLike) -> "CompositionAwareGapData":
        selected = np.asarray(mask, dtype=bool)
        if selected.shape != self.x.shape:
            raise ValueError("subset mask has the wrong shape")
        if not np.any(selected):
            raise ValueError("subset cannot be empty")
        return CompositionAwareGapData(
            benchmark=self.benchmark.subset(selected),
            sigma_x=self.sigma_x[selected].copy(),
            source=self.source[selected].copy(),
            measurement_class=self.measurement_class[selected].copy(),
        )


@dataclass(frozen=True)
class CompositionUncertaintySpec:
    """Configuration for first-order Gaussian composition propagation."""

    mode: CompositionMode = "shared_group"
    max_iterations: int = 50
    relative_tolerance: float = 1.0e-10
    require_convergence: bool = True
    group_consistency_atol: float = 1.0e-12

    def __post_init__(self) -> None:
        if self.mode not in ("independent", "shared_group"):
            raise ValueError("mode must be 'independent' or 'shared_group'")
        if not isinstance(self.max_iterations, int) or self.max_iterations < 1:
            raise ValueError("max_iterations must be a positive integer")
        if (
            not np.isfinite(self.relative_tolerance)
            or self.relative_tolerance <= 0.0
        ):
            raise ValueError("relative_tolerance must be finite and positive")
        if (
            not np.isfinite(self.group_consistency_atol)
            or self.group_consistency_atol < 0.0
        ):
            raise ValueError(
                "group_consistency_atol must be finite and non-negative"
            )


@dataclass(frozen=True)
class CompositionAwareGapFit:
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
    effective_covariance_ev2: FloatArray
    effective_sigma_ev: FloatArray
    composition_derivative_ev_per_x: FloatArray
    composition_iterations: int
    composition_converged: bool
    composition_mode: str
    covariance_interpretation: str

    def predict(self, x: ArrayLike, temperature_k: ArrayLike) -> float | FloatArray:
        matrix, _ = oscillator_design_matrix(self.specification, x, temperature_k)
        values = matrix @ self.coefficients
        scalar_input = (
            np.asarray(x).ndim == 0 and np.asarray(temperature_k).ndim == 0
        )
        return float(values[0]) if values.size == 1 and scalar_input else values

    def composition_derivative(
        self,
        x: ArrayLike,
        temperature_k: ArrayLike,
    ) -> float | FloatArray:
        matrix, _ = oscillator_composition_derivative_matrix(
            self.specification, x, temperature_k
        )
        values = matrix @ self.coefficients
        scalar_input = (
            np.asarray(x).ndim == 0 and np.asarray(temperature_k).ndim == 0
        )
        return float(values[0]) if values.size == 1 and scalar_input else values


@dataclass(frozen=True)
class CompositionHoldoutFold:
    name: str
    held_out_indices: NDArray[np.int64]
    prediction_ev: FloatArray
    effective_sigma_ev: FloatArray
    composition_derivative_ev_per_x: FloatArray
    metrics: ResidualMetrics
    fit: CompositionAwareGapFit


@dataclass(frozen=True)
class CompositionCrossValidationResult:
    predictions_ev: FloatArray
    residual_ev: FloatArray
    effective_sigma_ev: FloatArray
    metrics: ResidualMetrics
    folds: tuple[CompositionHoldoutFold, ...]


@dataclass(frozen=True)
class _FitCore:
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


def oscillator_composition_derivative_matrix(
    specification: OscillatorBasisSpec,
    x: ArrayLike,
    temperature_k: ArrayLike,
) -> tuple[FloatArray, tuple[str, ...]]:
    """Return the analytic derivative of every design column with respect to x."""

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
    base_matrix, labels = oscillator_design_matrix(
        specification, flat_x, flat_temperature
    )
    columns: list[FloatArray] = []
    column_index = 0

    for degree in range(specification.static_degree + 1):
        columns.append(
            np.zeros_like(flat_x)
            if degree == 0
            else degree * flat_x ** (degree - 1)
        )
        column_index += 1

    for _ in specification.oscillator_temperatures_k:
        for degree in range(specification.amplitude_degree + 1):
            thermal_column = base_matrix[:, column_index]
            columns.append(
                np.zeros_like(flat_x)
                if degree == 0
                else degree * thermal_column / flat_x
            )
            zero = flat_x == 0.0
            if degree == 1 and np.any(zero):
                columns[-1][zero] = base_matrix[zero, column_index]
            elif degree > 1 and np.any(zero):
                columns[-1][zero] = 0.0
            column_index += 1

    if specification.quasiharmonic_degree is not None:
        for degree in range(specification.quasiharmonic_degree + 1):
            columns.append(
                np.zeros_like(flat_x)
                if degree == 0
                else flat_temperature * degree * flat_x ** (degree - 1)
            )
            column_index += 1

    if column_index != base_matrix.shape[1]:
        raise RuntimeError("composition derivative columns do not match the design")
    return np.column_stack(columns), labels


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
    return particular, vh[rank:].T.copy()


def _validate_measurement_classes(
    data: CompositionAwareGapData,
    *,
    allow_mixed_measurement_classes: bool,
) -> None:
    classes = np.unique(data.measurement_class)
    if classes.size > 1 and not allow_mixed_measurement_classes:
        raise ValueError(
            "mixed measurement classes are not pooled automatically; subset the "
            "data or pass allow_mixed_measurement_classes=True explicitly"
        )


def _validate_shared_groups(
    data: CompositionAwareGapData,
    specification: CompositionUncertaintySpec,
) -> None:
    if specification.mode != "shared_group":
        return
    for group in np.unique(data.group):
        indices = np.flatnonzero(data.group == group)
        sigma = data.sigma_x[indices]
        if not np.any(sigma > 0.0):
            continue
        if not np.allclose(
            data.x[indices],
            data.x[indices][0],
            rtol=0.0,
            atol=specification.group_consistency_atol,
        ):
            raise ValueError(
                f"shared_group composition values disagree within group {group!r}"
            )
        if not np.allclose(
            sigma,
            sigma[0],
            rtol=0.0,
            atol=specification.group_consistency_atol,
        ):
            raise ValueError(
                f"shared_group sigma_x values disagree within group {group!r}"
            )


def _composition_covariance(
    data: CompositionAwareGapData,
    derivative_ev_per_x: FloatArray,
    specification: CompositionUncertaintySpec,
) -> FloatArray:
    derivative = np.asarray(derivative_ev_per_x, dtype=float)
    if derivative.shape != data.x.shape or not np.all(np.isfinite(derivative)):
        raise ValueError("composition derivative must be finite and observation-sized")

    covariance = np.diag(data.sigma_ev**2)
    if specification.mode == "independent":
        covariance[np.diag_indices_from(covariance)] += (
            derivative * data.sigma_x
        ) ** 2
        return covariance

    _validate_shared_groups(data, specification)
    for group in np.unique(data.group):
        indices = np.flatnonzero(data.group == group)
        sigma = float(data.sigma_x[indices][0])
        if sigma == 0.0:
            continue
        covariance[np.ix_(indices, indices)] += sigma**2 * np.outer(
            derivative[indices], derivative[indices]
        )
    return covariance


def _fit_with_covariance(
    data: CompositionAwareGapData,
    specification: OscillatorBasisSpec,
    covariance_ev2: FloatArray,
    constraints: LinearEqualityConstraints | None,
) -> _FitCore:
    covariance = np.asarray(covariance_ev2, dtype=float)
    expected_shape = (data.gap_ev.size, data.gap_ev.size)
    if covariance.shape != expected_shape:
        raise ValueError("effective covariance has the wrong shape")
    if not np.all(np.isfinite(covariance)) or not np.allclose(
        covariance, covariance.T, rtol=0.0, atol=1.0e-15
    ):
        raise ValueError("effective covariance must be finite and symmetric")
    try:
        cholesky = np.linalg.cholesky(covariance)
    except np.linalg.LinAlgError as error:
        raise np.linalg.LinAlgError(
            "effective covariance must be positive definite"
        ) from error

    matrix, labels = oscillator_design_matrix(
        specification, data.x, data.temperature_k
    )
    parameter_count = matrix.shape[1]
    particular, null_space = _constraint_parameterization(
        parameter_count, constraints
    )
    free_count = null_space.shape[1]

    weighted_matrix = np.linalg.solve(cholesky, matrix)
    weighted_target = np.linalg.solve(cholesky, data.gap_ev)
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
    whitened_residual = np.linalg.solve(cholesky, residual)
    chi_square = float(whitened_residual @ whitened_residual)
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
    effective_sigma = np.sqrt(np.diag(covariance))

    return _FitCore(
        parameter_labels=labels,
        coefficients=coefficients,
        covariance_known_sigma=covariance_known,
        covariance_scaled=covariance_scaled,
        correlation_scaled=correlation,
        standard_errors_scaled=standard_errors,
        fitted_gap_ev=fitted,
        residual_ev=residual,
        metrics=residual_metrics(
            data.gap_ev,
            fitted,
            sigma_ev=effective_sigma,
        ),
        free_parameter_count=free_count,
        design_rank=rank,
        singular_values=singular_values,
        condition_number=condition_number,
        chi_square=chi_square,
        degrees_of_freedom=degrees_of_freedom,
        reduced_chi_square=reduced_chi_square,
    )


def _from_exact_x_fit(
    data: CompositionAwareGapData,
    base: LinearGapFit,
) -> CompositionAwareGapFit:
    derivative_matrix, _ = oscillator_composition_derivative_matrix(
        base.specification, data.x, data.temperature_k
    )
    derivative = derivative_matrix @ base.coefficients
    covariance = np.diag(data.sigma_ev**2)
    return CompositionAwareGapFit(
        specification=base.specification,
        parameter_labels=base.parameter_labels,
        coefficients=base.coefficients,
        covariance_known_sigma=base.covariance_known_sigma,
        covariance_scaled=base.covariance_scaled,
        correlation_scaled=base.correlation_scaled,
        standard_errors_scaled=base.standard_errors_scaled,
        fitted_gap_ev=base.fitted_gap_ev,
        residual_ev=base.residual_ev,
        metrics=base.metrics,
        free_parameter_count=base.free_parameter_count,
        design_rank=base.design_rank,
        singular_values=base.singular_values,
        condition_number=base.condition_number,
        chi_square=base.chi_square,
        degrees_of_freedom=base.degrees_of_freedom,
        reduced_chi_square=base.reduced_chi_square,
        effective_covariance_ev2=covariance,
        effective_sigma_ev=data.sigma_ev.copy(),
        composition_derivative_ev_per_x=derivative,
        composition_iterations=0,
        composition_converged=True,
        composition_mode="exact_x",
        covariance_interpretation="ordinary weighted least squares",
    )


def _assemble_fit(
    specification: OscillatorBasisSpec,
    core: _FitCore,
    covariance: FloatArray,
    derivative: FloatArray,
    *,
    iterations: int,
    converged: bool,
    mode: str,
) -> CompositionAwareGapFit:
    return CompositionAwareGapFit(
        specification=specification,
        parameter_labels=core.parameter_labels,
        coefficients=core.coefficients,
        covariance_known_sigma=core.covariance_known_sigma,
        covariance_scaled=core.covariance_scaled,
        correlation_scaled=core.correlation_scaled,
        standard_errors_scaled=core.standard_errors_scaled,
        fitted_gap_ev=core.fitted_gap_ev,
        residual_ev=core.residual_ev,
        metrics=core.metrics,
        free_parameter_count=core.free_parameter_count,
        design_rank=core.design_rank,
        singular_values=core.singular_values,
        condition_number=core.condition_number,
        chi_square=core.chi_square,
        degrees_of_freedom=core.degrees_of_freedom,
        reduced_chi_square=core.reduced_chi_square,
        effective_covariance_ev2=covariance,
        effective_sigma_ev=np.sqrt(np.diag(covariance)),
        composition_derivative_ev_per_x=derivative,
        composition_iterations=iterations,
        composition_converged=converged,
        composition_mode=mode,
        covariance_interpretation=(
            "conditional working covariance from first-order Gaussian "
            "composition linearization; parameter covariance is not an exact "
            "errors-in-variables posterior"
        ),
    )


def fit_composition_aware_gap_model(
    data: CompositionAwareGapData,
    specification: OscillatorBasisSpec,
    *,
    composition_uncertainty: CompositionUncertaintySpec | None = None,
    constraints: LinearEqualityConstraints | None = None,
    allow_mixed_measurement_classes: bool = False,
) -> CompositionAwareGapFit:
    """Fit with first-order composition uncertainty and optional group correlation.

    Nonzero ``sigma_x`` requires an explicit ``CompositionUncertaintySpec``. This
    avoids silently choosing an independence or shared-specimen interpretation.
    """

    _validate_measurement_classes(
        data,
        allow_mixed_measurement_classes=allow_mixed_measurement_classes,
    )
    has_composition_uncertainty = bool(np.any(data.sigma_x > 0.0))
    if not has_composition_uncertainty:
        base = fit_linear_gap_model(
            data.benchmark,
            specification,
            constraints=constraints,
        )
        return _from_exact_x_fit(data, base)
    if composition_uncertainty is None:
        raise ValueError(
            "nonzero sigma_x requires an explicit CompositionUncertaintySpec"
        )

    _validate_shared_groups(data, composition_uncertainty)
    current_covariance = np.diag(data.sigma_ev**2)
    derivative_matrix, _ = oscillator_composition_derivative_matrix(
        specification, data.x, data.temperature_k
    )
    last_core: _FitCore | None = None
    last_derivative = np.zeros_like(data.x)

    for iteration in range(1, composition_uncertainty.max_iterations + 1):
        core = _fit_with_covariance(
            data,
            specification,
            current_covariance,
            constraints,
        )
        derivative = derivative_matrix @ core.coefficients
        updated_covariance = _composition_covariance(
            data,
            derivative,
            composition_uncertainty,
        )
        denominator = max(
            float(np.linalg.norm(current_covariance, ord="fro")),
            _EPS,
        )
        relative_change = float(
            np.linalg.norm(updated_covariance - current_covariance, ord="fro")
            / denominator
        )
        last_core = core
        last_derivative = derivative
        current_covariance = updated_covariance

        if relative_change <= composition_uncertainty.relative_tolerance:
            verification_core = _fit_with_covariance(
                data,
                specification,
                current_covariance,
                constraints,
            )
            verification_derivative = (
                derivative_matrix @ verification_core.coefficients
            )
            verification_covariance = _composition_covariance(
                data,
                verification_derivative,
                composition_uncertainty,
            )
            verification_denominator = max(
                float(np.linalg.norm(current_covariance, ord="fro")),
                _EPS,
            )
            verification_change = float(
                np.linalg.norm(
                    verification_covariance - current_covariance,
                    ord="fro",
                )
                / verification_denominator
            )
            if verification_change <= composition_uncertainty.relative_tolerance:
                return _assemble_fit(
                    specification,
                    verification_core,
                    current_covariance,
                    verification_derivative,
                    iterations=iteration,
                    converged=True,
                    mode=composition_uncertainty.mode,
                )
            current_covariance = verification_covariance
            last_core = verification_core
            last_derivative = verification_derivative

    if last_core is None:
        raise RuntimeError("composition iteration did not produce a fit")
    final_core = _fit_with_covariance(
        data,
        specification,
        current_covariance,
        constraints,
    )
    final_derivative = derivative_matrix @ final_core.coefficients
    if composition_uncertainty.require_convergence:
        raise RuntimeError(
            "composition covariance iteration did not converge within "
            f"{composition_uncertainty.max_iterations} iterations"
        )
    return _assemble_fit(
        specification,
        final_core,
        current_covariance,
        final_derivative,
        iterations=composition_uncertainty.max_iterations,
        converged=False,
        mode=composition_uncertainty.mode,
    )


def _holdout_splits_shared_group(
    data: CompositionAwareGapData,
    holdout: NDArray[np.bool_],
) -> bool:
    for group in np.unique(data.group):
        selected = holdout[data.group == group]
        if np.any(selected) and not np.all(selected):
            return True
    return False


def named_composition_holdout_cross_validation(
    data: CompositionAwareGapData,
    specification: OscillatorBasisSpec,
    holdouts: Mapping[str, ArrayLike],
    *,
    composition_uncertainty: CompositionUncertaintySpec | None = None,
    constraints: LinearEqualityConstraints | None = None,
    require_partition: bool = True,
    allow_mixed_measurement_classes: bool = False,
) -> CompositionCrossValidationResult:
    """Cross-validate without splitting a shared-composition specimen group."""

    if not holdouts:
        raise ValueError("at least one holdout mask is required")
    if np.any(data.sigma_x > 0.0) and composition_uncertainty is None:
        raise ValueError(
            "nonzero sigma_x requires an explicit CompositionUncertaintySpec"
        )

    predictions = np.full(data.gap_ev.shape, np.nan, dtype=float)
    effective_sigma = np.full(data.gap_ev.shape, np.nan, dtype=float)
    assigned = np.zeros(data.gap_ev.shape, dtype=int)
    folds: list[CompositionHoldoutFold] = []

    for name, raw_mask in holdouts.items():
        holdout = np.asarray(raw_mask, dtype=bool)
        if holdout.shape != data.gap_ev.shape:
            raise ValueError(f"holdout {name!r} has the wrong shape")
        if not np.any(holdout) or np.all(holdout):
            raise ValueError(f"holdout {name!r} must select some but not all points")
        if (
            composition_uncertainty is not None
            and composition_uncertainty.mode == "shared_group"
            and _holdout_splits_shared_group(data, holdout)
        ):
            raise ValueError(
                f"holdout {name!r} splits a shared-composition group"
            )

        training = data.subset(~holdout)
        held_out = data.subset(holdout)
        fit = fit_composition_aware_gap_model(
            training,
            specification,
            composition_uncertainty=composition_uncertainty,
            constraints=constraints,
            allow_mixed_measurement_classes=allow_mixed_measurement_classes,
        )
        matrix, _ = oscillator_design_matrix(
            specification, held_out.x, held_out.temperature_k
        )
        prediction = matrix @ fit.coefficients
        derivative_matrix, _ = oscillator_composition_derivative_matrix(
            specification, held_out.x, held_out.temperature_k
        )
        derivative = derivative_matrix @ fit.coefficients
        if composition_uncertainty is None or not np.any(held_out.sigma_x > 0.0):
            held_out_covariance = np.diag(held_out.sigma_ev**2)
        else:
            held_out_covariance = _composition_covariance(
                held_out,
                derivative,
                composition_uncertainty,
            )
        held_out_sigma = np.sqrt(np.diag(held_out_covariance))

        indices = np.flatnonzero(holdout)
        predictions[indices] = prediction
        effective_sigma[indices] = held_out_sigma
        assigned[indices] += 1
        folds.append(
            CompositionHoldoutFold(
                name=str(name),
                held_out_indices=indices.astype(np.int64),
                prediction_ev=prediction,
                effective_sigma_ev=held_out_sigma,
                composition_derivative_ev_per_x=derivative,
                metrics=residual_metrics(
                    held_out.gap_ev,
                    prediction,
                    sigma_ev=held_out_sigma,
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
    return CompositionCrossValidationResult(
        predictions_ev=predictions,
        residual_ev=residual,
        effective_sigma_ev=effective_sigma,
        metrics=residual_metrics(
            data.gap_ev[evaluated],
            predictions[evaluated],
            sigma_ev=effective_sigma[evaluated],
        ),
        folds=tuple(folds),
    )


def leave_one_composition_group_out(
    data: CompositionAwareGapData,
    specification: OscillatorBasisSpec,
    *,
    composition_uncertainty: CompositionUncertaintySpec | None = None,
    constraints: LinearEqualityConstraints | None = None,
    allow_mixed_measurement_classes: bool = False,
) -> CompositionCrossValidationResult:
    groups = np.unique(data.group)
    if groups.size < 2:
        raise ValueError("leave-one-group-out requires at least two groups")
    holdouts = {str(group): data.group == group for group in groups}
    return named_composition_holdout_cross_validation(
        data,
        specification,
        holdouts,
        composition_uncertainty=composition_uncertainty,
        constraints=constraints,
        require_partition=True,
        allow_mixed_measurement_classes=allow_mixed_measurement_classes,
    )


def leave_one_source_out(
    data: CompositionAwareGapData,
    specification: OscillatorBasisSpec,
    *,
    composition_uncertainty: CompositionUncertaintySpec | None = None,
    constraints: LinearEqualityConstraints | None = None,
    allow_mixed_measurement_classes: bool = False,
) -> CompositionCrossValidationResult:
    sources = np.unique(data.source)
    if sources.size < 2:
        raise ValueError("leave-one-source-out requires at least two sources")
    holdouts = {str(source): data.source == source for source in sources}
    return named_composition_holdout_cross_validation(
        data,
        specification,
        holdouts,
        composition_uncertainty=composition_uncertainty,
        constraints=constraints,
        require_partition=True,
        allow_mixed_measurement_classes=allow_mixed_measurement_classes,
    )
