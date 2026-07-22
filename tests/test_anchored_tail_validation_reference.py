from __future__ import annotations

import json
from pathlib import Path

from tools.build_anchored_tail_validation_reference import build_record


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "validation" / "chang_anchored_tail_recoverability.json"


def test_anchored_tail_reference_is_current() -> None:
    committed = json.loads(REFERENCE.read_text())
    assert build_record() == committed


def test_anchored_tail_reference_preserves_decision_boundary() -> None:
    record = json.loads(REFERENCE.read_text())
    assert record["decision"] == "terminate_chang_figure_digitization_path"
    assert not record["claim_boundary"]["manual_digitization_authorized"]
    assert not record["claim_boundary"]["manuscript_authorized"]
    assert record["claim_boundary"][
        "numeric_gap_anchor_values_and_uncertainty_not_tabulated"
    ]
    assert len(record["traces"]) == 4
    assert all(not trace["three_uncertainty_resolvable"] for trace in record["traces"])
    assert all(not trace["digitization_authorized"] for trace in record["traces"])
    assert max(
        trace["maximum_orthogonal_departure_px"] for trace in record["traces"]
    ) < 18.0
