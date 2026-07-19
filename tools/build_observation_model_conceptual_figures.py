#!/usr/bin/env python3
"""Build deterministic conceptual figures for the HgCdTe manuscript."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.observation_manuscript_figure_acquisition import build_acquisition_svg
from tools.observation_manuscript_figure_identifiability import build_identifiability_svg


FIGURES = {
    "figure4_identifiability.svg": build_identifiability_svg,
    "figure5_paired_acquisition_design.svg": build_acquisition_svg,
}


def build(output_dir: str | Path) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for name, factory in FIGURES.items():
        (output / name).write_text(factory(), encoding="utf-8")
    summary = {
        "schema_version": "1.0",
        "generated_files": sorted(FIGURES),
        "figure4_source": "declared paired observation equation and claim boundary",
        "figure5_source": "validated minimum-gap-identifiability design oracle",
        "new_empirical_model_introduced": False,
        "universal_correction_authorized": False,
    }
    (output / "conceptual_figure_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir), sort_keys=True))


if __name__ == "__main__":
    main()
