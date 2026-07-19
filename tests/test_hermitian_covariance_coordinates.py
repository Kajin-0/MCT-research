from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.code_exports import ExportDefaults, dataset_from_arrays
from mct_research.dataio import (
    LEGACY_SCHEMA_VERSION,
    SCHEMA_VERSION,
    MatrixDataset,
    MatrixRecord,
    load_matrix_dataset,
    save_matrix_dataset,
)
from mct_research.kane8 import KaneParameters, hamiltonian
from mct_research.matrix_coordinates import (
    COMPLEX_OBSERVATION_DIMENSION,
    HERMITIAN_OBSERVATION_DIMENSION,
    hermitian_covariance_to_legacy,
    hermitian_embedding,
    hermitian_matrix,
    hermitian_real_linear_map,
    hermitian_vector,
    legacy_covariance_to_hermitian,
)
from mct_research.pipeline import project_covariance, rotate_covariance
from mct_research.projection import covariance_whitener, fit_parameters
from mct_research.symmetry import gamma_irrep_symmetrize


def random_hermitian(seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    return 0.5 * (raw + raw.conj().T)


def random_psd(dimension: int, seed: int = 11) -> np.ndarray:
    rng = np.random.default_rng(seed)
    factor = rng.normal(size=(dimension, dimension))
    return factor @ factor.T + 0.5 * np.eye(dimension)


def random_unitary(seed: int = 13) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conj(phases))


def test_hermitian_coordinates_round_trip_and_preserve_frobenius_norm() -> None:
    matrix = random_hermitian()
    coordinates = hermitian_vector(matrix)
    assert coordinates.shape == (HERMITIAN_OBSERVATION_DIMENSION,)
    np.testing.assert_allclose(hermitian_matrix(coordinates), matrix, atol=1e-13)
    assert np.linalg.norm(coordinates) == pytest.approx(
        np.linalg.norm(matrix, ord="fro"), abs=1e-13
    )


def test_hermitian_embedding_is_orthonormal_and_covariance_round_trips() -> None:
    embedding = hermitian_embedding()
    assert embedding.shape == (
        COMPLEX_OBSERVATION_DIMENSION,
        HERMITIAN_OBSERVATION_DIMENSION,
    )
    np.testing.assert_allclose(
        embedding.T @ embedding,
        np.eye(HERMITIAN_OBSERVATION_DIMENSION),
        atol=1e-13,
    )
    covariance_64 = random_psd(HERMITIAN_OBSERVATION_DIMENSION)
    covariance_128 = hermitian_covariance_to_legacy(covariance_64)
    assert np.linalg.matrix_rank(covariance_128, tol=1e-10) == 64
    np.testing.assert_allclose(
        legacy_covariance_to_hermitian(covariance_128),
        covariance_64,
        atol=1e-10,
    )


def test_unitary_rotation_is_orthogonal_in_hermitian_coordinates() -> None:
    unitary = random_unitary()
    mapping = hermitian_real_linear_map(
        lambda matrix: unitary.conj().T @ matrix @ unitary
    )
    np.testing.assert_allclose(
        mapping.T @ mapping,
        np.eye(HERMITIAN_OBSERVATION_DIMENSION),
        atol=1e-12,
    )
    covariance = random_psd(HERMITIAN_OBSERVATION_DIMENSION)
    rotated = rotate_covariance(covariance, unitary)
    np.testing.assert_allclose(rotated, mapping @ covariance @ mapping.T, atol=1e-10)
    np.testing.assert_allclose(rotated, rotated.T, atol=1e-13)


def test_symmetry_projection_preserves_psd_in_64d() -> None:
    covariance = random_psd(HERMITIAN_OBSERVATION_DIMENSION)
    projected = project_covariance(covariance, gamma_irrep_symmetrize)
    np.testing.assert_allclose(projected, projected.T, atol=1e-13)
    assert np.min(np.linalg.eigvalsh(projected)) >= -1e-9


def test_projection_uses_64_observations_per_matrix() -> None:
    parameters = KaneParameters(
        ev=-0.04,
        eg=0.18,
        delta=0.95,
        p=7.2,
        f=0.12,
        gamma1=3.4,
        gamma2=1.1,
        gamma3=1.5,
    )
    k_points = [
        (0.0, 0.0, 0.0),
        (0.008, 0.0, 0.0),
        (0.0, 0.009, 0.0),
        (0.0, 0.0, 0.010),
        (0.007, 0.006, 0.0),
        (0.006, 0.005, 0.004),
    ]
    matrices = [hamiltonian(k, parameters) for k in k_points]
    fitted, diagnostics = fit_parameters(k_points, matrices)
    assert fitted == pytest.approx(parameters, abs=1e-10)
    assert diagnostics["observation_count"] == 64 * len(k_points)
    assert diagnostics["coordinate_dimension_per_matrix"] == 64
    assert diagnostics["coordinate_system"] == "orthonormal_hermitian_64"
    assert diagnostics["degrees_of_freedom"] == 64 * len(k_points) - 8


def test_covariance_whitener_rejects_legacy_dimension() -> None:
    with pytest.raises(ValueError, match="64, 64"):
        covariance_whitener(np.eye(COMPLEX_OBSERVATION_DIMENSION))


def _legacy_npz(path: Path, covariance_128: np.ndarray) -> None:
    matrix = random_hermitian(17)
    np.savez_compressed(
        path,
        schema_version=np.asarray(LEGACY_SCHEMA_VERSION),
        provenance_json=np.asarray(json.dumps({"source": "legacy-test"})),
        composition=np.asarray([0.25]),
        temperature_k=np.asarray([77.0]),
        volume_a3=np.asarray([68.0]),
        k_inv_a=np.asarray([[0.0, 0.0, 0.0]]),
        matrix_kind=np.asarray(["hamiltonian"]),
        frequency_ev=np.asarray([np.nan]),
        matrix_real=np.asarray([matrix.real]),
        matrix_imag=np.asarray([matrix.imag]),
        basis_overlap_present=np.asarray([False]),
        basis_overlap_real=np.zeros((1, 8, 8)),
        basis_overlap_imag=np.zeros((1, 8, 8)),
        covariance_present=np.asarray([True]),
        covariance=np.asarray([covariance_128]),
        metadata_json=np.asarray([json.dumps({"legacy": True})]),
    )


def test_schema_v1_hamiltonian_covariance_migrates_to_64d(tmp_path: Path) -> None:
    covariance_64 = random_psd(HERMITIAN_OBSERVATION_DIMENSION, 19)
    path = tmp_path / "legacy.npz"
    _legacy_npz(path, hermitian_covariance_to_legacy(covariance_64))
    dataset = load_matrix_dataset(path)
    assert dataset.schema_version == SCHEMA_VERSION
    assert dataset.records[0].covariance is not None
    assert dataset.records[0].covariance.shape == (64, 64)
    np.testing.assert_allclose(dataset.records[0].covariance, covariance_64, atol=1e-9)
    assert dataset.provenance["schema_migration"]["from"] == "1.0"


def test_schema_v2_round_trip_supports_64d_and_128d(tmp_path: Path) -> None:
    hermitian = random_hermitian(23)
    general = hermitian + 0.02j * np.eye(8)
    records = (
        MatrixRecord(
            composition=0.25,
            temperature_k=77.0,
            volume_a3=68.0,
            k_inv_a=(0.0, 0.0, 0.0),
            matrix_kind="hamiltonian",
            matrix=hermitian,
            covariance=random_psd(64, 29),
        ),
        MatrixRecord(
            composition=0.25,
            temperature_k=77.0,
            volume_a3=68.0,
            k_inv_a=(0.0, 0.0, 0.0),
            matrix_kind="self_energy_total",
            matrix=general,
            frequency_ev=0.1,
            covariance=random_psd(128, 31),
        ),
    )
    path = tmp_path / "v2.npz"
    save_matrix_dataset(path, MatrixDataset(records=records, provenance={"test": True}))
    loaded = load_matrix_dataset(path)
    assert loaded.schema_version == "2.0"
    assert loaded.records[0].covariance.shape == (64, 64)
    assert loaded.records[1].covariance.shape == (128, 128)
    np.testing.assert_allclose(loaded.records[0].covariance, records[0].covariance)
    np.testing.assert_allclose(loaded.records[1].covariance, records[1].covariance)


def test_external_legacy_hamiltonian_covariance_converts_to_64d() -> None:
    matrix = random_hermitian(37)
    covariance_64 = random_psd(64, 41)
    dataset = dataset_from_arrays(
        matrices=matrix,
        k_inv_a=(0.0, 0.0, 0.0),
        defaults=ExportDefaults(
            composition=0.25,
            temperature_k=77.0,
            volume_a3=68.0,
            matrix_kind="hamiltonian",
        ),
        provenance={"format": "legacy-128"},
        covariances=hermitian_covariance_to_legacy(covariance_64),
    )
    assert dataset.records[0].covariance.shape == (64, 64)
    np.testing.assert_allclose(dataset.records[0].covariance, covariance_64, atol=1e-9)


def test_64d_covariance_rejects_nonhermitian_operator() -> None:
    matrix = random_hermitian(43) + 0.01j * np.eye(8)
    with pytest.raises(ValueError, match="64D covariance requires a Hermitian matrix"):
        MatrixRecord(
            composition=0.25,
            temperature_k=77.0,
            volume_a3=68.0,
            k_inv_a=(0.0, 0.0, 0.0),
            matrix_kind="self_energy_total",
            matrix=matrix,
            frequency_ev=0.1,
            covariance=np.eye(64),
        )
