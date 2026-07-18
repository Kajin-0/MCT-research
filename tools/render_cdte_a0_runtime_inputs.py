#!/usr/bin/env python3
"""Render the first declared CdTe A0 runtime inputs and hash all dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from tools.cdte_volume_grid import grid_from_specification
from tools.render_first_principles_input import render


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "first_principles" / "a0" / "templates"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def pseudo_records(selection: dict[str, Any], pseudo_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for element in ("Cd", "Te"):
        entry = selection["elements"][element]
        for kind, source_key, hash_key in (
            ("upf", "upf", "upf_sha256"),
            ("psp8", "psp8", "psp8_sha256"),
        ):
            filename = Path(entry["source_files"][source_key]).name
            path = pseudo_dir / filename
            if not path.is_file():
                raise FileNotFoundError(path)
            digest = sha256_file(path)
            expected = entry[hash_key]
            if digest != expected:
                raise ValueError(
                    f"{element} {kind} hash mismatch: {digest} != {expected}"
                )
            records[f"{element}_{kind}"] = {
                "path": str(path),
                "filename": filename,
                "sha256": digest,
                "size_bytes": path.stat().st_size,
            }
    return records


def write_parameters(path: Path, values: dict[str, Any]) -> None:
    path.write_text(json.dumps(values, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def derive_settings(specification: dict[str, Any]) -> dict[str, Any]:
    ladders = specification["convergence_ladders"]
    protocol = specification["convergence_protocol"]
    reference = specification["structure"]["execution_lattice_constant_angstrom"]
    if not isinstance(reference, (int, float)) or reference <= 0:
        raise ValueError("execution lattice must be selected before rendering A0 inputs")

    ecutwfc = max(float(value) for value in ladders["ecutwfc_ry"])
    ecutrho = min(float(value) for value in ladders["ecutrho_ry"])
    kgrid = min(int(value) for value in ladders["k_grid_n"])
    nbnd = min(int(value) for value in ladders["nbnd"])
    scf_thr = max(float(value) for value in ladders["scf_conv_thr_ry"])
    ph_thr = max(float(value) for value in ladders["ph_tr2"])

    expected_first = protocol["sequence"][0]
    if expected_first != "ecutrho_at_ecutwfc_114Ry":
        raise ValueError("unexpected first convergence stage")
    if ecutwfc != 114.0 or ecutrho != 456.0:
        raise ValueError("declared first A0 cutoff point changed unexpectedly")

    return {
        "reference_lattice_angstrom": float(reference),
        "ecutwfc_ry": ecutwfc,
        "ecutrho_ry": ecutrho,
        "ecut_ha": ecutwfc / 2.0,
        "kgrid": kgrid,
        "nbnd": nbnd,
        "scf_conv_thr_ry": scf_thr,
        "ph_tr2": ph_thr,
        "volume_grid": grid_from_specification(specification),
    }


def render_runtime_inputs(
    specification_path: Path,
    selection_path: Path,
    pseudo_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    specification = load_object(specification_path)
    selection = load_object(selection_path)
    settings = derive_settings(specification)
    pseudos = pseudo_records(selection, pseudo_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    parameter_dir = output_dir / "parameters"
    manifest_dir = output_dir / "manifests"
    input_dir = output_dir / "inputs"
    parameter_dir.mkdir(parents=True, exist_ok=True)

    common = {
        "LATTICE_ANGSTROM": f"{settings['reference_lattice_angstrom']:.15f}",
        "KGRID": settings["kgrid"],
    }
    qe_parameters = {
        **common,
        "PREFIX": "cdte_a0",
        "PSEUDO_DIR": str(pseudo_dir.resolve()),
        "OUTDIR": str((output_dir / "qe-tmp").resolve()),
        "ECUTWFC_RY": f"{settings['ecutwfc_ry']:.1f}",
        "ECUTRHO_RY": f"{settings['ecutrho_ry']:.1f}",
        "NBND": settings["nbnd"],
        "SCF_CONV_THR_RY": f"{settings['scf_conv_thr_ry']:.1e}",
        "CD_UPF": pseudos["Cd_upf"]["filename"],
        "TE_UPF": pseudos["Te_upf"]["filename"],
    }
    ph_parameters = {
        "PREFIX": "cdte_a0",
        "OUTDIR": str((output_dir / "qe-tmp").resolve()),
        "FILDYN": str((output_dir / "cdte_a0.gamma.dyn").resolve()),
        "PH_TR2": f"{settings['ph_tr2']:.1e}",
        "NITER_PH": 0,
    }
    abinit_parameters = {
        **common,
        "PSEUDO_DIR": str(pseudo_dir.resolve()),
        "CD_PSP8": pseudos["Cd_psp8"]["filename"],
        "TE_PSP8": pseudos["Te_psp8"]["filename"],
        "ECUT_HA": f"{settings['ecut_ha']:.1f}",
        "NBAND": settings["nbnd"],
        "TOLVRS": "1.0d-10",
    }

    jobs = {
        "qe_scf": (
            TEMPLATES / "cdte_qe_scf_dry.in.template",
            input_dir / "cdte_qe_scf_dry.in",
            parameter_dir / "cdte_qe_scf_dry.json",
            manifest_dir / "cdte_qe_scf_dry.manifest.json",
            qe_parameters,
            [
                f"Cd_UPF={pseudos['Cd_upf']['path']}",
                f"Te_UPF={pseudos['Te_upf']['path']}",
            ],
        ),
        "qe_ph": (
            TEMPLATES / "cdte_qe_ph_gamma.in.template",
            input_dir / "cdte_qe_ph_gamma.in",
            parameter_dir / "cdte_qe_ph_gamma.json",
            manifest_dir / "cdte_qe_ph_gamma.manifest.json",
            ph_parameters,
            [],
        ),
        "abinit": (
            TEMPLATES / "cdte_abinit_dry.abi.template",
            input_dir / "cdte_abinit_dry.abi",
            parameter_dir / "cdte_abinit_dry.json",
            manifest_dir / "cdte_abinit_dry.manifest.json",
            abinit_parameters,
            [
                f"Cd_PSP8={pseudos['Cd_psp8']['path']}",
                f"Te_PSP8={pseudos['Te_psp8']['path']}",
            ],
        ),
    }

    manifests: dict[str, Any] = {}
    for name, (template, output, parameters, manifest, values, external) in jobs.items():
        write_parameters(parameters, values)
        manifests[name] = render(
            template,
            output,
            parameters,
            manifest,
            input_files=external,
        )

    result = {
        "schema_version": "1.0",
        "execution_performed": False,
        "scientific_result_available": False,
        "selected_first_a0_point": {
            key: value for key, value in settings.items() if key != "volume_grid"
        },
        "volume_grid": settings["volume_grid"],
        "runtime_pseudopotentials": pseudos,
        "rendered_inputs": {
            name: {
                "path": manifest["rendered_input"]["path"],
                "sha256": manifest["rendered_input"]["sha256"],
                "manifest_path": str(jobs[name][3]),
            }
            for name, manifest in manifests.items()
        },
    }
    (output_dir / "render-result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-spec",
        type=Path,
        default=ROOT / "first_principles" / "a0" / "cdte_a0_run_spec.json",
    )
    parser.add_argument(
        "--selection",
        type=Path,
        default=ROOT / "first_principles" / "a0" / "cdte_pseudopotential_selection.json",
    )
    parser.add_argument("--pseudo-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = render_runtime_inputs(
        args.run_spec, args.selection, args.pseudo_dir, args.output_dir
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
