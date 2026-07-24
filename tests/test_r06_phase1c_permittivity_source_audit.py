"""Fail-closed checks for the R06 static-permittivity source audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/validation/r06_static_permittivity_audit.json"
NOTE_PATH = ROOT / "literature/stochastic_transport_noise/source_notes/static_permittivity_phase1c.md"
LEDGER_PATH = ROOT / "literature/stochastic_transport_noise/hgcdte_parameter_source_ledger.csv"


def _audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def _ledger() -> dict[str, dict[str, str]]:
    with LEDGER_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def _epsilon(x: float, linear_coefficient: float) -> float:
    return 20.5 - linear_coefficient * x + 5.7 * x * x


def test_gate_authorizes_benchmark_not_material_closure() -> None:
    audit = _audit()
    assert audit["decision"] == (
        "STATIC_PERMITTIVITY_BENCHMARK_BRACKET_ACCEPTED_"
        "PRIMARY_ALLOY_FIT_LINEAGE_UNRESOLVED"
    )
    assert audit["benchmark_static_permittivity_bracket_authorized"] is True
    assert audit["source_exact_static_permittivity_relation_authorized"] is False
    assert audit["predictive_material_permittivity_closure_authorized"] is False


def test_electrostatic_and_optical_quantities_are_separated() -> None:
    definitions = _audit()["definitions"]
    assert "Poisson" in definitions["epsilon_s"]
    assert "not interchangeable" in definitions["epsilon_infinity"]
    assert "excluded" in definitions["oxide_permittivity"]


def test_primary_source_domain_is_retained() -> None:
    sources = {source["source_id"]: source for source in _audit()["source_lineage"]}
    source = sources["BAARS_SORGER1972"]
    assert source["doi"] == "10.1016/0038-1098(72)90211-6"
    assert source["composition_range"] == [0.0, 0.54]
    assert source["temperatures_K"] == [77.0, 300.0]
    assert source["direct_alloy_polynomial_reported"] is False


def test_data_review_lineage_is_not_promoted_to_primary_measurement() -> None:
    sources = {source["source_id"]: source for source in _audit()["source_lineage"]}
    review = sources["TONG_RAVINDRA1993"]
    compilation = sources["BRICE_CAPPER1987"]
    assert "secondary review" in review["source_role"]
    assert "compiled-data lineage" in compilation["source_role"]
    assert compilation["equation_quality_copy_recovered"] is False


def test_static_bracket_has_expected_width() -> None:
    for x in (0.17, 0.20, 0.21, 0.30, 0.54):
        lower = _epsilon(x, 15.6)
        upper = _epsilon(x, 15.5)
        nominal = _epsilon(x, 15.55)
        assert upper - lower == pytest.approx(0.1 * x)
        assert nominal == pytest.approx(0.5 * (lower + upper))


def test_reference_values_match_polynomials() -> None:
    values = _audit()["static_candidate_family"]["reference_values"]
    for record in values:
        x = record["x"]
        assert record["lower"] == pytest.approx(_epsilon(x, 15.6))
        assert record["nominal"] == pytest.approx(_epsilon(x, 15.55))
        assert record["upper"] == pytest.approx(_epsilon(x, 15.5))


def test_bracket_is_not_mislabeled_physical_uncertainty() -> None:
    family = _audit()["static_candidate_family"]
    assert "not a physical uncertainty" in family["coefficient_difference_interpretation"]


def test_high_frequency_typo_is_rejected() -> None:
    warning = _audit()["high_frequency_lineage_warning"]
    assert "15.6*x" in warning["commonly_reported_relation"]
    assert "5.6*x" in warning["known_secondary_typographical_variant"]
    assert "do not use" in warning["decision"]


def test_temperature_law_remains_unauthorized() -> None:
    temperature = _audit()["temperature_decision"]
    assert temperature["temperature_independence_authorized"] is False
    assert "77 K and 300 K" in temperature["benchmark_treatment"]


def test_note_and_ledger_preserve_fail_closed_boundary() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    rows = _ledger()
    assert "not a physical confidence interval" in note
    assert "not interchangeable" in note
    assert rows["BAARS_SORGER1972"]["verification_status"] == "primary_reststrahlen_domain_verified"
    assert rows["BRICE_CAPPER1987_PERMITTIVITY"]["verification_status"] == "datareview_lineage_verified_source_pages_pending"
    assert rows["PERMITTIVITY_BENCHMARK_BRACKET"]["source_role"] == "architecture-level static-permittivity bracket"
