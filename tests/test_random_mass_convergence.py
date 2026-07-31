from __future__ import annotations

import json
from pathlib import Path


def _record() -> dict[str, object]:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "validation"
        / "r05_convergence_summary.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_immutable_r05_convergence_record_passes_predeclared_numerical_gate() -> None:
    record = _record()
    assert record["schema_version"] == "r05_convergence_summary_v1"
    assert record["decision"] == "GO_PHYSICAL_SCREENING"
    checks = record["checks"]
    assert isinstance(checks, dict)
    assert checks
    assert all(checks.values())


def test_immutable_r05_record_retains_claim_boundary_and_error_metrics() -> None:
    record = _record()
    diagnostics = record["diagnostics"]
    assert diagnostics["minimum_accepted_converged_delta_1"] > 0.10
    assert diagnostics["primary_batch_standard_error"] <= 0.02
    assert diagnostics["finite_size_drift"] <= 0.03
    assert diagnostics["discretization_drift"] <= 0.03
    assert diagnostics["numerical_broadening_drift"] <= 0.03
    assert diagnostics["scalar_null_integrated_relative_difference"] <= 0.01
    assert "Synthetic one-dimensional" in record["claim_boundary"]