from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tools.run_polar_vertex_decomposition_oracle import (
    dielectric_tensor,
    evaluate,
    long_range_vertex,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/matrix_oracle/polar_vertex_decomposition_contract.json"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_oracle_closes_vertex_and_fan_with_cross_term() -> None:
    result = evaluate(_contract())
    metrics = result["metrics"]
    decision = result["decision"]

    assert all(result["checks"].values())
    assert metrics["short_range_training_relative_error"] < 1e-12
    assert metrics["maximum_target_vertex_holdout_relative_error"] < 1e-12
    assert metrics["maximum_fan_decomposition_closure_relative_error"] < 1e-12
    assert metrics["minimum_naive_addition_relative_error"] > 0.4
    assert metrics["minimum_missing_cross_term_relative_error"] > 0.3
    assert metrics["minimum_source_target_long_range_difference"] > 0.3

    assert decision["fan_vertex_subtract_restore_architecture_ready"] is True
    assert decision["restore_at_vertex_level_before_self_energy"] is True
    assert decision["direct_self_energy_component_replacement_forbidden"] is True
    assert decision["short_range_long_range_cross_term_required"] is True
    assert decision["debye_waller_path_ready"] is False
    assert decision["real_A1_authorized"] is False
    assert decision["automatic_additional_compute_authorized"] is False


def test_naive_addition_fails_every_holdout() -> None:
    result = evaluate(_contract())
    for record in result["holdout_records"]:
        assert record["target_vertex_relative_error"] < 1e-12
        assert record["naive_addition_relative_error"] > 0.4
        assert record["missing_cross_term_relative_error"] > 0.3


def test_long_range_vertex_rejects_zero_q() -> None:
    epsilon = np.eye(3)
    template = np.eye(8, dtype=np.complex128)
    with pytest.raises(ValueError, match="nonzero"):
        long_range_vertex(np.zeros(3), 1.0, epsilon, template)


def test_dielectric_tensor_must_be_positive_definite() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        dielectric_tensor([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]], "bad")
