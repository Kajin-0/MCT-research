from __future__ import annotations

import csv
from pathlib import Path

import pytest

from tools.analyze_laurenti1990_temperature_independent_composition import (
    analyze,
    physical_root,
    thermal_denominator,
    thermal_shift_ev,
)

LEDGER = Path(
    "data/experimental/laurenti1990_temperature_independent_composition.csv"
)


def test_printed_equation_root_rounds_to_reported_value() -> None:
    root, other = physical_root()

    assert root == pytest.approx(0.5047258866289238)
    assert round(root, 3) == 0.505
    assert other == pytest.approx(2.108449789046752)


def test_root_is_temperature_independent_only_within_printed_model() -> None:
    root, _ = physical_root()

    for temperature in [0.0, 100.0, 200.0, 300.0, 500.0]:
        assert thermal_denominator(root, temperature) > 0.0
        assert thermal_shift_ev(root, temperature) == pytest.approx(
            0.0, abs=3.0e-17
        )


def test_printed_precision_and_measurement_resolution_do_not_support_three_decimals() -> None:
    _, summary = analyze()
    rounding = summary["printed_coefficient_rounding_stress"]
    resolution = summary["experimental_resolution_audit"]

    assert rounding["root_min"] == pytest.approx(0.501711452365598)
    assert rounding["root_max"] == pytest.approx(0.5077230645618164)
    assert rounding["interval_width"] > 0.006
    assert resolution["shift_for_plus_or_minus_0p005_at_300k_mev"] == pytest.approx(
        1.2377440645600677
    )
    assert resolution["single_edge_3mev_equivalent_composition_resolution"] > 0.012
    assert resolution[
        "independent_two_edge_3mev_each_equivalent_composition_resolution"
    ] > 0.017


def test_paper_illustrations_bracket_the_sign_change() -> None:
    _, summary = analyze()
    shifts = summary["illustrated_300k_shifts_mev"]

    assert shifts["x_0p500"] == pytest.approx(1.1744236624619382)
    assert shifts["x_0p505"] == pytest.approx(-0.06784119401428478)
    assert shifts["x_0p550"] == pytest.approx(-10.795296279811062)
    assert shifts["x_0p500"] > 0.0 > shifts["x_0p550"]


def test_committed_ledger_matches_fresh_analysis() -> None:
    expected_rows, _ = analyze()
    recorded_rows = list(csv.DictReader(LEDGER.read_text(encoding="utf-8").splitlines()))

    assert len(recorded_rows) == len(expected_rows) == 20
    for expected, recorded in zip(expected_rows, recorded_rows, strict=True):
        assert set(recorded) == set(expected)
        for name, value in expected.items():
            if name == "composition_label":
                assert recorded[name] == value
            else:
                assert float(recorded[name]) == pytest.approx(
                    value, rel=1.0e-12, abs=5.0e-13
                )
