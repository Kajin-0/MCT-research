from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_orlita2014_near_critical_constraint import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/orlita2014_primary_near_critical_constraint.csv"


def test_orlita_audit_is_deterministic() -> None:
    assert analyze(DATA) == analyze(DATA)


def test_nominal_screen_prefers_laurenti_locally() -> None:
    result = analyze(DATA)
    assert result["nominal_winner"] == "laurenti"
    screen = result["nominal_composition_model_screen"]
    assert screen["laurenti"]["predicted_gap_mev"] == pytest.approx(
        2.9559968781933095, abs=1e-10
    )
    assert screen["provisional_hansen_pade"]["predicted_gap_mev"] == pytest.approx(
        6.785532107209771, abs=1e-10
    )
    assert screen["hansen"]["predicted_gap_mev"] == pytest.approx(
        7.414196000000007, abs=1e-10
    )


def test_required_compositions_match_reference_values() -> None:
    inferred = analyze(DATA)["composition_required_for_reported_gap"]
    assert inferred["laurenti"]["composition_for_4mev_gap"] == pytest.approx(
        0.17057311346319876, abs=1e-10
    )
    assert inferred["provisional_hansen_pade"][
        "composition_for_4mev_gap"
    ] == pytest.approx(0.16838738404572456, abs=1e-10)
    assert inferred["hansen"]["composition_for_4mev_gap"] == pytest.approx(
        0.16802141519260283, abs=1e-10
    )
    assert inferred["chu_1983"]["composition_for_4mev_gap"] == pytest.approx(
        0.1633919898205551, abs=1e-10
    )


def test_constraint_preserves_carrier_and_composition_caveats() -> None:
    result = analyze(DATA)
    source = result["source_record"]
    decision = result["decision"]
    assert source["composition_precision_status"] == "approximate_graded_plateau"
    assert source["fermi_energy_mev"] == [15.0, 17.0]
    assert source["carrier_density_cm3"] == [2e14, 3e14]
    assert source["composition_profile_thickness_um"] == pytest.approx(3.2)
    assert decision["exact_homogeneous_composition_gap_point"] is False
    assert decision["carrier_state_is_part_of_observation_operator"] is True
    assert decision["global_model_promotion_authorized"] is False
    assert decision["coefficient_refit_authorized"] is False
