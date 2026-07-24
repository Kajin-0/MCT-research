"""Fail-closed tests for the R06 Lowney-Madarasz source audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/validation/r06_lowney_madarasz_equation_audit.json"
NOTE_PATH = ROOT / "literature/stochastic_transport_noise/source_notes/lowney_madarasz_primary_audit.md"
LEDGER_PATH = ROOT / "literature/stochastic_transport_noise/hgcdte_parameter_source_ledger.csv"


def _audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def _ledger_rows() -> dict[str, dict[str, str]]:
    with LEDGER_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def test_gate_is_fail_closed() -> None:
    audit = _audit()
    assert audit["decision"] == (
        "ARCHITECTURE_RECOVERED_IMPLEMENTATION_BLOCKED_ON_SYMBOL_EXACT_TRANSCRIPTION"
    )
    assert audit["source_exact_statistics_implementation_authorized"] is False


def test_source_identities_are_fixed() -> None:
    sources = {source["source_id"]: source for source in _audit()["sources"]}
    assert sources["MADARASZ_SZMULOWICZ1985"]["doi"] == "10.1063/1.335868"
    assert sources["SEILER_LOWNEY_LITTLER_YOON1991"]["nist_publication_id"] == 22086
    assert sources["LOWNEY_SEILER_LITTLER_YOON1992"]["doi"] == "10.1063/1.351371"
    assert sources["LOWNEY_SEILER_LITTLER_YOON1992"]["authors"] == [
        "J. R. Lowney",
        "D. G. Seiler",
        "C. L. Littler",
        "I. T. Yoon",
    ]


def test_recovered_architecture_values() -> None:
    architecture = _audit()["recovered_model_architecture"]
    assert architecture["composition_range"] == [0.17, 0.30]
    assert architecture["temperature_range_K"] == [4.0, 300.0]
    assert architecture["conduction_band_model"] == "Kane three-band k.p"
    assert architecture["conduction_band_statistics"] == "full Fermi-Dirac"
    assert architecture["valence_band_statistics"] == "nondegenerate"
    assert architecture["split_off_energy_eV"] == 1.0
    assert architecture["momentum_matrix_element_eV_cm"] == 8.49e-8
    assert architecture["heavy_hole_mass_over_m0"] == 0.55


def test_gap_relation_is_immutable() -> None:
    relation = _audit()["verified_gap_relation"]
    assert relation["expression_ascii"] == (
        "Eg=-0.302+1.93*x-0.810*x^2+0.832*x^3+"
        "5.35e-4*(1-2*x)*((-1822+T^3)/(255.2+T^2))"
    )
    assert relation["units"] == {"Eg": "eV", "T": "K"}


def test_symbol_level_equations_remain_blocked() -> None:
    gate = _audit()["equation_transcription_gate"]
    assert gate["equation_1_gap_relation_symbol_level_verified"] is True
    assert gate["equation_2_charge_neutrality_symbol_level_verified"] is False
    assert gate["equation_3_integration_by_parts_symbol_level_verified"] is False
    assert gate["equation_4_intrinsic_density_symbol_level_verified"] is False
    assert gate["madarasz_equations_symbol_level_verified"] is False
    assert gate["lowney_1992_fit_coefficients_verified"] is False


def test_reference_requirements_cannot_be_empty() -> None:
    requirements = _audit()["equation_transcription_gate"]["required_before_implementation"]
    assert len(requirements) >= 4
    assert any("unit" in item.lower() for item in requirements)
    assert any("numerical reference" in item.lower() for item in requirements)


def test_note_states_no_silent_reconstruction() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    assert "not transcribed into executable code" in note
    assert "No missing symbol" in note
    assert "source-exact implementation" in note


def test_ledger_records_partial_recovery_without_authorization() -> None:
    rows = _ledger_rows()
    madarasz = rows["MADARASZ_SZMULOWICZ1985"]
    lowney = rows["LOWNEY_SEILER_LITTLER_YOON1992"]
    assert "symbol_level_transcription_pending" in madarasz["verification_status"]
    assert "open_primary_precursor_architecture_recovered" in lowney["verification_status"]
    assert "implementation remains blocked" in madarasz["phase1c_action"]
    assert "fit coefficients" in lowney["phase1c_action"]


def test_claim_boundary_keeps_model_comparison_unauthorized() -> None:
    unsupported = _audit()["claim_boundary"]["not_supported"]
    assert "numerical intrinsic-density comparison" in unsupported
    assert "material-accurate HgCdTe transport closure" in unsupported
