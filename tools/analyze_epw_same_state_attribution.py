#!/usr/bin/env python3
"""Analyze one immutable-state EPW exporter attribution fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.analyze_epw_raw_vertex_fixture import (
    RawVertexError,
    _q_coverage,
    _summed_diagonal_and_covariance,
    _validate_row_identities,
    parse_compact_self_energy_table,
    parse_raw_rows,
)
from tools.design_epw_same_state_attribution import evaluate_attribution


class SameStateAnalysisError(ValueError):
    """Raised when same-state evidence cannot be interpreted unambiguously."""


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SameStateAnalysisError(f"expected JSON object: {path}")
    return value


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _table_metrics(
    records: Sequence[Mapping[str, float | int]],
) -> tuple[list[tuple[int, int]], dict[str, list[float]]]:
    indices: list[tuple[int, int]] = []
    energy: list[float] = []
    self_energy: list[float] = []
    dimensionless: list[float] = []
    for row in records:
        indices.append((int(row["ik"]), int(row["ibnd"])))
        energy.append(float(row["energy_ev"]))
        self_energy.extend(
            [
                float(row["real_sigma_mev"]) * 1.0e-3,
                float(row["imag_sigma_mev"]) * 1.0e-3,
            ]
        )
        dimensionless.extend([float(row["z"]), float(row["lambda"])])
    if len(set(indices)) != len(indices):
        raise SameStateAnalysisError("compact EPW table contains duplicate indices")
    return indices, {
        "energy_ev": energy,
        "self_energy_ev": self_energy,
        "dimensionless": dimensionless,
    }


def _load_three_tables(
    disabled_a_path: str | Path,
    disabled_b_path: str | Path,
    enabled_path: str | Path,
) -> tuple[dict[str, list[float]], dict[str, list[float]], dict[str, list[float]], int]:
    parsed = [
        parse_compact_self_energy_table(disabled_a_path),
        parse_compact_self_energy_table(disabled_b_path),
        parse_compact_self_energy_table(enabled_path),
    ]
    converted = [_table_metrics(records) for records in parsed]
    reference_indices = converted[0][0]
    for label, (indices, _) in zip(
        ("disabled_b", "enabled"), converted[1:], strict=True
    ):
        if indices != reference_indices:
            raise SameStateAnalysisError(f"compact EPW table index mismatch: {label}")
    return converted[0][1], converted[1][1], converted[2][1], len(reference_indices)


def _raw_diagnostics(raw_path: str | Path, contract: Mapping[str, Any]) -> dict[str, Any]:
    rows = parse_raw_rows(raw_path)
    selected_ik = int(contract["replay"]["enabled_environment"]["R02_EXPORT_IK_GLOBAL"])
    if {row.ik_global for row in rows} != {selected_ik}:
        raise SameStateAnalysisError("raw export contains an unauthorized global k-point")
    row_checks = _validate_row_identities(rows)
    diagonal = _summed_diagonal_and_covariance(rows)
    q_coverage = _q_coverage(rows)
    thresholds = contract["thresholds"]
    checks = {
        "normalization_identity": row_checks["normalization_identity_max_abs_ry2"]
        <= float(thresholds["normalization_identity_max_abs_ry2"]),
        "per_row_real_diagonal": row_checks["per_row_real_diagonal_max_abs_ev"]
        <= float(thresholds["per_state_real_diagonal_max_abs_ev"]),
        "summed_real_diagonal": diagonal["summed_real_diagonal_max_abs_ev"]
        <= float(thresholds["summed_real_diagonal_max_abs_ev"]),
        "synthetic_external_covariance": diagonal[
            "synthetic_external_covariance_max_abs_ev"
        ]
        <= float(thresholds["synthetic_external_covariance_max_abs_ev"]),
        "q_weight_sum": q_coverage["q_weight_sum_max_abs_from_one"]
        <= float(thresholds["q_weight_sum_max_abs"]),
        "imaginary_sign": row_checks["imaginary_sign_failure_count"] == 0,
        "acoustic_mask": row_checks["zero_mask_max_abs_ry2_or_ry"] <= 1.0e-15,
        "complete_four_band_blocks": diagonal["external_dimension"] == 4,
    }
    return {
        "passed": all(checks.values()),
        "row_count": len(rows),
        "row_diagnostics": row_checks,
        "diagonal_and_covariance": diagonal,
        "q_coverage": q_coverage,
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }


def _classify(
    state_integrity: Mapping[str, Any],
    attribution: Mapping[str, Any],
    raw: Mapping[str, Any],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if state_integrity.get("pre_manifests_identical") is not True:
        reasons.append("pre_replay_manifests_not_identical")
        return "STOP_HARNESS", reasons
    if state_integrity.get("required_paths_present") is not True:
        reasons.append("required_prepared_state_paths_missing")
        return "STOP_HARNESS", reasons

    comparisons = state_integrity.get("replay_comparisons")
    if not isinstance(comparisons, dict) or set(comparisons) != {
        "disabled_a",
        "disabled_b",
        "enabled",
    }:
        reasons.append("replay_integrity_evidence_incomplete")
        return "STOP_HARNESS", reasons

    mutated_or_deleted = {
        clone: {
            "mutated": list(value.get("mutated", [])),
            "deleted": list(value.get("deleted", [])),
        }
        for clone, value in comparisons.items()
        if value.get("mutated") or value.get("deleted")
    }
    if mutated_or_deleted:
        reasons.append("preexisting_state_changed")
        return "STOP_STATE_MUTATION", reasons

    unauthorized = {
        clone: list(value.get("unauthorized_new", []))
        for clone, value in comparisons.items()
        if value.get("unauthorized_new")
    }
    if unauthorized:
        reasons.append("undeclared_new_output")
        return "STOP_UNDECLARED_OUTPUT", reasons

    metrics = attribution.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        reasons.append("attribution_metrics_missing")
        return "STOP_HARNESS", reasons
    baseline_failed = [
        name for name, value in metrics.items() if value.get("baseline_passed") is not True
    ]
    if baseline_failed:
        reasons.extend(f"baseline_failed:{name}" for name in baseline_failed)
        return "STOP_BASELINE_REPRODUCIBILITY", reasons
    envelope_failed = [
        name
        for name, value in metrics.items()
        if value.get("enabled_envelope_passed") is not True
    ]
    if envelope_failed:
        reasons.extend(f"enabled_envelope_failed:{name}" for name in envelope_failed)
        return "STOP_EXPORTER_ATTRIBUTION", reasons
    if raw.get("passed") is not True:
        reasons.extend(f"raw_failed:{name}" for name in raw.get("failed_checks", []))
        return "STOP_RAW_DIAGNOSTIC", reasons
    return "RESTRICTED_GO_SAME_STATE_NONINTERFERENCE", reasons


def analyze(
    *,
    raw_path: str | Path,
    disabled_a_stdout: str | Path,
    disabled_b_stdout: str | Path,
    enabled_stdout: str | Path,
    state_integrity_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    contract = _load_json(contract_path)
    if contract.get("stage") != "B0_epw_same_state_attribution_execution":
        raise SameStateAnalysisError("unexpected execution contract stage")
    if contract.get("phase") != "one_pinned_execution":
        raise SameStateAnalysisError("same-state analyzer requires one_pinned_execution")
    if contract.get("issue") != 332:
        raise SameStateAnalysisError("unexpected execution issue")

    disabled_a, disabled_b, enabled, row_count = _load_three_tables(
        disabled_a_stdout, disabled_b_stdout, enabled_stdout
    )
    thresholds = contract["thresholds"]
    attribution = evaluate_attribution(
        disabled_a,
        disabled_b,
        enabled,
        floors={
            "energy_ev": float(thresholds["enabled_energy_floor_ev"]),
            "self_energy_ev": float(thresholds["enabled_self_energy_floor_ev"]),
            "dimensionless": float(thresholds["enabled_dimensionless_floor"]),
        },
        baseline_ceilings={
            "energy_ev": float(thresholds["baseline_energy_max_abs_ev"]),
            "self_energy_ev": float(thresholds["baseline_self_energy_max_abs_ev"]),
            "dimensionless": float(thresholds["baseline_dimensionless_max_abs"]),
        },
    )
    raw = _raw_diagnostics(raw_path, contract)
    state_integrity = _load_json(state_integrity_path)
    classification, reasons = _classify(state_integrity, attribution, raw)
    restricted_go = classification == "RESTRICTED_GO_SAME_STATE_NONINTERFERENCE"
    return {
        "schema_version": "1.0",
        "stage": "B0_epw_same_state_attribution_result",
        "status": "restricted_go" if restricted_go else "stop",
        "classification": classification,
        "reasons": reasons,
        "input_sha256": {
            "raw_vertex": _sha256(raw_path),
            "disabled_a_stdout": _sha256(disabled_a_stdout),
            "disabled_b_stdout": _sha256(disabled_b_stdout),
            "enabled_stdout": _sha256(enabled_stdout),
            "state_integrity": _sha256(state_integrity_path),
            "contract": _sha256(contract_path),
        },
        "standard_output_row_count": row_count,
        "state_integrity": state_integrity,
        "attribution": attribution,
        "raw_diagnostics": raw,
        "decision": {
            "restricted_go": restricted_go,
            "historical_issue_313_result_changed": False,
            "exporter_noninterference_established_for_pinned_same_state_fixture": restricted_go,
            "soc_spinor_compatibility_validated": False,
            "material_self_energy_validated": False,
            "automatic_followup_authorized": False,
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--disabled-a-stdout", required=True)
    parser.add_argument("--disabled-b-stdout", required=True)
    parser.add_argument("--enabled-stdout", required=True)
    parser.add_argument("--state-integrity", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    try:
        result = analyze(
            raw_path=args.raw,
            disabled_a_stdout=args.disabled_a_stdout,
            disabled_b_stdout=args.disabled_b_stdout,
            enabled_stdout=args.enabled_stdout,
            state_integrity_path=args.state_integrity,
            contract_path=args.contract,
        )
    except (RawVertexError, SameStateAnalysisError, ValueError, KeyError) as exc:
        result = {
            "schema_version": "1.0",
            "stage": "B0_epw_same_state_attribution_result",
            "status": "stop",
            "classification": "STOP_HARNESS",
            "reasons": [str(exc)],
            "decision": {
                "restricted_go": False,
                "historical_issue_313_result_changed": False,
                "automatic_followup_authorized": False,
            },
        }
    Path(args.output_json).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
