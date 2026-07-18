#!/usr/bin/env python3
"""Audit candidate SOC finite-temperature matrix backends fail-closed."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

VALID_STATUS = {"pass", "fail", "unverified", "partial", "not_applicable"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("backend contract must be a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("stage") != "soc_finite_temperature_matrix_backend_gate":
        raise ValueError("unexpected backend audit stage")
    routes = contract.get("routes")
    hard_gates = contract.get("hard_gates_for_direct_A1")
    if not isinstance(routes, dict) or not routes:
        raise ValueError("contract must define candidate routes")
    if not isinstance(hard_gates, list) or not hard_gates:
        raise ValueError("contract must define hard gates")

    route_results: dict[str, Any] = {}
    direct_candidates: list[str] = []
    ranked: list[tuple[int, int, str]] = []

    for route_name, route in routes.items():
        capabilities = route.get("capabilities")
        if not isinstance(capabilities, dict):
            raise ValueError(f"{route_name} lacks capabilities")
        unknown = set(capabilities.values()) - VALID_STATUS
        if unknown:
            raise ValueError(f"{route_name} uses invalid statuses: {sorted(unknown)}")
        missing = [gate for gate in hard_gates if gate not in capabilities]
        if missing:
            raise ValueError(f"{route_name} lacks hard-gate fields: {missing}")

        hard_status = {gate: capabilities[gate] for gate in hard_gates}
        passed_hard = [gate for gate, status in hard_status.items() if status == "pass"]
        failed_hard = [gate for gate, status in hard_status.items() if status == "fail"]
        unresolved_hard = [
            gate
            for gate, status in hard_status.items()
            if status in {"unverified", "partial", "not_applicable"}
        ]
        direct_ready = len(passed_hard) == len(hard_gates)
        if route.get("execution_authorized") is not False:
            raise ValueError(f"{route_name} must remain execution-blocked")
        if direct_ready:
            direct_candidates.append(route_name)

        score = len(passed_hard)
        penalty = 3 * len(failed_hard) + len(unresolved_hard)
        ranked.append((score, -penalty, route_name))
        route_results[route_name] = {
            "hard_gate_status": hard_status,
            "passed_hard_gates": passed_hard,
            "failed_hard_gates": failed_hard,
            "unresolved_hard_gates": unresolved_hard,
            "direct_A1_ready": direct_ready,
            "pass_count": sum(status == "pass" for status in capabilities.values()),
            "fail_count": sum(status == "fail" for status in capabilities.values()),
            "unverified_or_partial_count": sum(
                status in {"unverified", "partial"} for status in capabilities.values()
            ),
            "blockers": route.get("blockers", []),
        }

    ranked_names = [entry[2] for entry in sorted(ranked, reverse=True)]
    policy = contract["selection_policy"]
    preferred = str(policy["preferred_next_design"])
    secondary = str(policy["secondary_design"])
    if preferred != "zg_selected_band_matrix_reconstruction_oracle":
        raise ValueError("unexpected preferred next design")
    if secondary != "qe_ahc_nonmagnetic_soc_capability_test":
        raise ValueError("unexpected secondary design")
    if direct_candidates:
        raise RuntimeError(
            "contract unexpectedly identifies direct A1 backends: "
            + ", ".join(direct_candidates)
        )

    return {
        "schema_version": "1.0",
        "status": "soc_finite_temperature_backend_audit_completed",
        "hard_gates": hard_gates,
        "route_results": route_results,
        "ranking_by_documented_hard_gate_coverage": ranked_names,
        "decision": {
            "direct_A1_backend_selected": False,
            "direct_A1_backend_candidates": [],
            "no_existing_route_closes_all_requirements": True,
            "preferred_next_design": preferred,
            "secondary_design": secondary,
            "zg_execution_authorized": False,
            "qe_ahc_execution_authorized": False,
            "epw_execution_authorized": False,
            "abinit_execution_authorized": False,
            "custom_debye_waller_implementation_authorized": False,
            "automatic_additional_compute_authorized": False,
            "interpretation": (
                "No documented backend closes SOC, off-diagonal eight-band matrices, "
                "complete thermal renormalization, polar long-range control, gauge handling, "
                "and held-out validation. Design a synthetic ZG selected-band matrix "
                "reconstruction oracle first; retain QE AHC SOC validation as a secondary path."
            ),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(
            "first_principles/decision_memos/soc_finite_temperature_backend_gate.json"
        ),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(load_json(args.contract))
    result["input_sha256"] = {"contract": sha256(args.contract)}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
