from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/kahlert1973_hsc_r09_source_metadata.csv"
SAMPLE = ROOT / "data/hansen/kahlert1973_sample_population.csv"
PARAMETERS = ROOT / "data/hansen/kahlert1973_model_parameters.csv"
RELATION = ROOT / "data/hansen/kahlert1973_temperature_relation.csv"
PAIRINGS = ROOT / "data/hansen/kahlert1973_hansen_ingestion_candidates.csv"
README = ROOT / "data/hansen/kahlert1973_hsc_r09_README.md"
REFERENCE = ROOT / "data/validation/kahlert1973_hsc_r09_audit.json"
TOOL = ROOT / "tools/audit_kahlert1973_hsc_r09.py"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_source_identity_and_hash() -> None:
    row = _csv(META)[0]
    assert row["source_id"] == "KAHLERT1973_HSC_R09"
    assert row["hansen_graph_id"] == "HSC_R09"
    assert row["first_page"] == "1211"
    assert row["last_page"] == "1214"
    assert row["doi"] == "10.1103/PhysRevLett.30.1211"
    assert row["source_pdf_sha256"] == (
        "3052179e8d216de4d7ba015ef61e1ce73d193127602418075cf3c096fa09275a"
    )
    assert row["source_binary_committed"] == "false"


def test_measurement_class_is_not_direct_optical_edge() -> None:
    row = _csv(META)[0]
    assert row["primary_measurement_class"] == (
        "longitudinal_magnetoresistance_sdh_and_magnetophonon_resonance"
    )
    assert "Kane" in row["primary_gap_observable"]
    text = README.read_text(encoding="utf-8")
    assert "not an optical absorption-edge experiment" in text
    assert "model-conditioned" in text


def test_sample_population_does_not_invent_specimen_count() -> None:
    row = _csv(SAMPLE)[0]
    assert row["nominal_composition_x"] == "0.212"
    assert row["mobility_4p2k_cm2_v_s"] == "85600"
    assert row["carrier_concentration_4p2k_cm3"] == "1.6e15"
    assert row["physical_specimen_count_status"] == (
        "plural_samples_count_not_reported"
    )


def test_sdh_parameters_and_phonon_assignment() -> None:
    rows = {row["parameter_id"]: row for row in _csv(PARAMETERS)}
    assert rows["KAH73_MSTAR0"]["value"] == "0.005"
    assert rows["KAH73_MSTAR0"]["half_width"] == "0.0003"
    assert rows["KAH73_GSTAR0"]["value"] == "-172"
    assert rows["KAH73_GSTAR0"]["half_width"] == "10"
    assert rows["KAH73_HGTE_LO"]["value"] == "0.0171"
    assert rows["KAH73_CDTE_LO"]["value"] == "0.0196"
    assert rows["KAH73_CDTE_LO"]["evidence_role"] == (
        "source_reported_rejected_assignment"
    )


def test_temperature_relation_and_rounding_are_preserved() -> None:
    row = _csv(RELATION)[0]
    assert row["Eg0_eV"] == "0.09"
    assert row["alpha_per_K"] == "0.0085"
    assert row["derived_exact_slope_eV_per_K"] == "0.000765"
    assert row["source_reported_rounded_slope_eV_per_K"] == "0.00076"
    assert row["pointwise_covariance"] == "not_reported"


def test_hansen_candidates_are_not_assignments() -> None:
    rows = _csv(PAIRINGS)
    assert len(rows) == 2
    assert {row["candidate_status"] for row in rows} == {"plausible_not_proven"}
    assert {row["gap_eV"] for row in rows} == {"0.1512", "0.1508"}


def test_canonical_audit_is_deterministic() -> None:
    generated = subprocess.check_output([sys.executable, str(TOOL)], text=True)
    assert generated == REFERENCE.read_text(encoding="utf-8")
    audit = json.loads(generated)
    assert audit["source_scope"]["physical_specimen_count_reported"] is False
    assert audit["decision"]["controlling_decision"] == (
        "primary_source_recovered_temperature_relation_reconstructed_"
        "hansen_marker_mapping_unresolved"
    )
    assert audit["decision"]["direct_hansen_validation_authorized"] is False


def test_no_dense_digitized_or_unreported_covariance_products() -> None:
    forbidden = [
        ROOT / "data/hansen/kahlert1973_figure1_digitized.csv",
        ROOT / "data/hansen/kahlert1973_figure3_digitized.csv",
        ROOT / "data/hansen/kahlert1973_pointwise_covariance.csv",
        ROOT / "data/hansen/kahlert1973_hansen_assigned_markers.csv",
    ]
    assert all(not path.exists() for path in forbidden)
