"""Deterministic Weiler quadratic-class templates in the fixed Novik basis."""
from __future__ import annotations

import math
from typing import Any

import numpy as np

from cdte_quadratic_invariant_space import (
    _conventional_span,
    _orthonormalize,
)

CLASS_SPECS: tuple[tuple[str, str, str], ...] = (
    ("F", "66", "A1"),
    ("N2", "68", "E"),
    ("G", "68", "T2"),
    ("G_prime", "67", "T2"),
    ("gamma1", "88", "A1"),
    ("gamma2", "88", "E"),
    ("gamma3", "88", "T2"),
    ("gamma2_prime", "87", "E"),
    ("gamma3_prime", "87", "T2"),
    ("gamma1_prime", "77", "A1"),
)
CLASS_NAMES = tuple(item[0] for item in CLASS_SPECS)


def tensor_irrep_bases() -> dict[str, np.ndarray]:
    """Return orthonormal A1, E, and T2 bases in the six k_i k_j tensors.

    Tensor coefficient order is ``xx, yy, zz, yz, zx, xy`` with the three
    off-diagonal tensor matrices normalized by ``1/sqrt(2)``.
    """
    a1 = np.asarray([[1.0, 1.0, 1.0, 0.0, 0.0, 0.0]]).T / math.sqrt(3.0)
    e = np.column_stack(
        (
            np.asarray([-1.0, -1.0, 2.0, 0.0, 0.0, 0.0]) / math.sqrt(6.0),
            np.asarray([1.0, -1.0, 0.0, 0.0, 0.0, 0.0]) / math.sqrt(2.0),
        )
    )
    t2 = np.eye(6)[:, 3:]
    return {"A1": a1, "E": e, "T2": t2}


def _class_basis(
    projector: np.ndarray,
    hermitian_sectors: list[str],
    sector: str,
    tensor_irrep: str,
) -> np.ndarray:
    tensor_basis = tensor_irrep_bases()[tensor_irrep]
    matrix_indices = [
        index for index, matrix_sector in enumerate(hermitian_sectors)
        if matrix_sector == sector
    ]
    candidates = []
    for tensor_vector in tensor_basis.T:
        for matrix_index in matrix_indices:
            matrix_vector = np.zeros(64)
            matrix_vector[matrix_index] = 1.0
            candidates.append(projector @ np.kron(tensor_vector, matrix_vector))
    basis = _orthonormalize(candidates)
    if basis.shape != (384, 1):
        raise RuntimeError(
            f"expected one invariant for {sector}/{tensor_irrep}, got {basis.shape[1]}"
        )
    return basis


def build_weiler_class_basis(
    projector: np.ndarray, hermitian_sectors: list[str]
) -> tuple[np.ndarray, dict[str, Any]]:
    columns = [
        _class_basis(projector, hermitian_sectors, sector, tensor_irrep)[:, 0]
        for _, sector, tensor_irrep in CLASS_SPECS
    ]
    basis = np.column_stack(columns)
    diagnostics = {
        "class_names": list(CLASS_NAMES),
        "class_specs": [
            {"name": name, "sector": sector, "tensor_irrep": tensor_irrep}
            for name, sector, tensor_irrep in CLASS_SPECS
        ],
        "gram_residual": float(np.linalg.norm(basis.T @ basis - np.eye(10))),
        "projector_residual": float(np.linalg.norm(basis @ basis.T - projector)),
    }
    return basis, diagnostics


def expected_conventional_unit_directions() -> np.ndarray:
    """Expected normalized f/gamma directions in repository class convention."""
    expected = np.zeros((10, 4))
    expected[0, 0] = 1.0
    expected[4, 1] = -math.sqrt(2.0 / 3.0)
    expected[9, 1] = -1.0 / math.sqrt(3.0)
    expected[5, 2] = -1.0 / math.sqrt(3.0)
    expected[7, 2] = -math.sqrt(2.0 / 3.0)
    expected[6, 3] = 1.0 / math.sqrt(3.0)
    expected[8, 3] = -math.sqrt(2.0 / 3.0)
    return expected


def conventional_relation_diagnostics(
    tensors: list[np.ndarray],
    hermitian_basis: list[np.ndarray],
    class_basis: np.ndarray,
) -> dict[str, Any]:
    raw, _ = _conventional_span(tensors, hermitian_basis)
    norms = np.linalg.norm(raw, axis=0)
    coordinates = class_basis.T @ raw
    normalized = coordinates / norms
    expected = expected_conventional_unit_directions()
    return {
        "template_names": ["f", "gamma1", "gamma2", "gamma3"],
        "raw_template_norms_ev_angstrom2_per_unit_parameter": norms.tolist(),
        "class_coordinates_ev_angstrom2_per_unit_parameter": coordinates.tolist(),
        "normalized_class_directions": normalized.tolist(),
        "expected_normalized_class_directions": expected.tolist(),
        "normalized_relation_residual": float(np.linalg.norm(normalized - expected)),
        "relations_in_repository_class_normalization": {
            "f": "+F",
            "gamma1": "-sqrt(2/3)*gamma1 - 1/sqrt(3)*gamma1_prime",
            "gamma2": "-1/sqrt(3)*gamma2 - sqrt(2/3)*gamma2_prime",
            "gamma3": "+1/sqrt(3)*gamma3 - sqrt(2/3)*gamma3_prime",
        },
    }


def conventional_tied_and_departure_coordinates(
    named_coordinates: dict[str, float]
) -> dict[str, Any]:
    g1 = np.asarray([named_coordinates["gamma1"], named_coordinates["gamma1_prime"]])
    g2 = np.asarray([named_coordinates["gamma2"], named_coordinates["gamma2_prime"]])
    g3 = np.asarray([named_coordinates["gamma3"], named_coordinates["gamma3_prime"]])
    tied = {
        "gamma1": np.asarray([-math.sqrt(2.0 / 3.0), -1.0 / math.sqrt(3.0)]),
        "gamma2": np.asarray([-1.0 / math.sqrt(3.0), -math.sqrt(2.0 / 3.0)]),
        "gamma3": np.asarray([1.0 / math.sqrt(3.0), -math.sqrt(2.0 / 3.0)]),
    }
    departure = {
        "gamma1": np.asarray([1.0 / math.sqrt(3.0), -math.sqrt(2.0 / 3.0)]),
        "gamma2": np.asarray([math.sqrt(2.0 / 3.0), -1.0 / math.sqrt(3.0)]),
        "gamma3": np.asarray([math.sqrt(2.0 / 3.0), 1.0 / math.sqrt(3.0)]),
    }
    pairs = {"gamma1": g1, "gamma2": g2, "gamma3": g3}
    return {
        "omitted_conduction_valence_class_coordinates_ev_angstrom2": {
            name: float(named_coordinates[name]) for name in ("N2", "G", "G_prime")
        },
        "tied_gamma_subspace_coordinates_ev_angstrom2": {
            name: float(tied[name] @ pairs[name]) for name in pairs
        },
        "untied_gamma_departure_coordinates_ev_angstrom2": {
            name: float(departure[name] @ pairs[name]) for name in pairs
        },
    }
