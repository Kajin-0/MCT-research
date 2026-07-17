"""Group-theoretical construction and fitting helpers for quadratic 8-band invariants."""
from __future__ import annotations

from dataclasses import fields
import math
from typing import Any, Callable

import numpy as np

from analyze_kane_symmetry_intertwiner import rotation, target_blocks
from mct_research.kane8 import (
    ExtendedKaneParameters,
    hamiltonian_two_p,
    time_reversal_unitary,
)

SECTORS = ("66", "68", "67", "88", "87", "77")

def _block_diagonal(*matrices: np.ndarray) -> np.ndarray:
    dimension = sum(matrix.shape[0] for matrix in matrices)
    result = np.zeros((dimension, dimension), dtype=complex)
    offset = 0
    for matrix in matrices:
        stop = offset + matrix.shape[0]
        result[offset:stop, offset:stop] = matrix
        offset = stop
    return result


def _td_operations() -> list[tuple[np.ndarray, np.ndarray]]:
    c3 = rotation((1.0, 1.0, 1.0), 2.0 * math.pi / 3.0)
    s4 = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, -1.0]])
    generators = [
        (c3, _block_diagonal(*target_blocks(c3))),
        (s4, _block_diagonal(*target_blocks(s4))),
    ]
    elements = [(np.eye(3), np.eye(8, dtype=complex))]
    queue = [0]
    while queue:
        rotation_index = queue.pop(0)
        spatial, representation = elements[rotation_index]
        for generator_spatial, generator_representation in generators:
            candidate_spatial = spatial @ generator_spatial
            candidate_representation = representation @ generator_representation
            if not any(
                np.linalg.norm(candidate_spatial - known_spatial, ord="fro") < 1.0e-10
                for known_spatial, _ in elements
            ):
                elements.append((candidate_spatial, candidate_representation))
                queue.append(len(elements) - 1)
                if len(elements) > 24:
                    raise RuntimeError("C3/S4 generated more than 24 spatial Td operations")
    if len(elements) != 24:
        raise RuntimeError(f"expected 24 spatial Td operations, got {len(elements)}")
    return elements


def _symmetric_tensor_basis() -> list[np.ndarray]:
    basis = []
    for index in range(3):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[index, index] = 1.0
        basis.append(matrix)
    for first, second in ((1, 2), (2, 0), (0, 1)):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[first, second] = matrix[second, first] = 1.0 / math.sqrt(2.0)
        basis.append(matrix)
    return basis


def _state_label(index: int) -> str:
    if index < 2:
        return "6"
    if index < 6:
        return "8"
    return "7"


def _sector(first: int, second: int) -> str:
    order = {"6": 0, "8": 1, "7": 2}
    labels = sorted((_state_label(first), _state_label(second)), key=order.get)
    return "".join(labels)


def _hermitian_basis() -> tuple[list[np.ndarray], list[str]]:
    basis: list[np.ndarray] = []
    sectors: list[str] = []
    for index in range(8):
        matrix = np.zeros((8, 8), dtype=complex)
        matrix[index, index] = 1.0
        basis.append(matrix)
        sectors.append(_sector(index, index))
    for first in range(8):
        for second in range(first + 1, 8):
            real = np.zeros((8, 8), dtype=complex)
            real[first, second] = real[second, first] = 1.0 / math.sqrt(2.0)
            basis.append(real)
            sectors.append(_sector(first, second))
            imaginary = np.zeros((8, 8), dtype=complex)
            imaginary[first, second] = -1.0j / math.sqrt(2.0)
            imaginary[second, first] = 1.0j / math.sqrt(2.0)
            basis.append(imaginary)
            sectors.append(_sector(first, second))
    if len(basis) != 64:
        raise RuntimeError("Hermitian basis dimension is not 64")
    return basis, sectors


def _matrix_action(
    representation: np.ndarray,
    hermitian_basis: list[np.ndarray],
    *,
    antiunitary: bool = False,
) -> np.ndarray:
    action = np.zeros((64, 64), dtype=float)
    for column, matrix in enumerate(hermitian_basis):
        transformed = (
            representation @ matrix.conj() @ representation.conj().T
            if antiunitary
            else representation @ matrix @ representation.conj().T
        )
        for row, target in enumerate(hermitian_basis):
            action[row, column] = float(
                np.trace(target.conj().T @ transformed).real
            )
    return action


def build_quadratic_projector() -> tuple[
    np.ndarray, list[np.ndarray], list[np.ndarray], list[str], dict[str, float]
]:
    tensors = _symmetric_tensor_basis()
    hermitian, sectors = _hermitian_basis()
    group_projector = np.zeros((384, 384), dtype=float)
    for spatial, representation in _td_operations():
        tensor_action = np.array(
            [
                [
                    np.trace(target.T @ (spatial @ source @ spatial.T))
                    for source in tensors
                ]
                for target in tensors
            ],
            dtype=float,
        )
        matrix_action = _matrix_action(representation, hermitian)
        group_projector += np.kron(tensor_action, matrix_action)
    group_projector /= 24.0
    time_reversal_action = _matrix_action(
        time_reversal_unitary(), hermitian, antiunitary=True
    )
    tr_even_projector = np.kron(
        np.eye(6), 0.5 * (np.eye(64) + time_reversal_action)
    )
    projector = group_projector @ tr_even_projector
    diagnostics = {
        "symmetry_residual": float(np.linalg.norm(projector - projector.T)),
        "idempotency_residual": float(np.linalg.norm(projector @ projector - projector)),
        "group_time_reversal_commutator": float(
            np.linalg.norm(group_projector @ tr_even_projector - tr_even_projector @ group_projector)
        ),
        "trace": float(np.trace(projector)),
    }
    return projector, tensors, hermitian, sectors, diagnostics


def _orthonormalize(candidates: list[np.ndarray], tolerance: float = 1.0e-10) -> np.ndarray:
    basis: list[np.ndarray] = []
    for candidate in candidates:
        vector = np.asarray(candidate, dtype=float).copy()
        for known in basis:
            vector -= known * float(known @ vector)
        for known in basis:
            vector -= known * float(known @ vector)
        norm = float(np.linalg.norm(vector))
        if norm <= tolerance:
            continue
        vector /= norm
        first = np.flatnonzero(np.abs(vector) > 1.0e-12)
        if first.size and vector[first[0]] < 0.0:
            vector *= -1.0
        basis.append(vector)
    if not basis:
        return np.zeros((len(candidates[0]), 0), dtype=float)
    return np.column_stack(basis)


def _projected_basis(
    projector: np.ndarray, raw_indices: list[int] | None = None
) -> np.ndarray:
    indices = list(range(projector.shape[0])) if raw_indices is None else raw_indices
    return _orthonormalize([projector[:, index] for index in indices])


def _coefficient_matrices(
    coefficient: np.ndarray, hermitian_basis: list[np.ndarray]
) -> np.ndarray:
    reshaped = np.asarray(coefficient, dtype=float).reshape(6, 64)
    return np.asarray(
        [
            sum(reshaped[tensor, matrix] * hermitian_basis[matrix] for matrix in range(64))
            for tensor in range(6)
        ]
    )


def _evaluate(
    coefficient: np.ndarray,
    k: np.ndarray,
    tensors: list[np.ndarray],
    hermitian_basis: list[np.ndarray],
) -> np.ndarray:
    k = np.asarray(k, dtype=float)
    monomials = np.asarray([k @ tensor @ k for tensor in tensors], dtype=float)
    return np.tensordot(
        monomials, _coefficient_matrices(coefficient, hermitian_basis), axes=(0, 0)
    )


def _real_vector(matrix: np.ndarray) -> np.ndarray:
    flat = np.asarray(matrix, dtype=complex).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def _function_coefficients(
    function: Callable[[np.ndarray], np.ndarray],
    tensors: list[np.ndarray],
    hermitian_basis: list[np.ndarray],
) -> np.ndarray:
    samples = np.asarray(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
        ]
    )
    monomials = np.asarray(
        [[sample @ tensor @ sample for tensor in tensors] for sample in samples]
    )
    observations = np.asarray(
        [
            [
                np.trace(target.conj().T @ function(sample)).real
                for target in hermitian_basis
            ]
            for sample in samples
        ]
    )
    return np.linalg.solve(monomials, observations).reshape(-1)


def _conventional_span(
    tensors: list[np.ndarray], hermitian_basis: list[np.ndarray]
) -> tuple[np.ndarray, np.ndarray]:
    zero = ExtendedKaneParameters()
    names = ("f", "gamma1", "gamma2", "gamma3")
    parameter_names = tuple(field.name for field in fields(ExtendedKaneParameters))
    columns = []
    for name in names:
        values = {parameter: 0.0 for parameter in parameter_names}
        values[name] = 1.0
        parameters = ExtendedKaneParameters(**values)
        columns.append(
            _function_coefficients(
                lambda k, parameters=parameters: hamiltonian_two_p(k, parameters)
                - hamiltonian_two_p(k, zero),
                tensors,
                hermitian_basis,
            )
        )
    raw = np.column_stack(columns)
    return raw, _orthonormalize(columns)


def _fit_subspace(
    basis: np.ndarray,
    observations: dict[str, np.ndarray],
    directions: dict[str, np.ndarray],
    training: list[str],
    tensors: list[np.ndarray],
    hermitian_basis: list[np.ndarray],
) -> dict[str, Any]:
    design = np.vstack(
        [
            np.column_stack(
                [
                    _real_vector(
                        _evaluate(basis[:, index], directions[name], tensors, hermitian_basis)
                    )
                    for index in range(basis.shape[1])
                ]
            )
            for name in training
        ]
    )
    target = np.concatenate([_real_vector(observations[name]) for name in training])
    solution, _, rank, singular_values = np.linalg.lstsq(design, target, rcond=None)
    predicted = {
        name: sum(
            solution[index]
            * _evaluate(basis[:, index], direction, tensors, hermitian_basis)
            for index in range(basis.shape[1])
        )
        for name, direction in directions.items()
    }
    residuals = {
        name: float(
            np.linalg.norm(observations[name] - predicted[name], ord="fro")
            / max(np.linalg.norm(observations[name], ord="fro"), np.finfo(float).eps)
        )
        for name in observations
    }
    return {
        "dimension": int(basis.shape[1]),
        "design_rank": int(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "training_relative_residual": float(
            np.linalg.norm(design @ solution - target) / np.linalg.norm(target)
        ),
        "direction_relative_residuals": residuals,
        "orthonormal_basis_coefficients_ev_angstrom2": solution.tolist(),
    }

