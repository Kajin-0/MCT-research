from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/hansen/antcliffe1970_hsc_r07_source_metadata.csv"
SPECIMEN_PATH = ROOT / "data/hansen/antcliffe1970_specimens.csv"
GAP_PATH = ROOT / "data/hansen/antcliffe1970_gap_observations.csv"
PARAMETER_PATH = ROOT / "data/hansen/antcliffe1970_band_parameters.csv"
INGESTION_PATH = ROOT / "data/hansen/antcliffe1970_hansen_ingestion_candidates.csv"
README_PATH = ROOT / "data/hansen/antcliffe1970_hsc_r07_README.md"
SOURCE_GRAPH_PATH = ROOT / "data/hansen/hansen_1982_source_graph.csv"
REFERENCE_PATH = ROOT / "data/validation/antcliffe1970_hsc_r07_audit.json"
TOOL_PATH = ROOT / "tools/audit_antcliffe1970_hsc_r07.py"
STATE_PATH = (
    ROOT
    / "research/programs/empirical_bandgap/state_updates/"
    "2026-07-23-antcliffe1970-hsc-r07-acquisition.md"
)


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _tool_module():
    spec = importlib.util.spec_from_file_location("antcliffe_audit", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_primary_identity_hash_and_access_state() -> None:
    rows = _csv(METADATA_PATH)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "ANTCLIFFE1970_HSC_R07"
    assert row["hansen_graph_id"] == "HSC_R07"
    assert row["author"] == "G. A. Antcliffe"
    assert row["title"] == "Effective Mass and Spin Splitting in Hg1-xCdxTe"
    assert row["container"] == "Physical Review B"
    assert row["volume"] == "2"
    assert row["issue"] == "2"
    assert row["pages"] == "345-351"
    assert row["publication_date"] == "1970-07-15"
    assert row["doi"] == "10.1103/PhysRevB.2.345"
    assert row["full_text_status"] == "materialized_and_verified"
    assert row["source_file_library_name"] == "antcliffe1970.pdf"
    assert row["source_pdf_sha256"] == (
        "43743f5f12598b0f7987be6fa1df2199f52b845b3c163189ac93d8d811901240"
    )
    assert row["source_pdf_sha256_status"] == "verified_user_supplied_primary_pdf"
    assert row["pdf_page_count"] == "7"
    assert row["copyrighted_source_committed"] == "false"


def test_material_composition_and_protocol_contract() -> None:
    row = _csv(METADATA_PATH)[0]
    assert row["material_system"] == "Hg0.796Cd0.204Te"
    assert float(row["nominal_composition_x"]) == 0.204
    assert float(row["composition_variation_half_width_x"]) == 0.003
    assert row["composition_uncertainty_semantics"] == (
        "source_reported_spatial_composition_variation_over_10_mm_not_gaussian_sigma"
    )
    assert "relative spectral response" in row["composition_methods"]
    assert "Cd-115 radioactive tracer analyses" in row["composition_methods"]
    assert row["growth_method"] == "solid_state_recrystallization"
    assert row["carrier_type"] == "n_type"
    assert float(row["carrier_concentration_min_cm3"]) == 2e15
    assert float(row["carrier_concentration_max_cm3"]) == 1e16
    assert float(row["transport_temperature_min_k"]) == 1.5
    assert float(row["transport_temperature_max_k"]) == 4.2
    assert float(row["overall_temperature_max_k"]) == 77.0
    assert float(row["max_magnetic_field_kg"]) == 20.0
    assert row["primary_measurement_class"].startswith("shubnikov_de_haas")


def test_six_table_rows_and_named_figure_examples_are_separated() -> None:
    rows = _csv(SPECIMEN_PATH)
    table = [row for row in rows if row["source_role"] == "table1_transport_fit"]
    figures = [row for row in rows if row["source_role"] != "table1_transport_fit"]
    assert [row["specimen_id"] for row in table] == [
        "Q228-9",
        "Q270-22",
        "Q190-15",
        "Q269-11",
        "Q269-30",
        "Q193-19",
    ]
    assert {row["specimen_id"] for row in figures} == {"Q224-25", "Q115-15"}
    q115 = next(row for row in figures if row["specimen_id"] == "Q115-15")
    assert float(q115["carrier_concentration_1e15_cm3"]) == 3.3
    assert float(q115["period_delta_inv_h_1e4_oe_inv"]) == 1.43
    assert q115["direct_numeric_status"] == "exact_figure_label_not_table1_fit"
    q224 = next(row for row in figures if row["specimen_id"] == "Q224-25")
    assert q224["quality_flag"] == "region_B_rejected"


def test_table1_numeric_values_are_exact() -> None:
    rows = {
        row["specimen_id"]: row
        for row in _csv(SPECIMEN_PATH)
        if row["source_role"] == "table1_transport_fit"
    }
    expected = {
        "Q228-9": (1.80, 2.32, 7.02, 8.0, 0.48, 137),
        "Q270-22": (1.50, 3.10, 7.55, 11.0, 0.45, 119),
        "Q190-15": (0.98, 5.90, 8.30, 15.2, 0.48, 115),
        "Q269-11": (0.90, 6.60, 9.10, 19.7, 0.45, 99),
        "Q269-30": (0.81, 8.00, 9.20, 20.4, 0.47, 100),
        "Q193-19": (0.645, 9.66, 9.66, 23.0, 0.44, 93),
    }
    for specimen, values in expected.items():
        row = rows[specimen]
        actual = (
            float(row["period_delta_inv_h_1e4_oe_inv"]),
            float(row["carrier_concentration_1e15_cm3"]),
            float(row["effective_mass_ratio_1e3"]),
            float(row["fermi_energy_mev"]),
            float(row["delta_expt"]),
            int(row["g_factor"]),
        )
        assert actual == values


def test_gap_observation_classes_and_uncertainty_boundaries() -> None:
    rows = {row["observation_id"]: row for row in _csv(GAP_PATH)}
    assert set(rows) == {
        "ANT70_PC50_77K",
        "ANT70_PC50_4P2K",
        "ANT70_SDH_KP_GAP",
    }
    optical_77 = rows["ANT70_PC50_77K"]
    assert optical_77["reported_or_derived"] == "repository_derived_from_source_wavelength"
    assert float(optical_77["wavelength_um"]) == 13.7
    assert float(optical_77["wavelength_half_width_um"]) == 0.5
    assert optical_77["signed_gap_eligible"] == "false"
    assert optical_77["intrinsic_gap_eligible_without_observation_operator"] == "false"

    optical_4p2 = rows["ANT70_PC50_4P2K"]
    assert float(optical_4p2["value_ev"]) == 0.0665
    assert float(optical_4p2["value_half_width_ev"]) == 0.002
    assert float(optical_4p2["wavelength_ratio_to_77k"]) == 1.37

    transport = rows["ANT70_SDH_KP_GAP"]
    assert float(transport["value_ev"]) == 0.0635
    assert float(transport["value_half_width_ev"]) == 0.008
    assert transport["signed_gap_eligible"] == "true"
    assert transport["intrinsic_gap_eligible_without_observation_operator"] == "false"
    assert transport["independent_validation_of_hansen"] == "false"


def test_source_reported_joint_parameters_and_absent_covariance() -> None:
    rows = {row["parameter_id"]: row for row in _csv(PARAMETER_PATH)}
    assert float(rows["ANT70_M0"]["value"]) == 0.00560
    assert float(rows["ANT70_M0"]["half_width"]) == 0.00025
    assert float(rows["ANT70_EP"]["value"]) == 17.0
    assert float(rows["ANT70_EP"]["half_width"]) == 1.4
    assert float(rows["ANT70_EG"]["value"]) == 0.0635
    assert float(rows["ANT70_EG"]["half_width"]) == 0.008
    assert float(rows["ANT70_G0"]["value"]) == 164.0
    assert float(rows["ANT70_G0"]["half_width"]) == 16.0
    for key in ["ANT70_M0", "ANT70_EP", "ANT70_EG"]:
        assert "covariance_not_reported" in rows[key]["error_semantics"]


def test_executable_audit_matches_canonical_reference() -> None:
    module = _tool_module()
    expected = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    actual = module.build_audit()
    assert actual == expected
    assert module.render_reference() == REFERENCE_PATH.read_text(encoding="utf-8")


def test_rounded_table_does_not_silently_replace_source_fit() -> None:
    audit = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    rounded = audit["rounded_table_reproduction"]
    source = audit["source_reported_fit"]
    assert math.isclose(rounded["band_edge_mass_ratio"], 0.005098080627572088)
    assert math.isclose(rounded["Ep_ev"], 15.127722471940565)
    assert math.isclose(rounded["interaction_gap_ev"], 0.0516783596934091)
    assert rounded["exactly_reproduces_source_reported_parameters"] is False
    assert source["band_edge_mass_ratio"] == 0.0056
    assert source["Ep_ev"] == 17.0
    assert source["interaction_gap_ev"] == 0.0635


def test_hansen_ingestion_candidates_remain_explicitly_unresolved() -> None:
    rows = {row["candidate_id"]: row for row in _csv(INGESTION_PATH)}
    assert set(rows) == {
        "ANT70_PC_REPORTED_PAIR",
        "ANT70_SDH_TO_PC_PAIR",
        "ANT70_PC_RATIO_CHECK",
    }
    assert rows["ANT70_PC_REPORTED_PAIR"]["status"] == "plausible_not_proven"
    assert rows["ANT70_SDH_TO_PC_PAIR"]["status"] == "plausible_not_proven"
    assert rows["ANT70_PC_RATIO_CHECK"]["status"] == (
        "internal_consistency_check_not_ingestion_claim"
    )

    audit = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    assert audit["decision"]["hansen_exact_ingestion_mapping_resolved"] is False
    assert audit["decision"]["direct_hansen_validation_authorized"] is False
    assert audit["decision"]["controlling_decision"] == (
        "primary_source_recovered_hansen_ingestion_mapping_unresolved"
    )


def test_source_graph_is_corrected_without_claiming_exact_hansen_mapping() -> None:
    rows = {row["graph_id"]: row for row in _csv(SOURCE_GRAPH_PATH)}
    row = rows["HSC_R07"]
    assert row["measurement_group"] == "magnetotransport_shubnikov_de_haas"
    assert "Kane two-band interaction gap" in row["gap_observable"]
    assert row["composition_method_stated_by_hansen"] == "not_stated_in_hansen"
    assert row["temperature_series_mapping"] == (
        "unresolved_source_specific_marker_mapping"
    )
    assert row["acquisition_priority"] == "complete_primary_source_audit"
    assert "exact Hansen low-temperature pairing remains unresolved" in row["notes"]


def test_readme_and_state_preserve_claim_boundary() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    state = STATE_PATH.read_text(encoding="utf-8")
    required_readme = [
        "Shubnikov-de Haas magnetotransport",
        "primary_source_recovered_hansen_ingestion_mapping_unresolved",
        "do **not** exactly reproduce",
        "exact Antcliffe value or pairing ingested by Hansen cannot be proven",
        "Figure 5 is not digitized",
        "cannot independently validate Hansen",
    ]
    for phrase in required_readme:
        assert phrase in readme
    required_state = [
        "source PDF SHA256",
        "six-row Table I transport ledger",
        "exact Hansen source-specific marker mapping         unresolved",
        "new equation or manuscript claim                    not authorized",
    ]
    for phrase in required_state:
        assert phrase in state


def test_no_duplicate_figure_or_inferred_hansen_products_exist() -> None:
    forbidden = [
        ROOT / "data/hansen/antcliffe1970_figure5_digitized.csv",
        ROOT / "data/hansen/antcliffe1970_figure5_curve.csv",
        ROOT / "data/hansen/antcliffe1970_hansen_marker_assignment.csv",
        ROOT / "data/hansen/antcliffe1970_inferred_hansen_points.csv",
        ROOT / "data/hansen/antcliffe1970_pointwise_covariance.csv",
    ]
    assert all(not path.exists() for path in forbidden)
