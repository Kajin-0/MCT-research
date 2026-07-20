from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mct_research.finkman_1984_operational_edge import (  # noqa: E402
    absorption_cm1_at_energy,
    composition_from_zero_intercept_wavenumber_300k_500um,
    energy_at_absorption_cm1,
    energy_ev_to_wavenumber_cm1,
    operational_edge_500_cm1,
    published_eq11_operational_edge_ev,
    zero_intercept_absorption_cm1,
    zero_intercept_energy_ev,
)
from tools.audit_finkman_1984_operational_edge import audit  # noqa: E402

INPUT = ROOT / "data/evidence/finkman_1984_operational_edge.json"


def load_payload() -> dict[str, object]:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def write_payload(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "finkman.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def row_map() -> dict[tuple[float, float], dict[str, float]]:
    return {
        (row["composition_x"], row["temperature_K"]): row
        for row in audit(INPUT)["reference_rows"]
    }


def test_source_semantics_and_decision_are_fail_closed() -> None:
    result = audit(INPUT)
    assert result["source_doi"] == "10.1063/1.333828"
    assert result["decision"] == {
        "copyrighted_source_content_committed": False,
        "historical_operational_edge_evidence_authorized": True,
        "latent_material_gap_point_authorized": False,
        "pool_with_magneto_optical_gaps_by_default": False,
        "source_bound_threshold_operator_authorized": True,
        "universal_gap_law_fit_authorized": False,
        "zero_intercept_and_alpha500_interchangeable": False,
    }
    assert "do not identify an intrinsic material gap" in result["claim_boundary"]


def test_eq10_reference_thresholds_and_spans() -> None:
    rows = row_map()
    expected = {
        (0.215, 80.0): {
            "alpha_20_cm1_eV": 0.09529904857121008,
            "alpha_50_cm1_eV": 0.09903632076919511,
            "alpha_500_cm1_eV": 0.10842786752634725,
            "alpha_1000_cm1_eV": 0.11125500480593087,
            "alpha_20_to_1000_span_meV": 15.95595623472079,
        },
        (0.215, 300.0): {
            "alpha_20_cm1_eV": 0.15266049443480623,
            "alpha_50_cm1_eV": 0.1614762093971933,
            "alpha_500_cm1_eV": 0.1836295862134775,
            "alpha_1000_cm1_eV": 0.19029841714042606,
            "alpha_20_to_1000_span_meV": 37.63792270561983,
        },
        (0.29, 80.0): {
            "alpha_20_cm1_eV": 0.21597938624696275,
            "alpha_50_cm1_eV": 0.21949937517762305,
            "alpha_500_cm1_eV": 0.22834490177447567,
            "alpha_1000_cm1_eV": 0.23100767060757185,
            "alpha_20_to_1000_span_meV": 15.028284360609101,
        },
        (0.29, 300.0): {
            "alpha_20_cm1_eV": 0.2490169049667393,
            "alpha_50_cm1_eV": 0.25732007836154575,
            "alpha_500_cm1_eV": 0.2781854681536274,
            "alpha_1000_cm1_eV": 0.28446657635226497,
            "alpha_20_to_1000_span_meV": 35.449671385525654,
        },
    }
    for key, fields in expected.items():
        for field, value in fields.items():
            assert rows[key][field] == pytest.approx(value, rel=0.0, abs=1.0e-12)


def test_eq10_inverse_round_trip_including_boundaries() -> None:
    for x in (0.205, 0.215, 0.29):
        for temperature in (80.0, 300.0):
            for absorption in (20.0, 50.0, 500.0, 1000.0):
                energy = energy_at_absorption_cm1(absorption, temperature, x)
                recovered = absorption_cm1_at_energy(energy, temperature, x)
                assert recovered == pytest.approx(absorption, rel=0.0, abs=1.0e-9)


def test_operational_edge_is_explicitly_alpha_500() -> None:
    for x in (0.205, 0.215, 0.29):
        for temperature in (80.0, 300.0):
            assert operational_edge_500_cm1(temperature, x) == pytest.approx(
                energy_at_absorption_cm1(500.0, temperature, x),
                rel=0.0,
                abs=1.0e-15,
            )


def test_published_eq11_rounding_difference_is_preserved() -> None:
    residual = audit(INPUT)["published_eq11_rounding_residual_meV"]
    assert residual["minimum"] == pytest.approx(-0.25666126587547966, abs=1.0e-12)
    assert residual["maximum"] == pytest.approx(-0.0869234021226295, abs=1.0e-12)
    assert residual["maximum_absolute"] == pytest.approx(
        0.25666126587547966,
        abs=1.0e-12,
    )
    assert published_eq11_operational_edge_ev(300.0, 0.29) < operational_edge_500_cm1(
        300.0,
        0.29,
    )


def test_zero_intercept_is_thickness_dependent_and_not_alpha_500() -> None:
    assert zero_intercept_absorption_cm1(500.0) == pytest.approx(
        54.3656365691809,
        rel=0.0,
        abs=1.0e-12,
    )
    rows = {row["composition_x"]: row for row in audit(INPUT)["zero_intercept_rows"]}
    assert rows[0.215]["zero_intercept_minus_alpha500_meV"] == pytest.approx(
        -21.34800247183563,
        abs=1.0e-12,
    )
    assert rows[0.29]["zero_intercept_minus_alpha500_meV"] == pytest.approx(
        -20.10683953742659,
        abs=1.0e-12,
    )


def test_zero_intercept_composition_relation_uses_wavenumber_not_absorption() -> None:
    for x, tolerance in ((0.215, 6.0e-5), (0.29, 1.1e-4)):
        edge = zero_intercept_energy_ev(500.0, 300.0, x)
        wavenumber = energy_ev_to_wavenumber_cm1(edge)
        recovered = composition_from_zero_intercept_wavenumber_300k_500um(wavenumber)
        assert recovered == pytest.approx(x, abs=tolerance)

    with pytest.raises(ValueError, match="composition calibration"):
        composition_from_zero_intercept_wavenumber_300k_500um(
            zero_intercept_absorption_cm1(500.0)
        )


def test_thin_sample_zero_intercept_can_leave_common_absorption_domain() -> None:
    thickness = {row["thickness_um"]: row for row in audit(INPUT)["thickness_rows"]}
    assert thickness[25.0]["inside_common_operator_domain"] is False
    assert thickness[50.0]["inside_common_operator_domain"] is True
    assert thickness[500.0]["inside_common_operator_domain"] is True
    with pytest.raises(ValueError, match="absorption_cm1"):
        zero_intercept_energy_ev(25.0, 300.0, 0.29)


def test_operator_rejects_extrapolation() -> None:
    with pytest.raises(ValueError, match="composition_x"):
        energy_at_absorption_cm1(500.0, 300.0, 0.30)
    with pytest.raises(ValueError, match="temperature_k"):
        energy_at_absorption_cm1(500.0, 77.0, 0.29)
    with pytest.raises(ValueError, match="absorption_cm1"):
        energy_at_absorption_cm1(19.0, 300.0, 0.29)
    with pytest.raises(ValueError, match="absorption_cm1"):
        energy_at_absorption_cm1(1001.0, 300.0, 0.29)


def test_source_fingerprint_and_decision_cannot_be_promoted(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["source_content_fingerprint_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="fingerprint"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["decision"]["latent_material_gap_point_authorized"] = True
    with pytest.raises(ValueError, match="decision"):
        audit(write_payload(tmp_path, payload))
