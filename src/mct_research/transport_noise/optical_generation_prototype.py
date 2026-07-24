"""Uniform optical pair-generation gate for the R06 trap architecture.

This Phase 1C module adds one non-negative dimensionless pair-generation rate
to the verified reversible trap model. Generation creates one mobile electron
and one mobile hole and does not act directly on trap occupancy or Poisson.
The module verifies deterministic source signs and balance only; it is not an
optical absorption, quantum-efficiency, responsivity, or HgCdTe prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .bipolar_prototype import BipolarBoundaryValues, BipolarFVParameters, hole_face_current
from .finite_volume_prototype import UniformNodeMesh1D, electron_face_current
from .nonlinear_verification import NewtonOptions
from .trap_kinetics_prototype import (
    ReversibleTrapParameters,
    TrapChannelRates,
    TrapNewtonIteration,
    assemble_trap_bipolar_jacobian,
    assemble_trap_bipolar_residual,
    reconstruct_trap_state,
    reversible_trap_channel_rates,
)


@dataclass(frozen=True)
class UniformOpticalGeneration:
    """Dimensionless spatially uniform mobile-pair generation rate."""

    pair_generation_rate: float

    def __post_init__(self) -> None:
        rate = float(self.pair_generation_rate)
        if not isfinite(rate) or rate < 0.0:
            raise ValueError("pair_generation_rate must be finite and non-negative")
        object.__setattr__(self, "pair_generation_rate", rate)


@dataclass(frozen=True)
class OpticalBalanceMetrics:
    """Independent generation, trap, carrier, and current diagnostics."""

    channel_rates: TrapChannelRates
    generation_rate: NDArray[np.float64]
    integrated_generation: float
    integrated_net_electron_capture: float
    integrated_net_hole_capture: float
    integrated_trap_kinetic_rate: float
    electron_terminal_difference: float
    hole_terminal_difference: float
    electron_absolute_mismatch: float
    electron_relative_mismatch: float
    hole_absolute_mismatch: float
    hole_relative_mismatch: float
    trap_absolute_mismatch: float
    trap_relative_mismatch: float
    total_current: NDArray[np.float64]
    total_current_terminal_difference: float
    total_current_maximum_absolute_variation: float
    total_current_relative_variation: float


@dataclass(frozen=True)
class OpticalNewtonResult:
    """Damped-Newton result for the uniformly generated trap system."""

    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    target_residual_inf_norm: float
    history: tuple[TrapNewtonIteration, ...]
    balance: OpticalBalanceMetrics


def assemble_illuminated_trap_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    optical_generation: UniformOpticalGeneration,
) -> NDArray[np.float64]:
    """Add uniform pair generation to the four-block trap residual.

    With net electron capture ``A``, net hole capture ``B``, and pair
    generation ``G``, the steady kinetic residuals are

    ``R_n = div(j_n) - A + G``

    ``R_p = div(j_p) + B - G``

    ``R_f = A - B``.

    Generation therefore cancels from the local charge equation.
    """

    result = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap_parameters,
    ).copy()
    count = mesh.interior_count
    generation = optical_generation.pair_generation_rate
    result[count : 2 * count] += generation
    result[2 * count : 3 * count] -= generation
    return result


def assemble_illuminated_trap_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    optical_generation: UniformOpticalGeneration,
) -> NDArray[np.float64]:
    """Return the trap Jacobian; uniform generation is state independent."""

    _ = optical_generation
    return assemble_trap_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap_parameters,
    )


def optical_balance_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    optical_generation: UniformOpticalGeneration,
) -> OpticalBalanceMetrics:
    """Evaluate generation-recombination and total-current balances."""

    reconstructed = reconstruct_trap_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    rates = reversible_trap_channel_rates(
        reconstructed.electron_density[1:-1],
        reconstructed.hole_density[1:-1],
        reconstructed.trap_occupancy,
        trap_parameters=trap_parameters,
    )
    generation = np.full(
        mesh.interior_count,
        optical_generation.pair_generation_rate,
        dtype=float,
    )
    electron_current = electron_face_current(
        reconstructed.potential,
        reconstructed.electron_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.electron_diffusion_ratio,
    )
    hole_current = hole_face_current(
        reconstructed.potential,
        reconstructed.hole_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.hole_diffusion_ratio,
    )
    integrated_generation = mesh.spacing * float(np.sum(generation))
    integrated_electron = mesh.spacing * float(
        np.sum(rates.net_electron_capture)
    )
    integrated_hole = mesh.spacing * float(np.sum(rates.net_hole_capture))
    integrated_trap = mesh.spacing * float(np.sum(rates.trap_kinetic_rate))
    electron_terminal = float(electron_current[-1] - electron_current[0])
    hole_terminal = float(hole_current[-1] - hole_current[0])
    electron_target = integrated_electron - integrated_generation
    hole_target = integrated_generation - integrated_hole
    electron_mismatch = electron_terminal - electron_target
    hole_mismatch = hole_terminal - hole_target
    electron_scale = max(1.0, abs(electron_terminal), abs(electron_target))
    hole_scale = max(1.0, abs(hole_terminal), abs(hole_target))
    trap_scale = max(1.0, abs(integrated_electron), abs(integrated_hole))

    total_current = electron_current + hole_current
    total_terminal = float(total_current[-1] - total_current[0])
    total_variation = float(np.max(total_current) - np.min(total_current))
    total_scale = max(1.0, float(np.max(np.abs(total_current))))
    return OpticalBalanceMetrics(
        channel_rates=rates,
        generation_rate=generation,
        integrated_generation=integrated_generation,
        integrated_net_electron_capture=integrated_electron,
        integrated_net_hole_capture=integrated_hole,
        integrated_trap_kinetic_rate=integrated_trap,
        electron_terminal_difference=electron_terminal,
        hole_terminal_difference=hole_terminal,
        electron_absolute_mismatch=abs(electron_mismatch),
        electron_relative_mismatch=abs(electron_mismatch) / electron_scale,
        hole_absolute_mismatch=abs(hole_mismatch),
        hole_relative_mismatch=abs(hole_mismatch) / hole_scale,
        trap_absolute_mismatch=abs(integrated_trap),
        trap_relative_mismatch=abs(integrated_trap) / trap_scale,
        total_current=total_current,
        total_current_terminal_difference=total_terminal,
        total_current_maximum_absolute_variation=abs(total_variation),
        total_current_relative_variation=abs(total_variation) / total_scale,
    )


def _block_norms(
    residual: NDArray[np.float64],
    count: int,
) -> tuple[float, float, float, float]:
    return (
        float(np.linalg.norm(residual[:count], ord=np.inf)),
        float(np.linalg.norm(residual[count : 2 * count], ord=np.inf)),
        float(np.linalg.norm(residual[2 * count : 3 * count], ord=np.inf)),
        float(np.linalg.norm(residual[3 * count :], ord=np.inf)),
    )


def _safe_residual(
    state: NDArray[np.float64],
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    optical_generation: UniformOpticalGeneration,
) -> NDArray[np.float64] | None:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            residual = assemble_illuminated_trap_residual(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap_parameters,
                optical_generation=optical_generation,
            )
    except (ValueError, FloatingPointError, OverflowError):
        return None
    if not np.all(np.isfinite(residual)):
        return None
    return residual


def solve_illuminated_trap_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    optical_generation: UniformOpticalGeneration,
    options: NewtonOptions | None = None,
) -> OpticalNewtonResult:
    """Solve the uniform-generation trap system with damped Newton."""

    controls = NewtonOptions() if options is None else options
    state = np.asarray(initial_state, dtype=float)
    if state.ndim != 1 or state.size != 4 * mesh.interior_count:
        raise ValueError("initial_state has incompatible shape")
    if not np.all(np.isfinite(state)):
        raise ValueError("initial_state must contain only finite values")
    state = state.copy()
    residual = _safe_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap_parameters,
        optical_generation=optical_generation,
    )
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")
    initial_norm = float(np.linalg.norm(residual, ord=np.inf))
    target = max(
        controls.absolute_tolerance,
        controls.relative_tolerance * max(1.0, initial_norm),
    )
    history: list[TrapNewtonIteration] = []

    def finish(converged: bool, reason: str) -> OpticalNewtonResult:
        final_residual = _safe_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap_parameters,
            optical_generation=optical_generation,
        )
        final_norm = (
            float("inf")
            if final_residual is None
            else float(np.linalg.norm(final_residual, ord=np.inf))
        )
        return OpticalNewtonResult(
            state=state.copy(),
            converged=converged,
            termination_reason=reason,
            iterations=len(history),
            initial_residual_inf_norm=initial_norm,
            final_residual_inf_norm=final_norm,
            target_residual_inf_norm=target,
            history=tuple(history),
            balance=optical_balance_metrics(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap_parameters,
                optical_generation=optical_generation,
            ),
        )

    if initial_norm <= target:
        return finish(True, "initial_residual_converged")

    for iteration in range(controls.maximum_iterations):
        poisson_norm, electron_norm, hole_norm, trap_norm = _block_norms(
            residual,
            mesh.interior_count,
        )
        jacobian = assemble_illuminated_trap_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap_parameters,
            optical_generation=optical_generation,
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
                trap_parameters=trap_parameters,
                optical_generation=optical_generation,
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
            TrapNewtonIteration(
                iteration=iteration,
                residual_inf_norm_before=float(
                    np.linalg.norm(residual, ord=np.inf)
                ),
                poisson_inf_norm_before=poisson_norm,
                electron_continuity_inf_norm_before=electron_norm,
                hole_continuity_inf_norm_before=hole_norm,
                trap_kinetic_inf_norm_before=trap_norm,
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
