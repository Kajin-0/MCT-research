from __future__ import annotations

import json
from pathlib import Path

import pytest

from mct_research.chang_validation_design import (
    estimate_tail_width_from_cutoff_pair,
    maximum_source_valid_thickness_ratio,
    required_equal_cutoff_sigma_ev,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "validation" / "chang_thickness_pair_validation_design.json"
SCHEMA = ROOT / "data" / "templates" / "chang_thickness_validation_dataset.schema.json"


def load(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_immutable_design_record_matches_executable_results() -> None:
    record = load(RECORD)
    baseline = record["declared_baseline"]
    result = estimate_tail_width_from_cutoff_pair(
        baseline["baseline_cutoff_energy_ev"],
        baseline["comparison_cutoff_energy_ev"],
        baseline["baseline_effective_thickness_um"],
        baseline["comparison_effective_thickness_um"],
        cutoff_sigma_1_ev=0.001,
        cutoff_sigma_2_ev=0.001,
    )
    assert result.width_ev == pytest.approx(baseline["recovered_tail_width_ev"])
    assert result.relative_standard_uncertainty == pytest.approx(
        record["ratio_4_uncertainty_cases"][
            "equal_1_mev_independent_cutoff_errors"
        ]["relative_width_uncertainty"]
    )

    limits = record["source_domain_limits"]
    assert maximum_source_valid_thickness_ratio(
        baseline["baseline_cutoff_energy_ev"],
        baseline["tail_width_ev"],
        baseline["minimum_source_energy_ev"],
    ) == pytest.approx(limits["absolute_maximum_ratio"])
    assert maximum_source_valid_thickness_ratio(
        baseline["baseline_cutoff_energy_ev"],
        baseline["tail_width_ev"],
        baseline["minimum_source_energy_ev"],
        energy_margin_ev=0.002,
    ) == pytest.approx(limits["maximum_ratio_with_2_mev_energy_margin"])

    for row in record["required_equal_independent_per_cutoff_precision"]:
        assert 1000.0 * required_equal_cutoff_sigma_ev(
            baseline["tail_width_ev"],
            baseline["thickness_ratio"],
            row["target_relative_width_uncertainty"],
        ) == pytest.approx(row["required_cutoff_sigma_mev_exact_ratio"])


def test_future_dataset_schema_separates_effective_and_physical_thickness() -> None:
    schema = load(SCHEMA)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    required = set(schema["required"])
    assert "cutoffs" in required
    assert "cutoff_energy_covariance_ev2" in required
    assert schema["properties"]["external_material_validation_authorized"][
        "const"
    ] is False

    cutoff = schema["properties"]["cutoffs"]["items"]
    cutoff_required = set(cutoff["required"])
    assert "effective_thickness_um" in cutoff_required
    assert "effective_thickness_uncertainty_um" in cutoff_required
    assert "physical_thickness_um" in cutoff_required
    assert cutoff["properties"]["branch"]["enum"] == [
        "tail",
        "intrinsic",
        "unknown",
    ]


def test_record_preserves_source_and_validation_boundaries() -> None:
    record = load(RECORD)
    assert record["status"].startswith("synthetic validation-design")
    assert record["source_operator"]["figure2_validation_authorized"] is False
    assert record["design_decision"]["recommended_synthetic_pair"] == (
        "5 um and 20 um effective thickness"
    )
    assert any(
        "Physical thickness" in statement
        for statement in record["unauthorized_conclusions"]
    )
    assert any(
        "No external material validation" in statement
        for statement in record["unauthorized_conclusions"]
    )
