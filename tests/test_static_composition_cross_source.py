from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mct_research.historical_gap_models import chu_1983_gap_ev
from tools.analyze_static_composition_cross_source import (
    analyze,
    invert_composition,
    load_chu_table,
    load_independent_seiler,
)

ROOT = Path(__file__).resolve().parents[1]
CHU = ROOT / "data/experimental/chu_sher_2008_table4_4_room_temperature_gap.csv"
SEILER = ROOT / "data/experimental/seiler1990_table2_low_temperature_magneto_optical.csv"


def test_chu_formula_reference_and_broadcasting() -> None:
    assert chu_1983_gap_ev(0.2, 300.0) == pytest.approx(0.16796, abs=1e-14)
    values = chu_1983_gap_ev(
        np.asarray([0.17, 0.20]), np.asarray([300.0, 300.0])
    )
    assert isinstance(values, np.ndarray)
    assert values.shape == (2,)
    assert np.all(np.isfinite(values))


def test_data_provenance_is_explicit() -> None:
    chu = load_chu_table(CHU)
    seiler = load_independent_seiler(SEILER)

    assert len(chu) == 8
    assert all(
        record["composition_provenance_status"]
        == "not_recovered_from_primary_article"
        for record in chu
    )
    assert all(
        record["uncertainty_status"] == "not_reported_in_secondary_table"
        for record in chu
    )
    assert {record["sample_number"] for record in seiler} == {3, 4, 5}


def test_cross_source_screen_reproduces_expected_model_hierarchy() -> None:
    result = analyze(CHU, SEILER)
    room = result["source_screen"]["chu_secondary_room_temperature"]
    low = result["source_screen"]["seiler_independent_low_temperature"]

    assert room["chu_1983"]["rmse_mev"] == pytest.approx(
        3.256771621080479, rel=1e-11
    )
    assert room["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        11.991099243506273, rel=1e-11
    )
    assert room["hansen"]["rmse_mev"] == pytest.approx(
        16.26639916257656, rel=1e-11
    )

    assert low["provisional_hansen_pade"]["rmse_mev"] == pytest.approx(
        4.176161297214716, rel=1e-11
    )
    assert low["hansen"]["rmse_mev"] == pytest.approx(
        3.8866718078537885, rel=1e-11
    )
    assert low["chu_1983"]["rmse_mev"] > 15.0


def test_no_diagnostic_static_correction_transfers() -> None:
    result = analyze(CHU, SEILER)
    corrections = result[
        "diagnostic_static_corrections_fit_to_secondary_chu_table"
    ]

    assert set(corrections) == {
        "constant",
        "affine",
        "quadratic",
        "endpoint_one",
        "endpoint_two",
    }
    assert result["universal_static_correction_candidates"] == []
    assert all(not record["universal_candidate"] for record in corrections.values())
    assert corrections["affine"]["chu_leave_one_composition_out_metrics"][
        "rmse_mev"
    ] < 3.0
    assert corrections["affine"]["seiler_independent_transfer_metrics"][
        "rmse_mev"
    ] > 7.0


def test_affine_composition_mapping_is_source_specific() -> None:
    result = analyze(CHU, SEILER)
    mapping = result["diagnostic_composition_scale_mapping"]
    coefficients = mapping[
        "x_effective_equals_intercept_plus_slope_times_reported_x"
    ]

    assert coefficients["intercept"] == pytest.approx(
        -0.01124905, abs=2e-8
    )
    assert coefficients["slope"] == pytest.approx(1.05943497, abs=2e-8)
    assert mapping["affine_mapping_rms_composition_residual"] == pytest.approx(
        0.001596343393671, rel=1e-10
    )
    assert mapping["chu_room_metrics_after_mapping"]["rmse_mev"] < 2.2
    assert mapping["seiler_low_temperature_metrics_after_mapping"][
        "rmse_mev"
    ] > 8.0
    assert mapping["mapping_transfers_to_seiler"] is False


def test_static_law_remains_blocked() -> None:
    result = analyze(CHU, SEILER)
    decision = result["decision"]

    assert decision["new_static_composition_polynomial_authorized"] is False
    assert decision["provisional_thermal_kernel_retained"] is True
    assert decision["chu_1983_retained_as_historical_comparator"] is True
    assert decision["source_specific_composition_calibration_is_plausible"] is True
    assert decision["cross_source_static_law_is_identified"] is False
    assert all(value is False for value in result["data_sufficiency_checks"].values())


def test_composition_inversion_fails_without_bracket() -> None:
    with pytest.raises(ValueError, match="does not bracket"):
        invert_composition(10.0, 300.0, lambda x, temperature: x)
