#!/usr/bin/env python3
"""Inspect and hash local UPF2 or ABINIT psp8 pseudopotential files.

The tool performs structural header checks only. Passing inspection is necessary for
A0 input rendering but is not evidence of pseudopotential transferability or numerical
convergence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


def _digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _as_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"t", "true", ".true.", "1", "yes"}:
        return True
    if normalized in {"f", "false", ".false.", "0", "no"}:
        return False
    raise ValueError(f"cannot interpret Boolean value {value!r}")


def inspect_upf(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    header = root.find("PP_HEADER")
    if header is None:
        raise ValueError("UPF file has no PP_HEADER")
    version = root.attrib.get("version")
    return {
        "format": "upf",
        "upf_version": version,
        "element": header.attrib.get("element"),
        "functional": header.attrib.get("functional"),
        "pseudo_type": header.attrib.get("pseudo_type"),
        "relativistic": header.attrib.get("relativistic"),
        "fully_relativistic": header.attrib.get("relativistic", "").lower() == "full",
        "spin_orbit": _as_bool(header.attrib.get("has_so")),
        "nonlinear_core_correction": _as_bool(header.attrib.get("core_correction")),
        "z_valence": float(header.attrib["z_valence"]),
        "l_max": int(header.attrib["l_max"]),
        "number_of_wfc": int(header.attrib["number_of_wfc"]),
        "number_of_proj": int(header.attrib["number_of_proj"]),
        "generator": header.attrib.get("generated"),
    }


def _numeric_prefix(line: str) -> list[str]:
    values: list[str] = []
    for token in line.split():
        try:
            float(token.replace("D", "E").replace("d", "e"))
        except ValueError:
            break
        values.append(token)
    return values


def inspect_psp8(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 9:
        raise ValueError("psp8 file is too short")
    first = lines[0].split()
    atom = _numeric_prefix(lines[1])
    control = _numeric_prefix(lines[2])
    if len(first) < 1 or len(atom) < 2 or len(control) < 4:
        raise ValueError("psp8 header is malformed")

    extension: list[str] | None = None
    nprojso: list[str] | None = None
    for line in lines[:20]:
        if "extension_switch" in line:
            extension = _numeric_prefix(line)
        if "nprojso" in line:
            nprojso = _numeric_prefix(line)
    if extension is None or nprojso is None:
        raise ValueError("psp8 relativistic extension metadata is missing")

    pspcod = int(float(control[0]))
    extension_switch = int(float(extension[-1]))
    spin_orbit_projectors = [int(float(value)) for value in nprojso]
    return {
        "format": "psp8",
        "element": first[0],
        "generator": " ".join(first[1:]),
        "z_atom": float(atom[0]),
        "z_valence": float(atom[1]),
        "pspcod": pspcod,
        "pspxc": int(float(control[1])),
        "l_max": int(float(control[2])),
        "l_local": int(float(control[3])),
        "extension_switch": extension_switch,
        "spin_orbit_projectors": spin_orbit_projectors,
        "fully_relativistic": pspcod == 8 and extension_switch == 1,
        "spin_orbit": sum(spin_orbit_projectors) > 0,
    }


def inspect(path: str | Path, file_format: str) -> dict[str, Any]:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    metadata = inspect_upf(source) if file_format == "upf" else inspect_psp8(source)
    metadata.update(
        {
            "path": str(source),
            "size_bytes": source.stat().st_size,
            "sha256": _digest(source, "sha256"),
            "md5": _digest(source, "md5"),
        }
    )
    return metadata


def validate(
    metadata: dict[str, Any],
    *,
    expected_element: str | None,
    expected_z_valence: float | None,
    expected_functional: str | None,
    expected_pspxc: int | None,
    require_fully_relativistic: bool,
    require_spin_orbit: bool,
    require_nlcc: bool,
) -> None:
    failures: list[str] = []
    if expected_element is not None and metadata.get("element") != expected_element:
        failures.append(f"element={metadata.get('element')!r}, expected {expected_element!r}")
    if expected_z_valence is not None and abs(metadata["z_valence"] - expected_z_valence) > 1e-8:
        failures.append(
            f"z_valence={metadata['z_valence']}, expected {expected_z_valence}"
        )
    if expected_functional is not None and metadata.get("functional") != expected_functional:
        failures.append(
            f"functional={metadata.get('functional')!r}, expected {expected_functional!r}"
        )
    if expected_pspxc is not None and metadata.get("pspxc") != expected_pspxc:
        failures.append(f"pspxc={metadata.get('pspxc')!r}, expected {expected_pspxc}")
    if require_fully_relativistic and not metadata.get("fully_relativistic"):
        failures.append("file is not identified as fully relativistic")
    if require_spin_orbit and not metadata.get("spin_orbit"):
        failures.append("file does not contain spin-orbit metadata/projectors")
    if require_nlcc and metadata.get("nonlinear_core_correction") is not True:
        failures.append("UPF nonlinear core correction is not enabled")
    if failures:
        raise ValueError("pseudopotential validation failed: " + "; ".join(failures))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--format", choices=("upf", "psp8"), required=True)
    parser.add_argument("--output-json")
    parser.add_argument("--expect-element")
    parser.add_argument("--expect-z-valence", type=float)
    parser.add_argument("--expect-functional")
    parser.add_argument("--expect-pspxc", type=int)
    parser.add_argument("--require-fully-relativistic", action="store_true")
    parser.add_argument("--require-spin-orbit", action="store_true")
    parser.add_argument("--require-nlcc", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    metadata = inspect(args.path, args.format)
    validate(
        metadata,
        expected_element=args.expect_element,
        expected_z_valence=args.expect_z_valence,
        expected_functional=args.expect_functional,
        expected_pspxc=args.expect_pspxc,
        require_fully_relativistic=args.require_fully_relativistic,
        require_spin_orbit=args.require_spin_orbit,
        require_nlcc=args.require_nlcc,
    )
    text = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        Path(args.output_json).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
