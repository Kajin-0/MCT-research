"""Restricted dimensionless finite-exchange contact prototype for R06 Phase 1C.

This module verifies a classical unipolar density-Robin boundary against exact
blocking and ideal-reservoir limits. It is not a quantitative HgCdTe contact
model and contains no material barrier, Richardson constant, interface state,
contact-noise, or predictive detector closure.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .finite_volume_prototype import (
    UniformNodeMesh1D,
    bernoulli_derivative,
    bernoulli_function,
    electron_face_current,
)


@dataclass(frozen=True)
class FiniteExchangeContact:
    equilibrium_density: float
    biot_number: float

    def __post_init__(self) -> None:
        density, biot = float(self.equilibrium_density), float(self.biot_number)
        if not isfinite(density) or density <= 0.0:
            raise ValueError("equilibrium_density must be finite and positive")
        if not isfinite(biot) or biot < 0.0:
            raise ValueError("biot_number must be finite and non-negative")
        object.__setattr__(self, "equilibrium_density", density)
        object.__setattr__(self, "biot_number", biot)


@dataclass(frozen=True)
class FiniteContactBoundaryValues:
    potential_left: float
    potential_right: float
    left: FiniteExchangeContact
    right: FiniteExchangeContact

    def __post_init__(self) -> None:
        if not all(isfinite(float(v)) for v in (self.potential_left, self.potential_right)):
            raise ValueError("boundary potentials must be finite")


@dataclass(frozen=True)
class FiniteContactFVParameters:
    screening_strength: float
    diffusion_ratio: float = 1.0
    background_density: float = 1.0

    def __post_init__(self) -> None:
        screening = float(self.screening_strength)
        diffusion = float(self.diffusion_ratio)
        background = float(self.background_density)
        if not isfinite(screening) or screening < 0.0:
            raise ValueError("screening_strength must be finite and non-negative")
        if not isfinite(diffusion) or diffusion <= 0.0:
            raise ValueError("diffusion_ratio must be finite and positive")
        if not isfinite(background) or background <= 0.0:
            raise ValueError("background_density must be finite and positive")
        object.__setattr__(self, "screening_strength", screening)
        object.__setattr__(self, "diffusion_ratio", diffusion)
        object.__setattr__(self, "background_density", background)


@dataclass(frozen=True)
class ReconstructedFiniteContactState:
    potential: NDArray[np.float64]
    density: NDArray[np.float64]


@dataclass(frozen=True)
class ContactRegimeMetrics:
    left_biot: float
    right_biot: float
    ideal_reservoir_current_fraction: float
    bulk_resistance_fraction: float
    left_contact_resistance_fraction: float
    right_contact_resistance_fraction: float


@dataclass(frozen=True)
class ContactBalanceMetrics:
    face_current: NDArray[np.float64]
    maximum_absolute_variation: float
    relative_variation: float
    left_exchange_current: float
    right_exchange_current: float
    left_boundary_mismatch: float
    right_boundary_mismatch: float


@dataclass(frozen=True)
class ContactNewtonResult:
    state: NDArray[np.float64]
    converged: bool
    termination_reason: str
    iterations: int
    initial_residual_inf_norm: float
    final_residual_inf_norm: float
    balance: ContactBalanceMetrics


def _velocity(contact: FiniteExchangeContact, length: float, diffusion: float) -> float:
    return contact.biot_number * diffusion / length


def pack_finite_contact_state(
    potential_interior: ArrayLike, log_density_all_nodes: ArrayLike
) -> NDArray[np.float64]:
    potential = np.asarray(potential_interior, dtype=float)
    log_density = np.asarray(log_density_all_nodes, dtype=float)
    if potential.ndim != 1 or log_density.ndim != 1:
        raise ValueError("state arrays must be one-dimensional")
    if log_density.size != potential.size + 2:
        raise ValueError("all-node density must have two more entries than potential")
    if not np.all(np.isfinite(potential)) or not np.all(np.isfinite(log_density)):
        raise ValueError("state arrays must be finite")
    return np.concatenate([potential, log_density])


def reconstruct_finite_contact_state(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
) -> ReconstructedFiniteContactState:
    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    if vector.ndim != 1 or vector.size != count + mesh.node_count:
        raise ValueError("state has incompatible shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("state must be finite")
    potential = np.empty(mesh.node_count)
    potential[0], potential[-1] = boundaries.potential_left, boundaries.potential_right
    potential[1:-1] = vector[:count]
    density = np.exp(vector[count:])
    if not np.all(np.isfinite(density)):
        raise ValueError("state reconstructs a non-finite density")
    return ReconstructedFiniteContactState(potential, density)


def assemble_finite_contact_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
) -> NDArray[np.float64]:
    recovered = reconstruct_finite_contact_state(state, mesh=mesh, boundaries=boundaries)
    psi, density, h = recovered.potential, recovered.density, mesh.spacing
    poisson = (psi[2:] - 2.0 * psi[1:-1] + psi[:-2]) / h**2
    poisson -= parameters.screening_strength * (density[1:-1] - parameters.background_density)
    current = electron_face_current(
        psi, density, spacing=h, diffusion_ratio=parameters.diffusion_ratio
    )
    continuity = (current[1:] - current[:-1]) / h
    left_velocity = _velocity(boundaries.left, mesh.length, parameters.diffusion_ratio)
    right_velocity = _velocity(boundaries.right, mesh.length, parameters.diffusion_ratio)
    left = current[0] - left_velocity * (density[0] - boundaries.left.equilibrium_density)
    right = current[-1] + right_velocity * (density[-1] - boundaries.right.equilibrium_density)
    return np.concatenate([poisson, continuity, [left, right]])


def assemble_finite_contact_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
) -> NDArray[np.float64]:
    recovered = reconstruct_finite_contact_state(state, mesh=mesh, boundaries=boundaries)
    psi, density = recovered.potential, recovered.density
    count, nodes, h, diffusion = (
        mesh.interior_count,
        mesh.node_count,
        mesh.spacing,
        parameters.diffusion_ratio,
    )
    jacobian = np.zeros((2 * count + 2, 2 * count + 2))
    for local in range(count):
        node = local + 1
        jacobian[local, local] = -2.0 / h**2
        if node > 1:
            jacobian[local, local - 1] = 1.0 / h**2
        if node < mesh.intervals - 1:
            jacobian[local, local + 1] = 1.0 / h**2
        jacobian[local, count + node] = -parameters.screening_strength * density[node]

    delta = np.diff(psi)
    bp, bm = np.asarray(bernoulli_function(delta)), np.asarray(bernoulli_function(-delta))
    dbp = np.asarray(bernoulli_derivative(delta))
    dbm = np.asarray(bernoulli_derivative(-delta))
    dj_psi_left = -diffusion / h * (dbp * density[1:] + dbm * density[:-1])
    dj_psi_right = -dj_psi_left
    dj_log_left = -diffusion / h * bm * density[:-1]
    dj_log_right = diffusion / h * bp * density[1:]

    for local in range(count):
        row = count + local
        for face, sign in ((local + 1, 1.0), (local, -1.0)):
            left_node, right_node = face, face + 1
            if 1 <= left_node <= mesh.intervals - 1:
                jacobian[row, left_node - 1] += sign * dj_psi_left[face] / h
            if 1 <= right_node <= mesh.intervals - 1:
                jacobian[row, right_node - 1] += sign * dj_psi_right[face] / h
            jacobian[row, count + left_node] += sign * dj_log_left[face] / h
            jacobian[row, count + right_node] += sign * dj_log_right[face] / h

    left_velocity = _velocity(boundaries.left, mesh.length, diffusion)
    right_velocity = _velocity(boundaries.right, mesh.length, diffusion)
    left_row, right_row = 2 * count, 2 * count + 1
    jacobian[left_row, 0] = dj_psi_right[0]
    jacobian[left_row, count] = dj_log_left[0] - left_velocity * density[0]
    jacobian[left_row, count + 1] = dj_log_right[0]
    jacobian[right_row, count - 1] = dj_psi_left[-1]
    jacobian[right_row, count + nodes - 2] = dj_log_left[-1]
    jacobian[right_row, count + nodes - 1] = dj_log_right[-1] + right_velocity * density[-1]
    return jacobian


def exact_zero_field_current(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
) -> float:
    if boundaries.potential_left != boundaries.potential_right:
        raise ValueError("exact zero-field benchmark requires equal potentials")
    left, right = boundaries.left.biot_number, boundaries.right.biot_number
    if left == 0.0 or right == 0.0:
        return 0.0
    ideal = parameters.diffusion_ratio / mesh.length
    ideal *= boundaries.right.equilibrium_density - boundaries.left.equilibrium_density
    return ideal / (1.0 + 1.0 / left + 1.0 / right)


def exact_zero_field_state(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
) -> NDArray[np.float64]:
    if parameters.screening_strength != 0.0:
        raise ValueError("exact zero-field state requires zero screening_strength")
    current = exact_zero_field_current(mesh=mesh, boundaries=boundaries, parameters=parameters)
    left, right = boundaries.left.biot_number, boundaries.right.biot_number
    if left == 0.0 and right == 0.0:
        density = np.full(mesh.node_count, parameters.background_density)
    elif left == 0.0 or right == 0.0:
        pinned = boundaries.left.equilibrium_density if left > 0.0 else boundaries.right.equilibrium_density
        density = np.full(mesh.node_count, pinned)
    else:
        velocity = _velocity(boundaries.left, mesh.length, parameters.diffusion_ratio)
        density_left = boundaries.left.equilibrium_density + current / velocity
        density = density_left + current / parameters.diffusion_ratio * mesh.nodes
    potential = np.linspace(boundaries.potential_left, boundaries.potential_right, mesh.node_count)
    return pack_finite_contact_state(potential[1:-1], np.log(density))


def contact_regime_metrics(left_biot: float, right_biot: float) -> ContactRegimeMetrics:
    left, right = float(left_biot), float(right_biot)
    if not isfinite(left) or not isfinite(right) or left < 0.0 or right < 0.0:
        raise ValueError("Biot numbers must be finite and non-negative")
    rl, rr = (np.inf if left == 0.0 else 1.0 / left), (np.inf if right == 0.0 else 1.0 / right)
    if np.isinf(rl) and np.isinf(rr):
        bulk, fl, fr = 0.0, 0.5, 0.5
    elif np.isinf(rl):
        bulk, fl, fr = 0.0, 1.0, 0.0
    elif np.isinf(rr):
        bulk, fl, fr = 0.0, 0.0, 1.0
    else:
        total = 1.0 + rl + rr
        bulk, fl, fr = 1.0 / total, rl / total, rr / total
    return ContactRegimeMetrics(left, right, bulk, bulk, fl, fr)


def loaded_current_fraction(series_load_number: float) -> float:
    load = float(series_load_number)
    if not isfinite(load) or load < 0.0:
        raise ValueError("series_load_number must be finite and non-negative")
    return 1.0 / (1.0 + load)


def contact_balance_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
) -> ContactBalanceMetrics:
    recovered = reconstruct_finite_contact_state(state, mesh=mesh, boundaries=boundaries)
    current = electron_face_current(
        recovered.potential,
        recovered.density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.diffusion_ratio,
    )
    variation = float(np.max(current) - np.min(current))
    scale = max(1.0, float(np.max(np.abs(current))))
    vl = _velocity(boundaries.left, mesh.length, parameters.diffusion_ratio)
    vr = _velocity(boundaries.right, mesh.length, parameters.diffusion_ratio)
    left = vl * (recovered.density[0] - boundaries.left.equilibrium_density)
    right = -vr * (recovered.density[-1] - boundaries.right.equilibrium_density)
    return ContactBalanceMetrics(
        current,
        variation,
        variation / scale,
        float(left),
        float(right),
        float(current[0] - left),
        float(current[-1] - right),
    )


def solve_finite_contact_damped_newton(
    initial_state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: FiniteContactBoundaryValues,
    parameters: FiniteContactFVParameters,
    maximum_iterations: int = 40,
    absolute_tolerance: float = 1.0e-11,
    maximum_backtracks: int = 24,
) -> ContactNewtonResult:
    state = np.asarray(initial_state, dtype=float)
    if state.ndim != 1 or state.size != 2 * mesh.interior_count + 2 or not np.all(np.isfinite(state)):
        raise ValueError("initial_state has incompatible shape or non-finite values")
    state = state.copy()

    def safe_residual(vector: NDArray[np.float64]) -> NDArray[np.float64] | None:
        try:
            with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
                value = assemble_finite_contact_residual(
                    vector, mesh=mesh, boundaries=boundaries, parameters=parameters
                )
        except (ValueError, FloatingPointError, OverflowError):
            return None
        return value if np.all(np.isfinite(value)) else None

    residual = safe_residual(state)
    if residual is None:
        raise ValueError("initial_state produces a non-finite residual")
    initial_norm = float(np.linalg.norm(residual, ord=np.inf))

    def finish(converged: bool, reason: str, iterations: int) -> ContactNewtonResult:
        final = safe_residual(state)
        final_norm = float("inf") if final is None else float(np.linalg.norm(final, ord=np.inf))
        return ContactNewtonResult(
            state.copy(),
            converged,
            reason,
            iterations,
            initial_norm,
            final_norm,
            contact_balance_metrics(state, mesh=mesh, boundaries=boundaries, parameters=parameters),
        )

    if initial_norm <= absolute_tolerance:
        return finish(True, "initial_residual_converged", 0)
    for iteration in range(maximum_iterations):
        jacobian = assemble_finite_contact_jacobian(
            state, mesh=mesh, boundaries=boundaries, parameters=parameters
        )
        try:
            step = np.linalg.solve(jacobian, -residual)
        except np.linalg.LinAlgError:
            return finish(False, "singular_jacobian", iteration)
        damping, old_norm = 1.0, float(np.linalg.norm(residual))
        accepted = None
        for _ in range(maximum_backtracks + 1):
            trial = state + damping * step
            trial_residual = safe_residual(trial)
            if trial_residual is not None and np.linalg.norm(trial_residual) <= (1.0 - 1.0e-4 * damping) * old_norm:
                accepted = trial, trial_residual
                break
            damping *= 0.5
        if accepted is None:
            return finish(False, "line_search_failed", iteration)
        state, residual = accepted
        if np.linalg.norm(residual, ord=np.inf) <= absolute_tolerance:
            return finish(True, "residual_converged", iteration + 1)
    return finish(False, "maximum_iterations", maximum_iterations)
