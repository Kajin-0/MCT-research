from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_krishnamurthy1995_table1 import analyze_tables

TABLE1 = Path("data/theory/krishnamurthy1995_hg078cd022_table1.csv")
TABLE2 = Path("data/theory/krishnamurthy1995_hg078cd022_table2.csv")


def _summary() -> dict:
    return analyze_tables(TABLE1, TABLE2)


def test_table1_modes_reproduce_printed_total_within_rounding() -> None:
    summary = _summary()
    total = summary["table1"]["total"]
    residual = summary["table1"]["mode_sum_minus_total"]

    assert total["valence_mev"] == pytest.approx(-207.02)
    assert total["conduction_mev"] == pytest.approx(-80.46)
    assert total["gap_mev"] == pytest.approx(126.56)
    assert residual["valence_mev"] == pytest.approx(-0.01)
    assert residual["conduction_mev"] == pytest.approx(0.02)
    assert residual["gap_mev"] == pytest.approx(0.03)


def test_acoustic_modes_reproduce_the_papers_about_75_percent_statement() -> None:
    channels = _summary()["phonon_channels"]

    assert channels["acoustic_combined_edge_magnitude_fraction"] == pytest.approx(
        0.7377556699596494
    )
    assert channels["acoustic_valence_magnitude_fraction"] == pytest.approx(
        0.8291952468360545
    )
    assert channels["acoustic_conduction_magnitude_fraction"] == pytest.approx(
        0.5024857071836938
    )
    assert channels["acoustic_gap_fraction_of_net"] == pytest.approx(
        1.0368994943109988
    )
    assert channels["TA_gap_fraction_of_net"] == pytest.approx(
        0.9747945638432364
    )
    assert channels["optical"]["gap_mev"] == pytest.approx(-4.64)


def test_intermediate_band_channels_are_strongly_cancelling() -> None:
    bands = _summary()["intermediate_bands"]

    assert bands["valence_bands_1_to_4"]["gap_mev"] == pytest.approx(-110.03)
    assert bands["conduction_bands_5_to_8"]["gap_mev"] == pytest.approx(236.59)
    assert bands["gap_cancellation_index"] == pytest.approx(2.73878002528445)
    assert bands["individual_gap_contributions_mev"] == pytest.approx(
        [-4.86, -11.15, -39.58, -54.44, 56.45, 67.06, 53.49, 59.59]
    )


def test_table1_and_table2_close_with_minus_7p90_mev_remainder() -> None:
    closure = _summary()["table1_table2_closure"]

    assert closure["unrenormalized_reference_gap_mev"] == pytest.approx(100.0)
    assert closure["electron_phonon_gap_shift_300k_mev"] == pytest.approx(126.56)
    assert closure["fixed_lattice_gap_300k_mev"] == pytest.approx(226.56)
    assert closure["gap_300k_mev"] == pytest.approx(218.66)
    assert closure["inferred_non_electron_phonon_300k_mev"] == pytest.approx(-7.90)
    assert closure["thermal_electron_phonon_beyond_zero_point_mev"] == pytest.approx(
        112.96
    )
    assert closure["table2_1_to_300k_shift_mev"] == pytest.approx(105.06)
    assert closure["reconstructed_1_to_300k_shift_mev"] == pytest.approx(105.06)
    assert closure["closure_residual_mev"] == pytest.approx(0.0)


def test_decision_does_not_invent_temperature_resolved_channels() -> None:
    summary = _summary()
    decision = summary["decision"]

    assert decision["new_oscillator_family_supported"] is False
    assert decision["low_temperature_turnover_resolved"] is False
    assert decision["experimental_validation"] is False
    assert summary["rounding_bounds"]["inferred_non_ep_worst_case_mev"] == pytest.approx(
        0.14
    )
