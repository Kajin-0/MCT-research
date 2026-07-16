#!/usr/bin/env python3
"""Build an auditable cubic CdTe volume-sensitivity grid from the A0 run spec."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _load_object(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def lattice_scale_from_volume_fraction(volume_fraction: float) -> float:
    """Return a/a_ref for a cubic cell with V/V_ref = 1 + volume_fraction."""
    if not isinstance(volume_fraction, (int, float)) or not math.isfinite(
        volume_fraction
    ):
        raise ValueError("volume_fraction must be finite")
    if volume_fraction <= -1.0:
        raise ValueError("volume_fraction must keep the cell volume positive")
    return (1.0 + float(volume_fraction)) ** (1.0 / 3.0)


def build_volume_grid(
    reference_lattice_angstrom: float,
    volume_fractional_offsets: list[float],
) -> list[dict[str, float]]:
    """Create volume and lattice points without confusing delta-V/V with delta-a/a."""
    if (
        not isinstance(reference_lattice_angstrom, (int, float))
        or not math.isfinite(reference_lattice_angstrom)
        or reference_lattice_angstrom <= 0
    ):
        raise ValueError("reference_lattice_angstrom must be positive and finite")
    if not isinstance(volume_fractional_offsets, list) or not volume_fractional_offsets:
        raise ValueError("volume_fractional_offsets must be a non-empty list")

    offsets = [float(value) for value in volume_fractional_offsets]
    if offsets != sorted(offsets):
        raise ValueError("volume_fractional_offsets must be sorted")
    if 0.0 not in offsets:
        raise ValueError("volume_fractional_offsets must include zero")
    if any(not math.isfinite(value) or value <= -1.0 for value in offsets):
        raise ValueError("every volume offset must be finite and greater than -1")

    negative = sorted(-value for value in offsets if value < 0)
    positive = sorted(value for value in offsets if value > 0)
    if len(negative) != len(positive) or any(
        not math.isclose(left, right, rel_tol=0.0, abs_tol=1e-15)
        for left, right in zip(negative, positive)
    ):
        raise ValueError("volume_fractional_offsets must be symmetric about zero")

    points: list[dict[str, float]] = []
    for volume_fraction in offsets:
        lattice_scale = lattice_scale_from_volume_fraction(volume_fraction)
        points.append(
            {
                "volume_fraction": volume_fraction,
                "volume_ratio": 1.0 + volume_fraction,
                "lattice_scale": lattice_scale,
                "lattice_fraction": lattice_scale - 1.0,
                "lattice_constant_angstrom": (
                    float(reference_lattice_angstrom) * lattice_scale
                ),
            }
        )
    return points


def grid_from_specification(
    specification: dict[str, Any],
    *,
    allow_planning_candidate: bool = False,
) -> dict[str, Any]:
    structure = specification.get("structure", {})
    if not isinstance(structure, dict):
        raise ValueError("structure must be an object")
    protocol = structure.get("fixed_volume_protocol", {})
    if not isinstance(protocol, dict):
        raise ValueError("structure.fixed_volume_protocol must be an object")

    execution_lattice = structure.get("execution_lattice_constant_angstrom")
    source = structure.get("execution_lattice_constant_source", {})
    source_is_primary = (
        isinstance(source, dict)
        and source.get("source_type") == "primary_experimental"
        and isinstance(source.get("source_sha256"), str)
        and len(source["source_sha256"]) == 64
    )

    if isinstance(execution_lattice, (int, float)) and execution_lattice > 0:
        if not source_is_primary:
            raise ValueError(
                "execution lattice requires a primary experimental source SHA-256"
            )
        reference_lattice = float(execution_lattice)
        reference_status = "execution_reference"
        execution_authorized = True
    elif allow_planning_candidate:
        candidate = structure.get("candidate_reference_lattice_constant_angstrom")
        if not isinstance(candidate, (int, float)) or candidate <= 0:
            raise ValueError("no positive planning candidate is available")
        reference_lattice = float(candidate)
        reference_status = "planning_candidate_only"
        execution_authorized = False
    else:
        raise ValueError(
            "execution lattice is unresolved; pass --allow-planning-candidate only "
            "to generate a non-executable planning grid"
        )

    offsets = protocol.get("volume_fractional_offsets")
    points = build_volume_grid(reference_lattice, offsets)
    return {
        "schema_version": "1.0",
        "stage": specification.get("stage"),
        "reference_status": reference_status,
        "execution_authorized": execution_authorized,
        "reference_lattice_constant_angstrom": reference_lattice,
        "reference_volume_temperature_k": protocol.get("reference_temperature_k"),
        "relationship": "a/a_ref = (V/V_ref)^(1/3)",
        "points": points,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-spec-json",
        default="first_principles/a0/cdte_a0_run_spec.json",
    )
    parser.add_argument("--output-json")
    parser.add_argument(
        "--allow-planning-candidate",
        action="store_true",
        help="permit a visibly non-executable grid from the candidate lattice value",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = grid_from_specification(
        _load_object(args.run_spec_json),
        allow_planning_candidate=args.allow_planning_candidate,
    )
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if args.output_json:
        path = Path(args.output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
