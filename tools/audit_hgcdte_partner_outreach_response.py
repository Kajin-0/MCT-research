#!/usr/bin/env python3
"""Fail-closed audit for priority-partner outreach and response ingestion."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_CANDIDATES = (
    "uic_microphysics_laboratory",
    "national_maglab_ir_thz",
    "wsu_positron_annihilation_spectrometer",
    "ut_austin_epma",
    "utk_electromagnetic_properties_lab",
)

EXPECTED_ROLES = {
    "uic_microphysics_laboratory": ("material_provider",),
    "national_maglab_ir_thz": ("absorption_laboratory", "magneto_optical_laboratory"),
    "wsu_positron_annihilation_spectrometer": ("vacancy_metrology",),
    "ut_austin_epma": ("composition_thickness_metrology",),
    "utk_electromagnetic_properties_lab": ("hall_state_metrology",),
}

OUTREACH_STATES = (
    "not_prepared",
    "draft_ready",
    "approved_to_send",
    "sent",
    "acknowledged",
    "response_received",
    "closed_no_response",
    "closed_not_feasible",
)
RESPONSE_STATES = (
    "unanswered",
    "unsupported_verbal",
    "written_conditional",
    "written_confirmed",
    "written_blocked",
)
RECOMMENDATIONS = ("unknown", "conditional", "confirmed", "blocked")

ROLE_REQUIRED_FIELDS = (
    "accountable_owner_id",
    "organization_id",
    "contact_id",
    "capability_evidence_ids",
    "geometry_limits_documented",
    "state_altering_steps_documented",
    "calibration_or_process_plan_id",
    "native_data_release",
    "processing_code_available",
    "covariance_available",
    "throughput_documented",
    "turnaround_documented",
    "shipping_storage_documented",
    "data_rights_status",
    "publication_rights_status",
    "cost_estimate_status",
)

ROLE_GATE_IDS = {
    "material_provider": (
        "two_composition_specimens_available",
        "no_irreversible_processing_between_modalities",
        "data_and_publication_rights_compatible",
    ),
    "composition_thickness_metrology": (
        "composition_sigma_x_capability_le_0p0015",
        "no_irreversible_processing_between_modalities",
        "native_data_and_sha256_release",
        "calibration_and_covariance_release",
        "technical_repeats_at_least_two",
        "data_and_publication_rights_compatible",
    ),
    "hall_state_metrology": (
        "sample_temperature_6K_and_300K",
        "temperature_uncertainty_within_protocol",
        "quantitative_carrier_state_with_uncertainty",
        "native_data_and_sha256_release",
        "calibration_and_covariance_release",
        "technical_repeats_at_least_two",
        "pre_post_state_drift_measurement",
        "data_and_publication_rights_compatible",
    ),
    "vacancy_metrology": (
        "sample_temperature_6K_and_300K",
        "temperature_uncertainty_within_protocol",
        "quantitative_vacancy_proxy_with_uncertainty",
        "native_data_and_sha256_release",
        "calibration_and_covariance_release",
        "technical_repeats_at_least_two",
        "pre_post_state_drift_measurement",
        "data_and_publication_rights_compatible",
    ),
    "absorption_laboratory": (
        "sample_temperature_6K_and_300K",
        "temperature_uncertainty_within_protocol",
        "co_registered_paired_area",
        "no_irreversible_processing_between_modalities",
        "native_data_and_sha256_release",
        "calibration_and_covariance_release",
        "technical_repeats_at_least_two",
        "data_and_publication_rights_compatible",
    ),
    "magneto_optical_laboratory": (
        "sample_temperature_6K_and_300K",
        "temperature_uncertainty_within_protocol",
        "co_registered_paired_area",
        "no_irreversible_processing_between_modalities",
        "native_data_and_sha256_release",
        "calibration_and_covariance_release",
        "technical_repeats_at_least_two",
        "data_and_publication_rights_compatible",
    ),
}

EXPECTED_STATIC_BOUNDARY = {
    "private_contact_details_committed": False,
    "candidate_endorsement_authorized": False,
    "role_or_gate_confirmation_authorized": False,
    "automatic_feasibility_mutation_authorized": False,
    "funding_or_publication_promised": False,
}


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include timezone")
    return parsed.astimezone(timezone.utc)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _contains_private_contact_details(value: Any) -> bool:
    if isinstance(value, dict):
        if any(key.lower() in {"email", "phone", "address"} for key in value):
            return True
        return any(_contains_private_contact_details(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_private_contact_details(item) for item in value)
    return isinstance(value, str) and "@" in value


def _events_by_type(candidate: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    events = candidate.get("event_log")
    if not isinstance(events, list) or not events:
        raise ValueError(f"event log missing for {candidate['candidate_id']}")
    grouped: dict[str, list[dict[str, Any]]] = {}
    previous: datetime | None = None
    for event in events:
        event_type = event.get("event_type")
        if not _nonempty(event_type) or not _nonempty(event.get("evidence_id")):
            raise ValueError(f"invalid event for {candidate['candidate_id']}")
        timestamp = _parse_timestamp(event.get("timestamp"), "event timestamp")
        if previous is not None and timestamp < previous:
            raise ValueError(f"event chronology changed for {candidate['candidate_id']}")
        previous = timestamp
        external = event.get("external_message")
        if not isinstance(external, bool):
            raise ValueError(f"external-message flag missing for {candidate['candidate_id']}")
        grouped.setdefault(event_type, []).append(event)
    return grouped


def _validate_outreach(candidate: dict[str, Any]) -> tuple[bool, bool, bool]:
    state = candidate.get("outreach_state")
    if state not in OUTREACH_STATES:
        raise ValueError(f"invalid outreach state for {candidate['candidate_id']}")
    events = _events_by_type(candidate)
    if state != "not_prepared" and "draft_prepared" not in events:
        raise ValueError(f"draft evidence missing for {candidate['candidate_id']}")

    approved = state in OUTREACH_STATES[2:]
    sent = state in OUTREACH_STATES[3:]
    responded = state in {"response_received", "closed_not_feasible"}

    if approved:
        if not _nonempty(candidate.get("approval_evidence_id")):
            raise ValueError(f"approval evidence missing for {candidate['candidate_id']}")
        approval_events = events.get("approved_to_send", [])
        if not approval_events or any(event["external_message"] for event in approval_events):
            raise ValueError(f"approval event missing or invalid for {candidate['candidate_id']}")
        if not _nonempty(candidate.get("recipient_public_contact_id")):
            raise ValueError(f"recipient identifier missing for {candidate['candidate_id']}")
    else:
        if candidate.get("approval_evidence_id") is not None:
            raise ValueError(f"unapproved draft carries approval evidence for {candidate['candidate_id']}")

    if sent:
        if not _nonempty(candidate.get("external_message_evidence_id")):
            raise ValueError(f"sent message evidence missing for {candidate['candidate_id']}")
        sent_events = events.get("sent", [])
        if not sent_events or not all(event["external_message"] for event in sent_events):
            raise ValueError(f"external sent event missing for {candidate['candidate_id']}")
    else:
        if candidate.get("external_message_evidence_id") is not None:
            raise ValueError(f"unsent draft carries message evidence for {candidate['candidate_id']}")
        if any(event["external_message"] for event_list in events.values() for event in event_list):
            raise ValueError(f"unsent draft claims external activity for {candidate['candidate_id']}")

    if responded and not sent:
        raise ValueError(f"response cannot precede outreach for {candidate['candidate_id']}")
    return approved, sent, responded


def _required_gate_ids(role_ids: tuple[str, ...]) -> set[str]:
    required: set[str] = set()
    for role_id in role_ids:
        required.update(ROLE_GATE_IDS[role_id])
    return required


def _validate_role_assessment(assessment: dict[str, Any], candidate_roles: set[str]) -> str:
    role_id = assessment.get("role_id")
    if role_id not in candidate_roles:
        raise ValueError(f"response contains non-candidate role {role_id}")
    recommendation = assessment.get("recommendation")
    if recommendation not in RECOMMENDATIONS:
        raise ValueError(f"invalid role recommendation for {role_id}")
    evidence = assessment.get("evidence_ids")
    if not isinstance(evidence, list):
        raise ValueError(f"role evidence must be a list for {role_id}")
    assumptions = assessment.get("unresolved_assumptions")
    if not isinstance(assumptions, list):
        raise ValueError(f"role assumptions must be a list for {role_id}")
    if recommendation == "conditional":
        if not evidence or not assumptions:
            raise ValueError(f"conditional role lacks evidence or assumptions for {role_id}")
    if recommendation == "confirmed":
        if assumptions:
            raise ValueError(f"confirmed role retains assumptions for {role_id}")
        if not evidence:
            raise ValueError(f"confirmed role lacks evidence for {role_id}")
        for field in ROLE_REQUIRED_FIELDS:
            value = assessment.get(field)
            if field in {
                "geometry_limits_documented",
                "state_altering_steps_documented",
                "throughput_documented",
                "turnaround_documented",
                "shipping_storage_documented",
            }:
                if value is not True:
                    raise ValueError(f"confirmed role missing {field} for {role_id}")
            elif field == "capability_evidence_ids":
                if not isinstance(value, list) or not value:
                    raise ValueError(f"confirmed role missing {field} for {role_id}")
            elif not _nonempty(value):
                raise ValueError(f"confirmed role missing {field} for {role_id}")
    if recommendation == "blocked" and not evidence:
        raise ValueError(f"blocked role lacks evidence for {role_id}")
    return recommendation


def _validate_response(candidate: dict[str, Any], sent: bool) -> tuple[int, int, int]:
    response = candidate.get("response")
    if not isinstance(response, dict):
        raise ValueError(f"response record missing for {candidate['candidate_id']}")
    state = response.get("state")
    if state not in RESPONSE_STATES:
        raise ValueError(f"invalid response state for {candidate['candidate_id']}")
    evidence = response.get("evidence_ids")
    role_assessments = response.get("role_assessments")
    gate_assessments = response.get("gate_assessments")
    assumptions = response.get("unresolved_assumptions")
    if not all(isinstance(value, list) for value in (evidence, role_assessments, gate_assessments, assumptions)):
        raise ValueError(f"response list fields invalid for {candidate['candidate_id']}")

    if state == "unanswered":
        if any((response.get("received_at") is not None, evidence, role_assessments, gate_assessments)):
            raise ValueError(f"unanswered response contains evidence for {candidate['candidate_id']}")
        return 0, 0, 0
    if not sent:
        raise ValueError(f"response evidence exists before sent outreach for {candidate['candidate_id']}")
    _parse_timestamp(response.get("received_at"), "response timestamp")
    if not evidence:
        raise ValueError(f"response evidence missing for {candidate['candidate_id']}")

    if state == "unsupported_verbal":
        if role_assessments or gate_assessments:
            raise ValueError(f"verbal response cannot support recommendations for {candidate['candidate_id']}")
        return 1, 0, 0
    if not _nonempty(response.get("accountable_contact_id")):
        raise ValueError(f"written response lacks accountable contact for {candidate['candidate_id']}")

    candidate_roles = set(candidate["role_ids"])
    observed_roles: set[str] = set()
    conditional_count = 0
    confirmed_count = 0
    for assessment in role_assessments:
        recommendation = _validate_role_assessment(assessment, candidate_roles)
        role_id = assessment["role_id"]
        if role_id in observed_roles:
            raise ValueError(f"duplicate role assessment for {role_id}")
        observed_roles.add(role_id)
        conditional_count += recommendation == "conditional"
        confirmed_count += recommendation == "confirmed"

    gate_map: dict[str, dict[str, Any]] = {}
    for assessment in gate_assessments:
        gate_id = assessment.get("gate_id")
        recommendation = assessment.get("recommendation")
        gate_evidence = assessment.get("evidence_ids")
        if not _nonempty(gate_id) or recommendation not in RECOMMENDATIONS:
            raise ValueError(f"invalid gate assessment for {candidate['candidate_id']}")
        if gate_id in gate_map:
            raise ValueError(f"duplicate gate assessment {gate_id}")
        if not isinstance(gate_evidence, list):
            raise ValueError(f"gate evidence must be a list for {gate_id}")
        if recommendation in {"conditional", "confirmed", "blocked"} and not gate_evidence:
            raise ValueError(f"gate recommendation lacks evidence for {gate_id}")
        gate_map[gate_id] = assessment

    if state == "written_conditional":
        if not assumptions or not role_assessments:
            raise ValueError(f"conditional response lacks assumptions or role assessment")
        if confirmed_count:
            raise ValueError("conditional response cannot contain confirmed role recommendation")
    elif state == "written_blocked":
        if not role_assessments or not all(
            assessment.get("recommendation") == "blocked" for assessment in role_assessments
        ):
            raise ValueError("blocked response requires blocked role assessments")
    elif state == "written_confirmed":
        if assumptions or response.get("unresolved_assumptions"):
            raise ValueError("confirmed response retains unresolved assumptions")
        if observed_roles != candidate_roles or confirmed_count != len(candidate_roles):
            raise ValueError("confirmed response lacks all candidate role confirmations")
        required_gates = _required_gate_ids(tuple(candidate["role_ids"]))
        if set(gate_map) != required_gates:
            raise ValueError("confirmed response lacks complete applicable gate inventory")
        if any(item.get("recommendation") != "confirmed" for item in gate_map.values()):
            raise ValueError("confirmed response contains non-confirmed gate")

    return 1, conditional_count, confirmed_count


def audit(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported outreach-response schema")
    if data.get("package_id") != "hgcdte_paired_gap_priority_outreach_v1":
        raise ValueError("outreach package identity changed")
    if data.get("parent_landscape_id") != "hgcdte_paired_gap_public_candidates_2026-07-20":
        raise ValueError("candidate-landscape lineage changed")
    if data.get("parent_feasibility_id") != "hgcdte_paired_gap_feasibility_v1":
        raise ValueError("feasibility lineage changed")
    if data.get("controlling_issue") != 165:
        raise ValueError("controlling issue changed")
    if data.get("package_status") not in {"drafts_ready_no_contact", "outreach_in_progress"}:
        raise ValueError("invalid package status")
    boundary = data.get("claim_boundary")
    if not isinstance(boundary, dict):
        raise ValueError("outreach claim boundary missing")
    static_boundary = {
        key: boundary.get(key) for key in EXPECTED_STATIC_BOUNDARY
    }
    if static_boundary != EXPECTED_STATIC_BOUNDARY:
        raise ValueError("outreach claim boundary changed")
    if not isinstance(boundary.get("messages_sent"), bool):
        raise ValueError("messages-sent status must be boolean")
    if not isinstance(boundary.get("direct_outreach_performed"), bool):
        raise ValueError("direct-outreach status must be boolean")
    if tuple(data.get("allowed_outreach_states", [])) != OUTREACH_STATES:
        raise ValueError("outreach-state vocabulary changed")
    if tuple(data.get("allowed_response_states", [])) != RESPONSE_STATES:
        raise ValueError("response-state vocabulary changed")
    if tuple(data.get("allowed_recommendations", [])) != RECOMMENDATIONS:
        raise ValueError("recommendation vocabulary changed")
    if _contains_private_contact_details(data):
        raise ValueError("private contact details are not permitted in the template")

    candidates = data.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != len(EXPECTED_CANDIDATES):
        raise ValueError("priority candidate inventory changed")
    if tuple(candidate.get("candidate_id") for candidate in candidates) != EXPECTED_CANDIDATES:
        raise ValueError("priority candidate order or identity changed")

    state_counts = {state: 0 for state in OUTREACH_STATES}
    approved_count = 0
    sent_count = 0
    response_count = 0
    conditional_recommendation_count = 0
    confirmed_recommendation_count = 0
    for expected_priority, candidate in enumerate(candidates, start=1):
        candidate_id = candidate["candidate_id"]
        if candidate.get("priority") != expected_priority:
            raise ValueError("candidate priority changed")
        if tuple(candidate.get("role_ids", [])) != EXPECTED_ROLES[candidate_id]:
            raise ValueError(f"candidate role assignment changed for {candidate_id}")
        if not _nonempty(candidate.get("draft_section_id")):
            raise ValueError(f"draft section missing for {candidate_id}")
        approved, sent, _ = _validate_outreach(candidate)
        responses, conditional, confirmed = _validate_response(candidate, sent)
        state_counts[candidate["outreach_state"]] += 1
        approved_count += approved
        sent_count += sent
        response_count += responses
        conditional_recommendation_count += conditional
        confirmed_recommendation_count += confirmed

    if boundary["messages_sent"] is not (sent_count > 0):
        raise ValueError("messages-sent status disagrees with event evidence")
    if boundary["direct_outreach_performed"] is not (sent_count > 0):
        raise ValueError("direct-outreach status disagrees with event evidence")

    initial_state = sent_count == 0 and response_count == 0
    if data["package_status"] == "drafts_ready_no_contact":
        if state_counts["draft_ready"] != len(EXPECTED_CANDIDATES) or not initial_state:
            raise ValueError("drafts-ready package claims contact or incomplete drafts")

    contract = data.get("assessment_contract")
    if not isinstance(contract, dict) or contract.get("feasibility_update_requires_separate_review") is not True:
        raise ValueError("separate feasibility-review boundary changed")

    return {
        "schema_version": data["schema_version"],
        "package_id": data["package_id"],
        "candidate_count": len(candidates),
        "draft_ready_count": state_counts["draft_ready"],
        "approved_to_send_or_later_count": approved_count,
        "sent_or_later_count": sent_count,
        "response_record_count": response_count,
        "conditional_role_recommendation_count": conditional_recommendation_count,
        "confirmed_role_recommendation_count": confirmed_recommendation_count,
        "external_messages_sent": sent_count > 0,
        "direct_outreach_performed": sent_count > 0,
        "automatic_feasibility_mutation_authorized": False,
        "feasibility_update_requires_separate_review": True,
        "next_action": "review_sender_identity_recipients_and_drafts_before_any_send",
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
