from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.build_published_tail_curvature_recoverability_reference import (
    build_reference,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data/validation/published_tail_curvature_recoverability.json"


def test_immutable_recoverability_record_matches_builder() -> None:
    committed = json.loads(RECORD.read_text(encoding="utf-8"))
    rebuilt = build_reference()
    assert rebuilt == committed


def test_recoverability_record_preserves_claim_boundaries() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    assert record["portfolio_contribution"] == "R03"
    assert record["issue"] == 235
    assert record["status"].endswith("not_material_validation")
    assert record["decision"]["manual_digitization_authorized"] is False

    cases = {
        case["source_identifier"]: case
        for case in record["source_conditioned_traces"]
    }
    assert cases["finkman_schacham_1984_fig4_85k"]["critical_upper_z_three_sigma"] is None
    assert cases["finkman_nemirovsky_1979_fig3_80k"]["critical_upper_z_three_sigma"] is None
    assert cases["finkman_schacham_1984_fig4_300k"][
        "critical_upper_z_three_sigma"
    ] == pytest.approx(-0.7171512656, abs=2.0e-9)
    assert cases["finkman_nemirovsky_1979_fig3_300k"][
        "critical_upper_z_three_sigma"
    ] == pytest.approx(-0.7227387645, abs=2.0e-9)

    boundaries = record["claim_boundaries"]
    assert any("not source measurement covariance" in item for item in boundaries)
    assert any("does not identify composition disorder" in item for item in boundaries)
    assert any("Ariel 1995" in item for item in boundaries)
