from __future__ import annotations

import copy
import json
from pathlib import Path

from mct_research.r04_r05_partner_campaign import (
    CONTACT_READY_STATUS,
    INGESTION_STATUS,
    OUTREACH_STATUS,
    campaign_is_contact_ready,
    validate_partner_campaign,
)


def _record() -> dict[str, object]:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "validation"
        / "r04_r05_partner_campaign.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_partner_campaign_is_valid_and_contact_ready() -> None:
    record = _record()
    assert validate_partner_campaign(record) == []
    assert campaign_is_contact_ready(record)
    assert record["campaign_status"] == CONTACT_READY_STATUS


def test_contact_ready_does_not_claim_outreach_or_data_access() -> None:
    record = _record()
    assert record["sender_identity"] == "UNSET"
    assert record["outbound_contact_authorized"] is False
    assert record["data_ingestion_authorized"] is False
    for route in record["contact_routes"]:
        assert route["message_status"] in {"NOT_SENT", "ROUTE_UNRESOLVED_NOT_SENT"}
        assert route["sent_at"] is None
        assert route["outcome"] is None
        assert route["evidence_commitment"] is None


def test_current_official_routes_cover_specimen_stm_metrology_and_archive() -> None:
    record = _record()
    route_types = {route["route_type"] for route in record["contact_routes"]}
    assert {
        "AUTHOR_AND_SPECIMEN_GROUP",
        "USER_FACILITY_STM",
        "SPECIMEN_GROWTH_AND_LOCAL_METROLOGY",
        "ARCHIVED_STS_AUTHOR_ROUTING",
    } <= route_types

    argonne = next(route for route in record["contact_routes"] if route["id"] == "argonne_cnm_stm")
    assert argonne["proposal_route"]["next_deadline"] == "2026-10-30T23:59:00-05:00"

    ornl = next(route for route in record["contact_routes"] if route["id"] == "ornl_cnms_stm")
    assert ornl["proposal_route"]["rapid_access"] == "OFF_CYCLE_POSSIBLE_FOR_LIMITED_PROOF_OF_CONCEPT"
    assert ornl["proposal_route"]["next_exact_deadline"] == "UNPOSTED_ON_AUDITED_PAGE_AS_OF_2026-07-31"


def test_prepared_packet_cannot_be_recorded_as_outreach() -> None:
    record = _record()
    modified = copy.deepcopy(record)
    modified["campaign_status"] = OUTREACH_STATUS
    assert "outreach requires a reviewed sender identity" in validate_partner_campaign(modified)
    assert "outreach status requires outbound_contact_authorized=true" in validate_partner_campaign(modified)
    assert "outreach status requires at least one sent route" in validate_partner_campaign(modified)


def test_ingestion_requires_a_real_commitment() -> None:
    record = _record()
    modified = copy.deepcopy(record)
    modified["campaign_status"] = INGESTION_STATUS
    assert "ingestion status requires data_ingestion_authorized=true" in validate_partner_campaign(modified)
    assert "ingestion status requires a concrete evidence commitment" in validate_partner_campaign(modified)


def test_facility_capability_is_not_misclassified_as_commitment() -> None:
    record = _record()
    facility_routes = [
        route
        for route in record["contact_routes"]
        if route["route_type"] == "USER_FACILITY_STM"
    ]
    assert len(facility_routes) == 2
    for route in facility_routes:
        assert route["evidence_commitment"] is None
        assert route["outcome"] is None


def test_stop_rules_remain_explicit() -> None:
    record = _record()
    unauthorized = set(record["unauthorized_work"])
    assert "recording a prepared message as sent" in unauthorized
    assert "recording facility capability as a measurement commitment" in unauthorized
    assert "data ingestion without a concrete archive or written commitment" in unauthorized
    assert "larger random-mass simulation" in unauthorized
    assert "full 8-band spatial disorder" in unauthorized
