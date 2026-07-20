from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.audit_chang2006_figure2_readiness import audit  # noqa: E402

INPUT = ROOT / "data/evidence/chang2006_figure2_readiness.json"


def load_payload() -> dict[str, object]:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def write_payload(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "figure2-readiness.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def profile_map(records: list[dict[str, float]]) -> dict[float, dict[str, float]]:
    return {record["scale"]: record for record in records}


def test_source_readiness_gate_is_closed() -> None:
    result = audit(INPUT)
    assert result["source_readiness"] == {
        "figure_composition_x": 0.21,
        "caption_temperature_K": 80,
        "body_temperature_K": 77,
        "temperature_metadata_consistent": False,
        "native_numeric_data_recovered": False,
        "same_specimen_urbach_width_recovered": False,
        "same_specimen_hyperbola_b_recovered": False,
    }
    assert result["decision"]["quantitative_operator_validation_authorized"] is False
    assert result["decision"]["figure_digitization_for_gap_inference_authorized"] is False
    assert result["decision"]["transfer_x023_b_as_exact_x021_input_authorized"] is False
    assert result["decision"]["material_gap_fit_authorized"] is False


def test_declared_synthetic_sampling_and_range_are_deterministic() -> None:
    result = audit(INPUT)
    assert result["synthetic_point_count"] == 105
    assert result["synthetic_tail_point_count_at_truth"] == 14
    assert result["synthetic_absorption_range_cm1"] == pytest.approx(
        [525.9907333699302, 22945.053992721336],
        rel=1e-12,
        abs=1e-12,
    )


def test_local_weighted_identifiability_matches_reference() -> None:
    result = audit(INPUT)["local_weighted_identifiability"]
    assert result["parameter_order"] == [
        "edge_eV",
        "log_urbach_width",
        "log_hyperbola_b",
        "log_amplitude",
    ]
    assert result["weighted_jacobian_condition_number"] == pytest.approx(
        255.6884697507069,
        rel=1e-8,
    )
    errors = result["linearized_standard_errors"]
    assert errors["edge_meV"] == pytest.approx(0.34545, rel=2e-4)
    assert errors["relative_urbach_width"] == pytest.approx(0.02416477, rel=2e-6)
    assert errors["relative_hyperbola_b"] == pytest.approx(0.01844270, rel=2e-6)
    assert errors["relative_amplitude"] == pytest.approx(0.01299676, rel=2e-6)
    correlations = result["correlations"]
    assert correlations["edge_log_urbach_width"] == pytest.approx(0.73098464, rel=2e-7)
    assert correlations["edge_log_hyperbola_b"] == pytest.approx(0.80113858, rel=2e-7)
    assert correlations["log_hyperbola_b_log_amplitude"] == pytest.approx(
        -0.92953996,
        rel=2e-7,
    )


def test_transferred_urbach_width_can_bias_edge_by_mev_scale() -> None:
    records = profile_map(audit(INPUT)["fixed_urbach_width_profiles"])
    expected_biases = {
        0.8: -1.720,
        0.9: -0.825,
        1.0: 0.000,
        1.1: 0.765,
        1.2: 1.490,
    }
    for scale, expected in expected_biases.items():
        assert records[scale]["edge_bias_meV"] == pytest.approx(expected, abs=0.006)
    assert records[1.1]["root_mean_square_log_residual"] == pytest.approx(
        0.0201320835,
        rel=1e-7,
    )


def test_transferred_hyperbola_b_can_bias_edge_while_fit_looks_close() -> None:
    records = profile_map(audit(INPUT)["fixed_hyperbola_b_profiles"])
    expected_biases = {
        0.9: -0.975,
        0.95: -0.470,
        1.0: 0.000,
        1.03: 0.265,
        1.05: 0.435,
        1.1: 0.835,
    }
    for scale, expected in expected_biases.items():
        assert records[scale]["edge_bias_meV"] == pytest.approx(expected, abs=0.006)
    assert records[1.03]["root_mean_square_log_residual"] == pytest.approx(
        0.00568234195,
        rel=1e-7,
    )
    assert audit(INPUT)["visually_small_residual_can_mask_mev_scale_edge_bias"] is True


def test_synthetic_screen_is_not_relabelled_as_real_uncertainty() -> None:
    result = audit(INPUT)
    assert result["decision"]["assign_real_specimen_uncertainty_from_synthetic_screen"] is False
    assert "not a measurement uncertainty" in result["claim_boundary"]


def test_temperature_inconsistency_cannot_be_erased(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["temperature_metadata_consistent"] = True
    with pytest.raises(ValueError, match="temperature_metadata_consistent"):
        audit(write_payload(tmp_path, payload))


def test_external_x023_b_cannot_be_promoted_to_figure2_input(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["reported_external_b"][
        "admissible_as_exact_figure2_input"
    ] = True
    with pytest.raises(ValueError, match="external b"):
        audit(write_payload(tmp_path, payload))


def test_source_hash_and_noncommitment_are_fail_closed(tmp_path: Path) -> None:
    payload = load_payload()
    payload["source"]["input_asset_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="asset hash"):
        audit(write_payload(tmp_path, payload))

    payload = load_payload()
    payload["source"]["copyrighted_source_committed"] = True
    with pytest.raises(ValueError, match="copyrighted"):
        audit(write_payload(tmp_path, payload))


def test_quantitative_validation_cannot_be_authorized_without_new_evidence(
    tmp_path: Path,
) -> None:
    payload = load_payload()
    payload["decision"]["quantitative_operator_validation_authorized"] = True
    with pytest.raises(ValueError, match="quantitative_operator_validation_authorized"):
        audit(write_payload(tmp_path, payload))
