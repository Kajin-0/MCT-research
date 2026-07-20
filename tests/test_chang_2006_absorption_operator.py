from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.absorption_edge_uncertainty import analyze_absorption_edge_contract
from mct_research.chang_2006_absorption import (
    CHANG_2006_NORMALIZATION,
    CHANG_2006_SOURCE_DOI,
    build_chang_2006_candidate,
    chang_2006_absorption_shape,
    chang_2006_intrinsic_shape,
    fit_chang_2006_nonparabolic_urbach_edge,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data/templates/absorption_edge_uncertainty_input.schema.json"


def synthetic_spectrum() -> tuple[np.ndarray, np.ndarray]:
    energy = np.linspace(0.085, 0.25, 1000)
    absorption = 50000.0 * chang_2006_absorption_shape(
        energy,
        edge_ev=0.1,
        urbach_width_ev=0.012,
        hyperbola_b_ev=0.1,
    )
    return energy, absorption


def enabled_configuration() -> dict[str, object]:
    return {
        "enabled": True,
        "fit_absorption_window_cm1": [400.0, 15000.0],
        "edge_search_bounds_ev": [0.095, 0.105],
        "urbach_width_ev": 0.012,
        "urbach_width_provenance": "synthetic declared width",
        "hyperbola_b_ev": 0.1,
        "hyperbola_b_provenance": "synthetic declared hyperbola fit",
        "grid_points": 2001,
    }


def synthetic_contract() -> dict[str, object]:
    energy, absorption = synthetic_spectrum()
    return {
        "schema_version": "1.0",
        "specimen_id": "synthetic-chang-2006",
        "measurement_id": "synthetic-chang-2006-spectrum",
        "source": {
            "kind": "synthetic_validation",
            "reference": "tests/test_chang_2006_absorption_operator.py",
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
            "tail_model": "Chang 2006 synthetic generator",
        },
        "analysis_assumptions": {
            "fit_absorption_window_cm1": [2000.0, 10000.0],
            "edge_search_bounds_ev": [0.08, 0.09],
            "thresholds_cm1": [1000.0, 2000.0],
            "fractional_power_exponents": ["free"],
            "chang_2006_nonparabolic_urbach": enabled_configuration(),
        },
        "spectrum": {
            "energy_ev": energy.tolist(),
            "absorption_cm1": absorption.tolist(),
        },
    }


def test_schema_declares_optional_chang_2006_configuration() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    option = schema["properties"]["analysis_assumptions"]["properties"][
        "chang_2006_nonparabolic_urbach"
    ]
    assert option["type"] == "object"
    assert option["required"] == ["enabled"]
    assert set(option["properties"]) == {
        "enabled",
        "fit_absorption_window_cm1",
        "edge_search_bounds_ev",
        "urbach_width_ev",
        "urbach_width_provenance",
        "hyperbola_b_ev",
        "hyperbola_b_provenance",
        "grid_points",
    }


def test_continuity_normalization_matches_intrinsic_join() -> None:
    edge = 0.1
    width = 0.012
    b_value = 0.1
    join = edge + width / 2.0
    intrinsic = chang_2006_intrinsic_shape(
        np.asarray([join]),
        edge_ev=edge,
        hyperbola_b_ev=b_value,
    )[0]
    values = chang_2006_absorption_shape(
        np.asarray([join - 1.0e-12, join]),
        edge_ev=edge,
        urbach_width_ev=width,
        hyperbola_b_ev=b_value,
    )
    assert values[1] == pytest.approx(intrinsic, rel=0.0, abs=1.0e-14)
    assert values[0] == pytest.approx(intrinsic, rel=2.0e-10)
    assert "ambiguous absolute exponential prefactor" in CHANG_2006_NORMALIZATION


def test_synthetic_fit_recovers_edge_and_amplitude() -> None:
    energy, absorption = synthetic_spectrum()
    fit = fit_chang_2006_nonparabolic_urbach_edge(
        energy,
        absorption,
        edge_bounds_ev=(0.095, 0.105),
        fit_absorption_window_cm1=(400.0, 15000.0),
        urbach_width_ev=0.012,
        hyperbola_b_ev=0.1,
        grid_points=2001,
    )
    assert fit["edge_ev"] == pytest.approx(0.1, abs=1.0e-12)
    assert fit["amplitude_cm1"] == pytest.approx(50000.0, rel=1.0e-11)
    assert fit["join_energy_ev"] == pytest.approx(0.106)
    assert fit["tail_point_count"] >= 5
    assert fit["intrinsic_point_count"] >= 10
    assert fit["log_mean_square_error"] < 1.0e-20


def test_opt_in_adds_one_provenance_bound_candidate() -> None:
    payload = synthetic_contract()
    result = analyze_absorption_edge_contract(payload)
    candidate = next(
        item
        for item in result["model_candidates"]
        if item["candidate_id"] == "chang_2006_nonparabolic_urbach"
    )
    assert len(result["model_candidates"]) == 2
    assert result["combined_envelope"]["candidate_count"] == 4
    assert candidate["source_doi"] == CHANG_2006_SOURCE_DOI
    assert candidate["edge_ev"] == pytest.approx(0.1, abs=1.0e-12)
    assert candidate["source_validity_range"] == {
        "composition_x": [0.21, 0.23],
        "temperature_k": [77.0, 80.0],
        "energy_minus_edge_ev": [-0.02, 0.3],
    }
    assert result["analysis_assumptions"][
        "chang_2006_nonparabolic_urbach"
    ] == enabled_configuration()
    assert result["decision"]["single_corrected_gap_selected"] is False
    assert "corrected_gap" not in result
    assert "recommended_edge" not in result


def test_parameter_provenance_fails_closed() -> None:
    energy, absorption = synthetic_spectrum()
    configuration = enabled_configuration()
    configuration["urbach_width_provenance"] = ""
    with pytest.raises(ValueError, match="urbach_width_provenance"):
        build_chang_2006_candidate(
            configuration,
            metadata={"composition_x": 0.21, "temperature_k": 80.0},
            energy_ev=energy,
            absorption_cm1=absorption,
        )


@pytest.mark.parametrize(
    ("metadata", "message"),
    [
        ({"composition_x": 0.30, "temperature_k": 80.0}, "composition_x in"),
        ({"composition_x": 0.21, "temperature_k": 100.0}, "temperature_k in"),
    ],
)
def test_source_composition_and_temperature_domains_fail_closed(
    metadata: dict[str, float],
    message: str,
) -> None:
    energy, absorption = synthetic_spectrum()
    with pytest.raises(ValueError, match=message):
        build_chang_2006_candidate(
            enabled_configuration(),
            metadata=metadata,
            energy_ev=energy,
            absorption_cm1=absorption,
        )


def test_relative_energy_domain_fails_closed() -> None:
    energy = np.linspace(0.085, 0.45, 1000)
    absorption = 50000.0 * chang_2006_absorption_shape(
        energy,
        edge_ev=0.1,
        urbach_width_ev=0.012,
        hyperbola_b_ev=0.1,
    )
    configuration = enabled_configuration()
    configuration["fit_absorption_window_cm1"] = [400.0, 30000.0]
    with pytest.raises(ValueError, match="relative-energy domain"):
        build_chang_2006_candidate(
            configuration,
            metadata={"composition_x": 0.21, "temperature_k": 80.0},
            energy_ev=energy,
            absorption_cm1=absorption,
        )


def test_both_tail_and_intrinsic_branches_are_required() -> None:
    energy, absorption = synthetic_spectrum()
    configuration = enabled_configuration()
    configuration["fit_absorption_window_cm1"] = [5000.0, 15000.0]
    with pytest.raises(ValueError, match="branch coverage"):
        build_chang_2006_candidate(
            configuration,
            metadata={"composition_x": 0.21, "temperature_k": 80.0},
            energy_ev=energy,
            absorption_cm1=absorption,
        )


def test_disabled_configuration_is_explicit_and_adds_no_candidate() -> None:
    payload = synthetic_contract()
    payload["analysis_assumptions"]["chang_2006_nonparabolic_urbach"] = {
        "enabled": False
    }
    result = analyze_absorption_edge_contract(payload)
    assert all(
        item["candidate_id"] != "chang_2006_nonparabolic_urbach"
        for item in result["model_candidates"]
    )
    assert result["combined_envelope"]["candidate_count"] == 3
