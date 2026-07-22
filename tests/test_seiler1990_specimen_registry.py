from __future__ import annotations

import csv
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "experimental" / "seiler1990_specimens.csv"
FIGURE7 = ROOT / "data" / "experimental" / "seiler1990_figure7_digitized.csv"
TABLE2 = (
    ROOT
    / "data"
    / "experimental"
    / "seiler1990_table2_low_temperature_magneto_optical.csv"
)
SOURCE_HASH = "5bc624ca8292fcba72ae55d13c5be03d07af03b57afc4584c2314ca08e459a49"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_registry_has_exact_five_specimens_and_electrical_properties() -> None:
    rows = _rows(REGISTRY)
    assert [int(row["sample_number"]) for row in rows] == [1, 2, 3, 4, 5]
    expected = {
        1: (1.4e14, 1.6e5),
        2: (2.8e14, 1.2e5),
        3: (1.0e14, 7.6e4),
        4: (1.4e14, 6.6e4),
        5: (9.9e13, 5.3e4),
    }
    for row in rows:
        sample = int(row["sample_number"])
        concentration, mobility = expected[sample]
        assert float(row["carrier_concentration_17k_cm3"]) == pytest.approx(
            concentration
        )
        assert float(row["mobility_17k_cm2_v_s"]) == pytest.approx(mobility)


def test_composition_values_and_admissibility_are_exact() -> None:
    rows = {int(row["sample_number"]): row for row in _rows(REGISTRY)}
    expected_x = {1: 0.239, 2: 0.253, 3: 0.259, 4: 0.277, 5: 0.300}
    expected_sigma = {1: "", 2: "", 3: "0.0015", 4: "0.0010", 5: "0.0035"}
    expected_independent = {1: "false", 2: "false", 3: "true", 4: "true", 5: "true"}
    for sample in range(1, 6):
        assert float(rows[sample]["composition_x"]) == pytest.approx(expected_x[sample])
        assert rows[sample]["composition_sigma_x"] == expected_sigma[sample]
        assert (
            rows[sample]["composition_independent_for_composition_law"]
            == expected_independent[sample]
        )
    assert rows[4]["composition_x"] == "0.277"
    assert "0.217" not in REGISTRY.read_text(encoding="utf-8")


def test_figure7_marker_counts_and_roles_match_registry() -> None:
    registry = {int(row["sample_number"]): row for row in _rows(REGISTRY)}
    figure_rows = _rows(FIGURE7)
    assert len(figure_rows) == 34
    counts = {sample: 0 for sample in range(1, 6)}
    for row in figure_rows:
        counts[int(row["sample_number"])] += 1
    assert counts == {1: 14, 2: 11, 3: 9, 4: 0, 5: 0}
    for sample, count in counts.items():
        assert int(registry[sample]["figure7_marker_count"]) == count
    assert registry[1]["figure7_temperature_series_role"] == "thermal_shape_only"
    assert registry[2]["figure7_temperature_series_role"] == "thermal_shape_only"
    assert (
        registry[3]["figure7_temperature_series_role"]
        == "thermal_shape_and_absolute_gap"
    )
    assert registry[4]["figure7_temperature_series_role"] == "low_temperature_anchor_only"
    assert registry[5]["figure7_temperature_series_role"] == "low_temperature_anchor_only"


def test_table2_present_work_rows_and_independent_anchors_match_registry() -> None:
    registry = {int(row["sample_number"]): row for row in _rows(REGISTRY)}
    table_rows = [
        row for row in _rows(TABLE2) if row["present_work"].strip().lower() == "true"
    ]
    assert [int(row["sample_number"]) for row in table_rows] == [1, 3, 4, 5]
    expected = {
        1: (0.239, 122.0, 1.0, False),
        3: (0.259, 158.5, 1.0, True),
        4: (0.277, 195.0, 1.0, True),
        5: (0.300, 224.0, 2.0, True),
    }
    for row in table_rows:
        sample = int(row["sample_number"])
        x_value, gap, sigma_gap, independent = expected[sample]
        assert float(row["composition_x"]) == pytest.approx(x_value)
        assert float(row["gap_mev"]) == pytest.approx(gap)
        assert float(row["gap_sigma_mev"]) == pytest.approx(sigma_gap)
        assert float(registry[sample]["low_temperature_gap_mev"]) == pytest.approx(gap)
        assert float(registry[sample]["low_temperature_gap_sigma_mev"]) == pytest.approx(
            sigma_gap
        )
        assert (
            registry[sample]["composition_independent_for_composition_law"] == "true"
        ) is independent
    independent_samples = [
        int(row["sample_number"])
        for row in table_rows
        if registry[int(row["sample_number"])][
            "composition_independent_for_composition_law"
        ]
        == "true"
    ]
    assert independent_samples == [3, 4, 5]
    assert registry[2]["table2_present_work"] == "false"
    assert float(registry[2]["low_temperature_gap_mev"]) == pytest.approx(146.5)
    assert registry[2]["low_temperature_gap_source_location"] == "Section_III_A_text"


def test_source_hash_and_measurement_class_are_consistent() -> None:
    registry = _rows(REGISTRY)
    figure_rows = _rows(FIGURE7)
    table_rows = _rows(TABLE2)
    assert {row["source_pdf_sha256"] for row in registry} == {SOURCE_HASH}
    assert {row["source_pdf_sha256"] for row in figure_rows} == {SOURCE_HASH}
    assert {row["source_pdf_sha256"] for row in table_rows} == {SOURCE_HASH}
    expected_class = "two_photon_magnetoabsorption_modified_Pidgeon_Brown_gap"
    assert {row["measurement_class"] for row in registry} == {expected_class}
    assert {row["measurement_class"] for row in figure_rows} == {expected_class}


def test_figure7_does_not_invent_pointwise_experimental_covariance() -> None:
    figure_rows = _rows(FIGURE7)
    assert {
        row["pointwise_experimental_gap_uncertainty"] for row in figure_rows
    } == {"not_reported_for_figure7"}
    assert all(float(row["gap_digitization_half_width_mev"]) > 0.0 for row in figure_rows)
