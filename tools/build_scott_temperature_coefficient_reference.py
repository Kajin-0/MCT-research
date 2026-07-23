from __future__ import annotations

import argparse
import json
from pathlib import Path

from mct_research.scott_temperature_coefficients import (
    build_reference,
    load_scott_points,
    quantize_for_json,
    source_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/experimental/scott1969_figure2_digitized.csv"
DEFAULT_OUTPUT = (
    ROOT / "data/validation/scott1969_temperature_coefficient_test.json"
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build the deterministic Scott 1969 fixed-alpha temperature-"
            "coefficient reference."
        )
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    points = load_scott_points(args.source)
    reference = build_reference(
        points,
        source_csv_sha256=source_sha256(args.source),
    )
    quantized = quantize_for_json(reference)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(quantized, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
