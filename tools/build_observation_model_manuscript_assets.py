#!/usr/bin/env python3
"""Build deterministic tables and SVG figures for the observation-model manuscript."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.analyze_moazzami2005_manuscript_comparators import analyze as compare_models
from tools.analyze_moazzami2005_real_spectra import analyze as analyze_real_spectra
from tools.audit_moazzami2005_digitization_sensitivity import audit as audit_digitization
from tools.observation_manuscript_figure_comparison import (
    build_edge_svg,
    build_residual_svg,
)
from tools.observation_manuscript_figure_spectrum import build_spectrum_svg
from tools.observation_manuscript_tables import build_tables


def build(root: str | Path, output_dir: str | Path) -> dict[str, Any]:
    root, output = Path(root), Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    base = analyze_real_spectra(root)
    comparison = compare_models(root)
    sensitivity = audit_digitization(root)
    generated = build_tables(output, base, comparison, sensitivity)
    figures = {
        "figure1_spectrum_models.svg": build_spectrum_svg(root, base),
        "figure2_edge_candidates.svg": build_edge_svg(comparison),
        "figure3_material_residual_envelopes.svg": build_residual_svg(
            base, comparison
        ),
    }
    for name, text in figures.items():
        (output / name).write_text(text, encoding="utf-8")
    generated.extend(sorted(figures))
    summary = {
        "schema_version": "1.0",
        "analysis": comparison["analysis"],
        "decision": comparison["decision"],
        "digitization_decision": sensitivity["decision"],
        "generated_files": sorted(generated),
        "claim_boundary": comparison["claim_boundary"],
    }
    (output / "manuscript_asset_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = build(args.repository_root, args.output_dir)
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
