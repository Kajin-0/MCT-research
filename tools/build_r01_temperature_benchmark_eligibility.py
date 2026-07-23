from __future__ import annotations

import argparse
import json
from pathlib import Path

from mct_research.r01_temperature_benchmark_eligibility import build_reference

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data/validation/r01_temperature_benchmark_eligibility.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the deterministic R01 temperature-benchmark eligibility record."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = build_reference(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
