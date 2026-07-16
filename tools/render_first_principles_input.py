#!/usr/bin/env python3
"""Render a parameterized first-principles input and write a hash manifest.

Placeholders use the exact form ``@UPPER_CASE_NAME@``. Rendering fails on missing
placeholders, unused parameters, duplicate external-input labels, or absent files.
The tool does not execute or syntax-check any electronic-structure code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

_PLACEHOLDER = re.compile(r"@([A-Z][A-Z0-9_]*)@")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _load_parameters(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("parameter JSON must contain one object")
    for key, item in value.items():
        if not _PLACEHOLDER.fullmatch(f"@{key}@"):
            raise ValueError(f"invalid parameter name {key!r}")
        if isinstance(item, (dict, list)) or item is None:
            raise ValueError(f"parameter {key!r} must be a non-null scalar")
    return value


def render_text(template: str, parameters: dict[str, Any]) -> str:
    required = set(_PLACEHOLDER.findall(template))
    supplied = set(parameters)
    missing = sorted(required - supplied)
    unused = sorted(supplied - required)
    if missing:
        raise ValueError("missing template parameters: " + ", ".join(missing))
    if unused:
        raise ValueError("unused template parameters: " + ", ".join(unused))

    rendered = _PLACEHOLDER.sub(lambda match: str(parameters[match.group(1)]), template)
    unresolved = sorted(set(_PLACEHOLDER.findall(rendered)))
    if unresolved:
        raise ValueError("unresolved placeholders: " + ", ".join(unresolved))
    return rendered


def _external_inputs(values: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for value in values:
        try:
            label, raw_path = value.split("=", 1)
        except ValueError as error:
            raise ValueError("--input-file values must have LABEL=PATH form") from error
        if not label or label in result:
            raise ValueError(f"invalid or duplicate input label {label!r}")
        path = Path(raw_path)
        if not path.is_file():
            raise FileNotFoundError(path)
        result[label] = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
        }
    return result


def render(
    template_path: str | Path,
    output_path: str | Path,
    parameters_path: str | Path,
    manifest_path: str | Path,
    *,
    input_files: list[str] | None = None,
) -> dict[str, Any]:
    template_file = Path(template_path)
    output_file = Path(output_path)
    parameter_file = Path(parameters_path)
    manifest_file = Path(manifest_path)
    template_bytes = template_file.read_bytes()
    template = template_bytes.decode("utf-8")
    parameters = _load_parameters(parameter_file)
    rendered = render_text(template, parameters)
    rendered_bytes = rendered.encode("utf-8")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(rendered_bytes)

    canonical_parameters = json.dumps(
        parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "renderer": "tools/render_first_principles_input.py",
        "execution_performed": False,
        "syntax_check_performed": False,
        "template": {
            "path": str(template_file),
            "sha256": _sha256_bytes(template_bytes),
        },
        "parameters": {
            "path": str(parameter_file),
            "sha256_canonical_json": _sha256_bytes(canonical_parameters),
            "values": parameters,
        },
        "rendered_input": {
            "path": str(output_file),
            "size_bytes": len(rendered_bytes),
            "sha256": _sha256_bytes(rendered_bytes),
        },
        "external_inputs": _external_inputs(input_files or []),
    }
    manifest_file.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template")
    parser.add_argument("output")
    parser.add_argument("--parameters-json", required=True)
    parser.add_argument("--manifest-json", required=True)
    parser.add_argument(
        "--input-file",
        action="append",
        default=[],
        metavar="LABEL=PATH",
        help="external file to hash into the manifest; may be repeated",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = render(
        args.template,
        args.output,
        args.parameters_json,
        args.manifest_json,
        input_files=args.input_file,
    )
    print(f"rendered_sha256={manifest['rendered_input']['sha256']}")
    print(f"manifest={args.manifest_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
