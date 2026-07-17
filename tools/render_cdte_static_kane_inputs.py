#!/usr/bin/env python3
"""Render the planning-only CdTe static Kane smoke inputs deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OUTPUT_NAMES = (
    "cdte_kane.scf.in",
    "cdte_kane.nscf.in",
    "cdte_kane.win",
    "cdte_kane.pw2wan.in",
)
PSEUDO_FILENAMES = {"Cd": "Cd-sp_r.upf", "Te": "Te-d_r.upf"}
ATOMIC_MASSES = {"Cd": 112.414, "Te": 127.60}


def _load(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("smoke specification must contain one JSON object")
    return value


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _number(value: float) -> str:
    return f"{float(value):.15f}".rstrip("0").rstrip(".") or "0"


def _validate(spec: dict[str, Any]) -> None:
    if spec.get("stage") != "static_kane_projection_method_smoke":
        raise ValueError("unexpected stage")
    authorization = spec.get("authorization", {})
    forbidden = (
        "physical_reference_geometry_claim",
        "phonons",
        "electron_phonon_self_energy",
        "production_ahc",
        "hgte",
        "alloy",
    )
    if any(authorization.get(name) is not False for name in forbidden):
        raise ValueError("method smoke must not authorize a physical or later-stage claim")

    geometry = spec.get("planning_geometry", {})
    if geometry.get("status") != "planning_geometry_only_not_physical_reference":
        raise ValueError("geometry is not explicitly planning-only")
    cell = geometry.get("primitive_cell_rows_angstrom")
    positions = geometry.get("fractional_positions")
    if (
        not isinstance(cell, list)
        or len(cell) != 3
        or any(not isinstance(row, list) or len(row) != 3 for row in cell)
        or not isinstance(positions, dict)
        or set(positions) != {"Cd", "Te"}
    ):
        raise ValueError("invalid primitive geometry")

    settings = spec.get("electronic_smoke_settings", {})
    required = {
        "noncolin": True,
        "lspinorb": True,
        "occupations": "fixed",
        "nbnd": 40,
        "ecutwfc_ry": 94,
        "ecutrho_ry": 376,
    }
    for name, expected in required.items():
        if settings.get(name) != expected:
            raise ValueError(f"unexpected {name}")
    if settings.get("gamma_centered_scf_grid") != [4, 4, 4]:
        raise ValueError("unexpected SCF grid")

    points = spec.get("k_stencil", {}).get("ordered_points")
    if (
        not isinstance(points, list)
        or len(points) != 13
        or [point.get("index") for point in points] != list(range(1, 14))
        or points[0].get("label") != "Gamma"
        or points[0].get("crystal") != [0.0, 0.0, 0.0]
    ):
        raise ValueError("invalid ordered 13-point stencil")

    export = spec.get("wavefunction_overlap_export", {})
    win = export.get("wannier90_win", {})
    pw2wan = export.get("pw2wannier90", {})
    if (
        win.get("num_bands") != 40
        or win.get("num_wann") != 8
        or win.get("spinors") is not True
        or win.get("postproc_setup") is not True
        or win.get("skip_B1_tests") is not True
        or len(win.get("export_only_parser_projections", [])) != 4
    ):
        raise ValueError("invalid Wannier90 export contract")
    if (
        pw2wan.get("spin_component") != "none"
        or pw2wan.get("write_mmn") is not True
        or pw2wan.get("write_amn") is not False
        or pw2wan.get("write_unk") is not False
    ):
        raise ValueError("invalid pw2wannier90 export contract")


def _geometry(spec: dict[str, Any]) -> str:
    geometry = spec["planning_geometry"]
    cell = "\n".join(
        "  " + " ".join(_number(value) for value in row)
        for row in geometry["primitive_cell_rows_angstrom"]
    )
    positions = "\n".join(
        f"  {element} "
        + " ".join(_number(value) for value in geometry["fractional_positions"][element])
        for element in ("Cd", "Te")
    )
    return (
        "ATOMIC_SPECIES\n"
        f"  Cd {ATOMIC_MASSES['Cd']:.3f} {PSEUDO_FILENAMES['Cd']}\n"
        f"  Te {ATOMIC_MASSES['Te']:.2f} {PSEUDO_FILENAMES['Te']}\n"
        "ATOMIC_POSITIONS crystal\n"
        f"{positions}\n"
        "CELL_PARAMETERS angstrom\n"
        f"{cell}\n"
    )


def _scf(spec: dict[str, Any], pseudo_dir: str, outdir: str) -> str:
    settings = spec["electronic_smoke_settings"]
    grid = " ".join(str(value) for value in settings["gamma_centered_scf_grid"])
    return (
        "&CONTROL\n"
        "  calculation = 'scf'\n"
        "  title = 'CdTe static Kane planning smoke: SCF'\n"
        "  prefix = 'cdte_kane'\n"
        f"  pseudo_dir = '{pseudo_dir}'\n"
        f"  outdir = '{outdir}'\n"
        "  verbosity = 'high'\n"
        "  restart_mode = 'from_scratch'\n"
        "  disk_io = 'low'\n"
        "/\n"
        "&SYSTEM\n"
        "  ibrav = 0\n"
        "  nat = 2\n"
        "  ntyp = 2\n"
        f"  nbnd = {settings['nbnd']}\n"
        f"  ecutwfc = {settings['ecutwfc_ry']}\n"
        f"  ecutrho = {settings['ecutrho_ry']}\n"
        "  occupations = 'fixed'\n"
        "  noncolin = .true.\n"
        "  lspinorb = .true.\n"
        "/\n"
        "&ELECTRONS\n"
        f"  conv_thr = {settings['conv_thr_ry']:.1e}\n"
        "/\n"
        f"{_geometry(spec)}"
        "K_POINTS automatic\n"
        f"  {grid} 0 0 0\n"
    )


def _nscf(spec: dict[str, Any], pseudo_dir: str, outdir: str) -> str:
    settings = spec["electronic_smoke_settings"]
    points = spec["k_stencil"]["ordered_points"]
    rendered_points = "\n".join(
        "  "
        + " ".join(_number(value) for value in point["crystal"])
        + " 1.0"
        + f" ! {point['index']:02d} {point['label']}"
        for point in points
    )
    return (
        "&CONTROL\n"
        "  calculation = 'nscf'\n"
        "  title = 'CdTe static Kane planning smoke: 13-point SOC NSCF'\n"
        "  prefix = 'cdte_kane'\n"
        f"  pseudo_dir = '{pseudo_dir}'\n"
        f"  outdir = '{outdir}'\n"
        "  verbosity = 'high'\n"
        "  restart_mode = 'from_scratch'\n"
        "  disk_io = 'low'\n"
        "/\n"
        "&SYSTEM\n"
        "  ibrav = 0\n"
        "  nat = 2\n"
        "  ntyp = 2\n"
        f"  nbnd = {settings['nbnd']}\n"
        f"  ecutwfc = {settings['ecutwfc_ry']}\n"
        f"  ecutrho = {settings['ecutrho_ry']}\n"
        "  occupations = 'fixed'\n"
        "  noncolin = .true.\n"
        "  lspinorb = .true.\n"
        "  nosym = .true.\n"
        "  noinv = .true.\n"
        "  no_t_rev = .true.\n"
        "/\n"
        "&ELECTRONS\n"
        f"  conv_thr = {settings['conv_thr_ry']:.1e}\n"
        "  startingpot = 'file'\n"
        "/\n"
        f"{_geometry(spec)}"
        "K_POINTS crystal\n"
        f"  {len(points)}\n"
        f"{rendered_points}\n"
    )


def _win(spec: dict[str, Any]) -> str:
    geometry = spec["planning_geometry"]
    export = spec["wavefunction_overlap_export"]["wannier90_win"]
    points = spec["k_stencil"]["ordered_points"]
    cell = "\n".join(
        "  " + " ".join(_number(value) for value in row)
        for row in geometry["primitive_cell_rows_angstrom"]
    )
    positions = "\n".join(
        f"  {element} "
        + " ".join(_number(value) for value in geometry["fractional_positions"][element])
        for element in ("Cd", "Te")
    )
    kpoints = "\n".join(
        "  "
        + " ".join(_number(value) for value in point["crystal"])
        + f" ! {point['index']:02d} {point['label']}"
        for point in points
    )
    nnkpts = "\n".join(f"  {index} 1 0 0 0" for index in range(1, 14))
    projections = "\n".join(
        "  " + value for value in export["export_only_parser_projections"]
    )
    return (
        f"num_bands = {export['num_bands']}\n"
        f"num_wann = {export['num_wann']}\n"
        "spinors = true\n"
        "postproc_setup = true\n"
        "skip_B1_tests = true\n\n"
        "begin unit_cell_cart\n"
        "ang\n"
        f"{cell}\n"
        "end unit_cell_cart\n\n"
        "begin atoms_frac\n"
        f"{positions}\n"
        "end atoms_frac\n\n"
        "begin projections\n"
        f"{projections}\n"
        "end projections\n\n"
        "begin kpoints\n"
        f"{kpoints}\n"
        "end kpoints\n\n"
        "begin nnkpts\n"
        f"{nnkpts}\n"
        "end nnkpts\n"
    )


def _pw2wan(spec: dict[str, Any], outdir: str) -> str:
    export = spec["wavefunction_overlap_export"]["pw2wannier90"]

    def logical(value: bool) -> str:
        return ".true." if value else ".false."

    return (
        "&INPUTPP\n"
        "  prefix = 'cdte_kane'\n"
        f"  outdir = '{outdir}'\n"
        "  seedname = 'cdte_kane'\n"
        f"  spin_component = '{export['spin_component']}'\n"
        "  wan_mode = 'standalone'\n"
        f"  write_mmn = {logical(export['write_mmn'])}\n"
        f"  write_amn = {logical(export['write_amn'])}\n"
        f"  write_unk = {logical(export['write_unk'])}\n"
        "/\n"
    )


def render(
    spec_path: str | Path,
    output_dir: str | Path,
    *,
    pseudo_dir: str = "./pseudo",
    outdir: str = "./tmp",
) -> dict[str, Any]:
    spec_path = Path(spec_path)
    spec = _load(spec_path)
    _validate(spec)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    contents = {
        "cdte_kane.scf.in": _scf(spec, pseudo_dir, outdir),
        "cdte_kane.nscf.in": _nscf(spec, pseudo_dir, outdir),
        "cdte_kane.win": _win(spec),
        "cdte_kane.pw2wan.in": _pw2wan(spec, outdir),
    }
    hashes: dict[str, str] = {}
    for name in OUTPUT_NAMES:
        data = contents[name].encode("utf-8")
        (output_dir / name).write_bytes(data)
        hashes[name] = _sha256(data)
    return {
        "schema_version": "1.0",
        "status": "rendered_planning_inputs_not_execution_evidence",
        "planning_geometry_status": spec["planning_geometry"]["status"],
        "qe_source_tag_required": spec["electronic_smoke_settings"]["required_source_tag"],
        "qe_source_commit_required": spec["electronic_smoke_settings"]["required_source_commit"],
        "expected_runtime_pseudopotential_sha256": spec["required_pseudopotential_sha256"],
        "pseudopotential_filenames": PSEUDO_FILENAMES,
        "pseudo_dir_literal": pseudo_dir,
        "outdir_literal": outdir,
        "ordered_kpoint_labels": [
            point["label"] for point in spec["k_stencil"]["ordered_points"]
        ],
        "rendered_file_sha256": hashes,
        "generated_nnkp_present": False,
        "runtime_hashes_verified": False,
        "calculation_executed": False,
        "scientific_result_available": False,
        "prohibited_claim": (
            "These files do not validate the lattice, cutoff, k grid, band count, "
            "or physical Kane parameters."
        ),
    }


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
