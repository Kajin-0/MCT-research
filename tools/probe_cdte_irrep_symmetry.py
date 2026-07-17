#!/usr/bin/env python3
"""Probe full Gamma symmetry matrices from a completed QE CdTe save directory.

This command records the actual IrRep/QE conventions before any canonical Kane
basis is accepted. It deliberately does not assign Gamma6, Gamma8, or Gamma7 and
does not fit a parameter model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def _complex_matrix(matrix: np.ndarray) -> list[list[list[float]]]:
    return [
        [[float(value.real), float(value.imag)] for value in row]
        for row in np.asarray(matrix, dtype=complex)
    ]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _operation_record(kpoint: Any, operation: Any) -> dict[str, Any]:
    blocks = [(0, 2), (2, 6), (6, 8)]
    record: dict[str, Any] = {
        "index": int(operation.ind),
        "time_reversal": bool(operation.time_reversal),
        "rotation_reduced": np.asarray(operation.rotation, dtype=float).tolist(),
        "translation_reduced": np.asarray(operation.translation, dtype=float).tolist(),
        "axis_cartesian": np.asarray(operation.axis, dtype=float).tolist(),
        "angle_over_pi": float(operation.angle / math.pi),
        "inversion_improper": bool(operation.inversion),
        "spinor_rotation": _complex_matrix(operation.spinor_rotation),
    }
    if hasattr(operation, "rotation_cart"):
        record["rotation_cartesian"] = np.asarray(
            operation.rotation_cart, dtype=float
        ).tolist()

    try:
        raw_blocks = kpoint.symm_matrix(
            kpoint,
            operation,
            block_indices=blocks,
            unitary=False,
        )
        unitary_blocks = kpoint.symm_matrix(
            kpoint,
            operation,
            block_indices=blocks,
            unitary=True,
        )
    except Exception as error:  # preserve a fail-closed diagnostic
        record["matrix_status"] = "error"
        record["matrix_error"] = f"{type(error).__name__}: {error}"
        return record

    record["matrix_status"] = "available"
    record["raw_blocks"] = [_complex_matrix(block) for block in raw_blocks]
    record["unitary_blocks"] = [
        _complex_matrix(block) for block in unitary_blocks
    ]
    record["raw_characters"] = [
        [float(np.trace(block).real), float(np.trace(block).imag)]
        for block in raw_blocks
    ]
    record["unitary_characters"] = [
        [float(np.trace(block).real), float(np.trace(block).imag)]
        for block in unitary_blocks
    ]
    record["raw_unitarity_residuals"] = [
        float(np.linalg.norm(block.conj().T @ block - np.eye(block.shape[0])))
        for block in raw_blocks
    ]
    record["raw_to_unitary_frobenius_changes"] = [
        float(np.linalg.norm(raw - unitary))
        for raw, unitary in zip(raw_blocks, unitary_blocks, strict=True)
    ]
    return record


def probe(prefix: str | Path) -> dict[str, Any]:
    import irrep
    from irrep.bandstructure import BandStructure

    prefix_path = Path(prefix).resolve()
    save_directory = Path(str(prefix_path) + ".save")
    schema = save_directory / "data-file-schema.xml"
    if not schema.is_file():
        raise FileNotFoundError(schema)

    band_structure = BandStructure.from_espresso(
        prefix=str(prefix_path),
        IBstart=30,
        IBend=38,
        kplist=[0],
        Ecut=None,
        calculate_traces=False,
        save_wf=True,
        include_TR=True,
        verbosity=1,
    )
    if len(band_structure.kpoints) != 1:
        raise RuntimeError("expected exactly the Gamma k point")
    kpoint = band_structure.kpoints[0]
    energies = np.asarray(kpoint.Energy_raw, dtype=float)
    if energies.shape != (8,):
        raise RuntimeError(f"expected eight selected bands, got {energies.shape}")

    operations = [
        _operation_record(kpoint, operation)
        for operation in band_structure.spacegroup.symmetries
    ]
    available = [item for item in operations if item["matrix_status"] == "available"]
    unitary_count = sum(not item["time_reversal"] for item in operations)
    antiunitary_count = sum(item["time_reversal"] for item in operations)
    if unitary_count < 24:
        raise RuntimeError("CdTe probe did not recover the expected unitary group size")
    if antiunitary_count == 0:
        raise RuntimeError("time-reversal operations were not included")
    if len(available) != len(operations):
        raise RuntimeError("at least one Gamma symmetry matrix could not be evaluated")

    return {
        "status": "raw_symmetry_probe_only_no_kane_basis_assignment",
        "irrep_version": str(irrep.__version__),
        "irrep_module_path": str(Path(irrep.__file__).resolve()),
        "qe_prefix": str(prefix_path),
        "data_file_schema_sha256": _sha256(schema),
        "space_group_name": str(band_structure.spacegroup.name),
        "space_group_number": str(band_structure.spacegroup.number_str),
        "spinor": bool(band_structure.spinor),
        "gamma_reduced_coordinate": np.asarray(kpoint.k, dtype=float).tolist(),
        "selected_global_bands_one_based": list(range(31, 39)),
        "selected_energy_ev": energies.tolist(),
        "declared_energy_blocks_relative": [[0, 2], [2, 6], [6, 8]],
        "declared_energy_blocks_global_one_based": [[31, 32], [33, 36], [37, 38]],
        "operation_count": len(operations),
        "unitary_operation_count": unitary_count,
        "antiunitary_operation_count": antiunitary_count,
        "operations": operations,
        "claim_boundary": (
            "This probe records full matrices and conventions only. No irrep label, "
            "canonical basis, Kane parameter, convergence, or physical-reference "
            "claim is authorized."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", help="QE prefix path without the .save suffix")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = probe(args.prefix)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
