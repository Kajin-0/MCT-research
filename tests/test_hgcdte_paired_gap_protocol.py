from __future__ import annotations

from copy import deepcopy
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.audit_hgcdte_paired_gap_acquisition import (  # noqa: E402
    audit,
    materialize_planning_observations,
)

TEMPLATE = ROOT / "data/templates/hgcdte_paired_gap_acquisition_template.json"
REFERENCE = ROOT / "data/derived/hgcdte_paired_gap_protocol_reference_audit.json"
ROLES = (
    "material_provider",
    "composition_metrology_lab",
    "hall_and_defect_lab",
    "absorption_lab",
    "magneto_optical_lab",
    "analysis_owner",
    "data_archive",
)


def planning_template() -> dict[str, object]:
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def completed_package() -> dict[str, object]:
    payload = deepcopy(planning_template())
    payload["status"] = "completed_package"
    for role in ROLES:
        payload["collaboration"][role] = f"Example {role.replace('_', ' ')}"

    blocks = {
        item["block_id"]: item
        for item in payload["design"]["temperature_blocks"]
    }
    for specimen in payload["specimens"]:
        specimen_id = specimen["specimen_id"]
        codes = specimen["nominal_codes"]
        lineage = specimen["lineage"]
        lineage.update(
            {
                "wafer_id": f"WAFER_{specimen_id}",
                "growth_method": "LPE example",
                "growth_run_id": "GROWTH_001",
                "passivation": "none during paired measurements",
                "contact_state": "reversible peripheral contacts",
                "storage_history": "dry nitrogen archive",
            }
        )
        specimen["composition"].update(
            {
                "method": "independent calibrated microprobe",
                "calibration_id": "COMP_CAL_001",
            }
        )
        specimen["thickness"].update(
            {
                "value_um": 10.0,
                "sigma_um": 0.05,
                "method": "calibrated cross-section metrology",
                "lateral_uniformity_fraction": 0.01,
            }
        )
        state_by_temperature = {}
        for block_id in blocks:
            carrier_code = int(codes["carrier"])
            vacancy_code = int(codes["vacancy"])
            state_by_temperature[block_id] = {
                "carrier": {
                    "polarity": "n",
                    "density_cm3": 1.0e14 if carrier_code < 0 else 1.0e16,
                    "sigma_log10_density": 0.05,
                    "mobility_cm2_Vs": 5.0e4 if block_id == "T006" else 2.0e4,
                    "sigma_mobility_cm2_Vs": 1.0e3,
                    "method": "van der Pauw Hall",
                    "calibration_id": f"HALL_{block_id}",
                    "assignment_basis": "same_specimen",
                    "witness_specimen_id": None,
                    "transfer_uncertainty_record_uri": None,
                },
                "vacancy_proxy": {
                    "value": -1.0 if vacancy_code < 0 else 1.0,
                    "sigma": 0.1,
                    "units": "standardized calibrated proxy",
                    "method": "quantitative vacancy-sensitive assay",
                    "calibration_id": f"VAC_{block_id}",
                    "assignment_basis": "same_specimen",
                    "witness_specimen_id": None,
                    "transfer_uncertainty_record_uri": None,
                },
                "processing_between_paired_modalities": False,
                "state_drift_check": {
                    "pre_post_hall_fractional_change": 0.02,
                    "maximum_allowed_fractional_change": 0.10,
                },
            }
        specimen["state_by_temperature"] = state_by_temperature

    observations = materialize_planning_observations(payload)
    for observation in observations:
        block_id = observation["temperature_block_id"]
        specimen_id = observation["specimen_id"]
        modality = observation["modality"]
        target_temperature = float(blocks[block_id]["target_temperature_K"])
        token = f"{block_id}:{specimen_id}:{modality}".encode()
        observation.update(
            {
                "measurement_area_id": f"AREA_{block_id}_{specimen_id}",
                "status": "complete",
                "technical_replicate_count": 3,
                "raw_data": {
                    "native_uri": f"archive://raw/{block_id}/{specimen_id}/{modality}.h5",
                    "sha256": hashlib.sha256(token).hexdigest(),
                    "format": "HDF5",
                },
                "calibration_ids": [f"ENERGY_{block_id}", f"TEMPERATURE_{block_id}"],
                "temperature": {
                    "measured_K": target_temperature,
                    "sigma_K": 0.05 if block_id == "T006" else 0.10,
                },
                "extraction": {
                    "edge_eV": 0.15 + 0.01 * int(specimen_id[1:]),
                    "sigma_edge_eV": 0.001,
                    "method_id": (
                        "calibrated_magneto_optical_fit_v1"
                        if modality == "magneto_optical"
                        else "complete_absorption_edge_ensemble_v1"
                    ),
                    "software_commit": "0123456789abcdef0123456789abcdef01234567",
                    "covariance_uri": f"archive://covariance/{observation['observation_id']}.json",
                    "analysis_record_uri": f"archive://analysis/{observation['observation_id']}.json",
                },
            }
        )
    payload["observations"] = observations
    return payload


def test_planning_template_inventory_and_nominal_diagnostics() -> None:
    result = audit(planning_template(), mode="planning")
    assert result["decision"]["planning_template_valid"] is True
    assert result["inventory"] == {
        "specimen_count": 8,
        "temperature_block_count": 2,
        "modality_count": 2,
        "primary_observation_count": 32,
        "completed_observation_count": 0,
    }
    for block in result["temperature_blocks"].values():
        diagnostics = block["design_diagnostics"]
        assert diagnostics["observation_count"] == 16
        assert diagnostics["parameter_count"] == 5
        assert diagnostics["rank"] == 5
        assert diagnostics["residual_degrees_of_freedom"] == 11
        assert math.isclose(diagnostics["condition_number"], 2.618033988749895, abs_tol=1e-12)
        assert math.isclose(diagnostics["maximum_leverage"], 0.4375, abs_tol=1e-12)
        assert math.isclose(block["carrier_vacancy_correlation"], 0.0, abs_tol=1e-12)


def test_template_contains_complete_factorial_and_randomized_orders() -> None:
    payload = planning_template()
    states = {
        tuple(specimen["nominal_codes"][name] for name in ("composition", "carrier", "vacancy"))
        for specimen in payload["specimens"]
    }
    assert states == set(itertools.product((-1, 1), repeat=3))
    for order in payload["observation_plan"]["orders"].values():
        assert len(order) == 16
        assert len(set(order)) == 16
        assert order != sorted(order)


def assert_nested_close(left: object, right: object) -> None:
    if isinstance(left, dict):
        assert isinstance(right, dict)
        assert set(left) == set(right)
        for key in left:
            assert_nested_close(left[key], right[key])
        return
    if isinstance(left, list):
        assert isinstance(right, list)
        assert len(left) == len(right)
        for left_item, right_item in zip(left, right, strict=True):
            assert_nested_close(left_item, right_item)
        return
    if isinstance(left, float):
        assert isinstance(right, (int, float))
        assert math.isclose(left, float(right), rel_tol=1e-10, abs_tol=1e-12)
        return
    assert left == right


def test_frozen_reference_audit_matches_planning_result() -> None:
    reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    result = audit(planning_template(), mode="planning")
    assert reference["decision"] == result["decision"]
    assert reference["inventory"] == result["inventory"]
    assert reference["composition"] == result["composition"]
    assert_nested_close(reference["temperature_blocks"], result["temperature_blocks"])


def test_completed_package_passes_all_gates() -> None:
    result = audit(completed_package(), mode="completed")
    assert result["decision"]["completed_package_audit_grade"] is True
    assert all(result["decision"]["gates"].values())
    assert result["inventory"]["completed_observation_count"] == 32


def test_missing_paired_observation_fails_closed() -> None:
    payload = completed_package()
    payload["observations"].pop()
    with pytest.raises(ValueError, match="exactly 32"):
        audit(payload, mode="completed")


def test_composition_uncertainty_above_hard_limit_fails_gate() -> None:
    payload = completed_package()
    payload["specimens"][0]["composition"]["sigma_x"] = 0.002
    result = audit(payload, mode="completed")
    assert result["decision"]["gates"]["composition_hard_maximum"] is False
    assert result["decision"]["completed_package_audit_grade"] is False


def test_mixed_carrier_polarity_fails_gate() -> None:
    payload = completed_package()
    payload["specimens"][0]["state_by_temperature"]["T006"]["carrier"]["polarity"] = "p"
    result = audit(payload, mode="completed")
    assert result["temperature_blocks"]["T006"]["carrier_polarity_pass"] is False
    assert result["decision"]["completed_package_audit_grade"] is False


def test_processing_or_state_drift_fails_gate() -> None:
    processing = completed_package()
    processing["specimens"][0]["state_by_temperature"]["T006"][
        "processing_between_paired_modalities"
    ] = True
    result = audit(processing, mode="completed")
    assert result["decision"]["gates"]["processing_frozen"] is False

    drift = completed_package()
    drift["specimens"][0]["state_by_temperature"]["T006"]["state_drift_check"][
        "pre_post_hall_fractional_change"
    ] = 0.20
    result = audit(drift, mode="completed")
    assert result["decision"]["gates"]["state_drift"] is False


def test_carrier_vacancy_aliasing_fails_correlation_gate() -> None:
    payload = completed_package()
    for specimen in payload["specimens"]:
        carrier_code = int(specimen["nominal_codes"]["carrier"])
        vacancy_code = int(specimen["nominal_codes"]["vacancy"])
        log_density = (14.0 if carrier_code < 0 else 16.0) + 0.8 * vacancy_code
        for state in specimen["state_by_temperature"].values():
            state["carrier"]["density_cm3"] = 10.0**log_density
    result = audit(payload, mode="completed")
    assert abs(result["temperature_blocks"]["T006"]["carrier_vacancy_correlation"]) > 0.5
    assert result["decision"]["gates"]["carrier_vacancy_correlation"] is False


def test_invalid_raw_sha_fails_closed() -> None:
    payload = completed_package()
    payload["observations"][0]["raw_data"]["sha256"] = "not-a-sha"
    with pytest.raises(ValueError, match="SHA-256"):
        audit(payload, mode="completed")


def test_mismatched_measurement_area_fails_pairing() -> None:
    payload = completed_package()
    first = payload["observations"][0]
    paired = next(
        item
        for item in payload["observations"]
        if item["temperature_block_id"] == first["temperature_block_id"]
        and item["specimen_id"] == first["specimen_id"]
        and item["modality"] != first["modality"]
    )
    paired["measurement_area_id"] = "DIFFERENT_AREA"
    with pytest.raises(ValueError, match="co-registered"):
        audit(payload, mode="completed")


def test_witness_assignment_requires_transfer_uncertainty_record() -> None:
    payload = completed_package()
    carrier = payload["specimens"][0]["state_by_temperature"]["T006"]["carrier"]
    carrier["assignment_basis"] = "witness"
    carrier["witness_specimen_id"] = "WITNESS_001"
    with pytest.raises(ValueError, match="transfer uncertainty"):
        audit(payload, mode="completed")
    carrier["transfer_uncertainty_record_uri"] = "archive://transfer/WITNESS_001.json"
    assert audit(payload, mode="completed")["decision"]["completed_package_audit_grade"] is True
