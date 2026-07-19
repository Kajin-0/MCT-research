from __future__ import annotations

import json

import numpy as np
import pytest

from mct_research.dataio import (
    COVARIANCE_COORDINATE_SYSTEM,
    MatrixRecord,
    load_matrix_dataset,
    save_matrix_dataset,
)
from mct_research.hermitian import (
    LEGACY_COMPLEX_CARTESIAN_DIMENSION,
    OBSERVATION_DIMENSION,
    hermitian_linear_map,
    hermitian_vector,
    legacy_covariance_to_hermitian,
    matrix_from_hermitian_vector,
)
from tools.validate_hermitian_covariance_schema import analyze


def random_hermitian(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    return 0.5 * (raw + raw.conjugate().T)


def random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    phases = np.where(np.abs(diagonal) > 0.0, diagonal / np.abs(diagonal), 1.0)
    return q @ np.diag(np.conjugate(phases))


def test_reference_validation_passes_declared_gates() -> None:
    result = analyze()
    assert result["schema_version"] == "2.0"
    assert result["covariance_coordinate_system"] == COVARIANCE_COORDINATE_SYSTEM
    assert result["legacy_dimension"] == LEGACY_COMPLEX_CARTESIAN_DIMENSION
    assert result["independent_dimension"] == OBSERVATION_DIMENSION
    assert result["roundtrip_max_abs"] < 1.0e-12
    assert result["frobenius_inner_product_abs_error"] < 1.0e-12
    assert result["unitary_map_orthogonality_frobenius"] < 1.0e-11
    assert result["legacy_identity_covariance_max_abs_error"] < 1.0e-12


def test_hermitian_coordinates_roundtrip_and_preserve_frobenius_metric() -> None:
    rng = np.random.default_rng(6408)
    first = random_hermitian(rng)
    second = random_hermitian(rng)
    first_vector = hermitian_vector(first)
    second_vector = hermitian_vector(second)

    np.testing.assert_allclose(matrix_from_hermitian_vector(first_vector), first)
    assert first_vector.shape == (64,)
    expected = float(np.trace(first.conjugate().T @ second).real)
    assert float(first_vector @ second_vector) == pytest.approx(expected, abs=1.0e-12)


def test_unitary_conjugation_is_orthogonal_in_64d_coordinates() -> None:
    rng = np.random.default_rng(771)
    unitary = random_unitary(rng)
    mapping = hermitian_linear_map(
        lambda matrix: unitary.conjugate().T @ matrix @ unitary
    )
    np.testing.assert_allclose(mapping.T @ mapping, np.eye(64), atol=2.0e-12)


def test_nonhermitian_matrix_is_rejected_by_hvec_and_covariance_record() -> None:
    matrix = np.eye(8, dtype=complex)
    matrix[0, 1] = 1.0j
    with pytest.raises(ValueError, match="must be Hermitian"):
        hermitian_vector(matrix)
    with pytest.raises(ValueError, match="covariance requires a Hermitian"):
        MatrixRecord(
            composition=0.0,
            temperature_k=0.0,
            volume_a3=1.0,
            k_inv_a=(0.0, 0.0, 0.0),
            matrix_kind="self_energy_total",
            matrix=matrix,
            covariance=np.eye(64),
        )


def test_legacy_identity_covariance_projects_to_identity_in_hvec() -> None:
    migrated = legacy_covariance_to_hermitian(np.eye(128))
    np.testing.assert_allclose(migrated, np.eye(64), atol=1.0e-14)


def test_schema1_archive_is_explicitly_migrated_to_schema2(tmp_path) -> None:
    matrix = np.diag(np.arange(8, dtype=float)).astype(np.complex128)
    legacy = tmp_path / "legacy-v1.npz"
    np.savez_compressed(
        legacy,
        schema_version=np.asarray("1.0"),
        provenance_json=np.asarray(json.dumps({"generator": "legacy-unit-test"})),
        composition=np.asarray([0.0]),
        temperature_k=np.asarray([77.0]),
        volume_a3=np.asarray([68.0]),
        k_inv_a=np.asarray([[0.0, 0.0, 0.0]]),
        matrix_kind=np.asarray(["hamiltonian"]),
        frequency_ev=np.asarray([np.nan]),
        matrix_real=matrix.real[None, :, :],
        matrix_imag=matrix.imag[None, :, :],
        basis_overlap_present=np.asarray([False]),
        basis_overlap_real=np.zeros((1, 8, 8)),
        basis_overlap_imag=np.zeros((1, 8, 8)),
        covariance_present=np.asarray([True]),
        covariance=np.eye(128)[None, :, :],
        metadata_json=np.asarray(["{}"]),
    )

    dataset = load_matrix_dataset(legacy)
    assert dataset.schema_version == "2.0"
    assert dataset.records[0].covariance is not None
    assert dataset.records[0].covariance.shape == (64, 64)
    assert dataset.records[0].metadata["covariance_schema_migration"]["to"] == (
        COVARIANCE_COORDINATE_SYSTEM
    )
    assert dataset.provenance["schema_migrations"][0]["from_schema"] == "1.0"

    rewritten = tmp_path / "schema-v2.npz"
    save_matrix_dataset(rewritten, dataset)
    with np.load(rewritten, allow_pickle=False) as payload:
        assert str(payload["schema_version"].item()) == "2.0"
        assert str(payload["covariance_coordinate_system"].item()) == (
            COVARIANCE_COORDINATE_SYSTEM
        )
        assert payload["covariance"].shape == (1, 64, 64)
