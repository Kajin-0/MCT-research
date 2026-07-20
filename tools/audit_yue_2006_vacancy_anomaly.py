#!/usr/bin/env python3
"""Fail-closed audit for Yue et al. 2006 vacancy-conditioned edge evidence."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from mct_research.yue_2006_vacancy_anomaly import (
    SOURCE_DOI,
    SOURCE_RECORD_FINGERPRINT_SHA256,
    bulk_critical_absorption_cm1,
)

EXPECTED_AUTHORS = [
    "Fangyu Yue",
    "Jun Shao",
    "Xiang Lu",
    "Wei Huang",
    "Junhao Chu",
    "Jun Wu",
    "Xingchao Lin",
    "Li He",
]
EXPECTED_TABLE = {
    "B2": ("bulk", 0.232, "gt", 200.0, 7.2e14, 77.0, 11.3, True),
    "B9": ("bulk", 0.337, "gt", 200.0, 1.4e14, 77.0, 10.5, True),
    "Mag": ("MBE", 0.298, "eq", 6.0, 3.25e15, 300.0, 10.0, True),
    "M16": ("MBE", 0.308, "eq", 6.1, 5.81e15, 300.0, 9.7, True),
    "M17": ("MBE", 0.306, "eq", 7.9, 4.19e15, 300.0, 0.0, False),
}
EXPECTED_DECISION = {
    "cross_temperature_carrier_density_correlation_authorized": False,
    "independent_composition_validation_authorized": False,
    "latent_material_gap_points_authorized": False,
    "measured_vacancy_concentration_available": False,
    "processing_conditioned_vacancy_mechanism_evidence_authorized": True,
    "same_specimen_causal_contrast_established": False,
    "temperature_resolved_vacancy_anomaly_evidence_authorized": True,
    "uncertainty_weighted_material_law_fitting_authorized": False,
    "universal_vacancy_correction_authorized": False,
    "vacancy_removing_anneal_control_evidence_status": "conditional",
}


def _require_close(actual: Any, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Yue 2006 evidence schema")

    source = payload["source"]
    if source.get("doi") != SOURCE_DOI:
        raise ValueError("Yue 2006 DOI changed")
    if source.get("authors") != EXPECTED_AUTHORS:
        raise ValueError("Yue 2006 author inventory changed")
    if source.get("canonical_extracted_record_fingerprint_sha256") != (
        SOURCE_RECORD_FINGERPRINT_SHA256
    ):
        raise ValueError("Yue 2006 extracted-record fingerprint changed")
    if source.get("primary_full_text_recovered") is not True:
        raise ValueError("Yue 2006 full-text recovery status changed")
    if source.get("copyrighted_source_content_committed") is not False:
        raise ValueError("copyrighted source content may not be committed")

    system = payload["measurement_system"]
    if system.get("spectrometer") != "Bruker IFS 66v/S":
        raise ValueError("spectrometer identity changed")
    _require_close(system["spectral_resolution_cm1"], 6.0, "spectral resolution")
    _require_close(
        system["spectral_resolution_meV_approx"],
        0.7,
        "approximate spectral resolution",
    )
    if system.get("temperature_range_K") != [11.0, 300.0]:
        raise ValueError("measurement temperature range changed")

    composition = payload["composition_provenance"]
    if composition.get("status") != (
        "absorption_derived_circular_for_material_law_validation"
    ):
        raise ValueError("composition provenance status changed")
    if composition.get("independent_composition_measurement") is not False:
        raise ValueError("absorption-derived composition cannot be made independent")
    if composition.get("composition_sigma_x") is not None:
        raise ValueError("unreported composition uncertainty was fabricated")
    _require_close(
        composition["critical_energy_total_error_meV_less_than"],
        0.8,
        "critical-energy error bound",
    )
    if composition.get("critical_energy_error_is_not_table_deltaE_sigma") is not True:
        raise ValueError("critical-point error was relabelled as Table I uncertainty")

    operators = payload["observation_operators"]
    bulk_operator = operators["bulk"]
    if bulk_operator.get("measurement_class") != (
        "bulk_absorption_extrapolation_to_critical_alpha"
    ):
        raise ValueError("bulk observation class changed")
    if bulk_operator.get("expression") != (
        "alpha_Eg=-65+1.88*T+(8694-10.31*T)*x"
    ):
        raise ValueError("bulk critical-alpha expression changed")
    mbe_operator = operators["mbe"]
    if mbe_operator.get("measurement_class") != (
        "exponential_edge_kane_plateau_intersection"
    ):
        raise ValueError("MBE observation class changed")
    if mbe_operator.get("numerical_operator_complete_without_native_spectrum") is not False:
        raise ValueError("MBE operator cannot be completed without native spectra")
    alternative = operators["alternative_bulk_methods"]
    _require_close(
        alternative["reported_scatter_meV_less_than"],
        2.0,
        "alternative-method scatter",
    )
    if alternative.get("scatter_is_not_specimen_uncertainty") is not True:
        raise ValueError("method scatter was relabelled as specimen uncertainty")

    specimens = payload["specimens"]
    if len(specimens) != 5:
        raise ValueError("Yue 2006 specimen inventory changed")
    specimen_by_id = {row["sample_id"]: row for row in specimens}
    if set(specimen_by_id) != set(EXPECTED_TABLE):
        raise ValueError("Yue 2006 sample identifiers changed")
    for sample_id, expected in EXPECTED_TABLE.items():
        row = specimen_by_id[sample_id]
        sample_class, x, relation, thickness, density, density_t, delta_e, anomaly = expected
        if row.get("sample_class") != sample_class:
            raise ValueError(f"{sample_id} sample class changed")
        _require_close(row["composition_x"], x, f"{sample_id} composition")
        if row.get("thickness_relation") != relation:
            raise ValueError(f"{sample_id} thickness relation changed")
        _require_close(row["thickness_um"], thickness, f"{sample_id} thickness")
        _require_close(row["carrier_density_cm3"], density, f"{sample_id} carrier density")
        _require_close(
            row["carrier_density_temperature_K"],
            density_t,
            f"{sample_id} carrier-density temperature",
        )
        _require_close(row["deltaE_meV"], delta_e, f"{sample_id} deltaE")
        if row.get("deltaE_value_status") != "exact_table":
            raise ValueError(f"{sample_id} Table I value status changed")
        if row.get("anomalous_temperature_dependence") is not anomaly:
            raise ValueError(f"{sample_id} anomaly status changed")
        if row.get("carrier_type") != "not reported in Table I":
            raise ValueError(f"{sample_id} carrier type was inferred")

    if specimen_by_id["M16"].get("achieved_vacancy_concentration_measured") is not False:
        raise ValueError("M16 vacancy concentration was fabricated")
    if specimen_by_id["M17"].get("achieved_vacancy_concentration_measured") is not False:
        raise ValueError("M17 vacancy concentration was fabricated")
    if specimen_by_id["M17"].get("temperature_dependence") != (
        "monotonic over measured range"
    ):
        raise ValueError("M17 monotonic control status changed")

    delta_semantics = payload["deltaE_semantics"]
    if delta_semantics.get("quantity") != (
        "extrapolated_zero_temperature_anomalous_edge_separation"
    ):
        raise ValueError("deltaE quantity changed")
    if delta_semantics.get("direct_defect_level_measurement") is not False:
        raise ValueError("deltaE cannot be promoted to direct defect metrology")
    if delta_semantics.get("latent_material_gap_shift") is not False:
        raise ValueError("deltaE cannot be promoted to a latent-gap shift")
    if delta_semantics.get("specimen_level_sigma_reported") is not False:
        raise ValueError("unreported deltaE uncertainty was fabricated")

    mechanism = payload["mechanism_interpretation"]
    if mechanism.get("direct_vacancy_metrology") is not False:
        raise ValueError("source interpretation cannot become direct vacancy metrology")
    if mechanism.get("same_physical_specimen_before_after_processing") is not False:
        raise ValueError("independent specimens cannot become a paired contrast")

    decision = payload["decision"]
    if decision != EXPECTED_DECISION:
        raise ValueError("Yue 2006 decision boundary changed")

    anomalous = [row for row in specimens if row["anomalous_temperature_dependence"]]
    positive_delta = [float(row["deltaE_meV"]) for row in anomalous]
    bulk_delta = [
        float(row["deltaE_meV"])
        for row in specimens
        if row["sample_class"] == "bulk"
    ]
    processing_reference_delta = [
        float(specimen_by_id[sample_id]["deltaE_meV"])
        for sample_id in ("Mag", "M16")
    ]
    operator_reference = [
        {
            "composition_x": x,
            "temperature_K": temperature,
            "critical_absorption_cm1": bulk_critical_absorption_cm1(x, temperature),
        }
        for x in (0.232, 0.337)
        for temperature in (11.0, 77.0, 300.0)
    ]

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "source_doi": source["doi"],
        "specimen_count": len(specimens),
        "anomalous_specimen_count": len(anomalous),
        "nonanomalous_specimen_ids": [
            row["sample_id"]
            for row in specimens
            if not row["anomalous_temperature_dependence"]
        ],
        "bulk_mean_deltaE_meV": sum(bulk_delta) / len(bulk_delta),
        "as_grown_and_vacancy_intensifying_mbe_mean_deltaE_meV": (
            sum(processing_reference_delta) / len(processing_reference_delta)
        ),
        "vacancy_removing_m17_deltaE_meV": float(specimen_by_id["M17"]["deltaE_meV"]),
        "positive_anomaly_deltaE_range_meV": [min(positive_delta), max(positive_delta)],
        "positive_anomaly_mean_deltaE_meV": sum(positive_delta) / len(positive_delta),
        "bulk_critical_absorption_reference": operator_reference,
        "carrier_density_temperature_groups": {
            "bulk_K": sorted(
                {
                    float(row["carrier_density_temperature_K"])
                    for row in specimens
                    if row["sample_class"] == "bulk"
                }
            ),
            "mbe_K": sorted(
                {
                    float(row["carrier_density_temperature_K"])
                    for row in specimens
                    if row["sample_class"] == "MBE"
                }
            ),
        },
        "decision": decision,
        "claim_boundary": (
            "The source establishes temperature-resolved, processing-conditioned "
            "absorption-edge anomalies. It does not provide independent composition, "
            "direct vacancy concentration, same-specimen causality, latent-gap points, "
            "or a universal vacancy correction."
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
