from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/stankiewicz1972_hsc_r10_source_metadata.csv"
SAMPLES = ROOT / "data/hansen/stankiewicz1972_sample_records.csv"
TABLE1 = ROOT / "data/hansen/stankiewicz1972_table1_parameters.csv"
ASSUMPTIONS = ROOT / "data/hansen/stankiewicz1972_model_assumptions.csv"
EQ4 = ROOT / "data/hansen/stankiewicz1972_equation4_relation.csv"
CANDIDATES = ROOT / "data/hansen/stankiewicz1972_hansen_ingestion_candidates.csv"
README = ROOT / "data/hansen/stankiewicz1972_hsc_r10_README.md"
REFERENCE = ROOT / "data/validation/stankiewicz1972_hsc_r10_audit.json"
TOOL = ROOT / "tools/audit_stankiewicz1972_hsc_r10.py"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_source_identity_and_hash() -> None:
    row = _csv(META)[0]
    assert row["source_id"] == "STANKIEWICZ1972_HSC_R10"
    assert row["hansen_graph_id"] == "HSC_R10"
    assert row["first_page"] == "387"
    assert row["last_page"] == "393"
    assert row["doi"] == "10.1002/pssb.2220490136"
    assert row["source_pdf_sha256"] == (
        "d48d5312fbd3de5e90a95eab695c7cf1e0b86a9e528f7c1035978abc4993245e"
    )
    assert row["source_binary_committed"] == "false"


def test_measurement_class_is_hall_transport_not_optical() -> None:
    row = _csv(META)[0]
    assert row["primary_measurement_class"] == (
        "hydrostatic_pressure_hall_transport_with_kane_model_inversion"
    )
    assert "signed zero-pressure gap" in row["primary_gap_observable"]
    text = README.read_text(encoding="utf-8")
    assert "not an optical experiment" in text
    assert "model-conditioned" in text


def test_four_specimens_and_composition_provenance() -> None:
    rows = _csv(SAMPLES)
    assert len(rows) == 4
    assert {row["composition_x"] for row in rows} == {"0.07", "0.095", "0.13", "0.18"}
    assert {row["composition_half_width_x"] for row in rows} == {"0.005"}
    assert {row["source_specimen_identifier"] for row in rows} == {"not_reported"}
    assert {row["composition_method"] for row in rows} == {"density_measurements"}


def test_table1_values_are_exactly_transcribed() -> None:
    rows = {row["composition_x"]: row for row in _csv(TABLE1)}
    assert len(rows) == 4
    assert rows["0.07"]["gap_77k_eV"] == "-0.122"
    assert rows["0.07"]["gap_280k_eV"] == "-0.035"
    assert rows["0.095"]["gap_280k_eV"] == "-0.008"
    assert rows["0.13"]["gap_280k_eV"] == "0.049"
    assert rows["0.18"]["gap_77k_eV"] == "0.042"
    assert rows["0.18"]["gap_280k_eV"] == "0.117"
    assert {row["gap_77k_half_width_eV"] for row in rows.values()} == {"0.006"}
    assert {row["gap_280k_half_width_eV"] for row in rows.values()} == {"0.006"}


def test_pressure_and_temperature_coefficients() -> None:
    rows = {row["composition_x"]: row for row in _csv(TABLE1)}
    assert rows["0.07"]["pressure_coefficient_eV_per_atm"] == "9.5e-6"
    assert rows["0.095"]["pressure_coefficient_eV_per_atm"] == "10.5e-6"
    assert rows["0.13"]["temperature_coefficient_eV_per_K"] == "4.0e-4"
    assert rows["0.18"]["temperature_coefficient_eV_per_K"] == "3.8e-4"
    assert {row["pressure_coefficient_half_width_eV_per_atm"] for row in rows.values()} == {"0.5e-6"}
    assert {row["temperature_coefficient_half_width_eV_per_K"] for row in rows.values()} == {"0.5e-4"}


def test_model_assumptions_and_source_warning() -> None:
    rows = {row["parameter_id"]: row for row in _csv(ASSUMPTIONS)}
    assert rows["SG72_EP"]["value"] == "18"
    assert rows["SG72_MH"]["value"] == "0.55"
    assert rows["SG72_DELTA_E"]["value"] == "0"
    text = README.read_text(encoding="utf-8")
    assert "not perfectly intrinsic" in text
    assert "error beyond the reported measurement errors" in text


def test_equation4_is_preserved_with_domain_and_caveat() -> None:
    row = _csv(EQ4)[0]
    assert row["domain_x_max"] == "0.2"
    assert row["intercept_eV"] == "-0.303"
    assert row["linear_x_coefficient_eV"] == "1.91"
    assert row["temperature_prefactor_eV_per_K"] == "5.25e-4"
    assert "x=0.18" in row["source_caveat"]


def test_hansen_candidates_are_not_assignments() -> None:
    rows = _csv(CANDIDATES)
    assert len(rows) == 9
    assert sum(row["candidate_basis"] == "Table_1_model_fit_output" for row in rows) == 8
    assert sum(row["candidate_basis"] == "Equation_4_scalar_relation" for row in rows) == 1
    assert all("not_hansen_assignment" in row["candidate_status"] for row in rows)


def test_canonical_audit_is_deterministic() -> None:
    generated = subprocess.check_output([sys.executable, str(TOOL)], text=True)
    assert generated == REFERENCE.read_text(encoding="utf-8")
    audit = json.loads(generated)
    assert audit["source_scope"]["physical_specimen_count"] == 4
    assert audit["source_scope"]["table1_gap_value_count"] == 8
    assert audit["decision"]["controlling_decision"] == (
        "primary_source_recovered_table1_and_equation4_reconstructed_"
        "hansen_marker_mapping_unresolved"
    )
    assert audit["decision"]["direct_hansen_validation_authorized"] is False


def test_no_dense_digitized_or_invented_covariance_products() -> None:
    forbidden = [
        ROOT / "data/hansen/stankiewicz1972_figure1_digitized.csv",
        ROOT / "data/hansen/stankiewicz1972_figures2_to_5_digitized.csv",
        ROOT / "data/hansen/stankiewicz1972_figure6_digitized.csv",
        ROOT / "data/hansen/stankiewicz1972_pointwise_covariance.csv",
        ROOT / "data/hansen/stankiewicz1972_hansen_assigned_markers.csv",
    ]
    assert all(not path.exists() for path in forbidden)
