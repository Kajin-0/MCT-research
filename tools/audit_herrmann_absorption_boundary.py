#!/usr/bin/env python3
"""Audit the recoverable and blocked portions of the Herrmann 1993 model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_PRIMITIVES = {
    "urbach_tail_segment",
    "urbach_width_temperature_law",
    "equilibrium_band_filling_limit",
}
EXPECTED_BLOCKED = {
    "complete Kane-region absorption expression",
    "complete non-equilibrium band-filling implementation",
    "Urbach-to-Kane transition matching",
    "full Herrmann edge fit on repository spectra",
}


def audit(path: str | Path) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported Herrmann boundary schema")

    source = data["source"]
    if source["doi"] != "10.1063/1.352954":
        raise ValueError("Herrmann 1993 DOI changed")
    if source["full_text_recovered"] is not True:
        raise ValueError("Herrmann 1993 full text must be recovered")
    if source["copyrighted_source_committed"] is not False:
        raise ValueError("copyrighted source content must not be committed")
    if len(source["input_asset_sha256"]) != 64:
        raise ValueError("Herrmann source asset lacks a SHA-256 binding")

    primitives = {row["name"] for row in data["exactly_recoverable_primitives"]}
    if primitives != EXPECTED_PRIMITIVES:
        raise ValueError("recoverable Herrmann primitive inventory changed")
    blocked = {row["component"] for row in data["blocked_components"]}
    if blocked != EXPECTED_BLOCKED:
        raise ValueError("blocked Herrmann component inventory changed")

    precursor = data["precursor_source"]
    if precursor["doi"] != "10.1016/0022-0248(92)90851-9":
        raise ValueError("Herrmann precursor DOI changed")
    if precursor["full_text_recovered"] is not False:
        raise ValueError("full operator cannot be unblocked without precursor review")

    decision = data["decision"]
    if decision["explicit_primitive_implementation_authorized"] is not True:
        raise ValueError("explicit Herrmann primitives must remain authorized")
    blocked_decisions = (
        "full_herrmann_operator_authorized",
        "apply_full_herrmann_fit_to_existing_spectra_authorized",
        "update_existing_edge_uncertainty_envelope_authorized",
        "fit_new_material_gap_coefficients_authorized",
    )
    if any(decision[key] is not False for key in blocked_decisions):
        raise ValueError("Herrmann evidence boundary was improperly widened")

    return {
        "schema_version": data["schema_version"],
        "analysis": data["analysis"],
        "recoverable_primitive_count": len(primitives),
        "blocked_component_count": len(blocked),
        "source_asset_bound": True,
        "precursor_full_text_recovered": False,
        "full_operator_authorized": False,
        "existing_edge_envelope_update_authorized": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boundary-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.boundary_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
