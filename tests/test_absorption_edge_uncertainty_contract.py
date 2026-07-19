from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.absorption_edge_uncertainty import analyze_absorption_edge_contract

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data/templates/absorption_edge_uncertainty_input.schema.json"


def synthetic_contract() -> dict[str, object]:
    latent_edge = 0.1
    energy = np.linspace(0.1001, 0.25, 1001)
    absorption = 5000.0 * (energy - latent_edge) ** 0.7 / energy
    return {
        "schema_version": "1.0",
        "specimen_id": "synthetic-specimen-001",
        "measurement_id": "synthetic-ftir-001",
        "source": {
            "kind": "synthetic_validation",
            "reference": "tests/test_absorption_edge_uncertainty_contract.py",
            "calibration_record": "native-digital-synthetic-grid",
        },
        "metadata": {
            "modality": "FTIR_absorption_coefficient",
            "temperature_k": 80.0,
            "thickness_um": 8.0,
            "composition_x": 0.21,
            "composition_sigma_x": 0.001,
            "composition_method": "synthetic_declared",
            "carrier_type": "n",
            "carrier_density_cm3": 2.0e15,
            "carrier_density_status": "synthetic_known",
            "tail_model": "none_in_generating_fractional_power_curve",
        },
        "analysis_assumptions": {
            "fit_absorption_window_cm1": [600.0, 5000.0],
            "edge_search_bounds_ev": [0.09, 0.101],
            "thresholds_cm1": [600.0, 1000.0, 1500.0, 2000.0],
            "fractional_power_exponents": ["free", 0.5, 1.0],
        },
        "spectrum": {
            "energy_ev": energy.tolist(),
            "absorption_cm1": absorption.tolist(),
        },
    }


def test_schema_file_is_valid_json_and_declares_required_metadata() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["properties"]["schema_version"]["const"] == "1.0"
    required = set(schema["properties"]["metadata"]["required"])
    assert {"carrier_type", "carrier_density_cm3", "tail_model"}.issubset(required)


def test_contract_exports_all_candidates_and_no_corrected_gap() -> None:
    result = analyze_absorption_edge_contract(synthetic_contract())
    assert len(result["model_candidates"]) == 3
    assert len(result["threshold_candidates"]) == 4
    assert result["combined_envelope"]["candidate_count"] == 7
    free = next(
        candidate
        for candidate in result["model_candidates"]
        if candidate["candidate_id"] == "fractional_power_free"
    )
    assert free["edge_ev"] == pytest.approx(0.1, abs=2e-5)
    assert free["exponent"] == pytest.approx(0.7, abs=0.003)
    assert result["combined_envelope"]["full_span_mev"] > 10.0
    assert result["decision"]["single_corrected_gap_selected"] is False
    rendered = json.dumps(result, sort_keys=True)
    assert "recommended_edge" not in rendered
    assert "corrected_gap" not in rendered


def test_output_is_deterministic_and_provenance_bound() -> None:
    payload = synthetic_contract()
    first = analyze_absorption_edge_contract(payload)
    second = analyze_absorption_edge_contract(payload)
    assert first == second
    assert len(first["input_sha256"]) == 64
    assert first["source"]["calibration_record"] == "native-digital-synthetic-grid"
    assert first["analysis_assumptions"]["fit_point_count"] >= 20


def test_threshold_candidates_preserve_definition_and_bias_direction() -> None:
    result = analyze_absorption_edge_contract(synthetic_contract())
    thresholds = result["threshold_candidates"]
    assert [candidate["threshold_cm1"] for candidate in thresholds] == [
        600.0,
        1000.0,
        1500.0,
        2000.0,
    ]
    edges = [candidate["edge_ev"] for candidate in thresholds]
    assert edges == sorted(edges)
    assert all(edge > 0.1 for edge in edges)
    assert result["threshold_envelope"]["full_span_mev"] > 20.0


def test_missing_or_implicit_metadata_fails_closed() -> None:
    missing = synthetic_contract()
    del missing["metadata"]["carrier_density_status"]
    with pytest.raises(ValueError, match="carrier_density_status"):
        analyze_absorption_edge_contract(missing)

    uncalibrated = synthetic_contract()
    uncalibrated["source"]["calibration_record"] = ""
    with pytest.raises(ValueError, match="calibration_record"):
        analyze_absorption_edge_contract(uncalibrated)

    unordered = synthetic_contract()
    unordered["spectrum"]["energy_ev"][5] = unordered["spectrum"]["energy_ev"][4]
    with pytest.raises(ValueError, match="strictly increasing"):
        analyze_absorption_edge_contract(unordered)


def test_unknown_carrier_state_is_allowed_only_when_explicit() -> None:
    payload = synthetic_contract()
    payload["metadata"]["carrier_type"] = "unknown"
    payload["metadata"]["carrier_density_cm3"] = None
    payload["metadata"]["carrier_density_status"] = "not_measured"
    result = analyze_absorption_edge_contract(payload)
    assert result["metadata"]["carrier_type"] == "unknown"
    assert result["metadata"]["carrier_density_status"] == "not_measured"


def test_uncrossed_threshold_is_reported_not_silently_dropped() -> None:
    payload = synthetic_contract()
    payload["analysis_assumptions"]["thresholds_cm1"].append(100000.0)
    result = analyze_absorption_edge_contract(payload)
    assert result["excluded_candidates"] == [
        {
            "candidate_id": "threshold_100000_cm-1",
            "reason": "threshold is not crossed",
        }
    ]
    assert result["combined_envelope"]["candidate_count"] == 7
