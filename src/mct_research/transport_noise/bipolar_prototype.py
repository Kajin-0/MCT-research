"""Conservative dimensionless bipolar finite-volume prototype for R06.

This Phase 1C module extends the verified one-carrier numerical architecture to
one electron and one hole population with fixed reservoir values. It contains
no traps, recombination, optical generation, dynamic contacts, external circuit
state, stochastic operators, or material-specific HgCdTe parameter relations.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .finite_volume_prototype import (
    CurrentConservationMetrics,
    UniformNodeMesh1D,
    bernoulli_derivative,
    bernoulli_function,
    electron_face_current,
)


@dataclass(frozen=True)
class BipolarBoundaryValues:
    """Fixed potential, electron density, and hole density at both reservoirs."""

    potential_left: float
    potential_right: float
    electron_density_left: float
    electron_density_right: float
    hole_density_left: float
    hole_density_right: float

    def __post_init__(self) -> None:
        values = (
            self.potential_left,
            self.potential_right,
            self.electron_density_left,
            self.electron_density_right,
            self.hole_density_left,
            self.hole_density_right,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("boundary values must be finite")
        if any(float(value) <= 0.0 for value in values[2:]):
            raise ValueError("boundary carrier densities must be positive")


@dataclass(frozen=True)
class BipolarFVParameters:
    """Dimensionless coefficients for the restricted bipolar benchmark."""

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
            raise ValueError(
                "electron_diffusion_ratio must be finite and positive"
            )
        if not isfinite(hole) or hole <= 0.0:
            raise ValueError("hole_diffusion_ratio must be finite and positive")
        if not isfinite(fixed):
            raise ValueError("fixed_charge_density must be finite")
        object.__setattr__(self, "screening_strength", screening)
        object.__setattr__(self, "electron_diffusion_ratio", electron)
        object.__setattr__(self, "hole_diffusion_ratio", hole)
        object.__setattr__(self, "fixed_charge_density", fixed)


@dataclass(frozen=True)
class ReconstructedBipolarState:
    """Full nodal potential and positive electron/hole densities."""

    potential: NDArray[np.float64]
    electron_density: NDArray[np.float64]
    hole_density: NDArray[np.float64]


@dataclass(frozen=True)
class BipolarCurrentConservationMetrics:
    """Independent current-conservation diagnostics for both carriers."""

    electron: CurrentConservationMetrics
    hole: CurrentConservationMetrics


def pack_bipolar_state(
    potential_interior: ArrayLike,
    log_electron_density_interior: ArrayLike,
    log_hole_density_interior: ArrayLike,
) -> NDArray[np.float64]:
    """Pack interior potential and logarithmic carrier densities."""

    potential = np.asarray(potential_interior, dtype=float)
    log_electron = np.asarray(log_electron_density_interior, dtype=float)
    log_hole = np.asarray(log_hole_density_interior, dtype=float)
    if potential.ndim != 1 or log_electron.ndim != 1 or log_hole.ndim != 1:
        raise ValueError("state arrays must be one-dimensional")
    if potential.shape != log_electron.shape or potential.shape != log_hole.shape:
        raise ValueError("state arrays must have equal shape")
    if not (
        np.all(np.isfinite(potential))
        and np.all(np.isfinite(log_electron))
        and np.all(np.isfinite(log_hole))
    ):
        raise ValueError("state arrays must contain only finite values")
    return np.concatenate([potential, log_electron, log_hole])


def reconstruct_bipolar_state(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
) -> ReconstructedBipolarState:
    """Reconstruct full nodal arrays from interior unknowns."""

    vector = np.asarray(state, dtype=float)
    count = mesh.interior_count
    if vector.ndim != 1 or vector.size != 3 * count:
        raise ValueError("state has incompatible shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("state must contain only finite values")

    potential = np.empty(mesh.node_count, dtype=float)
    electron = np.empty(mesh.node_count, dtype=float)
    hole = np.empty(mesh.node_count, dtype=float)
    potential[0] = boundaries.potential_left
    potential[-1] = boundaries.potential_right
    electron[0] = boundaries.electron_density_left
    electron[-1] = boundaries.electron_density_right
    hole[0] = boundaries.hole_density_left
    hole[-1] = boundaries.hole_density_right
    potential[1:-1] = vector[:count]
    electron[1:-1] = np.exp(vector[count : 2 * count])
    hole[1:-1] = np.exp(vector[2 * count :])
    return ReconstructedBipolarState(
        potential=potential,
        electron_density=electron,
        hole_density=hole,
    )


def hole_face_current(
    potential: ArrayLike,
    hole_density: ArrayLike,
    *,
    spacing: float,
    diffusion_ratio: float = 1.0,
) -> NDArray[np.float64]:
    r"""Return fitted conventional hole current at every face.

    The dimensionless current is

    .. math::

        j_p=-d_p(\partial_xP+P\partial_x\psi).

    For piecewise-linear potential and constant face current,

    .. math::

        j_{p,i+1/2}=\frac{d_p}{h}
        [B(\Delta\psi_i)P_i-B(-\Delta\psi_i)P_{i+1}].
    """

    psi = np.asarray(potential, dtype=float)
    carrier = np.asarray(hole_density, dtype=float)
    h = float(spacing)
    diffusion = float(diffusion_ratio)
    if psi.ndim != 1 or carrier.ndim != 1 or psi.shape != carrier.shape:
        raise ValueError("potential and hole_density must be equal-length 1D arrays")
    if psi.size < 2:
        raise ValueError("at least two nodes are required")
    if not np.all(np.isfinite(psi)) or not np.all(np.isfinite(carrier)):
        raise ValueError("potential and hole_density must be finite")
    if np.any(carrier <= 0.0):
        raise ValueError("hole_density must be positive")
    if not isfinite(h) or h <= 0.0:
        raise ValueError("spacing must be finite and positive")
    if not isfinite(diffusion) or diffusion <= 0.0:
        raise ValueError("diffusion_ratio must be finite and positive")

    delta = np.diff(psi)
    return diffusion / h * (
        bernoulli_function(delta) * carrier[:-1]
        - bernoulli_function(-delta) * carrier[1:]
    )


def assemble_bipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
) -> NDArray[np.float64]:
    """Assemble Poisson, electron-continuity, and hole-continuity residuals."""

    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    psi = reconstructed.potential
    electron = reconstructed.electron_density
    hole = reconstructed.hole_density
    h = mesh.spacing

    poisson = (
        psi[2:] - 2.0 * psi[1:-1] + psi[:-2]
    ) / h**2 - parameters.screening_strength * (
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
    electron_continuity = (electron_current[1:] - electron_current[:-1]) / h
    hole_continuity = (hole_current[1:] - hole_current[:-1]) / h
    return np.concatenate([poisson, electron_continuity, hole_continuity])


def assemble_bipolar_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
) -> NDArray[np.float64]:
    """Assemble the dense analytical Jacobian of the bipolar residual."""

    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    psi = reconstructed.potential
    electron = reconstructed.electron_density
    hole = reconstructed.hole_density
    count = mesh.interior_count
    h = mesh.spacing
    electron_diffusion = parameters.electron_diffusion_ratio
    hole_diffusion = parameters.hole_diffusion_ratio

    jacobian = np.zeros((3 * count, 3 * count), dtype=float)

    for local in range(count):
        node = local + 1
        jacobian[local, local] = -2.0 / h**2
        if node - 1 >= 1:
            jacobian[local, local - 1] = 1.0 / h**2
        if node + 1 <= mesh.intervals - 1:
            jacobian[local, local + 1] = 1.0 / h**2
        jacobian[local, count + local] = (
            -parameters.screening_strength * electron[node]
        )
        jacobian[local, 2 * count + local] = (
            parameters.screening_strength * hole[node]
        )

    delta = np.diff(psi)
    b_plus = np.asarray(bernoulli_function(delta), dtype=float)
    b_minus = np.asarray(bernoulli_function(-delta), dtype=float)
    db_plus = np.asarray(bernoulli_derivative(delta), dtype=float)
    db_minus = np.asarray(bernoulli_derivative(-delta), dtype=float)

    djn_dpsi_left = -electron_diffusion / h * (
        db_plus * electron[1:] + db_minus * electron[:-1]
    )
    djn_dpsi_right = -djn_dpsi_left
    djn_dlogn_left = -electron_diffusion / h * b_minus * electron[:-1]
    djn_dlogn_right = electron_diffusion / h * b_plus * electron[1:]

    djp_dpsi_left = -hole_diffusion / h * (
        db_plus * hole[:-1] + db_minus * hole[1:]
    )
    djp_dpsi_right = -djp_dpsi_left
    djp_dlogp_left = hole_diffusion / h * b_plus * hole[:-1]
    djp_dlogp_right = -hole_diffusion / h * b_minus * hole[1:]

    for local in range(count):
        electron_row = count + local
        hole_row = 2 * count + local
        left_face = local
        right_face = local + 1
        scale = 1.0 / h

        for face, sign in ((right_face, 1.0), (left_face, -1.0)):
            left_node = face
            right_node = face + 1
            if 1 <= left_node <= mesh.intervals - 1:
                col = left_node - 1
                jacobian[electron_row, col] += (
                    sign * scale * djn_dpsi_left[face]
                )
                jacobian[electron_row, count + col] += (
                    sign * scale * djn_dlogn_left[face]
                )
                jacobian[hole_row, col] += sign * scale * djp_dpsi_left[face]
                jacobian[hole_row, 2 * count + col] += (
                    sign * scale * djp_dlogp_left[face]
                )
            if 1 <= right_node <= mesh.intervals - 1:
                col = right_node - 1
                jacobian[electron_row, col] += (
                    sign * scale * djn_dpsi_right[face]
                )
                jacobian[electron_row, count + col] += (
                    sign * scale * djn_dlogn_right[face]
                )
                jacobian[hole_row, col] += sign * scale * djp_dpsi_right[face]
                jacobian[hole_row, 2 * count + col] += (
                    sign * scale * djp_dlogp_right[face]
                )

    return jacobian


def _current_metrics(current: NDArray[np.float64]) -> CurrentConservationMetrics:
    variation = float(np.max(current) - np.min(current))
    scale = max(1.0, float(np.max(np.abs(current))))
    return CurrentConservationMetrics(
        face_current=current,
        maximum_absolute_variation=abs(variation),
        relative_variation=abs(variation) / scale,
    )


def bipolar_current_conservation_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
    parameters: BipolarFVParameters,
) -> BipolarCurrentConservationMetrics:
    """Compute independent electron and hole face-current diagnostics."""

    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    electron = electron_face_current(
        reconstructed.potential,
        reconstructed.electron_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.electron_diffusion_ratio,
    )
    hole = hole_face_current(
        reconstructed.potential,
        reconstructed.hole_density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.hole_diffusion_ratio,
    )
    return BipolarCurrentConservationMetrics(
        electron=_current_metrics(electron),
        hole=_current_metrics(hole),
    )


def linear_bipolar_reservoir_state(
    *,
    mesh: UniformNodeMesh1D,
    boundaries: BipolarBoundaryValues,
) -> NDArray[np.float64]:
    """Return linear potential and linear logarithmic carrier profiles."""

    fraction = mesh.nodes / mesh.length
    potential = boundaries.potential_left + fraction * (
        boundaries.potential_right - boundaries.potential_left
    )
    log_electron = np.log(boundaries.electron_density_left) + fraction * (
        np.log(boundaries.electron_density_right)
        - np.log(boundaries.electron_density_left)
    )
    log_hole = np.log(boundaries.hole_density_left) + fraction * (
        np.log(boundaries.hole_density_right) - np.log(boundaries.hole_density_left)
    )
    return pack_bipolar_state(
        potential[1:-1],
        log_electron[1:-1],
        log_hole[1:-1],
    )
