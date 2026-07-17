#!/usr/bin/env python3
"""Certify the Novik Gamma6/Gamma8/Gamma7 basis from symmetry matrices.

This is a deterministic group-theory protocol test. It does not analyze a
material calculation. Full symmetry representation matrices are required;
characters or irrep labels alone cannot determine a basis inside a degeneracy.
"""

from __future__ import annotations

import json
import math

import numpy as np


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def rotation(axis: tuple[float, float, float], angle: float) -> np.ndarray:
    n = np.asarray(axis, dtype=float)
    n /= np.linalg.norm(n)
    x, y, z = n
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return (
        math.cos(angle) * np.eye(3)
        + (1.0 - math.cos(angle)) * np.outer(n, n)
        + math.sin(angle) * cross
    )


def su2_from_proper_rotation(matrix: np.ndarray) -> np.ndarray:
    cosine = float(np.clip((np.trace(matrix) - 1.0) / 2.0, -1.0, 1.0))
    angle = math.acos(cosine)
    if angle < 1.0e-12:
        return I2.copy()
    axis = np.array(
        [
            matrix[2, 1] - matrix[1, 2],
            matrix[0, 2] - matrix[2, 0],
            matrix[1, 0] - matrix[0, 1],
        ]
    ) / (2.0 * math.sin(angle))
    return (
        math.cos(angle / 2.0) * I2
        - 1j * math.sin(angle / 2.0) * (axis[0] * SX + axis[1] * SY + axis[2] * SZ)
    )


def coupled_p_basis() -> tuple[np.ndarray, np.ndarray]:
    """Return the explicit Gamma8 and Gamma7 states of Novik Eq. (4).

    Cartesian orbital order is ``(X,Y,Z)`` and spin order is ``(up,down)``.
    The phase of the second Gamma7 state is essential: changing it preserves
    characters but breaks covariance of the published Kane Hamiltonian.
    """
    x = np.array([1.0, 0.0, 0.0])
    y = np.array([0.0, 1.0, 0.0])
    z = np.array([0.0, 0.0, 1.0])
    up = np.array([1.0, 0.0])
    down = np.array([0.0, 1.0])
    product = lambda orbital, spin: np.kron(orbital, spin)

    gamma8 = np.column_stack(
        [
            product(x + 1j * y, up) / math.sqrt(2.0),
            (product(x + 1j * y, down) - 2.0 * product(z, up))
            / math.sqrt(6.0),
            -(product(x - 1j * y, up) + 2.0 * product(z, down))
            / math.sqrt(6.0),
            -product(x - 1j * y, down) / math.sqrt(2.0),
        ]
    )
    gamma7 = np.column_stack(
        [
            (product(x + 1j * y, down) + product(z, up)) / math.sqrt(3.0),
            (product(x - 1j * y, up) - product(z, down)) / math.sqrt(3.0),
        ]
    )
    return gamma8, gamma7


def target_blocks(orthogonal: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Spin is axial: an improper polar operation R acts on spin through det(R) R.
    spin = su2_from_proper_rotation(np.linalg.det(orthogonal) * orthogonal)
    gamma8_basis, gamma7_basis = coupled_p_basis()
    p_spin = np.kron(orthogonal.astype(complex), spin)
    return (
        spin,
        gamma8_basis.conj().T @ p_spin @ gamma8_basis,
        gamma7_basis.conj().T @ p_spin @ gamma7_basis,
    )


def time_reversal_blocks() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return antiunitary matrices in the Novik/Kane phase convention.

    The p-like Bloch sector carries the conventional extra minus sign relative
    to the s-like sector. This reproduces the time-reversal unitary used by the
    executable Novik Hamiltonian rather than the bare Cartesian-orbital K gauge.
    """
    spin = np.array([[0.0, -1.0], [1.0, 0.0]], dtype=complex)
    gamma8_basis, gamma7_basis = coupled_p_basis()
    p_spin = -np.kron(np.eye(3), spin)
    return (
        spin,
        gamma8_basis.conj().T @ p_spin @ gamma8_basis.conj(),
        gamma7_basis.conj().T @ p_spin @ gamma7_basis.conj(),
    )


def random_unitary(dimension: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(matrix)
    phase = np.diag(r)
    return q * (phase / np.abs(phase)).conj()


def intertwiner(
    calculated: list[np.ndarray], target: list[np.ndarray]
) -> tuple[np.ndarray, np.ndarray, float]:
    dimension = target[0].shape[0]
    operator = np.vstack(
        [
            np.kron(np.eye(dimension), left)
            - np.kron(right.T, np.eye(dimension))
            for left, right in zip(calculated, target, strict=True)
        ]
    )
    _, singular_values, vh = np.linalg.svd(operator)
    raw = vh[-1].conj().reshape((dimension, dimension), order="F")
    left, _, right = np.linalg.svd(raw)
    unitary = left @ right
    residual = max(
        float(np.linalg.norm(a @ unitary - unitary @ b))
        for a, b in zip(calculated, target, strict=True)
    )
    return unitary, singular_values, residual


def nullity(singular_values: np.ndarray, threshold: float = 1.0e-10) -> int:
    return int(np.sum(singular_values < threshold))


def fix_time_reversal_phase(
    unitary: np.ndarray, calculated_tr: np.ndarray, target_tr: np.ndarray
) -> tuple[np.ndarray, float]:
    transformed = unitary.conj().T @ calculated_tr @ unitary.conj()
    scalar = np.trace(target_tr.conj().T @ transformed) / unitary.shape[0]
    unitary = unitary * np.exp(0.5j * np.angle(scalar))
    residual = float(
        np.linalg.norm(unitary.conj().T @ calculated_tr @ unitary.conj() - target_tr)
    )
    return unitary, residual


def analyze() -> dict[str, object]:
    c3 = rotation((1.0, 1.0, 1.0), 2.0 * math.pi / 3.0)
    s4 = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, -1.0]])
    generators = [target_blocks(c3), target_blocks(s4)]
    time_reversal = time_reversal_blocks()
    labels = ("Gamma6", "Gamma8", "Gamma7")
    dimensions = (2, 4, 2)

    result: dict[str, object] = {
        "status": "analytical_protocol_only_not_material_data",
        "basis_convention": "Novik_2005_Eq_4",
        "generators": ["C3_[111]", "S4_z"],
        "irreps": {},
    }
    maximum_recovery_error = 0.0
    maximum_symmetry_residual = 0.0
    maximum_time_reversal_residual = 0.0

    for index, (label, dimension) in enumerate(zip(labels, dimensions, strict=True)):
        target = [generator[index] for generator in generators]
        gauge = random_unitary(dimension, 120 + index)
        calculated = [gauge.conj().T @ matrix @ gauge for matrix in target]
        calculated_tr = gauge.conj().T @ time_reversal[index] @ gauge.conj()

        one_generator = intertwiner(calculated[:1], target[:1])
        recovered, singular_values, symmetry_residual = intertwiner(calculated, target)
        recovered, tr_residual = fix_time_reversal_phase(
            recovered, calculated_tr, time_reversal[index]
        )
        overlap = np.trace(gauge @ recovered) / dimension
        recovery_error = float(
            np.linalg.norm(recovered - np.exp(1j * np.angle(overlap)) * gauge.conj().T)
        )
        character_error = max(
            abs(np.trace(a) - np.trace(b))
            for a, b in zip(calculated, target, strict=True)
        )

        result["irreps"][label] = {
            "dimension": dimension,
            "target_characters": [
                [float(np.trace(matrix).real), float(np.trace(matrix).imag)]
                for matrix in target
            ],
            "character_error_after_random_gauge": float(character_error),
            "nullity_C3_only": nullity(one_generator[1]),
            "nullity_C3_and_S4": nullity(singular_values),
            "next_singular_value_above_nullspace": float(singular_values[-2]),
            "symmetry_intertwiner_residual": symmetry_residual,
            "time_reversal_residual_after_phase_fix": tr_residual,
            "recovery_error_up_to_remaining_sign": recovery_error,
        }
        maximum_recovery_error = max(maximum_recovery_error, recovery_error)
        maximum_symmetry_residual = max(maximum_symmetry_residual, symmetry_residual)
        maximum_time_reversal_residual = max(
            maximum_time_reversal_residual, tr_residual
        )

    if any(block["nullity_C3_and_S4"] != 1 for block in result["irreps"].values()):
        raise RuntimeError("generator pair did not produce a unique complex intertwiner")
    if maximum_recovery_error > 1.0e-12:
        raise RuntimeError("failed to recover the planted degenerate-subspace gauge")
    if maximum_time_reversal_residual > 1.0e-12:
        raise RuntimeError("time reversal failed to fix the continuous phase")

    result["maximum_recovery_error"] = maximum_recovery_error
    result["maximum_symmetry_residual"] = maximum_symmetry_residual
    result["maximum_time_reversal_residual"] = maximum_time_reversal_residual
    result["remaining_freedom"] = (
        "One discrete sign per inequivalent irrep remains after time reversal. Fix the "
        "relative signs by a declared Kane linear-k matrix-element convention."
    )
    result["decision"] = (
        "Characters identify Gamma6, Gamma8, and Gamma7 but cannot define their "
        "internal bases. Full C3 and S4 representation matrices give a unique complex "
        "intertwiner in each irrep by Schur's lemma; Novik-convention time reversal "
        "removes its continuous phase, leaving only conventional discrete signs."
    )
    return result


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
