from __future__ import annotations

import json

import pytest

from mct_research.absorption_observation import (
    AbsorptionEdgeObservation,
    AnalysisWindow,
    CarrierState,
    CompositionMetadata,
    EdgeModel,
    SensitivityEstimate,
    TailTreatment,
    TemperatureMetadata,
    build_edge_uncertainty_envelope,
    load_absorption_edge_export,
    save_absorption_edge_export,
)
from tools.build_absorption_edge_uncertainty_contract import analyze, build_records


def _minimal_observation(**overrides) -> AbsorptionEdgeObservation:
    values = {
        "record_id": "unit_record",
        "composition": CompositionMetadata(
            value_x=0.21,
            standard_uncertainty_x=0.001,
            method="independent calibrated composition measurement",
            status="measured",
        ),
        "temperature": TemperatureMetadata(value_k=80.0, standard_uncertainty_k=0.2),
        "reported_edge_ev": 0.100,
        "reported_standard_uncertainty_ev": 0.001,
        "observable_definition": "absorption_edge_energy",
        "measurement_modality": "FTIR transmission-derived absorption",
        "extraction_method": "fixed_absorption_threshold",
        "edge_model": EdgeModel(
            name="threshold crossing",
            expression="alpha(E)=alpha_threshold",
            parameters={},
        ),
        "analysis_window": AnalysisWindow(
            energy_ev=(0.08, 0.16), absorption_cm1=(600.0, 5000.0)
        ),
        "fixed_threshold_cm1": 1500.0,
        "carrier_state": CarrierState(
            status="measured",
            carrier_type="n",
            density_cm3=2.0e14,
            standard_uncertainty_cm3=2.0e13,
            method="Hall effect",
        ),
        "tail_treatment": TailTreatment(
            status="modeled", model="Urbach", parameters={"energy_mev": 6.0}
        ),
        "sensitivity_estimates": (
            SensitivityEstimate(
                label="threshold_1000",
                edge_ev=0.095,
                varied_factors=("fixed_threshold",),
                settings={"threshold_cm1": 1000.0},
            ),
            SensitivityEstimate(
                label="alternate_model",
                edge_ev=0.108,
                varied_factors=("model_family",),
                settings={"model": "fractional power"},
            ),
        ),
        "source_doi": "10.0000/unit",
        "source_locator": "Table 1",
        "evidence_class": "experimental_primary",
        "notes": None,
    }
    values.update(overrides)
    return AbsorptionEdgeObservation(**values)


def test_contract_builder_matches_reference_metrics() -> None:
    result = analyze()
    assert result["record_count"] == 4
    assert result["sensitivity_estimates_per_record"] == [7]
    assert result["all_records_cover_threshold_and_model_family"] is True
    assert result["minimum_envelope_span_mev"] == pytest.approx(
        30.501075699817235, abs=1.0e-10
    )
    assert result["maximum_envelope_span_mev"] == pytest.approx(
        46.14826694691032, abs=1.0e-10
    )
    assert result["production_correction_authorized"] is False


def test_envelope_keeps_measurement_sigma_separate() -> None:
    envelope = build_edge_uncertainty_envelope(_minimal_observation())
    assert envelope.minimum_edge_ev == pytest.approx(0.095)
    assert envelope.maximum_edge_ev == pytest.approx(0.108)
    assert envelope.lower_deviation_mev == pytest.approx(5.0)
    assert envelope.upper_deviation_mev == pytest.approx(8.0)
    assert envelope.span_mev == pytest.approx(13.0)
    assert envelope.reported_standard_uncertainty_ev == pytest.approx(0.001)
    assert set(envelope.varied_factors) == {"fixed_threshold", "model_family"}
    assert "not combined in quadrature" in envelope.interpretation


def test_fixed_threshold_requires_threshold_value() -> None:
    with pytest.raises(ValueError, match="requires fixed_threshold_cm1"):
        _minimal_observation(fixed_threshold_cm1=None)


def test_threshold_must_lie_inside_declared_absorption_window() -> None:
    with pytest.raises(ValueError, match="must lie inside absorption_cm1 window"):
        _minimal_observation(fixed_threshold_cm1=5500.0)


def test_contract_requires_same_record_sensitivity() -> None:
    with pytest.raises(ValueError, match="at least one same-record sensitivity"):
        _minimal_observation(sensitivity_estimates=())


def test_measured_carrier_state_requires_density_and_method() -> None:
    with pytest.raises(ValueError, match="requires type, density, and method"):
        CarrierState(status="measured", carrier_type="n")


def test_absorption_edge_energy_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        _minimal_observation(reported_edge_ev=-0.001)


def test_json_roundtrip_recomputes_envelope(tmp_path) -> None:
    records = build_records()
    path = tmp_path / "contract.json"
    provenance = {"generator": "unit-test", "evidence_class": "synthetic"}
    save_absorption_edge_export(path, records, provenance=provenance)
    loaded, loaded_provenance = load_absorption_edge_export(path)
    assert loaded == records
    assert loaded_provenance == provenance

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][0]["model_sensitivity_envelope"]["span_mev"] += 1.0
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match normalized contract recomputation"):
        load_absorption_edge_export(path)
