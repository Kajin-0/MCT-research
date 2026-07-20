from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.audit_mroczkowski_1983_vacancy_tail import audit  # noqa: E402

INPUT = ROOT / "data/evidence/mroczkowski_1983_vacancy_tail_constraint.json"


def load_payload() -> dict[str, object]:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def write_payload(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "mroczkowski.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_publisher_record_and_source_status_are_exact() -> None:
    result = audit(INPUT)
    assert result["source_doi"] == "10.1116/1.572210"
    assert result["measurement_class"] == "vacancy_conditioned_exponential_tail_slope"
    assert result["composition_nominal_x"] == pytest.approx(0.3)
    assert result["carrier_type"] == "p"
    assert result["temperature_context"] == "ambient temperature"


def test_reported_slopes_and_acceptor_density_are_preserved() -> None:
    reported = audit(INPUT)["reported_values"]
    assert reported == {
        "high_purity_tail_slope_k_eV_inverse": 148.0,
        "vacancy_rich_acceptor_concentration_cm3": 2.0e16,
        "vacancy_rich_tail_slope_k_eV_inverse": 105.0,
    }


def test_e_fold_energy_transformations_are_deterministic() -> None:
    derived = audit(INPUT)["derived_diagnostics"]
    assert derived["high_purity_e_fold_energy_meV"] == pytest.approx(
        6.756756756756757,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["vacancy_rich_e_fold_energy_meV"] == pytest.approx(
        9.523809523809524,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["e_fold_energy_difference_meV"] == pytest.approx(
        2.7670527670527667,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["e_fold_width_ratio"] == pytest.approx(
        1.4095238095238096,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["e_fold_width_increase_percent"] == pytest.approx(
        40.95238095238096,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["tail_slope_ratio"] == pytest.approx(
        0.7094594594594594,
        rel=0.0,
        abs=1.0e-12,
    )
    assert derived["tail_slope_decrease_percent"] == pytest.approx(
        29.054054054054056,
        rel=0.0,
        abs=1.0e-12,
    )


def test_authorization_boundary_remains_closed() -> None:
    decision = audit(INPUT)["decision"]
    assert decision == {
        "complete_absorption_operator_implementation_authorized": False,
        "full_text_recovery_priority": "high",
        "latent_material_gap_point_authorized": False,
        "paired_protocol_vacancy_covariate_priority_strengthened": True,
        "uncertainty_weighted_fitting_authorized": False,
        "universal_vacancy_correction_authorized": False,
        "vacancy_conditioned_tail_mechanism_evidence_authorized": True,
        "within_specimen_paired_contrast_established": False,
    }
    assert "does not establish a latent-gap shift" in audit(INPUT)["claim_boundary"]


def test_full_text_status_cannot_be_promoted_without_recovery(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["primary_full_text_recovered"] = True
    with pytest.raises(ValueError, match="full-text status"):
        audit(write_payload(tmp_path, payload))


def test_ambient_temperature_cannot_be_relabelled_exactly(tmp_path: Path) -> None:
    payload = load_payload()
    payload["common_metadata"]["temperature_K"] = 300.0
    with pytest.raises(ValueError, match="exact Kelvin"):
        audit(write_payload(tmp_path, payload))


def test_missing_uncertainties_cannot_be_invented(tmp_path: Path) -> None:
    payload = load_payload()
    payload["reported_endpoints"][0]["tail_slope_sigma_eV_inverse"] = 1.0
    with pytest.raises(ValueError, match="uncertainty"):
        audit(write_payload(tmp_path, payload))


def test_same_specimen_causality_cannot_be_promoted(tmp_path: Path) -> None:
    payload = load_payload()
    payload["common_metadata"]["same_physical_specimen_contrast_established"] = True
    with pytest.raises(ValueError, match="same_physical_specimen"):
        audit(write_payload(tmp_path, payload))


def test_latent_gap_or_universal_correction_cannot_be_authorized(tmp_path: Path) -> None:
    payload = load_payload()
    payload["decision"]["latent_material_gap_point_authorized"] = True
    with pytest.raises(ValueError, match="decision"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["decision"]["universal_vacancy_correction_authorized"] = True
    with pytest.raises(ValueError, match="decision"):
        audit(write_payload(tmp_path, payload))


def test_publisher_identity_fingerprint_is_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["publisher_record_fingerprint_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="publisher source field"):
        audit(write_payload(tmp_path, payload))
