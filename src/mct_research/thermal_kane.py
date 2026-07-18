"""Finite-temperature matrix and thermal-reduction primitives for Kane models.

The functions in this module are deterministic method-validation tools. They do
not calculate an electron-phonon self-energy from first principles and do not
represent CdTe or HgCdTe material predictions by themselves.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Iterable, Mapping, Sequence

import numpy as np
from numpy.typing import NDArray

from .kane8 import ExtendedKaneParameters, KaneParameters, hamiltonian, hamiltonian_two_p

ComplexMatrix = NDArray[np.complex128]


@dataclass(frozen=True)
class ThermalParameterScale:
    """One fixed Bose scale and its signed parameter amplitudes.

    ``shifts`` contains the coefficient multiplying
    ``2 / (exp(theta_k / temperature_k) - 1)`` for each named Kane parameter.
    Consequently every shift is zero at ``temperature_k = 0``.
    """

    theta_k: float
    shifts: Mapping[str, float]

    def __post_init__(self) -> None:
        if not np.isfinite(self.theta_k) or self.theta_k <= 0.0:
            raise ValueError("thermal scale theta_k must be finite and positive")
        allowed = {item.name for item in fields(ExtendedKaneParameters)}
        unknown = set(self.shifts) - allowed
        if unknown:
            raise ValueError(f"unknown ExtendedKaneParameters fields: {sorted(unknown)}")
        if not all(np.isfinite(float(value)) for value in self.shifts.values()):
            raise ValueError("thermal parameter amplitudes must be finite")


@dataclass(frozen=True)
class RationalSelfEnergy:
    """Scalar retarded self-energy used by the dynamical-pole oracle.

    The real test model is

    ``Sigma(z) = offset + slope*(z-reference) + coupling^2/(z-remote)``.

    The remote pole must lie outside the bracket used for the target
    quasiparticle root.
    """

    reference_ev: float
    offset_ev: float
    slope: float
    coupling_ev: float
    remote_ev: float

    def value(self, energy_ev: float) -> float:
        denominator = float(energy_ev) - self.remote_ev
        if denominator == 0.0:
            raise ZeroDivisionError("self-energy evaluated on its remote pole")
        return (
            self.offset_ev
            + self.slope * (float(energy_ev) - self.reference_ev)
            + self.coupling_ev * self.coupling_ev / denominator
        )

    def derivative(self, energy_ev: float) -> float:
        denominator = float(energy_ev) - self.remote_ev
        if denominator == 0.0:
            raise ZeroDivisionError("self-energy derivative evaluated on remote pole")
        return self.slope - self.coupling_ev * self.coupling_ev / denominator**2


def bose_thermal_factor(theta_k: float, temperature_k: float) -> float:
    """Return the finite-temperature Bose factor relative to zero temperature.

    The returned factor is ``2*n_B = 2/(exp(theta/T)-1)``. The implementation is
    stable for both very small and very large ``theta/T``.
    """

    theta = float(theta_k)
    temperature = float(temperature_k)
    if not np.isfinite(theta) or theta <= 0.0:
        raise ValueError("theta_k must be finite and positive")
    if not np.isfinite(temperature) or temperature < 0.0:
        raise ValueError("temperature_k must be finite and nonnegative")
    if temperature == 0.0:
        return 0.0
    ratio = theta / temperature
    if ratio > 745.0:
        return 0.0
    return float(2.0 / np.expm1(ratio))


def thermal_extended_parameters(
    base: ExtendedKaneParameters,
    scales: Sequence[ThermalParameterScale],
    temperature_k: float,
) -> ExtendedKaneParameters:
    """Evaluate a signed fixed-scale thermal trajectory of Kane parameters."""

    names = tuple(item.name for item in fields(ExtendedKaneParameters))
    values = {name: float(getattr(base, name)) for name in names}
    for scale in scales:
        factor = bose_thermal_factor(scale.theta_k, temperature_k)
        for name, amplitude in scale.shifts.items():
            values[name] += factor * float(amplitude)
    return ExtendedKaneParameters(**values)


def gamma_irrep_matrix(
    sigma6_ev: float,
    sigma8_ev: float,
    sigma7_ev: float,
) -> ComplexMatrix:
    """Return the most general Td-symmetric Hermitian Gamma self-energy."""

    values = np.asarray(
        [sigma6_ev, sigma6_ev]
        + [sigma8_ev] * 4
        + [sigma7_ev, sigma7_ev],
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("Gamma self-energy values must be finite")
    return np.diag(values).astype(np.complex128)


def gamma_irrep_covariance_residual(matrix: ComplexMatrix) -> float:
    """Measure deviation from scalar Gamma6, Gamma8 and Gamma7 blocks."""

    candidate = np.asarray(matrix, dtype=np.complex128)
    if candidate.shape != (8, 8):
        raise ValueError("Gamma matrix must be 8x8")
    projected = np.zeros((8, 8), dtype=np.complex128)
    for block in (slice(0, 2), slice(2, 6), slice(6, 8)):
        value = np.trace(candidate[block, block]).real / (block.stop - block.start)
        projected[block, block] = value * np.eye(block.stop - block.start)
    scale = max(float(np.linalg.norm(candidate, ord="fro")), 1.0)
    return float(np.linalg.norm(candidate - projected, ord="fro") / scale)


def hermitian_inverse_sqrt(
    matrix: ComplexMatrix,
    *,
    eigenvalue_floor: float = 1.0e-12,
) -> tuple[ComplexMatrix, NDArray[np.float64]]:
    """Return the Hermitian inverse square root and eigenvalues."""

    candidate = np.asarray(matrix, dtype=np.complex128)
    if candidate.ndim != 2 or candidate.shape[0] != candidate.shape[1]:
        raise ValueError("matrix must be square")
    hermiticity = np.linalg.norm(candidate - candidate.conj().T, ord="fro")
    if hermiticity > 1.0e-10:
        raise ValueError("matrix must be Hermitian")
    values, vectors = np.linalg.eigh(0.5 * (candidate + candidate.conj().T))
    if float(values.min()) <= eigenvalue_floor:
        raise ValueError("quasiparticle metric is not positive definite")
    inverse_sqrt = (vectors * (1.0 / np.sqrt(values))) @ vectors.conj().T
    return inverse_sqrt, values


def hermitian_sqrt(
    matrix: ComplexMatrix,
    *,
    eigenvalue_floor: float = 1.0e-12,
) -> tuple[ComplexMatrix, NDArray[np.float64]]:
    """Return the positive Hermitian square root and eigenvalues."""

    candidate = np.asarray(matrix, dtype=np.complex128)
    if candidate.ndim != 2 or candidate.shape[0] != candidate.shape[1]:
        raise ValueError("matrix must be square")
    hermiticity = np.linalg.norm(candidate - candidate.conj().T, ord="fro")
    if hermiticity > 1.0e-10:
        raise ValueError("matrix must be Hermitian")
    values, vectors = np.linalg.eigh(0.5 * (candidate + candidate.conj().T))
    if float(values.min()) <= eigenvalue_floor:
        raise ValueError("quasiparticle metric is not positive definite")
    square_root = (vectors * np.sqrt(values)) @ vectors.conj().T
    return square_root, values


def linearized_quasiparticle_hamiltonian(
    bare_hamiltonian: ComplexMatrix,
    sigma_at_reference: ComplexMatrix,
    sigma_derivative: ComplexMatrix,
    reference_ev: float,
) -> tuple[ComplexMatrix, dict[str, float]]:
    """Construct ``A^-1/2 B A^-1/2`` for a linearized matrix self-energy."""

    bare = np.asarray(bare_hamiltonian, dtype=np.complex128)
    sigma0 = np.asarray(sigma_at_reference, dtype=np.complex128)
    derivative = np.asarray(sigma_derivative, dtype=np.complex128)
    if bare.shape != sigma0.shape or bare.shape != derivative.shape:
        raise ValueError("bare Hamiltonian and self-energy matrices must have equal shape")
    dimension = bare.shape[0]
    metric = np.eye(dimension, dtype=np.complex128) - derivative
    inverse_sqrt, metric_eigenvalues = hermitian_inverse_sqrt(metric)
    effective_b = bare + sigma0 - float(reference_ev) * derivative
    effective_b = 0.5 * (effective_b + effective_b.conj().T)
    result = inverse_sqrt @ effective_b @ inverse_sqrt
    result = 0.5 * (result + result.conj().T)
    return result, {
        "minimum_metric_eigenvalue": float(metric_eigenvalues.min()),
        "maximum_metric_eigenvalue": float(metric_eigenvalues.max()),
        "hermiticity_residual": float(np.linalg.norm(result - result.conj().T)),
    }


def linear_self_energy_for_target(
    bare_hamiltonian: ComplexMatrix,
    target_hamiltonian: ComplexMatrix,
    sigma_derivative: ComplexMatrix,
    reference_ev: float,
) -> ComplexMatrix:
    """Return ``Sigma(reference)`` whose linearization gives ``target`` exactly."""

    bare = np.asarray(bare_hamiltonian, dtype=np.complex128)
    target = np.asarray(target_hamiltonian, dtype=np.complex128)
    derivative = np.asarray(sigma_derivative, dtype=np.complex128)
    if bare.shape != target.shape or bare.shape != derivative.shape:
        raise ValueError("bare, target and derivative matrices must have equal shape")
    metric = np.eye(bare.shape[0], dtype=np.complex128) - derivative
    square_root, _ = hermitian_sqrt(metric)
    effective_b = square_root @ target @ square_root
    sigma0 = effective_b - bare + float(reference_ev) * derivative
    return 0.5 * (sigma0 + sigma0.conj().T)


def solve_quasiparticle_pole(
    bare_energy_ev: float,
    self_energy: RationalSelfEnergy,
    bracket_ev: tuple[float, float],
    *,
    tolerance_ev: float = 1.0e-13,
    maximum_iterations: int = 300,
) -> float:
    """Solve ``E - epsilon - Sigma(E) = 0`` by fail-closed bisection."""

    lower, upper = map(float, bracket_ev)
    if not lower < upper:
        raise ValueError("quasiparticle bracket must be ordered")
    if lower < self_energy.remote_ev < upper:
        raise ValueError("quasiparticle bracket crosses the remote self-energy pole")

    def residual(energy: float) -> float:
        return energy - float(bare_energy_ev) - self_energy.value(energy)

    left = residual(lower)
    right = residual(upper)
    if left == 0.0:
        return lower
    if right == 0.0:
        return upper
    if left * right > 0.0:
        raise ValueError("quasiparticle bracket does not contain a sign change")
    for _ in range(maximum_iterations):
        middle = 0.5 * (lower + upper)
        value = residual(middle)
        if abs(value) <= tolerance_ev or 0.5 * (upper - lower) <= tolerance_ev:
            return middle
        if left * value <= 0.0:
            upper = middle
            right = value
        else:
            lower = middle
            left = value
    raise RuntimeError("quasiparticle pole solver did not converge")


def linearized_scalar_pole(
    bare_energy_ev: float,
    self_energy: RationalSelfEnergy,
    reference_ev: float,
) -> float:
    """Return the scalar quasiparticle pole from first-order linearization."""

    sigma0 = self_energy.value(reference_ev)
    derivative = self_energy.derivative(reference_ev)
    denominator = 1.0 - derivative
    if denominator <= 0.0:
        raise ValueError("scalar quasiparticle weight is nonpositive")
    return float(
        (float(bare_energy_ev) + sigma0 - reference_ev * derivative) / denominator
    )


def _real_vector(matrix: ComplexMatrix) -> NDArray[np.float64]:
    flat = np.asarray(matrix, dtype=np.complex128).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def fit_extended_kane_parameters(
    k_points_inverse_angstrom: Sequence[Iterable[float]],
    matrices_ev: Sequence[ComplexMatrix],
) -> tuple[ExtendedKaneParameters, dict[str, float]]:
    """Recover all extended-Kane parameters by deterministic matrix regression."""

    if len(k_points_inverse_angstrom) != len(matrices_ev) or not matrices_ev:
        raise ValueError("k points and matrices must have equal nonzero length")
    names = tuple(item.name for item in fields(ExtendedKaneParameters))
    zero = ExtendedKaneParameters()
    rows: list[NDArray[np.float64]] = []
    targets: list[NDArray[np.float64]] = []
    for k_point, observed in zip(k_points_inverse_angstrom, matrices_ev, strict=True):
        offset = hamiltonian_two_p(k_point, zero)
        columns = []
        for name in names:
            values = {item: 0.0 for item in names}
            values[name] = 1.0
            unit = ExtendedKaneParameters(**values)
            columns.append(_real_vector(hamiltonian_two_p(k_point, unit) - offset))
        rows.append(np.column_stack(columns))
        targets.append(_real_vector(np.asarray(observed) - offset))
    design = np.vstack(rows)
    target = np.concatenate(targets)
    solution, _, rank, singular_values = np.linalg.lstsq(design, target, rcond=None)
    if rank != len(names):
        raise RuntimeError(f"extended-Kane parameter fit is rank deficient: {rank}")
    residual = design @ solution - target
    parameters = ExtendedKaneParameters(**dict(zip(names, solution.tolist(), strict=True)))
    return parameters, {
        "design_rank": int(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "absolute_residual_ev": float(np.linalg.norm(residual)),
        "relative_residual": float(
            np.linalg.norm(residual) / max(np.linalg.norm(target), np.finfo(float).eps)
        ),
    }


def fit_one_p_kane_parameters(
    k_points_inverse_angstrom: Sequence[Iterable[float]],
    matrices_ev: Sequence[ComplexMatrix],
) -> tuple[KaneParameters, dict[str, float]]:
    """Fit the conventional one-P Kane model to an extended-Kane matrix target."""

    if len(k_points_inverse_angstrom) != len(matrices_ev) or not matrices_ev:
        raise ValueError("k points and matrices must have equal nonzero length")
    names = tuple(item.name for item in fields(KaneParameters))
    zero = KaneParameters()
    rows: list[NDArray[np.float64]] = []
    targets: list[NDArray[np.float64]] = []
    for k_point, observed in zip(k_points_inverse_angstrom, matrices_ev, strict=True):
        offset = hamiltonian(k_point, zero)
        columns = []
        for name in names:
            values = {item: 0.0 for item in names}
            values[name] = 1.0
            unit = KaneParameters(**values)
            columns.append(_real_vector(hamiltonian(k_point, unit) - offset))
        rows.append(np.column_stack(columns))
        targets.append(_real_vector(np.asarray(observed) - offset))
    design = np.vstack(rows)
    target = np.concatenate(targets)
    solution, _, rank, singular_values = np.linalg.lstsq(design, target, rcond=None)
    if rank != len(names):
        raise RuntimeError(f"one-P Kane parameter fit is rank deficient: {rank}")
    residual = design @ solution - target
    parameters = KaneParameters(**dict(zip(names, solution.tolist(), strict=True)))
    return parameters, {
        "design_rank": int(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "absolute_residual_ev": float(np.linalg.norm(residual)),
        "relative_residual": float(
            np.linalg.norm(residual) / max(np.linalg.norm(target), np.finfo(float).eps)
        ),
    }


def fit_fixed_bose_scales(
    temperatures_k: Sequence[float],
    values_ev: Sequence[float],
    theta_scales_k: Sequence[float],
    training_indices: Sequence[int],
) -> tuple[NDArray[np.float64], NDArray[np.float64], dict[str, float]]:
    """Fit amplitudes for fixed Bose scales and return predictions at all T."""

    temperatures = np.asarray(temperatures_k, dtype=float)
    values = np.asarray(values_ev, dtype=float)
    scales = np.asarray(theta_scales_k, dtype=float)
    indices = np.asarray(training_indices, dtype=int)
    if temperatures.ndim != 1 or values.shape != temperatures.shape:
        raise ValueError("temperatures and values must be equal one-dimensional arrays")
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("at least one fixed Bose scale is required")
    if indices.ndim != 1 or indices.size < scales.size:
        raise ValueError("training set is too small for fixed-scale fit")
    design = np.asarray(
        [
            [bose_thermal_factor(theta, temperature) for theta in scales]
            for temperature in temperatures
        ],
        dtype=float,
    )
    solution, _, rank, singular_values = np.linalg.lstsq(
        design[indices], values[indices], rcond=None
    )
    if rank != scales.size:
        raise RuntimeError("fixed-scale Bose fit is rank deficient")
    prediction = design @ solution
    residual = prediction[indices] - values[indices]
    return solution, prediction, {
        "design_rank": int(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "training_absolute_residual_ev": float(np.linalg.norm(residual)),
        "training_relative_residual": float(
            np.linalg.norm(residual)
            / max(np.linalg.norm(values[indices]), np.finfo(float).eps)
        ),
    }


def signed_thermal_moments(
    amplitudes_ev: Sequence[float],
    theta_scales_k: Sequence[float],
    powers: Sequence[int] = (-1, 0, 1),
) -> dict[str, float]:
    """Return signed moments ``mu_p = sum A_j theta_j^p``."""

    amplitudes = np.asarray(amplitudes_ev, dtype=float)
    scales = np.asarray(theta_scales_k, dtype=float)
    if amplitudes.shape != scales.shape or amplitudes.ndim != 1:
        raise ValueError("amplitudes and scales must be equal one-dimensional arrays")
    if np.any(scales <= 0.0):
        raise ValueError("thermal scales must be positive")
    return {
        str(int(power)): float(np.sum(amplitudes * scales ** int(power)))
        for power in powers
    }
