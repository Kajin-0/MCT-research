#!/usr/bin/env python3
"""Render the single authorized CdTe A0 breadth-smoke input pair."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.check_cdte_a0_readiness import evaluate_readiness
from tools.render_cdte_a0_runtime_inputs import (
    ROOT,
    TEMPLATES,
    derive_settings,
    load_object,
    pseudo_records,
    write_parameters,
)
from tools.render_first_principles_input import render


CONTRACT = ROOT / "first_principles" / "a0" / "cdte_a0_first_point_contract.json"


def _required_settings(contract: dict[str, Any]) -> dict[str, Any]:
    required = contract.get("required_settings")
    if not isinstance(required, dict):
        raise ValueError("first-point contract lacks required_settings")
    return required


def _check_settings(settings: dict[str, Any], required: dict[str, Any]) -> None:
    actual = {
        "reference_lattice_angstrom": settings["reference_lattice_angstrom"],
        "ecutwfc_ry": settings["ecutwfc_ry"],
        "ecutrho_ry": settings["ecutrho_ry"],
        "k_grid": [settings["kgrid"]] * 3,
        "k_grid_shift": [0, 0, 0],
        "nbnd": settings["nbnd"],
        "scf_conv_thr_ry": settings["scf_conv_thr_ry"],
        "ph_tr2": settings["ph_tr2"],
        "q_point": [0.0, 0.0, 0.0],
    }
    if actual != required:
        raise ValueError(f"run-spec first point differs from contract: {actual!r}")


def render_first_point(
    specification_path: Path,
    selection_path: Path,
    contract_path: Path,
    pseudo_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    specification = load_object(specification_path)
    selection = load_object(selection_path)
    contract = load_object(contract_path)

    readiness = evaluate_readiness(specification, selection)
    if not readiness["ready_for_execution"]:
        raise ValueError(
            "repository is not ready for A0 execution: "
            + ", ".join(readiness["blocking_checks"])
        )
    if contract.get("stage") != "A0_first_point_breadth_smoke":
        raise ValueError("unexpected first-point contract stage")
    authorization = contract.get("authorization", {})
    if not (
        authorization.get("one_qe_scf_point") is True
        and authorization.get("gamma_eigenvalue_extraction") is True
        and authorization.get("one_gamma_phonon_dielectric_born_point") is True
        and authorization.get("convergence_claim") is False
        and authorization.get("automatic_ladder_continuation") is False
        and authorization.get("a1_electron_phonon") is False
        and authorization.get("production_ahc") is False
        and authorization.get("hgte") is False
        and authorization.get("alloy") is False
    ):
        raise ValueError("first-point authorization boundary is invalid")

    settings = derive_settings(specification)
    _check_settings(settings, _required_settings(contract))
    pseudos = pseudo_records(selection, pseudo_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir = output_dir / "inputs"
    parameter_dir = output_dir / "parameters"
    manifest_dir = output_dir / "manifests"
    parameter_dir.mkdir(parents=True, exist_ok=True)

    common = {
        "PREFIX": "cdte_a0_first",
        "PSEUDO_DIR": str(pseudo_dir.resolve()),
        "OUTDIR": str((output_dir / "qe-tmp").resolve()),
    }
    scf_parameters = {
        **common,
        "LATTICE_ANGSTROM": f"{settings['reference_lattice_angstrom']:.15f}",
        "ECUTWFC_RY": f"{settings['ecutwfc_ry']:.1f}",
        "ECUTRHO_RY": f"{settings['ecutrho_ry']:.1f}",
        "NBND": settings["nbnd"],
        "SCF_CONV_THR_RY": f"{settings['scf_conv_thr_ry']:.1e}",
        "KGRID": settings["kgrid"],
        "CD_UPF": pseudos["Cd_upf"]["filename"],
        "TE_UPF": pseudos["Te_upf"]["filename"],
    }
    ph_parameters = {
        **common,
        "FILDYN": str((output_dir / "cdte_a0_first.gamma.dyn").resolve()),
        "PH_TR2": f"{settings['ph_tr2']:.1e}",
    }

    jobs = {
        "qe_scf": (
            TEMPLATES / "cdte_qe_scf_first_point.in.template",
            input_dir / "cdte_qe_scf_first_point.in",
            parameter_dir / "cdte_qe_scf_first_point.json",
            manifest_dir / "cdte_qe_scf_first_point.manifest.json",
            scf_parameters,
            [
                f"Cd_UPF={pseudos['Cd_upf']['path']}",
                f"Te_UPF={pseudos['Te_upf']['path']}",
            ],
        ),
        "qe_ph": (
            TEMPLATES / "cdte_qe_ph_gamma_first_point.in.template",
            input_dir / "cdte_qe_ph_gamma_first_point.in",
            parameter_dir / "cdte_qe_ph_gamma_first_point.json",
            manifest_dir / "cdte_qe_ph_gamma_first_point.manifest.json",
            ph_parameters,
            [],
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
        "stage": contract["stage"],
        "repository_ready": True,
        "execution_performed": False,
        "scientific_result_available": False,
        "settings": _required_settings(contract),
        "runtime_pseudopotentials": pseudos,
        "rendered_inputs": {
            name: {
                "path": manifest["rendered_input"]["path"],
                "sha256": manifest["rendered_input"]["sha256"],
                "manifest_path": str(jobs[name][3]),
            }
            for name, manifest in manifests.items()
        },
        "contract": str(contract_path),
    }
    (output_dir / "render-result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--pseudo-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = render_first_point(
        args.run_spec,
        args.selection,
        args.contract,
        args.pseudo_dir,
        args.output_dir,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
