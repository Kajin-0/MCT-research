#!/usr/bin/env python3
"""Build the immutable Chang anchored-tail recoverability record."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from mct_research.anchored_tail_validation import chang_reference_traces


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "validation" / "chang_anchored_tail_recoverability.json"


def _quantize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, list):
        return [_quantize(item) for item in value]
    if isinstance(value, tuple):
        return [_quantize(item) for item in value]
    if isinstance(value, dict):
        return {key: _quantize(item) for key, item in value.items()}
    return value


def build_record() -> dict[str, Any]:
    traces = [_quantize(asdict(trace)) for trace in chang_reference_traces()]
    return {
        "schema_version": 1,
        "program": "R03_distributional_band_edge",
        "claim_boundary": {
            "urbach_energy_use": "maps source exponential span into plot pixels only",
            "urbach_energy_not_identified_with_sigma_G": True,
            "six_pixels_is_a_declared_figure_scenario_not_measurement_covariance": True,
            "numeric_gap_anchor_values_and_uncertainty_not_tabulated": True,
            "manual_digitization_authorized": False,
            "manuscript_authorized": False,
        },
        "decision": "terminate_chang_figure_digitization_path",
        "decision_reason": (
            "No declared Chang trace reaches the conservative 18-pixel threshold at "
            "z_upper=0, and the same-specimen numerical gap anchor with uncertainty is "
            "not tabulated."
        ),
        "traces": traces,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    output = _parse_args().output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_record(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
