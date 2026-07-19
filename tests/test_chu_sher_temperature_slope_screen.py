from __future__ import annotations

from pathlib import Path

import pytest

from tools.audit_chu_sher_temperature_slope_screen import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/chu_sher_2008_table3_7_temperature_coefficients.csv"


def result() -> dict[str, object]:
    return analyze(DATA)


def test_secondary_screen_preserves_source_boundary() -> None:
    audit = result()
    assert audit["source_record_count"] == 10
    assert audit["composition_range"] == pytest.approx([0.200, 0.443])
    assert audit["decision"]["primary_fit_authority"] is False
    assert audit["decision"]["coefficient_refit_authorized"] is False
    assert audit["decision"]["global_model_ranking_authorized"] is False
    assert "Secondary screen only" in audit["claim_boundary"]


def test_linear_model_coefficients_are_operator_invariant() -> None:
    diagnostics = result()["cross_operator_diagnostics"]
    differences = diagnostics[
        "linear_model_maximum_operator_difference_1e4_ev_per_k"
    ]
    assert differences["hansen"] <= 1.0e-12
    assert differences["chu_1983"] <= 1.0e-12


def test_nonlinear_model_ranking_depends_on_slope_operator() -> None:
    audit = result()
    diagnostics = audit["cross_operator_diagnostics"]
    assert diagnostics["winner_changes_with_nonlinear_slope_operator"] is True
    assert diagnostics["winners_by_operator"] == {
        "local_derivative_at_300_k": "chu_1983",
        "secant_80_to_300_k": "chu_1983",
        "secant_4p2_to_300_k": "laurenti",
    }
    assert audit["decision"]["screen_identifies_operator_dependence"] is True


def test_declared_rmse_values_match_reference() -> None:
    operators = result()["operator_results"]
    local = operators["local_derivative_at_300_k"]["models"]
    high_temperature = operators["secant_80_to_300_k"]["models"]
    full_range = operators["secant_4p2_to_300_k"]["models"]

    assert local["chu_1983"]["metrics"]["rmse_1e4_ev_per_k"] == pytest.approx(
        0.10519840925460804, abs=1.0e-13
    )
    assert high_temperature["hansen"]["metrics"][
        "rmse_1e4_ev_per_k"
    ] == pytest.approx(0.14347938179404043, abs=1.0e-13)
    assert full_range["laurenti"]["metrics"][
        "rmse_1e4_ev_per_k"
    ] == pytest.approx(0.08250460716651327, abs=1.0e-13)


def test_provisional_model_is_systematically_steeper_in_this_screen() -> None:
    audit = result()
    diagnostics = audit["cross_operator_diagnostics"]
    assert diagnostics["provisional_hansen_pade_rank_by_operator"] == {
        "local_derivative_at_300_k": 4,
        "secant_80_to_300_k": 4,
        "secant_4p2_to_300_k": 4,
    }
    assert diagnostics[
        "provisional_alpha_relative_to_hansen_slope_amplitude"
    ] == pytest.approx(0.10621927436198364, abs=1.0e-15)
    assert audit["decision"][
        "provisional_model_is_last_under_all_declared_operators"
    ] is True


def test_source_family_screen_does_not_select_a_universal_law() -> None:
    interpretation = result()["decision"]["interpretation"]
    assert "cross-source screen" in interpretation
    assert "cannot select or refit a universal material law" in interpretation
