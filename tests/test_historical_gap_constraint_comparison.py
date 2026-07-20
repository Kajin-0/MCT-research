from __future__ import annotations

import math
from pathlib import Path

from mct_research.historical_gap_models import (
    schmit_stelzer_1969_gap_ev,
    seiler_1990_gap_ev,
)
from tools.analyze_historical_gap_constraints import analyze

ROOT = Path(__file__).resolve().parents[1]
SPECIMENS = ROOT / "data/evidence/hgcdte_historical_observation_specimens.json"
RECORDS = ROOT / "data/evidence/hgcdte_historical_observation_records.json"


def result() -> dict[str, object]:
    return analyze(SPECIMENS, RECORDS)


def test_historical_model_reference_values() -> None:
    assert math.isclose(
        schmit_stelzer_1969_gap_ev(0.262, 300),
        0.24389773565600006,
        abs_tol=1e-12,
    )
    assert math.isclose(
        seiler_1990_gap_ev(0.226, 300),
        0.19011175067821742,
        abs_tol=1e-12,
    )


def test_schmit_table_inventory_and_fit_adjustment() -> None:
    data = result()
    adjusted = data["schmit_cutoff_comparison"]["adjusted"]["schmit_stelzer_1969"]
    nominal = data["schmit_cutoff_comparison"]["nominal"]["schmit_stelzer_1969"]
    assert adjusted["count"] == 56
    assert adjusted["mae_meV"] < 1.8
    assert nominal["mae_meV"] > 7.0


def test_chu_is_best_independent_cutoff_comparator_but_not_global_winner() -> None:
    data = result()
    assert data["decision"]["best_independent_adjusted_cutoff_comparator"] == "chu_1983"
    assert data["schmit_cutoff_comparison"]["adjusted"]["chu_1983"]["mae_meV"] < 5.1
    assert data["decision"]["strict_global_model_ranking_authorized"] is False


def test_groves_same_specimen_sign_change_discriminates_models() -> None:
    data = result()
    assert data["decision"]["groves_4K_definite_violations"] == [
        "schmit_stelzer_1969"
    ]
    assert data["decision"]["groves_4K_composition_ambiguous"] == ["chu_1983"]
    sign_77k = next(
        row for row in data["sign_constraints"] if row["temperature_K"] == 77
    )
    assert all(
        model["status"] == "satisfied_entire_interval"
        for model in sign_77k["models"].values()
    )


def test_mccombe_point_remains_composition_limited() -> None:
    data = result()
    assert data["decision"]["mccombe_all_models_overpredict_at_reported_x"] is True
    assert (
        data["decision"]["mccombe_smallest_absolute_residual_model"]
        == "laurenti_reconstructed"
    )
    assert 19.0 < data["decision"]["mccombe_smallest_absolute_residual_meV"] < 19.01
    row = next(
        row
        for row in data["point_constraints"]
        if row["observation_id"] == "mccombe1970_sample4_gap"
    )
    assert row["models"]["hansen_1982"]["required_composition_shift"] < -0.014


def test_hgte_endpoint_rejects_schmit_endpoint_extrapolation() -> None:
    data = result()
    row = next(
        row
        for row in data["point_constraints"]
        if row["observation_id"] == "groves1967_hgte_gap_30K"
    )
    assert abs(row["models"]["hansen_1982"]["residual_meV"]) < 3.0
    assert abs(row["models"]["schmit_stelzer_1969"]["residual_meV"]) > 48.0
    assert data["decision"]["hgte_30K_smallest_absolute_residual_model"] == "hansen_1982"


def test_no_new_universal_refit_is_authorized() -> None:
    assert result()["decision"]["new_universal_gap_refit_authorized"] is False
