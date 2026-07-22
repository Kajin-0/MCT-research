from __future__ import annotations

import json
from pathlib import Path


LEDGER_PATH = Path("data/validation/r04_public_data_recovery_ledger.json")


def _ledger() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _records_by_id() -> dict[str, dict]:
    return {item["record_id"]: item for item in _ledger()["records"]}


def test_public_recovery_is_fail_closed_and_contact_free() -> None:
    ledger = _ledger()
    policy = ledger["communication_policy"]
    authorization = ledger["authorization"]

    assert ledger["schema_version"] == "1.0"
    assert ledger["portfolio_contribution"] == "R04"
    assert ledger["parent_issue"] == 290
    assert ledger["recovery_issues"] == [297, 299, 307]
    assert ledger["status"] == "external_data_blocked"

    assert policy["external_contact_permitted"] is False
    assert policy["email_permitted"] is False
    assert policy["direct_messages_permitted"] is False
    assert policy["author_or_institutional_outreach_permitted"] is False
    assert policy["request_for_data_communication_permitted"] is False
    assert policy["permitted_recovery_mode"] == "public_records_only"

    assert authorization == {
        "source_native_analysis_branch_authorized": False,
        "covariance_family_fitting_authorized": False,
        "publication_figure_digitization_as_source_data_authorized": False,
        "new_r04_mechanism_authorized": False,
        "r05_computation_authorized": False,
        "manuscript_authorized": False,
    }


def test_headline_preserves_zero_qualification_result() -> None:
    headline = _ledger()["headline"]

    assert headline["complete_user_supplied_pdfs_audited"] == 3
    assert headline["public_source_native_packages_found"] == 0
    assert headline["qualified_direct_validation_packages"] == 0
    assert headline["records_confirming_native_data_originally_existed"] == 2
    assert headline["strongest_same_region_cross_modality_lead"] == (
        "furstenberg_2005_same_region_pl_transmission"
    )
    assert headline["strongest_physical_two_scale_lead"] == (
        "gopal_1992_two_beam_transmission"
    )
    assert headline["strongest_measured_pump_kernel_contract"] == (
        "chen_2019_ssftir_pl_mapping"
    )


def test_supplied_pdf_hashes_and_object_boundaries_are_exact() -> None:
    records = _records_by_id()

    gopal = records["gopal_1992_two_beam_transmission"]
    chen = records["chen_2019_ssftir_pl_mapping"]
    furstenberg = records["furstenberg_2005_same_region_pl_transmission"]

    assert gopal["user_supplied_pdf_sha256"] == (
        "dda85e0b6f8ceece323ffe8436084868112e1fb2679c189a1e7563e3f4aabe34"
    )
    assert chen["user_supplied_pdf_sha256"] == (
        "84d849ee955a7580b59c8643714768b4080832249a032432d53070d72c52672d"
    )
    assert furstenberg["user_supplied_pdf_sha256"] == (
        "b77621b6c8093d8c1d3295f4172255f6abd118b3f5343c42481a5892ab8a3cb3"
    )

    for record in (gopal, chen, furstenberg):
        audit = record["pdf_object_audit"]
        assert audit["embedded_file_count"] == 0
        assert record["source_native_public_package_found"] is False

    assert gopal["pdf_object_audit"]["source_native_spectra_present"] is False
    assert chen["pdf_object_audit"]["source_native_spectral_cube_present"] is False
    assert furstenberg["pdf_object_audit"]["source_native_map_arrays_present"] is False


def test_gopal_two_scale_result_is_not_misread_as_variance_data() -> None:
    gopal = _records_by_id()["gopal_1992_two_beam_transmission"]
    contract = gopal["instrument_contract"]
    result = gopal["source_bounded_result"]
    boundary = gopal["critical_interpretation_boundary"]

    assert gopal["doi"] == "10.1016/0020-0891(92)90053-V"
    assert contract["instrument"] == "FTS-40 FTIR"
    assert contract["nominal_beam_diameters_micrometre"] == [3000.0, 250.0]
    assert contract["physical_scale_count"] == 2
    assert contract["measured_psf_available"] is False
    assert contract["beam_center_registration_available"] is False
    assert result["focused_beam_z_half_composition_estimate"] == 0.2255
    assert result["focused_beam_z_intercept_composition_estimate"] == 0.2304
    assert "not compositions assigned independently" in boundary
    assert "not a two-scale variance datum" in boundary


def test_chen_instrument_contract_is_preserved_without_composition_claim() -> None:
    chen = _records_by_id()["chen_2019_ssftir_pl_mapping"]
    contract = chen["instrument_contract"]
    observation = chen["material_and_observation"]

    assert chen["doi"] == "10.1063/1.5111788"
    assert contract["pump_spot_diameter_1_over_e2_micrometre"] == 26.3
    assert contract["pump_spot_diameter_half_maximum_micrometre"] == 15.3
    assert contract["raster_step_micrometre"] == [40.0, 40.0]
    assert contract["stage_translation_resolution_micrometre"] == 1.0
    assert contract["stage_angular_resolution_degree"] == 0.002
    assert contract["lw_ir_map_grid"] == [25, 25]
    assert contract["lw_ir_map_area_micrometre"] == [960.0, 960.0]
    assert contract["lw_ir_spectral_resolution_cm_inverse"] == 12.0
    assert contract["lw_ir_snr_lower_bound"] == 30.0
    assert observation["composition_field_directly_observed"] is False
    assert "interface roughness" in observation["declared_possible_latent_causes"]


def test_furstenberg_same_region_contract_and_nuisance_boundaries() -> None:
    furstenberg = _records_by_id()["furstenberg_2005_same_region_pl_transmission"]
    contract = furstenberg["same_region_contract"]
    boundaries = " ".join(furstenberg["critical_interpretation_boundaries"])

    assert furstenberg["doi"] == "10.1007/s11664-005-0022-8"
    assert contract["sample"] == "HRL3307"
    assert contract["map_area_micrometre"] == [1200.0, 1200.0]
    assert contract["reported_map_resolution_micrometre"] == 25.0
    assert contract["nominal_grid_implied_by_area"] == [48, 48]
    assert contract["same_region_explicitly_reported"] is True
    assert contract["highest_attainable_resolution_micrometre"] == 10.0
    assert "physical thickness, composition fluctuation, and Te inclusions" in boundaries
    assert "not a direct composition observable" in boundaries
    assert "not two probe scales" in boundaries


def test_dissertation_confirms_native_file_existence_not_public_recovery() -> None:
    thesis = _records_by_id()["furstenberg_2006_dissertation"]
    acquisition = thesis["acquisition_and_processing_contract"]
    mapping = thesis["same_region_map_contract"]

    assert thesis["persistent_identifier"] == "hdl:2142/34731"
    assert thesis["native_data_originally_existed"] is True
    assert thesis["native_data_publicly_recovered"] is False
    assert acquisition["ftir_platform"] == "ThermoNicolet Nexus 670 rapid scan"
    assert acquisition["parallel_interferograms"] == ["PL", "transmission or background"]
    assert "stored on a hard drive" in acquisition["storage"]
    assert acquisition["processing_chain"] == [
        "coherent addition",
        "apodization",
        "phase correction",
        "Fourier transform",
    ]
    assert mapping["grid"] == [48, 48]
    assert mapping["temperature_runs_k"] == [300.0, 77.0]
    assert mapping["acquisition_seconds_per_pixel"] == [19.0, 8.4]
    assert thesis["public_companion_dataset_found"] is False


def test_public_lineage_targets_are_search_results_not_data_packages() -> None:
    targets = _ledger()["public_lineage_targets"]
    by_doi = {item["doi"]: item for item in targets}

    assert set(by_doi) == {
        "10.1007/s11664-004-0071-4",
        "10.1063/1.2214931",
        "10.1063/5.0164195",
        "10.1063/5.0244755",
    }
    assert all(
        item["source_native_package_status"]
        == "not_located_in_declared_public_search"
        for item in targets
    )


def test_gate_and_claim_boundaries_prohibit_substitution() -> None:
    ledger = _ledger()
    gate = ledger["qualification_gate"]
    stops = " ".join(ledger["stop_rules"])
    claims = " ".join(ledger["claim_boundaries"])

    assert "at least three calibrated effective scales" in gate["accepted_package_A"]
    assert "one original high-resolution numerical map" in gate["accepted_package_B"]
    assert "No publication-figure extraction" in stops
    assert "No nominal beam diameter or quoted spot size" in stops
    assert "No raster pixel count" in stops
    assert "No multiple-modality record" in stops
    assert "does not prove that private or unindexed data do not exist" in claims
    assert "does not support Q_G evaluation" in claims
    assert "No specimen covariance" in claims
    assert "R05 computation" in claims
