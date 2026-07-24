"""Restricted dimensionless bipolar finite-exchange contact prototype for R06.

This Phase 1C module extends the verified classical density-Robin contact gate to
independent electron and hole exchange. It is a numerical architecture and
limiting-regime benchmark, not a material-specific HgCdTe contact model.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .bipolar_prototype import hole_face_current
from .contact_control_prototype import FiniteExchangeContact
from .finite_volume_prototype import (
    UniformNodeMesh1D,
    bernoulli_derivative,
    bernoulli_function,
    electron_face_current,
)


@dataclass(frozen=True)
class BipolarFiniteContactBoundaryValues:
    potential_left: float
    potential_right: float
    electron_left: FiniteExchangeContact
    electron_right: FiniteExchangeContact
    hole_left: FiniteExchangeContact
    hole_right: FiniteExchangeContact

    def __post_init__(self) -> None:
        if not all(isfinite(float(v)) for v in (self.potential_left, self.potential_right)):
            raise ValueError("boundary potentials must be finite")


@dataclass(frozen=True)
class BipolarFiniteContactFVParameters:
    screening_strength: float
    electron_diffusion_ratio: float = 1.0
    hole_diffusion_ratio: float = 1.0
    fixed_charge_density: float = 0.0

    def __post_init__(self) -> None:
        screening = float(self.screening_strength)
        electron = float(self.electron_diffusion_ratio)
        hole = float(self.hole_diffusion_ratio)
        fixed = float(self.fixed_charge_density)
        if not isfinite(screening) or screening < 0.0:
            raise ValueError("screening_strength must be finite and non-negative")
        if not isfinite(electron) or electron <= 0.0:
            raise ValueError("electron_diffusion_ratio must be finite and positive")
        if not isfinite(hole) or hole <= 0.0:
            raise ValueError("hole_diffusion_ratio must be finite and positive")
        if not isfinite(fixed):
            raise ValueError("fixed_charge_density must be finite")
        object.__setattr__(self, "screening_strength", screening)
        object.__setattr__(self, "electron_diffusion_ratio", electron)
        object.__setattr__(self, "hole_diffusion_ratio", hole)
        object.__setattr__(self, "fixed_charge_density", fixed)


@dataclass(frozen=True)
class ReconstructedBipolarFiniteContactState:
    potential: NDArray[np.float64]
    electron_density: NDArray[np.float64]
    hole_density: NDArray[np.float64]


@dataclass(frozen=True)
class CarrierContactBalance:
    face_current: NDArray[np.float64]
    maximum_absolute_variation: float
    relative_variation: float
    left_exchange_current: float
    right_exchange_current: float
    left_boundary_mismatch: float
    right_boundary_mismatch: float


@dataclass(frozen=True)
class BipolarContactBalanceMetrics:
    electron: CarrierContactBalance
    hole: CarrierContactBalance
    total_face_current: NDArray[np.float64]
    total_current_relative_variation: float


@dataclass(frozen=True)
class BipolarContactNewtonResult:
    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    balance: BipolarContactBalanceMetrics


def _velocity(contact: FiniteExchangeContact, length: float, diffusion: float) -> float:
    return contact.biot_number * diffusion / length


def pack_bipolar_finite_contact_state(
    potential_interior: ArrayLike,
    log_electron_density_all_nodes: ArrayLike,
    log_hole_density_all_nodes: ArrayLike,
) -> NDArray[np.float64]:
    potential = np.asarray(potential_interior, dtype=float)
    electron = np.asarray(log_electron_density_all_nodes, dtype=float)
    hole = np.asarray(log_hole_density_all_nodes, dtype=float)
    if potential.ndim != 1 or electron.ndim != 1 or hole.ndim != 1:
        raise ValueError("state arrays must be one-dimensional")
    if electron.size != potential.size + 2 or hole.shape != electron.shape:
        raise ValueError("all-node carrier arrays have incompatible shape")
    if not (
        np.all(np.isfinite(potential))
        and np.all(np.isfinite(electron))
        and np.all(np.isfinite(hole))
    ):
        raise ValueError("state arrays must be finite")
    return np.concatenate([potential, electron, hole])


def reconstruct_bipolar_finite_contact_state(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
) -> ReconstructedBipolarFiniteContactState:
    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    nodes = mesh.node_count
    if vector.ndim != 1 or vector.size != count + 2 * nodes:
        raise ValueError("state has incompatible shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("state must be finite")
    potential = np.empty(nodes, dtype=float)
    potential[0] = boundaries.potential_left
    potential[-1] = boundaries.potential_right
    potential[1:-1] = vector[:count]
    electron = np.exp(vector[count : count + nodes])
    hole = np.exp(vector[count + nodes :])
    if not np.all(np.isfinite(electron)) or not np.all(np.isfinite(hole)):
        raise ValueError("state reconstructs non-finite carrier density")
    return ReconstructedBipolarFiniteContactState(potential, electron, hole)


def assemble_bipolar_finite_contact_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
) -> NDArray[np.float64]:
    recovered = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    psi = recovered.potential
    electron = recovered.electron_density
    hole = recovered.hole_density
    h = mesh.spacing
    poisson = (psi[2:] - 2.0 * psi[1:-1] + psi[:-2]) / h**2
    poisson -= parameters.screening_strength * (
        electron[1:-1] - hole[1:-1] - parameters.fixed_charge_density
    )
    electron_current = electron_face_current(
        psi,
        electron,
        spacing=h,
        diffusion_ratio=parameters.electron_diffusion_ratio,
    )
    hole_current = hole_face_current(
        psi,
        hole,
        spacing=h,
        diffusion_ratio=parameters.hole_diffusion_ratio,
    )
    electron_continuity = np.diff(electron_current) / h
    hole_continuity = np.diff(hole_current) / h

    ven_left = _velocity(
        boundaries.electron_left, mesh.length, parameters.electron_diffusion_ratio
    )
    ven_right = _velocity(
        boundaries.electron_right, mesh.length, parameters.electron_diffusion_ratio
    )
    vhp_left = _velocity(
        boundaries.hole_left, mesh.length, parameters.hole_diffusion_ratio
    )
    vhp_right = _velocity(
        boundaries.hole_right, mesh.length, parameters.hole_diffusion_ratio
    )
    electron_left = electron_current[0] - ven_left * (
        electron[0] - boundaries.electron_left.equilibrium_density
    )
    electron_right = electron_current[-1] + ven_right * (
        electron[-1] - boundaries.electron_right.equilibrium_density
    )
    hole_left = hole_current[0] + vhp_left * (
        hole[0] - boundaries.hole_left.equilibrium_density
    )
    hole_right = hole_current[-1] - vhp_right * (
        hole[-1] - boundaries.hole_right.equilibrium_density
    )
    return np.concatenate(
        [
            poisson,
            electron_continuity,
            hole_continuity,
            [electron_left, electron_right, hole_left, hole_right],
        ]
    )


def assemble_bipolar_finite_contact_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
) -> NDArray[np.float64]:
    recovered = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    psi = recovered.potential
    electron = recovered.electron_density
    hole = recovered.hole_density
    count = mesh.interior_count
    nodes = mesh.node_count
    h = mesh.spacing
    electron_offset = count
    hole_offset = count + nodes
    size = count + 2 * nodes
    jacobian = np.zeros((size, size), dtype=float)

    for local in range(count):
        node = local + 1
        jacobian[local, local] = -2.0 / h**2
        if node > 1:
            jacobian[local, local - 1] = 1.0 / h**2
        if node < mesh.intervals - 1:
            jacobian[local, local + 1] = 1.0 / h**2
        jacobian[local, electron_offset + node] = (
            -parameters.screening_strength * electron[node]
        )
        jacobian[local, hole_offset + node] = (
            parameters.screening_strength * hole[node]
        )

    delta = np.diff(psi)
    b_plus = np.asarray(bernoulli_function(delta), dtype=float)
    b_minus = np.asarray(bernoulli_function(-delta), dtype=float)
    db_plus = np.asarray(bernoulli_derivative(delta), dtype=float)
    db_minus = np.asarray(bernoulli_derivative(-delta), dtype=float)
    dn = parameters.electron_diffusion_ratio
    dp = parameters.hole_diffusion_ratio

    djn_dpsi_left = -dn / h * (
        db_plus * electron[1:] + db_minus * electron[:-1]
    )
    djn_dpsi_right = -djn_dpsi_left
    djn_dlogn_left = -dn / h * b_minus * electron[:-1]
    djn_dlogn_right = dn / h * b_plus * electron[1:]

    djp_dpsi_left = -dp / h * (
        db_plus * hole[:-1] + db_minus * hole[1:]
    )
    djp_dpsi_right = -djp_dpsi_left
    djp_dlogp_left = dp / h * b_plus * hole[:-1]
    djp_dlogp_right = -dp / h * b_minus * hole[1:]

    for local in range(count):
        electron_row = count + local
        hole_row = 2 * count + local
        for face, sign in ((local + 1, 1.0), (local, -1.0)):
            left_node = face
            right_node = face + 1
            if 1 <= left_node <= mesh.intervals - 1:
                column = left_node - 1
                jacobian[electron_row, column] += sign * djn_dpsi_left[face] / h
                jacobian[hole_row, column] += sign * djp_dpsi_left[face] / h
            if 1 <= right_node <= mesh.intervals - 1:
                column = right_node - 1
                jacobian[electron_row, column] += sign * djn_dpsi_right[face] / h
                jacobian[hole_row, column] += sign * djp_dpsi_right[face] / h
            jacobian[electron_row, electron_offset + left_node] += (
                sign * djn_dlogn_left[face] / h
            )
            jacobian[electron_row, electron_offset + right_node] += (
                sign * djn_dlogn_right[face] / h
            )
            jacobian[hole_row, hole_offset + left_node] += (
                sign * djp_dlogp_left[face] / h
            )
            jacobian[hole_row, hole_offset + right_node] += (
                sign * djp_dlogp_right[face] / h
            )

    ven_left = _velocity(boundaries.electron_left, mesh.length, dn)
    ven_right = _velocity(boundaries.electron_right, mesh.length, dn)
    vhp_left = _velocity(boundaries.hole_left, mesh.length, dp)
    vhp_right = _velocity(boundaries.hole_right, mesh.length, dp)
    electron_left_row = 3 * count
    electron_right_row = electron_left_row + 1
    hole_left_row = electron_left_row + 2
    hole_right_row = electron_left_row + 3

    jacobian[electron_left_row, 0] = djn_dpsi_right[0]
    jacobian[electron_left_row, electron_offset] = (
        djn_dlogn_left[0] - ven_left * electron[0]
    )
    jacobian[electron_left_row, electron_offset + 1] = djn_dlogn_right[0]
    jacobian[electron_right_row, count - 1] = djn_dpsi_left[-1]
    jacobian[electron_right_row, electron_offset + nodes - 2] = djn_dlogn_left[-1]
    jacobian[electron_right_row, electron_offset + nodes - 1] = (
        djn_dlogn_right[-1] + ven_right * electron[-1]
    )

    jacobian[hole_left_row, 0] = djp_dpsi_right[0]
    jacobian[hole_left_row, hole_offset] = (
        djp_dlogp_left[0] + vhp_left * hole[0]
    )
    jacobian[hole_left_row, hole_offset + 1] = djp_dlogp_right[0]
    jacobian[hole_right_row, count - 1] = djp_dpsi_left[-1]
    jacobian[hole_right_row, hole_offset + nodes - 2] = djp_dlogp_left[-1]
    jacobian[hole_right_row, hole_offset + nodes - 1] = (
        djp_dlogp_right[-1] - vhp_right * hole[-1]
    )
    return jacobian


def _exact_carrier_current(
    diffusion: float,
    length: float,
    left: FiniteExchangeContact,
    right: FiniteExchangeContact,
    *,
    hole: bool,
) -> float:
    if left.biot_number == 0.0 or right.biot_number == 0.0:
        return 0.0
    numerator = (
        left.equilibrium_density - right.equilibrium_density
        if hole
        else right.equilibrium_density - left.equilibrium_density
    )
    return diffusion / length * numerator / (
        1.0 + 1.0 / left.biot_number + 1.0 / right.biot_number
    )


def exact_zero_field_bipolar_contact_currents(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
) -> tuple[float, float]:
    if boundaries.potential_left != boundaries.potential_right:
        raise ValueError("zero-field benchmark requires equal boundary potentials")
    electron = _exact_carrier_current(
        parameters.electron_diffusion_ratio,
        mesh.length,
        boundaries.electron_left,
        boundaries.electron_right,
        hole=False,
    )
    hole = _exact_carrier_current(
        parameters.hole_diffusion_ratio,
        mesh.length,
        boundaries.hole_left,
        boundaries.hole_right,
        hole=True,
    )
    return electron, hole


def _exact_density_profile(
    *,
    mesh: UniformNodeMesh1D,
    diffusion: float,
    left: FiniteExchangeContact,
    right: FiniteExchangeContact,
    current: float,
    hole: bool,
    fallback_density: float,
) -> NDArray[np.float64]:
    if left.biot_number == 0.0 and right.biot_number == 0.0:
        return np.full(mesh.node_count, fallback_density, dtype=float)
    if left.biot_number == 0.0 or right.biot_number == 0.0:
        pinned = (
            left.equilibrium_density
            if left.biot_number > 0.0
            else right.equilibrium_density
        )
        return np.full(mesh.node_count, pinned, dtype=float)
    left_velocity = _velocity(left, mesh.length, diffusion)
    boundary_density = (
        left.equilibrium_density - current / left_velocity
        if hole
        else left.equilibrium_density + current / left_velocity
    )
    slope = -current / diffusion if hole else current / diffusion
    return boundary_density + slope * mesh.nodes


def exact_zero_field_bipolar_contact_state(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
) -> NDArray[np.float64]:
    if parameters.screening_strength != 0.0:
        raise ValueError("exact state requires zero screening_strength")
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    electron = _exact_density_profile(
        mesh=mesh,
        diffusion=parameters.electron_diffusion_ratio,
        left=boundaries.electron_left,
        right=boundaries.electron_right,
        current=electron_current,
        hole=False,
        fallback_density=max(1.0, parameters.fixed_charge_density + 1.0),
    )
    hole = _exact_density_profile(
        mesh=mesh,
        diffusion=parameters.hole_diffusion_ratio,
        left=boundaries.hole_left,
        right=boundaries.hole_right,
        current=hole_current,
        hole=True,
        fallback_density=1.0,
    )
    potential = np.linspace(
        boundaries.potential_left, boundaries.potential_right, mesh.node_count
    )
    return pack_bipolar_finite_contact_state(
        potential[1:-1], np.log(electron), np.log(hole)
    )


def _carrier_balance(
    current: NDArray[np.float64], left_exchange: float, right_exchange: float
) -> CarrierContactBalance:
    variation = float(np.max(current) - np.min(current))
    scale = max(1.0, float(np.max(np.abs(current))))
    return CarrierContactBalance(
        current,
        variation,
        variation / scale,
        float(left_exchange),
        float(right_exchange),
        float(current[0] - left_exchange),
        float(current[-1] - right_exchange),
    )


def bipolar_contact_balance_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
) -> BipolarContactBalanceMetrics:
    recovered = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    electron_current = electron_face_current(
        recovered.potential,
        recovered.electron_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.electron_diffusion_ratio,
    )
    hole_current = hole_face_current(
        recovered.potential,
        recovered.hole_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.hole_diffusion_ratio,
    )
    ven_left = _velocity(
        boundaries.electron_left, mesh.length, parameters.electron_diffusion_ratio
    )
    ven_right = _velocity(
        boundaries.electron_right, mesh.length, parameters.electron_diffusion_ratio
    )
    vhp_left = _velocity(
        boundaries.hole_left, mesh.length, parameters.hole_diffusion_ratio
    )
    vhp_right = _velocity(
        boundaries.hole_right, mesh.length, parameters.hole_diffusion_ratio
    )
    electron_left = ven_left * (
        recovered.electron_density[0]
        - boundaries.electron_left.equilibrium_density
    )
    electron_right = -ven_right * (
        recovered.electron_density[-1]
        - boundaries.electron_right.equilibrium_density
    )
    hole_left = -vhp_left * (
        recovered.hole_density[0] - boundaries.hole_left.equilibrium_density
    )
    hole_right = vhp_right * (
        recovered.hole_density[-1] - boundaries.hole_right.equilibrium_density
    )
    total = electron_current + hole_current
    total_variation = float(np.max(total) - np.min(total))
    total_scale = max(1.0, float(np.max(np.abs(total))))
    return BipolarContactBalanceMetrics(
        _carrier_balance(electron_current, electron_left, electron_right),
        _carrier_balance(hole_current, hole_left, hole_right),
        total,
        total_variation / total_scale,
    )


def solve_bipolar_finite_contact_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarFiniteContactBoundaryValues,
    parameters: BipolarFiniteContactFVParameters,
    maximum_iterations: int = 40,
    absolute_tolerance: float = 1.0e-11,
    maximum_backtracks: int = 24,
) -> BipolarContactNewtonResult:
    state = np.asarray(initial_state, dtype=float)
    expected = mesh.interior_count + 2 * mesh.node_count
    if state.ndim != 1 or state.size != expected or not np.all(np.isfinite(state)):
        raise ValueError("initial_state has incompatible shape or non-finite values")
    state = state.copy()

    def safe_residual(vector: NDArray[np.float64]) -> NDArray[np.float64] | None:
        try:
            with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
                value = assemble_bipolar_finite_contact_residual(
                    vector, mesh=mesh, boundaries=boundaries, parameters=parameters
                )
        except (ValueError, FloatingPointError, OverflowError):
            return None
        return value if np.all(np.isfinite(value)) else None

    residual = safe_residual(state)
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")
    initial_norm = float(np.linalg.norm(residual, ord=np.inf))

    def finish(converged: bool, reason: str, iterations: int) -> BipolarContactNewtonResult:
        final = safe_residual(state)
        final_norm = float("inf") if final is None else float(np.linalg.norm(final, ord=np.inf))
        return BipolarContactNewtonResult(
            state.copy(),
            converged,
            reason,
            iterations,
            initial_norm,
            final_norm,
            bipolar_contact_balance_metrics(
                state, mesh=mesh, boundaries=boundaries, parameters=parameters
            ),
        )

    if initial_norm <= absolute_tolerance:
        return finish(True, "initial_residual_converged", 0)
    for iteration in range(maximum_iterations):
        jacobian = assemble_bipolar_finite_contact_jacobian(
            state, mesh=mesh, boundaries=boundaries, parameters=parameters
        )
        try:
            step = np.linalg.solve(jacobian, -residual)
        except np.linalg.LinAlgError:
            return finish(False, "singular_jacobian", iteration)
        damping = 1.0
        old_norm = float(np.linalg.norm(residual))
        accepted = None
        for _ in range(maximum_backtracks + 1):
            trial = state + damping * step
            trial_residual = safe_residual(trial)
            if trial_residual is not None and np.linalg.norm(trial_residual) <= (
                1.0 - 1.0e-4 * damping
            ) * old_norm:
                accepted = trial, trial_residual
                break
            damping *= 0.5
        if accepted is None:
            return finish(False, "line_search_failed", iteration)
        state, residual = accepted
        if np.linalg.norm(residual, ord=np.inf) <= absolute_tolerance:
            return finish(True, "residual_converged", iteration + 1)
    return finish(False, "maximum_iterations", maximum_iterations)
