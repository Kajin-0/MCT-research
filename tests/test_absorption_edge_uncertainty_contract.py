from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.absorption_edge_uncertainty import (
    CHU_1994_SOURCE_DOI,
    analyze_absorption_edge_contract,
    chu_1994_beta_ev_inverse,
    fit_chu_1994_kane_edge,
)

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
    chu_option = schema["properties"]["analysis_assumptions"]["properties"][
        "include_chu_1994_kane_region"
    ]
    assert chu_option == {
        "type": "boolean",
        "default": False,
        "description": (
            "Opt in to the provenance-bound Chu 1994 Kane-region candidate within "
            "0.170<=x<=0.443 and 77<=T<=300 K."
        ),
    }


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
    assert "recommended_edge" not in result
    assert "corrected_gap" not in result


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
    assert result["threshold_envelope"]["full_span_mev"] > 9.0


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


def test_chu_1994_beta_reproduces_reported_temperature_limits() -> None:
    assert chu_1994_beta_ev_inverse(0.21, 80.0) == pytest.approx(7.866)
    assert chu_1994_beta_ev_inverse(0.21, 300.0) == pytest.approx(20.12)
    assert chu_1994_beta_ev_inverse(0.30, 77.0) == pytest.approx(
        5.391 + 10.99 * 0.30,
        abs=1.0e-12,
    )


def test_chu_1994_candidate_recovers_its_generating_edge() -> None:
    edge = 0.1
    composition = 0.21
    temperature = 80.0
    alpha_g = 700.0
    beta = chu_1994_beta_ev_inverse(composition, temperature)
    energy = np.linspace(0.101, 0.25, 1001)
    absorption = alpha_g * np.exp(np.sqrt(beta * (energy - edge)))
    fit = fit_chu_1994_kane_edge(
        energy,
        absorption,
        edge_bounds_ev=(0.09, 0.1005),
        composition_x=composition,
        temperature_k=temperature,
    )
    assert fit["edge_ev"] == pytest.approx(edge, abs=2.0e-5)
    assert fit["alpha_g_cm1"] == pytest.approx(alpha_g, rel=2.0e-4)
    assert fit["beta_ev_inverse"] == pytest.approx(beta)
    assert fit["log_mean_square_error"] < 1.0e-10


def test_opt_in_adds_one_provenance_bound_candidate() -> None:
    payload = synthetic_contract()
    payload["analysis_assumptions"]["include_chu_1994_kane_region"] = True
    result = analyze_absorption_edge_contract(payload)
    assert len(result["model_candidates"]) == 4
    assert result["combined_envelope"]["candidate_count"] == 8
    candidate = next(
        item
        for item in result["model_candidates"]
        if item["candidate_id"] == "chu_1994_kane_region"
    )
    assert candidate["source_doi"] == CHU_1994_SOURCE_DOI
    assert candidate["method"] == "chu_1994_kane_region_fit"
    assert candidate["beta_expression"] == "-1+0.083*T+(21-0.13*T)*x"
    assert candidate["source_validity_range"] == {
        "composition_x": [0.17, 0.443],
        "temperature_k": [77.0, 300.0],
    }
    assert result["decision"]["single_corrected_gap_selected"] is False


def test_chu_1994_candidate_fails_closed_outside_source_domain() -> None:
    low_temperature = synthetic_contract()
    low_temperature["metadata"]["temperature_k"] = 40.0
    low_temperature["analysis_assumptions"]["include_chu_1994_kane_region"] = True
    with pytest.raises(ValueError, match="temperature_k in"):
        analyze_absorption_edge_contract(low_temperature)

    high_composition = synthetic_contract()
    high_composition["metadata"]["composition_x"] = 0.60
    high_composition["analysis_assumptions"]["include_chu_1994_kane_region"] = True
    with pytest.raises(ValueError, match="composition_x in"):
        analyze_absorption_edge_contract(high_composition)

    unknown_composition = synthetic_contract()
    unknown_composition["metadata"]["composition_x"] = None
    unknown_composition["analysis_assumptions"]["include_chu_1994_kane_region"] = True
    with pytest.raises(ValueError, match="requires a measured or declared composition_x"):
        analyze_absorption_edge_contract(unknown_composition)
