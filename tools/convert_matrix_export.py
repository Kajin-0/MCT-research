#!/usr/bin/env python3
"""Convert an explicit full-matrix export into the repository NPZ schema."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mct_research.code_exports import (
    ExportDefaults,
    NetcdfFieldMap,
    load_jsonl_matrix_export,
    load_netcdf_matrix_export,
)
from mct_research.dataio import save_matrix_dataset


def _json_file(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a JSONL or explicitly mapped NetCDF full 8x8 matrix export "
            "into the integrity-checkable MatrixDataset NPZ format."
        )
    )
    parser.add_argument("input", help="input JSONL or NetCDF file")
    parser.add_argument("output", help="output .npz MatrixDataset file")
    parser.add_argument(
        "--format",
        choices=("jsonl", "netcdf"),
        required=True,
        dest="input_format",
    )
    parser.add_argument("--composition", type=float, required=True)
    parser.add_argument("--temperature-k", type=float, required=True)
    parser.add_argument("--volume-a3", type=float, required=True)
    parser.add_argument(
        "--matrix-kind",
        required=True,
        choices=(
            "hamiltonian",
            "quasiparticle_hamiltonian",
            "self_energy_fan",
            "self_energy_dw",
            "self_energy_total",
        ),
    )
    parser.add_argument("--frequency-ev", type=float)
    parser.add_argument(
        "--mapping-json",
        help="required for NetCDF; explicit variable-name mapping",
    )
    parser.add_argument(
        "--provenance-json",
        required=True,
        help="JSON object containing code version, inputs, pseudopotentials, and hashes",
    )
    parser.add_argument(
        "--metadata-json",
        help="optional default per-record metadata JSON object",
    )
    parser.add_argument(
        "--sha256-output",
        help="optional path receiving the output file SHA-256 digest",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    provenance = _json_file(args.provenance_json)
    metadata = None if args.metadata_json is None else _json_file(args.metadata_json)
    defaults = ExportDefaults(
        composition=args.composition,
        temperature_k=args.temperature_k,
        volume_a3=args.volume_a3,
        matrix_kind=args.matrix_kind,
        frequency_ev=args.frequency_ev,
        metadata=metadata,
    )

    if args.input_format == "jsonl":
        dataset = load_jsonl_matrix_export(
            args.input,
            defaults=defaults,
            provenance=provenance,
        )
    else:
        if args.mapping_json is None:
            raise SystemExit("--mapping-json is required for NetCDF conversion")
        mapping = NetcdfFieldMap(**_json_file(args.mapping_json))
        dataset = load_netcdf_matrix_export(
            args.input,
            fields=mapping,
            defaults=defaults,
            provenance=provenance,
        )

    digest = save_matrix_dataset(args.output, dataset)
    print(f"records={len(dataset.records)}")
    print(f"sha256={digest}")
    if args.sha256_output is not None:
        Path(args.sha256_output).write_text(digest + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
