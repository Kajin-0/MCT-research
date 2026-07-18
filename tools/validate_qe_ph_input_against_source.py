#!/usr/bin/env python3
"""Validate a rendered ph.x namelist against the pinned INPUT_PH.def source."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


_ASSIGNMENT = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=", re.MULTILINE)
_INPUTPH = re.compile(
    r"&INPUTPH\b(.*?)^\s*/\s*$",
    flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
)


def input_keys(rendered_input: str) -> list[str]:
    match = _INPUTPH.search(rendered_input)
    if not match:
        raise ValueError("rendered input does not contain a terminated &INPUTPH namelist")
    keys = sorted(set(name.casefold() for name in _ASSIGNMENT.findall(match.group(1))))
    if not keys:
        raise ValueError("&INPUTPH namelist has no assignments")
    return keys


def source_variables(definition: str) -> set[str]:
    return {
        name.casefold()
        for name in re.findall(r"\bvar\s+([A-Za-z][A-Za-z0-9_]*)\b", definition)
    }


def validate(input_path: Path, definition_path: Path) -> dict[str, Any]:
    keys = input_keys(input_path.read_text(encoding="utf-8"))
    variables = source_variables(definition_path.read_text(encoding="utf-8"))
    missing = sorted(set(keys) - variables)
    result = {
        "schema_version": "1.0",
        "rendered_input": str(input_path),
        "pinned_definition": str(definition_path),
        "input_keys": keys,
        "source_variable_count": len(variables),
        "missing_from_pinned_source": missing,
        "passed": not missing,
    }
    if missing:
        raise ValueError("ph.x variables absent from pinned source: " + ", ".join(missing))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--definition", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.input, args.definition)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
