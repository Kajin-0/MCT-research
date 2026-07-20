#!/usr/bin/env python3
"""Fail-closed audit for Finkman-Schacham 1984 operational-edge evidence."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.finkman_1984_operational_edge import (
    ABSORPTION_RANGE_CM1,
    COMPOSITION_RANGE,
    OPERATIONAL_EDGE_THRESHOLD_CM1,
    SOURCE_CONTENT_FINGERPRINT_SHA256,
    SOURCE_DOI,
    TEMPERATURE_RANGE_K,
    absorption_cm1_at_energy,
    energy_at_absorption_cm1,
    operational_edge_500_cm1,
    published_eq11_operational_edge_ev,
    zero_intercept_absorption_cm1,
    zero_intercept_energy_ev,
)

EXPECTED_DECISION = {
    "copyrighted_source_content_committed": False,
    "historical_operational_edge_evidence_authorized": True,
    "latent_material_gap_point_authorized": False,
    "pool_with_magneto_optical_gaps_by_default": False,
    "source_bound_threshold_operator_authorized": True,
    "universal_gap_law_fit_authorized": False,
    "zero_intercept_and_alpha500_interchangeable": False,
}


def _require_close(actual: Any, expected: float, field: str) -> None:
    if not isinstance(actual, (int, float)) or not math.isclose(
        float(actual), expected, rel_tol=0.0, abs_tol=1.0e-12
    ):
        raise ValueError(f"{field} changed: {actual!r} != {expected!r}")


def audit(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("unsupported Finkman 1984 evidence schema")

    source = payload["source"]
    if source.get("doi") != SOURCE_DOI:
        raise ValueError("Finkman 1984 DOI changed")
    if source.get("source_content_fingerprint_sha256") != SOURCE_CONTENT_FINGERPRINT_SHA256:
        raise ValueError("Finkman 1984 source-content fingerprint changed")
    if source.get("full_text_recovered") is not True:
        raise ValueError("Finkman 1984 full-text recovery status changed")
    if source.get("copyrighted_source_committed") is not False:
        raise ValueError("copyrighted source content may not be committed")

    specimens = payload["direct_hgcdte_specimens"]
    _require_close(specimens["composition_x"], 0.29, "direct composition")
    _require_close(specimens["composition_deviation"], 0.005, "composition deviation")
    if specimens.get("carrier_type") != "n":
        raise ValueError("direct specimen carrier type changed")
    if specimens.get("sample_count") != 6:
        raise ValueError("direct specimen inventory changed")
    if specimens.get("growth_methods") != [
        "solid-state recrystallization",
        "Bridgman",
    ]:
        raise ValueError("direct specimen growth-method inventory changed")
    if specimens.get("carrier_density_cm3_range_at_77K") != [9.0e14, 3.0e15]:
        raise ValueError("carrier-density range changed")
    if specimens.get("hall_mobility_cm2_Vs_range_at_77K") != [3.0e4, 5.0e4]:
        raise ValueError("Hall-mobility range changed")
    if specimens.get("thickness_um_range") != [25.0, 300.0]:
        raise ValueError("specimen thickness range changed")
    _require_close(specimens["temperature_stability_K"], 0.3, "temperature stability")

    domain = payload["combined_hg_rich_operator_domain"]
    if tuple(domain["composition_x_range"]) != COMPOSITION_RANGE:
        raise ValueError("Finkman composition domain changed")
    if tuple(domain["temperature_K_range"]) != TEMPERATURE_RANGE_K:
        raise ValueError("Finkman temperature domain changed")
    if tuple(domain["absorption_cm1_range"]) != ABSORPTION_RANGE_CM1:
        raise ValueError("Finkman absorption domain changed")

    semantics = payload["operational_edge_500_cm1"]
    _require_close(
        semantics["absorption_threshold_cm1"],
        OPERATIONAL_EDGE_THRESHOLD_CM1,
        "operational threshold",
    )
    if semantics.get("source_symbol") != "Eg":
        raise ValueError("source symbol changed")
    if semantics.get("repository_quantity") != "energy_at_alpha_500_cm1":
        raise ValueError("repository quantity changed")
    if semantics.get("observation_class") != "fixed_absorption_threshold":
        raise ValueError("observation class changed")
    if semantics.get("latent_material_gap_identified") is not False:
        raise ValueError("operational edge cannot be promoted to a latent gap")
    if semantics.get("exact_detector_equivalence_claimed") is not False:
        raise ValueError("approximate detector relationship cannot be made exact")

    zero = payload["zero_intercept"]
    _require_close(zero["reference_thickness_um"], 500.0, "zero-intercept thickness")
    _require_close(
        zero["reference_absorption_cm1"],
        zero_intercept_absorption_cm1(500.0),
        "zero-intercept absorption",
    )
    if zero.get("interchangeable_with_alpha_500_edge") is not False:
        raise ValueError("zero-intercept and alpha=500 edges cannot be interchangeable")

    decision = payload["decision"]
    if decision != EXPECTED_DECISION:
        raise ValueError("Finkman operational-edge decision changed")

    thresholds = [float(value) for value in payload["reference_absorption_thresholds_cm1"]]
    if thresholds != [20.0, 50.0, 500.0, 1000.0]:
        raise ValueError("reference threshold inventory changed")

    reference_rows: list[dict[str, Any]] = []
    for point in payload["reference_points"]:
        x = float(point["composition_x"])
        temperature = float(point["temperature_K"])
        energies = {
            f"alpha_{threshold:g}_cm1_eV": energy_at_absorption_cm1(
                threshold,
                temperature,
                x,
            )
            for threshold in thresholds
        }
        for threshold in thresholds:
            recovered = absorption_cm1_at_energy(
                energies[f"alpha_{threshold:g}_cm1_eV"],
                temperature,
                x,
            )
            if not math.isclose(recovered, threshold, rel_tol=0.0, abs_tol=1.0e-9):
                raise ValueError("Finkman Eq. (10) round trip failed")
        reference_rows.append(
            {
                "composition_x": x,
                "temperature_K": temperature,
                **energies,
                "alpha_20_to_1000_span_meV": 1000.0
                * (energies["alpha_1000_cm1_eV"] - energies["alpha_20_cm1_eV"]),
                "alpha_50_to_500_span_meV": 1000.0
                * (energies["alpha_500_cm1_eV"] - energies["alpha_50_cm1_eV"]),
            }
        )

    x_grid = np.linspace(COMPOSITION_RANGE[0], COMPOSITION_RANGE[1], 101)
    t_grid = np.linspace(TEMPERATURE_RANGE_K[0], TEMPERATURE_RANGE_K[1], 101)
    eq11_residuals_mev = [
        1000.0
        * (
            published_eq11_operational_edge_ev(float(temperature), float(x))
            - operational_edge_500_cm1(float(temperature), float(x))
        )
        for x in x_grid
        for temperature in t_grid
    ]

    zero_intercept_rows: list[dict[str, float]] = []
    for x in (0.215, 0.29):
        zero_energy = zero_intercept_energy_ev(500.0, 300.0, x)
        threshold_energy = operational_edge_500_cm1(300.0, x)
        zero_intercept_rows.append(
            {
                "composition_x": x,
                "temperature_K": 300.0,
                "thickness_um": 500.0,
                "zero_intercept_absorption_cm1": zero_intercept_absorption_cm1(500.0),
                "zero_intercept_energy_eV": zero_energy,
                "alpha_500_operational_edge_eV": threshold_energy,
                "zero_intercept_minus_alpha500_meV": 1000.0
                * (zero_energy - threshold_energy),
            }
        )

    thickness_rows = [
        {
            "thickness_um": thickness,
            "zero_intercept_absorption_cm1": zero_intercept_absorption_cm1(thickness),
            "inside_common_operator_domain": (
                ABSORPTION_RANGE_CM1[0]
                <= zero_intercept_absorption_cm1(thickness)
                <= ABSORPTION_RANGE_CM1[1]
            ),
        }
        for thickness in (25.0, 50.0, 100.0, 300.0, 500.0)
    ]

    return {
        "schema_version": payload["schema_version"],
        "analysis": payload["analysis"],
        "source_doi": SOURCE_DOI,
        "reference_rows": reference_rows,
        "published_eq11_rounding_residual_meV": {
            "minimum": float(min(eq11_residuals_mev)),
            "maximum": float(max(eq11_residuals_mev)),
            "maximum_absolute": float(max(abs(value) for value in eq11_residuals_mev)),
        },
        "zero_intercept_rows": zero_intercept_rows,
        "thickness_rows": thickness_rows,
        "decision": decision,
        "claim_boundary": (
            "The source-bound formulas quantify fixed-absorption and thickness-dependent "
            "operational edges. They do not identify an intrinsic material gap, authorize "
            "cross-modality pooling, or define a universal HgCdTe gap law."
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
