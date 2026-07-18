from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pytest

from tools.design_minimum_gap_identifiability_dataset import analyze

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/templates/paired_gap_identifiability_acquisition_template.csv"


def _scenarios(result: dict) -> dict[str, dict]:
    return {entry["name"]: entry for entry in result["scenarios"]}


def test_design_oracle_is_deterministic() -> None:
    assert analyze() == analyze()


def test_identifiability_progression_has_expected_ranks() -> None:
    scenarios = _scenarios(analyze())
    expected = {
        "current_secondary_chu_absorption_only": 2,
        "three_paired_gap_measurements_only": 3,
        "three_paired_plus_hall": 4,
        "three_paired_plus_vacancy_proxy": 4,
        "algebraic_minimum_three_paired_specimens": 5,
        "audit_grade_eight_specimen_factorial": 5,
    }
    assert {
        name: scenario["diagnostics"]["rank"]
        for name, scenario in scenarios.items()
    } == expected

    assert scenarios["current_secondary_chu_absorption_only"]["diagnostics"][
        "nullity"
    ] == 3
    assert scenarios["three_paired_gap_measurements_only"]["diagnostics"][
        "nullity"
    ] == 2
    assert scenarios["three_paired_plus_hall"]["diagnostics"]["nullity"] == 1
    assert scenarios["three_paired_plus_vacancy_proxy"]["diagnostics"][
        "nullity"
    ] == 1


def test_algebraic_minimum_is_full_rank_but_not_audit_grade() -> None:
    scenario = _scenarios(analyze())["algebraic_minimum_three_paired_specimens"]
    diagnostics = scenario["diagnostics"]

    assert scenario["specimen_count"] == 3
    assert diagnostics["observation_count"] == 6
    assert diagnostics["full_parameter_identification"] is True
    assert diagnostics["residual_degrees_of_freedom"] == 1
    assert diagnostics["condition_number"] == pytest.approx(
        3.2627233713686215, abs=1e-12
    )
    assert diagnostics["maximum_leverage"] == pytest.approx(1.0, abs=1e-12)
    assert diagnostics["audit_grade"] is False


def test_eight_specimen_factorial_is_audit_grade() -> None:
    scenario = _scenarios(analyze())["audit_grade_eight_specimen_factorial"]
    diagnostics = scenario["diagnostics"]
    standard_error = diagnostics["parameter_standard_error_per_1mev_noise"]

    assert scenario["specimen_count"] == 8
    assert diagnostics["observation_count"] == 16
    assert diagnostics["rank"] == 5
    assert diagnostics["residual_degrees_of_freedom"] == 11
    assert diagnostics["condition_number"] == pytest.approx(
        2.6180339887498953, abs=1e-12
    )
    assert diagnostics["information_determinant"] == pytest.approx(
        65536.0, abs=1e-8
    )
    assert diagnostics["maximum_leverage"] == pytest.approx(0.4375, abs=1e-12)
    assert diagnostics["audit_grade"] is True

    assert standard_error["latent_intercept_mev"] == pytest.approx(
        0.3535533905932738, abs=1e-12
    )
    assert standard_error[
        "latent_composition_slope_mev_per_coded_x"
    ] == pytest.approx(0.25, abs=1e-12)
    assert standard_error["absorption_class_offset_mev"] == pytest.approx(
        0.5, abs=1e-12
    )
    assert standard_error[
        "carrier_filling_scale_mev_per_proxy"
    ] == pytest.approx(0.3535533905932738, abs=1e-12)
    assert standard_error[
        "vacancy_edge_scale_mev_per_proxy"
    ] == pytest.approx(0.3535533905932738, abs=1e-12)


def test_minimum_decision_and_composition_budget_are_explicit() -> None:
    result = analyze()
    decision = result["minimum_design_decision"]
    budget = result["composition_uncertainty_budget"]["temperature_sensitivity"]

    assert decision["algebraic_minimum_specimen_count_per_temperature"] == 3
    assert decision["algebraic_minimum_is_audit_grade"] is False
    assert decision["recommended_audit_grade_specimen_count"] == 8
    assert decision["recommended_total_paired_gap_observations"] == 32
    assert decision["recommended_design_is_audit_grade"] is True

    assert budget["6K"]["maximum_sigma_x_for_2mev_gap_budget"] == pytest.approx(
        0.001190267893, abs=1e-12
    )
    assert budget["77K"]["maximum_sigma_x_for_2mev_gap_budget"] == pytest.approx(
        0.001254224670, abs=1e-12
    )
    assert budget["300K"]["maximum_sigma_x_for_2mev_gap_budget"] == pytest.approx(
        0.001506948067, abs=1e-12
    )

    fields = " ".join(result["required_specimen_fields"])
    assert "independent composition" in fields
    assert "paired magneto-optical gap" in fields
    assert "raw intrinsic-absorption spectrum" in fields
    assert "Hall carrier type" in fields
    assert "vacancy-sensitive proxy" in fields


def test_acquisition_template_encodes_balanced_two_temperature_factorial() -> None:
    rows = list(csv.DictReader(TEMPLATE.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 16
    assert {row["specimen_id"] for row in rows} == {
        f"factorial_{index}" for index in range(1, 9)
    }
    assert {row["temperature_block"] for row in rows} == {
        "low_temperature",
        "room_temperature",
    }

    per_specimen: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        per_specimen.setdefault(row["specimen_id"], []).append(row)
    assert all(len(records) == 2 for records in per_specimen.values())

    coded_combinations = {
        (
            int(row["design_composition_code"]),
            int(row["design_carrier_proxy_code"]),
            int(row["design_vacancy_proxy_code"]),
        )
        for row in rows
        if row["temperature_block"] == "low_temperature"
    }
    assert coded_combinations == {
        tuple(values)
        for values in np.asarray(
            [
                [-1, -1, -1],
                [-1, -1, 1],
                [-1, 1, -1],
                [-1, 1, 1],
                [1, -1, -1],
                [1, -1, 1],
                [1, 1, -1],
                [1, 1, 1],
            ],
            dtype=int,
        )
    }
