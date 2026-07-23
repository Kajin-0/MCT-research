"""Nonlinear verification tools for the restricted R06 bipolar kernel.

This Phase 1C module adds numerical globalization, voltage continuation,
manufactured forcing, mesh refinement, and independent continuity-balance
checks to the source-free dimensionless bipolar finite-volume residual. It does
not add HgCdTe material relations, traps, recombination, optical generation,
dynamic contacts, stochastic operators, or terminal PSD calculations.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite, log, pi

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarCurrentConservationMetrics,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    assemble_bipolar_residual,
    bipolar_current_conservation_metrics,
    linear_bipolar_reservoir_state,
    pack_bipolar_state,
    reconstruct_bipolar_state,
)
from .finite_volume_prototype import UniformNodeMesh1D
from .nonlinear_verification import NewtonOptions, SparseCOOMatrix


@dataclass(frozen=True)
class BipolarForcing:
    """Interior forcing for Poisson and both continuity equations."""

    poisson: NDArray[np.float64]
    electron_continuity: NDArray[np.float64]
    hole_continuity: NDArray[np.float64]

    def vector(self, interior_count: int) -> NDArray[np.float64]:
        arrays = tuple(
            np.asarray(values, dtype=float)
            for values in (
                self.poisson,
                self.electron_continuity,
                self.hole_continuity,
            )
        )
        expected = (interior_count,)
        if any(values.shape != expected for values in arrays):
            raise ValueError("forcing arrays must match the mesh interior count")
        if not all(np.all(np.isfinite(values)) for values in arrays):
            raise ValueError("forcing arrays must contain only finite values")
        return np.concatenate(arrays)


@dataclass(frozen=True)
class BipolarContinuityBalance:
    """Terminal-minus-volume balance diagnostics for both carrier equations."""

    electron_terminal_difference: float
    electron_volume_source: float
    electron_absolute_mismatch: float
    electron_relative_mismatch: float
    hole_terminal_difference: float
    hole_volume_source: float
    hole_absolute_mismatch: float
    hole_relative_mismatch: float


@dataclass(frozen=True)
class BipolarNewtonIteration:
    """One accepted damped-Newton iteration for the bipolar system."""

    iteration: int
    residual_inf_norm_before: float
    poisson_inf_norm_before: float
    electron_continuity_inf_norm_before: float
    hole_continuity_inf_norm_before: float
    step_inf_norm: float
    accepted_damping: float
    backtracks: int
    jacobian_condition_estimate: float
    residual_inf_norm_after: float


@dataclass(frozen=True)
class BipolarNewtonResult:
    """Bipolar damped-Newton result with explicit termination diagnostics."""

    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    target_residual_inf_norm: float
    history: tuple[BipolarNewtonIteration, ...]
    current_conservation: BipolarCurrentConservationMetrics
    continuity_balance: BipolarContinuityBalance


@dataclass(frozen=True)
class BipolarContinuationStep:
    """One accepted or failed right-contact voltage continuation point."""

    potential_right: float
    result: BipolarNewtonResult


@dataclass(frozen=True)
class BipolarContinuationResult:
    """Sequence of bipolar voltage-continuation solves."""

    steps: tuple[BipolarContinuationStep, ...]
    completed: bool
    final_state: NDArray[np.float64]


@dataclass(frozen=True)
class ManufacturedBipolarSolutionSpec:
    """Smooth positive manufactured bipolar state on ``0 <= x <= L``."""

    potential_linear_slope: float = 0.35
    potential_sine_amplitude: float = 0.10
    log_electron_sine_amplitude: float = 0.18
    log_hole_sine_amplitude: float = -0.14
    electron_boundary_density: float = 1.20
    hole_boundary_density: float = 0.90

    def __post_init__(self) -> None:
        values = (
            self.potential_linear_slope,
            self.potential_sine_amplitude,
            self.log_electron_sine_amplitude,
            self.log_hole_sine_amplitude,
            self.electron_boundary_density,
            self.hole_boundary_density,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("manufactured-solution coefficients must be finite")
        if self.electron_boundary_density <= 0.0:
            raise ValueError("electron_boundary_density must be positive")
        if self.hole_boundary_density <= 0.0:
            raise ValueError("hole_boundary_density must be positive")


@dataclass(frozen=True)
class ManufacturedBipolarCase:
    """Sampled exact bipolar state, boundaries, and continuous forcing."""

    boundaries: BipolarBoundaryValues
    exact_state: NDArray[np.float64]
    exact_potential: NDArray[np.float64]
    exact_electron_density: NDArray[np.float64]
    exact_hole_density: NDArray[np.float64]
    forcing: BipolarForcing


@dataclass(frozen=True)
class BipolarRefinementRecord:
    """Manufactured-solution errors and balance on one mesh."""

    intervals: int
    spacing: float
    potential_linf_error: float
    electron_linf_error: float
    hole_linf_error: float
    potential_l2_error: float
    electron_l2_error: float
    hole_l2_error: float
    iterations: int
    final_residual_inf_norm: float
    electron_balance_relative_mismatch: float
    hole_balance_relative_mismatch: float


@dataclass(frozen=True)
class BipolarRefinementStudy:
    """Bipolar mesh-refinement records and observed consecutive orders."""

    records: tuple[BipolarRefinementRecord, ...]
    potential_linf_orders: tuple[float, ...]
    electron_linf_orders: tuple[float, ...]
    hole_linf_orders: tuple[float, ...]


def assemble_forced_bipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    forcing: BipolarForcing | None = None,
) -> NDArray[np.float64]:
    """Return the bipolar residual minus declared interior forcing."""

    residual = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    if forcing is None:
        return residual
    return residual - forcing.vector(mesh.interior_count)


def bipolar_continuity_balance(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    forcing: BipolarForcing | None = None,
) -> BipolarContinuityBalance:
    """Compare terminal current differences with integrated volume forcing."""

    metrics = bipolar_current_conservation_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    if forcing is None:
        electron_source = 0.0
        hole_source = 0.0
    else:
        vector = forcing.vector(mesh.interior_count)
        count = mesh.interior_count
        electron_source = mesh.spacing * float(np.sum(vector[count : 2 * count]))
        hole_source = mesh.spacing * float(np.sum(vector[2 * count :]))

    electron_terminal = float(
        metrics.electron.face_current[-1] - metrics.electron.face_current[0]
    )
    hole_terminal = float(metrics.hole.face_current[-1] - metrics.hole.face_current[0])
    electron_mismatch = electron_terminal - electron_source
    hole_mismatch = hole_terminal - hole_source
    electron_scale = max(1.0, abs(electron_terminal), abs(electron_source))
    hole_scale = max(1.0, abs(hole_terminal), abs(hole_source))
    return BipolarContinuityBalance(
        electron_terminal_difference=electron_terminal,
        electron_volume_source=electron_source,
        electron_absolute_mismatch=abs(electron_mismatch),
        electron_relative_mismatch=abs(electron_mismatch) / electron_scale,
        hole_terminal_difference=hole_terminal,
        hole_volume_source=hole_source,
        hole_absolute_mismatch=abs(hole_mismatch),
        hole_relative_mismatch=abs(hole_mismatch) / hole_scale,
    )


def bipolar_jacobian_as_coo(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    drop_tolerance: float = 0.0,
) -> SparseCOOMatrix:
    """Serialize the verified dense bipolar Jacobian in COO form."""

    tolerance = float(drop_tolerance)
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("drop_tolerance must be finite and non-negative")
    dense = assemble_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    row, column = np.nonzero(np.abs(dense) > tolerance)
    return SparseCOOMatrix(
        shape=dense.shape,
        row=row.astype(np.int64),
        column=column.astype(np.int64),
        data=dense[row, column].astype(float),
    )


def _block_norms(
    residual: NDArray[np.float64],
    interior_count: int,
) -> tuple[float, float, float]:
    count = interior_count
    return (
        float(np.linalg.norm(residual[:count], ord=np.inf)),
        float(np.linalg.norm(residual[count : 2 * count], ord=np.inf)),
        float(np.linalg.norm(residual[2 * count :], ord=np.inf)),
    )


def _safe_residual(
    state: NDArray[np.float64],
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    forcing: BipolarForcing | None,
) -> NDArray[np.float64] | None:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            residual = assemble_forced_bipolar_residual(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                forcing=forcing,
            )
    except (ValueError, FloatingPointError, OverflowError):
        return None
    if not np.all(np.isfinite(residual)):
        return None
    return residual


def solve_bipolar_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    forcing: BipolarForcing | None = None,
    options: NewtonOptions | None = None,
) -> BipolarNewtonResult:
    """Solve the restricted bipolar system with residual-decreasing damping."""

    controls = NewtonOptions() if options is None else options
    state = np.asarray(initial_state, dtype=float)
    if state.ndim != 1 or state.size != 3 * mesh.interior_count:
        raise ValueError("initial_state has incompatible shape")
    if not np.all(np.isfinite(state)):
        raise ValueError("initial_state must contain only finite values")
    state = state.copy()

    residual = _safe_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        forcing=forcing,
    )
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")

    initial_norm = float(np.linalg.norm(residual, ord=np.inf))
    target = max(
        controls.absolute_tolerance,
        controls.relative_tolerance * max(1.0, initial_norm),
    )
    history: list[BipolarNewtonIteration] = []

    def finish(converged: bool, reason: str) -> BipolarNewtonResult:
        final_residual = _safe_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            forcing=forcing,
        )
        final_norm = (
            float("inf")
            if final_residual is None
            else float(np.linalg.norm(final_residual, ord=np.inf))
        )
        return BipolarNewtonResult(
            state=state.copy(),
            converged=converged,
            termination_reason=reason,
            iterations=len(history),
            initial_residual_inf_norm=initial_norm,
            final_residual_inf_norm=final_norm,
            target_residual_inf_norm=target,
            history=tuple(history),
            current_conservation=bipolar_current_conservation_metrics(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
            ),
            continuity_balance=bipolar_continuity_balance(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                forcing=forcing,
            ),
        )

    if initial_norm <= target:
        return finish(True, "initial_residual_converged")

    for iteration in range(controls.maximum_iterations):
        poisson_norm, electron_norm, hole_norm = _block_norms(
            residual,
            mesh.interior_count,
        )
        jacobian = assemble_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        try:
            condition = float(np.linalg.cond(jacobian))
            step = np.linalg.solve(jacobian, -residual)
        except np.linalg.LinAlgError:
            return finish(False, "singular_jacobian")

        if not np.all(np.isfinite(step)):
            return finish(False, "nonfinite_newton_step")

        step_norm = float(np.linalg.norm(step, ord=np.inf))
        old_two_norm = float(np.linalg.norm(residual))
        damping = 1.0
        accepted_state: NDArray[np.float64] | None = None
        accepted_residual: NDArray[np.float64] | None = None
        accepted_backtracks = 0

        for backtracks in range(controls.maximum_backtracks + 1):
            trial_state = state + damping * step
            trial_residual = _safe_residual(
                trial_state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                forcing=forcing,
            )
            if trial_residual is not None:
                trial_two_norm = float(np.linalg.norm(trial_residual))
                if trial_two_norm <= (
                    1.0 - controls.armijo_fraction * damping
                ) * old_two_norm:
                    accepted_state = trial_state
                    accepted_residual = trial_residual
                    accepted_backtracks = backtracks
                    break
            damping *= controls.backtrack_factor
            if damping < controls.minimum_damping:
                break

        if accepted_state is None or accepted_residual is None:
            return finish(False, "line_search_failed")

        after_norm = float(np.linalg.norm(accepted_residual, ord=np.inf))
        history.append(
            BipolarNewtonIteration(
                iteration=iteration,
                residual_inf_norm_before=float(
                    np.linalg.norm(residual, ord=np.inf)
                ),
                poisson_inf_norm_before=poisson_norm,
                electron_continuity_inf_norm_before=electron_norm,
                hole_continuity_inf_norm_before=hole_norm,
                step_inf_norm=step_norm,
                accepted_damping=damping,
                backtracks=accepted_backtracks,
                jacobian_condition_estimate=condition,
                residual_inf_norm_after=after_norm,
            )
        )
        state = accepted_state
        residual = accepted_residual

        if after_norm <= target:
            return finish(True, "residual_converged")

        accepted_step_norm = damping * step_norm
        state_scale = max(1.0, float(np.linalg.norm(state, ord=np.inf)))
        if accepted_step_norm <= controls.step_tolerance * state_scale:
            return finish(False, "step_stagnation")

    return finish(False, "maximum_iterations")


def continue_bipolar_right_contact_potential(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    initial_boundaries: BipolarBoundaryValues,
    target_potential_right: float,
    steps: int,
    parameters: BipolarFVParameters,
    forcing: BipolarForcing | None = None,
    options: NewtonOptions | None = None,
) -> BipolarContinuationResult:
    """Continue the bipolar right reservoir potential through converged states."""

    target = float(target_potential_right)
    if not isfinite(target):
        raise ValueError("target_potential_right must be finite")
    if int(steps) != steps or steps < 1:
        raise ValueError("steps must be a positive integer")

    state = np.asarray(initial_state, dtype=float).copy()
    records: list[BipolarContinuationStep] = []
    potentials = np.linspace(
        initial_boundaries.potential_right,
        target,
        int(steps) + 1,
    )[1:]

    for potential_right in potentials:
        boundaries = BipolarBoundaryValues(
            potential_left=initial_boundaries.potential_left,
            potential_right=float(potential_right),
            electron_density_left=initial_boundaries.electron_density_left,
            electron_density_right=initial_boundaries.electron_density_right,
            hole_density_left=initial_boundaries.hole_density_left,
            hole_density_right=initial_boundaries.hole_density_right,
        )
        result = solve_bipolar_damped_newton(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            forcing=forcing,
            options=options,
        )
        records.append(
            BipolarContinuationStep(
                potential_right=float(potential_right),
                result=result,
            )
        )
        state = result.state.copy()
        if not result.converged:
            return BipolarContinuationResult(
                steps=tuple(records),
                completed=False,
                final_state=state,
            )

    return BipolarContinuationResult(
        steps=tuple(records),
        completed=True,
        final_state=state,
    )


def manufactured_bipolar_case(
    *,
    mesh: UniformNodeMesh1D,
    parameters: BipolarFVParameters,
    specification: ManufacturedBipolarSolutionSpec | None = None,
) -> ManufacturedBipolarCase:
    """Construct a smooth exact bipolar state and its continuous forcing."""

    spec = ManufacturedBipolarSolutionSpec() if specification is None else specification
    x = mesh.nodes
    xi = x / mesh.length
    angle = pi * xi
    sine = np.sin(angle)
    cosine = np.cos(angle)
    wave_number = pi / mesh.length

    potential = (
        spec.potential_linear_slope * xi
        + spec.potential_sine_amplitude * sine
    )
    log_electron = (
        log(spec.electron_boundary_density)
        + spec.log_electron_sine_amplitude * sine
    )
    log_hole = (
        log(spec.hole_boundary_density)
        + spec.log_hole_sine_amplitude * sine
    )
    electron = np.exp(log_electron)
    hole = np.exp(log_hole)

    potential_prime = (
        spec.potential_linear_slope / mesh.length
        + spec.potential_sine_amplitude * wave_number * cosine
    )
    potential_second = (
        -spec.potential_sine_amplitude * wave_number**2 * sine
    )
    log_electron_prime = (
        spec.log_electron_sine_amplitude * wave_number * cosine
    )
    log_electron_second = (
        -spec.log_electron_sine_amplitude * wave_number**2 * sine
    )
    log_hole_prime = spec.log_hole_sine_amplitude * wave_number * cosine
    log_hole_second = -spec.log_hole_sine_amplitude * wave_number**2 * sine

    poisson = potential_second - parameters.screening_strength * (
        electron - hole - parameters.fixed_charge_density
    )
    electron_continuity = parameters.electron_diffusion_ratio * electron * (
        log_electron_prime * (log_electron_prime - potential_prime)
        + log_electron_second
        - potential_second
    )
    hole_continuity = -parameters.hole_diffusion_ratio * hole * (
        log_hole_prime * (log_hole_prime + potential_prime)
        + log_hole_second
        + potential_second
    )

    boundaries = BipolarBoundaryValues(
        potential_left=float(potential[0]),
        potential_right=float(potential[-1]),
        electron_density_left=float(electron[0]),
        electron_density_right=float(electron[-1]),
        hole_density_left=float(hole[0]),
        hole_density_right=float(hole[-1]),
    )
    exact_state = pack_bipolar_state(
        potential[1:-1],
        log_electron[1:-1],
        log_hole[1:-1],
    )
    return ManufacturedBipolarCase(
        boundaries=boundaries,
        exact_state=exact_state,
        exact_potential=potential,
        exact_electron_density=electron,
        exact_hole_density=hole,
        forcing=BipolarForcing(
            poisson=poisson[1:-1],
            electron_continuity=electron_continuity[1:-1],
            hole_continuity=hole_continuity[1:-1],
        ),
    )


def _observed_orders(
    spacings: Sequence[float],
    errors: Sequence[float],
) -> tuple[float, ...]:
    if len(spacings) != len(errors):
        raise ValueError("spacings and errors must have equal length")
    orders: list[float] = []
    for coarse_h, fine_h, coarse_error, fine_error in zip(
        spacings[:-1],
        spacings[1:],
        errors[:-1],
        errors[1:],
        strict=True,
    ):
        if coarse_error <= 0.0 or fine_error <= 0.0:
            raise ValueError("observed order requires positive errors")
        orders.append(
            float(
                np.log(coarse_error / fine_error)
                / np.log(coarse_h / fine_h)
            )
        )
    return tuple(orders)


def manufactured_bipolar_refinement_study(
    intervals: Sequence[int],
    *,
    length: float,
    parameters: BipolarFVParameters,
    specification: ManufacturedBipolarSolutionSpec | None = None,
    options: NewtonOptions | None = None,
) -> BipolarRefinementStudy:
    """Solve a continuous manufactured bipolar case over several meshes."""

    interval_values = tuple(int(value) for value in intervals)
    if len(interval_values) < 3:
        raise ValueError("at least three mesh levels are required")
    if any(value < 3 for value in interval_values):
        raise ValueError("each interval count must be at least three")
    if any(
        later <= earlier
        for earlier, later in zip(
            interval_values[:-1],
            interval_values[1:],
            strict=True,
        )
    ):
        raise ValueError("interval counts must be strictly increasing")

    controls = NewtonOptions() if options is None else options
    records: list[BipolarRefinementRecord] = []
    for interval_count in interval_values:
        mesh = UniformNodeMesh1D(length=length, intervals=interval_count)
        case = manufactured_bipolar_case(
            mesh=mesh,
            parameters=parameters,
            specification=specification,
        )
        initial = linear_bipolar_reservoir_state(
            mesh=mesh,
            boundaries=case.boundaries,
        )
        result = solve_bipolar_damped_newton(
            initial,
            mesh=mesh,
            boundaries=case.boundaries,
            parameters=parameters,
            forcing=case.forcing,
            options=controls,
        )
        if not result.converged:
            raise RuntimeError(
                "manufactured bipolar solve failed: "
                f"{result.termination_reason}"
            )
        reconstructed = reconstruct_bipolar_state(
            result.state,
            mesh=mesh,
            boundaries=case.boundaries,
        )
        potential_error = reconstructed.potential - case.exact_potential
        electron_error = (
            reconstructed.electron_density - case.exact_electron_density
        )
        hole_error = reconstructed.hole_density - case.exact_hole_density
        records.append(
            BipolarRefinementRecord(
                intervals=interval_count,
                spacing=mesh.spacing,
                potential_linf_error=float(np.max(np.abs(potential_error))),
                electron_linf_error=float(np.max(np.abs(electron_error))),
                hole_linf_error=float(np.max(np.abs(hole_error))),
                potential_l2_error=float(
                    np.sqrt(mesh.spacing * np.sum(potential_error**2))
                ),
                electron_l2_error=float(
                    np.sqrt(mesh.spacing * np.sum(electron_error**2))
                ),
                hole_l2_error=float(
                    np.sqrt(mesh.spacing * np.sum(hole_error**2))
                ),
                iterations=result.iterations,
                final_residual_inf_norm=result.final_residual_inf_norm,
                electron_balance_relative_mismatch=(
                    result.continuity_balance.electron_relative_mismatch
                ),
                hole_balance_relative_mismatch=(
                    result.continuity_balance.hole_relative_mismatch
                ),
            )
        )

    spacings = tuple(record.spacing for record in records)
    return BipolarRefinementStudy(
        records=tuple(records),
        potential_linf_orders=_observed_orders(
            spacings,
            tuple(record.potential_linf_error for record in records),
        ),
        electron_linf_orders=_observed_orders(
            spacings,
            tuple(record.electron_linf_error for record in records),
        ),
        hole_linf_orders=_observed_orders(
            spacings,
            tuple(record.hole_linf_error for record in records),
        ),
    )
