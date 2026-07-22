"""Build the R04 same-wafer spatial-observation method source record."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Any

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    QualificationClass,
    ValidationCandidate,
    qualify_validation_portfolio,
)
from tools.build_spatial_disorder_depth_observation_source_reference import (
    build_reference as prior_build_reference,
    candidate_records as prior_candidate_records,
)


def ariel_1996_candidate() -> ValidationCandidate:
    """Return the abstract-bounded same-wafer differential-absorption record."""

    return ValidationCandidate(
        source_id="ariel_1996_same_wafer_differential_absorption",
        citation=(
            "V. Ariel, V. Garber, G. Bahir, S. Krishnamurthy, and A. Sher, "
            "Monitoring HgCdTe Layer Uniformity by the Differential Absorption "
            "Technique, Applied Physics Letters 69, 1864-1866 (1996)."
        ),
        doi=None,
        record_scope=(
            "accessible abstract and bibliographic records audited; full text and "
            "authoritative DOI record not retrieved"
        ),
        same_specimen=EvidenceState.CONFIRMED,
        same_spatial_region=EvidenceState.NOT_APPLICABLE,
        numerical_data_available=EvidenceState.NOT_RETRIEVED,
        independent_effective_scale_count=1,
        reusable_high_resolution_map=EvidenceState.NOT_RETRIEVED,
        declared_filterable_scale_count=0,
        kernel_characterized=EvidenceState.NOT_RETRIEVED,
        spatial_registration=EvidenceState.UNKNOWN,
        thickness_characterized=EvidenceState.UNKNOWN,
        depth_model_declared=EvidenceState.UNKNOWN,
        uncertainty_characterized=EvidenceState.UNKNOWN,
        observable_defined=EvidenceState.CONFIRMED,
        preprocessing_declared=EvidenceState.CONFIRMED,
        modality_count=1,
        spatial_map_reported=EvidenceState.UNKNOWN,
        rendered_figure_available=EvidenceState.NOT_RETRIEVED,
        depth_profile_observation_model=EvidenceState.NOT_RETRIEVED,
        spatial_point_observation_method=EvidenceState.CONFIRMED,
        notes=(
            "The accessible abstract reports room-temperature transmission measurements on HgCdTe wafers.",
            "Data filtering removes interference fringes and high-frequency noise and is reported to produce reliable transmission for layers as thin as 8 micrometres.",
            "The interference-fringe spectrum is used to estimate HgCdTe layer thickness with reported accuracy approximately plus or minus 0.1 micrometre.",
            "The absorption coefficient is differentiated twice with respect to photon energy and an approximate band gap is estimated from derivative extrema.",
            "The procedure is applied at different points on the same HgCdTe wafer to determine lateral and transverse band-gap fluctuations.",
            "Initial differential-absorption accuracy is reported as around plus or minus 0.5 meV for HgCdTe wafers.",
            "The method is described as simple, nondestructive, and applicable at room temperature.",
            "The accessible record does not expose point count, point spacing, physical coordinates, acquisition order, aperture or PSF, a spatial map, numerical arrays, repeats, or observation covariance.",
            "The exact DOI remains unresolved from an authoritative accessible record and is intentionally not guessed.",
        ),
    )


def candidate_records() -> tuple[ValidationCandidate, ...]:
    """Return the prior portfolio plus the Ariel 1996 method record."""

    records = prior_candidate_records() + (ariel_1996_candidate(),)
    return tuple(sorted(records, key=lambda item: item.source_id))


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def build_reference() -> dict[str, object]:
    candidates = candidate_records()
    portfolio = qualify_validation_portfolio(candidates)
    prior = prior_build_reference()
    headline = dict(prior["headline"])
    headline.update(
        {
            "nearest_spatial_observation_method_context": (
                "ariel_1996_same_wafer_differential_absorption"
            ),
            "spatial_method_full_text_status": "not_retrieved",
            "spatial_method_doi_status": "unresolved_not_guessed",
            "spatial_method_temperature_k": 300.0,
            "minimum_reliable_layer_thickness_micrometre": 8.0,
            "reported_thickness_accuracy_micrometre": 0.1,
            "reported_band_gap_method_accuracy_mev": 0.5,
            "same_wafer_multiple_positions_reported": True,
            "reported_effective_lateral_scale_count": 1,
            "price_boyd_review_doi": "10.1088/0268-1242/8/6S/006",
            "price_boyd_full_text_status": "not_retrieved",
            "decision": (
                "Ariel 1996 supplies abstract-bounded same-wafer point-sampling "
                "method context, not a calibrated raster, numerical map, or "
                "multiresolution dataset. Price and Boyd 1993 remains a verified "
                "review target whose full text was not retrieved. R04 remains "
                "externally data-blocked rather than analytically blocked."
            ),
            "minimum_data_upgrade_for_ariel_1996": [
                "authoritative full text and DOI record",
                "original transmission, absorption, and derivative arrays",
                "physical coordinates, point count, spacing, and acquisition order",
                "measured or reconstructable aperture and spatial PSF",
                "repeat uncertainty or observation covariance",
                "explicit numerical separation of lateral and transverse fluctuations",
                "at least two additional calibrated effective scales or one reusable high-resolution map",
            ],
        }
    )
    return {
        "schema_version": "1.4",
        "portfolio_contribution": "R04",
        "parent_issue": 196,
        "implementation_issues": [250, 272, 281, 291, 302],
        "status": portfolio.status,
        "direct_candidate_ids": list(portfolio.direct_candidate_ids),
        "partial_multiresolution_candidate_ids": list(
            portfolio.partial_multiresolution_candidate_ids
        ),
        "qualification_classes": [item.value for item in QualificationClass],
        "candidates": [_jsonable(asdict(item)) for item in candidates],
        "qualifications": [
            _jsonable(asdict(item)) for item in portfolio.qualifications
        ],
        "minimum_next_action": list(portfolio.minimum_next_action),
        "headline": headline,
        "claim_boundaries": list(prior["claim_boundaries"])
        + [
            "Measurements at different points on one wafer establish spatial sampling intent but do not establish a calibrated raster or spatial map.",
            "One uncharacterized optical setup remains one effective lateral scale.",
            "A reported plus-or-minus 0.5 meV method accuracy is not repeat uncertainty or observation covariance.",
            "Lateral and transverse fluctuation language does not supply their numerical decomposition without the full data and model.",
            "An unresolved DOI must remain null rather than being inferred from journal metadata.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(build_reference(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
