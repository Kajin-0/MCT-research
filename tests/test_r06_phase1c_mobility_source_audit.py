"""Fail-closed checks for the R06 low-temperature mobility audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/validation/r06_low_temperature_mobility_audit.json"
NOTE_PATH = ROOT / "literature/stochastic_transport_noise/source_notes/low_temperature_mobility_phase1c.md"
LEDGER_PATH = ROOT / "literature/stochastic_transport_noise/hgcdte_parameter_source_ledger.csv"


def _audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def _ledger() -> dict[str, dict[str, str]]:
    with LEDGER_PATH.open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def test_gate_remains_fail_closed() -> None:
    audit = _audit()
    assert audit["decision"] == (
        "SPECIMEN_CONDITIONED_ELECTRON_ANCHORS_ACCEPTED_"
        "UNIVERSAL_MOBILITY_CLOSURE_BLOCKED"
    )
    assert audit["universal_electron_mobility_relation_authorized"] is False
    assert audit["universal_hole_mobility_relation_authorized"] is False
    assert audit["predictive_material_mobility_closure_authorized"] is False


def test_wiley_table_has_seven_77k_specimens() -> None:
    direct = _audit()["direct_electron_measurements"]
    assert direct["temperature_K"] == 77.0
    samples = direct["samples"]
    assert len(samples) == 7
    assert [sample["x"] for sample in samples] == [
        0.135, 0.144, 0.149, 0.150, 0.188, 0.193, 0.203
    ]


def test_wiley_values_and_units_are_preserved() -> None:
    samples = _audit()["direct_electron_measurements"]["samples"]
    assert min(sample["mu_V_m2_Vs"] for sample in samples) == 18.0
    assert max(sample["mu_K_m2_Vs"] for sample in samples) == 64.0
    assert min(sample["density_m3"] for sample in samples) == 9.0e20
    assert max(sample["density_m3"] for sample in samples) == 2.3e22
    assert all(sample["mu_K_uncertainty"] > 0 for sample in samples)
    assert all(sample["mu_V_uncertainty"] > 0 for sample in samples)


def test_no_composition_only_interpolation_is_authorized() -> None:
    direct = _audit()["direct_electron_measurements"]
    assert "universal composition-only" in direct["prohibited_use"]


def test_model_benchmark_pair_is_consistent() -> None:
    benchmark = _audit()["model_conditioned_benchmark"]
    ratio = benchmark["electron_mobility_cm2_Vs"] / benchmark["hole_mobility_cm2_Vs"]
    assert ratio == benchmark["mobility_ratio"] == 400.0
    assert benchmark["status"].startswith("cross-checked model input")


def test_yoo_kwack_metadata_is_corrected() -> None:
    source = _audit()["theoretical_source_correction"]
    assert source["source_id"] == "YOO_KWACK1997"
    assert source["year"] == 1997
    assert source["doi"] == "10.1063/1.364212"
    assert source["not_a_measurement_relation"] is True
    assert source["authors"] == ["Sang-Dong Yoo", "Kae Dal Kwack"]


def test_p_type_source_is_methodological_not_numeric_closure() -> None:
    source = _audit()["p_type_variable_field_source"]
    assert source["numeric_table_transcribed"] is False
    assert "uncertainty evidence" in source["accepted_use"]
    assert "hole-mobility constant" in source["prohibited_use"]


def test_required_work_includes_primary_hole_measurements() -> None:
    requirements = _audit()["required_before_material_closure"]
    assert any("hole-mobility" in item for item in requirements)
    assert any("compensation" in item for item in requirements)
    assert any("Hall data" in item for item in requirements)


def test_note_preserves_provenance_tiers() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    assert "Tier A" in note
    assert "Tier B" in note
    assert "Tier C" in note
    assert "not promoted to a material constant" in note


def test_ledger_contains_corrected_and_new_sources() -> None:
    rows = _ledger()
    assert rows["YOO_KWACK1997"]["year"] == "1997"
    assert "theoretical" in rows["YOO_KWACK1997"]["source_role"]
    assert rows["WILEY_DEXTER1969"]["verification_status"] == "primary_table_transcribed"
    assert rows["SMITH1984_MOBILITY_BENCHMARK"]["source_role"] == "model-conditioned detector benchmark"
    assert rows["HOLE_MOBILITY_UNRESOLVED"]["verification_status"] == "partially_constrained_no_universal_relation"
