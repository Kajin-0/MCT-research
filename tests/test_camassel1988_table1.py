from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPECIMENS = ROOT / "data" / "experimental" / "camassel1988_specimens.csv"
OBSERVATIONS = (
    ROOT / "data" / "experimental" / "camassel1988_table1_observations.csv"
)


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_exact_specimen_registry() -> None:
    rows = _rows(SPECIMENS)
    assert len(rows) == 11
    assert [row["sample_label"] for row in rows] == [
        "MCT 48",
        "MCT 83",
        "bulk",
        "MCT 51",
        "MCT 49",
        "MCT 47",
        "MCT 56",
        "MCT 61",
        "MCT 31",
        "MCT 67",
        "MCT 68",
    ]
    assert [float(row["composition_x"]) for row in rows] == pytest.approx(
        [1.000, 0.970, 0.955, 0.925, 0.880, 0.780, 0.710, 0.710, 0.620, 0.550, 0.500]
    )
    assert Counter(row["growth_technique"] for row in rows) == Counter(
        {"LPE": 10, "THM": 1}
    )
    assert rows[2]["specimen_form"] == "bulk_reference"
    assert all(float(row["temperature_k"]) == 2.0 for row in rows)
    assert all(row["composition_method"] == "ionic_microprobe" for row in rows)


def test_composition_accuracy_semantics_are_preserved() -> None:
    rows = _rows(SPECIMENS)
    assert {float(row["composition_accuracy_x"]) for row in rows} == {0.005}
    assert {row["composition_accuracy_semantics"] for row in rows} == {
        "source_reported_standard_accuracy_not_asserted_gaussian_sigma"
    }
    assert {row["source_hash_status"] for row in rows} == {
        "file_library_binary_not_materialized_hash_unavailable"
    }
    assert {row["source_pdf_sha256"] for row in rows} == {""}


def test_observation_counts_and_specimen_grouping() -> None:
    rows = _rows(OBSERVATIONS)
    assert len(rows) == 13
    assert Counter(row["modality"] for row in rows) == Counter(
        {"reflectivity": 6, "absorption_derivative": 7}
    )
    assert Counter(row["measurement_class"] for row in rows) == Counter(
        {
            "reflectivity_exciton_polariton_gap": 6,
            "absorption_derivative_excitonic_gap": 7,
        }
    )
    counts = Counter(row["specimen_id"] for row in rows)
    assert counts["camassel1988_mct49"] == 2
    assert counts["camassel1988_mct47"] == 2
    assert all(counts[key] == 1 for key in counts if key not in {
        "camassel1988_mct49",
        "camassel1988_mct47",
    })
    assert {
        row["composition_group_id"] for row in rows
    } == {row["specimen_id"] for row in rows}


def test_reflectivity_rows_match_table_i_and_binding_basis() -> None:
    rows = [row for row in _rows(OBSERVATIONS) if row["modality"] == "reflectivity"]
    expected = [
        ("camassel1988_mct48", 1.5965, 9.5, "theoretical_exciton_binding_energy", 1.6060),
        ("camassel1988_mct83", 1.5315, 9.0, "theoretical_exciton_binding_energy", 1.5405),
        ("camassel1988_bulk", 1.4992, 8.7, "theoretical_exciton_binding_energy", 1.5079),
        ("camassel1988_mct51", 1.4416, 8.2, "theoretical_exciton_binding_energy", 1.4498),
        ("camassel1988_mct49", 1.3440, 8.0, "experimental_exciton_binding_energy", 1.3520),
        ("camassel1988_mct47", 1.1260, 6.5, "experimental_exciton_binding_energy", 1.1325),
    ]
    assert len(rows) == len(expected)
    for row, (specimen, transition, binding, basis, gap) in zip(rows, expected, strict=True):
        assert row["specimen_id"] == specimen
        assert float(row["transition_energy_ev"]) == pytest.approx(transition)
        assert float(row["binding_energy_mev"]) == pytest.approx(binding)
        assert row["binding_energy_basis"] == basis
        assert float(row["tabulated_gap_ev"]) == pytest.approx(gap)
        assert float(row["tabulated_gap_ev"]) == pytest.approx(
            transition + binding / 1000.0,
            abs=5.0e-7,
        )


def test_absorption_rows_match_table_i_and_close_exactly() -> None:
    rows = [
        row for row in _rows(OBSERVATIONS) if row["modality"] == "absorption_derivative"
    ]
    expected = [
        ("camassel1988_mct49", 1.3420, 8.0, 1.3500),
        ("camassel1988_mct47", 1.1435, 6.5, 1.1500),
        ("camassel1988_mct56", 1.0130, 6.0, 1.0190),
        ("camassel1988_mct61", 1.0130, 6.0, 1.0190),
        ("camassel1988_mct31", 0.8625, 5.0, 0.8675),
        ("camassel1988_mct67", 0.6980, 3.0, 0.7010),
        ("camassel1988_mct68", 0.6250, 3.0, 0.6280),
    ]
    assert len(rows) == len(expected)
    for row, (specimen, transition, binding, gap) in zip(rows, expected, strict=True):
        assert row["specimen_id"] == specimen
        assert row["binding_energy_basis"] == "experimental_exciton_binding_energy"
        assert float(row["transition_energy_ev"]) == pytest.approx(transition)
        assert float(row["binding_energy_mev"]) == pytest.approx(binding)
        assert float(row["tabulated_gap_ev"]) == pytest.approx(gap)
        assert float(row["tabulated_gap_ev"]) == pytest.approx(
            transition + binding / 1000.0,
            abs=5.0e-7,
        )


def test_duplicate_composition_specimens_remain_distinct() -> None:
    specimens = _rows(SPECIMENS)
    x071 = [row for row in specimens if float(row["composition_x"]) == pytest.approx(0.710)]
    assert [row["specimen_id"] for row in x071] == [
        "camassel1988_mct56",
        "camassel1988_mct61",
    ]
    observations = _rows(OBSERVATIONS)
    assert {
        row["specimen_id"] for row in observations if row["specimen_id"] in {
            "camassel1988_mct56",
            "camassel1988_mct61",
        }
    } == {"camassel1988_mct56", "camassel1988_mct61"}


def test_no_pointwise_energy_covariance_is_invented() -> None:
    rows = _rows(OBSERVATIONS)
    assert {row["energy_uncertainty_ev"] for row in rows} == {""}
    assert {row["energy_uncertainty_status"] for row in rows} == {
        "not_reported_for_table1"
    }
    assert {row["source_hash_status"] for row in rows} == {
        "file_library_binary_not_materialized_hash_unavailable"
    }
    assert {row["source_pdf_sha256"] for row in rows} == {""}
