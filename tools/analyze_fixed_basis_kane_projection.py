#!/usr/bin/env python3
"""Synthetic checks for overlap-metric projection into a fixed Kane basis."""

from __future__ import annotations

import json

import numpy as np


def inverse_sqrt_hermitian(matrix: np.ndarray, floor: float = 1.0e-12) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    if float(values.min()) <= floor:
        raise ValueError("projected subspace is rank deficient")
    inverse_sqrt = (vectors * (1.0 / np.sqrt(values))) @ vectors.conj().T
    return inverse_sqrt, values


def reconstruct_fixed_basis(overlap: np.ndarray, hamiltonian_in_target_basis: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    metric = overlap @ overlap.conj().T
    metric_inverse_sqrt, metric_eigenvalues = inverse_sqrt_hermitian(metric)
    isometry = metric_inverse_sqrt @ overlap
    fixed = isometry @ hamiltonian_in_target_basis @ isometry.conj().T
    fixed = 0.5 * (fixed + fixed.conj().T)
    return fixed, np.sqrt(metric_eigenvalues)


def random_hermitian(seed: int, size: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    return 0.5 * (raw + raw.conj().T)


def frobenius_relative_error(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / np.linalg.norm(right))


def analyze() -> dict[str, object]:
    size = 8
    reference_hamiltonian = random_hermitian(20260716, size)
    energies, eigenvectors = np.linalg.eigh(reference_hamiltonian)

    overlap = eigenvectors
    reconstructed, singular_values = reconstruct_fixed_basis(overlap, np.diag(energies))
    exact_error = frobenius_relative_error(reconstructed, reference_hamiltonian)

    permutation = np.asarray([3, 0, 7, 2, 5, 1, 6, 4])
    permuted_overlap = overlap[:, permutation]
    permuted_hamiltonian = np.diag(energies[permutation])
    permuted, _ = reconstruct_fixed_basis(permuted_overlap, permuted_hamiltonian)
    permutation_error = frobenius_relative_error(permuted, reference_hamiltonian)

    phases = np.exp(1j * np.linspace(0.2, 2.1, size))
    phased_overlap = overlap @ np.diag(phases)
    phased, _ = reconstruct_fixed_basis(phased_overlap, np.diag(energies))
    phase_error = frobenius_relative_error(phased, reference_hamiltonian)

    degenerate_energies = np.asarray([-2.0, -2.0, -0.5, -0.5, 0.3, 0.9, 1.4, 2.2])
    degenerate_vectors = np.linalg.qr(random_hermitian(8, size))[0]
    degenerate_reference = degenerate_vectors @ np.diag(degenerate_energies) @ degenerate_vectors.conj().T
    rotation = np.eye(size, dtype=complex)
    angle = 0.37
    rotation[:2, :2] = np.asarray([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    rotated_overlap = degenerate_vectors @ rotation
    rotated, _ = reconstruct_fixed_basis(rotated_overlap, np.diag(degenerate_energies))
    degenerate_rotation_error = frobenius_relative_error(rotated, degenerate_reference)

    leakage_angle = np.deg2rad(35.0)
    leakage_overlap = np.eye(size, dtype=complex)
    leakage_overlap[-1, -1] = np.cos(leakage_angle)
    _, leakage_singular_values = reconstruct_fixed_basis(leakage_overlap, np.diag(np.arange(size, dtype=float)))

    checks = {
        "exact_recovery_relative_error": exact_error,
        "permutation_invariance_relative_error": permutation_error,
        "phase_invariance_relative_error": phase_error,
        "degenerate_rotation_invariance_relative_error": degenerate_rotation_error,
        "exact_case_minimum_overlap_singular_value": float(singular_values.min()),
        "leakage_case_minimum_overlap_singular_value": float(leakage_singular_values.min()),
    }
    if max(exact_error, permutation_error, phase_error, degenerate_rotation_error) > 1.0e-12:
        raise RuntimeError(f"fixed-basis reconstruction check failed: {checks}")
    return {
        "method": "H_fixed = M^-1/2 S H_target S^dagger M^-1/2, M = S S^dagger",
        "checks": checks,
        "decision": "projection_preserves_physical_mixing_and_is_gauge_ordering_invariant",
        "warning": "rotating eigenvectors to maximize overlap and then reading a diagonal Hamiltonian would erase physical mixing",
        "production_rule": "reject or enlarge the target subspace when the minimum overlap singular value falls below the declared threshold",
    }


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
