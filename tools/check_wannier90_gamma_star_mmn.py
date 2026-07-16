#!/usr/bin/env python3
"""Validate the Wannier90 .mmn topology for the static Kane method smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def read_mmn(path: str | Path) -> tuple[int, int, int, list[tuple[int, int, tuple[int, int, int], np.ndarray]]]:
    with Path(path).open("r", encoding="utf-8") as stream:
        if stream.readline() == "":
            raise ValueError("missing .mmn comment")
        header = stream.readline().split()
        if len(header) != 3:
            raise ValueError("invalid .mmn header")
        nbnd, nk, nntot = map(int, header)
        blocks = []
        for _ in range(nk * nntot):
            metadata = stream.readline().split()
            if len(metadata) != 5:
                raise ValueError("invalid .mmn block metadata")
            ik, ik2, g1, g2, g3 = map(int, metadata)
            matrix = np.empty((nbnd, nbnd), complex)
            for n in range(nbnd):
                for m in range(nbnd):
                    values = stream.readline().split()
                    if len(values) != 2:
                        raise ValueError("invalid .mmn matrix element")
                    matrix[m, n] = complex(float(values[0]), float(values[1]))
            if not np.all(np.isfinite(matrix)):
                raise ValueError("non-finite .mmn matrix")
            blocks.append((ik, ik2, (g1, g2, g3), matrix))
        if stream.read().strip():
            raise ValueError("unexpected trailing .mmn content")
    return nbnd, nk, nntot, blocks


def validate(path: str | Path, expected_bands: int = 40) -> dict[str, object]:
    nbnd, nk, nntot, blocks = read_mmn(path)
    if (nbnd, nk, nntot, len(blocks)) != (expected_bands, 13, 1, 13):
        raise ValueError("expected a 40-band, 13-point, one-neighbor Gamma star")

    by_source = {block[0]: block for block in blocks}
    if len(by_source) != 13 or set(by_source) != set(range(1, 14)):
        raise ValueError("source indices must be exactly 1 through 13")
    for source, (_, target, image, _) in by_source.items():
        if target != 1 or image != (0, 0, 0):
            raise ValueError(f"source {source} is not linked directly to Gamma")

    gamma = by_source[1][3]
    residual = gamma - np.eye(nbnd)
    return {
        "status": "topology_only_not_material_interpretation",
        "num_bands": nbnd,
        "num_kpoints": nk,
        "nntot": nntot,
        "block_count": len(blocks),
        "finite_overlap_count": 12,
        "gamma_self_maximum_absolute_residual": float(np.max(np.abs(residual))),
        "gamma_self_frobenius_residual": float(np.linalg.norm(residual)),
        "fixed_reference_orientation": "S_i=M_i.conjugate_transpose",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mmn")
    parser.add_argument("--expected-bands", type=int, default=40)
    parser.add_argument("--summary-json")
    args = parser.parse_args()
    summary = validate(args.mmn, args.expected_bands)
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.summary_json:
        Path(args.summary_json).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
