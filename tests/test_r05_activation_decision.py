from __future__ import annotations

import json
from pathlib import Path


def _decision() -> dict[str, object]:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "validation"
        / "r05_activation_decision.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_r05_final_decision_is_benchmark_reframe() -> None:
    record = _decision()
    assert record["schema_version"] == "r05_activation_decision_v1"
    assert record["decision"] == "REFRAME_AS_METHOD_BENCHMARK"
    assert record["failed_activation_gates"] == [
        "source_supported_hgcdte_parameter_regime",
        "survives_source_grounded_experimental_convolution",
        "experiment_can_distinguish_models",
        "next_full_kane_calculation_is_decision_changing",
    ]


def test_r05_threshold_is_bracketed_without_claiming_universality() -> None:
    record = _decision()
    bracket = record["threshold_bracket_near_massless_mean"]
    assert bracket["lower_g"] == 0.25
    assert bracket["lower_delta_1"] < 0.10
    assert bracket["upper_g"] == 0.30
    assert bracket["upper_delta_1"] > 0.10
    assert "not a universal critical coupling" in bracket["interpretation"]


def test_r05_material_mapping_remains_exploratory() -> None:
    record = _decision()
    mapping = record["hgcdte_exploratory_mapping"]
    nominal = next(
        row
        for row in mapping
        if row["sigma_x_exploratory"] == 0.002 and row["g"] == 0.3
    )
    assert 127.0 < nominal["xi_nm_required"] < 128.0
    assert 1.38 < nominal["decision_resolution_meV"] < 1.39
    assert record["activation_gates"]["source_supported_hgcdte_parameter_regime"] is False
    assert "No new HgCdTe physical law" in record["claim_boundary"]