from __future__ import annotations

from collections.abc import Mapping, Sequence


REQUIRED_GATES = (
    "local_variance_gate",
    "correlation_length_gate",
    "same_population_gate",
    "near_critical_gate",
    "resolution_gate",
    "matched_null_gate",
    "robustness_gate",
    "decision_changing_gate",
)

ALLOWED_DECISIONS = {
    "PUBLIC_DATA_FEASIBLE",
    "PARTNER_DATA_REQUIRED",
    "EXTERNAL_DATA_BLOCKED",
}


def _is_sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def candidate_passes_all_gates(candidate: Mapping[str, object]) -> bool:
    gate_status = candidate.get("gate_status")
    if not isinstance(gate_status, Mapping):
        return False
    return all(gate_status.get(gate) == "PASS" for gate in REQUIRED_GATES)


def _has_partner_lead(candidates: Sequence[object]) -> bool:
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        qualification = str(candidate.get("qualification", ""))
        if any(
            token in qualification
            for token in (
                "PARTNER_LEAD",
                "AUTHOR_CONTACT_LEAD",
                "COMPOSITION_METHOD_LEAD",
                "GROWTH_PROCESS_LEAD",
            )
        ):
            return True
    return False


def validate_public_data_audit(record: Mapping[str, object]) -> list[str]:
    errors: list[str] = []

    if record.get("schema_version") != "r04_r05_public_data_audit_v1":
        errors.append("unexpected schema_version")

    decision = record.get("decision")
    if decision not in ALLOWED_DECISIONS:
        errors.append("decision is outside the PR2 vocabulary")

    gates = record.get("required_evidence_gates")
    if not _is_sequence(gates) or tuple(gates) != REQUIRED_GATES:
        errors.append("required evidence gates differ from the frozen PR1 order")

    candidates = record.get("candidate_records")
    if not _is_sequence(candidates) or not candidates:
        errors.append("candidate_records must be a nonempty sequence")
        candidates = []

    all_pass_candidates = [
        candidate
        for candidate in candidates
        if isinstance(candidate, Mapping) and candidate_passes_all_gates(candidate)
    ]

    qualifying_found = record.get("qualifying_complete_record_found")
    if bool(all_pass_candidates) != bool(qualifying_found):
        errors.append(
            "qualifying_complete_record_found disagrees with candidate gate states"
        )

    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            errors.append("candidate record is not an object")
            continue
        status = candidate.get("gate_status")
        if not isinstance(status, Mapping):
            errors.append(f"candidate {candidate.get('id')} lacks gate_status")
            continue
        missing = [gate for gate in REQUIRED_GATES if gate not in status]
        if missing:
            errors.append(
                f"candidate {candidate.get('id')} lacks gates: {', '.join(missing)}"
            )

    if record.get("r05_material_activation") != "BLOCKED":
        errors.append("PR2 cannot activate R05 material physics")

    unauthorized = record.get("unauthorized_work")
    if not _is_sequence(unauthorized):
        errors.append("unauthorized_work must be a sequence")
    else:
        required_prohibitions = {
            "R05 reactivation",
            "larger random-mass simulation",
            "full 8-band spatial disorder",
            "manuscript drafting",
        }
        if not required_prohibitions.issubset(set(unauthorized)):
            errors.append("PR2 stop-rule prohibitions are incomplete")

    if decision == "PUBLIC_DATA_FEASIBLE":
        if not all_pass_candidates:
            errors.append("PUBLIC_DATA_FEASIBLE requires an all-gates-pass record")

    if decision == "PARTNER_DATA_REQUIRED":
        if all_pass_candidates:
            errors.append("PARTNER_DATA_REQUIRED is inconsistent with a complete record")
        if not _has_partner_lead(candidates):
            errors.append("PARTNER_DATA_REQUIRED requires at least one plausible lead")
        requests = record.get("minimum_partner_requests")
        if not _is_sequence(requests) or len(requests) < 6:
            errors.append("partner request package is incomplete")
        logic = record.get("decision_logic")
        if not isinstance(logic, Mapping):
            errors.append("decision_logic is missing")
        else:
            for key in (
                "why_not_public_data_feasible",
                "why_not_external_data_blocked",
                "why_partner_data_required",
            ):
                if not logic.get(key):
                    errors.append(f"decision_logic lacks {key}")

    if decision == "EXTERNAL_DATA_BLOCKED" and _has_partner_lead(candidates):
        errors.append("EXTERNAL_DATA_BLOCKED conflicts with plausible partner leads")

    claim_boundary = record.get("claim_boundary")
    if not _is_sequence(claim_boundary) or not any(
        "not evidence that the physical effect is absent" in str(item)
        for item in claim_boundary
    ):
        errors.append("negative public-data result lacks the required claim boundary")

    return errors
