#!/usr/bin/env python3
"""Audit Blue 1964 signed-gap commensurability without fitting a model."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


SOURCE_COUNTEREXAMPLE = {
    "temperature_k": 50.0,
    "actual_edge_gap_ev": 0.0,
    "band_curvature_scale_ev": 0.03,
    "source_status": "hypothetical_example_explicitly_stated_by_Blue_1964",
}
HIGH_ENERGY_NEAR_DEGENERACY_EV = (0.02, 0.03, 0.04)


def _read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def audit(observations_path: str | Path) -> dict[str, Any]:
    rows = _read_rows(observations_path)
    if len(rows) != 7:
        raise ValueError("expected exactly seven Blue 1964 observations")

    parameters = [float(row["optical_gap_parameter_ev"]) for row in rows]
    if not all(value > 0.0 for value in parameters):
        raise ValueError("Blue optical-fit parameters must remain positive as printed")
    if {row["signed_gap_eligible"] for row in rows} != {"false"}:
        raise ValueError("all Blue rows must remain ineligible for signed-gap ranking")
    if {row["observable_sign_semantics"] for row in rows} != {
        "positive_parameter_not_signed_Gamma6_minus_Gamma8"
    }:
        raise ValueError("unexpected Blue observable sign semantics")
    if {row["fit_region_alpha_cm_inverse"] for row in rows} != {
        "approximately_above_1e3"
    }:
        raise ValueError("unexpected Blue high-absorption fit region")

    return {
        "schema_version": "1.0",
        "analysis": "Blue 1964 signed-gap non-commensurability certificate",
        "source_id": "BLUE1964",
        "observation_contract": {
            "row_count": len(rows),
            "measurement_class": (
                "theory_conditioned_positive_optical_gap_parameter"
            ),
            "parameter_min_ev": min(parameters),
            "parameter_max_ev": max(parameters),
            "all_parameters_positive": True,
            "all_rows_signed_gap_eligible": False,
            "fit_region_alpha_cm_inverse": "approximately_above_1e3",
            "temperature_context": "room_temperature_exact_kelvin_unknown",
        },
        "source_counterexample": SOURCE_COUNTEREXAMPLE,
        "source_high_energy_near_degeneracy": {
            "trial_curvature_scales_ev": list(HIGH_ENERGY_NEAR_DEGENERACY_EV),
            "source_statement": (
                "theoretical_curves_give_essentially_the_same_results_at_"
                "higher_photon_energies"
            ),
            "physical_reason_as_stated": (
                "density_of_states_contributions_are_similar"
            ),
            "magnitude_identifiability_status": (
                "weak_non_unique_in_the_declared_high_absorption_comparison"
            ),
        },
        "identifiability_decision": {
            "source_parameterization_represents_signed_band_order": False,
            "blue_parameter_equals_actual_edge_gap": False,
            "sign_of_modern_Gamma6_minus_Gamma8_identified": False,
            "one_to_one_gap_magnitude_identified": False,
            "direct_signed_gap_residual_ranking_authorized": False,
            "external_validated_observation_operator_required": True,
            "universal_numerical_correction_identified": False,
        },
        "analysis_bookkeeping": {
            "fitted_parameter_count": 0,
            "correction_coefficient_count": 0,
            "signed_model_evaluations": 0,
            "source_rows_modified": 0,
        },
        "scientific_decision": {
            "blue_table_directly_commensurate_with_signed_gap_laws": False,
            "blue_table_retained_for_observation_model_studies": True,
            "production_equation_authorized": False,
            "manuscript_authorized": False,
        },
        "claim_boundary": [
            (
                "Blue explicitly permits zero actual edge gap with a positive "
                "0.03 eV band-curvature scale."
            ),
            (
                "Blue reports that 0.02, 0.03 and 0.04 eV theoretical gap "
                "choices give essentially the same higher-energy absorption."
            ),
            (
                "The seven tabulated values were selected in the same high-"
                "absorption regime where this weak sensitivity is stated."
            ),
            (
                "The positive Blue parameter therefore does not identify the "
                "sign or a unique magnitude of a modern signed gap."
            ),
            (
                "No signed residual, model ranking or numerical correction is "
                "computed by this audit."
            ),
        ],
    }


def quantize(value: Any, digits: int = 9) -> Any:
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return value
    if isinstance(value, float):
        return round(value, digits)
    if isinstance(value, list):
        return [quantize(item, digits) for item in value]
    if isinstance(value, dict):
        return {key: quantize(item, digits) for key, item in value.items()}
    raise TypeError(f"unsupported serialization type: {type(value)!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--observations-csv",
        default="data/experimental/blue1964_table2_optical_gaps.csv",
    )
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = quantize(audit(args.observations_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
