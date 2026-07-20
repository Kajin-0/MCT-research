#!/usr/bin/env python3
"""Fail-closed audit for the Mroczkowski 1983 abstract-level constraint."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

EXPECTED_SOURCE = {
    "title": "Optical absorption edge in Hg0.7Cd0.3Te",
    "authors": [
        "J. A. Mroczkowski",
        "D. A. Nelson",
        "R. Murosako",
        "P. H. Zimmermann",
    ],
    "journal": "Journal of Vacuum Science & Technology A",
    "volume": 1,
    "issue": 3,
    "pages": "1756-1760",
    "year": 1983,
    "doi": "10.1116/1.572210",
    "publisher_record_fingerprint_sha256": (
        "3bff3953d0395730cd6d07f6444ffd90e009bdfec7ba633365c56fe796b440d3"
    ),
}
EXPECTED_DECISION = {
    "complete_absorption_operator_implementation_authorized": False,
    "full_text_recovery_priority": "high",
    "latent_material_gap_point_authorized": False,
    "paired_protocol_vacancy_covariate_priority_strengthened": True,
    "uncertainty_weighted_fitting_authorized": False,
    "universal_vacancy_correction_authorized": False,
    "vacancy_conditioned_tail_mechanism_evidence_authorized": True,
    "within_specimen_paired_contrast_established": False,
}
EXPECTED_REOPENING_REQUIREMENTS = {
    "primary full text",
    "specimen inventory and lineage",
    "measurement temperature for each endpoint",
    "acceptor-density assignment for each specimen or state",
    "growth and stoichiometric-processing history",
    "composition measurement method and uncertainty",
    "spectral fit windows and slope uncertainties",
    "comparison design identifying same, matched, or independent specimens",
}


def _require_close(actual: Any, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Mroczkowski 1983 evidence schema")

    source = payload["source"]
    for field, expected in EXPECTED_SOURCE.items():
        if source.get(field) != expected:
            raise ValueError(f"publisher source field {field} changed")
    if source.get("publisher_record_recovered") is not True:
        raise ValueError("publisher record recovery status changed")
    if source.get("publisher_abstract_recovered") is not True:
        raise ValueError("publisher abstract recovery status changed")
    if source.get("primary_full_text_recovered") is not False:
        raise ValueError("full-text status cannot be promoted without recovery")
    if source.get("copyrighted_source_content_committed") is not False:
        raise ValueError("copyrighted source content may not be committed")

    if payload.get("measurement_class") != "vacancy_conditioned_exponential_tail_slope":
        raise ValueError("measurement class changed")
    model = payload["model"]
    if model.get("expression") != "alpha_e=alpha_0*exp[k*(E-E_0)]":
        raise ValueError("reported exponential model changed")
    if model.get("reported_parameter") != "k":
        raise ValueError("reported parameter changed")
    if model.get("reported_parameter_units") != "eV^-1":
        raise ValueError("reported parameter units changed")
    if model.get("derived_characteristic_quantity") != "1/k":
        raise ValueError("derived characteristic quantity changed")
    if model.get("derived_characteristic_quantity_semantics") != (
        "exponential e-fold energy, not a material-gap shift"
    ):
        raise ValueError("e-fold energy semantics changed")

    metadata = payload["common_metadata"]
    _require_close(metadata["composition_nominal_x"], 0.3, "nominal composition")
    if metadata.get("composition_uncertainty") is not None:
        raise ValueError("unreported composition uncertainty was fabricated")
    if metadata.get("carrier_type") != "p":
        raise ValueError("carrier type changed")
    if metadata.get("temperature_context") != "ambient temperature":
        raise ValueError("temperature context changed")
    if metadata.get("temperature_K") is not None:
        raise ValueError("ambient temperature cannot be assigned an exact Kelvin value")
    if metadata.get("specimen_count") is not None:
        raise ValueError("unreported specimen count was fabricated")
    for field in (
        "same_physical_specimen_contrast_established",
        "matched_specimen_design_established",
        "fit_window_reported",
        "slope_uncertainty_reported",
    ):
        if metadata.get(field) is not False:
            raise ValueError(f"unsupported metadata field {field} was promoted")

    endpoints = payload["reported_endpoints"]
    if len(endpoints) != 2:
        raise ValueError("reported endpoint inventory changed")
    endpoint_by_id = {row["state_id"]: row for row in endpoints}
    if set(endpoint_by_id) != {
        "high_purity_p_type",
        "stoichiometrically_doped_vacancy_rich",
    }:
        raise ValueError("reported state inventory changed")

    high_purity = endpoint_by_id["high_purity_p_type"]
    vacancy_rich = endpoint_by_id["stoichiometrically_doped_vacancy_rich"]
    _require_close(high_purity["tail_slope_k_eV_inverse"], 148.0, "high-purity k")
    _require_close(vacancy_rich["tail_slope_k_eV_inverse"], 105.0, "vacancy-rich k")
    if high_purity.get("acceptor_concentration_cm3") is not None:
        raise ValueError("high-purity acceptor concentration was fabricated")
    _require_close(
        vacancy_rich["acceptor_concentration_cm3"],
        2.0e16,
        "vacancy-rich acceptor concentration",
    )
    if vacancy_rich.get("acceptor_concentration_status") != (
        "approximate publisher-abstract value"
    ):
        raise ValueError("acceptor-concentration approximation status changed")
    for row in endpoints:
        if row.get("tail_slope_sigma_eV_inverse") is not None:
            raise ValueError("unreported slope uncertainty was fabricated")
        if row.get("value_status") != "exact_publisher_abstract":
            raise ValueError("publisher-abstract value status changed")

    interpretation = payload["source_interpretation"]
    if interpretation.get("reported_mechanism") != (
        "valence-band tailing associated with native Hg-vacancy acceptor defects"
    ):
        raise ValueError("reported source mechanism changed")
    if interpretation.get("mechanism_status") != "primary-source interpretation":
        raise ValueError("mechanism authority status changed")
    if interpretation.get("independent_causal_identification_established") is not False:
        raise ValueError("causal identification cannot be promoted")

    decision = payload["decision"]
    if decision != EXPECTED_DECISION:
        raise ValueError("Mroczkowski vacancy-tail decision changed")
    if set(payload["reopening_requirements"]) != EXPECTED_REOPENING_REQUIREMENTS:
        raise ValueError("full-text reopening requirement inventory changed")

    k_high = float(high_purity["tail_slope_k_eV_inverse"])
    k_vacancy = float(vacancy_rich["tail_slope_k_eV_inverse"])
    e_fold_high_mev = 1000.0 / k_high
    e_fold_vacancy_mev = 1000.0 / k_vacancy
    width_ratio = e_fold_vacancy_mev / e_fold_high_mev
    width_increase_percent = 100.0 * (width_ratio - 1.0)
    slope_ratio = k_vacancy / k_high
    slope_decrease_percent = 100.0 * (1.0 - slope_ratio)

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "source_doi": source["doi"],
        "measurement_class": payload["measurement_class"],
        "composition_nominal_x": metadata["composition_nominal_x"],
        "carrier_type": metadata["carrier_type"],
        "temperature_context": metadata["temperature_context"],
        "reported_values": {
            "high_purity_tail_slope_k_eV_inverse": k_high,
            "vacancy_rich_tail_slope_k_eV_inverse": k_vacancy,
            "vacancy_rich_acceptor_concentration_cm3": float(
                vacancy_rich["acceptor_concentration_cm3"]
            ),
        },
        "derived_diagnostics": {
            "high_purity_e_fold_energy_meV": e_fold_high_mev,
            "vacancy_rich_e_fold_energy_meV": e_fold_vacancy_mev,
            "e_fold_energy_difference_meV": e_fold_vacancy_mev - e_fold_high_mev,
            "e_fold_width_ratio": width_ratio,
            "e_fold_width_increase_percent": width_increase_percent,
            "tail_slope_ratio": slope_ratio,
            "tail_slope_decrease_percent": slope_decrease_percent,
        },
        "decision": decision,
        "claim_boundary": (
            "The publisher abstract establishes a fixed-nominal-composition association "
            "between Hg-vacancy acceptor state and exponential-tail slope. It does not "
            "establish a latent-gap shift, same-specimen causality, a universal vacancy "
            "coefficient, or uncertainty-weighted fit authority."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = audit(args.input_json)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
