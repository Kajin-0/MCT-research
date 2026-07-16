from __future__ import annotations

import pytest

from tools.analyze_seiler1990_tpma_provenance import analyze


def test_table_counts_and_measurement_classes() -> None:
    _, summary = analyze()
    assert summary["table1_sample_count"] == 5
    assert summary["table2_gap_row_count"] == 18
    assert summary["measurement_class_counts"] == {
        "cyclotron_combined_and_cyclotron_phonon_resonance": 1,
        "electron_spin_resonance": 1,
        "four_photon_mixing_esr": 1,
        "interband_magnetoabsorption": 11,
        "two_photon_magnetoabsorption": 4,
    }


def test_only_three_present_tpma_points_have_independent_composition() -> None:
    rows, summary = analyze()
    assert summary["present_work_tpma_count"] == 4
    assert summary["independent_present_work_tpma_count"] == 3
    assert summary["independent_sample_numbers"] == [3, 4, 5]
    assert summary["independent_compositions"] == [0.259, 0.277, 0.300]
    assert [row["sample_number"] for row in rows] == [1, 3, 4, 5]
    assert rows[0]["independent_for_composition_law"] is False


def test_composition_uncertainty_exceeds_reported_gap_uncertainty() -> None:
    rows, summary = analyze()
    by_sample = {row["sample_number"]: row for row in rows}
    assert by_sample[3]["composition_energy_sigma_range_2_10k_mev"] == pytest.approx(
        [2.500731264, 2.513571264]
    )
    assert by_sample[4]["composition_energy_sigma_range_2_10k_mev"] == pytest.approx(
        [1.662075584, 1.670635584]
    )
    assert by_sample[5]["composition_energy_sigma_range_2_10k_mev"] == pytest.approx(
        [5.80279, 5.83275]
    )
    assert summary["composition_uncertainty_exceeds_gap_sigma"] is True
    assert summary["hansen_derivative_used_only_as_sensitivity"] is True


def test_compilation_provenance_remains_unresolved() -> None:
    _, summary = analyze()
    assert summary["provenance_status_counts"] == {
        "cutoff_derived_not_independent": 1,
        "not_audited_in_seiler": 14,
        "wet_chemistry_tied_independent": 3,
    }
    assert "modified Pidgeon-Brown" in summary["observable_boundary"]
