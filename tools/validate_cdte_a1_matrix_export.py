#!/usr/bin/env python3
"""Validate the minimum real CdTe A1 matrix self-energy export."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.kane8 import time_reversal_unitary
from mct_research.thermal_kane import gamma_irrep_covariance_residual


MATRIX_FIELDS = (
    "fan_real_ev",
    "fan_imag_ev",
    "debye_waller_real_ev",
    "fan_derivative_real",
    "total_real_ev",
)


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _matrix(record: dict[str, Any], name: str, dimension: int) -> np.ndarray:
    value = np.asarray(record[name], dtype=float)
    if value.shape != (dimension, dimension) or not np.all(np.isfinite(value)):
        raise ValueError(f"{name} must be a finite {dimension}x{dimension} matrix")
    return value.astype(complex)


def _relative_residual(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.linalg.norm(left - right, ord="fro")
        / max(np.linalg.norm(right, ord="fro"), 1.0)
    )


def validate(
    payload: dict[str, Any],
    a0_audit: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    if contract.get("stage") != "cdte_a1_matrix_self_energy_export_gate":
        raise ValueError("unexpected A1 export contract stage")
    prerequisite = contract["prerequisite"]
    prerequisite_stage_pass = a0_audit.get("status") == prerequisite["audit_stage"]
    prerequisite_value = bool(
        a0_audit.get("decision", {}).get(prerequisite["required_decision"], False)
    )
    prerequisite_pass = prerequisite_stage_pass and (
        prerequisite_value is bool(prerequisite["required_value"])
    )

    basis = contract["basis"]
    metadata_checks = {
        "stage": payload.get("stage") == "cdte_a1_matrix_self_energy_export",
        "basis": payload.get("basis") == basis["name"],
        "gauge": payload.get("gauge") == basis["gauge"],
        "state_order": payload.get("state_order") == basis["state_order"],
        "fan_provenance": bool(payload.get("provenance", {}).get("fan_complete")),
        "debye_waller_provenance": bool(
            payload.get("provenance", {}).get("debye_waller_complete")
        ),
        "separate_components": bool(
            payload.get("provenance", {}).get("fan_and_dw_separate")
        ),
        "source_identity": bool(payload.get("provenance", {}).get("source_digest")),
    }
    expected_temperatures = [float(value) for value in contract["temperature_grid_k"]]
    temperatures = [float(value) for value in payload.get("temperature_grid_k", [])]
    metadata_checks["temperature_grid"] = temperatures == expected_temperatures
    expected_k = {
        label: np.asarray(vector, dtype=float)
        for label, vector in contract["k_points_inverse_angstrom"].items()
    }
    payload_k = payload.get("k_points_inverse_angstrom", {})
    metadata_checks["k_point_labels"] = set(payload_k) == set(expected_k)
    metadata_checks["k_point_values"] = metadata_checks["k_point_labels"] and all(
        np.linalg.norm(np.asarray(payload_k[label], dtype=float) - vector) <= 1.0e-12
        for label, vector in expected_k.items()
    )

    dimension = int(basis["matrix_dimension"])
    records = payload.get("records", [])
    expected_count = len(expected_temperatures) * len(expected_k)
    metadata_checks["record_count"] = len(records) == expected_count
    by_key: dict[tuple[float, str], dict[str, Any]] = {}
    matrix_symmetry_residuals = []
    closure_residuals = []
    gamma_residuals = []
    damping_maximum_eigenvalues = []
    metric_minimum_eigenvalues = []
    for record in records:
        key = (float(record["temperature_k"]), str(record["k_label"]))
        if key in by_key:
            raise ValueError(f"duplicate A1 record {key}")
        by_key[key] = record
        matrices = {name: _matrix(record, name, dimension) for name in MATRIX_FIELDS}
        for name, matrix in matrices.items():
            matrix_symmetry_residuals.append(
                _relative_residual(matrix, matrix.conj().T)
            )
        closure_residuals.append(
            float(
                np.linalg.norm(
                    matrices["total_real_ev"]
                    - matrices["fan_real_ev"]
                    - matrices["debye_waller_real_ev"],
                    ord="fro",
                )
            )
        )
        damping_maximum_eigenvalues.append(
            float(np.linalg.eigvalsh(matrices["fan_imag_ev"]).max())
        )
        metric_minimum_eigenvalues.append(
            float(
                np.linalg.eigvalsh(
                    np.eye(dimension) - matrices["fan_derivative_real"]
                ).min()
            )
        )
        if key[1] == "Gamma":
            gamma_residuals.extend(
                (
                    gamma_irrep_covariance_residual(matrices["total_real_ev"]),
                    gamma_irrep_covariance_residual(
                        matrices["fan_derivative_real"]
                    ),
                )
            )

    expected_keys = {
        (temperature, label)
        for temperature in expected_temperatures
        for label in expected_k
    }
    metadata_checks["record_keys"] = set(by_key) == expected_keys

    tr = time_reversal_unitary()
    time_reversal_residuals = []
    if metadata_checks["record_keys"]:
        for temperature in expected_temperatures:
            for plus, minus in contract["time_reversal_pairs"]:
                plus_record = by_key[(temperature, plus)]
                minus_record = by_key[(temperature, minus)]
                for name in MATRIX_FIELDS:
                    plus_matrix = _matrix(plus_record, name, dimension)
                    minus_matrix = _matrix(minus_record, name, dimension)
                    transformed = tr @ minus_matrix.conj() @ tr.conj().T
                    time_reversal_residuals.append(
                        _relative_residual(plus_matrix, transformed)
                    )

    bins = payload.get("mode_resolved_gamma_frequency_bins", [])
    mode_identity_residuals = []
    valid_bins = True
    for item in bins:
        theta = float(item["theta_k"])
        conduction = float(item["conduction_amplitude_ev"])
        valence = float(item["valence_amplitude_ev"])
        gap = float(item["gap_amplitude_ev"])
        valid_bins = valid_bins and theta > 0.0 and np.isfinite(theta)
        mode_identity_residuals.append(abs(gap - (conduction - valence)))

    thresholds = contract["thresholds"]
    numerical_checks = {
        "matrix_components_hermitian": max(matrix_symmetry_residuals, default=float("inf"))
        <= float(thresholds["maximum_matrix_symmetry_residual"]),
        "fan_dw_total_closure": max(closure_residuals, default=float("inf"))
        <= float(thresholds["maximum_component_closure_residual_ev"]),
        "time_reversal": max(time_reversal_residuals, default=float("inf"))
        <= float(thresholds["maximum_time_reversal_residual"]),
        "gamma_td_covariance": max(gamma_residuals, default=float("inf"))
        <= float(thresholds["maximum_gamma_td_residual"]),
        "causal_damping": max(damping_maximum_eigenvalues, default=float("inf"))
        <= float(thresholds["maximum_positive_damping_eigenvalue_ev"]),
        "positive_quasiparticle_metric": min(
            metric_minimum_eigenvalues, default=-float("inf")
        )
        >= float(thresholds["minimum_quasiparticle_metric_eigenvalue"]),
        "frequency_bin_count": len(bins)
        >= int(thresholds["minimum_frequency_bin_count"]),
        "frequency_bins_valid": valid_bins,
        "mode_gap_identity": max(mode_identity_residuals, default=float("inf"))
        <= float(thresholds["maximum_mode_gap_identity_residual_ev"]),
    }
    metadata_pass = all(metadata_checks.values())
    numerical_pass = all(numerical_checks.values())
    accepted = prerequisite_pass and metadata_pass and numerical_pass
    return {
        "schema_version": "1.0",
        "status": "cdte_a1_matrix_self_energy_export_validated",
        "checks": {
            "prerequisite": {
                "stage": prerequisite_stage_pass,
                "a1_authorized": prerequisite_value,
                "passed": prerequisite_pass,
            },
            "metadata": metadata_checks,
            "numerical": numerical_checks,
        },
        "diagnostics": {
            "maximum_matrix_symmetry_residual": max(
                matrix_symmetry_residuals, default=float("inf")
            ),
            "maximum_component_closure_residual_ev": max(
                closure_residuals, default=float("inf")
            ),
            "maximum_time_reversal_residual": max(
                time_reversal_residuals, default=float("inf")
            ),
            "maximum_gamma_td_residual": max(
                gamma_residuals, default=float("inf")
            ),
            "maximum_damping_eigenvalue_ev": max(
                damping_maximum_eigenvalues, default=float("inf")
            ),
            "minimum_quasiparticle_metric_eigenvalue": min(
                metric_minimum_eigenvalues, default=-float("inf")
            ),
            "maximum_mode_gap_identity_residual_ev": max(
                mode_identity_residuals, default=float("inf")
            ),
        },
        "decision": {
            "accepted_for_validated_matrix_pipeline": accepted,
            "a0_prerequisite_pass": prerequisite_pass,
            "schema_and_provenance_pass": metadata_pass,
            "matrix_physics_pass": numerical_pass,
            "interpretation": (
                "The export is complete and may populate the validated matrix pipeline."
                if accepted
                else "The export is blocked by the A0 prerequisite, schema/provenance, "
                "or matrix-physics gates. Do not run downstream A1 analysis."
            ),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def analyze(
    payload_path: str | Path,
    a0_audit_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    payload = json.loads(Path(payload_path).read_text(encoding="utf-8"))
    a0_audit = json.loads(Path(a0_audit_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    result = validate(payload, a0_audit, contract)
    result["input_sha256"] = {
        "payload": _sha256(payload_path),
        "a0_audit": _sha256(a0_audit_path),
        "contract": _sha256(contract_path),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--a0-audit", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.payload, args.a0_audit, args.contract)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
