from pathlib import Path

from tools.analyze_moazzami2005_real_spectra import analyze

ROOT = Path(__file__).resolve().parents[1]


def test_two_real_spectra_pass_the_contract_gate() -> None:
    result = analyze(ROOT)
    assert result["decision"]["real_spectrum_count"] == 2
    assert result["decision"]["contract_gate_passed"] is True
    assert [item["digitized_point_count"] for item in result["specimens"]] == [125, 115]


def test_fractional_power_model_uncertainty_is_multi_mev() -> None:
    result = analyze(ROOT)
    spans = [item["model_family_envelope"]["full_span_mev"] for item in result["specimens"]]
    assert 6.0 < spans[0] < 7.0
    assert 6.0 < spans[1] < 7.5


def test_material_model_ranking_changes_only_when_threshold_definition_changes() -> None:
    result = analyze(ROOT)
    decision = result["decision"]
    assert decision["material_model_winner_changes_across_declared_observation_candidates"] is True
    assert decision["fractional_power_candidates_alone_change_material_model_winner"] is False
    assert decision["fixed_threshold_candidates_change_material_model_winner"] is True
    for specimen in result["specimens"]:
        assert specimen["model_candidate_winners"] == ["hansen"]


def test_boundary_limited_candidates_are_reported() -> None:
    result = analyze(ROOT)
    by_id = {item["specimen_id"]: item for item in result["specimens"]}
    assert "chu_1994_kane_region" in by_id["moazzami2005_x0.226"]["boundary_limited_model_candidates"]
    assert "chu_1994_kane_region" in by_id["moazzami2005_x0.310"]["boundary_limited_model_candidates"]


def test_no_single_gap_or_universal_correction_is_authorized() -> None:
    decision = analyze(ROOT)["decision"]
    assert decision["universal_correction_authorized"] is False
    assert decision["single_edge_selection_authorized"] is False
