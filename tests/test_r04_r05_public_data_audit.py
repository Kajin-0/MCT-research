from __future__ import annotations

import json
from pathlib import Path

from mct_research.r04_r05_public_data_audit import (
    REQUIRED_GATES,
    candidate_passes_all_gates,
    validate_public_data_audit,
)


def _record() -> dict[str, object]:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "validation"
        / "r04_r05_public_data_audit.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_public_data_audit_is_internally_consistent() -> None:
    record = _record()
    assert validate_public_data_audit(record) == []


def test_pr2_decision_requires_partner_data_without_reactivating_r05() -> None:
    record = _record()
    assert record["decision"] == "PARTNER_DATA_REQUIRED"
    assert record["qualifying_complete_record_found"] is False
    assert record["r05_material_activation"] == "BLOCKED"
    assert record["authorized_next_stage"] == "PARTNER_ACQUISITION_AND_AUTHOR_CONTACT"


def test_no_candidate_passes_the_complete_evidence_gate() -> None:
    record = _record()
    candidates = record["candidate_records"]
    assert len(candidates) >= 8
    assert not any(candidate_passes_all_gates(candidate) for candidate in candidates)
    for candidate in candidates:
        assert tuple(candidate["gate_status"]) == REQUIRED_GATES


def test_open_raw_spectroscopy_is_not_misclassified_as_local_dos_evidence() -> None:
    record = _record()
    open_raw = [
        candidate
        for candidate in record["candidate_records"]
        if candidate["raw_data_status"] == "AVAILABLE"
    ]
    assert len(open_raw) >= 2
    for candidate in open_raw:
        assert candidate["gate_status"]["local_variance_gate"] != "PASS"
        assert candidate["gate_status"]["correlation_length_gate"] != "PASS"
        assert candidate["gate_status"]["matched_null_gate"] != "PASS"


def test_near_critical_article_does_not_satisfy_the_joint_gate() -> None:
    record = _record()
    phase_diagram = next(
        candidate
        for candidate in record["candidate_records"]
        if candidate["id"] == "bovkun_2025_phase_diagram"
    )
    assert phase_diagram["gate_status"]["near_critical_gate"] == "PASS"
    assert phase_diagram["gate_status"]["local_variance_gate"] == "FAIL"
    assert phase_diagram["gate_status"]["same_population_gate"] == "FAIL"
    assert phase_diagram["qualification"] == "NONQUALIFYING_PARTNER_LEAD"


def test_sts_surface_systematics_remain_explicit() -> None:
    record = _record()
    sts = next(
        candidate
        for candidate in record["candidate_records"]
        if candidate["id"] == "wang_2012_hgcdte_sts"
    )
    assert "tip-induced band bending" in sts["useful_evidence"]
    assert "surface or pit states" in sts["useful_evidence"]
    assert sts["gate_status"]["robustness_gate"] == "FAIL_SURFACE_SYSTEMATICS_UNCONTROLLED"


def test_figure_digitization_and_larger_simulation_are_not_authorized() -> None:
    record = _record()
    unauthorized = set(record["unauthorized_work"])
    assert "claiming public-data validation from digitized figures" in unauthorized
    assert "larger random-mass simulation" in unauthorized
    assert "full 8-band spatial disorder" in unauthorized
    assert "R05 reactivation" in unauthorized
