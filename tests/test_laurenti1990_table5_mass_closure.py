from pathlib import Path

import pytest

from tools.analyze_laurenti1990_table5_mass_closure import (
    analyze,
    infer_p2_ev,
    predict_mass_ratio,
    spin_orbit_ev,
)

SOURCE = Path("data/theory/laurenti1990_tables4_5_cd_rich.csv")


def test_three_band_forward_inverse_closure() -> None:
    delta = spin_orbit_ev(1.0)
    p2 = infer_p2_ev(1.606, 0.090, delta)
    reconstructed = predict_mass_ratio(1.606, p2, delta)

    assert delta == pytest.approx(0.927)
    assert p2 == pytest.approx(18.494595223820948)
    assert reconstructed == pytest.approx(0.090)


def test_table_v_is_closed_by_composition_fixed_coupling() -> None:
    summary = analyze(SOURCE)
    closure = summary["global_closure"]

    assert summary["row_count"] == 66
    assert closure["maximum_p2_cv"] == pytest.approx(0.007826504048538074)
    assert closure["mass_rmse_m0"] == pytest.approx(0.0002730161154652197)
    assert closure["mass_max_abs_error_m0"] == pytest.approx(
        0.0004930296026296049
    )
    assert closure["mass_max_abs_error_m0"] < 0.0005


def test_cdte_endpoint_matches_table_vii_three_band_value() -> None:
    diagnostic = analyze(SOURCE)["p2_linear_diagnostic"]

    assert diagnostic["cdte_x1_ev"] == pytest.approx(18.48323447139118)
    assert abs(diagnostic["cdte_x1_ev"] - diagnostic["table_vii_cdte_ev"]) < 0.02


def test_temperature_dependence_is_not_independent_pt_evidence() -> None:
    summary = analyze(SOURCE)

    assert summary["source_kind"] == "historical_model_generated_tables_not_experiment"
    assert "not independent P(T) evidence" in summary["decision"]
    assert summary["composition_summaries"]["0.50"]["p2_cv"] < 0.002
    assert summary["composition_summaries"]["1.00"]["p2_cv"] < 0.004
