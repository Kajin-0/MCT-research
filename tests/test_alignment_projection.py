from __future__ import annotations

import numpy as np
import pytest

from mct_research.gauge import (
    GaugeAlignmentError,
    KANE_IRREP_BLOCKS,
    align_basis,
    procrustes_unitary,
    rotate_operator,
)
from mct_research.kane8 import KaneParameters, hamiltonian
from mct_research.projection import OBSERVATION_DIMENSION, fit_parameters
from mct_research.symmetry import (
    forbidden_gamma_coupling_norm,
    gamma_irrep_residual,
    gamma_irrep_symmetrize,
    time_reversal_pair_residual,
    time_reversal_pair_symmetrize,
)


def random_unitary(size: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conjugate(phases))


def representative_k_grid() -> list[tuple[float, float, float]]:
    directions = np.asarray(
        [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ],
        dtype=float,
    )
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    points = [(0.0, 0.0, 0.0)]
    for magnitude in (0.004, 0.009, 0.015):
        points.extend(tuple(magnitude * direction) for direction in directions)
    return points


def test_global_procrustes_recovers_arbitrary_internal_gauge() -> None:
    reference = np.eye(8, dtype=np.complex128)
    gauge = random_unitary(8, seed=4)
    target = reference @ gauge

    rotation, diagnostics = procrustes_unitary(reference, target)
    aligned = target @ rotation

    np.testing.assert_allclose(aligned, reference, atol=2e-14)
    assert diagnostics.minimum_overlap == pytest.approx(1.0, abs=2e-14)
    assert diagnostics.basis_residual < 2e-14


def test_block_alignment_prevents_cross_irrep_rotation() -> None:
    reference = np.eye(8, dtype=np.complex128)
    block_gauge = np.zeros((8, 8), dtype=np.complex128)
    for block, seed in zip(KANE_IRREP_BLOCKS, (1, 2, 3), strict=True):
        indices = np.arange(8)[block]
        block_gauge[np.ix_(indices, indices)] = random_unitary(indices.size, seed)
    target = reference @ block_gauge

    aligned, rotation, diagnostics = align_basis(
        reference, target, blocks=KANE_IRREP_BLOCKS
    )
    np.testing.assert_allclose(aligned, reference, atol=2e-14)
    assert len(diagnostics) == 3
    np.testing.assert_allclose(rotation, block_gauge.conjugate().T, atol=2e-14)


def test_operator_rotation_restores_reference_matrix() -> None:
    rng = np.random.default_rng(9)
    reference = np.eye(8, dtype=np.complex128)
    gauge = random_unitary(8, seed=5)
    target = reference @ gauge
    operator_reference = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    operator_reference = 0.5 * (operator_reference + operator_reference.conjugate().T)
    operator_target = gauge.conjugate().T @ operator_reference @ gauge

    _, rotation, _ = align_basis(reference, target)
    restored = rotate_operator(operator_target, rotation)
    np.testing.assert_allclose(restored, operator_reference, atol=3e-14)


def test_alignment_rejects_nearly_orthogonal_subspaces() -> None:
    reference = np.eye(4, 2, dtype=np.complex128)
    target = np.eye(4, dtype=np.complex128)[:, 2:4]
    with pytest.raises(GaugeAlignmentError):
        procrustes_unitary(reference, target, minimum_singular_value=0.1)


def test_gamma_irrep_projection_removes_forbidden_couplings() -> None:
    rng = np.random.default_rng(11)
    matrix = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    projected = gamma_irrep_symmetrize(matrix)

    assert gamma_irrep_residual(projected) < 1e-14
    assert forbidden_gamma_coupling_norm(projected) == pytest.approx(0.0, abs=1e-15)
    for block in KANE_IRREP_BLOCKS:
        indices = np.arange(8)[block]
        subblock = projected[np.ix_(indices, indices)]
        np.testing.assert_allclose(
            subblock,
            np.trace(subblock) / indices.size * np.eye(indices.size),
            atol=1e-14,
        )


def test_time_reversal_pair_projection_is_idempotent() -> None:
    rng = np.random.default_rng(14)
    matrix_k = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    matrix_minus = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))

    sym_k, sym_minus = time_reversal_pair_symmetrize(matrix_k, matrix_minus)
    assert time_reversal_pair_residual(sym_k, sym_minus) < 2e-14

    sym2_k, sym2_minus = time_reversal_pair_symmetrize(sym_k, sym_minus)
    np.testing.assert_allclose(sym2_k, sym_k, atol=2e-14)
    np.testing.assert_allclose(sym2_minus, sym_minus, atol=2e-14)


def test_covariance_weighting_downweights_corrupted_gamma_point() -> None:
    true = KaneParameters.from_ep(
        ev=0.0,
        eg=-0.303,
        delta=1.08,
        ep=18.8,
        f=0.0,
        gamma1=4.1,
        gamma2=0.5,
        gamma3=1.3,
    )
    k_points = representative_k_grid()
    matrices = [hamiltonian(k, true) for k in k_points]

    corrupted = [matrix.copy() for matrix in matrices]
    corrupted[0][0, 0] += 0.08
    corrupted[0][1, 1] += 0.08

    ordinary, _ = fit_parameters(k_points, corrupted)

    baseline_variance = 1.0e-8
    covariances = [
        baseline_variance * np.eye(OBSERVATION_DIMENSION) for _ in k_points
    ]
    covariances[0] = 1.0e2 * np.eye(OBSERVATION_DIMENSION)
    weighted, diagnostics = fit_parameters(
        k_points, corrupted, covariances=covariances
    )

    assert abs(weighted.eg - true.eg) < abs(ordinary.eg - true.eg)
    assert diagnostics["parameter_covariance"].shape == (8, 8)
    assert diagnostics["degrees_of_freedom"] > 0
    assert all(
        value >= 0.0
        for value in diagnostics["parameter_standard_errors"].values()
    )


def test_covariance_fit_recovers_noiseless_parameters() -> None:
    true = KaneParameters.from_ep(
        eg=-0.2,
        delta=1.0,
        ep=19.0,
        f=-0.1,
        gamma1=4.0,
        gamma2=0.6,
        gamma3=1.2,
    )
    k_points = representative_k_grid()
    matrices = [hamiltonian(k, true) for k in k_points]
    covariances = []
    for index, _ in enumerate(k_points):
        variance = np.linspace(1.0e-8, 3.0e-8, OBSERVATION_DIMENSION)
        variance *= 1.0 + 0.05 * index
        covariances.append(np.diag(variance))

    recovered, diagnostics = fit_parameters(
        k_points, matrices, covariances=covariances
    )
    for name in ("ev", "eg", "delta", "p", "f", "gamma1", "gamma2", "gamma3"):
        assert getattr(recovered, name) == pytest.approx(
            getattr(true, name), rel=3e-11, abs=3e-11
        )
    assert diagnostics["chi_square"] < 1e-14
