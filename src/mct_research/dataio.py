"""Versioned, integrity-checked storage for projected electronic matrices."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import numpy as np
from numpy.typing import NDArray

from .hermitian import (
    LEGACY_COMPLEX_CARTESIAN_DIMENSION,
    OBSERVATION_DIMENSION,
    hermiticity_residual,
    legacy_covariance_to_hermitian,
)

SCHEMA_VERSION = "2.0"
LEGACY_SCHEMA_VERSION = "1.0"
COVARIANCE_COORDINATE_SYSTEM = "hermitian_frobenius_64"
LEGACY_COVARIANCE_COORDINATE_SYSTEM = "complex_cartesian_128"
_ALLOWED_KINDS = {
    "hamiltonian",
    "quasiparticle_hamiltonian",
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
    expected = (OBSERVATION_DIMENSION, OBSERVATION_DIMENSION)
    if array.shape != expected:
        raise ValueError(f"{name} must have shape {expected}, got {array.shape}")
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


@dataclass(frozen=True)
class MatrixRecord:
    """One projected 8x8 matrix and its physical/numerical provenance.

    Covariance is defined only for a Hermitian matrix observable and is stored in
    the 64 independent Frobenius-isometric coordinates declared by
    :mod:`mct_research.hermitian`.  A general complex self-energy may still be
    stored, but it must not carry covariance until a distinct non-Hermitian
    coordinate schema is introduced.
    """

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
        covariance = (
            None
            if self.covariance is None
            else _covariance(self.covariance, name="covariance")
        )
        if covariance is not None:
            residual = hermiticity_residual(matrix)
            if residual > 1.0e-10:
                raise ValueError(
                    "covariance requires a Hermitian matrix observable: "
                    f"hermiticity residual={residual:.3e}"
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
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {self.schema_version!r}; "
                f"expected {SCHEMA_VERSION!r}"
            )
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "provenance", provenance)


def file_sha256(path: str | Path) -> str:
    """Return the SHA-256 digest of a file."""

    digest = sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_matrix_dataset(path: str | Path, dataset: MatrixDataset) -> str:
    """Write a compressed schema-2 NPZ dataset and return its SHA-256 digest."""

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
    covariances = np.zeros(
        (count, OBSERVATION_DIMENSION, OBSERVATION_DIMENSION), dtype=float
    )
    for index, record in enumerate(records):
        if record.basis_overlap is not None:
            overlaps[index] = record.basis_overlap
        if record.covariance is not None:
            covariances[index] = record.covariance

    frequencies = np.asarray(
        [np.nan if record.frequency_ev is None else record.frequency_ev for record in records],
        dtype=float,
    )
    metadata = np.asarray(
        [_json_text(record.metadata, name="metadata") for record in records], dtype=str
    )

    np.savez_compressed(
        path,
        schema_version=np.asarray(dataset.schema_version),
        covariance_coordinate_system=np.asarray(COVARIANCE_COORDINATE_SYSTEM),
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
        covariance=covariances,
        metadata_json=metadata,
    )
    return file_sha256(path)


def _required_shapes(count: int, *, covariance_dimension: int) -> dict[str, tuple[int, ...]]:
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
        "covariance": (count, covariance_dimension, covariance_dimension),
        "metadata_json": (count,),
    }


def load_matrix_dataset(
    path: str | Path,
    *,
    expected_sha256: str | None = None,
) -> MatrixDataset:
    """Load and validate a dataset, migrating schema-1 covariance explicitly.

    Schema 1.0 used redundant 128D real/imaginary coordinates.  During read, its
    covariance is projected through Hermitization into the independent 64D
    Frobenius coordinates.  The returned object is always schema 2.0 and records
    the migration in both global provenance and per-record metadata.
    """

    path = Path(path)
    actual_digest = file_sha256(path)
    if expected_sha256 is not None and actual_digest.lower() != expected_sha256.lower():
        raise ValueError(
            f"SHA-256 mismatch for {path}: expected {expected_sha256}, got {actual_digest}"
        )

    with np.load(path, allow_pickle=False) as data:
        source_version = str(data["schema_version"].item())
        if source_version not in (SCHEMA_VERSION, LEGACY_SCHEMA_VERSION):
            raise ValueError(
                f"unsupported schema_version {source_version!r}; expected "
                f"{SCHEMA_VERSION!r} or legacy {LEGACY_SCHEMA_VERSION!r}"
            )
        if source_version == SCHEMA_VERSION:
            if "covariance_coordinate_system" not in data:
                raise ValueError("schema 2.0 dataset is missing covariance coordinates")
            coordinate_system = str(data["covariance_coordinate_system"].item())
            if coordinate_system != COVARIANCE_COORDINATE_SYSTEM:
                raise ValueError(
                    f"unsupported covariance coordinate system {coordinate_system!r}"
                )
            covariance_dimension = OBSERVATION_DIMENSION
        else:
            coordinate_system = LEGACY_COVARIANCE_COORDINATE_SYSTEM
            covariance_dimension = LEGACY_COMPLEX_CARTESIAN_DIMENSION

        provenance = json.loads(str(data["provenance_json"].item()))
        composition = np.asarray(data["composition"], dtype=float)
        count = composition.size

        for name, shape in _required_shapes(
            count, covariance_dimension=covariance_dimension
        ).items():
            if data[name].shape != shape:
                raise ValueError(
                    f"invalid shape for {name}: {data[name].shape}, expected {shape}"
                )

        if source_version == LEGACY_SCHEMA_VERSION:
            provenance = dict(provenance)
            migrations = list(provenance.get("schema_migrations", []))
            migrations.append(
                {
                    "from_schema": LEGACY_SCHEMA_VERSION,
                    "to_schema": SCHEMA_VERSION,
                    "from_covariance_coordinates": coordinate_system,
                    "to_covariance_coordinates": COVARIANCE_COORDINATE_SYSTEM,
                    "operation": "Hermitian projection followed by Frobenius-isometric hvec",
                }
            )
            provenance["schema_migrations"] = migrations

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
            metadata = json.loads(str(data["metadata_json"][index]))
            if bool(data["covariance_present"][index]):
                raw_covariance = np.asarray(data["covariance"][index], dtype=float)
                if source_version == LEGACY_SCHEMA_VERSION:
                    covariance = legacy_covariance_to_hermitian(raw_covariance)
                    metadata = dict(metadata)
                    metadata["covariance_schema_migration"] = {
                        "from": LEGACY_COVARIANCE_COORDINATE_SYSTEM,
                        "to": COVARIANCE_COORDINATE_SYSTEM,
                    }
                else:
                    covariance = raw_covariance
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
                    metadata=metadata,
                )
            )

    return MatrixDataset(
        records=tuple(records), provenance=provenance, schema_version=SCHEMA_VERSION
    )
