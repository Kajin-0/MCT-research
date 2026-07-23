"""Equilibrium-consistent deterministic pair-recombination gate for R06.

This Phase 1C module adds one dimensionless mass-action pair source to the
verified bipolar drift-diffusion-Poisson residual. The source is a numerical
architecture model only. It is not an HgCdTe lifetime law, SRH model, radiative
coefficient, Auger coefficient, trap model, optical-generation model, or
predictive detector relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .bipolar_nonlinear_verification import BipolarNewtonIteration
from .bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    assemble_bipolar_residual,
    hole_face_current,
    reconstruct_bipolar_state,
)
from .finite_volume_prototype import (
    UniformNodeMesh1D,
    electron_face_current,
)
from .nonlinear_verification import NewtonOptions


@dataclass(frozen=True)
class MassActionPairParameters:
    """Dimensionless net-pair source parameters.

    The net annihilation rate is

    ``U = rate_coefficient * (N * P - equilibrium_product)``.

    Positive ``U`` denotes net electron-hole pair annihilation; negative ``U``
    denotes the reverse thermal-generation direction required by detailed
    balance.
    """

    rate_coefficient: float
    equilibrium_product: float = 1.0

    def __post_init__(self) -> None:
        coefficient = float(self.rate_coefficient)
        product = float(self.equilibrium_product)
        if not isfinite(coefficient) or coefficient < 0.0:
            raise ValueError("rate_coefficient must be finite and non-negative")
        if not isfinite(product) or product <= 0.0:
            raise ValueError("equilibrium_product must be finite and positive")
        object.__setattr__(self, "rate_coefficient", coefficient)
        object.__setattr__(self, "equilibrium_product", product)


@dataclass(frozen=True)
class PairBalanceMetrics:
    """Independent local and global diagnostics for the pair source."""

    pair_rate: NDArray[np.float64]
    integrated_pair_rate: float
    electron_terminal_difference: float
    hole_terminal_difference: float
    electron_absolute_mismatch: float
    electron_relative_mismatch: float
    hole_absolute_mismatch: float
    hole_relative_mismatch: float
    total_current: NDArray[np.float64]
    total_current_terminal_difference: float
    total_current_maximum_absolute_variation: float
    total_current_relative_variation: float


@dataclass(frozen=True)
class RecombinationNewtonResult:
    """Damped-Newton result for the mass-action pair-source system."""

    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    target_residual_inf_norm: float
    history: tuple[BipolarNewtonIteration, ...]
    pair_balance: PairBalanceMetrics


def mass_action_pair_rate(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    pair_parameters: MassActionPairParameters,
) -> float | NDArray[np.float64]:
    """Return the local net electron-hole pair annihilation rate."""

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    if electron.shape != hole.shape:
        raise ValueError("electron_density and hole_density must have equal shape")
    if not np.all(np.isfinite(electron)) or not np.all(np.isfinite(hole)):
        raise ValueError("carrier densities must contain only finite values")
    if np.any(electron <= 0.0) or np.any(hole <= 0.0):
        raise ValueError("carrier densities must be positive")
    rate = pair_parameters.rate_coefficient * (
        electron * hole - pair_parameters.equilibrium_product
    )
    if rate.ndim == 0:
        return float(rate)
    return rate


def assemble_recombining_bipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    pair_parameters: MassActionPairParameters,
) -> NDArray[np.float64]:
    r"""Assemble the bipolar residual with an equilibrium-consistent pair source.

    With positive ``U`` denoting net pair annihilation, the steady conventional
    current equations are

    .. math::

        \partial_x j_n - U = 0,

        \partial_x j_p + U = 0.

    The opposite residual signs are required because electron and hole
    conventional currents enter their continuity equations with opposite charge
    signs. Their sum therefore remains source-free:

    .. math::

        \partial_x(j_n+j_p)=0.
    """

    residual = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    count = mesh.interior_count
    pair_rate = np.asarray(
        mass_action_pair_rate(
            reconstructed.electron_density[1:-1],
            reconstructed.hole_density[1:-1],
            pair_parameters=pair_parameters,
        ),
        dtype=float,
    )
    result = residual.copy()
    result[count : 2 * count] -= pair_rate
    result[2 * count :] += pair_rate
    return result


def assemble_recombining_bipolar_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    pair_parameters: MassActionPairParameters,
) -> NDArray[np.float64]:
    """Return the analytical Jacobian including pair-source derivatives."""

    jacobian = assemble_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    count = mesh.interior_count
    derivative = (
        pair_parameters.rate_coefficient
        * reconstructed.electron_density[1:-1]
        * reconstructed.hole_density[1:-1]
    )
    index = np.arange(count)
    electron_row = count + index
    hole_row = 2 * count + index
    electron_column = count + index
    hole_column = 2 * count + index

    jacobian[electron_row, electron_column] -= derivative
    jacobian[electron_row, hole_column] -= derivative
    jacobian[hole_row, electron_column] += derivative
    jacobian[hole_row, hole_column] += derivative
    return jacobian


def pair_balance_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    pair_parameters: MassActionPairParameters,
) -> PairBalanceMetrics:
    r"""Evaluate pair and total-current conservation independently.

    At a converged steady state,

    .. math::

        j_{n,R}-j_{n,L}=h\sum_i U_i,

        j_{p,R}-j_{p,L}=-h\sum_i U_i,

        (j_n+j_p)_R-(j_n+j_p)_L=0.
    """

    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    pair_rate = np.asarray(
        mass_action_pair_rate(
            reconstructed.electron_density[1:-1],
            reconstructed.hole_density[1:-1],
            pair_parameters=pair_parameters,
        ),
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
    integrated = mesh.spacing * float(np.sum(pair_rate))
    electron_terminal = float(electron_current[-1] - electron_current[0])
    hole_terminal = float(hole_current[-1] - hole_current[0])
    electron_mismatch = electron_terminal - integrated
    hole_mismatch = hole_terminal + integrated
    electron_scale = max(1.0, abs(electron_terminal), abs(integrated))
    hole_scale = max(1.0, abs(hole_terminal), abs(integrated))

    total_current = electron_current + hole_current
    total_terminal = float(total_current[-1] - total_current[0])
    total_variation = float(np.max(total_current) - np.min(total_current))
    total_scale = max(1.0, float(np.max(np.abs(total_current))))
    return PairBalanceMetrics(
        pair_rate=pair_rate,
        integrated_pair_rate=integrated,
        electron_terminal_difference=electron_terminal,
        hole_terminal_difference=hole_terminal,
        electron_absolute_mismatch=abs(electron_mismatch),
        electron_relative_mismatch=abs(electron_mismatch) / electron_scale,
        hole_absolute_mismatch=abs(hole_mismatch),
        hole_relative_mismatch=abs(hole_mismatch) / hole_scale,
        total_current=total_current,
        total_current_terminal_difference=total_terminal,
        total_current_maximum_absolute_variation=abs(total_variation),
        total_current_relative_variation=abs(total_variation) / total_scale,
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
    pair_parameters: MassActionPairParameters,
) -> NDArray[np.float64] | None:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            residual = assemble_recombining_bipolar_residual(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                pair_parameters=pair_parameters,
            )
    except (ValueError, FloatingPointError, OverflowError):
        return None
    if not np.all(np.isfinite(residual)):
        return None
    return residual


def solve_recombining_bipolar_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    pair_parameters: MassActionPairParameters,
    options: NewtonOptions | None = None,
) -> RecombinationNewtonResult:
    """Solve the restricted pair-source system with damped Newton iteration."""

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
        pair_parameters=pair_parameters,
    )
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")
    initial_norm = float(np.linalg.norm(residual, ord=np.inf))
    target = max(
        controls.absolute_tolerance,
        controls.relative_tolerance * max(1.0, initial_norm),
    )
    history: list[BipolarNewtonIteration] = []

    def finish(converged: bool, reason: str) -> RecombinationNewtonResult:
        final_residual = _safe_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            pair_parameters=pair_parameters,
        )
        final_norm = (
            float("inf")
            if final_residual is None
            else float(np.linalg.norm(final_residual, ord=np.inf))
        )
        return RecombinationNewtonResult(
            state=state.copy(),
            converged=converged,
            termination_reason=reason,
            iterations=len(history),
            initial_residual_inf_norm=initial_norm,
            final_residual_inf_norm=final_norm,
            target_residual_inf_norm=target,
            history=tuple(history),
            pair_balance=pair_balance_metrics(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                pair_parameters=pair_parameters,
            ),
        )

    if initial_norm <= target:
        return finish(True, "initial_residual_converged")

    for iteration in range(controls.maximum_iterations):
        poisson_norm, electron_norm, hole_norm = _block_norms(
            residual,
            mesh.interior_count,
        )
        jacobian = assemble_recombining_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            pair_parameters=pair_parameters,
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
                pair_parameters=pair_parameters,
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
