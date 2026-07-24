"""Reversible deterministic trap-occupancy gate for R06.

This Phase 1C module adds one bounded trap-occupancy unknown to the verified
steady dimensionless bipolar drift-diffusion-Poisson architecture. The trap is
neutral when empty and carries one electron-like negative charge when occupied.
The four reversible channels are electron capture/emission and hole
capture/emission. Their coefficients are constrained by a declared equilibrium
state so that both channel pairs satisfy detailed balance exactly.

The module is a numerical architecture model only. It is not an identified
HgCdTe defect, an SRH lifetime law, a stochastic trap-noise model, or a
predictive detector relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    assemble_bipolar_residual,
    hole_face_current,
    reconstruct_bipolar_state,
)
from .finite_volume_prototype import UniformNodeMesh1D, electron_face_current
from .nonlinear_verification import NewtonOptions


@dataclass(frozen=True)
class ReversibleTrapParameters:
    """Dimensionless reversible single-level trap parameters.

    The occupied trap carries one electron-like charge. Empty traps are
    neutral. Emission coefficients are derived from the equilibrium state:

    ``e_n = c_n * N_eq * (1-f_eq) / f_eq``

    ``e_p = c_p * P_eq * f_eq / (1-f_eq)``

    so electron and hole channel pairs each satisfy detailed balance.
    """

    trap_density: float
    electron_capture_coefficient: float
    hole_capture_coefficient: float
    equilibrium_electron_density: float = 1.0
    equilibrium_hole_density: float = 1.0
    equilibrium_occupancy: float = 0.5

    def __post_init__(self) -> None:
        trap_density = float(self.trap_density)
        electron_capture = float(self.electron_capture_coefficient)
        hole_capture = float(self.hole_capture_coefficient)
        electron_equilibrium = float(self.equilibrium_electron_density)
        hole_equilibrium = float(self.equilibrium_hole_density)
        occupancy = float(self.equilibrium_occupancy)
        if not isfinite(trap_density) or trap_density < 0.0:
            raise ValueError("trap_density must be finite and non-negative")
        if not isfinite(electron_capture) or electron_capture <= 0.0:
            raise ValueError(
                "electron_capture_coefficient must be finite and positive"
            )
        if not isfinite(hole_capture) or hole_capture <= 0.0:
            raise ValueError("hole_capture_coefficient must be finite and positive")
        if not isfinite(electron_equilibrium) or electron_equilibrium <= 0.0:
            raise ValueError(
                "equilibrium_electron_density must be finite and positive"
            )
        if not isfinite(hole_equilibrium) or hole_equilibrium <= 0.0:
            raise ValueError("equilibrium_hole_density must be finite and positive")
        if not isfinite(occupancy) or not 0.0 < occupancy < 1.0:
            raise ValueError("equilibrium_occupancy must lie strictly between 0 and 1")
        object.__setattr__(self, "trap_density", trap_density)
        object.__setattr__(
            self, "electron_capture_coefficient", electron_capture
        )
        object.__setattr__(self, "hole_capture_coefficient", hole_capture)
        object.__setattr__(
            self, "equilibrium_electron_density", electron_equilibrium
        )
        object.__setattr__(self, "equilibrium_hole_density", hole_equilibrium)
        object.__setattr__(self, "equilibrium_occupancy", occupancy)

    @property
    def electron_emission_coefficient(self) -> float:
        occupancy = self.equilibrium_occupancy
        return (
            self.electron_capture_coefficient
            * self.equilibrium_electron_density
            * (1.0 - occupancy)
            / occupancy
        )

    @property
    def hole_emission_coefficient(self) -> float:
        occupancy = self.equilibrium_occupancy
        return (
            self.hole_capture_coefficient
            * self.equilibrium_hole_density
            * occupancy
            / (1.0 - occupancy)
        )

    @property
    def equilibrium_product(self) -> float:
        return self.equilibrium_electron_density * self.equilibrium_hole_density


@dataclass(frozen=True)
class TrapChannelRates:
    """Four reversible volumetric channel rates and their net combinations."""

    electron_capture: NDArray[np.float64]
    electron_emission: NDArray[np.float64]
    hole_capture: NDArray[np.float64]
    hole_emission: NDArray[np.float64]
    net_electron_capture: NDArray[np.float64]
    net_hole_capture: NDArray[np.float64]
    trap_kinetic_rate: NDArray[np.float64]


@dataclass(frozen=True)
class ReconstructedTrapState:
    """Full mobile-carrier state and bounded interior trap occupancy."""

    potential: NDArray[np.float64]
    electron_density: NDArray[np.float64]
    hole_density: NDArray[np.float64]
    trap_occupancy: NDArray[np.float64]


@dataclass(frozen=True)
class TrapBalanceMetrics:
    """Independent carrier, trap, charge, and current-balance diagnostics."""

    channel_rates: TrapChannelRates
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
class TrapNewtonIteration:
    """One accepted damped-Newton step for the four-block trap system."""

    iteration: int
    residual_inf_norm_before: float
    poisson_inf_norm_before: float
    electron_continuity_inf_norm_before: float
    hole_continuity_inf_norm_before: float
    trap_kinetic_inf_norm_before: float
    step_inf_norm: float
    accepted_damping: float
    backtracks: int
    jacobian_condition_estimate: float
    residual_inf_norm_after: float


@dataclass(frozen=True)
class TrapNewtonResult:
    """Damped-Newton result for the reversible trap system."""

    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    target_residual_inf_norm: float
    history: tuple[TrapNewtonIteration, ...]
    balance: TrapBalanceMetrics


def occupancy_from_logit(logit_occupancy: ArrayLike) -> float | NDArray[np.float64]:
    """Map unconstrained logits to occupancies strictly between zero and one."""

    logit = np.asarray(logit_occupancy, dtype=float)
    if not np.all(np.isfinite(logit)):
        raise ValueError("logit_occupancy must contain only finite values")
    result = np.empty_like(logit, dtype=float)
    nonnegative = logit >= 0.0
    result[nonnegative] = 1.0 / (1.0 + np.exp(-logit[nonnegative]))
    exponential = np.exp(logit[~nonnegative])
    result[~nonnegative] = exponential / (1.0 + exponential)
    result = np.clip(
        result,
        np.nextafter(0.0, 1.0),
        np.nextafter(1.0, 0.0),
    )
    if result.ndim == 0:
        return float(result)
    return result


def logit_from_occupancy(occupancy: ArrayLike) -> float | NDArray[np.float64]:
    """Map occupancies in ``(0,1)`` to unconstrained logits."""

    value = np.asarray(occupancy, dtype=float)
    if not np.all(np.isfinite(value)) or np.any(value <= 0.0) or np.any(value >= 1.0):
        raise ValueError("occupancy must lie strictly between zero and one")
    result = np.log(value) - np.log1p(-value)
    if result.ndim == 0:
        return float(result)
    return result


def pack_trap_state(
    potential_interior: ArrayLike,
    log_electron_density_interior: ArrayLike,
    log_hole_density_interior: ArrayLike,
    logit_trap_occupancy_interior: ArrayLike,
) -> NDArray[np.float64]:
    """Pack the four interior unknown blocks into one vector."""

    blocks = [
        np.asarray(potential_interior, dtype=float),
        np.asarray(log_electron_density_interior, dtype=float),
        np.asarray(log_hole_density_interior, dtype=float),
        np.asarray(logit_trap_occupancy_interior, dtype=float),
    ]
    if any(block.ndim != 1 for block in blocks):
        raise ValueError("state arrays must be one-dimensional")
    if len({block.shape for block in blocks}) != 1:
        raise ValueError("state arrays must have equal shape")
    if not all(np.all(np.isfinite(block)) for block in blocks):
        raise ValueError("state arrays must contain only finite values")
    return np.concatenate(blocks)


def reconstruct_trap_state(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
) -> ReconstructedTrapState:
    """Reconstruct mobile carriers and bounded interior trap occupancy."""

    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    if vector.ndim != 1 or vector.size != 4 * count:
        raise ValueError("state has incompatible shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("state must contain only finite values")
    mobile = reconstruct_bipolar_state(
        vector[: 3 * count],
        mesh=mesh,
        boundaries=boundaries,
    )
    occupancy = np.asarray(occupancy_from_logit(vector[3 * count :]), dtype=float)
    return ReconstructedTrapState(
        potential=mobile.potential,
        electron_density=mobile.electron_density,
        hole_density=mobile.hole_density,
        trap_occupancy=occupancy,
    )


def reversible_trap_channel_rates(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    trap_occupancy: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
) -> TrapChannelRates:
    """Evaluate all four reversible trap channels and net rates."""

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    occupancy = np.asarray(trap_occupancy, dtype=float)
    if electron.shape != hole.shape or electron.shape != occupancy.shape:
        raise ValueError("electron, hole, and occupancy arrays must have equal shape")
    if not (
        np.all(np.isfinite(electron))
        and np.all(np.isfinite(hole))
        and np.all(np.isfinite(occupancy))
    ):
        raise ValueError("rate inputs must contain only finite values")
    if np.any(electron <= 0.0) or np.any(hole <= 0.0):
        raise ValueError("carrier densities must be positive")
    if np.any(occupancy <= 0.0) or np.any(occupancy >= 1.0):
        raise ValueError("trap occupancy must lie strictly between zero and one")

    density = trap_parameters.trap_density
    empty = 1.0 - occupancy
    electron_capture = (
        density
        * trap_parameters.electron_capture_coefficient
        * electron
        * empty
    )
    electron_emission = (
        density * trap_parameters.electron_emission_coefficient * occupancy
    )
    hole_capture = (
        density * trap_parameters.hole_capture_coefficient * hole * occupancy
    )
    hole_emission = density * trap_parameters.hole_emission_coefficient * empty
    net_electron = electron_capture - electron_emission
    net_hole = hole_capture - hole_emission
    return TrapChannelRates(
        electron_capture=electron_capture,
        electron_emission=electron_emission,
        hole_capture=hole_capture,
        hole_emission=hole_emission,
        net_electron_capture=net_electron,
        net_hole_capture=net_hole,
        trap_kinetic_rate=net_electron - net_hole,
    )


def steady_trap_occupancy(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
) -> float | NDArray[np.float64]:
    """Return occupancy satisfying zero local trap-kinetic residual."""

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    if electron.shape != hole.shape:
        raise ValueError("electron_density and hole_density must have equal shape")
    if not np.all(np.isfinite(electron)) or not np.all(np.isfinite(hole)):
        raise ValueError("carrier densities must contain only finite values")
    if np.any(electron <= 0.0) or np.any(hole <= 0.0):
        raise ValueError("carrier densities must be positive")
    numerator = (
        trap_parameters.electron_capture_coefficient * electron
        + trap_parameters.hole_emission_coefficient
    )
    denominator = (
        numerator
        + trap_parameters.electron_emission_coefficient
        + trap_parameters.hole_capture_coefficient * hole
    )
    result = numerator / denominator
    if result.ndim == 0:
        return float(result)
    return result


def effective_mass_action_coefficient(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
) -> float | NDArray[np.float64]:
    """Return the positive state-dependent eliminated pair coefficient."""

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    if electron.shape != hole.shape:
        raise ValueError("electron_density and hole_density must have equal shape")
    if not np.all(np.isfinite(electron)) or not np.all(np.isfinite(hole)):
        raise ValueError("carrier densities must contain only finite values")
    if np.any(electron <= 0.0) or np.any(hole <= 0.0):
        raise ValueError("carrier densities must be positive")
    denominator = (
        trap_parameters.electron_capture_coefficient * electron
        + trap_parameters.hole_emission_coefficient
        + trap_parameters.electron_emission_coefficient
        + trap_parameters.hole_capture_coefficient * hole
    )
    result = (
        trap_parameters.trap_density
        * trap_parameters.electron_capture_coefficient
        * trap_parameters.hole_capture_coefficient
        / denominator
    )
    if result.ndim == 0:
        return float(result)
    return result


def trap_eliminated_pair_rate(
    electron_density: ArrayLike,
    hole_density: ArrayLike,
    *,
    trap_parameters: ReversibleTrapParameters,
) -> float | NDArray[np.float64]:
    """Return the steady-occupancy pair rate.

    The result is ``kappa_eff(N,P) * (N*P-K_eq)``. The previously merged
    constant-coefficient mass-action source is therefore a local reduction,
    not an exact global identity for this four-channel model.
    """

    electron = np.asarray(electron_density, dtype=float)
    hole = np.asarray(hole_density, dtype=float)
    coefficient = effective_mass_action_coefficient(
        electron,
        hole,
        trap_parameters=trap_parameters,
    )
    result = coefficient * (
        electron * hole - trap_parameters.equilibrium_product
    )
    if np.asarray(result).ndim == 0:
        return float(result)
    return np.asarray(result, dtype=float)


def assemble_trap_bipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
) -> NDArray[np.float64]:
    """Assemble Poisson, carrier-continuity, and trap-kinetic residuals.

    Define ``A`` as net electron capture and ``B`` as net hole capture. The
    steady residuals are ``R_n=div(j_n)-A``, ``R_p=div(j_p)+B``, and
    ``R_f=A-B``. Their source terms cancel identically. Occupied traps add
    electron-like charge to Poisson through ``N + N_t*f - P - C``.
    """

    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    reconstructed = reconstruct_trap_state(
        vector,
        mesh=mesh,
        boundaries=boundaries,
    )
    base = assemble_bipolar_residual(
        vector[: 3 * count],
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    ).copy()
    rates = reversible_trap_channel_rates(
        reconstructed.electron_density[1:-1],
        reconstructed.hole_density[1:-1],
        reconstructed.trap_occupancy,
        trap_parameters=trap_parameters,
    )
    base[:count] -= (
        parameters.screening_strength
        * trap_parameters.trap_density
        * reconstructed.trap_occupancy
    )
    base[count : 2 * count] -= rates.net_electron_capture
    base[2 * count : 3 * count] += rates.net_hole_capture
    return np.concatenate([base, rates.trap_kinetic_rate])


def assemble_trap_bipolar_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
) -> NDArray[np.float64]:
    """Return the complete analytical four-block Jacobian."""

    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    reconstructed = reconstruct_trap_state(
        vector,
        mesh=mesh,
        boundaries=boundaries,
    )
    base = assemble_bipolar_jacobian(
        vector[: 3 * count],
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    jacobian = np.zeros((4 * count, 4 * count), dtype=float)
    jacobian[: 3 * count, : 3 * count] = base

    electron = reconstructed.electron_density[1:-1]
    hole = reconstructed.hole_density[1:-1]
    occupancy = reconstructed.trap_occupancy
    derivative_occupancy = occupancy * (1.0 - occupancy)
    density = trap_parameters.trap_density

    d_a_d_logn = (
        density
        * trap_parameters.electron_capture_coefficient
        * electron
        * (1.0 - occupancy)
    )
    d_a_d_logit = -density * (
        trap_parameters.electron_capture_coefficient * electron
        + trap_parameters.electron_emission_coefficient
    ) * derivative_occupancy
    d_b_d_logp = (
        density
        * trap_parameters.hole_capture_coefficient
        * hole
        * occupancy
    )
    d_b_d_logit = density * (
        trap_parameters.hole_capture_coefficient * hole
        + trap_parameters.hole_emission_coefficient
    ) * derivative_occupancy

    index = np.arange(count)
    poisson_row = index
    electron_row = count + index
    hole_row = 2 * count + index
    trap_row = 3 * count + index
    electron_column = count + index
    hole_column = 2 * count + index
    trap_column = 3 * count + index

    jacobian[poisson_row, trap_column] -= (
        parameters.screening_strength
        * trap_parameters.trap_density
        * derivative_occupancy
    )
    jacobian[electron_row, electron_column] -= d_a_d_logn
    jacobian[electron_row, trap_column] -= d_a_d_logit
    jacobian[hole_row, hole_column] += d_b_d_logp
    jacobian[hole_row, trap_column] += d_b_d_logit
    jacobian[trap_row, electron_column] += d_a_d_logn
    jacobian[trap_row, hole_column] -= d_b_d_logp
    jacobian[trap_row, trap_column] += d_a_d_logit - d_b_d_logit
    return jacobian


def trap_balance_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
) -> TrapBalanceMetrics:
    """Evaluate carrier, trap, and total-current balances independently."""

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
    integrated_electron = mesh.spacing * float(
        np.sum(rates.net_electron_capture)
    )
    integrated_hole = mesh.spacing * float(np.sum(rates.net_hole_capture))
    integrated_trap = mesh.spacing * float(np.sum(rates.trap_kinetic_rate))
    electron_terminal = float(electron_current[-1] - electron_current[0])
    hole_terminal = float(hole_current[-1] - hole_current[0])
    electron_mismatch = electron_terminal - integrated_electron
    hole_mismatch = hole_terminal + integrated_hole
    trap_mismatch = integrated_trap
    electron_scale = max(1.0, abs(electron_terminal), abs(integrated_electron))
    hole_scale = max(1.0, abs(hole_terminal), abs(integrated_hole))
    trap_scale = max(1.0, abs(integrated_electron), abs(integrated_hole))

    total_current = electron_current + hole_current
    total_terminal = float(total_current[-1] - total_current[0])
    total_variation = float(np.max(total_current) - np.min(total_current))
    total_scale = max(1.0, float(np.max(np.abs(total_current))))
    return TrapBalanceMetrics(
        channel_rates=rates,
        integrated_net_electron_capture=integrated_electron,
        integrated_net_hole_capture=integrated_hole,
        integrated_trap_kinetic_rate=integrated_trap,
        electron_terminal_difference=electron_terminal,
        hole_terminal_difference=hole_terminal,
        electron_absolute_mismatch=abs(electron_mismatch),
        electron_relative_mismatch=abs(electron_mismatch) / electron_scale,
        hole_absolute_mismatch=abs(hole_mismatch),
        hole_relative_mismatch=abs(hole_mismatch) / hole_scale,
        trap_absolute_mismatch=abs(trap_mismatch),
        trap_relative_mismatch=abs(trap_mismatch) / trap_scale,
        total_current=total_current,
        total_current_terminal_difference=total_terminal,
        total_current_maximum_absolute_variation=abs(total_variation),
        total_current_relative_variation=abs(total_variation) / total_scale,
    )


def equilibrium_trap_state(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    trap_parameters: ReversibleTrapParameters,
) -> NDArray[np.float64]:
    """Return the constant-density equilibrium state for compatible boundaries."""

    if not np.isclose(
        boundaries.electron_density_left,
        trap_parameters.equilibrium_electron_density,
    ) or not np.isclose(
        boundaries.electron_density_right,
        trap_parameters.equilibrium_electron_density,
    ):
        raise ValueError("electron boundaries do not match trap equilibrium")
    if not np.isclose(
        boundaries.hole_density_left,
        trap_parameters.equilibrium_hole_density,
    ) or not np.isclose(
        boundaries.hole_density_right,
        trap_parameters.equilibrium_hole_density,
    ):
        raise ValueError("hole boundaries do not match trap equilibrium")
    fraction = mesh.nodes / mesh.length
    potential = boundaries.potential_left + fraction * (
        boundaries.potential_right - boundaries.potential_left
    )
    count = mesh.interior_count
    return pack_trap_state(
        potential[1:-1],
        np.full(count, np.log(trap_parameters.equilibrium_electron_density)),
        np.full(count, np.log(trap_parameters.equilibrium_hole_density)),
        np.full(count, logit_from_occupancy(trap_parameters.equilibrium_occupancy)),
    )


def _block_norms(
    residual: NDArray[np.float64],
    interior_count: int,
) -> tuple[float, float, float, float]:
    count = interior_count
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
) -> NDArray[np.float64] | None:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            residual = assemble_trap_bipolar_residual(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap_parameters,
            )
    except (ValueError, FloatingPointError, OverflowError):
        return None
    if not np.all(np.isfinite(residual)):
        return None
    return residual


def solve_trap_bipolar_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
    trap_parameters: ReversibleTrapParameters,
    options: NewtonOptions | None = None,
) -> TrapNewtonResult:
    """Solve the restricted reversible trap system with damped Newton."""

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
    )
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")
    initial_norm = float(np.linalg.norm(residual, ord=np.inf))
    target = max(
        controls.absolute_tolerance,
        controls.relative_tolerance * max(1.0, initial_norm),
    )
    history: list[TrapNewtonIteration] = []

    def finish(converged: bool, reason: str) -> TrapNewtonResult:
        final_residual = _safe_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap_parameters,
        )
        final_norm = (
            float("inf")
            if final_residual is None
            else float(np.linalg.norm(final_residual, ord=np.inf))
        )
        return TrapNewtonResult(
            state=state.copy(),
            converged=converged,
            termination_reason=reason,
            iterations=len(history),
            initial_residual_inf_norm=initial_norm,
            final_residual_inf_norm=final_norm,
            target_residual_inf_norm=target,
            history=tuple(history),
            balance=trap_balance_metrics(
                state,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap_parameters,
            ),
        )

    if initial_norm <= target:
        return finish(True, "initial_residual_converged")

    for iteration in range(controls.maximum_iterations):
        poisson_norm, electron_norm, hole_norm, trap_norm = _block_norms(
            residual,
            mesh.interior_count,
        )
        jacobian = assemble_trap_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap_parameters,
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
