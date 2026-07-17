#!/usr/bin/env python3
"""Extract ordered k-point eigenvalues from QE data-file-schema.xml."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

HARTREE_TO_EV = 27.211386245988


def _tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _child(parent: ET.Element, name: str) -> ET.Element:
    for child in parent:
        if _tag(child) == name:
            return child
    raise ValueError(f"missing {name} in {_tag(parent)}")


def _numbers(element: ET.Element) -> list[float]:
    values = [float(token) for token in " ".join(element.itertext()).split()]
    if not values:
        raise ValueError(f"empty {_tag(element)}")
    return values


def extract(path: str | Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    blocks: list[dict[str, object]] = []
    for element in root.iter():
        if _tag(element) != "ks_energies":
            continue
        k_point = _child(element, "k_point")
        eigenvalues = _child(element, "eigenvalues")
        occupations = _child(element, "occupations")
        k = _numbers(k_point)
        eig_ha = _numbers(eigenvalues)
        occ = _numbers(occupations)
        if len(k) != 3:
            raise ValueError("every k_point must have three coordinates")
        if len(eig_ha) != len(occ):
            raise ValueError("eigenvalue and occupation counts differ")
        blocks.append(
            {
                "index": len(blocks) + 1,
                "k_point_crystal": k,
                "weight": float(k_point.attrib.get("weight", "nan")),
                "eigenvalues_hartree": eig_ha,
                "eigenvalues_ev": [value * HARTREE_TO_EV for value in eig_ha],
                "occupations": occ,
            }
        )
    if not blocks:
        raise ValueError("no ks_energies blocks found")
    band_counts = {len(block["eigenvalues_hartree"]) for block in blocks}
    if len(band_counts) != 1:
        raise ValueError("inconsistent band count across k points")
    return {
        "status": "raw_qe_eigenvalues_not_band_assignment",
        "source_file": str(path),
        "source_units": "hartree",
        "hartree_to_ev": HARTREE_TO_EV,
        "num_kpoints": len(blocks),
        "num_bands": band_counts.pop(),
        "blocks": blocks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema_xml")
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = extract(args.schema_xml)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output_json:
        Path(args.output_json).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
