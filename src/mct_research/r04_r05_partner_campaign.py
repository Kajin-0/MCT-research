from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


CONTACT_READY_STATUS = "CONTACT_READY_NOT_SENT"
OUTREACH_STATUS = "OUTREACH_IN_PROGRESS"
INGESTION_STATUS = "GO_PARTNER_DATA_INGESTION"

_ALLOWED_MESSAGE_STATUSES = {
    "NOT_SENT",
    "ROUTE_UNRESOLVED_NOT_SENT",
    "SENT",
    "FOLLOW_UP_SENT",
    "CLOSED",
}

_REQUIRED_ROUTE_TYPES = {
    "AUTHOR_AND_SPECIMEN_GROUP",
    "USER_FACILITY_STM",
    "SPECIMEN_GROWTH_AND_LOCAL_METROLOGY",
    "ARCHIVED_STS_AUTHOR_ROUTING",
}


def _is_nonempty_sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and len(value) > 0


def _route_contacts(route: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    contacts: list[Mapping[str, Any]] = []
    primary_contacts = route.get("primary_contacts")
    if isinstance(primary_contacts, list):
        contacts.extend(item for item in primary_contacts if isinstance(item, Mapping))
    primary_contact = route.get("primary_contact")
    if isinstance(primary_contact, str):
        contacts.append({"name": primary_contact, "public_email": route.get("public_email")})
    return contacts


def validate_partner_campaign(record: Mapping[str, Any]) -> list[str]:
    """Return deterministic campaign-integrity errors without network access."""

    errors: list[str] = []

    if record.get("schema_version") != "r04_r05_partner_campaign_v1":
        errors.append("unexpected schema_version")
    if record.get("issue") != 398:
        errors.append("campaign must be controlled by issue 398")
    if record.get("predecessor_decision") != "PARTNER_DATA_REQUIRED":
        errors.append("campaign must inherit PARTNER_DATA_REQUIRED")
    if record.get("r05_material_activation") != "BLOCKED":
        errors.append("R05 material activation must remain blocked")

    status = record.get("campaign_status")
    routes = record.get("contact_routes")
    if not isinstance(routes, list) or not routes:
        errors.append("contact_routes must be a nonempty list")
        routes = []

    route_ids: set[str] = set()
    route_types: set[str] = set()
    sent_routes = 0
    commitment_routes = 0

    for index, route_raw in enumerate(routes):
        if not isinstance(route_raw, Mapping):
            errors.append(f"contact route {index} is not an object")
            continue
        route = route_raw
        route_id = route.get("id")
        if not isinstance(route_id, str) or not route_id:
            errors.append(f"contact route {index} has no id")
        elif route_id in route_ids:
            errors.append(f"duplicate route id: {route_id}")
        else:
            route_ids.add(route_id)

        route_type = route.get("route_type")
        if not isinstance(route_type, str):
            errors.append(f"route {route_id!r} has no route_type")
        else:
            route_types.add(route_type)

        sources = route.get("official_sources")
        if not _is_nonempty_sequence(sources):
            errors.append(f"route {route_id!r} lacks official sources")
        elif any(not isinstance(source, str) or not source.startswith("https://") for source in sources):
            errors.append(f"route {route_id!r} has a non-HTTPS source")

        if route.get("source_verified_date") != "2026-07-31":
            errors.append(f"route {route_id!r} has an unexpected source verification date")

        message_status = route.get("message_status")
        if message_status not in _ALLOWED_MESSAGE_STATUSES:
            errors.append(f"route {route_id!r} has invalid message_status")

        sent_at = route.get("sent_at")
        if message_status in {"SENT", "FOLLOW_UP_SENT", "CLOSED"}:
            sent_routes += 1
            if not isinstance(sent_at, str) or not sent_at:
                errors.append(f"route {route_id!r} is sent but lacks sent_at")
        elif sent_at is not None:
            errors.append(f"route {route_id!r} is unsent but has sent_at")

        outcome = route.get("outcome")
        commitment = route.get("evidence_commitment")
        if commitment is not None:
            commitment_routes += 1
            if outcome not in {"DATA_ARCHIVE_EXISTS", "NEW_MEASUREMENT_POSSIBLE"}:
                errors.append(f"route {route_id!r} has a commitment without a qualifying outcome")

        contacts = _route_contacts(route)
        if not contacts:
            errors.append(f"route {route_id!r} has no contact representation")

    missing_types = _REQUIRED_ROUTE_TYPES - route_types
    if missing_types:
        errors.append(f"missing required route types: {sorted(missing_types)!r}")

    if status == CONTACT_READY_STATUS:
        if record.get("sender_identity") != "UNSET":
            errors.append("contact-ready record must preserve sender_identity as UNSET")
        if record.get("outbound_contact_authorized") is not False:
            errors.append("contact-ready record must not authorize outbound contact")
        if record.get("data_ingestion_authorized") is not False:
            errors.append("contact-ready record must not authorize data ingestion")
        if sent_routes:
            errors.append("contact-ready record cannot contain sent routes")
        if commitment_routes:
            errors.append("contact-ready record cannot contain evidence commitments")
        for route in routes:
            if isinstance(route, Mapping) and route.get("outcome") is not None:
                errors.append("contact-ready record cannot contain outreach outcomes")
                break
    elif status == OUTREACH_STATUS:
        if record.get("sender_identity") in {None, "", "UNSET"}:
            errors.append("outreach requires a reviewed sender identity")
        if record.get("outbound_contact_authorized") is not True:
            errors.append("outreach status requires outbound_contact_authorized=true")
        if sent_routes == 0:
            errors.append("outreach status requires at least one sent route")
    elif status == INGESTION_STATUS:
        if record.get("data_ingestion_authorized") is not True:
            errors.append("ingestion status requires data_ingestion_authorized=true")
        if commitment_routes == 0:
            errors.append("ingestion status requires a concrete evidence commitment")
    else:
        errors.append("invalid campaign_status")

    follow_up = record.get("follow_up_protocol")
    if not isinstance(follow_up, Mapping):
        errors.append("follow_up_protocol must be an object")
    else:
        if follow_up.get("first_follow_up_days") != 7:
            errors.append("first follow-up must remain fixed at 7 days")
        if follow_up.get("closure_request_days") != 14:
            errors.append("closure request must remain fixed at 14 days")
        if follow_up.get("repeat_after_explicit_decline") is not False:
            errors.append("repeat solicitation after explicit decline is prohibited")

    unauthorized = record.get("unauthorized_work")
    if not _is_nonempty_sequence(unauthorized):
        errors.append("unauthorized_work must be declared")
    else:
        required_prohibitions = {
            "sending outreach before sender and recipient review",
            "recording a prepared message as sent",
            "recording facility capability as a measurement commitment",
            "data ingestion without a concrete archive or written commitment",
            "R05 reactivation",
            "larger random-mass simulation",
            "full 8-band spatial disorder",
            "manuscript drafting",
        }
        missing = required_prohibitions - set(unauthorized)
        if missing:
            errors.append(f"missing unauthorized-work safeguards: {sorted(missing)!r}")

    return errors


def campaign_is_contact_ready(record: Mapping[str, Any]) -> bool:
    return record.get("campaign_status") == CONTACT_READY_STATUS and not validate_partner_campaign(record)
