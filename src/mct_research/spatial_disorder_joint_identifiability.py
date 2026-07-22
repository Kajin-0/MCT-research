"""Joint identifiability envelopes for multiscale spatial-disorder experiments.

This module combines existing R04 layers without redefining them:

* the exact composite Gaussian instrument kernel and its calibration Jacobian;
* Gaussian and supported half-integer Matérn lateral covariance filtering;
* log-variance and reciprocal-variance Gaussian surrogate fits;
* transmission and cutoff observation-order operators.

The alternative-family calculation is deliberately controlled.  Lateral Matérn
covariance is evaluated with the instrument's axiswise moment-matched Gaussian
scale, while the existing Gaussian finite-depth factor is retained.  The exact
Gaussian composite-kernel versus moment-matched discrepancy is carried as a
separate systematic vector.  The result is an experiment-design envelope, not a
specimen covariance estimate or a universal three-dimensional covariance model.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt
from typing import Literal, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_covariance_bias import (
    fit_gaussian_log_variance_surrogate,
)
from .spatial_disorder_covariance_families import (
    SUPPORTED_MATERN_SMOOTHNESS,
    gaussian_reciprocal_linearity_fit,
    gaussian_reference_variance,
    matern_gaussian_probe_variance_2d,
)
from .spatial_disorder_cutoff import lateral_gaussian_gap_response_cutoff
from .spatial_disorder_instrument import (
    CompositeInstrumentKernel,
    composite_instrument_effective_variance,
    composite_instrument_log_sensitivity,
)
from .spatial_disorder_optics import (
    lateral_gaussian_gap_transmission_observation,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]
ObservationKind = Literal[
    "log_variance",
    "log_gap_standard_deviation",
    "log_transmission_effective_absorption",
    "log_cutoff_energy",
]
FittingConvention = Literal["log_variance", "reciprocal_variance"]


def _finite_positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite_nonnegative(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be a positive integer")
    result = int(value)
    if result <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return result


def _read_only_float(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _validated_vector(
    name: str,
    value: ArrayLike,
    length: int,
    *,
    positive: bool,
) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    if result.shape != (length,):
        raise ValueError(f"{name} must have shape ({length},)")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    if positive and np.any(result <= 0.0):
        raise ValueError(f"{name} must be positive")
    if not positive and np.any(result < 0.0):
        raise ValueError(f"{name} must be non-negative")
    result.setflags(write=False)
    return result


def _validated_covariance(name: str, value: ArrayLike, dimension: int) -> FloatMatrix:
    matrix = np.array(value, dtype=float, copy=True)
    if matrix.shape != (dimension, dimension):
        raise ValueError(f"{name} must have shape ({dimension}, {dimension})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    if not np.allclose(matrix, matrix.T, rtol=1.0e-12, atol=1.0e-14 * scale):
        raise ValueError(f"{name} must be symmetric")
    eigenvalues = np.linalg.eigvalsh(matrix)
    tolerance = 256.0 * np.finfo(float).eps * max(
        1.0,
        scale,
        float(np.max(np.abs(eigenvalues))),
    )
    if float(np.min(eigenvalues)) < -tolerance:
        raise ValueError(f"{name} must be positive semidefinite")
    matrix.setflags(write=False)
    return matrix


@dataclass(frozen=True)
class ObservationOperatorSpecification:
    """Declared scalar observation extracted from each filtered variance."""

    kind: ObservationKind = "log_variance"
    gap_slope_ev_per_fraction: float = 1.0
    mean_gap_ev: float = 0.1
    optical_thickness_cm: float = 1.0e-3
    photon_energy_ev: float = 0.12
    target_response: float = 0.5
    lower_energy_ev: float = 0.04
    upper_energy_ev: float = 0.25
    exponent: float = 0.5
    amplitude_cm_inverse_ev_power: float = 1.0e4
    quadrature_order: int = 128
    standard_deviation_limit: float = 10.0
    absolute_tolerance_ev: float = 1.0e-9
    response_tolerance: float = 1.0e-10
    log_derivative_step: float = 1.0e-4

    def __post_init__(self) -> None:
        allowed = {
            "log_variance",
            "log_gap_standard_deviation",
            "log_transmission_effective_absorption",
            "log_cutoff_energy",
        }
        if self.kind not in allowed:
            raise ValueError(f"kind must be one of {sorted(allowed)}")
        object.__setattr__(
            self,
            "gap_slope_ev_per_fraction",
            _finite_positive(
                "gap_slope_ev_per_fraction", self.gap_slope_ev_per_fraction
            ),
        )
        object.__setattr__(
            self,
            "mean_gap_ev",
            _finite_positive("mean_gap_ev", self.mean_gap_ev),
        )
        object.__setattr__(
            self,
            "optical_thickness_cm",
            _finite_positive("optical_thickness_cm", self.optical_thickness_cm),
        )
        object.__setattr__(
            self,
            "photon_energy_ev",
            _finite_positive("photon_energy_ev", self.photon_energy_ev),
        )
        target = float(self.target_response)
        if not isfinite(target) or not 0.0 < target < 1.0:
            raise ValueError("target_response must lie strictly between zero and one")
        object.__setattr__(self, "target_response", target)
        lower = _finite_positive("lower_energy_ev", self.lower_energy_ev)
        upper = _finite_positive("upper_energy_ev", self.upper_energy_ev)
        if upper <= lower:
            raise ValueError("upper_energy_ev must exceed lower_energy_ev")
        object.__setattr__(self, "lower_energy_ev", lower)
        object.__setattr__(self, "upper_energy_ev", upper)
        object.__setattr__(
            self,
            "exponent",
            _finite_nonnegative("exponent", self.exponent),
        )
        object.__setattr__(
            self,
            "amplitude_cm_inverse_ev_power",
            _finite_positive(
                "amplitude_cm_inverse_ev_power",
                self.amplitude_cm_inverse_ev_power,
            ),
        )
        object.__setattr__(
            self,
            "quadrature_order",
            _positive_integer("quadrature_order", self.quadrature_order),
        )
        object.__setattr__(
            self,
            "standard_deviation_limit",
            _finite_positive(
                "standard_deviation_limit", self.standard_deviation_limit
            ),
        )
        object.__setattr__(
            self,
            "absolute_tolerance_ev",
            _finite_positive("absolute_tolerance_ev", self.absolute_tolerance_ev),
        )
        object.__setattr__(
            self,
            "response_tolerance",
            _finite_positive("response_tolerance", self.response_tolerance),
        )
        step = _finite_positive("log_derivative_step", self.log_derivative_step)
        if step > 0.05:
            raise ValueError("log_derivative_step must not exceed 0.05")
        object.__setattr__(self, "log_derivative_step", step)


@dataclass(frozen=True)
class ObservationOperatorEvaluation:
    """Exact operator values, local sensitivities, and closure shifts."""

    log_observables: FloatArray
    log_variance_sensitivities: FloatArray
    closure_log_shifts: FloatArray


def _single_log_observable(
    variance: float,
    specification: ObservationOperatorSpecification,
    *,
    closure: bool,
) -> float:
    value = _finite_positive("variance", variance)
    if specification.kind == "log_variance":
        return log(value)
    gap_sigma = specification.gap_slope_ev_per_fraction * sqrt(value)
    if specification.kind == "log_gap_standard_deviation":
        return log(gap_sigma)
    if specification.kind == "log_transmission_effective_absorption":
        observation = lateral_gaussian_gap_transmission_observation(
            np.asarray([specification.photon_energy_ev]),
            specification.mean_gap_ev,
            gap_sigma,
            specification.optical_thickness_cm,
            exponent=specification.exponent,
            amplitude_cm_inverse_ev_power=(
                specification.amplitude_cm_inverse_ev_power
            ),
            quadrature_order=specification.quadrature_order,
            standard_deviation_limit=specification.standard_deviation_limit,
        )
        if closure:
            observable = float(observation.mean_absorption_cm_inverse[0])
        else:
            observable = float(
                observation.transmission_effective_absorption_cm_inverse[0]
            )
        return log(_finite_positive("transmission observable", observable))
    comparison = lateral_gaussian_gap_response_cutoff(
        mean_gap_ev=specification.mean_gap_ev,
        gap_sigma_ev=gap_sigma,
        thickness_cm=specification.optical_thickness_cm,
        lower_energy_ev=specification.lower_energy_ev,
        upper_energy_ev=specification.upper_energy_ev,
        target_response=specification.target_response,
        exponent=specification.exponent,
        amplitude_cm_inverse_ev_power=(
            specification.amplitude_cm_inverse_ev_power
        ),
        quadrature_order=specification.quadrature_order,
        standard_deviation_limit=specification.standard_deviation_limit,
        absolute_tolerance_ev=specification.absolute_tolerance_ev,
        response_tolerance=specification.response_tolerance,
    )
    observable = (
        comparison.mean_absorption_closure_energy_ev
        if closure
        else comparison.transmission_averaged_energy_ev
    )
    return log(_finite_positive("cutoff energy", observable))


def evaluate_observation_operator(
    variances: ArrayLike,
    specification: ObservationOperatorSpecification,
) -> ObservationOperatorEvaluation:
    """Map filtered variances into a declared observation space.

    The exact transmission-average or cutoff operator supplies the reported
    observable.  The existing arithmetic-absorption closure supplies a separate
    operation-order shift.  Sensitivities are derivatives of log observable with
    respect to log filtered variance.
    """

    values = np.asarray(variances, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("variances must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("variances must be finite and positive")
    if not isinstance(specification, ObservationOperatorSpecification):
        raise TypeError("specification must be an ObservationOperatorSpecification")

    exact = np.array(
        [
            _single_log_observable(float(value), specification, closure=False)
            for value in values
        ],
        dtype=float,
    )
    closure = np.array(
        [
            _single_log_observable(float(value), specification, closure=True)
            for value in values
        ],
        dtype=float,
    )
    if specification.kind == "log_variance":
        sensitivity = np.ones(values.size, dtype=float)
    elif specification.kind == "log_gap_standard_deviation":
        sensitivity = np.full(values.size, 0.5, dtype=float)
    else:
        step = specification.log_derivative_step
        sensitivity = np.empty(values.size, dtype=float)
        for index, value in enumerate(values):
            plus = _single_log_observable(
                float(value * exp(step)), specification, closure=False
            )
            minus = _single_log_observable(
                float(value * exp(-step)), specification, closure=False
            )
            sensitivity[index] = (plus - minus) / (2.0 * step)
    return ObservationOperatorEvaluation(
        log_observables=_read_only_float(exact),
        log_variance_sensitivities=_read_only_float(sensitivity),
        closure_log_shifts=_read_only_float(closure - exact),
    )


@dataclass(frozen=True)
class SeparationStage:
    """Rank-aware Mahalanobis separation under one covariance stage."""

    covariance: FloatMatrix
    squared_distance: float
    distance: float
    rank: int
    condition_number: float


def _separation_stage(residual: FloatArray, covariance: FloatMatrix) -> SeparationStage:
    matrix = np.asarray(covariance, dtype=float)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    largest = max(0.0, float(np.max(eigenvalues)))
    tolerance = max(1.0e-15, 1.0e-12 * largest * matrix.shape[0])
    active = eigenvalues > tolerance
    rank = int(np.count_nonzero(active))
    if rank == 0:
        squared = 0.0 if float(np.linalg.norm(residual)) <= tolerance else float("inf")
        condition = float("inf")
    else:
        coordinates = eigenvectors[:, active].T @ np.asarray(residual)
        squared = float(np.sum(coordinates**2 / eigenvalues[active]))
        if rank < matrix.shape[0]:
            null_coordinates = eigenvectors[:, ~active].T @ np.asarray(residual)
            if float(np.linalg.norm(null_coordinates)) > 1.0e-10 * max(
                1.0, float(np.linalg.norm(residual))
            ):
                squared = float("inf")
        condition = float(np.max(eigenvalues[active]) / np.min(eigenvalues[active]))
    distance = sqrt(squared) if isfinite(squared) else float("inf")
    return SeparationStage(
        covariance=_read_only_float(matrix),
        squared_distance=squared,
        distance=float(distance),
        rank=rank,
        condition_number=condition,
    )


@dataclass(frozen=True)
class FamilyConventionIdentifiability:
    """One covariance family interpreted through one Gaussian fit convention."""

    true_family: str
    true_matern_smoothness: float | None
    fitting_convention: FittingConvention
    true_variances: FloatArray
    fitted_variances: FloatArray
    fitted_point_variance: float
    fitted_correlation_length: float
    true_log_observables: FloatArray
    fitted_log_observables: FloatArray
    log_observable_residuals: FloatArray
    observation_only: SeparationStage
    calibration_added: SeparationStage
    kernel_shape_added: SeparationStage
    full_envelope: SeparationStage
    threshold_distance: float
    decision: str


@dataclass(frozen=True)
class JointIdentifiabilityScreen:
    """Controlled family screen under a declared multiscale instrument design."""

    equivalent_probe_sigmas: FloatArray
    depth_ratios: FloatArray
    exact_gaussian_variances: FloatArray
    reduced_gaussian_variances: FloatArray
    kernel_shape_log_shifts: FloatArray
    instrument_log_sensitivity: FloatMatrix
    instrument_log_variance_covariance: FloatMatrix
    observation_log_standard_deviations: FloatArray
    observation_specification: ObservationOperatorSpecification
    results: tuple[FamilyConventionIdentifiability, ...]
    convention_sensitive_families: tuple[str, ...]


def _family_label(smoothness: float | None) -> str:
    return "gaussian" if smoothness is None else f"matern_{smoothness:g}"


def _fit_gaussian_surrogate(
    scales: FloatArray,
    lateral_variances: FloatArray,
    observation_log_standard_deviations: FloatArray,
    convention: FittingConvention,
) -> tuple[float, float, FloatArray]:
    relative_standard_deviations = np.asarray(observation_log_standard_deviations)
    if convention == "log_variance":
        weights = 1.0 / relative_standard_deviations**2
        fit = fit_gaussian_log_variance_surrogate(
            scales,
            lateral_variances,
            weights=weights,
        )
        return (
            fit.fitted_point_variance,
            fit.fitted_correlation_length,
            fit.fitted_variances,
        )
    standard_deviations = np.asarray(lateral_variances) * relative_standard_deviations
    fit = gaussian_reciprocal_linearity_fit(
        scales,
        lateral_variances,
        variance_standard_deviations=standard_deviations,
    )
    return (
        fit.fitted_point_variance,
        fit.fitted_correlation_length,
        fit.fitted_variances,
    )


def _decision(
    observation_only: SeparationStage,
    calibration_added: SeparationStage,
    kernel_added: SeparationStage,
    full: SeparationStage,
    threshold: float,
) -> str:
    if full.distance >= threshold:
        return "resolved_under_full_envelope"
    if observation_only.distance < threshold:
        return "observation_limited"
    if calibration_added.distance < threshold:
        return "instrument_calibration_limited"
    if kernel_added.distance < threshold:
        return "kernel_shape_limited"
    return "observation_operator_limited"


def joint_identifiability_screen(
    *,
    point_variance: float,
    lateral_correlation_length: float,
    depth_correlation_length: float,
    kernels: Sequence[CompositeInstrumentKernel],
    instrument_parameter_log_covariance: ArrayLike,
    observation_log_standard_deviations: ArrayLike,
    observation_specification: ObservationOperatorSpecification | None = None,
    matern_smoothness_values: Sequence[float] = SUPPORTED_MATERN_SMOOTHNESS,
    fitting_conventions: Sequence[FittingConvention] = (
        "log_variance",
        "reciprocal_variance",
    ),
    threshold_distance: float = 3.0,
    depth_quadrature_order: int = 96,
) -> JointIdentifiabilityScreen:
    """Evaluate covariance-family separation under a joint uncertainty envelope.

    Instrument log-parameter perturbations are shared across all declared kernels,
    so calibration produces a correlated cross-scale covariance.  Kernel-shape and
    observation-operation shifts are conservatively represented as rank-one outer
    products using their full declared shift as one standard deviation.
    """

    amplitude = _finite_positive("point_variance", point_variance)
    lateral_xi = _finite_positive(
        "lateral_correlation_length", lateral_correlation_length
    )
    depth_xi = _finite_positive("depth_correlation_length", depth_correlation_length)
    threshold = _finite_positive("threshold_distance", threshold_distance)
    order = _positive_integer("depth_quadrature_order", depth_quadrature_order)
    kernel_tuple = tuple(kernels)
    if len(kernel_tuple) < 3:
        raise ValueError("at least three instrument kernels are required")
    if not all(isinstance(item, CompositeInstrumentKernel) for item in kernel_tuple):
        raise TypeError("kernels must contain only CompositeInstrumentKernel values")
    if any(
        min(
            item.psf_sigma_x,
            item.psf_sigma_y,
            item.pixel_width_x,
            item.pixel_width_y,
        )
        <= 0.0
        for item in kernel_tuple
    ):
        raise ValueError(
            "all lateral instrument parameters must be positive for joint calibration"
        )

    specification = observation_specification or ObservationOperatorSpecification()
    if not isinstance(specification, ObservationOperatorSpecification):
        raise TypeError(
            "observation_specification must be an ObservationOperatorSpecification"
        )
    calibration_covariance = _validated_covariance(
        "instrument_parameter_log_covariance",
        instrument_parameter_log_covariance,
        len(CompositeInstrumentKernel.log_parameter_names),
    )
    observation_sd = _validated_vector(
        "observation_log_standard_deviations",
        observation_log_standard_deviations,
        len(kernel_tuple),
        positive=True,
    )

    scales: list[float] = []
    exact_gaussian: list[float] = []
    depth_ratios: list[float] = []
    sensitivity_rows: list[FloatArray] = []
    for kernel in kernel_tuple:
        if not np.isclose(
            kernel.moment_matched_sigma_x,
            kernel.moment_matched_sigma_y,
            rtol=1.0e-10,
            atol=1.0e-14
            * max(1.0, kernel.moment_matched_sigma_x, kernel.moment_matched_sigma_y),
        ):
            raise ValueError(
                "joint family screen requires isotropic moment-matched lateral kernels"
            )
        scales.append(kernel.moment_matched_sigma_x)
        composite = composite_instrument_effective_variance(
            amplitude,
            [lateral_xi, lateral_xi, depth_xi],
            kernel,
            depth_quadrature_order=order,
        )
        exact_gaussian.append(composite.effective_variance)
        depth_ratios.append(composite.depth_ratio)
        sensitivity_rows.append(
            composite_instrument_log_sensitivity(
                [lateral_xi, lateral_xi, depth_xi],
                kernel,
                depth_quadrature_order=order,
            )
        )

    scale_array = np.asarray(scales, dtype=float)
    if np.unique(scale_array).size != scale_array.size:
        raise ValueError("equivalent probe scales must be distinct")
    sort_order = np.argsort(scale_array)
    scale_array = scale_array[sort_order]
    exact_gaussian_array = np.asarray(exact_gaussian, dtype=float)[sort_order]
    depth_array = np.asarray(depth_ratios, dtype=float)[sort_order]
    sensitivity_matrix = np.asarray(sensitivity_rows, dtype=float)[sort_order]
    observation_sd_array = np.asarray(observation_sd, dtype=float)[sort_order]

    reduced_gaussian_lateral = gaussian_reference_variance(
        amplitude,
        lateral_xi,
        scale_array,
    )
    reduced_gaussian = np.asarray(reduced_gaussian_lateral) * depth_array
    kernel_shift = np.log(exact_gaussian_array) - np.log(reduced_gaussian)
    instrument_log_variance_covariance = (
        sensitivity_matrix
        @ np.asarray(calibration_covariance)
        @ sensitivity_matrix.T
    )

    families: list[tuple[float | None, FloatArray]] = [
        (None, _read_only_float(reduced_gaussian))
    ]
    seen_smoothness: set[float] = set()
    for raw in matern_smoothness_values:
        smoothness = float(raw)
        if smoothness not in SUPPORTED_MATERN_SMOOTHNESS:
            raise ValueError(
                "matern_smoothness_values must use supported half-integer values"
            )
        if smoothness in seen_smoothness:
            raise ValueError("matern_smoothness_values must be unique")
        seen_smoothness.add(smoothness)
        lateral = matern_gaussian_probe_variance_2d(
            amplitude,
            lateral_xi,
            scale_array,
            smoothness,
        )
        families.append((smoothness, _read_only_float(np.asarray(lateral) * depth_array)))

    conventions = tuple(fitting_conventions)
    if not conventions or any(
        item not in ("log_variance", "reciprocal_variance")
        for item in conventions
    ):
        raise ValueError(
            "fitting_conventions must contain log_variance or reciprocal_variance"
        )
    if len(set(conventions)) != len(conventions):
        raise ValueError("fitting_conventions must be unique")

    results: list[FamilyConventionIdentifiability] = []
    decisions_by_family: dict[str, set[str]] = {}
    observation_log_variance_covariance = np.diag(observation_sd_array**2)
    for smoothness, true_variances in families:
        label = _family_label(smoothness)
        true_operator = evaluate_observation_operator(true_variances, specification)
        transform = np.diag(true_operator.log_variance_sensitivities)
        observation_covariance = (
            transform @ observation_log_variance_covariance @ transform.T
        )
        calibration_covariance_observable = (
            transform
            @ instrument_log_variance_covariance
            @ transform.T
        )
        kernel_vector = transform @ kernel_shift
        operator_vector = np.asarray(true_operator.closure_log_shifts)
        covariance_observation = observation_covariance
        covariance_calibration = (
            covariance_observation + calibration_covariance_observable
        )
        covariance_kernel = covariance_calibration + np.outer(
            kernel_vector, kernel_vector
        )
        covariance_full = covariance_kernel + np.outer(
            operator_vector, operator_vector
        )

        lateral_true = np.asarray(true_variances) / depth_array
        for convention in conventions:
            fitted_amplitude, fitted_xi, fitted_lateral = _fit_gaussian_surrogate(
                _read_only_float(scale_array),
                _read_only_float(lateral_true),
                _read_only_float(observation_sd_array),
                convention,
            )
            fitted_variances = np.asarray(fitted_lateral) * depth_array
            fitted_operator = evaluate_observation_operator(
                fitted_variances,
                specification,
            )
            residual = (
                np.asarray(true_operator.log_observables)
                - np.asarray(fitted_operator.log_observables)
            )
            stage_observation = _separation_stage(
                _read_only_float(residual),
                _read_only_float(covariance_observation),
            )
            stage_calibration = _separation_stage(
                _read_only_float(residual),
                _read_only_float(covariance_calibration),
            )
            stage_kernel = _separation_stage(
                _read_only_float(residual),
                _read_only_float(covariance_kernel),
            )
            stage_full = _separation_stage(
                _read_only_float(residual),
                _read_only_float(covariance_full),
            )
            decision = _decision(
                stage_observation,
                stage_calibration,
                stage_kernel,
                stage_full,
                threshold,
            )
            decisions_by_family.setdefault(label, set()).add(decision)
            results.append(
                FamilyConventionIdentifiability(
                    true_family=label,
                    true_matern_smoothness=smoothness,
                    fitting_convention=convention,
                    true_variances=_read_only_float(true_variances),
                    fitted_variances=_read_only_float(fitted_variances),
                    fitted_point_variance=float(fitted_amplitude),
                    fitted_correlation_length=float(fitted_xi),
                    true_log_observables=true_operator.log_observables,
                    fitted_log_observables=fitted_operator.log_observables,
                    log_observable_residuals=_read_only_float(residual),
                    observation_only=stage_observation,
                    calibration_added=stage_calibration,
                    kernel_shape_added=stage_kernel,
                    full_envelope=stage_full,
                    threshold_distance=threshold,
                    decision=decision,
                )
            )

    convention_sensitive = tuple(
        sorted(
            label
            for label, decisions in decisions_by_family.items()
            if len(decisions) > 1
        )
    )
    return JointIdentifiabilityScreen(
        equivalent_probe_sigmas=_read_only_float(scale_array),
        depth_ratios=_read_only_float(depth_array),
        exact_gaussian_variances=_read_only_float(exact_gaussian_array),
        reduced_gaussian_variances=_read_only_float(reduced_gaussian),
        kernel_shape_log_shifts=_read_only_float(kernel_shift),
        instrument_log_sensitivity=_read_only_float(sensitivity_matrix),
        instrument_log_variance_covariance=_read_only_float(
            instrument_log_variance_covariance
        ),
        observation_log_standard_deviations=_read_only_float(
            observation_sd_array
        ),
        observation_specification=specification,
        results=tuple(results),
        convention_sensitive_families=convention_sensitive,
    )
