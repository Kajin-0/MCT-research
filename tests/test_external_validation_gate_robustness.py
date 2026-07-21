from __future__ import annotations

import json
from pathlib import Path

from mct_research.validation_gate_robustness import selection_robustness
from tools.build_external_validation_gate import build_report

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "literature" / "acquisition" / "distributional_band_edge_sources.json"
)


def load_manifest() -> dict[str, object]:
    with MANIFEST.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_chang_selection_is_one_step_but_not_two_route_stress_robust() -> None:
    diagnostics = selection_robustness(load_manifest())
    assert diagnostics.selected_route_id == "chang_thickness_cutoff"
    assert diagnostics.closest_competitor_id == "dingrong_carrier_spectrum"
    assert diagnostics.current_margin == 4
    assert diagnostics.maximum_selected_one_step_drop == 3
    assert diagnostics.margin_after_selected_adverse_step == 1
    assert diagnostics.maximum_competitor_one_step_gain == 2
    assert diagnostics.margin_after_competitor_favorable_step == 2
    assert diagnostics.margin_after_simultaneous_two_route_steps == -1
    assert diagnostics.robust_to_any_single_one_level_change is True
    assert (
        diagnostics.robust_to_simultaneous_adverse_and_favorable_steps
        is False
    )


def test_gate_report_states_robustness_boundary() -> None:
    report, markdown = build_report(ROOT)
    robustness = report["selection_robustness"]
    assert robustness["robust_to_any_single_one_level_change"] is True
    assert (
        robustness[
            "robust_to_simultaneous_adverse_and_favorable_steps"
        ]
        is False
    )
    assert "locally robust to one criterion revision" in markdown
    assert "not to the declared two-route stress test" in markdown
