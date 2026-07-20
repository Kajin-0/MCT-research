from __future__ import annotations

import ast
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.reproduce_cdte_static_independent import (  # noqa: E402
    canonical_columns,
    parse_mmn,
    projector_basis,
    real_vector,
)

TOOL = ROOT / "tools/reproduce_cdte_static_independent.py"
FORBIDDEN_IMPORTS = {
    "cdte_finite_k_projection",
    "cdte_quadratic_invariant_space",
    "cdte_weiler_class_templates",
    "analyze_cdte_corrected_static",
}


def random_unitary(seed: int, size: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    unitary, diagonal = np.linalg.qr(raw)
    phases = np.diag(diagonal) / np.maximum(np.abs(np.diag(diagonal)), 1e-15)
    return unitary @ np.diag(phases.conj())


def metric_polar(overlap: np.ndarray) -> np.ndarray:
    metric = overlap @ overlap.conj().T
    values, vectors = np.linalg.eigh(metric)
    inverse_sqrt = (vectors * (1.0 / np.sqrt(values))) @ vectors.conj().T
    return inverse_sqrt @ overlap


def svd_polar(overlap: np.ndarray) -> np.ndarray:
    left, _, right_h = np.linalg.svd(overlap, full_matrices=False)
    return left @ right_h


def test_direct_svd_polar_matches_independent_metric_formula() -> None:
    left = random_unitary(20260720, 8)
    right = random_unitary(20260721, 8)
    singular = np.linspace(0.991, 1.009, 8)
    overlap = left @ np.diag(singular) @ right.conj().T
    assert np.linalg.norm(svd_polar(overlap) - metric_polar(overlap)) < 1e-12


def test_svd_reconstruction_is_phase_and_permutation_invariant() -> None:
    overlap = random_unitary(31, 8) @ np.diag(np.linspace(0.995, 1.004, 8))
    energies = np.asarray([-2.0, -1.2, -0.5, 0.1, 0.4, 0.9, 1.4, 2.0])

    polar = svd_polar(overlap)
    reference = polar @ np.diag(energies) @ polar.conj().T

    phases = np.exp(1j * np.linspace(0.13, 1.97, 8))
    phased = overlap @ np.diag(phases)
    phased_polar = svd_polar(phased)
    phased_result = phased_polar @ np.diag(energies) @ phased_polar.conj().T
    assert np.linalg.norm(reference - phased_result) < 1e-12

    permutation = np.asarray([3, 0, 7, 2, 5, 1, 6, 4])
    permuted = overlap[:, permutation]
    permuted_polar = svd_polar(permuted)
    permuted_result = (
        permuted_polar
        @ np.diag(energies[permutation])
        @ permuted_polar.conj().T
    )
    assert np.linalg.norm(reference - permuted_result) < 1e-12


def test_mmn_parser_preserves_wannier_n_outer_m_inner_order(tmp_path: Path) -> None:
    path = tmp_path / "tiny.mmn"
    path.write_text(
        "test\n"
        "2 1 1\n"
        "1 1 0 0 0\n"
        "1 0\n"
        "2 0\n"
        "3 0\n"
        "4 0\n",
        encoding="utf-8",
    )
    nbnd, nk, nntot, blocks = parse_mmn(path)
    assert (nbnd, nk, nntot) == (2, 1, 1)
    assert blocks[0][0:3] == (1, 1, (0, 0, 0))
    assert np.array_equal(blocks[0][3], np.asarray([[1, 3], [2, 4]], complex))


def test_canonical_columns_reorders_probe_blocks() -> None:
    identity2 = np.stack((np.eye(2), np.zeros((2, 2))), axis=-1).tolist()
    identity4 = np.stack((np.eye(4), np.zeros((4, 4))), axis=-1).tolist()
    payload = {
        "selected_global_bands_one_based": list(range(31, 39)),
        "irreps": {
            "Gamma7": {
                "probe_block_index": 0,
                "bands_one_based": [31, 32],
                "intertwiner": identity2,
            },
            "Gamma8": {
                "probe_block_index": 1,
                "bands_one_based": [33, 34, 35, 36],
                "intertwiner": identity4,
            },
            "Gamma6": {
                "probe_block_index": 2,
                "bands_one_based": [37, 38],
                "intertwiner": identity2,
            },
        },
    }
    columns = canonical_columns(payload)
    expected_order = [6, 7, 2, 3, 4, 5, 0, 1]
    assert np.array_equal(columns, np.eye(8)[:, expected_order])


def test_projector_basis_uses_only_unit_eigenspace() -> None:
    rotation = random_unitary(91, 6).real
    rotation, _ = np.linalg.qr(rotation)
    projector = rotation[:, :3] @ rotation[:, :3].T
    basis, values = projector_basis(projector, 3)
    assert np.linalg.norm(basis.T @ basis - np.eye(3)) < 1e-12
    assert np.allclose(values, 1.0, atol=1e-12)
    assert np.linalg.norm(projector @ basis - basis) < 1e-12


def test_independent_tool_does_not_import_existing_static_analysis_modules() -> None:
    tree = ast.parse(TOOL.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[-1] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[-1])
    assert imported.isdisjoint(FORBIDDEN_IMPORTS)


def test_real_vector_preserves_frobenius_norm() -> None:
    matrix = np.asarray([[1 + 2j, 3 - 4j], [5 + 0.5j, -2j]])
    assert math.isclose(
        np.linalg.norm(real_vector(matrix)),
        np.linalg.norm(matrix),
        rel_tol=0.0,
        abs_tol=1e-14,
    )
