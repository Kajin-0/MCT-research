"""Versioned, integrity-checked storage for projected electronic matrices."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import numpy as np
from numpy.typing import NDArray

from .matrix_coordinates import (
    COMPLEX_OBSERVATION_DIMENSION,
    HERMITIAN_OBSERVATION_DIMENSION,
    hermitian_residual,
    legacy_covariance_to_hermitian,
)

OBSERVATION_DIMENSION = HERMITIAN_OBSERVATION_DIMENSION
MAX_COVARIANCE_DIMENSION = COMPLEX_OBSERVATION_DIMENSION
SCHEMA_VERSION = "2.0"
LEGACY_SCHEMA_VERSION = "1.0"
HAMILTONIAN_MATRIX_KINDS = {"hamiltonian", "quasiparticle_hamiltonian"}
_ALLOWED_KINDS = HAMILTONIAN_MATRIX_KINDS | {
    "self_energy_fan",
    "self_energy_dw",
    "self_energy_total",
}

ComplexMatrix = NDArray[np.complex128]
RealMatrix = NDArray[np.float64]


def _json_text(value: Any, *, name: str) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be JSON serializable") from exc


def _complex_matrix(value: ComplexMatrix, *, name: str) -> ComplexMatrix:
    array = np.asarray(value, dtype=np.complex128)
    if array.shape != (8, 8):
        raise ValueError(f"{name} must have shape (8, 8), got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains non-finite values")
    return array.copy()


def _covariance(value: RealMatrix, *, name: str) -> RealMatrix:
    array = np.asarray(value, dtype=float)
    allowed = {
        (HERMITIAN_OBSERVATION_DIMENSION, HERMITIAN_OBSERVATION_DIMENSION),
        (COMPLEX_OBSERVATION_DIMENSION, COMPLEX_OBSERVATION_DIMENSION),
    }
    if array.shape not in allowed:
        raise ValueError(
            f"{name} must have shape (64, 64) or (128, 128), got {array.shape}"
        )
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains non-finite values")
    symmetric = 0.5 * (array + array.T)
    scale = max(np.linalg.norm(symmetric, ord="fro"), np.finfo(float).eps)
    if np.linalg.norm(array - array.T, ord="fro") / scale > 1.0e-10:
        raise ValueError(f"{name} must be symmetric")
    diagonal = np.diag(symmetric)
    off_diagonal = symmetric - np.diag(diagonal)
    if np.linalg.norm(off_diagonal, ord="fro") <= 1.0e-13 * scale:
        minimum = float(np.min(diagonal))
        maximum = max(float(np.max(diagonal)), np.finfo(float).eps)
    else:
        eigenvalues = np.linalg.eigvalsh(symmetric)
        minimum = float(np.min(eigenvalues))
        maximum = max(float(np.max(eigenvalues)), np.finfo(float).eps)
    if minimum < -1.0e-10 * maximum:
        raise ValueError(f"{name} must be positive semidefinite")
    return symmetric


def _normalize_covariance(
    covariance: RealMatrix | None,
    *,
    matrix_kind: str,
    matrix: ComplexMatrix,
) -> RealMatrix | None:
    if covariance is None:
        return None
    value = _covariance(covariance, name="covariance")
    if matrix_kind in HAMILTONIAN_MATRIX_KINDS and value.shape[0] == 128:
        value = legacy_covariance_to_hermitian(value)
    if value.shape[0] == 64 and hermitian_residual(matrix) > 1.0e-8:
        raise ValueError(
            "64D covariance requires a Hermitian matrix; use 128D coordinates for "
            "a general complex operator"
        )
    return value


@dataclass(frozen=True)
class MatrixRecord:
    """One projected 8x8 matrix and its physical/numerical provenance."""

    composition: float
    temperature_k: float
    volume_a3: float
    k_inv_a: tuple[float, float, float]
    matrix_kind: str
    matrix: ComplexMatrix
    frequency_ev: float | None = None
    basis_overlap: ComplexMatrix | None = None
    covariance: RealMatrix | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        composition = float(self.composition)
        temperature = float(self.temperature_k)
        volume = float(self.volume_a3)
        k = tuple(float(component) for component in self.k_inv_a)
        if not 0.0 <= composition <= 1.0:
            raise ValueError("composition must lie in [0, 1]")
        if temperature < 0.0 or not np.isfinite(temperature):
            raise ValueError("temperature_k must be finite and nonnegative")
        if volume <= 0.0 or not np.isfinite(volume):
            raise ValueError("volume_a3 must be finite and positive")
        if len(k) != 3 or not np.all(np.isfinite(k)):
            raise ValueError("k_inv_a must contain three finite components")
        if self.matrix_kind not in _ALLOWED_KINDS:
            raise ValueError(
                f"matrix_kind must be one of {sorted(_ALLOWED_KINDS)}, "
                f"got {self.matrix_kind!r}"
            )
        frequency = None if self.frequency_ev is None else float(self.frequency_ev)
        if frequency is not None and not np.isfinite(frequency):
            raise ValueError("frequency_ev must be finite when supplied")
        metadata = dict(self.metadata)
        _json_text(metadata, name="metadata")
        matrix = _complex_matrix(self.matrix, name="matrix")
        covariance = _normalize_covariance(
            self.covariance,
            matrix_kind=self.matrix_kind,
            matrix=matrix,
        )

        object.__setattr__(self, "composition", composition)
        object.__setattr__(self, "temperature_k", temperature)
        object.__setattr__(self, "volume_a3", volume)
        object.__setattr__(self, "k_inv_a", k)
        object.__setattr__(self, "matrix", matrix)
        object.__setattr__(self, "frequency_ev", frequency)
        object.__setattr__(
            self,
            "basis_overlap",
            None
            if self.basis_overlap is None
            else _complex_matrix(self.basis_overlap, name="basis_overlap"),
        )
        object.__setattr__(self, "covariance", covariance)
        object.__setattr__(self, "metadata", metadata)


@dataclass(frozen=True)
class MatrixDataset:
    """A versioned collection of matrix records with global provenance."""

    records: tuple[MatrixRecord, ...]
    provenance: Mapping[str, Any]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        records = tuple(self.records)
        if not records:
            raise ValueError("dataset must contain at least one record")
        provenance = dict(self.provenance)
        _json_text(provenance, name="provenance")
        version = str(self.schema_version)
        if version not in {SCHEMA_VERSION, LEGACY_SCHEMA_VERSION}:
            raise ValueError(
                f"unsupported schema_version {version!r}; expected "
                f"{SCHEMA_VERSION!r} or legacy {LEGACY_SCHEMA_VERSION!r}"
            )
        if version == LEGACY_SCHEMA_VERSION:
            provenance = {
                **provenance,
                "schema_migration": {
                    "from": LEGACY_SCHEMA_VERSION,
                    "to": SCHEMA_VERSION,
                    "hamiltonian_covariance": "legacy_128_to_hermitian_64",
                },
            }
            version = SCHEMA_VERSION
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "provenance", provenance)
        object.__setattr__(self, "schema_version", version)


def file_sha256(path: str | Path) -> str:
    """Return the SHA-256 digest of a file."""

    digest = sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_matrix_dataset(path: str | Path, dataset: MatrixDataset) -> str:
    """Write one schema-v2 compressed NPZ dataset and return its digest."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = dataset.records
    count = len(records)
    matrices = np.stack([record.matrix for record in records])
    overlap_present = np.asarray(
        [record.basis_overlap is not None for record in records], dtype=bool
    )
    overlaps = np.zeros((count, 8, 8), dtype=np.complex128)
    covariance_present = np.asarray(
        [record.covariance is not None for record in records], dtype=bool
    )
    covariance_dimension = np.asarray(
        [0 if record.covariance is None else record.covariance.shape[0] for record in records],
        dtype=np.int16,
    )
    covariances = np.zeros(
        (count, MAX_COVARIANCE_DIMENSION, MAX_COVARIANCE_DIMENSION), dtype=float
    )
    for index, record in enumerate(records):
        if record.basis_overlap is not None:
            overlaps[index] = record.basis_overlap
        if record.covariance is not None:
            dimension = record.covariance.shape[0]
            covariances[index, :dimension, :dimension] = record.covariance

    frequencies = np.asarray(
        [np.nan if record.frequency_ev is None else record.frequency_ev for record in records],
        dtype=float,
    )
    metadata = np.asarray(
        [_json_text(record.metadata, name="metadata") for record in records], dtype=str
    )
    np.savez_compressed(
        path,
        schema_version=np.asarray(SCHEMA_VERSION),
        provenance_json=np.asarray(_json_text(dataset.provenance, name="provenance")),
        composition=np.asarray([record.composition for record in records], dtype=float),
        temperature_k=np.asarray([record.temperature_k for record in records], dtype=float),
        volume_a3=np.asarray([record.volume_a3 for record in records], dtype=float),
        k_inv_a=np.asarray([record.k_inv_a for record in records], dtype=float),
        matrix_kind=np.asarray([record.matrix_kind for record in records], dtype=str),
        frequency_ev=frequencies,
        matrix_real=matrices.real,
        matrix_imag=matrices.imag,
        basis_overlap_present=overlap_present,
        basis_overlap_real=overlaps.real,
        basis_overlap_imag=overlaps.imag,
        covariance_present=covariance_present,
        covariance_dimension=covariance_dimension,
        covariance=covariances,
        metadata_json=metadata,
    )
    return file_sha256(path)


def _common_shapes(count: int) -> dict[str, tuple[int, ...]]:
    return {
        "temperature_k": (count,),
        "volume_a3": (count,),
        "k_inv_a": (count, 3),
        "matrix_kind": (count,),
        "frequency_ev": (count,),
        "matrix_real": (count, 8, 8),
        "matrix_imag": (count, 8, 8),
        "basis_overlap_present": (count,),
        "basis_overlap_real": (count, 8, 8),
        "basis_overlap_imag": (count, 8, 8),
        "covariance_present": (count,),
        "metadata_json": (count,),
    }


def load_matrix_dataset(
    path: str | Path,
    *,
    expected_sha256: str | None = None,
) -> MatrixDataset:
    """Load schema v2 or migrate one schema-v1 dataset in memory."""

    path = Path(path)
    actual_digest = file_sha256(path)
    if expected_sha256 is not None and actual_digest.lower() != expected_sha256.lower():
        raise ValueError(
            f"SHA-256 mismatch for {path}: expected {expected_sha256}, got {actual_digest}"
        )

    with np.load(path, allow_pickle=False) as data:
        version = str(data["schema_version"].item())
        if version not in {SCHEMA_VERSION, LEGACY_SCHEMA_VERSION}:
            raise ValueError(
                f"unsupported schema_version {version!r}; expected {SCHEMA_VERSION!r} "
                f"or legacy {LEGACY_SCHEMA_VERSION!r}"
            )
        provenance = json.loads(str(data["provenance_json"].item()))
        composition = np.asarray(data["composition"], dtype=float)
        count = composition.size
        required_shapes = _common_shapes(count)
        if version == SCHEMA_VERSION:
            required_shapes |= {
                "covariance_dimension": (count,),
                "covariance": (
                    count,
                    MAX_COVARIANCE_DIMENSION,
                    MAX_COVARIANCE_DIMENSION,
                ),
            }
        else:
            required_shapes["covariance"] = (
                count,
                COMPLEX_OBSERVATION_DIMENSION,
                COMPLEX_OBSERVATION_DIMENSION,
            )
        for name, shape in required_shapes.items():
            if name not in data or data[name].shape != shape:
                actual = None if name not in data else data[name].shape
                raise ValueError(f"invalid shape for {name}: {actual}, expected {shape}")

        records: list[MatrixRecord] = []
        for index in range(count):
            frequency_raw = float(data["frequency_ev"][index])
            overlap = None
            if bool(data["basis_overlap_present"][index]):
                overlap = (
                    np.asarray(data["basis_overlap_real"][index], dtype=float)
                    + 1j * np.asarray(data["basis_overlap_imag"][index], dtype=float)
                )
            covariance = None
            if bool(data["covariance_present"][index]):
                if version == LEGACY_SCHEMA_VERSION:
                    covariance = np.asarray(data["covariance"][index], dtype=float)
                else:
                    dimension = int(data["covariance_dimension"][index])
                    if dimension not in {64, 128}:
                        raise ValueError(
                            f"invalid covariance dimension {dimension} at record {index}"
                        )
                    covariance = np.asarray(
                        data["covariance"][index, :dimension, :dimension], dtype=float
                    )
            records.append(
                MatrixRecord(
                    composition=float(composition[index]),
                    temperature_k=float(data["temperature_k"][index]),
                    volume_a3=float(data["volume_a3"][index]),
                    k_inv_a=tuple(float(value) for value in data["k_inv_a"][index]),
                    matrix_kind=str(data["matrix_kind"][index]),
                    frequency_ev=None if np.isnan(frequency_raw) else frequency_raw,
                    matrix=(
                        np.asarray(data["matrix_real"][index], dtype=float)
                        + 1j * np.asarray(data["matrix_imag"][index], dtype=float)
                    ),
                    basis_overlap=overlap,
                    covariance=covariance,
                    metadata=json.loads(str(data["metadata_json"][index])),
                )
            )

    if version == LEGACY_SCHEMA_VERSION:
        provenance = {
            **provenance,
            "schema_migration": {
                "from": LEGACY_SCHEMA_VERSION,
                "to": SCHEMA_VERSION,
                "source_sha256": actual_digest,
                "hamiltonian_covariance": "legacy_128_to_hermitian_64",
                "complex_self_energy_covariance": "retained_128",
            },
        }
    return MatrixDataset(
        records=tuple(records),
        provenance=provenance,
        schema_version=SCHEMA_VERSION,
    )
