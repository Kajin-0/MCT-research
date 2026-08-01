from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from mct_research.r04_r05_literature_batch import (
    LiteratureBatchValidationError,
    load_literature_batch,
    validate_literature_batch,
)


RECORD_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "validation"
    / "r04_r05_literature_batch_001.json"
)


def record() -> dict:
    return load_literature_batch(RECORD_PATH)


def source_by_id(data: dict, source_id: str) -> dict:
    return next(source for source in data["sources"] if source["source_id"] == source_id)


def test_literature_batch_record_is_valid() -> None:
    validate_literature_batch(record())


def test_batch_remains_user_supplied_and_no_outreach() -> None:
    data = record()
    assert data["source_mode"] == "USER_SUPPLIED_PUBLISHED_PAPERS_ONLY"
    assert data["outreach_authorized"] is False
    assert data["cross_paper_specimen_synthesis"] is False
    assert data["r05_material_activation"] == "BLOCKED"


def test_chang_wafer_sigma_is_not_promoted_to_nanoscale_variance() -> None:
    chang = source_by_id(record(), "chang_2005_ir_mapping")
    assert chang["measurement"]["aperture_used_um"] == 100.0
    assert chang["measurement"]["measured_spatial_psf_reported"] is False
    assert chang["measurement"]["explicit_sampling_pitch_reported"] is False
    assert chang["gate_status"]["local_variance"] == "PARTIAL"
    assert chang["gate_status"]["correlation_length"] == "FAIL"
    prohibited = " ".join(chang["figure_reanalysis"]["prohibited_outputs"])
    assert "nanoscale correlation length" in prohibited
    assert "stationary random-field variance" in prohibited


def test_chang_numerical_convergence_is_not_measurement_uncertainty() -> None:
    chang = source_by_id(record(), "chang_2005_ir_mapping")
    assert chang["measurement"]["fit_stop_delta_x"] == 0.0001
    assert chang["measurement"]["fit_stop_delta_thickness_um"] == 0.01
    assert chang["measurement"]["measurement_uncertainty_propagated"] is False
    constraints = " ".join(chang["scientific_constraints"]).lower()
    assert "convergence thresholds are not measurement uncertainties" in constraints


def test_zha_topography_remains_an_artifact_constraint_not_a_mass_map() -> None:
    zha = source_by_id(record(), "zha_2012_nanopit_stm")
    observations = zha["quantitative_observations"]
    assert observations["pit_apparent_depth_change_nm"] == [20.0, 30.0]
    assert observations["flat_region_bias_inversion_step_nm"] == 30.0
    prohibited = " ".join(zha["figure_reanalysis"]["prohibited_outputs"]).lower()
    assert "mass or composition covariance" in prohibited
    assert "geometric pit-depth field from a single bias" in prohibited


def test_zha_apparent_gap_is_not_treated_as_local_dos_resolution() -> None:
    zha = source_by_id(record(), "zha_2012_nanopit_stm")
    observations = zha["quantitative_observations"]
    assert observations["flat_region_zero_current_plateau_eV"] == 0.40
    assert observations["bulk_reported_gap_eV"] == 0.27
    assert observations["apparent_plateau_excess_eV"] == pytest.approx(0.13)
    assert zha["specimen"]["stm_measurement_temperature"] == "NOT_REPORTED"
    assert zha["surface_and_instrument"]["lockin_modulation_reported"] is False
    assert zha["surface_and_instrument"]["measured_energy_kernel_reported"] is False
    assert zha["gate_status"]["resolution"] == "FAIL"


def test_cross_paper_gate_cannot_be_manufactured() -> None:
    data = record()
    mutated = copy.deepcopy(data)
    mutated["overall_decision"] = "QUALIFYING_PUBLISHED_DATA_FOUND"
    mutated["aggregate_findings"]["qualifying_single_source_found"] = True
    with pytest.raises(LiteratureBatchValidationError):
        validate_literature_batch(mutated)


def test_committing_copyrighted_pdf_is_rejected() -> None:
    data = record()
    mutated = copy.deepcopy(data)
    mutated["sources"][0]["copyrighted_pdf_committed"] = True
    with pytest.raises(LiteratureBatchValidationError):
        validate_literature_batch(mutated)


def test_unreported_stm_temperature_cannot_be_inferred() -> None:
    data = record()
    mutated = copy.deepcopy(data)
    zha = source_by_id(mutated, "zha_2012_nanopit_stm")
    zha["specimen"]["stm_measurement_temperature"] = 300
    with pytest.raises(LiteratureBatchValidationError):
        validate_literature_batch(mutated)


def test_record_round_trips_as_json() -> None:
    data = record()
    assert json.loads(json.dumps(data)) == data
