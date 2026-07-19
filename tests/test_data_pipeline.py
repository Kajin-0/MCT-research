from __future__ import annotations

import numpy as np
import pytest

from mct_research.dataio import (
    MatrixDataset,
    MatrixRecord,
    file_sha256,
    load_matrix_dataset,
    save_matrix_dataset,
)
from mct_research.hermitian import OBSERVATION_DIMENSION
from mct_research.kane8 import KaneParameters, hamiltonian
from mct_research.pipeline import process_record, rotate_covariance
from mct_research.projection import PARAMETER_NAMES, fit_parameters


def random_unitary(size: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(size, size)) + 1j * rng.normal(size=(size, size))
    q, r = np.linalg.qr(matrix)
    diagonal = np.diag(r)
    phases = np.where(np.abs(diagonal) > 0.0, diagonal / np.abs(diagonal), 1.0)
    return q @ np.diag(np.conjugate(phases))


def block_unitary(rng: np.random.Generator) -> np.ndarray:
    result = np.zeros((8, 8), dtype=np.complex128)
    for start, stop in ((0, 2), (2, 6), (6, 8)):
        result[start:stop, start:stop] = random_unitary(stop - start, rng)
    return result


def k_grid() -> list[tuple[float, float, float]]:
    scale = 0.01
    rt2 = np.sqrt(2.0)
    rt3 = np.sqrt(3.0)
    return [
        (0.0, 0.0, 0.0),
        (scale, 0.0, 0.0),
        (0.0, scale, 0.0),
        (0.0, 0.0, scale),
        (scale / rt2, scale / rt2, 0.0),
        (scale / rt2, 0.0, scale / rt2),
        (0.0, scale / rt2, scale / rt2),
        (scale / rt3, scale / rt3, scale / rt3),
    ]


def test_dataset_roundtrip_and_integrity(tmp_path) -> None:
    record = MatrixRecord(
        composition=0.0,
        temperature_k=77.0,
        volume_a3=68.0,
        k_inv_a=(0.0, 0.0, 0.0),
        matrix_kind="hamiltonian",
        matrix=np.diag(np.arange(8, dtype=float)).astype(np.complex128),
        frequency_ev=None,
        basis_overlap=np.eye(8, dtype=np.complex128),
        covariance=1.0e-8 * np.eye(OBSERVATION_DIMENSION),
        metadata={"code": "synthetic", "replicate": 1},
    )
    dataset = MatrixDataset(
        records=(record,),
        provenance={"generator": "unit-test", "commit": "abc123"},
    )
    path = tmp_path / "matrices.npz"
    digest = save_matrix_dataset(path, dataset)

    assert digest == file_sha256(path)
    loaded = load_matrix_dataset(path, expected_sha256=digest)
    assert loaded.provenance == dataset.provenance
    assert loaded.records[0].metadata == record.metadata
    np.testing.assert_allclose(loaded.records[0].matrix, record.matrix)
    np.testing.assert_allclose(loaded.records[0].covariance, record.covariance)

    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_matrix_dataset(path, expected_sha256="0" * 64)


def test_unitary_covariance_rotation_preserves_total_variance() -> None:
    rng = np.random.default_rng(22)
    rotation = random_unitary(8, rng)
    diagonal = np.linspace(1.0e-8, 4.0e-8, OBSERVATION_DIMENSION)
    covariance = np.diag(diagonal)
    transformed = rotate_covariance(covariance, rotation)

    assert np.trace(transformed) == pytest.approx(np.trace(covariance), rel=2e-12)
    assert np.min(np.linalg.eigvalsh(transformed)) > -1e-18


def test_end_to_end_random_gauge_symmetry_and_gls_recovery() -> None:
    rng = np.random.default_rng(31)
    true = KaneParameters.from_ep(
        ev=0.01,
        eg=-0.285,
        delta=1.04,
        ep=18.6,
        f=-0.05,
        gamma1=4.2,
        gamma2=0.55,
        gamma3=1.25,
    )

    raw_records = []
    for index, k in enumerate(k_grid()):
        physical = hamiltonian(k, true)
        gauge = block_unitary(rng) if index == 0 else random_unitary(8, rng)

        if index == 0:
            physical = physical.copy()
            physical[0, 2] += 2.0e-4
            physical[2, 0] += 2.0e-4

        raw = gauge.conjugate().T @ physical @ gauge
        overlap = gauge.conjugate().T
        covariance = (1.0e-10 * (1.0 + 0.1 * index)) * np.eye(
            OBSERVATION_DIMENSION
        )
        raw_records.append(
            MatrixRecord(
                composition=0.0,
                temperature_k=77.0,
                volume_a3=68.0,
                k_inv_a=k,
                matrix_kind="quasiparticle_hamiltonian",
                matrix=raw,
                basis_overlap=overlap,
                covariance=covariance,
                metadata={"synthetic_index": index},
            )
        )

    processed = [process_record(record) for record in raw_records]
    records = [item[0] for item in processed]
    diagnostics = [item[1] for item in processed]

    assert diagnostics[0].symmetry_residual_before is not None
    assert diagnostics[0].symmetry_residual_before > 1.0e-5
    assert all(
        block.minimum_overlap == pytest.approx(1.0, abs=3e-13)
        for diagnostic in diagnostics
        for block in diagnostic.gauge
    )

    recovered, fit_diagnostics = fit_parameters(
        [record.k_inv_a for record in records],
        [record.matrix for record in records],
        covariances=[record.covariance for record in records],
    )
    standard_errors = fit_diagnostics["parameter_standard_errors"]
    for name in PARAMETER_NAMES:
        error = abs(getattr(recovered, name) - getattr(true, name))
        assert error < 5.0e-8
        assert error < 0.01 * standard_errors[name]
    assert fit_diagnostics["relative_residual"] < 1e-8
    assert fit_diagnostics["rank"] == 8.0
    assert fit_diagnostics["observation_count"] == len(k_grid()) * 64
    assert fit_diagnostics["observation_coordinate_system"] == (
        "hermitian_frobenius_64"
    )
