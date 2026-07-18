#!/usr/bin/env python3
"""Create one compact, fail-closed CdTe A0 runtime-readiness evidence record."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED_QE_COMMIT = "500de340b820e1cb8c05f2d8bb8fced102f377c1"
EXPECTED_ABINIT_COMMIT = "d50172aacfc501b46cd33ae58fda139e674d40e3"
EXPECTED_PSEUDO_COMMIT = "7aa01a3fcf5ad226caf25bd387a9be9612be9f27"


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


def text_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "text": text.strip(),
    }


def executable_record(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def summarize(
    *,
    render_result_path: Path,
    ph_validation_path: Path,
    qe_dry_output_path: Path,
    abinit_dry_output_path: Path,
    pw_path: Path,
    ph_path: Path,
    abinit_path: Path,
    pw_version_path: Path,
    ph_version_path: Path,
    abinit_version_path: Path,
    source_identity_path: Path,
) -> dict[str, Any]:
    render_result = load_object(render_result_path)
    ph_validation = load_object(ph_validation_path)
    source_identity = load_object(source_identity_path)

    expected_sources = {
        "quantum_espresso": EXPECTED_QE_COMMIT,
        "abinit": EXPECTED_ABINIT_COMMIT,
        "pseudodojo": EXPECTED_PSEUDO_COMMIT,
    }
    if source_identity != expected_sources:
        raise ValueError(
            f"source identity mismatch: {source_identity!r} != {expected_sources!r}"
        )
    if render_result.get("execution_performed") is not False:
        raise ValueError("renderer must record execution_performed=false")
    if render_result.get("scientific_result_available") is not False:
        raise ValueError("renderer must record scientific_result_available=false")
    if ph_validation.get("passed") is not True:
        raise ValueError("pinned-source ph.x keyword validation did not pass")

    qe_dry = text_record(qe_dry_output_path)
    if "JOB DONE" not in qe_dry["text"]:
        raise ValueError("QE nstep=0 parser initialization did not reach JOB DONE")
    abinit_dry = text_record(abinit_dry_output_path)
    if not abinit_dry["text"]:
        raise ValueError("ABINIT --dry-run produced no output")

    rendered_inputs = render_result.get("rendered_inputs")
    runtime_pseudos = render_result.get("runtime_pseudopotentials")
    if not isinstance(rendered_inputs, dict) or set(rendered_inputs) != {
        "qe_scf",
        "qe_ph",
        "abinit",
    }:
        raise ValueError("render result does not contain all three required inputs")
    if not isinstance(runtime_pseudos, dict) or set(runtime_pseudos) != {
        "Cd_upf",
        "Cd_psp8",
        "Te_upf",
        "Te_psp8",
    }:
        raise ValueError("render result does not contain all four runtime pseudos")

    return {
        "schema_version": "1.0",
        "status": "runtime_and_rendered_inputs_validated_no_scientific_run",
        "source_identity": source_identity,
        "executables": {
            "pw.x": executable_record(pw_path),
            "ph.x": executable_record(ph_path),
            "abinit": executable_record(abinit_path),
        },
        "version_outputs": {
            "pw.x": text_record(pw_version_path),
            "ph.x": text_record(ph_version_path),
            "abinit": text_record(abinit_version_path),
        },
        "runtime_pseudopotentials": runtime_pseudos,
        "rendered_inputs": rendered_inputs,
        "selected_first_a0_point": render_result["selected_first_a0_point"],
        "volume_grid": render_result["volume_grid"],
        "syntax_validation": {
            "qe_scf_nstep_zero": {
                "passed": True,
                "output": qe_dry,
                "scope": "input parsing and initialization only",
            },
            "qe_ph_pinned_source_variables": ph_validation,
            "abinit_dry_run": {
                "passed": True,
                "output": abinit_dry,
                "scope": "ABINIT command-line dry run only",
            },
        },
        "runtime_hashes_verified": True,
        "release_specific_syntax_checked": True,
        "calculation_executed": False,
        "scientific_result_available": False,
        "claim_boundary": (
            "This record validates exact runtime bytes and rendered-input syntax for "
            "the first declared A0 point. It contains no converged setting, static "
            "electronic result, phonon result, dielectric tensor, Born charge, AHC, "
            "HgTe, or alloy result."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-result", type=Path, required=True)
    parser.add_argument("--ph-validation", type=Path, required=True)
    parser.add_argument("--qe-dry-output", type=Path, required=True)
    parser.add_argument("--abinit-dry-output", type=Path, required=True)
    parser.add_argument("--pw", type=Path, required=True)
    parser.add_argument("--ph", type=Path, required=True)
    parser.add_argument("--abinit", type=Path, required=True)
    parser.add_argument("--pw-version", type=Path, required=True)
    parser.add_argument("--ph-version", type=Path, required=True)
    parser.add_argument("--abinit-version", type=Path, required=True)
    parser.add_argument("--source-identity", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    result = summarize(
        render_result_path=args.render_result,
        ph_validation_path=args.ph_validation,
        qe_dry_output_path=args.qe_dry_output,
        abinit_dry_output_path=args.abinit_dry_output,
        pw_path=args.pw,
        ph_path=args.ph,
        abinit_path=args.abinit,
        pw_version_path=args.pw_version,
        ph_version_path=args.ph_version,
        abinit_version_path=args.abinit_version,
        source_identity_path=args.source_identity,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
