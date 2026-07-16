#!/usr/bin/env python3
"""Evaluate the fail-closed readiness state for the authorized CdTe A0 stage."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def _load_object(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _strictly_increasing(values: list[Any]) -> bool:
    return bool(values) and all(
        isinstance(value, (int, float)) and value > 0 for value in values
    ) and all(left < right for left, right in zip(values, values[1:]))


def _strictly_decreasing_positive(values: list[Any]) -> bool:
    return bool(values) and all(
        isinstance(value, (int, float)) and value > 0 for value in values
    ) and all(left > right for left, right in zip(values, values[1:]))


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_sha256(value: Any) -> bool:
    return bool(_SHA256.fullmatch(str(value)))


def _lattice_provenance_complete(
    lattice: Any,
    source: Any,
) -> bool:
    if not (_finite_number(lattice) and lattice > 0 and isinstance(source, dict)):
        return False

    measurement_temperature = source.get("measurement_temperature_k")
    reported_lattice = source.get("reported_lattice_constant_angstrom")
    reported_uncertainty = source.get("reported_standard_uncertainty_angstrom")
    reference_temperature = source.get("reference_volume_temperature_k")

    anchor_complete = (
        source.get("source_type") == "primary_experimental"
        and _nonempty_string(source.get("citation"))
        and _valid_sha256(source.get("source_sha256"))
        and _finite_number(measurement_temperature)
        and measurement_temperature >= 0
        and _finite_number(reported_lattice)
        and reported_lattice > 0
        and _finite_number(reported_uncertainty)
        and reported_uncertainty >= 0
        and _nonempty_string(source.get("observable_definition"))
        and _finite_number(reference_temperature)
        and reference_temperature >= 0
    )
    if not anchor_complete:
        return False

    same_temperature = math.isclose(
        float(measurement_temperature),
        float(reference_temperature),
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    if same_temperature:
        return math.isclose(
            float(lattice),
            float(reported_lattice),
            rel_tol=0.0,
            abs_tol=max(float(reported_uncertainty), 1e-12),
        )

    transformation = source.get("transformation_to_reference", {})
    if not isinstance(transformation, dict):
        return False
    bounds = transformation.get("integration_temperature_bounds_k")
    bounds_complete = (
        isinstance(bounds, list)
        and len(bounds) == 2
        and all(_finite_number(value) and value >= 0 for value in bounds)
        and math.isclose(
            min(float(value) for value in bounds),
            min(float(measurement_temperature), float(reference_temperature)),
            rel_tol=0.0,
            abs_tol=1e-12,
        )
        and math.isclose(
            max(float(value) for value in bounds),
            max(float(measurement_temperature), float(reference_temperature)),
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    return (
        _nonempty_string(transformation.get("method"))
        and _nonempty_string(transformation.get("thermal_expansion_citation"))
        and _valid_sha256(transformation.get("thermal_expansion_source_sha256"))
        and transformation.get("thermal_expansion_status")
        == "primary_measurement_acquired_verified"
        and bounds_complete
        and _nonempty_string(transformation.get("uncertainty_propagation"))
        and _nonempty_string(transformation.get("derivation_manifest"))
    )


def evaluate_readiness(
    specification: dict[str, Any],
    pseudopotential_selection: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    add(
        "stage_is_a0",
        specification.get("stage") == "A0_static_phonon_readiness",
        "Only the static/phonon A0 readiness stage is accepted.",
    )

    authorization = specification.get("authorization", {})
    allowed = (
        "static_scf",
        "coarse_phonon_sanity",
        "dielectric_born_charge_sanity",
    )
    forbidden = (
        "a1_timed_4x4x4_smoke_test",
        "production_ahc",
        "dense_epw",
        "hgte",
        "alloy",
    )
    add(
        "a0_scope_authorized",
        isinstance(authorization, dict)
        and all(authorization.get(name) is True for name in allowed)
        and all(authorization.get(name) is False for name in forbidden),
        "A0 sanity work must be enabled and all later stages must remain disabled.",
    )

    verification = pseudopotential_selection.get("verification_state", {})
    elements = pseudopotential_selection.get("elements", {})
    hashes_present = (
        isinstance(elements, dict)
        and all(
            isinstance(elements.get(element), dict)
            and _SHA256.fullmatch(str(elements[element].get("upf_sha256", "")))
            and _SHA256.fullmatch(str(elements[element].get("psp8_sha256", "")))
            for element in ("Cd", "Te")
        )
    )
    add(
        "pseudopotential_bytes_verified",
        isinstance(verification, dict)
        and verification.get("downloaded_byte_sha256_verified") is True
        and hashes_present,
        "Cd and Te UPF/psp8 SHA-256 values must be recorded from verified bytes.",
    )

    source_code = specification.get("source_code", {})
    for key, expected_repo in (
        ("quantum_espresso", "QEF/q-e"),
        ("abinit", "abinit/abinit"),
    ):
        code = source_code.get(key, {}) if isinstance(source_code, dict) else {}
        add(
            f"{key}_source_pinned",
            isinstance(code, dict)
            and code.get("repository") == expected_repo
            and isinstance(code.get("tag"), str)
            and bool(code.get("tag"))
            and bool(_GIT_SHA.fullmatch(str(code.get("commit", "")))),
            f"{key} requires an immutable 40-character source commit.",
        )
        executables = code.get("executable_sha256", {})
        expected_executables = code.get("executables", [])
        add(
            f"{key}_installed_binary_recorded",
            isinstance(code.get("installed_version_output"), str)
            and bool(code["installed_version_output"].strip())
            and isinstance(executables, dict)
            and isinstance(expected_executables, list)
            and bool(expected_executables)
            and all(
                _SHA256.fullmatch(str(executables.get(name, "")))
                for name in expected_executables
            ),
            f"{key} installed version output and executable SHA-256 values are required.",
        )
        add(
            f"{key}_release_syntax_checked",
            code.get("release_specific_syntax_checked") is True,
            f"Rendered inputs must be checked with the pinned {key} release.",
        )

    structure = specification.get("structure", {})
    source = (
        structure.get("execution_lattice_constant_source", {})
        if isinstance(structure, dict)
        else {}
    )
    lattice = (
        structure.get("execution_lattice_constant_angstrom")
        if isinstance(structure, dict)
        else None
    )
    add(
        "execution_lattice_constant_provenance",
        _lattice_provenance_complete(lattice, source),
        (
            "A positive execution lattice requires a hashed primary absolute "
            "measurement with temperature and uncertainty. Extrapolation to the "
            "reference temperature additionally requires a verified thermal-expansion "
            "source and derivation manifest."
        ),
    )

    ladders = specification.get("convergence_ladders", {})
    ecutwfc = ladders.get("ecutwfc_ry", []) if isinstance(ladders, dict) else []
    expected_cutoffs = (
        pseudopotential_selection.get("cdte_cutoff_ladder_rydberg", {})
        if isinstance(pseudopotential_selection, dict)
        else {}
    )
    expected_ecutwfc = [
        expected_cutoffs.get("low"),
        expected_cutoffs.get("normal"),
        expected_cutoffs.get("high"),
    ]
    add(
        "ecutwfc_ladder_matches_verified_hints",
        ecutwfc == expected_ecutwfc and _strictly_increasing(ecutwfc),
        "The 94/102/114 Ry ladder must match the verified PseudoDojo conversion.",
    )

    ecutrho = ladders.get("ecutrho_ry", []) if isinstance(ladders, dict) else []
    add(
        "ecutrho_ladder_declared",
        isinstance(ecutrho, list)
        and len(ecutrho) >= len(ecutwfc)
        and all(isinstance(value, (int, float)) and value > 0 for value in ecutrho)
        and min(ecutrho) >= max(ecutwfc),
        "Declare an independent charge-density cutoff ladder; no ratio is assumed.",
    )
    add(
        "k_grid_ladder_declared",
        isinstance(ladders.get("k_grid_n"), list)
        and len(ladders["k_grid_n"]) >= 3
        and _strictly_increasing(ladders["k_grid_n"]),
        "At least three increasing Monkhorst-Pack grid sizes are required.",
    )
    add(
        "band_count_ladder_declared",
        isinstance(ladders.get("nbnd"), list)
        and len(ladders["nbnd"]) >= 3
        and _strictly_increasing(ladders["nbnd"]),
        "At least three increasing band counts are required.",
    )
    add(
        "electronic_threshold_ladder_declared",
        isinstance(ladders.get("scf_conv_thr_ry"), list)
        and len(ladders["scf_conv_thr_ry"]) >= 2
        and _strictly_decreasing_positive(ladders["scf_conv_thr_ry"]),
        "SCF thresholds must tighten monotonically.",
    )
    add(
        "phonon_threshold_ladder_declared",
        isinstance(ladders.get("ph_tr2"), list)
        and len(ladders["ph_tr2"]) >= 2
        and _strictly_decreasing_positive(ladders["ph_tr2"]),
        "Phonon thresholds must tighten monotonically.",
    )

    runtime = specification.get("runtime_inputs", {})
    add(
        "runtime_pseudopotential_hashes_verified",
        isinstance(runtime, dict)
        and runtime.get("runtime_hashes_verified") is True
        and isinstance(runtime.get("runtime_hash_manifest"), str)
        and bool(runtime["runtime_hash_manifest"].strip()),
        "The exact runtime copies must match the verified pseudopotential manifest.",
    )
    add(
        "render_manifests_recorded",
        isinstance(runtime, dict)
        and all(
            isinstance(runtime.get(name), str) and bool(runtime[name].strip())
            for name in (
                "rendered_qe_scf_manifest",
                "rendered_qe_phonon_manifest",
                "rendered_abinit_manifest",
            )
        ),
        "Hash manifests for every rendered A0 input are required.",
    )

    claim = specification.get("readiness_claim", {})
    add(
        "no_result_claim_before_execution",
        isinstance(claim, dict)
        and claim.get("calculation_executed") is False
        and claim.get("scientific_result_available") is False,
        "The readiness record cannot claim a calculation or scientific result.",
    )

    ready = all(check["passed"] for check in checks)
    return {
        "schema_version": "1.1",
        "stage": specification.get("stage"),
        "ready_for_execution": ready,
        "passed_checks": sum(check["passed"] for check in checks),
        "total_checks": len(checks),
        "blocking_checks": [
            check["name"] for check in checks if not check["passed"]
        ],
        "checks": checks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-spec-json",
        default="first_principles/a0/cdte_a0_run_spec.json",
    )
    parser.add_argument(
        "--selection-json",
        default="first_principles/a0/cdte_pseudopotential_selection.json",
    )
    parser.add_argument("--report-json")
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="exit nonzero unless every execution prerequisite passes",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = evaluate_readiness(
        _load_object(args.run_spec_json),
        _load_object(args.selection_json),
    )
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if args.report_json:
        path = Path(args.report_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    return 1 if args.require_ready and not report["ready_for_execution"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
