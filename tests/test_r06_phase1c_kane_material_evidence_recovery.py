import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = (
    REPOSITORY_ROOT
    / "configs"
    / "transport_noise"
    / "kane_material_evidence_candidates.json"
)
GATE_PATH = (
    REPOSITORY_ROOT
    / "configs"
    / "transport_noise"
    / "kane_material_validation_gate.json"
)


def load_candidates() -> dict:
    return json.loads(CANDIDATE_PATH.read_text(encoding="utf-8"))


def load_gate() -> dict:
    return json.loads(GATE_PATH.read_text(encoding="utf-8"))


def candidates_by_id() -> dict[str, dict]:
    return {
        candidate["source_id"]: candidate
        for candidate in load_candidates()["candidates"]
    }


def test_candidate_ledger_remains_blocked_with_zero_accepted_points() -> None:
    ledger = load_candidates()
    assert ledger["status"] == "blocked_no_accepted_hgcdte_reference_set"
    assert ledger["accepted_material_evidence"] == []
    assert ledger["summary"]["countable_pr385_point_count"] == 0


def test_candidate_sources_have_unique_ids_dois_and_provenance_groups() -> None:
    candidates = load_candidates()["candidates"]
    assert len(candidates) == 6
    for key in ("source_id", "doi", "provenance_group"):
        values = [candidate[key] for candidate in candidates]
        assert len(values) == len(set(values))
        assert all(str(value).strip() for value in values)


def test_nemirovsky_finkman_is_priority_direct_density_but_not_countable() -> None:
    source = candidates_by_id()["NEMIROVSKY_FINKMAN_1979"]
    assert source["source_class"] == "primary_experimental_intrinsic_density"
    assert source["disposition"] == "priority_1_primary_data_recovery"
    assert source["independent_or_primary"]
    assert source["hgcdte_specific"]
    assert source["point_level_values_recovered"] is False
    assert source["positive_standard_uncertainties_recovered"] is False
    assert source["eta_known"] is False
    assert source["validated_neutrality_model_recovered"] is False
    assert source["countable_as_accepted_material_evidence"] is False


def test_finkman_parameter_inversion_is_not_silently_mapped_to_project_alpha() -> None:
    source = candidates_by_id()["FINKMAN_1983"]
    assert source["source_class"] == "primary_experimental_hall_parameter_inversion"
    assert "indirect_nonparabolic_band_parameter_candidate" in source[
        "pr385_observable_mapping"
    ]
    assert any(
        "cannot be mapped silently" in reason
        for reason in source["blocking_reasons"]
    )
    assert source["countable_as_accepted_material_evidence"] is False


def test_historical_calculated_density_sources_remain_model_benchmarks() -> None:
    sources = candidates_by_id()
    for source_id in (
        "HANSEN_SCHMIT_1983",
        "SEILER_LOWNEY_LITTLER_YOON_1991",
        "LOWNEY_SEILER_LITTLER_YOON_1992",
    ):
        source = sources[source_id]
        assert "model" in " ".join(source["pr385_observable_mapping"])
        assert source["countable_as_accepted_material_evidence"] is False


def test_nist_precursor_pins_architecture_without_creating_material_points() -> None:
    source = candidates_by_id()["SEILER_LOWNEY_LITTLER_YOON_1991"]
    assert source["recovered_parameters"] == {
        "split_off_energy_ev": 1.0,
        "momentum_matrix_element_ev_cm": 8.49e-08,
        "heavy_hole_mass_m0": 0.55,
    }
    assert source["point_level_values_recovered"] is False
    assert source["positive_standard_uncertainties_recovered"] is False
    assert source["eta_known"] is False
    assert source["countable_as_accepted_material_evidence"] is False


def test_no_direct_compressibility_or_einstein_sources_were_recovered() -> None:
    summary = load_candidates()["summary"]
    assert summary["direct_compressibility_source_count"] == 0
    assert summary["direct_generalized_einstein_source_count"] == 0
    failures = load_candidates()["contract_failures"]
    assert "no recovered direct chemical-compressibility measurements" in failures
    assert "no recovered direct generalized-Einstein-factor measurements" in failures


def test_tepppe_source_is_uncertainty_bearing_but_indirect() -> None:
    source = candidates_by_id()["TEPPE_ET_AL_2016"]
    assert source["source_class"] == "primary_experimental_band_structure"
    assert source["positive_standard_uncertainties_recovered"]
    assert source["pr385_observable_mapping"] == [
        "indirect_nonparabolic_model_adequacy_constraint"
    ]
    assert source["disposition"] == (
        "retain_for_simplified_versus_three_band_adequacy"
    )
    assert source["countable_as_accepted_material_evidence"] is False


def test_every_candidate_remains_noncountable() -> None:
    candidates = load_candidates()["candidates"]
    assert all(
        candidate["countable_as_accepted_material_evidence"] is False
        for candidate in candidates
    )


def test_existing_material_authorization_boundary_is_unchanged() -> None:
    gate = load_gate()
    assert gate["status"] == "blocked_no_accepted_hgcdte_reference_set"
    assert gate["accepted_material_evidence"] == []
    for key in (
        "material_parameter_values_authorized",
        "equilibrium_density_authorized",
        "chemical_compressibility_authorized",
        "screening_authorized",
        "detector_coupling_authorized",
        "predictive_noise_claims_authorized",
    ):
        assert gate[key] is False


def test_recovery_queue_prioritizes_primary_data_and_shape_evidence() -> None:
    actions = load_candidates()["next_recovery_actions"]
    assert "Nemirovsky-Finkman 1979" in actions[0]
    assert "Finkman 1983" in actions[1]
    assert any("chemical-compressibility" in action for action in actions)
    assert actions[-1] == (
        "keep fitting, screening, detector coupling, and predictive noise blocked"
    )
