#!/usr/bin/env python3
"""Fail-closed readiness audit for the paired HgCdTe collaboration package."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROLE_IDS = (
    "material_provider",
    "composition_thickness_metrology",
    "hall_state_metrology",
    "vacancy_metrology",
    "absorption_laboratory",
    "magneto_optical_laboratory",
    "analysis_owner",
    "data_archive_owner",
)

PILOT_GATE_IDS = (
    "two_composition_specimens_available",
    "composition_sigma_x_capability_le_0p0015",
    "sample_temperature_6K_and_300K",
    "temperature_uncertainty_within_protocol",
    "quantitative_carrier_state_with_uncertainty",
    "quantitative_vacancy_proxy_with_uncertainty",
    "co_registered_paired_area",
    "no_irreversible_processing_between_modalities",
    "native_data_and_sha256_release",
    "calibration_and_covariance_release",
    "technical_repeats_at_least_two",
    "pre_post_state_drift_measurement",
    "data_and_publication_rights_compatible",
)

ASSESSMENT_STATES = {"unknown", "conditional", "confirmed", "blocked"}
ROLE_DATA_STATES = {"unknown", "required", "confirmed", "not_applicable"}
RIGHTS_STATES = {"unknown", "compatible", "restricted_documented", "blocked"}
COST_STATES = {"unknown", "estimated", "quoted", "not_applicable", "blocked"}
READINESS_STATES = (
    "not_ready",
    "capability_review_complete",
    "logistics_pilot_ready",
    "logistics_pilot_complete",
    "prescreening_ready",
    "full_experiment_ready",
)


def _finite(value: Any, field: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{field} must be finite")
    return float(value)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _role_documented(role: dict[str, Any]) -> bool:
    core = (
        _nonempty(role.get("accountable_owner_id")),
        _nonempty(role.get("organization_id")),
        _nonempty(role.get("contact_id")),
        bool(role.get("capability_evidence_ids")),
        role.get("geometry_limits_documented") is True,
        role.get("state_altering_steps_documented") is True,
        _nonempty(role.get("calibration_or_process_plan_id")),
        role.get("throughput_documented") is True,
        role.get("turnaround_documented") is True,
        role.get("shipping_storage_documented") is True,
        role.get("data_rights_status") in RIGHTS_STATES - {"unknown"},
        role.get("publication_rights_status") in RIGHTS_STATES - {"unknown"},
        role.get("cost_estimate_status") in COST_STATES - {"unknown"},
    )
    return all(core)


def _validate_roles(roles: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(roles, list) or len(roles) != len(ROLE_IDS):
        raise ValueError("collaboration role inventory changed")
    observed = [role.get("role_id") for role in roles]
    if tuple(observed) != ROLE_IDS:
        raise ValueError("collaboration role order or identity changed")

    blockers: list[str] = []
    for role in roles:
        role_id = role["role_id"]
        state = role.get("status")
        if state not in ASSESSMENT_STATES:
            raise ValueError(f"invalid role status for {role_id}")
        for field in ("native_data_release", "processing_code_available", "covariance_available"):
            if role.get(field) not in ROLE_DATA_STATES:
                raise ValueError(f"invalid {field} state for {role_id}")
        if role.get("data_rights_status") not in RIGHTS_STATES:
            raise ValueError(f"invalid data-rights state for {role_id}")
        if role.get("publication_rights_status") not in RIGHTS_STATES:
            raise ValueError(f"invalid publication-rights state for {role_id}")
        if role.get("cost_estimate_status") not in COST_STATES:
            raise ValueError(f"invalid cost state for {role_id}")
        assumptions = role.get("blocking_assumptions")
        if not isinstance(assumptions, list):
            raise ValueError(f"blocking_assumptions must be a list for {role_id}")
        if state in {"conditional", "blocked"} and not assumptions:
            blockers.append(f"role:{role_id}:missing_blocking_assumption")
        if state == "confirmed":
            if not _role_documented(role):
                blockers.append(f"role:{role_id}:confirmed_without_complete_documentation")
            if assumptions:
                blockers.append(f"role:{role_id}:confirmed_with_unresolved_assumption")
    return roles, blockers


def _validate_gates(gates: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(gates, list) or len(gates) != len(PILOT_GATE_IDS):
        raise ValueError("pilot gate inventory changed")
    observed = [gate.get("gate_id") for gate in gates]
    if tuple(observed) != PILOT_GATE_IDS:
        raise ValueError("pilot gate order or identity changed")

    blockers: list[str] = []
    for gate in gates:
        gate_id = gate["gate_id"]
        state = gate.get("status")
        if state not in ASSESSMENT_STATES:
            raise ValueError(f"invalid gate status for {gate_id}")
        evidence = gate.get("evidence_ids")
        if not isinstance(evidence, list):
            raise ValueError(f"evidence_ids must be a list for {gate_id}")
        if state == "confirmed" and not evidence:
            blockers.append(f"gate:{gate_id}:confirmed_without_evidence")
        if state in {"conditional", "blocked"}:
            blockers.append(f"gate:{gate_id}:{state}")
    return gates, blockers


def _validate_fixed_design(data: dict[str, Any]) -> None:
    boundary = data.get("claim_boundary")
    if not isinstance(boundary, dict) or any(value is not False for value in boundary.values()):
        raise ValueError("logistics-pilot claim boundary was weakened")

    pilot = data["pilot_plan"]
    expected_pilot = {
        "specimen_count": 2,
        "composition_level_count": 2,
        "carrier_level_count": 1,
        "vacancy_level_count": 1,
        "modality_count": 2,
        "temperature_block_count": 2,
        "primary_observation_count": 8,
        "technical_replicate_hard_minimum": 2,
        "identifies_carrier_term": False,
        "identifies_vacancy_term": False,
        "status": "planned",
    }
    if pilot != expected_pilot:
        raise ValueError("logistics-pilot design or claim boundary changed")

    full = data["full_experiment_plan"]
    expected_full_fields = {
        "specimen_count": 8,
        "modality_count": 2,
        "temperature_block_count": 2,
        "primary_observation_count": 32,
        "technical_replicate_hard_minimum": 2,
    }
    if any(full.get(key) != value for key, value in expected_full_fields.items()):
        raise ValueError("full experiment design changed")
    if full.get("status") not in {"blocked_pending_prescreening", "ready"}:
        raise ValueError("invalid full experiment plan status")


def _pilot_execution_passes(execution: dict[str, Any]) -> bool:
    if execution.get("status") != "complete":
        return False
    numeric_checks = (
        execution.get("completed_specimen_count") == 2,
        execution.get("completed_primary_observation_count") == 8,
        isinstance(execution.get("minimum_technical_replicates"), int)
        and execution["minimum_technical_replicates"] >= 2,
    )
    boolean_checks = (
        execution.get("same_area_pairing_pass") is True,
        execution.get("temperature_gate_pass") is True,
        execution.get("native_data_transfer_pass") is True,
        execution.get("calibration_transfer_pass") is True,
        execution.get("pre_post_state_drift_pass") is True,
        execution.get("irreversible_processing_detected") is False,
        execution.get("failure_records") == [],
    )
    return all(numeric_checks + boolean_checks)


def _prescreening_plan_passes(plan: dict[str, Any]) -> bool:
    count = plan.get("candidate_pool_count")
    return all(
        (
            plan.get("documented") is True,
            isinstance(count, int) and count >= 8,
            plan.get("two_composition_levels") is True,
            plan.get("composition_carrier_vacancy_measured_before_selection") is True,
            plan.get("selection_algorithm_predeclared") is True,
            plan.get("same_polarity_requirement_declared") is True,
            plan.get("aliasing_gate_declared") is True,
        )
    )


def _prescreening_result_passes(result: dict[str, Any]) -> tuple[bool, list[str]]:
    blockers: list[str] = []
    if result.get("status") != "complete":
        return False, ["prescreening:not_complete"]
    if result.get("selected_core_specimen_count") != 8:
        blockers.append("prescreening:selected_core_count_not_8")
    sigma_x = result.get("maximum_composition_sigma_x")
    if not isinstance(sigma_x, (int, float)) or not math.isfinite(float(sigma_x)) or sigma_x > 0.0015:
        blockers.append("prescreening:composition_sigma_x_above_hard_maximum")
    for temperature in ("6K", "300K"):
        if result.get(f"same_carrier_polarity_at_{temperature}") is not True:
            blockers.append(f"prescreening:mixed_or_unknown_carrier_polarity_{temperature}")
        for factor in ("carrier", "vacancy"):
            value = result.get(f"{factor}_separation_sigma_{temperature}")
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)) or value < 3.0:
                blockers.append(f"prescreening:{factor}_separation_below_3sigma_{temperature}")
        corr = result.get(f"carrier_vacancy_correlation_{temperature}")
        if not isinstance(corr, (int, float)) or not math.isfinite(float(corr)) or abs(float(corr)) > 0.5:
            blockers.append(f"prescreening:carrier_vacancy_aliasing_{temperature}")
    if result.get("specimen_ids_frozen") is not True:
        blockers.append("prescreening:specimen_ids_not_frozen")
    if result.get("processing_histories_frozen") is not True:
        blockers.append("prescreening:processing_histories_not_frozen")
    return not blockers, blockers


def audit(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported feasibility schema")
    if data.get("feasibility_id") != "hgcdte_paired_gap_feasibility_v1":
        raise ValueError("feasibility identity changed")
    if data.get("parent_protocol_id") != "hgcdte_paired_gap_2x2x2_v1":
        raise ValueError("parent protocol identity changed")
    if data.get("controlling_issue") != 161:
        raise ValueError("controlling issue changed")
    if data.get("status") not in {"planning_template", "completed_review"}:
        raise ValueError("invalid package status")

    _validate_fixed_design(data)
    roles, role_blockers = _validate_roles(data.get("roles"))
    gates, gate_blockers = _validate_gates(data.get("pilot_gates"))

    documented_roles = sum(_role_documented(role) for role in roles)
    unknown_roles = sum(role["status"] == "unknown" for role in roles)
    conditional_roles = sum(role["status"] == "conditional" for role in roles)
    confirmed_roles = sum(role["status"] == "confirmed" for role in roles)
    blocked_roles = sum(role["status"] == "blocked" for role in roles)
    unknown_gates = sum(gate["status"] == "unknown" for gate in gates)
    confirmed_gates = sum(gate["status"] == "confirmed" for gate in gates)

    review_complete = (
        unknown_roles == 0
        and unknown_gates == 0
        and documented_roles == len(ROLE_IDS)
        and not any("missing_blocking_assumption" in item for item in role_blockers)
    )
    pilot_ready = (
        review_complete
        and confirmed_roles == len(ROLE_IDS)
        and confirmed_gates == len(PILOT_GATE_IDS)
        and not role_blockers
        and not gate_blockers
    )
    pilot_complete = pilot_ready and _pilot_execution_passes(data["pilot_execution"])
    prescreening_ready = pilot_complete and _prescreening_plan_passes(data["prescreening_plan"])
    prescreening_pass, prescreening_blockers = _prescreening_result_passes(
        data["prescreening_result"]
    )
    full_ready = (
        prescreening_ready
        and prescreening_pass
        and data["full_experiment_plan"].get("status") == "ready"
    )

    if full_ready:
        readiness = "full_experiment_ready"
    elif prescreening_ready:
        readiness = "prescreening_ready"
    elif pilot_complete:
        readiness = "logistics_pilot_complete"
    elif pilot_ready:
        readiness = "logistics_pilot_ready"
    elif review_complete:
        readiness = "capability_review_complete"
    else:
        readiness = "not_ready"

    blockers = list(role_blockers) + list(gate_blockers)
    if not review_complete:
        blockers.append("capability_review:incomplete")
    if pilot_ready and not pilot_complete:
        blockers.append("logistics_pilot:not_complete")
    if pilot_complete and not _prescreening_plan_passes(data["prescreening_plan"]):
        blockers.append("prescreening:plan_not_ready")
    if prescreening_ready and not prescreening_pass:
        blockers.extend(prescreening_blockers)
    if (
        prescreening_ready
        and prescreening_pass
        and data["full_experiment_plan"].get("status") != "ready"
    ):
        blockers.append("full_experiment:plan_not_promoted")

    return {
        "schema_version": data["schema_version"],
        "feasibility_id": data["feasibility_id"],
        "readiness_status": readiness,
        "role_count": len(roles),
        "documented_role_count": documented_roles,
        "unknown_role_count": unknown_roles,
        "conditional_role_count": conditional_roles,
        "confirmed_role_count": confirmed_roles,
        "blocked_role_count": blocked_roles,
        "pilot_gate_count": len(gates),
        "unknown_pilot_gate_count": unknown_gates,
        "confirmed_pilot_gate_count": confirmed_gates,
        "capability_review_complete": review_complete,
        "logistics_pilot_ready": pilot_ready,
        "logistics_pilot_complete": pilot_complete,
        "prescreening_ready": prescreening_ready,
        "full_experiment_ready": full_ready,
        "pilot_primary_observation_count": data["pilot_plan"]["primary_observation_count"],
        "full_primary_observation_count": data["full_experiment_plan"]["primary_observation_count"],
        "pilot_identifies_carrier_term": data["pilot_plan"]["identifies_carrier_term"],
        "pilot_identifies_vacancy_term": data["pilot_plan"]["identifies_vacancy_term"],
        "blockers": sorted(set(blockers)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        Path(args.output_json).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
