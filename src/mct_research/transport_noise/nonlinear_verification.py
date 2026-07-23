"""Nonlinear verification tools for the restricted R06 unipolar kernel.

This module remains a Phase 1C numerical-verification package. It provides
residual-decreasing damped Newton iteration, voltage continuation,
manufactured forcing, and mesh refinement for the existing dimensionless
steady unipolar finite-volume residual. It does not add HgCdTe material
parameters, bipolar transport, traps, optical generation, stochastic
operators, or terminal PSDs.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite, pi

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .finite_volume_prototype import (
    CurrentConservationMetrics,
    UniformNodeMesh1D,
    UnipolarBoundaryValues,
    UnipolarFVParameters,
    assemble_unipolar_jacobian,
    assemble_unipolar_residual,
    current_conservation_metrics,
    pack_unipolar_state,
    reconstruct_unipolar_state,
)


@dataclass(frozen=True)
class UnipolarForcing:
    """Interior forcing values for Poisson and continuity residuals."""

    poisson: NDArray[np.float64]
    continuity: NDArray[np.float64]

    def vector(self, interior_count: int) -> NDArray[np.float64]:
        poisson = np.asarray(self.poisson, dtype=float)
        continuity = np.asarray(self.continuity, dtype=float)
        expected = (interior_count,)
        if poisson.shape != expected or continuity.shape != expected:
            raise ValueError("forcing arrays must match the mesh interior count")
        if not np.all(np.isfinite(poisson)) or not np.all(np.isfinite(continuity)):
            raise ValueError("forcing arrays must contain only finite values")
        return np.concatenate([poisson, continuity])


@dataclass(frozen=True)
class NewtonOptions:
    """Controls for residual-decreasing damped Newton iteration."""

    maximum_iterations: int = 40
    absolute_tolerance: float = 1.0e-11
    relative_tolerance: float = 1.0e-10
    step_tolerance: float = 1.0e-12
    armijo_fraction: float = 1.0e-4
    backtrack_factor: float = 0.5
    minimum_damping: float = 2.0**-20
    maximum_backtracks: int = 24

    def __post_init__(self) -> None:
        if (
            int(self.maximum_iterations) != self.maximum_iterations
            or self.maximum_iterations < 1
        ):
            raise ValueError("maximum_iterations must be a positive integer")
        if (
            int(self.maximum_backtracks) != self.maximum_backtracks
            or self.maximum_backtracks < 0
        ):
            raise ValueError("maximum_backtracks must be a non-negative integer")
        for name in (
            "absolute_tolerance",
            "relative_tolerance",
            "step_tolerance",
            "armijo_fraction",
            "minimum_damping",
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        factor = float(self.backtrack_factor)
        if not isfinite(factor) or not 0.0 < factor < 1.0:
            raise ValueError(
                "backtrack_factor must lie strictly between zero and one"
            )
        if not 0.0 < self.armijo_fraction < 1.0:
            raise ValueError(
                "armijo_fraction must lie strictly between zero and one"
            )
        if self.minimum_damping > 1.0:
            raise ValueError("minimum_damping must not exceed one")


@dataclass(frozen=True)
class NewtonIteration:
    """One accepted Newton iteration."""

    iteration: int
    residual_inf_norm_before: float
    poisson_inf_norm_before: float
    continuity_inf_norm_before: float
    step_inf_norm: float
    accepted_damping: float
    backtracks: int
    jacobian_condition_estimate: float
    residual_inf_norm_after: float


@dataclass(frozen=True)
class NewtonResult:
    """Damped Newton result with explicit termination diagnostics."""

    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    target_residual_inf_norm: float
    history: tuple[NewtonIteration, ...]
    current_conservation: CurrentConservationMetrics


@dataclass(frozen=True)
class ContinuationStep:
    """One accepted or failed voltage-continuation point."""

    potential_right: float
    result: NewtonResult


@dataclass(frozen=True)
class ContinuationResult:
    """Sequence of voltage-continuation solves."""

    steps: tuple[ContinuationStep, ...]
    completed: bool
    final_state: NDArray[np.float64]


@dataclass(frozen=True)
class ManufacturedSolutionSpec:
    """Smooth positive manufactured state on ``0 <= x <= L``."""

    potential_linear_slope: float = 0.4
    potential_sine_amplitude: float = 0.12
    log_density_sine_amplitude: float = 0.20

    def __post_init__(self) -> None:
        values = (
            self.potential_linear_slope,
            self.potential_sine_amplitude,
            self.log_density_sine_amplitude,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("manufactured-solution coefficients must be finite")


@dataclass(frozen=True)
class ManufacturedCase:
    """Sampled exact state, boundaries, and continuous forcing on one mesh."""

    boundaries: UnipolarBoundaryValues
    exact_state: NDArray[np.float64]
    exact_potential: NDArray[np.float64]
    exact_density: NDArray[np.float64]
    forcing: UnipolarForcing


@dataclass(frozen=True)
class RefinementRecord:
    """Manufactured-solution error on one mesh."""

    intervals: int
    spacing: float
    potential_linf_error: float
    density_linf_error: float
    potential_l2_error: float
    density_l2_error: float
    iterations: int
    face_current_relative_variation: float


@dataclass(frozen=True)
class RefinementStudy:
    """Mesh-refinement records and observed consecutive orders."""

    records: tuple[RefinementRecord, ...]
    potential_linf_orders: tuple[float, ...]
    density_linf_orders: tuple[float, ...]


@dataclass(frozen=True)
class SparseCOOMatrix:
    """Dependency-free coordinate representation used for equality checks."""

    shape: tuple[int, int]
    row: NDArray[np.int64]
    column: NDArray[np.int64]
    data: NDArray[np.float64]

    def to_dense(self) -> NDArray[np.float64]:
        dense = np.zeros(self.shape, dtype=float)
        np.add.at(dense, (self.row, self.column), self.data)
        return dense


def assemble_forced_unipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
    forcing: UnipolarForcing | None = None,
) -> NDArray[np.float64]:
    """Return the base residual minus declared interior forcing."""

    residual = assemble_unipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    if forcing is None:
        return residual
    return residual - forcing.vector(mesh.interior_count)


def linear_reservoir_state(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
) -> NDArray[np.float64]:
    """Return a linear-potential, linear-log-density interior initial state."""

    fraction = mesh.nodes / mesh.length
    potential = (
        boundaries.potential_left
        + fraction * (boundaries.potential_right - boundaries.potential_left)
    )
    log_density = (
        np.log(boundaries.density_left)
        + fraction
        * (np.log(boundaries.density_right) - np.log(boundaries.density_left))
    )
    return pack_unipolar_state(potential[1:-1], log_density[1:-1])


def jacobian_as_coo(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
    drop_tolerance: float = 0.0,
) -> SparseCOOMatrix:
    """Serialize the verified dense Jacobian as a dependency-free COO matrix.

    This is an equality and storage-layout gate, not an independent sparse
    assembly and not a sparse linear solver.
    """

    tolerance = float(drop_tolerance)
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("drop_tolerance must be finite and non-negative")
    dense = assemble_unipolar_jacobian(
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
) -> tuple[float, float]:
    poisson = float(np.linalg.norm(residual[:interior_count], ord=np.inf))
    continuity = float(np.linalg.norm(residual[interior_count:], ord=np.inf))
    return poisson, continuity


def _safe_residual(
    state: NDArray[np.float64],
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
    forcing: UnipolarForcing | None,
) -> NDArray[np.float64] | None:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            residual = assemble_forced_unipolar_residual(
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


def solve_unipolar_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
    forcing: UnipolarForcing | None = None,
    options: NewtonOptions | None = None,
) -> NewtonResult:
    """Solve the restricted nonlinear system with residual-decreasing damping."""

    controls = NewtonOptions() if options is None else options
    state = np.asarray(initial_state, dtype=float)
    if state.ndim != 1 or state.size != 2 * mesh.interior_count:
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
    history: list[NewtonIteration] = []

    def finish(converged: bool, reason: str) -> NewtonResult:
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
        return NewtonResult(
            state=state.copy(),
            converged=converged,
            termination_reason=reason,
            iterations=len(history),
            initial_residual_inf_norm=initial_norm,
            final_residual_inf_norm=final_norm,
            target_residual_inf_norm=target,
            history=tuple(history),
            current_conservation=current_conservation_metrics(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
            ),
        )

    if initial_norm <= target:
        return finish(True, "initial_residual_converged")

    for iteration in range(controls.maximum_iterations):
        poisson_norm, continuity_norm = _block_norms(
            residual,
            mesh.interior_count,
        )
        jacobian = assemble_unipolar_jacobian(
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
            NewtonIteration(
                iteration=iteration,
                residual_inf_norm_before=float(
                    np.linalg.norm(residual, ord=np.inf)
                ),
                poisson_inf_norm_before=poisson_norm,
                continuity_inf_norm_before=continuity_norm,
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


def continue_right_contact_potential(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    initial_boundaries: UnipolarBoundaryValues,
    target_potential_right: float,
    steps: int,
    parameters: UnipolarFVParameters,
    forcing: UnipolarForcing | None = None,
    options: NewtonOptions | None = None,
) -> ContinuationResult:
    """Continue the right reservoir potential using each converged state."""

    target = float(target_potential_right)
    if not isfinite(target):
        raise ValueError("target_potential_right must be finite")
    if int(steps) != steps or steps < 1:
        raise ValueError("steps must be a positive integer")

    state = np.asarray(initial_state, dtype=float).copy()
    records: list[ContinuationStep] = []
    potentials = np.linspace(
        initial_boundaries.potential_right,
        target,
        int(steps) + 1,
    )[1:]

    for potential_right in potentials:
        boundaries = UnipolarBoundaryValues(
            potential_left=initial_boundaries.potential_left,
            potential_right=float(potential_right),
            density_left=initial_boundaries.density_left,
            density_right=initial_boundaries.density_right,
        )
        result = solve_unipolar_damped_newton(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            forcing=forcing,
            options=options,
        )
        records.append(
            ContinuationStep(
                potential_right=float(potential_right),
                result=result,
            )
        )
        state = result.state.copy()
        if not result.converged:
            return ContinuationResult(
                steps=tuple(records),
                completed=False,
                final_state=state,
            )

    return ContinuationResult(
        steps=tuple(records),
        completed=True,
        final_state=state,
    )


def manufactured_unipolar_case(
    *,
    mesh: UniformNodeMesh1D,
    parameters: UnipolarFVParameters,
    specification: ManufacturedSolutionSpec | None = None,
) -> ManufacturedCase:
    """Return a smooth manufactured solution and its continuous forcing."""

    spec = ManufacturedSolutionSpec() if specification is None else specification
    x = mesh.nodes
    wave_number = pi / mesh.length
    sine = np.sin(wave_number * x)
    cosine = np.cos(wave_number * x)

    slope = spec.potential_linear_slope
    potential_amplitude = spec.potential_sine_amplitude
    density_amplitude = spec.log_density_sine_amplitude

    potential = slope * x + potential_amplitude * sine
    density = np.exp(density_amplitude * sine)
    boundaries = UnipolarBoundaryValues(
        potential_left=float(potential[0]),
        potential_right=float(potential[-1]),
        density_left=float(density[0]),
        density_right=float(density[-1]),
    )
    exact_state = pack_unipolar_state(
        potential[1:-1],
        np.log(density[1:-1]),
    )

    poisson_forcing = (
        -potential_amplitude * wave_number**2 * sine[1:-1]
        - parameters.screening_strength
        * (density[1:-1] - parameters.background_density)
    )

    current_factor = (
        -slope
        + (density_amplitude - potential_amplitude)
        * wave_number
        * cosine
    )
    continuity_forcing_full = (
        parameters.diffusion_ratio
        * density
        * (
            density_amplitude
            * wave_number
            * cosine
            * current_factor
            - (density_amplitude - potential_amplitude)
            * wave_number**2
            * sine
        )
    )
    forcing = UnipolarForcing(
        poisson=np.asarray(poisson_forcing, dtype=float),
        continuity=np.asarray(continuity_forcing_full[1:-1], dtype=float),
    )
    return ManufacturedCase(
        boundaries=boundaries,
        exact_state=exact_state,
        exact_potential=np.asarray(potential, dtype=float),
        exact_density=np.asarray(density, dtype=float),
        forcing=forcing,
    )


def _observed_orders(
    errors: Sequence[float],
    spacings: Sequence[float],
) -> tuple[float, ...]:
    orders: list[float] = []
    for coarse_error, fine_error, coarse_h, fine_h in zip(
        errors[:-1],
        errors[1:],
        spacings[:-1],
        spacings[1:],
        strict=True,
    ):
        if coarse_error <= 0.0 or fine_error <= 0.0:
            orders.append(float("nan"))
        else:
            orders.append(
                float(
                    np.log(coarse_error / fine_error)
                    / np.log(coarse_h / fine_h)
                )
            )
    return tuple(orders)


def manufactured_refinement_study(
    interval_counts: Sequence[int],
    *,
    parameters: UnipolarFVParameters,
    specification: ManufacturedSolutionSpec | None = None,
    options: NewtonOptions | None = None,
) -> RefinementStudy:
    """Solve the continuous manufactured problem on refined meshes."""

    counts = tuple(int(value) for value in interval_counts)
    if len(counts) < 2 or any(value < 4 for value in counts):
        raise ValueError(
            "interval_counts must contain at least two values >= 4"
        )
    if any(
        fine <= coarse
        for coarse, fine in zip(counts[:-1], counts[1:], strict=True)
    ):
        raise ValueError("interval_counts must be strictly increasing")

    records: list[RefinementRecord] = []
    for intervals in counts:
        mesh = UniformNodeMesh1D(length=1.0, intervals=intervals)
        case = manufactured_unipolar_case(
            mesh=mesh,
            parameters=parameters,
            specification=specification,
        )
        initial_state = linear_reservoir_state(
            mesh=mesh,
            boundaries=case.boundaries,
        )
        result = solve_unipolar_damped_newton(
            initial_state,
            mesh=mesh,
            boundaries=case.boundaries,
            parameters=parameters,
            forcing=case.forcing,
            options=options,
        )
        if not result.converged:
            raise RuntimeError(
                f"manufactured solve failed for intervals={intervals}: "
                f"{result.termination_reason}"
            )
        reconstructed = reconstruct_unipolar_state(
            result.state,
            mesh=mesh,
            boundaries=case.boundaries,
        )
        potential_error = reconstructed.potential - case.exact_potential
        density_error = reconstructed.density - case.exact_density
        records.append(
            RefinementRecord(
                intervals=intervals,
                spacing=mesh.spacing,
                potential_linf_error=float(
                    np.linalg.norm(potential_error, ord=np.inf)
                ),
                density_linf_error=float(
                    np.linalg.norm(density_error, ord=np.inf)
                ),
                potential_l2_error=float(
                    np.sqrt(mesh.spacing * np.sum(potential_error**2))
                ),
                density_l2_error=float(
                    np.sqrt(mesh.spacing * np.sum(density_error**2))
                ),
                iterations=result.iterations,
                face_current_relative_variation=(
                    result.current_conservation.relative_variation
                ),
            )
        )

    spacings = tuple(record.spacing for record in records)
    return RefinementStudy(
        records=tuple(records),
        potential_linf_orders=_observed_orders(
            tuple(record.potential_linf_error for record in records),
            spacings,
        ),
        density_linf_orders=_observed_orders(
            tuple(record.density_linf_error for record in records),
            spacings,
        ),
    )
