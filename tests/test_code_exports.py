from __future__ import annotations

import json

import numpy as np
import pytest

from mct_research.code_exports import (
    ExportDefaults,
    ExportFormatError,
    NetcdfFieldMap,
    dataset_from_arrays,
    load_jsonl_matrix_export,
)


def _defaults() -> ExportDefaults:
    return ExportDefaults(
        composition=1.0,
        temperature_k=77.0,
        volume_a3=100.0,
        matrix_kind="self_energy_total",
    )


def test_dataset_from_arrays_broadcasts_defaults() -> None:
    matrices = np.stack([np.eye(8), 2.0 * np.eye(8)]).astype(complex)
    dataset = dataset_from_arrays(
        matrices=matrices,
        k_inv_a=[[0.0, 0.0, 0.0], [0.01, 0.0, 0.0]],
        defaults=_defaults(),
        provenance={"code": "synthetic"},
    )

    assert len(dataset.records) == 2
    assert dataset.records[1].temperature_k == 77.0
    assert dataset.records[1].matrix[0, 0] == 2.0


def test_jsonl_rejects_diagonal_only_self_energy(tmp_path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text(
        json.dumps({"k_inv_a": [0.0, 0.0, 0.0], "diagonal": [1.0, 2.0, 3.0]})
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ExportFormatError, match="full matrix exports"):
        load_jsonl_matrix_export(path, defaults=_defaults(), provenance={})


def test_jsonl_full_matrix_roundtrip(tmp_path) -> None:
    path = tmp_path / "matrix.jsonl"
    rows = []
    for kx in (0.0, 0.01):
        matrix = np.eye(8, dtype=complex) * (1.0 + kx)
        rows.append(
            {
                "k_inv_a": [kx, 0.0, 0.0],
                "matrix_real": matrix.real.tolist(),
                "matrix_imag": matrix.imag.tolist(),
                "metadata": {"source": "unit"},
            }
        )
    path.write_text(
        "\n".join(json.dumps(row) for row in rows), encoding="utf-8"
    )

    dataset = load_jsonl_matrix_export(
        path,
        defaults=_defaults(),
        provenance={"code": "mock"},
    )

    assert len(dataset.records) == 2
    assert dataset.records[1].k_inv_a == (0.01, 0.0, 0.0)
    assert dataset.records[0].metadata["source"] == "unit"


def test_netcdf_mapping_requires_explicit_full_matrix() -> None:
    with pytest.raises(ValueError, match="exactly one matrix representation"):
        NetcdfFieldMap(k_inv_a="k")

    mapping = NetcdfFieldMap(
        k_inv_a="k",
        matrix_real="matrix_real",
        matrix_imag="matrix_imag",
    )
    assert mapping.matrix_real == "matrix_real"
