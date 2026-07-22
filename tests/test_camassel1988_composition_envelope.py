from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from tools.analyze_camassel1988_composition_envelope import (
    analyze,
    quantize_for_serialization,
)


ROOT = Path(__file__).resolve().parents[1]
SPECIMENS = ROOT / "data" / "experimental" / "camassel1988_specimens.csv"
OBSERVATIONS = (
    ROOT / "data" / "experimental" / "camassel1988_table1_observations.csv"
)
REFERENCE = ROOT / "validation" / "camassel1988_composition_envelope_reference.json"
RECORDS = ROOT / "validation" / "camassel1988_composition_envelope_records.csv"


def _result() -> dict[str, object]:
    return analyze(SPECIMENS, OBSERVATIONS)


def _compact(result: dict[str, object]) -> dict[str, object]:
    return {
        key: value for key, value in result.items() if key != "records"
    } | {"record_count": len(result["records"])}


def test_forward_evaluation_has_no_fitted_parameters() -> None:
    result = _result()
    records = result["records"]
    assert len(records) == 39
    assert len({record["observation_id"] for record in records}) == 13
    assert len({record["specimen_id"] for record in records}) == 11
    assert result["fitted_parameter_count"] == 0
    assert {record["fitted_parameters"] for record in records} == {0}


def test_composition_envelopes_are_exact_and_clipped() -> None:
    records = _result()["records"]
    endpoint = next(
        record
        for record in records
        if record["observation_id"] == "camassel1988_mct48_reflectivity"
        and record["model"] == "hansen_1982"
    )
    low = next(
        record
        for record in records
        if record["observation_id"] == "camassel1988_mct68_absorption"
        and record["model"] == "hansen_1982"
    )
    assert endpoint["composition_interval_lower"] == pytest.approx(0.995)
    assert endpoint["composition_interval_upper"] == pytest.approx(1.0)
    assert low["composition_interval_lower"] == pytest.approx(0.495)
    assert low["composition_interval_upper"] == pytest.approx(0.505)
    assert {
        record["composition_interval_interpretation"] for record in records
    } == {
        "deterministic_source_accuracy_envelope_not_probability_distribution"
    }


def test_same_specimen_modality_differences_are_preserved() -> None:
    differences = {
        row["specimen_id"]: row
        for row in _result()["same_specimen_modality_differences"]
    }
    assert set(differences) == {"camassel1988_mct49", "camassel1988_mct47"}
    assert differences["camassel1988_mct49"][
        "reflectivity_minus_absorption_mev"
    ] == pytest.approx(2.0)
    assert differences["camassel1988_mct47"][
        "reflectivity_minus_absorption_mev"
    ] == pytest.approx(-17.5)
    assert {row["independent_specimen_count"] for row in differences.values()} == {1}


def test_hansen_within_domain_discrepancy_survives_full_envelope() -> None:
    focus = _result()["hansen_within_domain_focus"]
    x50 = focus["x_0p50"]["hansen_1982"]
    x55 = focus["x_0p55"]["hansen_1982"]
    assert x50["model_domain_status"] == "within_declared_composition_evidence"
    assert x55["model_domain_status"] == "within_declared_composition_evidence"
    assert x50["minimum_absolute_residual_mev"] == pytest.approx(54.779646)
    assert x55["minimum_absolute_residual_mev"] == pytest.approx(39.234326)
    assert x50["zero_residual_reachable"] is False
    assert x55["zero_residual_reachable"] is False


def test_provisional_thermal_term_does_not_repair_static_discrepancy() -> None:
    result = _result()
    focus = result["hansen_within_domain_focus"]
    assert focus["x_0p50"]["provisional_hansen_pade"][
        "minimum_absolute_residual_mev"
    ] == pytest.approx(54.769089413)
    assert focus["x_0p55"]["provisional_hansen_pade"][
        "minimum_absolute_residual_mev"
    ] == pytest.approx(39.118203546)
    assert result["scientific_decision"][
        "provisional_thermal_term_repairs_static_discrepancy"
    ] is False


def test_laurenti_is_encoded_as_source_lineage_dependent() -> None:
    result = _result()
    assert result["model_lineage"]["laurenti_1990"] == (
        "camassel_lineage_dependent_not_heldout"
    )
    assert result["scientific_decision"]["laurenti_independently_validated"] is False
    assert {
        record["model_domain_status"]
        for record in result["records"]
        if record["model"] == "laurenti_1990"
    } == {"source_lineage_dependent_not_heldout"}


def test_immutable_reference_and_observation_csv_regenerate() -> None:
    result = _result()
    expected = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert quantize_for_serialization(_compact(result)) == expected

    with RECORDS.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 39
    assert {row["model"] for row in rows} == {
        "hansen_1982",
        "laurenti_1990",
        "provisional_hansen_pade",
    }
    assert {row["fitted_parameters"] for row in rows} == {"0"}


def test_result_contains_no_probabilistic_ranking_claim() -> None:
    result = quantize_for_serialization(_compact(_result()))
    serialized = json.dumps(result, sort_keys=True).lower()
    prohibited = (
        '"p_value"',
        '"chi_square"',
        '"likelihood"',
        '"statistical_significance"',
        '"laurenti_independently_validated": true',
        '"production_equation_authorized": true',
        '"manuscript_authorized": true',
    )
    assert all(token not in serialized for token in prohibited)
