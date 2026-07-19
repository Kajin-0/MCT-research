#!/usr/bin/env python3
"""Export one explicit absorption-edge model uncertainty envelope."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from mct_research.absorption_edge_uncertainty import analyze_absorption_edge_contract


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_json)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input JSON must contain one object")
    result = analyze_absorption_edge_contract(payload)
    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
