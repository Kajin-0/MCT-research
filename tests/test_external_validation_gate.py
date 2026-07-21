from __future__ import annotations

import json
from pathlib import Path

import pytest

from mct_research.validation_gate import (
    rank_validation_routes,
    score_validation_criteria,
    select_first_external_validation_route,
)
from tools.build_external_validation_gate import build_report

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT / "literature" / "acquisition" / "distributional_band_edge_sources.json"
)

EXPECTED_DOIS = {
    "10.1016/0038-1098(85)90315-1",
    "10.1007/s11664-007-0162-0",
    "10.1063/1.2245220",
    "10.1016/0022-0248(92)90851-9",
    "10.1016/j.physb.2009.08.210",
    "10.1038/ncomms12576",
    "10.1016/0020-0891(91)90110-2",
    "10.1063/1.333828",
    "10.1103/PhysRevB.106.115203",
    "10.1007/s11664-005-0019-3",
}


def load_manifest() -> dict[str, object]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def claim_ids() -> set[str]:
    text = (
        ROOT / "manuscript" / "distributional_band_edge" / "claim_matrix.md"
    ).read_text(encoding="utf-8")
    return {f"C{index:02d}" for index in range(1, 24) if f"C{index:02d}" in text}


def test_source_manifest_has_unique_priority_doi_and_claim_provenance() -> None:
    manifest = load_manifest()
    sources = manifest["sources"]
    assert isinstance(sources, list)
    assert len(sources) == 10

    keys = [source["citation_key"] for source in sources]
    dois = [source["doi"] for source in sources]
    priorities = [source["priority"] for source in sources]
    assert len(set(keys)) == len(keys)
    assert set(dois) == EXPECTED_DOIS
    assert len(set(dois)) == len(dois)
    assert sorted(priorities) == list(range(1, 11))

    declared_claims = claim_ids()
    assert declared_claims == {f"C{index:02d}" for index in range(1, 24)}
    for source in sources:
        assert source["blocked_claim_ids"]
        assert set(source["blocked_claim_ids"]) <= declared_claims
        assert source["requested_artifacts"]
        assert source["scientific_payoff"]
        assert source["rejection_conditions"]


def test_manifest_status_values_are_declared_and_files_fail_closed() -> None:
    manifest = load_manifest()
    enums = manifest["status_enums"]
    for source in manifest["sources"]:
        assert source["availability"] in enums["availability"]
        assert source["rights"] in enums["rights"]
        assert source["audit"] in enums["audit"]
        assert source["operator_authorization"] in enums[
            "operator_authorization"
        ]
        assert source["local_file"] is None
        assert source["sha256"] is None
        assert source["acquisition_provenance"] is None

    for route in manifest["validation_routes"]:
        assert route["readiness"] in enums["readiness"]


def test_validation_gate_ranking_and_selected_route() -> None:
    manifest = load_manifest()
    ranked = rank_validation_routes(manifest)
    assert [(route.route_id, route.score) for route in ranked] == [
        ("chang_thickness_cutoff", 24),
        ("dingrong_carrier_spectrum", 20),
        ("chu_intrinsic_absorption", 19),
        ("herrmann_multimodal_tail", 18),
        ("teppe_transition_series", 18),
        ("moazzami_source_native", 16),
        ("ivanov_pl_joint_closure", 15),
        ("finkman_tail_independent", 14),
        ("krishtopenko_prior_art", 2),
    ]

    selected = select_first_external_validation_route(manifest)
    assert selected.route_id == "chang_thickness_cutoff"
    assert selected.source_keys == (
        "chang2007_nonparabolic_urbach",
        "chang2006_near_edge_absorption",
    )
    assert selected.readiness == "ready_after_retrieval"


def test_gate_report_is_deterministic_and_requests_chang_pair_first() -> None:
    first_json, first_md = build_report(ROOT)
    second_json, second_md = build_report(ROOT)
    assert first_json == second_json
    assert first_md == second_md

    selected = first_json["selected_route"]
    assert selected["route_id"] == "chang_thickness_cutoff"
    assert selected["source_dois"] == [
        "10.1007/s11664-007-0162-0",
        "10.1063/1.2245220",
    ]
    requests = first_json["source_request_order"]
    assert [request["doi"] for request in requests[:3]] == [
        "10.1007/s11664-007-0162-0",
        "10.1063/1.2245220",
        "10.1016/0038-1098(85)90315-1",
    ]
    assert first_json["external_material_validation_complete"] is False
    assert "No route currently establishes external material validation" in first_md


def test_score_validation_criteria_rejects_schema_and_range_errors() -> None:
    valid = {
        "same_specimen_state": 2,
        "composition_provenance": 1,
        "carrier_provenance": 1,
        "thickness_provenance": 1,
        "calibrated_spectrum": 1,
        "equation_completeness": 2,
        "falsification_power": 3,
        "reproducibility_rights": 1,
        "flagship_relevance": 3,
        "nuisance_penalty": 2,
        "implementation_cost": 2,
    }
    assert score_validation_criteria(valid) == 24

    with pytest.raises(ValueError, match="criteria keys"):
        score_validation_criteria({**valid, "unknown": 1})
    invalid = dict(valid)
    invalid["falsification_power"] = 4
    with pytest.raises(ValueError, match="inclusive range"):
        score_validation_criteria(invalid)
    invalid = dict(valid)
    invalid["implementation_cost"] = True
    with pytest.raises(ValueError, match="must be an integer"):
        score_validation_criteria(invalid)
