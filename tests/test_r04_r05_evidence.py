from __future__ import annotations

import copy
import json
from pathlib import Path

from mct_research.r04_r05_evidence import validate_evidence_record


ROOT = Path(__file__).resolve().parents[1]


def _template() -> dict[str, object]:
    path = ROOT / "data" / "templates" / "r04_r05_matched_evidence_template.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _schema() -> dict[str, object]:
    path = ROOT / "data" / "schemas" / "r04_r05_matched_evidence_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_normative_schema_preserves_frozen_conventions() -> None:
    schema = _schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    properties = schema["properties"]
    inference = properties["joint_inference"]["properties"]
    assert inference["gap_to_mass_convention"]["const"] == "M=Eg/2"
    assert inference["g_threshold_lower"]["const"] == 0.25
    assert inference["g_threshold_upper"]["const"] == 0.3
    spatial = properties["spatial_measurement"]["properties"]
    assert spatial["wafer_tolerance_used_as_local_sigma"]["const"] is False


def test_nonclaiming_template_is_internally_valid() -> None:
    result = validate_evidence_record(_template())
    assert result.is_valid, result.errors


def test_wafer_tolerance_cannot_be_used_as_local_sigma() -> None:
    record = _template()
    record["spatial_measurement"]["wafer_tolerance_used_as_local_sigma"] = True
    result = validate_evidence_record(record)
    assert not result.is_valid
    assert any("wafer_tolerance_used_as_local_sigma" in error for error in result.errors)


def test_covariance_family_check_requires_gaussian_and_matern() -> None:
    record = _template()
    record["spatial_measurement"]["covariance_families"] = ["gaussian"]
    result = validate_evidence_record(record)
    assert not result.is_valid
    assert any("Matérn" in error for error in result.errors)


def test_universal_resolution_claim_is_rejected() -> None:
    record = _template()
    kernel = record["spectroscopy_measurement"]["energy_resolution_kernel"]
    kernel["universal_requirement_claimed"] = True
    result = validate_evidence_record(record)
    assert not result.is_valid
    assert any("universal_requirement_claimed" in error for error in result.errors)


def test_reactivation_cannot_use_unresolved_template_evidence() -> None:
    record = _template()
    record["decision"] = "R05_REACTIVATION_RECOMMENDED"
    for gate in record["gates"].values():
        gate["status"] = "PASS"
        gate["reason"] = "Placeholder pass used to test claim enforcement."
    record["joint_inference"]["m_max_frozen_before_final_comparison"] = True
    result = validate_evidence_record(record)
    assert not result.is_valid
    assert any("exploratory or unresolved evidence" in error for error in result.errors)
    assert any("unlinked" in error for error in result.errors)


def test_reactivation_requires_every_gate_to_pass() -> None:
    record = copy.deepcopy(_template())
    record["decision"] = "R05_REACTIVATION_RECOMMENDED"
    record["gates"]["local_variance_gate"]["status"] = "FAIL"
    result = validate_evidence_record(record)
    assert not result.is_valid
    assert any("every gate to PASS" in error for error in result.errors)
