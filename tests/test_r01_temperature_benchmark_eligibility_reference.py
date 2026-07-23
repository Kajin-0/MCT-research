from __future__ import annotations

import json
from pathlib import Path

from mct_research.r01_temperature_benchmark_eligibility import build_reference

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data/validation/r01_temperature_benchmark_eligibility.json"


def test_committed_reference_matches_deterministic_builder() -> None:
    committed = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert committed == build_reference(ROOT)


def test_committed_reference_preserves_fail_closed_claim_boundary() -> None:
    committed = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert committed["decision"] == "class_specific_single_source_benchmarks_only"
    assert committed["gates"]["E2_any_exact_class_source_holdout_authorized"] is False
    assert committed["gates"]["E4_universal_model_advancement_authorized"] is False
    assert "pooled_cross_class_ranking" in committed["claim_boundary"]["not_authorized"]
