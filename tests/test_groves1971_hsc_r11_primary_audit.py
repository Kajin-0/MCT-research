from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "data/hansen/groves1971_hsc_r11_source_metadata.csv"
SAMPLE = ROOT / "data/hansen/groves1971_sample_record.csv"
STATES = ROOT / "data/hansen/groves1971_measurement_states.csv"
TRANSITIONS = ROOT / "data/hansen/groves1971_transition_summary.csv"
PARAMETERS = ROOT / "data/hansen/groves1971_model_parameters.csv"
CANDIDATES = ROOT / "data/hansen/groves1971_hansen_ingestion_candidates.csv"
README = ROOT / "data/hansen/groves1971_hsc_r11_README.md"
GRAPH = ROOT / "data/hansen/hansen_1982_source_graph.csv"
REFERENCE = ROOT / "data/validation/groves1971_hsc_r11_audit.json"
TOOL = ROOT / "tools/audit_groves1971_hsc_r11.py"


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_source_identity_and_hash() -> None:
    row = _csv(META)[0]
    assert row["source_id"] == "GROVES1971_HSC_R11"
    assert row["hansen_graph_id"] == "HSC_R11"
    assert row["first_page"] == "451"
    assert row["last_page"] == "455"
    assert row["doi"] == "10.1016/0038-1098(71)90320-6"
    assert row["source_pdf_sha256"] == (
        "ccbad551b170c97d2550cd31533b80ec6715772793dc4b18b8d56466fd83083f"
    )
    assert row["source_binary_committed"] == "false"


def test_single_sample_provenance_is_preserved() -> None:
    row = _csv(SAMPLE)[0]
    assert row["physical_specimen_count"] == "1"
    assert row["nominal_composition_x"] == "0.161"
    assert row["composition_half_width"] == "0.003"
    assert row["carrier_concentration_4k_cm3"] == "9.4e14"
    assert row["hall_mobility_4k_cm2_v_s"] == "2.6e6"
    assert row["reflecting_surface"] == "(100)"


def test_measurement_class_is_interband_magnetoreflection() -> None:
    row = _csv(META)[0]
    assert row["primary_measurement_class"] == (
        "interband_magnetoreflection_circular_polarization"
    )
    assert "Pidgeon-Brown" in row["primary_gap_observable"]
    text = README.read_text(encoding="utf-8")
    assert "genuinely magneto-optical" in text
    assert "not a direct zero-field extrapolation" not in text
    assert "cannot be determined reliably by extrapolating" in text


def test_body_and_abstract_temperature_states_are_not_conflated() -> None:
    rows = {row["state_id"]: row for row in _csv(STATES)}
    assert rows["GR71_LOW_BODY"]["temperature_min_k"] == "20"
    assert rows["GR71_LOW_BODY"]["temperature_max_k"] == "30"
    assert rows["GR71_LOW_BODY"]["gamma6_minus_gamma8_gap_eV"] == "-0.01"
    assert rows["GR71_HIGH_BODY"]["temperature_min_k"] == "90"
    assert rows["GR71_HIGH_BODY"]["temperature_max_k"] == "100"
    assert rows["GR71_HIGH_BODY"]["gamma6_minus_gamma8_gap_eV"] == "0.01"
    assert rows["GR71_ABSTRACT_4K"]["gamma6_minus_gamma8_gap_eV"] == ""
    assert rows["GR71_ABSTRACT_77K"]["gamma6_minus_gamma8_gap_eV"] == ""


def test_transition_summary_preserves_direct_observation_limits() -> None:
    rows = {row["summary_id"]: row for row in _csv(TRANSITIONS)}
    low = rows["GR71_FIG2_LOW"]
    assert low["field_max_kOe"] == "100"
    assert low["photon_energy_observed_max_eV"] == "0.3"
    assert low["photon_energy_plotted_max_eV"] == "0.2"
    assert low["transition_count_status"] == "about_20"
    assert low["figure_digitized"] == "false"
    assert low["pointwise_covariance"] == "not_reported"
    assert rows["GR71_HIGH_NOT_SHOWN"]["state_id"] == "GR71_HIGH_BODY"


def test_model_parameters_preserve_status_and_sign() -> None:
    rows = {row["parameter_id"]: row for row in _csv(PARAMETERS)}
    assert rows["GR71_GAP_LOW"]["value"] == "-0.01"
    assert rows["GR71_GAP_HIGH"]["value"] == "0.01"
    assert rows["GR71_EP"]["value"] == "18.5"
    assert rows["GR71_MV_SIGNED"]["value"] == "-0.28"
    assert rows["GR71_MV_SIGNED"]["half_width"] == "0.1"
    assert rows["GR71_MV_SIGNED"]["evidence_class"] == (
        "fit_sensitivity_interval_not_statistical_uncertainty"
    )


def test_hansen_candidates_are_not_marker_assignments() -> None:
    rows = _csv(CANDIDATES)
    assert len(rows) == 4
    assert {row["candidate_status"] for row in rows} == {
        "source_native_candidate_not_hansen_assignment",
        "qualitative_candidate_not_numeric_assignment",
    }
    numeric = [row for row in rows if row["gap_eV"]]
    qualitative = [row for row in rows if not row["gap_eV"]]
    assert len(numeric) == 2
    assert len(qualitative) == 2


def test_source_graph_records_completed_audit() -> None:
    row = next(row for row in _csv(GRAPH) if row["graph_id"] == "HSC_R11")
    assert row["measurement_group"] == "interband_magnetoreflection"
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    assert "20_30" in row["temperature_series_mapping"]
    assert "0.161" in row["composition_method_stated_by_hansen"]


def test_canonical_audit_is_deterministic() -> None:
    generated = subprocess.check_output([sys.executable, str(TOOL)], text=True)
    assert generated == REFERENCE.read_text(encoding="utf-8")
    audit = json.loads(generated)
    assert audit["source_scope"]["physical_specimen_count"] == 1
    assert audit["temperature_provenance"]["body_and_abstract_temperature_labels_identical"] is False
    assert audit["decision"]["controlling_decision"] == (
        "primary_source_recovered_interband_magnetoreflection_parameters_"
        "reconstructed_temperature_labels_and_hansen_marker_mapping_unresolved"
    )
    assert audit["decision"]["direct_hansen_validation_authorized"] is False


def test_no_dense_digitization_or_invented_covariance_products() -> None:
    forbidden = [
        ROOT / "data/hansen/groves1971_figure2_digitized.csv",
        ROOT / "data/hansen/groves1971_theoretical_curves.csv",
        ROOT / "data/hansen/groves1971_pointwise_covariance.csv",
        ROOT / "data/hansen/groves1971_hansen_assigned_markers.csv",
    ]
    assert all(not path.exists() for path in forbidden)
