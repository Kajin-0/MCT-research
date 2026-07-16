from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = (
    ROOT
    / "first_principles"
    / "decision_memos"
    / "cdte_fixed_volume_thermal_moment_pilot.json"
)


def _decision() -> dict[str, object]:
    with DECISION_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_cdte_memo_authorizes_smoke_test_only() -> None:
    decision = _decision()
    assert decision["decision"] == "authorize_A0_and_one_timed_A1_smoke_test_only"
    assert decision["target_material"] == "CdTe"
    assert decision["production_ahc_authorized"] is False
    assert decision["dense_epw_authorized"] is False
    assert decision["hgte_authorized"] is False


def test_cdte_memo_preserves_accuracy_and_grid_gates() -> None:
    decision = _decision()
    targets = decision["accuracy_targets"]
    assert isinstance(targets, dict)
    assert targets["gap_shift_mev"] <= 1.5
    assert targets["leading_slope_mev_per_k"] <= 0.01
    assert decision["q_grid_ladder"] == [4, 6, 8]
    assert decision["temperature_grid_k"] == [0, 20, 50, 100, 200, 300]


def test_cdte_memo_requires_mode_resolved_information_and_stops() -> None:
    decision = _decision()
    exports = set(decision["required_exports"])
    stops = set(decision["hard_stops"])
    assert "mode_or_frequency_binned_gap_coupling_weights" in exports
    assert "Fan_edge_shifts" in exports
    assert "Debye_Waller_edge_shifts" in exports
    assert "no_mode_or_frequency_resolved_export" in stops
    assert "result_only_duplicates_total_experimental_gap_curve" in stops
