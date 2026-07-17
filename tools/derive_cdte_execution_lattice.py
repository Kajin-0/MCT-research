#!/usr/bin/env python3
"""Derive a conservative CdTe 0 K reference lattice for A0 sensitivity work.

The central curve uses primary Williams, Smith-White, and Browder data. The
microcrystalline-to-single-crystal transfer is not assumed exact: the largest
observed Browder-minus-Smith alpha discrepancy is applied over the entire
unresolved interval as a conservative absolute morphology bound.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from tools.analyze_cdte_browder_bridge import analyze as analyze_browder


ROOT = Path(__file__).resolve().parents[1]
RUN_SPEC = ROOT / "first_principles" / "a0" / "cdte_a0_run_spec.json"
BAGOT_RESULT = (
    ROOT / "first_principles" / "a0" / "cdte_bagot_bridge_reference_result.json"
)


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def derive(acquisition_result: dict[str, Any]) -> dict[str, Any]:
    if acquisition_result.get("success") is not True:
        raise ValueError("official Browder publisher-table acquisition did not pass")
    table_validation = acquisition_result.get("table_validation", {})
    if not isinstance(table_validation, dict) or table_validation.get("exact_match") is not True:
        raise ValueError("committed Browder table was not validated against the publisher")

    run_spec = load_object(RUN_SPEC)
    bagot = load_object(BAGOT_RESULT)
    browder = analyze_browder()

    source_record = run_spec["structure"]["execution_lattice_constant_source"]
    anchor = source_record["absolute_anchor_candidate"]
    sensitivity = browder["zero_k_sensitivity"]
    overlap = browder["overlap_with_smith_white_single_crystal"]

    central = float(sensitivity["endpoint_adjusted_browder_shape_a0_a"])
    anchor_temperature = float(anchor["anchor_temperature_k"])
    splice_temperature = 85.0
    unresolved_interval = anchor_temperature - splice_temperature
    maximum_alpha_difference = float(
        overlap["maximum_absolute_difference_1e6_per_k"]
    ) * 1.0e-6
    morphology_integral_bound = maximum_alpha_difference * unresolved_interval
    morphology_lattice_bound = central * (math.exp(morphology_integral_bound) - 1.0)
    anchor_bound = float(anchor["conservative_anchor_bound_angstrom"])
    rounding_bound = float(sensitivity["table_rounding_only_a_bound"])
    total_bound = anchor_bound + morphology_lattice_bound + rounding_bound

    lower = central - total_bound
    upper = central + total_bound
    lower_volume_fraction = (lower / central) ** 3 - 1.0
    upper_volume_fraction = (upper / central) ** 3 - 1.0
    maximum_volume_fraction = max(
        abs(lower_volume_fraction), abs(upper_volume_fraction)
    )
    intended_volume_offset = max(
        abs(float(value))
        for value in run_spec["structure"]["fixed_volume_protocol"][
            "volume_fractional_offsets"
        ]
    )
    fraction_of_volume_offset = maximum_volume_fraction / intended_volume_offset
    declared_limit_fraction = 0.20

    comparison_values = {
        "bagot_bogucki_secondary_fit": float(
            bagot["zero_temperature_diagnostic"]["bagot_fit_a0_angstrom"]
        ),
        "previous_endpoint_linear_bridge": float(
            sensitivity["linear_bridge_previous_a0_a"]
        ),
        "smith_below_10_then_browder": float(
            sensitivity["smith_below_10_then_browder_a0_a"]
        ),
        "smith_through_85_then_raw_browder": float(
            sensitivity["smith_through_85_then_browder_a0_a"]
        ),
    }
    comparison_offsets = {
        name: value - central for name, value in comparison_values.items()
    }
    comparison_containment = {
        name: abs(offset) <= total_bound
        for name, offset in comparison_offsets.items()
    }

    decision_passed = (
        all(comparison_containment.values())
        and maximum_volume_fraction <= declared_limit_fraction * intended_volume_offset
        and morphology_lattice_bound > abs(
            comparison_offsets["bagot_bogucki_secondary_fit"]
        )
        and table_validation.get("maximum_temperature_difference_k") == 0.0
        and table_validation.get("maximum_alpha_difference_1e6_per_k") == 0.0
    )
    if not decision_passed:
        raise RuntimeError("bounded CdTe lattice decision did not pass declared gates")

    return {
        "schema_version": "1.0",
        "status": "authorized_for_fixed_volume_a0_sensitivity_not_metrology_reference",
        "source_chain": {
            "absolute_anchor": {
                "citation": anchor["citation"],
                "doi": anchor["doi"],
                "source_sha256": anchor["source_sha256"],
                "measurement_temperature_k": anchor_temperature,
                "lattice_constant_angstrom": float(
                    anchor["polynomial_anchor_lattice_constant_angstrom"]
                ),
                "conservative_absolute_bound_angstrom": anchor_bound,
            },
            "low_temperature_expansion": {
                "citation": source_record["transformation_to_reference"][
                    "thermal_expansion_citation"
                ],
                "doi": source_record["transformation_to_reference"][
                    "thermal_expansion_doi"
                ],
                "source_sha256": source_record["transformation_to_reference"][
                    "thermal_expansion_source_sha256"
                ],
                "direct_data_used_through_k": splice_temperature,
            },
            "bridge_shape": {
                "citation": acquisition_result["citation"],
                "source_url": acquisition_result["source_url"],
                "publisher_html_sha256": acquisition_result["source_sha256"],
                "canonical_table_sha256": table_validation[
                    "publisher_rows_sha256"
                ],
                "publisher_table_exactly_matches_committed_csv": True,
                "material_form": "microcrystalline hot-pressed CdTe Irtran 6",
                "temperature_range_k": [10.0, 300.0],
                "bridge_interval_used_k": [splice_temperature, anchor_temperature],
                "endpoint_adjustment": (
                    "linearly adjust Browder alpha to Smith-White at 85 K and "
                    "Williams alpha at 293.15 K"
                ),
            },
        },
        "reference_lattice": {
            "reference_temperature_k": 0.0,
            "central_angstrom": central,
            "lower_conservative_bound_angstrom": lower,
            "upper_conservative_bound_angstrom": upper,
            "conservative_absolute_bound_angstrom": total_bound,
            "uncertainty_type": "conservative_absolute_bound_not_standard_uncertainty",
        },
        "uncertainty_components": {
            "williams_anchor_bound_angstrom": anchor_bound,
            "morphology_transfer": {
                "rule": (
                    "apply the largest absolute Browder-minus-Smith alpha difference "
                    "as a constant signed error over the entire unresolved interval"
                ),
                "largest_overlap_alpha_difference_1e6_per_k": (
                    maximum_alpha_difference * 1.0e6
                ),
                "interval_k": [splice_temperature, anchor_temperature],
                "interval_width_k": unresolved_interval,
                "integral_bound": morphology_integral_bound,
                "lattice_bound_angstrom": morphology_lattice_bound,
            },
            "publisher_table_rounding_bound_angstrom": rounding_bound,
            "combination_rule": "linear sum of absolute component bounds",
            "total_bound_angstrom": total_bound,
        },
        "cross_checks": {
            "comparison_lattices_angstrom": comparison_values,
            "offsets_from_central_angstrom": comparison_offsets,
            "contained_by_total_bound": comparison_containment,
            "all_contained": all(comparison_containment.values()),
        },
        "volume_sensitivity_gate": {
            "lower_volume_fraction": lower_volume_fraction,
            "upper_volume_fraction": upper_volume_fraction,
            "maximum_absolute_volume_fraction": maximum_volume_fraction,
            "intended_one_sided_a0_volume_offset": intended_volume_offset,
            "fraction_of_intended_offset": fraction_of_volume_offset,
            "declared_maximum_fraction_of_offset": declared_limit_fraction,
            "passed": maximum_volume_fraction
            <= declared_limit_fraction * intended_volume_offset,
        },
        "decision": {
            "physical_volume_provenance_gate_passed_for_a0_sensitivity": True,
            "execution_lattice_constant_angstrom": central,
            "execution_lattice_conservative_bound_angstrom": total_bound,
            "metrology_grade_zero_k_lattice_claim": False,
            "quasiharmonic_path_authorized": False,
            "new_electronic_structure_run_authorized_by_this_manifest": False,
            "remaining_a0_blockers": [
                "installed runtime binary hashes and version outputs",
                "release-specific rendered-input syntax validation",
                "runtime pseudopotential-copy hash verification",
                "rendered QE and ABINIT input manifests",
            ],
        },
        "claim_boundary": (
            "This value is an uncertainty-bounded fixed-volume reference for the declared "
            "A0 sensitivity bracket. It is not a universal or metrology-grade 0 K CdTe "
            "lattice constant and does not validate morphology independence."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquisition-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    result = derive(load_object(args.acquisition_json))
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
