from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mct_research.yue_2006_vacancy_anomaly import (  # noqa: E402
    bulk_critical_absorption_cm1,
)
from tools.audit_yue_2006_vacancy_anomaly import audit  # noqa: E402

INPUT = ROOT / "data/evidence/yue_2006_vacancy_anomaly.json"


def load_payload() -> dict[str, object]:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def write_payload(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "yue2006.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_exact_specimen_inventory_and_anomaly_diagnostics() -> None:
    result = audit(INPUT)
    assert result["source_doi"] == "10.1063/1.2221411"
    assert result["specimen_count"] == 5
    assert result["anomalous_specimen_count"] == 4
    assert result["nonanomalous_specimen_ids"] == ["M17"]
    assert result["bulk_mean_deltaE_meV"] == pytest.approx(10.9)
    assert result[
        "as_grown_and_vacancy_intensifying_mbe_mean_deltaE_meV"
    ] == pytest.approx(9.85)
    assert result["vacancy_removing_m17_deltaE_meV"] == pytest.approx(0.0)
    assert result["positive_anomaly_deltaE_range_meV"] == pytest.approx([9.7, 11.3])
    assert result["positive_anomaly_mean_deltaE_meV"] == pytest.approx(10.375)


def test_bulk_critical_alpha_reference_values() -> None:
    expected = {
        (0.232, 11.0): 1946.37688,
        (0.232, 77.0): 1912.59016,
        (0.232, 300.0): 1798.432,
        (0.337, 11.0): 2847.33883,
        (0.337, 77.0): 2742.10381,
        (0.337, 300.0): 2386.537,
    }
    records = {
        (row["composition_x"], row["temperature_K"]): row["critical_absorption_cm1"]
        for row in audit(INPUT)["bulk_critical_absorption_reference"]
    }
    assert set(records) == set(expected)
    for key, value in expected.items():
        assert records[key] == pytest.approx(value, rel=0.0, abs=1.0e-10)
        assert bulk_critical_absorption_cm1(*key) == pytest.approx(
            value,
            rel=0.0,
            abs=1.0e-10,
        )


def test_observation_classes_remain_separate() -> None:
    payload = load_payload()
    operators = payload["observation_operators"]
    assert operators["bulk"]["measurement_class"] == (
        "bulk_absorption_extrapolation_to_critical_alpha"
    )
    assert operators["mbe"]["measurement_class"] == (
        "exponential_edge_kane_plateau_intersection"
    )
    assert operators["mbe"]["numerical_operator_complete_without_native_spectrum"] is False
    assert operators["alternative_bulk_methods"]["reported_scatter_meV_less_than"] == 2.0
    assert operators["alternative_bulk_methods"]["scatter_is_not_specimen_uncertainty"] is True


def test_composition_is_absorption_derived_not_independent() -> None:
    payload = load_payload()
    provenance = payload["composition_provenance"]
    assert provenance["status"] == (
        "absorption_derived_circular_for_material_law_validation"
    )
    assert provenance["independent_composition_measurement"] is False
    assert provenance["composition_sigma_x"] is None
    assert provenance["critical_energy_total_error_meV_less_than"] == 0.8
    assert provenance["critical_energy_error_is_not_table_deltaE_sigma"] is True


def test_carrier_density_temperature_groups_are_not_pooled() -> None:
    result = audit(INPUT)
    assert result["carrier_density_temperature_groups"] == {
        "bulk_K": [77.0],
        "mbe_K": [300.0],
    }
    assert result["decision"]["cross_temperature_carrier_density_correlation_authorized"] is False


def test_decision_boundary_is_exact() -> None:
    assert audit(INPUT)["decision"] == {
        "cross_temperature_carrier_density_correlation_authorized": False,
        "independent_composition_validation_authorized": False,
        "latent_material_gap_points_authorized": False,
        "measured_vacancy_concentration_available": False,
        "processing_conditioned_vacancy_mechanism_evidence_authorized": True,
        "same_specimen_causal_contrast_established": False,
        "temperature_resolved_vacancy_anomaly_evidence_authorized": True,
        "uncertainty_weighted_material_law_fitting_authorized": False,
        "universal_vacancy_correction_authorized": False,
        "vacancy_removing_anneal_control_evidence_status": "conditional",
    }
    assert "does not provide independent composition" in audit(INPUT)["claim_boundary"]


def test_operator_rejects_extrapolation() -> None:
    with pytest.raises(ValueError, match="composition_x"):
        bulk_critical_absorption_cm1(0.20, 77.0)
    with pytest.raises(ValueError, match="composition_x"):
        bulk_critical_absorption_cm1(0.35, 77.0)
    with pytest.raises(ValueError, match="temperature_k"):
        bulk_critical_absorption_cm1(0.232, 10.0)
    with pytest.raises(ValueError, match="temperature_k"):
        bulk_critical_absorption_cm1(0.232, 301.0)


def test_table_value_and_thickness_relation_are_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["specimens"][3]["deltaE_meV"] = 9.8
    with pytest.raises(ValueError, match="M16 deltaE"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["specimens"][0]["thickness_relation"] = "eq"
    with pytest.raises(ValueError, match="B2 thickness relation"):
        audit(write_payload(tmp_path, payload))


def test_unreported_uncertainty_or_vacancy_metrology_cannot_be_invented(
    tmp_path: Path,
) -> None:
    payload = load_payload()
    payload["composition_provenance"]["composition_sigma_x"] = 0.001
    with pytest.raises(ValueError, match="composition uncertainty"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["specimens"][3]["achieved_vacancy_concentration_measured"] = True
    with pytest.raises(ValueError, match="M16 vacancy concentration"):
        audit(write_payload(tmp_path, payload))


def test_processing_control_cannot_be_promoted_to_same_specimen_causality(
    tmp_path: Path,
) -> None:
    payload = load_payload()
    payload["mechanism_interpretation"][
        "same_physical_specimen_before_after_processing"
    ] = True
    with pytest.raises(ValueError, match="paired contrast"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["decision"]["universal_vacancy_correction_authorized"] = True
    with pytest.raises(ValueError, match="decision boundary"):
        audit(write_payload(tmp_path, payload))


def test_source_fingerprint_and_noncommitment_are_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["canonical_extracted_record_fingerprint_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="fingerprint"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["source"]["copyrighted_source_content_committed"] = True
    with pytest.raises(ValueError, match="copyrighted"):
        audit(write_payload(tmp_path, payload))
