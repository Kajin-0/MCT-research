from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/elliott1972_hsc_r08_source_metadata.csv"
SPECIMENS = ROOT / "data/hansen/elliott1972_specimens.csv"
CARRIERS = ROOT / "data/hansen/elliott1972_table1_carriers.csv"
GAPS = ROOT / "data/hansen/elliott1972_table2_gap_candidates.csv"
PARAMETERS = ROOT / "data/hansen/elliott1972_model_parameters.csv"
PAIRINGS = ROOT / "data/hansen/elliott1972_hansen_ingestion_candidates.csv"
README = ROOT / "data/hansen/elliott1972_hsc_r08_README.md"
REFERENCE = ROOT / "data/validation/elliott1972_hsc_r08_audit.json"
TOOL = ROOT / "tools/audit_elliott1972_hsc_r08.py"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_source_identity_and_hash() -> None:
    row = _csv(META)[0]
    assert row["source_id"] == "ELLIOTT1972_HSC_R08"
    assert row["hansen_graph_id"] == "HSC_R08"
    assert row["page_range"] == "2985-2997"
    assert row["doi"] == "10.1103/PhysRevB.5.2985"
    assert row["source_pdf_sha256"] == (
        "509bbcfd3c4b72312ab49ee2460e56561a9324e4e96af56dd29e8612b0b2b328"
    )
    assert row["source_binary_committed"] == "false"


def test_measurement_class_is_pressure_magnetotransport() -> None:
    row = _csv(META)[0]
    assert row["primary_measurement_class"] == "hydrostatic_pressure_magnetotransport"
    assert "zero-pressure signed gap" in row["primary_gap_observable"]
    text = README.read_text(encoding="utf-8")
    assert "not direct optical edges" in text
    assert "Hansen 1982 grouped HSC_R08 with magneto-optical gap evidence" in text


def test_specimen_registry_and_transition_intervals() -> None:
    rows = {row["sample_id"]: row for row in _csv(SPECIMENS)}
    assert set(rows) == {"7B", "7B1", "8B"}
    assert rows["7B"]["anneal_state"] == "annealed"
    assert rows["7B1"]["anneal_state"] == "unannealed"
    assert rows["8B"]["anneal_state"] == "unannealed"
    assert rows["7B"]["transition_interval_4p2k_kbar"] == "3-4"
    assert rows["7B1"]["transition_interval_4p2k_kbar"] == "3-4"
    assert rows["8B"]["transition_interval_4p2k_kbar"] == "7-8"
    assert all(row["composition_half_width_x"] == "0.005" for row in rows.values())


def test_table1_exact_rows_and_pressure_footnote() -> None:
    rows = _csv(CARRIERS)
    assert len(rows) == 11
    index = {row["observation_id"]: row for row in rows}
    assert index["ELL72_T1_7B_77_H"]["pressure_condition"] == "P_gt_5_kbar"
    assert index["ELL72_T1_7B_77_H"]["concentration_cm3"] == "1.5e16"
    assert index["ELL72_T1_7B_77_E"]["mobility_cm2_v_s"] == "3.7e5"
    assert index["ELL72_T1_8B_4P2_H"]["concentration_cm3"] == "7.6e17"
    assert index["ELL72_T1_8B_4P2_E"]["mobility_cm2_v_s"] == "1.6e4"


def test_table2_exact_model_outputs() -> None:
    rows = {row["observation_id"]: row for row in _csv(GAPS)}
    assert len(rows) == 5
    assert rows["ELL72_T2_7B_4P2"]["zero_pressure_gap_mev"] == "-16"
    assert rows["ELL72_T2_7B1_4P2"]["fermi_energy_from_valence_mev"] == "16"
    assert rows["ELL72_T2_8B_4P2"]["zero_pressure_gap_mev"] == "-33"
    assert rows["ELL72_T2_7B_77_MH03"]["hole_mass_ratio_assumption"] == "0.3"
    assert rows["ELL72_T2_7B_77_MH03"]["zero_pressure_gap_mev"] == "-8.0"
    assert rows["ELL72_T2_7B_77_MH07"]["hole_mass_ratio_assumption"] == "0.7"
    assert rows["ELL72_T2_7B_77_MH07"]["zero_pressure_gap_mev"] == "2.0"


def test_pressure_coefficient_and_fixed_kane_parameter() -> None:
    rows = {row["parameter_id"]: row for row in _csv(PARAMETERS)}
    assert rows["ELL72_GAP_PRESSURE_COEFF"]["value"] == "7.0e-6"
    assert rows["ELL72_GAP_PRESSURE_COEFF"]["unit"] == "eV_per_bar"
    assert rows["ELL72_KANE_MATRIX"]["value_status"] == "fixed_inherited_parameter"
    assert rows["ELL72_KANE_MATRIX"]["value"] == "8.4e-8"


def test_pairings_are_candidates_not_assignments() -> None:
    rows = _csv(PAIRINGS)
    assert len(rows) == 2
    assert {row["candidate_status"] for row in rows} == {"plausible_not_proven"}
    assert {row["slope_ev_per_k"] for row in rows} == {
        "0.00010989010989010989",
        "0.00024725274725274725",
    }
    assert "Hansen markers are not source-labeled" in rows[0]["reason"]


def test_canonical_audit_is_deterministic() -> None:
    generated = subprocess.check_output([sys.executable, str(TOOL)], text=True)
    assert generated == REFERENCE.read_text(encoding="utf-8")
    audit = json.loads(generated)
    assert audit["source_scope"]["physical_specimen_count_lower_bound"] == 4
    assert audit["decision"]["controlling_decision"] == (
        "primary_source_recovered_source_native_gap_candidates_reconstructed_"
        "hansen_marker_mapping_unresolved"
    )
    assert audit["decision"]["direct_hansen_validation_authorized"] is False


def test_no_dense_digitized_or_unreported_covariance_products() -> None:
    forbidden = [
        ROOT / "data/hansen/elliott1972_figure5_digitized.csv",
        ROOT / "data/hansen/elliott1972_figure8_digitized.csv",
        ROOT / "data/hansen/elliott1972_pointwise_pressure_covariance.csv",
        ROOT / "data/hansen/elliott1972_hansen_assigned_markers.csv",
    ]
    assert all(not path.exists() for path in forbidden)
