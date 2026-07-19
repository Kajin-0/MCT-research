"""Strict adapters from external first-principles matrix exports to MatrixDataset."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
from numpy.typing import NDArray

from .dataio import HAMILTONIAN_MATRIX_KINDS, MatrixDataset, MatrixRecord
from .matrix_coordinates import (
    COMPLEX_OBSERVATION_DIMENSION,
    HERMITIAN_OBSERVATION_DIMENSION,
)

ComplexArray = NDArray[np.complex128]
_ALLOWED_MATRIX_KINDS = HAMILTONIAN_MATRIX_KINDS | {
    "self_energy_fan",
    "self_energy_dw",
    "self_energy_total",
}


class ExportFormatError(ValueError):
    """Raised when an external export cannot be interpreted without guessing."""


@dataclass(frozen=True)
class ExportDefaults:
    composition: float
    temperature_k: float
    volume_a3: float
    matrix_kind: str
    frequency_ev: float | None = None
    metadata: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= float(self.composition) <= 1.0:
            raise ValueError("composition must lie in [0, 1]")
        if float(self.temperature_k) < 0.0:
            raise ValueError("temperature_k must be nonnegative")
        if float(self.volume_a3) <= 0.0:
            raise ValueError("volume_a3 must be positive")
        if self.matrix_kind not in _ALLOWED_MATRIX_KINDS:
            raise ValueError(f"unsupported matrix_kind {self.matrix_kind!r}")


@dataclass(frozen=True)
class NetcdfFieldMap:
    """Explicit mapping from NetCDF variables to full-matrix export fields."""

    k_inv_a: str
    matrix: str | None = None
    matrix_real: str | None = None
    matrix_imag: str | None = None
    temperature_k: str | None = None
    volume_a3: str | None = None
    composition: str | None = None
    frequency_ev: str | None = None
    basis_overlap: str | None = None
    basis_overlap_real: str | None = None
    basis_overlap_imag: str | None = None
    covariance: str | None = None

    def __post_init__(self) -> None:
        complex_matrix_representation = self.matrix is not None
        split_matrix = self.matrix_real is not None or self.matrix_imag is not None
        if complex_matrix_representation == split_matrix:
            raise ValueError(
                "specify exactly one matrix representation: `matrix` or both "
                "`matrix_real` and `matrix_imag`"
            )
        if split_matrix and (self.matrix_real is None or self.matrix_imag is None):
            raise ValueError("both matrix_real and matrix_imag are required")
        complex_overlap = self.basis_overlap is not None
        split_overlap = (
            self.basis_overlap_real is not None or self.basis_overlap_imag is not None
        )
        if complex_overlap and split_overlap:
            raise ValueError(
                "basis overlap must use complex or split representation, not both"
            )
        if split_overlap and (
            self.basis_overlap_real is None or self.basis_overlap_imag is None
        ):
            raise ValueError("both basis_overlap_real and basis_overlap_imag are required")


def _as_record_array(
    value: Any,
    count: int,
    *,
    name: str,
    trailing_shape: tuple[int, ...],
) -> np.ndarray:
    array = np.asarray(value)
    if trailing_shape:
        if array.shape == trailing_shape and count == 1:
            array = array.reshape((1,) + trailing_shape)
        expected = (count,) + trailing_shape
        if array.shape != expected:
            raise ExportFormatError(f"{name} must have shape {expected}, got {array.shape}")
    else:
        if array.ndim == 0:
            array = np.repeat(array.reshape(1), count)
        if array.shape != (count,):
            raise ExportFormatError(
                f"{name} must be scalar or shape ({count},), got {array.shape}"
            )
    return array


def _complex_records(real: Any, imag: Any, count: int, *, name: str) -> ComplexArray:
    real_array = _as_record_array(
        real, count, name=f"{name}_real", trailing_shape=(8, 8)
    )
    imag_array = _as_record_array(
        imag, count, name=f"{name}_imag", trailing_shape=(8, 8)
    )
    result = np.asarray(real_array, dtype=float) + 1j * np.asarray(
        imag_array, dtype=float
    )
    if not np.all(np.isfinite(result)):
        raise ExportFormatError(f"{name} contains non-finite values")
    return np.asarray(result, dtype=np.complex128)


def _covariance_records(value: Any, count: int) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    allowed_dimensions = {
        HERMITIAN_OBSERVATION_DIMENSION,
        COMPLEX_OBSERVATION_DIMENSION,
    }
    if array.ndim == 2 and count == 1 and array.shape[0] in allowed_dimensions:
        if array.shape[0] != array.shape[1]:
            raise ExportFormatError("covariance must be square")
        array = array.reshape((1,) + array.shape)
    if array.ndim != 3 or array.shape[0] != count:
        raise ExportFormatError(
            "covariance must have shape (N,64,64) or (N,128,128)"
        )
    if array.shape[1] != array.shape[2] or array.shape[1] not in allowed_dimensions:
        raise ExportFormatError(
            "covariance must have shape (N,64,64) or (N,128,128)"
        )
    if not np.all(np.isfinite(array)):
        raise ExportFormatError("covariance contains non-finite values")
    return array


def dataset_from_arrays(
    *,
    matrices: Any,
    k_inv_a: Any,
    defaults: ExportDefaults,
    provenance: Mapping[str, Any],
    temperatures_k: Any | None = None,
    volumes_a3: Any | None = None,
    compositions: Any | None = None,
    frequencies_ev: Any | None = None,
    basis_overlaps: Any | None = None,
    covariances: Any | None = None,
    record_metadata: Sequence[Mapping[str, Any]] | None = None,
) -> MatrixDataset:
    """Build a validated MatrixDataset from explicit array-valued fields.

    Covariance may use native 64D Hermitian coordinates or legacy/general 128D
    complex coordinates. MatrixRecord performs the explicit 128-to-64 migration
    for Hamiltonian-like matrix kinds.
    """

    matrices_array = np.asarray(matrices, dtype=np.complex128)
    if matrices_array.shape == (8, 8):
        matrices_array = matrices_array.reshape(1, 8, 8)
    if matrices_array.ndim != 3 or matrices_array.shape[1:] != (8, 8):
        raise ExportFormatError(
            f"matrices must have shape (N, 8, 8), got {matrices_array.shape}"
        )
    if not np.all(np.isfinite(matrices_array)):
        raise ExportFormatError("matrices contain non-finite values")
    count = matrices_array.shape[0]
    k_array = _as_record_array(
        k_inv_a, count, name="k_inv_a", trailing_shape=(3,)
    ).astype(float)
    temperature_array = _as_record_array(
        defaults.temperature_k if temperatures_k is None else temperatures_k,
        count,
        name="temperature_k",
        trailing_shape=(),
    ).astype(float)
    volume_array = _as_record_array(
        defaults.volume_a3 if volumes_a3 is None else volumes_a3,
        count,
        name="volume_a3",
        trailing_shape=(),
    ).astype(float)
    composition_array = _as_record_array(
        defaults.composition if compositions is None else compositions,
        count,
        name="composition",
        trailing_shape=(),
    ).astype(float)

    if frequencies_ev is None:
        frequency_values = [defaults.frequency_ev] * count
    else:
        raw = _as_record_array(
            frequencies_ev, count, name="frequency_ev", trailing_shape=()
        ).astype(float)
        frequency_values = [None if np.isnan(value) else float(value) for value in raw]

    overlap_array = None
    if basis_overlaps is not None:
        overlap_array = _as_record_array(
            basis_overlaps, count, name="basis_overlap", trailing_shape=(8, 8)
        ).astype(np.complex128)
    covariance_array = None if covariances is None else _covariance_records(covariances, count)

    if record_metadata is None:
        metadata_values = [dict(defaults.metadata or {}) for _ in range(count)]
    else:
        if len(record_metadata) != count:
            raise ExportFormatError("record_metadata must contain one mapping per record")
        metadata_values = [
            dict(defaults.metadata or {}) | dict(value) for value in record_metadata
        ]

    records = tuple(
        MatrixRecord(
            composition=float(composition_array[index]),
            temperature_k=float(temperature_array[index]),
            volume_a3=float(volume_array[index]),
            k_inv_a=tuple(float(value) for value in k_array[index]),
            matrix_kind=defaults.matrix_kind,
            matrix=matrices_array[index],
            frequency_ev=frequency_values[index],
            basis_overlap=None if overlap_array is None else overlap_array[index],
            covariance=None if covariance_array is None else covariance_array[index],
            metadata=metadata_values[index],
        )
        for index in range(count)
    )
    return MatrixDataset(records=records, provenance=dict(provenance))


def load_jsonl_matrix_export(
    path: str | Path,
    *,
    defaults: ExportDefaults,
    provenance: Mapping[str, Any],
) -> MatrixDataset:
    """Load a code-agnostic JSONL export containing explicit full matrices."""

    records_raw: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ExportFormatError(
                    f"invalid JSON on line {line_number}: {exc}"
                ) from exc
            if not isinstance(value, dict):
                raise ExportFormatError(f"line {line_number} must contain a JSON object")
            records_raw.append(value)
    if not records_raw:
        raise ExportFormatError("JSONL export contains no records")

    matrices: list[np.ndarray] = []
    k_values: list[Any] = []
    temperatures: list[Any] = []
    volumes: list[Any] = []
    compositions: list[Any] = []
    frequencies: list[Any] = []
    overlaps: list[np.ndarray] = []
    overlap_present: list[bool] = []
    covariances: list[np.ndarray] = []
    covariance_present: list[bool] = []
    metadata: list[Mapping[str, Any]] = []

    default_covariance_dimension = (
        HERMITIAN_OBSERVATION_DIMENSION
        if defaults.matrix_kind in HAMILTONIAN_MATRIX_KINDS
        else COMPLEX_OBSERVATION_DIMENSION
    )
    for index, raw in enumerate(records_raw):
        if "matrix_real" not in raw or "matrix_imag" not in raw:
            raise ExportFormatError(
                f"record {index} must contain matrix_real and matrix_imag; "
                "diagonal self-energy tables are not full matrix exports"
            )
        matrices.append(
            np.asarray(raw["matrix_real"], dtype=float)
            + 1j * np.asarray(raw["matrix_imag"], dtype=float)
        )
        if "k_inv_a" not in raw:
            raise ExportFormatError(f"record {index} is missing k_inv_a")
        k_values.append(raw["k_inv_a"])
        temperatures.append(raw.get("temperature_k", defaults.temperature_k))
        volumes.append(raw.get("volume_a3", defaults.volume_a3))
        compositions.append(raw.get("composition", defaults.composition))
        frequencies.append(
            raw.get(
                "frequency_ev",
                np.nan if defaults.frequency_ev is None else defaults.frequency_ev,
            )
        )

        overlap_present.append(
            "basis_overlap_real" in raw or "basis_overlap_imag" in raw
        )
        if overlap_present[-1]:
            if "basis_overlap_real" not in raw or "basis_overlap_imag" not in raw:
                raise ExportFormatError(f"record {index} has an incomplete basis overlap")
            overlaps.append(
                np.asarray(raw["basis_overlap_real"], dtype=float)
                + 1j * np.asarray(raw["basis_overlap_imag"], dtype=float)
            )
        else:
            overlaps.append(np.eye(8, dtype=np.complex128))

        covariance_present.append("covariance" in raw)
        covariances.append(
            np.asarray(
                raw.get(
                    "covariance",
                    np.eye(default_covariance_dimension, dtype=float),
                ),
                dtype=float,
            )
        )
        metadata.append(raw.get("metadata", {}))

    if any(overlap_present) and not all(overlap_present):
        raise ExportFormatError("basis overlap must be supplied for every record or none")
    if any(covariance_present) and not all(covariance_present):
        raise ExportFormatError("covariance must be supplied for every record or none")
    if all(covariance_present) and len({value.shape for value in covariances}) != 1:
        raise ExportFormatError(
            "all JSONL covariance records must use the same coordinate dimension"
        )

    return dataset_from_arrays(
        matrices=np.stack(matrices),
        k_inv_a=np.asarray(k_values, dtype=float),
        defaults=defaults,
        provenance=provenance,
        temperatures_k=np.asarray(temperatures, dtype=float),
        volumes_a3=np.asarray(volumes, dtype=float),
        compositions=np.asarray(compositions, dtype=float),
        frequencies_ev=np.asarray(frequencies, dtype=float),
        basis_overlaps=np.stack(overlaps) if all(overlap_present) else None,
        covariances=np.stack(covariances) if all(covariance_present) else None,
        record_metadata=metadata,
    )


def load_netcdf_matrix_export(
    path: str | Path,
    *,
    fields: NetcdfFieldMap,
    defaults: ExportDefaults,
    provenance: Mapping[str, Any],
) -> MatrixDataset:
    """Load a full-matrix NetCDF export using an explicit variable mapping."""

    try:
        from netCDF4 import Dataset  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "NetCDF conversion requires the optional dependency netCDF4"
        ) from exc

    with Dataset(Path(path), mode="r") as dataset:
        variables = dataset.variables

        def read(name: str | None, *, required: bool = False) -> Any | None:
            if name is None:
                return None
            if name not in variables:
                if required:
                    raise ExportFormatError(f"NetCDF variable {name!r} is missing")
                return None
            return np.asarray(variables[name][:])

        if fields.matrix is not None:
            matrices = np.asarray(read(fields.matrix, required=True), dtype=np.complex128)
        else:
            matrix_real = read(fields.matrix_real, required=True)
            matrix_imag = read(fields.matrix_imag, required=True)
            raw_real = np.asarray(matrix_real)
            count_guess = 1 if raw_real.shape == (8, 8) else raw_real.shape[0]
            matrices = _complex_records(
                matrix_real, matrix_imag, count_guess, name="matrix"
            )

        count = 1 if matrices.shape == (8, 8) else matrices.shape[0]
        k_values = read(fields.k_inv_a, required=True)
        temperatures = read(fields.temperature_k)
        volumes = read(fields.volume_a3)
        compositions = read(fields.composition)
        frequencies = read(fields.frequency_ev)
        covariances = read(fields.covariance)
        overlaps = None
        if fields.basis_overlap is not None:
            overlaps = np.asarray(
                read(fields.basis_overlap, required=True), dtype=np.complex128
            )
        elif fields.basis_overlap_real is not None:
            overlaps = _complex_records(
                read(fields.basis_overlap_real, required=True),
                read(fields.basis_overlap_imag, required=True),
                count,
                name="basis_overlap",
            )

    return dataset_from_arrays(
        matrices=matrices,
        k_inv_a=k_values,
        defaults=defaults,
        provenance=provenance,
        temperatures_k=temperatures,
        volumes_a3=volumes,
        compositions=compositions,
        frequencies_ev=frequencies,
        basis_overlaps=overlaps,
        covariances=covariances,
    )
