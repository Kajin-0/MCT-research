from __future__ import annotations

from pathlib import Path

import pytest

from tools.analyze_orlita2014_near_critical_constraint import analyze

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/experimental/orlita2014_primary_near_critical_constraint.csv"


def result() -> dict[str, object]:
    return analyze(DATA)


def test_orlita_audit_is_deterministic() -> None:
    assert result() == result()


def test_nominal_screen_prefers_laurenti_locally() -> None:
    audit = result()
    assert audit["nominal_winner"] == "laurenti"
    screen = audit["nominal_composition_model_screen"]
    assert screen["laurenti"]["predicted_gap_mev"] == pytest.approx(
        2.9559968781933095, abs=1e-10
    )
    assert screen["provisional_hansen_pade"]["predicted_gap_mev"] == pytest.approx(
        6.785532107209771, abs=1e-10
    )
    assert screen["hansen"]["predicted_gap_mev"] == pytest.approx(
        7.414196000000007, abs=1e-10
    )
    assert screen["chu_1983"]["predicted_gap_mev"] == pytest.approx(
        15.76752950000003, abs=1e-10
    )


def test_required_compositions_match_reference_values() -> None:
    inferred = result()["composition_required_for_reported_gap"]
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


def test_constraint_preserves_carrier_composition_and_lineage_caveats() -> None:
    audit = result()
    source = audit["source_record"]
    decision = audit["decision"]
    assert source["composition_precision_status"] == "approximate_graded_plateau"
    assert source["fermi_energy_mev"] == [15.0, 17.0]
    assert source["carrier_density_cm3"] == [2e14, 3e14]
    assert source["composition_profile_thickness_um"] == pytest.approx(3.2)
    assert source["source_lineage"] == "Mikhailov_Dvoretskii_MBE_magneto_optical_lineage"
    assert decision["central_source_recovery_status"] == "conditional"
    assert decision["exact_homogeneous_composition_gap_point"] is False
    assert decision["carrier_state_is_part_of_observation_operator"] is True
    assert decision["independent_cross_laboratory_validation"] is False
    assert decision["global_model_promotion_authorized"] is False
    assert decision["coefficient_refit_authorized"] is False
    assert decision["new_static_refit_authorized"] is False


def test_model_differences_are_composition_scale_diagnostics_not_refit_authority() -> None:
    audit = result()
    diagnostic = audit["cross_model_diagnostic"]
    assert diagnostic["maximum_model_equivalent_composition_offset"] == pytest.approx(
        0.006608010179444913, abs=1e-12
    )
    assert "independent homogeneous" in diagnostic[
        "composition_precision_needed_for_strict_ranking"
    ]
    assert "not an exact composition-gap calibration point" in audit["claim_boundary"]
