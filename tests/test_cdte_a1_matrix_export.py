from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from mct_research.thermal_kane import gamma_irrep_matrix
from tools.validate_cdte_a1_matrix_export import validate


def _contract() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    return json.loads(
        (
            root
            / "first_principles/a1/cdte_matrix_self_energy_export_contract.json"
        ).read_text(encoding="utf-8")
    )


def _payload(contract: dict[str, object]) -> dict[str, object]:
    fan_real = gamma_irrep_matrix(0.003, -0.001, 0.002).real.tolist()
    fan_imag = (-0.001 * np.eye(8)).tolist()
    dw = gamma_irrep_matrix(0.001, 0.0005, -0.0002).real.tolist()
    derivative = gamma_irrep_matrix(0.05, 0.03, 0.04).real.tolist()
    total = (np.asarray(fan_real) + np.asarray(dw)).tolist()
    records = []
    for temperature in contract["temperature_grid_k"]:
        for label in contract["k_points_inverse_angstrom"]:
            records.append(
                {
                    "temperature_k": temperature,
                    "k_label": label,
                    "fan_real_ev": fan_real,
                    "fan_imag_ev": fan_imag,
                    "debye_waller_real_ev": dw,
                    "fan_derivative_real": derivative,
                    "total_real_ev": total,
                }
            )
    return {
        "stage": "cdte_a1_matrix_self_energy_export",
        "basis": contract["basis"]["name"],
        "gauge": contract["basis"]["gauge"],
        "state_order": contract["basis"]["state_order"],
        "temperature_grid_k": contract["temperature_grid_k"],
        "k_points_inverse_angstrom": contract["k_points_inverse_angstrom"],
        "provenance": {
            "fan_complete": True,
            "debye_waller_complete": True,
            "fan_and_dw_separate": True,
            "source_digest": "sha256:synthetic-fixture",
        },
        "records": records,
        "mode_resolved_gamma_frequency_bins": [
            {
                "theta_k": 70.0,
                "conduction_amplitude_ev": 0.003,
                "valence_amplitude_ev": -0.001,
                "gap_amplitude_ev": 0.004,
            },
            {
                "theta_k": 240.0,
                "conduction_amplitude_ev": -0.010,
                "valence_amplitude_ev": 0.008,
                "gap_amplitude_ev": -0.018,
            },
        ],
    }


def _audit(authorized: bool) -> dict[str, object]:
    return {
        "status": "cdte_a0_first_point_scientific_audit_completed",
        "decision": {"a1_electron_phonon_authorized": authorized},
    }


def test_valid_a1_export_is_accepted_after_a0_pass() -> None:
    contract = _contract()
    result = validate(_payload(contract), _audit(True), contract)
    assert result["decision"]["accepted_for_validated_matrix_pipeline"]
    assert result["decision"]["schema_and_provenance_pass"]
    assert result["decision"]["matrix_physics_pass"]


def test_valid_export_is_still_blocked_when_a0_fails() -> None:
    contract = _contract()
    result = validate(_payload(contract), _audit(False), contract)
    assert not result["decision"]["accepted_for_validated_matrix_pipeline"]
    assert not result["decision"]["a0_prerequisite_pass"]
    assert result["decision"]["schema_and_provenance_pass"]
    assert result["decision"]["matrix_physics_pass"]


def test_positive_damping_is_rejected() -> None:
    contract = _contract()
    payload = _payload(contract)
    payload["records"][0]["fan_imag_ev"][0][0] = 0.001
    result = validate(payload, _audit(True), contract)
    assert not result["decision"]["accepted_for_validated_matrix_pipeline"]
    assert not result["checks"]["numerical"]["causal_damping"]
