#!/usr/bin/env python3
"""Render the exact runtime-compatible CdTe static Kane smoke inputs.

The base renderer produces the scientific planning inputs. Wannier90 3.1 also
requires an mp_grid bookkeeping entry during preprocessing even though the
explicit nnkpts star defines the actual overlap topology. This wrapper inserts
that declared parser-only entry deterministically and updates the manifest hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tools.render_cdte_static_kane_inputs import render as render_base

WIN_NAME = "cdte_kane.win"
MP_GRID_LINE = "mp_grid = 13 1 1"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render(
    spec_path: str | Path,
    output_dir: str | Path,
    *,
    pseudo_dir: str = "./pseudo",
    outdir: str = "./tmp",
) -> dict[str, object]:
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    expected = spec["wavefunction_overlap_export"]["wannier90_win"].get(
        "parser_mp_grid"
    )
    if expected != [13, 1, 1]:
        raise ValueError("expected declared parser_mp_grid [13, 1, 1]")

    manifest = render_base(
        spec_path,
        output_dir,
        pseudo_dir=pseudo_dir,
        outdir=outdir,
    )
    path = Path(output_dir) / WIN_NAME
    text = path.read_text(encoding="utf-8")
    if "mp_grid" in text.lower():
        raise ValueError("base renderer unexpectedly emitted mp_grid")
    marker = "skip_B1_tests = true\n"
    if text.count(marker) != 1:
        raise ValueError("could not locate unique Wannier90 parser marker")
    text = text.replace(marker, marker + MP_GRID_LINE + "\n", 1)
    path.write_text(text, encoding="utf-8")

    hashes = dict(manifest["rendered_file_sha256"])
    hashes[WIN_NAME] = _sha256(path.read_bytes())
    manifest["rendered_file_sha256"] = hashes
    manifest["runtime_compatibility"] = {
        "wannier90_parser_mp_grid": expected,
        "scientific_kpoint_topology_source": "explicit nnkpts Gamma star",
        "runtime_input_mutation_required": False,
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        default="first_principles/a0/cdte_static_kane_method_smoke.json",
    )
    parser.add_argument(
        "--output-dir",
        default="first_principles/a0/cdte_static_kane_smoke_inputs",
    )
    parser.add_argument("--pseudo-dir", default="./pseudo")
    parser.add_argument("--outdir", default="./tmp")
    parser.add_argument("--manifest-json")
    args = parser.parse_args()
    manifest = render(
        args.spec,
        args.output_dir,
        pseudo_dir=args.pseudo_dir,
        outdir=args.outdir,
    )
    rendered = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.manifest_json:
        Path(args.manifest_json).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
