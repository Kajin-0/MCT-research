#!/usr/bin/env python3
"""Independent post-processing reproduction of the static CdTe selected-band result.

The implementation deliberately avoids the repository's existing finite-k projection,
quadratic-invariant, Weiler-template, and corrected-static analysis modules. It uses
only the immutable raw overlap/eigenvalue evidence, the committed canonical-basis
record, the raw symmetry-probe operations, and the public Kane Hamiltonian.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import fields
from pathlib import Path
from typing import Any, Callable

import numpy as np

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p

SELECTED = slice(30, 38)
SELECTED_BANDS_ONE_BASED = list(range(31, 39))
CANONICAL_ORDER = ("Gamma6", "Gamma8", "Gamma7")
TRAINING = ("001", "111")
HOLDOUT = "110"
PARAMETER_NAMES = tuple(item.name for item in fields(ExtendedKaneParameters))


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def complex_array(payload: Any) -> np.ndarray:
    array = np.asarray(payload, dtype=float)
    if array.shape[-1] != 2:
        raise ValueError("complex arrays must use trailing [real, imaginary] pairs")
    return array[..., 0] + 1j * array[..., 1]


def real_vector(matrix: np.ndarray) -> np.ndarray:
    flat = np.asarray(matrix, dtype=complex).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def parse_mmn(
    path: str | Path,
) -> tuple[
    int,
    int,
    int,
    list[tuple[int, int, tuple[int, int, int], np.ndarray]],
]:
    """Parse Wannier90 MMN independently, including n-outer/m-inner ordering."""

    with Path(path).open("r", encoding="utf-8") as stream:
        if stream.readline() == "":
            raise ValueError("missing MMN comment")
        header = stream.readline().split()
        if len(header) != 3:
            raise ValueError("invalid MMN header")
        nbnd, nk, nntot = map(int, header)
        blocks = []
        for _ in range(nk * nntot):
            metadata = stream.readline().split()
            if len(metadata) != 5:
                raise ValueError("invalid MMN block metadata")
            source, target, g1, g2, g3 = map(int, metadata)
            matrix = np.empty((nbnd, nbnd), dtype=complex)
            for n in range(nbnd):
                for m in range(nbnd):
                    values = stream.readline().split()
                    if len(values) != 2:
                        raise ValueError("invalid MMN matrix element")
                    matrix[m, n] = complex(float(values[0]), float(values[1]))
            if not np.all(np.isfinite(matrix)):
                raise ValueError("MMN contains non-finite values")
            blocks.append((source, target, (g1, g2, g3), matrix))
        if stream.read().strip():
            raise ValueError("unexpected trailing MMN content")
    return nbnd, nk, nntot, blocks


def parse_nnkp(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    def section(start: str, end: str) -> list[str]:
        first = lines.index(start) + 1
        last = lines.index(end)
        return lines[first:last]

    reciprocal = np.asarray(
        [
            [float(value) for value in line.split()]
            for line in section("begin recip_lattice", "end recip_lattice")
        ],
        dtype=float,
    )
    kpoint_lines = section("begin kpoints", "end kpoints")
    count = int(kpoint_lines[0])
    reduced = np.asarray(
        [
            [float(value) for value in line.split()]
            for line in kpoint_lines[1:]
        ],
        dtype=float,
    )
    if reciprocal.shape != (3, 3) or reduced.shape != (count, 3):
        raise ValueError("invalid NNKP reciprocal lattice or k-point section")
    return reduced, reduced @ reciprocal


def load_eigenvalues(path: str | Path) -> list[np.ndarray]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("num_kpoints") != 13 or payload.get("num_bands") != 40:
        raise ValueError("expected 13 exact 40-band eigenvalue blocks")
    values = []
    for expected, block in enumerate(payload["blocks"], start=1):
        if int(block.get("index", -1)) != expected:
            raise ValueError("eigenvalue blocks are not in exact k-point order")
        array = np.asarray(block["eigenvalues_ev"], dtype=float)
        if array.shape != (40,) or not np.all(np.isfinite(array)):
            raise ValueError("invalid eigenvalue block")
        values.append(array)
    return values


def canonical_columns(basis_payload: dict[str, Any]) -> np.ndarray:
    if (
        basis_payload.get("selected_global_bands_one_based")
        != SELECTED_BANDS_ONE_BASED
    ):
        raise ValueError("canonical basis does not use selected bands 31-38")
    by_probe = sorted(
        basis_payload["irreps"].items(),
        key=lambda item: int(item[1]["probe_block_index"]),
    )
    sizes = [len(record["bands_one_based"]) for _, record in by_probe]
    if sizes != [2, 4, 2]:
        raise ValueError(
            "expected probe order Gamma7/Gamma8/Gamma6 with dimensions 2/4/2"
        )
    block = np.zeros((8, 8), dtype=complex)
    offsets: dict[str, tuple[int, int]] = {}
    offset = 0
    for label, record in by_probe:
        intertwiner = complex_array(record["intertwiner"])
        dimension = intertwiner.shape[0]
        block[offset : offset + dimension, offset : offset + dimension] = (
            intertwiner
        )
        offsets[label] = (offset, offset + dimension)
        offset += dimension
    columns: list[int] = []
    for label in CANONICAL_ORDER:
        columns.extend(range(*offsets[label]))
    canonical = block[:, columns]
    if (
        np.linalg.norm(canonical.conj().T @ canonical - np.eye(8))
        > 1.0e-10
    ):
        raise ValueError("canonical intertwiners are not unitary")
    return canonical


def reconstruct_svd_polar(
    mmn_path: str | Path,
    eigenvalues_path: str | Path,
    basis_path: str | Path,
) -> tuple[list[np.ndarray], list[dict[str, float]], np.ndarray]:
    nbnd, nk, nntot, blocks = parse_mmn(mmn_path)
    if (nbnd, nk, nntot, len(blocks)) != (40, 13, 1, 13):
        raise ValueError("expected a 40-band, 13-point Gamma-star MMN")
    by_source = {
        source: (target, image, matrix)
        for source, target, image, matrix in blocks
    }
    if set(by_source) != set(range(1, 14)):
        raise ValueError("MMN source indices must be exactly 1-13")
    for target, image, _ in by_source.values():
        if target != 1 or image != (0, 0, 0):
            raise ValueError("every finite-k overlap must link directly to Gamma")

    eigenvalues = load_eigenvalues(eigenvalues_path)
    basis_payload = json.loads(Path(basis_path).read_text(encoding="utf-8"))
    canonical = canonical_columns(basis_payload)

    matrices: list[np.ndarray] = []
    diagnostics: list[dict[str, float]] = []
    for source in range(1, 14):
        matrix = by_source[source][2]
        # Wannier90 stores M(source,Gamma). The fixed-reference selected overlap is
        # S = M^dagger restricted to Gamma rows and selected finite-k columns.
        overlap = matrix.conj().T[SELECTED, SELECTED]
        left, singular_values, right_h = np.linalg.svd(
            overlap, full_matrices=False
        )
        polar = left @ right_h
        fixed = (
            polar
            @ np.diag(eigenvalues[source - 1][SELECTED])
            @ polar.conj().T
        )
        canonical_matrix = canonical.conj().T @ fixed @ canonical
        canonical_matrix = 0.5 * (
            canonical_matrix + canonical_matrix.conj().T
        )
        selected = np.sort(eigenvalues[source - 1][SELECTED])
        reconstructed = np.linalg.eigvalsh(canonical_matrix)
        matrices.append(canonical_matrix)
        diagnostics.append(
            {
                "minimum_overlap_singular_value": float(
                    np.min(singular_values)
                ),
                "maximum_overlap_singular_value": float(
                    np.max(singular_values)
                ),
                "polar_unitarity_residual": float(
                    np.linalg.norm(
                        polar.conj().T @ polar - np.eye(8)
                    )
                ),
                "maximum_selected_eigenvalue_absolute_error_ev": float(
                    np.max(np.abs(reconstructed - selected))
                ),
            }
        )
    return matrices, diagnostics, canonical


def validate_kpoints(cartesian: np.ndarray, contract: dict[str, Any]) -> float:
    if cartesian.shape != (13, 3) or np.linalg.norm(cartesian[0]) > 1.0e-10:
        raise ValueError("expected 13 k points beginning at Gamma")
    maximum = 0.0
    for name, spec in contract["pairs"].items():
        direction = np.asarray(spec["unit_direction"], dtype=float)
        direction /= np.linalg.norm(direction)
        radius = float(spec["radius_inverse_angstrom"])
        expected = {
            "plus_h": radius * direction,
            "minus_h": -radius * direction,
            "plus_h_over_2": 0.5 * radius * direction,
            "minus_h_over_2": -0.5 * radius * direction,
        }
        for key, target in expected.items():
            index = int(spec[key]) - 1
            residual = float(np.linalg.norm(cartesian[index] - target))
            maximum = max(maximum, residual)
            if residual > 1.0e-7:
                raise ValueError(f"{name} {key} k point violates the contract")
    return maximum


def apply_signs(
    matrices: list[np.ndarray], gamma8: int, gamma7: int
) -> list[np.ndarray]:
    signs = np.asarray([1, 1] + [gamma8] * 4 + [gamma7] * 2, dtype=float)
    transform = np.diag(signs)
    return [transform @ matrix @ transform for matrix in matrices]


def extract_radius_coefficients(
    matrices: list[np.ndarray],
    pairs: dict[str, dict[str, Any]],
    mode: str,
) -> dict[str, dict[str, np.ndarray]]:
    if mode not in {"coarse", "fine", "richardson"}:
        raise ValueError("radius mode must be coarse, fine, or richardson")
    gamma = matrices[0]
    result: dict[str, dict[str, np.ndarray]] = {}
    for name, spec in pairs.items():
        plus_h, minus_h, plus_fine, minus_fine = [
            int(spec[key]) - 1
            for key in (
                "plus_h",
                "minus_h",
                "plus_h_over_2",
                "minus_h_over_2",
            )
        ]
        radius = float(spec["radius_inverse_angstrom"])
        linear_coarse = (
            matrices[plus_h] - matrices[minus_h]
        ) / (2.0 * radius)
        linear_fine = (
            matrices[plus_fine] - matrices[minus_fine]
        ) / radius
        quadratic_coarse = (
            matrices[plus_h] + matrices[minus_h] - 2.0 * gamma
        ) / (2.0 * radius**2)
        quadratic_fine = (
            matrices[plus_fine] + matrices[minus_fine] - 2.0 * gamma
        ) / (2.0 * (radius / 2.0) ** 2)
        if mode == "coarse":
            linear, quadratic = linear_coarse, quadratic_coarse
        elif mode == "fine":
            linear, quadratic = linear_fine, quadratic_fine
        else:
            linear = (4.0 * linear_fine - linear_coarse) / 3.0
            quadratic = (4.0 * quadratic_fine - quadratic_coarse) / 3.0
        result[name] = {
            "linear": 0.5 * (linear + linear.conj().T),
            "quadratic": 0.5 * (quadratic + quadratic.conj().T),
        }
    return result


def block_diagonal(matrices: list[np.ndarray]) -> np.ndarray:
    dimension = sum(matrix.shape[0] for matrix in matrices)
    result = np.zeros((dimension, dimension), dtype=complex)
    offset = 0
    for matrix in matrices:
        stop = offset + matrix.shape[0]
        result[offset:stop, offset:stop] = matrix
        offset = stop
    return result


def hermitian_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for index in range(8):
        matrix = np.zeros((8, 8), dtype=complex)
        matrix[index, index] = 1.0
        basis.append(matrix)
    for first in range(8):
        for second in range(first + 1, 8):
            real = np.zeros((8, 8), dtype=complex)
            real[first, second] = real[second, first] = 1.0 / math.sqrt(2.0)
            basis.append(real)
            imaginary = np.zeros((8, 8), dtype=complex)
            imaginary[first, second] = -1.0j / math.sqrt(2.0)
            imaginary[second, first] = 1.0j / math.sqrt(2.0)
            basis.append(imaginary)
    if len(basis) != 64:
        raise RuntimeError("Hermitian basis dimension is not 64")
    return basis


def quadratic_tensor_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for index in range(3):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[index, index] = 1.0
        basis.append(matrix)
    for first, second in ((1, 2), (2, 0), (0, 1)):
        matrix = np.zeros((3, 3), dtype=float)
        matrix[first, second] = matrix[second, first] = (
            1.0 / math.sqrt(2.0)
        )
        basis.append(matrix)
    return basis


def matrix_action(
    representation: np.ndarray,
    basis: list[np.ndarray],
    *,
    antiunitary: bool,
) -> np.ndarray:
    action = np.empty((64, 64), dtype=float)
    for column, source in enumerate(basis):
        transformed = (
            representation
            @ (source.conj() if antiunitary else source)
            @ representation.conj().T
        )
        action[:, column] = [
            float(np.trace(target.conj().T @ transformed).real)
            for target in basis
        ]
    return action


def canonical_symmetry_operations(
    probe_payload: dict[str, Any], canonical: np.ndarray
) -> list[tuple[np.ndarray, np.ndarray, bool]]:
    operations = []
    for operation in probe_payload["operations"]:
        raw = block_diagonal(
            [complex_array(block) for block in operation["unitary_blocks"]]
        )
        antiunitary = bool(operation["time_reversal"])
        # Antiunitary basis changes use C* on the right: C^dagger U C* K.
        representation = canonical.conj().T @ raw @ (
            canonical.conj() if antiunitary else canonical
        )
        rotation = np.asarray(operation["rotation_cartesian"], dtype=float)
        if (
            np.linalg.norm(
                representation.conj().T @ representation - np.eye(8)
            )
            > 1.0e-10
        ):
            raise ValueError("canonical symmetry representation is not unitary")
        operations.append((rotation, representation, antiunitary))
    if len(operations) != 48 or sum(item[2] for item in operations) != 24:
        raise ValueError("expected 24 unitary and 24 antiunitary operations")
    return operations


def invariant_projectors(
    probe_payload: dict[str, Any], canonical: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    hermitian = hermitian_basis()
    tensors = quadratic_tensor_basis()
    operations = canonical_symmetry_operations(probe_payload, canonical)

    group_linear = np.zeros((3 * 64, 3 * 64), dtype=float)
    group_quadratic = np.zeros((6 * 64, 6 * 64), dtype=float)
    unitary_count = 0
    for rotation, representation, antiunitary in operations:
        if antiunitary:
            continue
        unitary_count += 1
        matrix_map = matrix_action(
            representation, hermitian, antiunitary=False
        )
        tensor_map = np.asarray(
            [
                [
                    np.trace(target.T @ (rotation @ source @ rotation.T))
                    for source in tensors
                ]
                for target in tensors
            ],
            dtype=float,
        )
        group_linear += np.kron(rotation, matrix_map)
        group_quadratic += np.kron(tensor_map, matrix_map)
    if unitary_count != 24:
        raise ValueError("expected 24 unitary spatial operations")
    group_linear /= unitary_count
    group_quadratic /= unitary_count

    pure_time_reversal = min(
        (item for item in operations if item[2]),
        key=lambda item: np.linalg.norm(item[0] - np.eye(3)),
    )
    if np.linalg.norm(pure_time_reversal[0] - np.eye(3)) > 1.0e-8:
        raise ValueError("pure time reversal was not found")
    time_reversal_map = matrix_action(
        pure_time_reversal[1], hermitian, antiunitary=True
    )
    tr_odd = np.kron(
        np.eye(3), 0.5 * (np.eye(64) - time_reversal_map)
    )
    tr_even = np.kron(
        np.eye(6), 0.5 * (np.eye(64) + time_reversal_map)
    )

    linear = group_linear @ tr_odd
    quadratic = group_quadratic @ tr_even
    diagnostics = {
        "linear_trace": float(np.trace(linear)),
        "linear_idempotency_residual": float(
            np.linalg.norm(linear @ linear - linear)
        ),
        "linear_symmetry_residual": float(np.linalg.norm(linear - linear.T)),
        "quadratic_trace": float(np.trace(quadratic)),
        "quadratic_idempotency_residual": float(
            np.linalg.norm(quadratic @ quadratic - quadratic)
        ),
        "quadratic_symmetry_residual": float(
            np.linalg.norm(quadratic - quadratic.T)
        ),
    }
    return linear, quadratic, diagnostics


def projector_basis(
    projector: np.ndarray, expected_dimension: int
) -> tuple[np.ndarray, np.ndarray]:
    symmetric = 0.5 * (projector + projector.T)
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    selected = np.flatnonzero(eigenvalues > 0.5)
    if selected.size != expected_dimension:
        raise RuntimeError(
            f"invariant dimension is {selected.size}, expected {expected_dimension}"
        )
    basis, _ = np.linalg.qr(eigenvectors[:, selected])
    return basis, eigenvalues[selected]


def coefficient_matrices(
    coefficient: np.ndarray,
    count: int,
    hermitian: list[np.ndarray],
) -> np.ndarray:
    reshaped = np.asarray(coefficient, dtype=float).reshape(count, 64)
    return np.asarray(
        [
            sum(
                reshaped[tensor, index] * hermitian[index]
                for index in range(64)
            )
            for tensor in range(count)
        ]
    )


def evaluate_linear(
    coefficient: np.ndarray,
    direction: np.ndarray,
    hermitian: list[np.ndarray],
) -> np.ndarray:
    return np.tensordot(
        np.asarray(direction, dtype=float),
        coefficient_matrices(coefficient, 3, hermitian),
        axes=(0, 0),
    )


def evaluate_quadratic(
    coefficient: np.ndarray,
    direction: np.ndarray,
    tensors: list[np.ndarray],
    hermitian: list[np.ndarray],
) -> np.ndarray:
    direction = np.asarray(direction, dtype=float)
    monomials = np.asarray(
        [direction @ tensor @ direction for tensor in tensors]
    )
    return np.tensordot(
        monomials,
        coefficient_matrices(coefficient, 6, hermitian),
        axes=(0, 0),
    )


def fit_invariant_basis(
    basis: np.ndarray,
    observations: dict[str, np.ndarray],
    directions: dict[str, np.ndarray],
    evaluator: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> dict[str, Any]:
    rows = []
    target = []
    for name in TRAINING:
        rows.append(
            np.column_stack(
                [
                    real_vector(evaluator(basis[:, index], directions[name]))
                    for index in range(basis.shape[1])
                ]
            )
        )
        target.append(real_vector(observations[name]))
    design = np.vstack(rows)
    vector = np.concatenate(target)
    solution, _, rank, singular_values = np.linalg.lstsq(
        design, vector, rcond=None
    )
    predicted = {
        name: sum(
            solution[index] * evaluator(basis[:, index], direction)
            for index in range(basis.shape[1])
        )
        for name, direction in directions.items()
    }
    residuals = {
        name: float(
            np.linalg.norm(observations[name] - predicted[name])
            / max(np.linalg.norm(observations[name]), np.finfo(float).eps)
        )
        for name in observations
    }
    return {
        "dimension": int(basis.shape[1]),
        "design_rank": int(rank),
        "condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
        "training_relative_residual": float(
            np.linalg.norm(design @ solution - vector) / np.linalg.norm(vector)
        ),
        "direction_relative_residuals": residuals,
    }


def parameter_template(
    name: str, direction: np.ndarray, order: str
) -> np.ndarray:
    values = {parameter: 0.0 for parameter in PARAMETER_NAMES}
    values[name] = 1.0
    parameter = ExtendedKaneParameters(**values)
    zero = ExtendedKaneParameters()
    if order == "linear":
        return 0.5 * (
            hamiltonian_two_p(direction, parameter)
            - hamiltonian_two_p(-direction, parameter)
        )
    if order == "quadratic":
        return hamiltonian_two_p(
            direction, parameter
        ) - hamiltonian_two_p(direction, zero)
    raise ValueError("template order must be linear or quadratic")


def fit_conventional(
    observations: dict[str, np.ndarray],
    directions: dict[str, np.ndarray],
    names: tuple[str, ...],
    order: str,
) -> dict[str, Any]:
    rows = []
    target = []
    for direction_name in TRAINING:
        rows.append(
            np.column_stack(
                [
                    real_vector(
                        parameter_template(
                            name, directions[direction_name], order
                        )
                    )
                    for name in names
                ]
            )
        )
        target.append(real_vector(observations[direction_name]))
    design = np.vstack(rows)
    vector = np.concatenate(target)
    solution, _, rank, singular_values = np.linalg.lstsq(
        design, vector, rcond=None
    )
    predicted = {
        direction_name: sum(
            solution[index] * parameter_template(name, direction, order)
            for index, name in enumerate(names)
        )
        for direction_name, direction in directions.items()
    }
    residuals = {
        direction_name: float(
            np.linalg.norm(
                observations[direction_name] - predicted[direction_name]
            )
            / max(
                np.linalg.norm(observations[direction_name]),
                np.finfo(float).eps,
            )
        )
        for direction_name in observations
    }
    return {
        "parameters": {
            name: float(solution[index]) for index, name in enumerate(names)
        },
        "design_rank": int(rank),
        "condition_number": float(
            singular_values[0] / singular_values[-1]
        ),
        "training_relative_residual": float(
            np.linalg.norm(design @ solution - vector) / np.linalg.norm(vector)
        ),
        "direction_relative_residuals": residuals,
    }


def choose_signs(
    matrices: list[np.ndarray],
    pairs: dict[str, dict[str, Any]],
    directions: dict[str, np.ndarray],
) -> tuple[list[np.ndarray], dict[str, Any]]:
    candidates = []
    for gamma8 in (1, -1):
        for gamma7 in (1, -1):
            signed = apply_signs(matrices, gamma8, gamma7)
            coefficients = extract_radius_coefficients(
                signed, pairs, "richardson"
            )
            linear = {
                name: record["linear"]
                for name, record in coefficients.items()
            }
            fit = fit_conventional(
                linear, directions, ("p8", "p7"), "linear"
            )
            candidates.append(
                {
                    "gamma8_sign": gamma8,
                    "gamma7_sign": gamma7,
                    "p8_ev_angstrom": fit["parameters"]["p8"],
                    "p7_ev_angstrom": fit["parameters"]["p7"],
                    "linear_training_relative_residual": fit[
                        "training_relative_residual"
                    ],
                }
            )
    positive = [
        item
        for item in candidates
        if item["p8_ev_angstrom"] > 0.0
        and item["p7_ev_angstrom"] > 0.0
    ]
    if len(positive) != 1:
        raise RuntimeError(
            "positive P8/P7 convention does not select one sign pair"
        )
    selected = positive[0]
    return (
        apply_signs(
            matrices,
            int(selected["gamma8_sign"]),
            int(selected["gamma7_sign"]),
        ),
        {"candidates": candidates, "selected": selected},
    )


def relative_range(values: list[float]) -> float:
    scale = max(abs(value) for value in values)
    if scale == 0.0:
        return 0.0
    return (max(values) - min(values)) / scale


def compare_reference(
    result: dict[str, Any], reference: dict[str, Any]
) -> dict[str, float]:
    independent = result["richardson"]
    reference_quadratic = reference[
        "quadratic_matrix_closure_in_polar_gauge"
    ]
    return {
        "p8_absolute_difference_ev_angstrom": abs(
            independent["two_p_linear"]["parameters"]["p8"]
            - float(reference["linear"]["p8_ev_angstrom"])
        ),
        "p7_absolute_difference_ev_angstrom": abs(
            independent["two_p_linear"]["parameters"]["p7"]
            - float(reference["linear"]["p7_ev_angstrom"])
        ),
        "complete_quadratic_training_residual_difference": abs(
            independent["complete_quadratic"]["training_relative_residual"]
            - float(
                reference_quadratic["complete_training_relative_residual"]
            )
        ),
        "complete_quadratic_110_residual_difference": abs(
            independent["complete_quadratic"][
                "direction_relative_residuals"
            ][HOLDOUT]
            - float(
                reference_quadratic[
                    "complete_maximum_holdout_relative_residual"
                ]
            )
        ),
        "conventional_quadratic_training_residual_difference": abs(
            independent["conventional_quadratic"][
                "training_relative_residual"
            ]
            - float(
                reference_quadratic[
                    "conventional_training_relative_residual"
                ]
            )
        ),
        "conventional_quadratic_110_residual_difference": abs(
            independent["conventional_quadratic"][
                "direction_relative_residuals"
            ][HOLDOUT]
            - float(
                reference_quadratic[
                    "conventional_maximum_holdout_relative_residual"
                ]
            )
        ),
    }


def analyze(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_path: str | Path,
    symmetry_probe_path: str | Path,
    contract_path: str | Path,
    reference_path: str | Path | None = None,
) -> dict[str, Any]:
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if (
        contract.get("reconstruction", {}).get("scientific_mode")
        != "selected_band_polar"
    ):
        raise ValueError(
            "contract does not declare selected-band polar reconstruction"
        )
    if tuple(contract.get("training_directions", [])) != TRAINING:
        raise ValueError("training directions must be [001] and [111]")
    if contract.get("holdout_directions") != [HOLDOUT]:
        raise ValueError("[110] must remain the sole holdout")

    _, cartesian = parse_nnkp(nnkp_path)
    kpoint_residual = validate_kpoints(cartesian, contract)
    matrices, reconstruction, canonical = reconstruct_svd_polar(
        mmn_path, eigenvalues_path, basis_path
    )
    directions = {
        name: np.asarray(spec["unit_direction"], dtype=float)
        for name, spec in contract["pairs"].items()
    }
    signed, sign_result = choose_signs(
        matrices, contract["pairs"], directions
    )

    probe_payload = json.loads(
        Path(symmetry_probe_path).read_text(encoding="utf-8")
    )
    linear_projector, quadratic_projector, projector_diagnostics = (
        invariant_projectors(probe_payload, canonical)
    )
    linear_basis, linear_eigenvalues = projector_basis(
        linear_projector, 4
    )
    quadratic_basis, quadratic_eigenvalues = projector_basis(
        quadratic_projector, 10
    )
    hermitian = hermitian_basis()
    tensors = quadratic_tensor_basis()

    modes: dict[str, Any] = {}
    p8_values: list[float] = []
    p7_values: list[float] = []
    for mode in ("coarse", "fine", "richardson"):
        coefficients = extract_radius_coefficients(
            signed, contract["pairs"], mode
        )
        linear_observations = {
            name: record["linear"]
            for name, record in coefficients.items()
        }
        quadratic_observations = {
            name: record["quadratic"]
            for name, record in coefficients.items()
        }
        complete_linear = fit_invariant_basis(
            linear_basis,
            linear_observations,
            directions,
            lambda coefficient, direction: evaluate_linear(
                coefficient, direction, hermitian
            ),
        )
        complete_quadratic = fit_invariant_basis(
            quadratic_basis,
            quadratic_observations,
            directions,
            lambda coefficient, direction: evaluate_quadratic(
                coefficient, direction, tensors, hermitian
            ),
        )
        two_p = fit_conventional(
            linear_observations,
            directions,
            ("p8", "p7"),
            "linear",
        )
        conventional_quadratic = fit_conventional(
            quadratic_observations,
            directions,
            ("f", "gamma1", "gamma2", "gamma3"),
            "quadratic",
        )
        p8_values.append(float(two_p["parameters"]["p8"]))
        p7_values.append(float(two_p["parameters"]["p7"]))
        modes[mode] = {
            "complete_linear": complete_linear,
            "two_p_linear": two_p,
            "complete_quadratic": complete_quadratic,
            "conventional_quadratic": conventional_quadratic,
        }

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "status": "independent_static_cdte_postprocessing_reproduction",
        "independence_boundary": {
            "same_physical_qe_artifact": True,
            "independent_svd_polar_reconstruction": True,
            "independent_mmn_parser": True,
            "independent_symmetry_projector_from_raw_operations": True,
            "imports_existing_static_postprocessing_modules": False,
            "independent_electronic_structure_calculation": False,
        },
        "source_evidence": {
            "physical_workflow_run": 29640468978,
            "physical_artifact_id": 8428509605,
            "physical_artifact_digest": "sha256:7e34882d03de1d45697586671bb8e77fc260a0993914e4ddafe3ebe1eb61ee4b",
        },
        "input_sha256": {
            "mmn": sha256(mmn_path),
            "nnkp": sha256(nnkp_path),
            "exact_qe_eigenvalues": sha256(eigenvalues_path),
            "canonical_basis_result": sha256(basis_path),
            "raw_symmetry_probe": sha256(symmetry_probe_path),
            "finite_k_contract": sha256(contract_path),
        },
        "kpoint_contract": {
            "training_directions": list(TRAINING),
            "holdout_directions": [HOLDOUT],
            "holdout_used_in_training": False,
            "maximum_cartesian_residual_inverse_angstrom": kpoint_residual,
        },
        "reconstruction": {
            "method": (
                "direct SVD polar factor Q=U V^dagger "
                "for S=U Sigma V^dagger"
            ),
            "minimum_overlap_singular_value": min(
                item["minimum_overlap_singular_value"]
                for item in reconstruction
            ),
            "maximum_selected_eigenvalue_absolute_error_ev": max(
                item["maximum_selected_eigenvalue_absolute_error_ev"]
                for item in reconstruction
            ),
            "maximum_polar_unitarity_residual": max(
                item["polar_unitarity_residual"]
                for item in reconstruction
            ),
        },
        "sign_convention": sign_result,
        "invariant_spaces": {
            "linear_dimension": int(linear_basis.shape[1]),
            "quadratic_dimension": int(quadratic_basis.shape[1]),
            "linear_selected_projector_eigenvalues": (
                linear_eigenvalues.tolist()
            ),
            "quadratic_selected_projector_eigenvalues": (
                quadratic_eigenvalues.tolist()
            ),
            "projector_diagnostics": projector_diagnostics,
        },
        **modes,
        "radius_stability": {
            "p8_values_ev_angstrom": p8_values,
            "p7_values_ev_angstrom": p7_values,
            "p8_relative_range": relative_range(p8_values),
            "p7_relative_range": relative_range(p7_values),
        },
    }

    if reference_path is not None:
        reference = json.loads(
            Path(reference_path).read_text(encoding="utf-8")
        )
        result["reference_comparison"] = compare_reference(
            result, reference
        )
        result["input_sha256"][
            "controlling_reference_comparison_only"
        ] = sha256(reference_path)

    richardson = result["richardson"]
    reference_comparison = result.get("reference_comparison", {})
    gates = {
        "selected_eigenvalue_error": result["reconstruction"][
            "maximum_selected_eigenvalue_absolute_error_ev"
        ]
        <= 1.0e-6,
        "minimum_overlap": result["reconstruction"][
            "minimum_overlap_singular_value"
        ]
        >= 0.99,
        "linear_dimension": (
            result["invariant_spaces"]["linear_dimension"] == 4
        ),
        "quadratic_dimension": (
            result["invariant_spaces"]["quadratic_dimension"] == 10
        ),
        "complete_linear_training": richardson["complete_linear"][
            "training_relative_residual"
        ]
        <= 1.0e-5,
        "complete_linear_holdout": richardson["complete_linear"][
            "direction_relative_residuals"
        ][HOLDOUT]
        <= 1.0e-5,
        "complete_quadratic_training": richardson[
            "complete_quadratic"
        ]["training_relative_residual"]
        <= 1.0e-3,
        "complete_quadratic_holdout": richardson[
            "complete_quadratic"
        ]["direction_relative_residuals"][HOLDOUT]
        <= 1.0e-3,
        "conventional_quadratic_training_failure": richardson[
            "conventional_quadratic"
        ]["training_relative_residual"]
        >= 0.20,
        "conventional_quadratic_holdout_failure": richardson[
            "conventional_quadratic"
        ]["direction_relative_residuals"][HOLDOUT]
        >= 0.20,
        "p8_radius_stability": (
            result["radius_stability"]["p8_relative_range"] <= 0.05
        ),
        "p7_radius_stability": (
            result["radius_stability"]["p7_relative_range"] <= 0.05
        ),
        "holdout_not_trained": not result["kpoint_contract"][
            "holdout_used_in_training"
        ],
    }
    if reference_comparison:
        gates["reference_scalar_agreement"] = (
            max(reference_comparison.values()) <= 1.0e-9
        )
    passed = all(gates.values())
    result["decision"] = {
        "gates": gates,
        "passed": passed,
        "selected_band_method_reproduced": passed,
        "complete_linear_space_reproduced": passed,
        "complete_quadratic_space_reproduced": passed,
        "conventional_quadratic_failure_reproduced": passed,
        "additional_electronic_structure_compute_authorized": False,
        "claim_boundary": (
            "A pass independently reproduces the post-processing conclusion on "
            "the same immutable physical artifact. It does not validate PBE, the "
            "pseudopotentials, planning geometry, or convergence and does not "
            "turn the fitted coefficients into reference CdTe parameters."
        ),
    }
    if not passed:
        failed = [name for name, value in gates.items() if not value]
        raise RuntimeError(
            f"independent static CdTe reproduction failed gates: {failed}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmn", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--basis-result", required=True)
    parser.add_argument("--symmetry-probe", required=True)
    parser.add_argument("--finite-k-contract", required=True)
    parser.add_argument("--reference-result")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.symmetry_probe,
        args.finite_k_contract,
        args.reference_result,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
