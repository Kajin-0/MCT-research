#!/usr/bin/env python3
"""Render the one authorized same-geometry CdTe stricter-response point."""
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

CONTRACT = ROOT / "first_principles/a0/cdte_a0_stricter_response_contract.json"


def _effective_settings(
    specification: dict[str, Any], contract: dict[str, Any]
) -> dict[str, Any]:
    derived = derive_settings(specification)
    required = contract["required_settings"]
    unchanged = {
        "reference_lattice_angstrom": derived["reference_lattice_angstrom"],
        "ecutwfc_ry": derived["ecutwfc_ry"],
        "k_grid": [derived["kgrid"]] * 3,
        "k_grid_shift": [0, 0, 0],
        "nbnd": derived["nbnd"],
        "scf_conv_thr_ry": derived["scf_conv_thr_ry"],
        "q_point": [0.0, 0.0, 0.0],
    }
    for name, value in unchanged.items():
        if required[name] != value:
            raise ValueError(f"unauthorized stricter-response drift in {name}: {value!r}")
    baseline = contract["baseline"]
    if derived["ecutrho_ry"] != baseline["ecutrho_ry"]:
        raise ValueError("merged run-spec ecutrho no longer matches the audited baseline")
    if derived["ph_tr2"] != baseline["ph_tr2"]:
        raise ValueError("merged run-spec PH threshold no longer matches the audited baseline")
    if required["ecutrho_ry"] != 570.0 or required["ph_tr2"] != 1.0e-14:
        raise ValueError("diagnostic overrides differ from the authorized decision")
    return {
        **derived,
        "ecutrho_ry": float(required["ecutrho_ry"]),
        "ph_tr2": float(required["ph_tr2"]),
    }


def render_diagnostic(
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
    if contract.get("stage") != "A0_same_geometry_stricter_response_diagnostic":
        raise ValueError("unexpected stricter-response contract stage")
    authorization = contract["authorization"]
    required_true = (
        "one_qe_scf_point",
        "gamma_eigenvalue_extraction",
        "one_gamma_phonon_dielectric_born_point",
        "scientific_audit",
        "comparison_to_first_point",
    )
    required_false = (
        "convergence_claim",
        "automatic_ladder_continuation",
        "volume_change",
        "functional_change",
        "pseudopotential_change",
        "q_grid_change",
        "a1_electron_phonon",
        "production_ahc",
        "hgte",
        "alloy",
    )
    if not all(authorization[name] is True for name in required_true):
        raise ValueError("required diagnostic authorization is missing")
    if not all(authorization[name] is False for name in required_false):
        raise ValueError("diagnostic authorization boundary is too broad")

    settings = _effective_settings(specification, contract)
    pseudos = pseudo_records(selection, pseudo_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir = output_dir / "inputs"
    parameter_dir = output_dir / "parameters"
    manifest_dir = output_dir / "manifests"
    parameter_dir.mkdir(parents=True, exist_ok=True)

    prefix = "cdte_a0_strict"
    outdir = str((output_dir / "qe-tmp").resolve())
    scf_parameters = {
        "PREFIX": prefix,
        "PSEUDO_DIR": str(pseudo_dir.resolve()),
        "OUTDIR": outdir,
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
        "PREFIX": prefix,
        "OUTDIR": outdir,
        "FILDYN": str((output_dir / "cdte_a0_strict.gamma.dyn").resolve()),
        "PH_TR2": f"{settings['ph_tr2']:.1e}",
    }
    jobs = {
        "qe_scf": (
            TEMPLATES / "cdte_qe_scf_stricter_response.in.template",
            input_dir / "cdte_qe_scf_stricter_response.in",
            parameter_dir / "cdte_qe_scf_stricter_response.json",
            manifest_dir / "cdte_qe_scf_stricter_response.manifest.json",
            scf_parameters,
            [
                f"Cd_UPF={pseudos['Cd_upf']['path']}",
                f"Te_UPF={pseudos['Te_upf']['path']}",
            ],
        ),
        "qe_ph": (
            TEMPLATES / "cdte_qe_ph_gamma_stricter_response.in.template",
            input_dir / "cdte_qe_ph_gamma_stricter_response.in",
            parameter_dir / "cdte_qe_ph_gamma_stricter_response.json",
            manifest_dir / "cdte_qe_ph_gamma_stricter_response.manifest.json",
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
        "settings": contract["required_settings"],
        "baseline": contract["baseline"],
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
        default=ROOT / "first_principles/a0/cdte_a0_run_spec.json",
    )
    parser.add_argument(
        "--selection",
        type=Path,
        default=ROOT / "first_principles/a0/cdte_pseudopotential_selection.json",
    )
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--pseudo-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = render_diagnostic(
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
