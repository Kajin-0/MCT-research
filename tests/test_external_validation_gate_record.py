from __future__ import annotations

import json
from pathlib import Path

from tools.build_external_validation_gate import build_report

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "validation" / "external_validation_route_gate.json"


def test_immutable_gate_record_matches_executable_ranking() -> None:
    with RECORD.open(encoding="utf-8") as handle:
        recorded = json.load(handle)
    generated, _ = build_report(ROOT)

    assert generated["selected_route"] == recorded["selected_route"]
    assert generated["selection_robustness"] == recorded[
        "selection_robustness"
    ]
    assert [
        {
            "rank": route["rank"],
            "route_id": route["route_id"],
            "score": route["score"],
            "readiness": route["readiness"],
        }
        for route in generated["ranked_routes"]
    ] == recorded["ranked_routes"]
    assert [
        request["doi"] for request in generated["source_request_order"]
    ] == recorded["source_request_order"]
    assert recorded["external_material_validation_complete"] is False
    assert "not a probability" in recorded["score_interpretation"]
