#!/usr/bin/env python3
"""Design the minimum paired HgCdTe dataset that separates gap and observation terms.

The oracle uses a local linearization, not a new band-gap equation.  At one fixed
measurement temperature the parameter vector is

    latent intercept,
    latent composition slope,
    absorption-class offset,
    carrier-filling scale,
    vacancy-edge scale.

A magneto-optical row observes only the latent terms.  A paired absorption row
observes the same latent terms plus the three absorption-specific terms.  The
purpose is to determine which metadata and pairings make those coefficients
algebraically and statistically identifiable.
"""
from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from mct_research.gap_models import provisional_hansen_pade_gap_ev

PARAMETER_LABELS = (
    "latent_intercept_mev",
    "latent_composition_slope_mev_per_coded_x",
    "absorption_class_offset_mev",
    "carrier_filling_scale_mev_per_proxy",
    "vacancy_edge_scale_mev_per_proxy",
)
PARAMETER_COUNT = len(PARAMETER_LABELS)
COMPOSITION_REFERENCE_X = 0.27
COMPOSITION_SCALE_X = 0.03
TARGET_COMPOSITION_X = 0.25
TARGET_GAP_ERROR_EV = 0.002


@dataclass(frozen=True)
class SpecimenDesign:
    specimen_id: str
    composition_code: float
    carrier_proxy_code: float
    vacancy_proxy_code: float
    paired_magneto_optical: bool = True


def _row(
    composition_code: float,
    measurement_class: str,
    carrier_proxy_code: float,
    vacancy_proxy_code: float,
) -> list[float]:
    if measurement_class == "magneto_optical":
        return [1.0, composition_code, 0.0, 0.0, 0.0]
    if measurement_class == "intrinsic_absorption":
        return [
            1.0,
            composition_code,
            1.0,
            carrier_proxy_code,
            -vacancy_proxy_code,
        ]
    raise ValueError(f"unsupported measurement class: {measurement_class}")


def design_matrix(specimens: Iterable[SpecimenDesign]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    rows: list[list[float]] = []
    ledger: list[dict[str, Any]] = []
    for specimen in specimens:
        composition_x = (
            COMPOSITION_REFERENCE_X
            + COMPOSITION_SCALE_X * specimen.composition_code
        )
        if specimen.paired_magneto_optical:
            rows.append(
                _row(
                    specimen.composition_code,
                    "magneto_optical",
                    specimen.carrier_proxy_code,
                    specimen.vacancy_proxy_code,
                )
            )
            ledger.append(
                {
                    "specimen_id": specimen.specimen_id,
                    "measurement_class": "magneto_optical",
                    "composition_x": composition_x,
                    "composition_code": specimen.composition_code,
                    "carrier_proxy_code": specimen.carrier_proxy_code,
                    "vacancy_proxy_code": specimen.vacancy_proxy_code,
                }
            )
        rows.append(
            _row(
                specimen.composition_code,
                "intrinsic_absorption",
                specimen.carrier_proxy_code,
                specimen.vacancy_proxy_code,
            )
        )
        ledger.append(
            {
                "specimen_id": specimen.specimen_id,
                "measurement_class": "intrinsic_absorption",
                "composition_x": composition_x,
                "composition_code": specimen.composition_code,
                "carrier_proxy_code": specimen.carrier_proxy_code,
                "vacancy_proxy_code": specimen.vacancy_proxy_code,
            }
        )
    return np.asarray(rows, dtype=float), ledger


def _matrix_diagnostics(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    tolerance = float(max(matrix.shape) * np.finfo(float).eps * singular_values[0])
    rank = int(np.sum(singular_values > tolerance))
    full_rank = rank == PARAMETER_COUNT
    result: dict[str, Any] = {
        "observation_count": int(matrix.shape[0]),
        "parameter_count": PARAMETER_COUNT,
        "rank": rank,
        "nullity": PARAMETER_COUNT - rank,
        "residual_degrees_of_freedom": int(matrix.shape[0] - rank),
        "singular_values": singular_values.tolist(),
        "smallest_singular_value": float(singular_values[-1]),
        "full_parameter_identification": full_rank,
        "condition_number": None,
        "information_determinant": 0.0,
        "parameter_standard_error_per_1mev_noise": None,
        "maximum_leverage": None,
    }
    if full_rank:
        information = matrix.T @ matrix
        covariance = np.linalg.inv(information)
        result.update(
            {
                "condition_number": float(singular_values[0] / singular_values[-1]),
                "information_determinant": float(np.linalg.det(information)),
                "parameter_standard_error_per_1mev_noise": {
                    label: float(value)
                    for label, value in zip(
                        PARAMETER_LABELS,
                        np.sqrt(np.diag(covariance)),
                        strict=True,
                    )
                },
                "maximum_leverage": float(
                    np.max(np.diag(matrix @ covariance @ matrix.T))
                ),
            }
        )
    result["audit_grade"] = bool(
        full_rank
        and result["condition_number"] is not None
        and result["condition_number"] <= 5.0
        and result["residual_degrees_of_freedom"] >= 8
        and result["maximum_leverage"] is not None
        and result["maximum_leverage"] <= 0.5
    )
    return result


def _scenario(
    name: str,
    specimens: list[SpecimenDesign],
    *,
    available_metadata: list[str],
    known_failure_mode: str,
) -> dict[str, Any]:
    matrix, ledger = design_matrix(specimens)
    return {
        "name": name,
        "specimen_count": len(specimens),
        "available_metadata": available_metadata,
        "known_failure_mode": known_failure_mode,
        "design_matrix": matrix.tolist(),
        "observation_ledger": ledger,
        "diagnostics": _matrix_diagnostics(matrix),
    }


def _current_chu_specimens() -> list[SpecimenDesign]:
    composition = [0.170, 0.200, 0.226, 0.276, 0.330, 0.366, 0.416, 0.443]
    return [
        SpecimenDesign(
            specimen_id=f"chu_secondary_{index + 1}",
            composition_code=(value - COMPOSITION_REFERENCE_X)
            / COMPOSITION_SCALE_X,
            carrier_proxy_code=0.0,
            vacancy_proxy_code=0.0,
            paired_magneto_optical=False,
        )
        for index, value in enumerate(composition)
    ]


def _paired_three(
    *, carrier: tuple[float, float, float], vacancy: tuple[float, float, float]
) -> list[SpecimenDesign]:
    return [
        SpecimenDesign(
            specimen_id=f"paired_{index + 1}",
            composition_code=composition,
            carrier_proxy_code=carrier[index],
            vacancy_proxy_code=vacancy[index],
        )
        for index, composition in enumerate((-1.0, 0.0, 1.0))
    ]


def _audit_grade_factorial() -> list[SpecimenDesign]:
    return [
        SpecimenDesign(
            specimen_id=f"factorial_{index + 1}",
            composition_code=float(composition),
            carrier_proxy_code=float(carrier),
            vacancy_proxy_code=float(vacancy),
        )
        for index, (composition, carrier, vacancy) in enumerate(
            itertools.product((-1.0, 1.0), repeat=3)
        )
    ]


def _composition_uncertainty_budget() -> dict[str, Any]:
    values: dict[str, Any] = {}
    step = 1.0e-6
    for temperature_k in (6.0, 77.0, 300.0):
        upper = float(
            provisional_hansen_pade_gap_ev(
                TARGET_COMPOSITION_X + step, temperature_k
            )
        )
        lower = float(
            provisional_hansen_pade_gap_ev(
                TARGET_COMPOSITION_X - step, temperature_k
            )
        )
        derivative = (upper - lower) / (2.0 * step)
        values[f"{temperature_k:g}K"] = {
            "absolute_dEg_dx_ev_per_x": abs(float(derivative)),
            "maximum_sigma_x_for_2mev_gap_budget": float(
                TARGET_GAP_ERROR_EV / abs(derivative)
            ),
        }
    return {
        "target_composition_x": TARGET_COMPOSITION_X,
        "target_gap_error_mev": 1000.0 * TARGET_GAP_ERROR_EV,
        "temperature_sensitivity": values,
        "recommendation": (
            "Use an independent composition method with sigma_x approximately "
            "1e-3 or better so composition uncertainty does not consume the full "
            "2 meV gap budget."
        ),
    }


def analyze() -> dict[str, Any]:
    scenarios = [
        _scenario(
            "current_secondary_chu_absorption_only",
            _current_chu_specimens(),
            available_metadata=[
                "reported_composition",
                "reported_absorption_fit_gap",
                "alpha_at_gap",
            ],
            known_failure_mode=(
                "latent intercept and absorption offset are exactly aliased; carrier "
                "and vacancy columns are unobserved"
            ),
        ),
        _scenario(
            "three_paired_gap_measurements_only",
            _paired_three(carrier=(0.0, 0.0, 0.0), vacancy=(0.0, 0.0, 0.0)),
            available_metadata=[
                "independent_composition",
                "paired_magneto_optical_gap",
                "paired_absorption_gap",
            ],
            known_failure_mode=(
                "pairing identifies the absorption offset but carrier and vacancy "
                "effects remain unobserved"
            ),
        ),
        _scenario(
            "three_paired_plus_hall",
            _paired_three(carrier=(-1.0, 0.0, 1.0), vacancy=(0.0, 0.0, 0.0)),
            available_metadata=[
                "independent_composition",
                "paired_gap_classes",
                "Hall_carrier_proxy",
            ],
            known_failure_mode="vacancy-edge contribution remains unobserved",
        ),
        _scenario(
            "three_paired_plus_vacancy_proxy",
            _paired_three(carrier=(0.0, 0.0, 0.0), vacancy=(-1.0, 0.0, 1.0)),
            available_metadata=[
                "independent_composition",
                "paired_gap_classes",
                "vacancy_sensitive_proxy",
            ],
            known_failure_mode="carrier-filling contribution remains unobserved",
        ),
        _scenario(
            "algebraic_minimum_three_paired_specimens",
            _paired_three(carrier=(-1.0, 1.0, 0.0), vacancy=(-1.0, -1.0, 1.0)),
            available_metadata=[
                "independent_composition",
                "paired_gap_classes",
                "Hall_carrier_proxy",
                "vacancy_sensitive_proxy",
            ],
            known_failure_mode=(
                "full rank but only one residual degree of freedom and unit maximum "
                "leverage; unsuitable as an audit-grade validation dataset"
            ),
        ),
        _scenario(
            "audit_grade_eight_specimen_factorial",
            _audit_grade_factorial(),
            available_metadata=[
                "independent_composition",
                "paired_gap_classes",
                "Hall_carrier_proxy",
                "vacancy_sensitive_proxy",
                "raw_absorption_curve",
                "extraction_method_and_covariance",
            ],
            known_failure_mode=(
                "none in the declared five-parameter linearization; nonlinear physics "
                "and external transfer still require holdout validation"
            ),
        ),
    ]

    scenario_map = {entry["name"]: entry for entry in scenarios}
    algebraic = scenario_map["algebraic_minimum_three_paired_specimens"][
        "diagnostics"
    ]
    audit_grade = scenario_map["audit_grade_eight_specimen_factorial"][
        "diagnostics"
    ]

    return {
        "schema_version": "1.0",
        "analysis": "minimum paired HgCdTe gap-identifiability dataset design",
        "linearized_parameter_labels": list(PARAMETER_LABELS),
        "composition_coding": {
            "reference_x": COMPOSITION_REFERENCE_X,
            "scale_x": COMPOSITION_SCALE_X,
            "coded_minus_one_x": COMPOSITION_REFERENCE_X - COMPOSITION_SCALE_X,
            "coded_plus_one_x": COMPOSITION_REFERENCE_X + COMPOSITION_SCALE_X,
        },
        "scenarios": scenarios,
        "minimum_design_decision": {
            "algebraic_minimum_specimen_count_per_temperature": 3,
            "algebraic_minimum_observation_count_per_temperature": 6,
            "algebraic_minimum_full_rank": algebraic[
                "full_parameter_identification"
            ],
            "algebraic_minimum_is_audit_grade": algebraic["audit_grade"],
            "recommended_audit_grade_specimen_count": 8,
            "recommended_paired_gap_observations_per_temperature": 16,
            "recommended_temperature_blocks": ["low_temperature", "300K"],
            "recommended_total_paired_gap_observations": 32,
            "recommended_design_is_audit_grade": audit_grade["audit_grade"],
            "recommended_residual_degrees_of_freedom_per_temperature": audit_grade[
                "residual_degrees_of_freedom"
            ],
            "recommended_maximum_leverage": audit_grade["maximum_leverage"],
            "recommended_condition_number": audit_grade["condition_number"],
        },
        "required_specimen_fields": [
            "specimen_id shared across all measurements",
            "independent composition x and sigma_x",
            "temperature and its uncertainty",
            "paired magneto-optical gap on the same specimen",
            "raw intrinsic-absorption spectrum on the same specimen",
            "absorption extraction definition and covariance",
            "Hall carrier type, density and mobility at each temperature block",
            "measured vacancy-sensitive proxy or controlled paired anneal state",
            "sample thickness, strain state and doping/anneal history",
        ],
        "composition_uncertainty_budget": _composition_uncertainty_budget(),
        "scientific_decision": (
            "The existing absorption-only table is structurally unable to identify a "
            "latent material gap separately from measurement-class effects. Three paired "
            "specimens are the algebraic minimum, but an eight-specimen two-level factorial "
            "measured in paired modalities at low temperature and 300 K is the minimum "
            "recommended audit-grade acquisition."
        ),
        "claim_boundary": [
            "The oracle is a local linearized design analysis, not a physical gap fit.",
            "Carrier and vacancy proxy codes denote independently measured contrasts, not raw concentrations.",
            "Full matrix rank does not prove the assumed observation model is complete.",
            "The recommended design must reserve specimens or conditions for external holdout validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
