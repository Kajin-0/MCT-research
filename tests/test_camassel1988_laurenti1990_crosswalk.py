from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_camassel1988_laurenti1990_crosswalk import analyze

DATA = Path("data/experimental/camassel1988_laurenti1990_cd_rich_crosswalk.csv")


def test_priority_specimen_identities_and_growth_methods() -> None:
    rows, summary = analyze(DATA)

    assert [(row["composition_x"], row["sample_id"], row["growth_method"]) for row in rows] == [
        (0.970, "MCT 83", "LPE"),
        (0.955, "bulk reference", "THM"),
        (0.925, "MCT 51", "LPE"),
    ]
    assert summary["growth_method_counts"] == {"LPE": 2, "THM": 1}


def test_exciton_to_gap_arithmetic_closes() -> None:
    rows, summary = analyze(DATA)

    assert summary["all_gap_closure_residuals_below_microelectronvolt"] is True
    for row in rows:
        assert row["gap_closure_residual_mev"] == pytest.approx(0.0, abs=1.0e-9)


def test_composition_uncertainty_exceeds_reported_energy_extraction_scale() -> None:
    rows, summary = analyze(DATA)

    assert summary["composition_energy_scale_mev"] == pytest.approx(10.0)
    assert summary["laurenti_reported_extraction_accuracy_upper_bound_mev"] == pytest.approx(3.0)
    assert summary["composition_uncertainty_dominates_extraction_accuracy"] is True
    for row in rows:
        assert row["composition_to_extraction_scale_ratio"] == pytest.approx(10.0 / 3.0)


def test_crosswalk_preserves_model_corrected_observable_boundary() -> None:
    _, summary = analyze(DATA)

    assert summary["source_kind"] == "primary_experiment_with_model_corrected_exciton_gap"
    assert "not LPE" in summary["corrected_task_wording"]
    assert "exciton-model corrected" in summary["scientific_decision"]
