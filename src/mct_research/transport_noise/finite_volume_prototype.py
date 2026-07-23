"""Conservative one-dimensional finite-volume prototypes for R06.

This module is deliberately restricted to a dimensionless, steady, unipolar
drift-diffusion-Poisson benchmark with ideal reservoir boundary values. It is
not a production HgCdTe detector solver and contains no stochastic operators,
trap kinetics, optical generation, or material-specific parameter relations.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class UniformNodeMesh1D:
    """Uniform node-centered mesh on ``0 <= x <= length``."""

    length: float
    intervals: int

    def __post_init__(self) -> None:
        length = float(self.length)
        intervals = int(self.intervals)
        if not isfinite(length) or length <= 0.0:
            raise ValueError("length must be finite and positive")
        if intervals != self.intervals or intervals < 2:
            raise ValueError("intervals must be an integer >= 2")
        object.__setattr__(self, "length", length)
        object.__setattr__(self, "intervals", intervals)

    @property
    def spacing(self) -> float:
        return self.length / self.intervals

    @property
    def node_count(self) -> int:
        return self.intervals + 1

    @property
    def interior_count(self) -> int:
        return self.intervals - 1

    @property
    def nodes(self) -> NDArray[np.float64]:
        return np.linspace(0.0, self.length, self.node_count)


@dataclass(frozen=True)
class UnipolarBoundaryValues:
    """Fixed electrostatic potential and electron density at both reservoirs."""

    potential_left: float
    potential_right: float
    density_left: float
    density_right: float

    def __post_init__(self) -> None:
        values = (
            self.potential_left,
            self.potential_right,
            self.density_left,
            self.density_right,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("boundary values must be finite")
        if self.density_left <= 0.0 or self.density_right <= 0.0:
            raise ValueError("boundary densities must be positive")


@dataclass(frozen=True)
class UnipolarFVParameters:
    """Dimensionless coefficients for the restricted unipolar benchmark."""

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
class ReconstructedUnipolarState:
    """Full nodal potential and positive density reconstructed from unknowns."""

    potential: NDArray[np.float64]
    density: NDArray[np.float64]


@dataclass(frozen=True)
class CurrentConservationMetrics:
    """Independent diagnostics computed from reconstructed face currents."""

    face_current: NDArray[np.float64]
    maximum_absolute_variation: float
    relative_variation: float


def bernoulli_function(argument: ArrayLike) -> float | NDArray[np.float64]:
    r"""Evaluate ``B(x)=x/(exp(x)-1)`` with stable limiting branches."""

    x = np.asarray(argument, dtype=float)
    scalar = x.ndim == 0
    flat = np.atleast_1d(x).reshape(-1)
    if not np.all(np.isfinite(flat)):
        raise ValueError("argument must contain only finite values")

    result = np.empty_like(flat)
    small = np.abs(flat) < 1.0e-4
    positive_large = flat > 50.0
    negative_large = flat < -50.0
    regular = ~(small | positive_large | negative_large)

    xs = flat[small]
    result[small] = (
        1.0
        - 0.5 * xs
        + xs**2 / 12.0
        - xs**4 / 720.0
        + xs**6 / 30240.0
    )
    xp = flat[positive_large]
    result[positive_large] = xp * np.exp(-xp)
    result[negative_large] = -flat[negative_large]
    xr = flat[regular]
    result[regular] = xr / np.expm1(xr)

    reshaped = result.reshape(np.atleast_1d(x).shape)
    if scalar:
        return float(reshaped[0])
    return reshaped


def bernoulli_derivative(argument: ArrayLike) -> float | NDArray[np.float64]:
    """Return the derivative of :func:`bernoulli_function`."""

    x = np.asarray(argument, dtype=float)
    scalar = x.ndim == 0
    flat = np.atleast_1d(x).reshape(-1)
    if not np.all(np.isfinite(flat)):
        raise ValueError("argument must contain only finite values")

    result = np.empty_like(flat)
    small = np.abs(flat) < 1.0e-4
    positive_large = flat > 50.0
    negative_large = flat < -50.0
    regular = ~(small | positive_large | negative_large)

    xs = flat[small]
    result[small] = (
        -0.5
        + xs / 6.0
        - xs**3 / 180.0
        + xs**5 / 5040.0
    )
    xp = flat[positive_large]
    result[positive_large] = (1.0 - xp) * np.exp(-xp)
    result[negative_large] = -1.0
    xr = flat[regular]
    denominator = np.expm1(xr)
    result[regular] = (
        denominator - xr * np.exp(xr)
    ) / denominator**2

    reshaped = result.reshape(np.atleast_1d(x).shape)
    if scalar:
        return float(reshaped[0])
    return reshaped


def pack_unipolar_state(
    potential_interior: ArrayLike,
    log_density_interior: ArrayLike,
) -> NDArray[np.float64]:
    """Pack interior potential and log-density arrays into one state vector."""

    potential = np.asarray(potential_interior, dtype=float)
    log_density = np.asarray(log_density_interior, dtype=float)
    if potential.ndim != 1 or log_density.ndim != 1:
        raise ValueError("state arrays must be one-dimensional")
    if potential.shape != log_density.shape:
        raise ValueError("potential and log-density arrays must have equal shape")
    if not np.all(np.isfinite(potential)) or not np.all(np.isfinite(log_density)):
        raise ValueError("state arrays must contain only finite values")
    return np.concatenate([potential, log_density])


def reconstruct_unipolar_state(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
) -> ReconstructedUnipolarState:
    """Reconstruct full nodal arrays from interior unknowns."""

    vector = np.asarray(state, dtype=float)
    if vector.ndim != 1 or vector.size != 2 * mesh.interior_count:
        raise ValueError("state has incompatible shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("state must contain only finite values")

    count = mesh.interior_count
    potential = np.empty(mesh.node_count, dtype=float)
    density = np.empty(mesh.node_count, dtype=float)
    potential[0] = boundaries.potential_left
    potential[-1] = boundaries.potential_right
    density[0] = boundaries.density_left
    density[-1] = boundaries.density_right
    potential[1:-1] = vector[:count]
    density[1:-1] = np.exp(vector[count:])
    return ReconstructedUnipolarState(potential=potential, density=density)


def electron_face_current(
    potential: ArrayLike,
    density: ArrayLike,
    *,
    spacing: float,
    diffusion_ratio: float = 1.0,
) -> NDArray[np.float64]:
    r"""Return fitted electron current at every face.

    The dimensionless current is

    .. math::

        j_n = d_n(\partial_x N - N\partial_x\psi).

    For piecewise-linear potential and constant face current, the
    Scharfetter-Gummel expression is exact:

    .. math::

        j_{i+1/2}
        = \frac{d_n}{h}
          [B(\Delta\psi_i)N_{i+1}
           -B(-\Delta\psi_i)N_i].
    """

    psi = np.asarray(potential, dtype=float)
    carrier = np.asarray(density, dtype=float)
    h = float(spacing)
    diffusion = float(diffusion_ratio)
    if psi.ndim != 1 or carrier.ndim != 1 or psi.shape != carrier.shape:
        raise ValueError("potential and density must be equal-length 1D arrays")
    if psi.size < 2:
        raise ValueError("at least two nodes are required")
    if not np.all(np.isfinite(psi)) or not np.all(np.isfinite(carrier)):
        raise ValueError("potential and density must be finite")
    if np.any(carrier <= 0.0):
        raise ValueError("density must be positive")
    if not isfinite(h) or h <= 0.0:
        raise ValueError("spacing must be finite and positive")
    if not isfinite(diffusion) or diffusion <= 0.0:
        raise ValueError("diffusion_ratio must be finite and positive")

    delta = np.diff(psi)
    return diffusion / h * (
        bernoulli_function(delta) * carrier[1:]
        - bernoulli_function(-delta) * carrier[:-1]
    )


def assemble_unipolar_residual(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
) -> NDArray[np.float64]:
    """Assemble conservative Poisson and steady electron-continuity residuals."""

    reconstructed = reconstruct_unipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    psi = reconstructed.potential
    density = reconstructed.density
    h = mesh.spacing

    poisson = (
        psi[2:] - 2.0 * psi[1:-1] + psi[:-2]
    ) / h**2 - parameters.screening_strength * (
        density[1:-1] - parameters.background_density
    )

    face_current = electron_face_current(
        psi,
        density,
        spacing=h,
        diffusion_ratio=parameters.diffusion_ratio,
    )
    continuity = (face_current[1:] - face_current[:-1]) / h
    return np.concatenate([poisson, continuity])


def assemble_unipolar_jacobian(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
) -> NDArray[np.float64]:
    """Assemble the dense analytical Jacobian of the prototype residual."""

    reconstructed = reconstruct_unipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    psi = reconstructed.potential
    density = reconstructed.density
    count = mesh.interior_count
    h = mesh.spacing
    diffusion = parameters.diffusion_ratio

    jacobian = np.zeros((2 * count, 2 * count), dtype=float)

    for local in range(count):
        node = local + 1
        jacobian[local, local] = -2.0 / h**2
        if node - 1 >= 1:
            jacobian[local, local - 1] = 1.0 / h**2
        if node + 1 <= mesh.intervals - 1:
            jacobian[local, local + 1] = 1.0 / h**2
        jacobian[local, count + local] = (
            -parameters.screening_strength * density[node]
        )

    delta = np.diff(psi)
    b_plus = np.asarray(bernoulli_function(delta), dtype=float)
    b_minus = np.asarray(bernoulli_function(-delta), dtype=float)
    db_plus = np.asarray(bernoulli_derivative(delta), dtype=float)
    db_minus = np.asarray(bernoulli_derivative(-delta), dtype=float)

    dcurrent_dpsi_left = -diffusion / h * (
        db_plus * density[1:] + db_minus * density[:-1]
    )
    dcurrent_dpsi_right = -dcurrent_dpsi_left
    dcurrent_dlogn_left = -diffusion / h * b_minus * density[:-1]
    dcurrent_dlogn_right = diffusion / h * b_plus * density[1:]

    for local in range(count):
        row = count + local
        left_face = local
        right_face = local + 1
        scale = 1.0 / h

        left_node = right_face
        right_node = right_face + 1
        if 1 <= left_node <= mesh.intervals - 1:
            col = left_node - 1
            jacobian[row, col] += scale * dcurrent_dpsi_left[right_face]
            jacobian[row, count + col] += (
                scale * dcurrent_dlogn_left[right_face]
            )
        if 1 <= right_node <= mesh.intervals - 1:
            col = right_node - 1
            jacobian[row, col] += scale * dcurrent_dpsi_right[right_face]
            jacobian[row, count + col] += (
                scale * dcurrent_dlogn_right[right_face]
            )

        left_node = left_face
        right_node = left_face + 1
        if 1 <= left_node <= mesh.intervals - 1:
            col = left_node - 1
            jacobian[row, col] -= scale * dcurrent_dpsi_left[left_face]
            jacobian[row, count + col] -= (
                scale * dcurrent_dlogn_left[left_face]
            )
        if 1 <= right_node <= mesh.intervals - 1:
            col = right_node - 1
            jacobian[row, col] -= scale * dcurrent_dpsi_right[left_face]
            jacobian[row, count + col] -= (
                scale * dcurrent_dlogn_right[left_face]
            )

    return jacobian


def current_conservation_metrics(
    state: ArrayLike,
    *,
    mesh: UniformNodeMesh1D,
    boundaries: UnipolarBoundaryValues,
    parameters: UnipolarFVParameters,
) -> CurrentConservationMetrics:
    """Compute face-current variation independently of the residual vector."""

    reconstructed = reconstruct_unipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    current = electron_face_current(
        reconstructed.potential,
        reconstructed.density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.diffusion_ratio,
    )
    variation = float(np.max(current) - np.min(current))
    scale = max(1.0, float(np.max(np.abs(current))))
    return CurrentConservationMetrics(
        face_current=current,
        maximum_absolute_variation=abs(variation),
        relative_variation=abs(variation) / scale,
    )
