#!/usr/bin/env python3
"""Fail-closed audit for the public HgCdTe candidate-facility landscape."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

EXPECTED_CANDIDATES = (
    "uic_microphysics_laboratory",
    "ut_austin_epma",
    "utk_electromagnetic_properties_lab",
    "uic_ppms",
    "wsu_positron_annihilation_spectrometer",
    "ncsu_positron_user_facility",
    "national_maglab_ir_thz",
    "zenodo_archive_infrastructure",
)

EXPECTED_ROLES = (
    "material_provider",
    "composition_thickness_metrology",
    "hall_state_metrology",
    "vacancy_metrology",
    "absorption_laboratory",
    "magneto_optical_laboratory",
    "data_archive_infrastructure",
)

OFFICIAL_DOMAINS = {
    "phys.uic.edu",
    "www.jsg.utexas.edu",
    "research.utk.edu",
    "materialsresearch.wsu.edu",
    "nrp.ne.ncsu.edu",
    "nationalmaglab.org",
    "zenodo.org",
    "help.zenodo.org",
    "about.zenodo.org",
}

EXPECTED_DECISION = {
    "public_candidate_landscape_authorized": True,
    "candidate_endorsement_authorized": False,
    "role_confirmation_authorized": False,
    "gate_confirmation_authorized": False,
    "feasibility_readiness_promotion_authorized": False,
    "direct_outreach_performed": False,
    "next_action": "documented_candidate_outreach",
}


def _require_nonempty_list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty list")
    return value


def audit(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported candidate-landscape schema")
    if data.get("landscape_id") != "hgcdte_paired_gap_public_candidates_2026-07-20":
        raise ValueError("candidate-landscape identity changed")
    if data.get("parent_feasibility_id") != "hgcdte_paired_gap_feasibility_v1":
        raise ValueError("parent feasibility identity changed")
    if data.get("controlling_issue") != 163:
        raise ValueError("controlling issue changed")
    access_date = date.fromisoformat(data["evidence_access_date"])
    if access_date != date(2026, 7, 20):
        raise ValueError("evidence access date changed")
    if data.get("evidence_scope") != "official_public_webpages_only":
        raise ValueError("evidence scope changed")

    boundary = data.get("status_boundary")
    expected_boundary = {
        "candidate_status": "public_evidence_only",
        "confirmed_role_count": 0,
        "confirmed_gate_count": 0,
        "direct_contact_performed": False,
        "access_assumed": False,
        "endorsement_claimed": False,
        "hard_uncertainty_gate_inferred": False,
        "feasibility_template_modified": False,
    }
    if boundary != expected_boundary:
        raise ValueError("public-evidence status boundary changed")

    if tuple(data.get("target_roles", [])) != EXPECTED_ROLES:
        raise ValueError("target-role inventory changed")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != len(EXPECTED_CANDIDATES):
        raise ValueError("candidate inventory changed")
    if tuple(candidate.get("candidate_id") for candidate in candidates) != EXPECTED_CANDIDATES:
        raise ValueError("candidate order or identity changed")

    source_count = 0
    role_candidates: dict[str, set[str]] = {role: set() for role in EXPECTED_ROLES}
    priority_counts = {1: 0, 2: 0}
    all_blockers: list[str] = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        if candidate.get("candidate_status") != "public_evidence_only":
            raise ValueError(f"{candidate_id} was promoted beyond public evidence")
        priority = candidate.get("priority")
        if priority not in priority_counts:
            raise ValueError(f"invalid priority for {candidate_id}")
        priority_counts[priority] += 1
        roles = _require_nonempty_list(candidate.get("candidate_roles"), f"{candidate_id} roles")
        for role in roles:
            if role not in role_candidates:
                raise ValueError(f"unknown role {role} for {candidate_id}")
            role_candidates[role].add(candidate_id)
        sources = _require_nonempty_list(candidate.get("official_sources"), f"{candidate_id} sources")
        source_count += len(sources)
        for source in sources:
            source_id = source.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                raise ValueError(f"missing source ID for {candidate_id}")
            url = source.get("url")
            parsed = urlparse(url) if isinstance(url, str) else None
            if parsed is None or parsed.scheme != "https" or parsed.netloc not in OFFICIAL_DOMAINS:
                raise ValueError(f"non-official or non-HTTPS source for {candidate_id}")
            if source.get("accessed") != "2026-07-20":
                raise ValueError(f"source access date changed for {candidate_id}")
            _require_nonempty_list(source.get("public_claims"), f"{source_id} public claims")
        _require_nonempty_list(
            candidate.get("publicly_supported_capabilities"),
            f"{candidate_id} public capabilities",
        )
        blockers = _require_nonempty_list(
            candidate.get("unresolved_hard_gates"),
            f"{candidate_id} unresolved gates",
        )
        all_blockers.extend(f"{candidate_id}:{blocker}" for blocker in blockers)
        if candidate.get("readiness_effect") != "none":
            raise ValueError(f"public evidence changed readiness for {candidate_id}")
        if not isinstance(candidate.get("contact_action"), str) or not candidate["contact_action"].strip():
            raise ValueError(f"missing contact action for {candidate_id}")

    uncovered_roles = [role for role, ids in role_candidates.items() if not ids]
    if uncovered_roles:
        raise ValueError(f"uncovered target roles: {uncovered_roles}")

    coverage = data.get("role_coverage")
    if not isinstance(coverage, dict) or tuple(coverage) != EXPECTED_ROLES:
        raise ValueError("role-coverage map changed")
    for role in EXPECTED_ROLES:
        if set(coverage[role]) != role_candidates[role]:
            raise ValueError(f"role coverage disagrees with candidate records for {role}")

    sequence = data.get("recommended_contact_sequence")
    if not isinstance(sequence, list) or len(sequence) != len(EXPECTED_CANDIDATES):
        raise ValueError("contact sequence changed")
    if set(sequence) != set(EXPECTED_CANDIDATES):
        raise ValueError("contact sequence does not cover all candidates")
    if sequence[:5] != [
        "uic_microphysics_laboratory",
        "national_maglab_ir_thz",
        "wsu_positron_annihilation_spectrometer",
        "ut_austin_epma",
        "utk_electromagnetic_properties_lab",
    ]:
        raise ValueError("primary contact priority changed")

    controlling_blockers = _require_nonempty_list(
        data.get("controlling_blockers"), "controlling blockers"
    )
    if len(controlling_blockers) != 6:
        raise ValueError("controlling blocker inventory changed")
    if data.get("decision") != EXPECTED_DECISION:
        raise ValueError("candidate-landscape decision changed")

    maglab = next(
        candidate for candidate in candidates if candidate["candidate_id"] == "national_maglab_ir_thz"
    )
    deadline = date.fromisoformat(
        maglab["time_sensitive_public_information"]["next_listed_proposal_deadline"]
    )
    days_to_deadline = (deadline - access_date).days
    if days_to_deadline != 116:
        raise ValueError("MagLab deadline interval changed")

    return {
        "schema_version": data["schema_version"],
        "landscape_id": data["landscape_id"],
        "candidate_count": len(candidates),
        "priority_1_candidate_count": priority_counts[1],
        "priority_2_candidate_count": priority_counts[2],
        "official_source_count": source_count,
        "target_role_count": len(EXPECTED_ROLES),
        "covered_role_count": len(EXPECTED_ROLES) - len(uncovered_roles),
        "candidate_role_assignments": sum(len(ids) for ids in role_candidates.values()),
        "unresolved_candidate_gate_count": len(all_blockers),
        "confirmed_role_count": boundary["confirmed_role_count"],
        "confirmed_gate_count": boundary["confirmed_gate_count"],
        "feasibility_readiness_promoted": False,
        "next_maglab_deadline": deadline.isoformat(),
        "days_from_evidence_date_to_maglab_deadline": days_to_deadline,
        "recommended_first_contact_ids": sequence[:5],
        "controlling_blocker_count": len(controlling_blockers),
        "decision": data["decision"],
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
