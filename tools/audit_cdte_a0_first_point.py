#!/usr/bin/env python3
"""Audit the raw CdTe A0 first-point artifact and gate all A1 work."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

import numpy as np


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _last_float(pattern: str, text: str, label: str) -> float:
    values = re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not values:
        raise ValueError(f"missing {label}")
    return float(values[-1])


def _frequencies(text: str) -> list[float]:
    values = [
        float(match.group(1))
        for match in re.finditer(
            r"^\s*\d+\s+(-?\d+(?:\.\d+)?)\s+-?\d+(?:\.\d+)?\s+\d",
            text,
            flags=re.MULTILINE,
        )
    ]
    if len(values) != 6:
        raise ValueError(f"expected six Gamma frequencies, got {len(values)}")
    return values


def _dielectric_matrix(ph_text: str) -> np.ndarray:
    marker = "Dielectric constant in cartesian axis"
    start = ph_text.find(marker)
    if start < 0:
        raise ValueError("missing dielectric tensor")
    rows = re.findall(
        r"\(\s*([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s*\)",
        ph_text[start : start + 1000],
    )
    if len(rows) < 3:
        raise ValueError("incomplete dielectric tensor")
    return np.asarray([[float(value) for value in row] for row in rows[:3]])


def _relative_triplet_spread(values: list[float]) -> float:
    array = np.asarray(values, dtype=float)
    mean = float(np.mean(np.abs(array)))
    return float((array.max() - array.min()) / max(mean, np.finfo(float).eps))


def analyze(
    scf_path: str | Path,
    ph_path: str | Path,
    dynmat_no_asr_path: str | Path,
    dynmat_simple_asr_path: str | Path,
    calculation_state_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    scf_text = Path(scf_path).read_text(encoding="utf-8", errors="replace")
    ph_text = Path(ph_path).read_text(encoding="utf-8", errors="replace")
    no_asr_text = Path(dynmat_no_asr_path).read_text(
        encoding="utf-8", errors="replace"
    )
    simple_asr_text = Path(dynmat_simple_asr_path).read_text(
        encoding="utf-8", errors="replace"
    )
    state = json.loads(Path(calculation_state_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "cdte_a0_first_point_scientific_audit":
        raise ValueError("unexpected A0 audit contract stage")

    total_energy_ry = _last_float(
        r"!\s+total energy\s*=\s*([-+0-9.Ee]+)\s+Ry",
        scf_text,
        "final total energy",
    )
    scf_accuracy_ry = _last_float(
        r"estimated scf accuracy\s*<\s*([-+0-9.Ee]+)\s+Ry",
        scf_text,
        "SCF accuracy",
    )
    occupied, unoccupied = re.findall(
        r"highest occupied, lowest unoccupied level \(ev\):\s*([-+0-9.Ee]+)\s+([-+0-9.Ee]+)",
        scf_text,
        flags=re.IGNORECASE,
    )[-1]
    occupied_ev = float(occupied)
    unoccupied_ev = float(unoccupied)
    direct_gap_ev = unoccupied_ev - occupied_ev
    pressure_kbar = _last_float(
        r"P=\s*([-+0-9.Ee]+)", scf_text, "hydrostatic pressure"
    )

    dielectric = _dielectric_matrix(ph_text)
    dielectric_eigenvalues = np.linalg.eigvalsh(
        0.5 * (dielectric + dielectric.T)
    )
    dielectric_mean = float(np.mean(dielectric_eigenvalues))
    dielectric_anisotropy = float(
        (dielectric_eigenvalues.max() - dielectric_eigenvalues.min())
        / max(abs(dielectric_mean), np.finfo(float).eps)
    )
    born_sum_mean = _last_float(
        r"Effective charges Sum:\s*Mean:\s*([-+0-9.Ee]+)",
        ph_text,
        "Born-charge sum",
    )
    ph_convergence_count = len(
        re.findall(r"Convergence has been achieved", ph_text, flags=re.IGNORECASE)
    )

    raw_frequencies = _frequencies(no_asr_text)
    simple_frequencies = _frequencies(simple_asr_text)
    raw_acoustic = raw_frequencies[:3]
    raw_optical = raw_frequencies[3:]
    simple_acoustic = simple_frequencies[:3]
    simple_optical = simple_frequencies[3:]
    maximum_raw_acoustic = max(abs(value) for value in raw_acoustic)
    raw_optical_mean = float(np.mean(raw_optical))
    simple_optical_mean = float(np.mean(simple_optical))
    asr_optical_shift = abs(simple_optical_mean - raw_optical_mean) / max(
        abs(raw_optical_mean), np.finfo(float).eps
    )

    thresholds = contract["thresholds"]
    required_execution = contract["required_execution"]
    execution_checks = {
        name: bool(state.get(name)) is bool(required)
        for name, required in required_execution.items()
    }
    execution_checks.update(
        {
            "scf_job_done": "JOB DONE" in scf_text,
            "ph_job_done": "JOB DONE" in ph_text,
            "dynmat_no_asr_job_done": "JOB DONE" in no_asr_text,
            "dynmat_simple_asr_job_done": "JOB DONE" in simple_asr_text,
            "ph_response_converged": ph_convergence_count >= 2,
        }
    )
    execution_pass = all(execution_checks.values())

    electronic_checks = {
        "scf_accuracy": scf_accuracy_ry
        <= float(thresholds["maximum_scf_accuracy_ry"]),
        "positive_direct_gamma_gap": direct_gap_ev
        >= float(thresholds["minimum_direct_gamma_gap_ev"]),
    }
    electronic_pass = all(electronic_checks.values())

    response_checks = {
        "raw_acoustic_translation": maximum_raw_acoustic
        <= float(thresholds["maximum_raw_acoustic_absolute_frequency_cm1"]),
        "born_charge_neutrality": abs(born_sum_mean)
        <= float(thresholds["maximum_born_charge_sum_absolute_e"]),
        "asr_optical_stability": asr_optical_shift
        <= float(thresholds["maximum_asr_optical_relative_shift"]),
        "positive_dielectric_tensor": float(dielectric_eigenvalues.min())
        >= float(thresholds["minimum_dielectric_eigenvalue"]),
        "dielectric_cubic_isotropy": dielectric_anisotropy
        <= float(thresholds["maximum_dielectric_relative_anisotropy"]),
        "raw_optical_triplet_degeneracy": _relative_triplet_spread(raw_optical)
        <= float(thresholds["maximum_optical_triplet_relative_spread"]),
        "simple_asr_optical_triplet_degeneracy": _relative_triplet_spread(
            simple_optical
        )
        <= float(thresholds["maximum_optical_triplet_relative_spread"]),
    }
    response_pass = all(response_checks.values())

    fixed_volume_checks = {
        "bounded_static_pressure": abs(pressure_kbar)
        <= float(
            thresholds[
                "maximum_absolute_pressure_kbar_for_unqualified_physical_interpretation"
            ]
        ),
        "response_numerically_sane": response_pass,
    }
    fixed_volume_pass = all(fixed_volume_checks.values())
    a1_authorized = (
        execution_pass and electronic_pass and response_pass and fixed_volume_pass
    )
    failed_response_checks = [
        name for name, passed in response_checks.items() if not passed
    ]
    failed_volume_checks = [
        name for name, passed in fixed_volume_checks.items() if not passed
    ]

    return {
        "schema_version": "1.0",
        "status": "cdte_a0_first_point_scientific_audit_completed",
        "input_sha256": {
            "scf": _sha256(scf_path),
            "ph": _sha256(ph_path),
            "dynmat_no_asr": _sha256(dynmat_no_asr_path),
            "dynmat_simple_asr": _sha256(dynmat_simple_asr_path),
            "calculation_state": _sha256(calculation_state_path),
            "contract": _sha256(contract_path),
        },
        "source": contract["source"],
        "observables": {
            "total_energy_ry": total_energy_ry,
            "scf_accuracy_ry": scf_accuracy_ry,
            "highest_occupied_ev": occupied_ev,
            "lowest_unoccupied_ev": unoccupied_ev,
            "direct_gamma_gap_ev": direct_gap_ev,
            "pressure_kbar": pressure_kbar,
            "dielectric_tensor": dielectric.tolist(),
            "dielectric_eigenvalues": dielectric_eigenvalues.tolist(),
            "dielectric_relative_anisotropy": dielectric_anisotropy,
            "born_charge_sum_mean_e": born_sum_mean,
            "ph_convergence_count": ph_convergence_count,
            "raw_frequencies_cm1": raw_frequencies,
            "simple_asr_frequencies_cm1": simple_frequencies,
            "maximum_raw_acoustic_absolute_frequency_cm1": maximum_raw_acoustic,
            "raw_optical_mean_cm1": raw_optical_mean,
            "simple_asr_optical_mean_cm1": simple_optical_mean,
            "asr_optical_relative_shift": asr_optical_shift,
            "raw_optical_triplet_relative_spread": _relative_triplet_spread(
                raw_optical
            ),
            "simple_asr_optical_triplet_relative_spread": _relative_triplet_spread(
                simple_optical
            ),
            "simple_asr_acoustic_frequencies_cm1": simple_acoustic,
        },
        "checks": {
            "execution": execution_checks,
            "electronic": electronic_checks,
            "response": response_checks,
            "fixed_volume_interpretation": fixed_volume_checks,
        },
        "decision": {
            "execution_pass": execution_pass,
            "electronic_sanity_pass": electronic_pass,
            "response_numerical_sanity_pass": response_pass,
            "fixed_volume_interpretation_pass": fixed_volume_pass,
            "scientific_result_validated": a1_authorized,
            "a1_electron_phonon_authorized": a1_authorized,
            "failed_response_checks": failed_response_checks,
            "failed_fixed_volume_checks": failed_volume_checks,
            "next_authorized_diagnostic": (
                None
                if a1_authorized
                else contract["decision_policy"][
                    "only_authorized_diagnostic_after_failure"
                ]
            ),
            "interpretation": (
                "Execution succeeded and all physical gates passed."
                if a1_authorized
                else "Execution succeeded, but raw response and/or fixed-volume "
                "physical gates failed. Do not use the response as a physical "
                "reference and do not execute A1."
            ),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scf", required=True)
    parser.add_argument("--ph", required=True)
    parser.add_argument("--dynmat-no-asr", required=True)
    parser.add_argument("--dynmat-simple-asr", required=True)
    parser.add_argument("--calculation-state", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.scf,
        args.ph,
        args.dynmat_no_asr,
        args.dynmat_simple_asr,
        args.calculation_state,
        args.contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
