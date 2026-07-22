"""Build the R04 depth-observation external-source extension record."""

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
from tools.build_spatial_disorder_pixel_scale_source_reference import (
    build_reference as prior_build_reference,
    candidate_records as prior_candidate_records,
)


def ariel_1995_candidate() -> ValidationCandidate:
    """Return the source-bounded derivative FTIR depth-grading record."""

    return ValidationCandidate(
        source_id="ariel_1995_derivative_depth_grading",
        citation=(
            "V. Ariel, V. Garber, D. Rosenfeld, and G. Bahir, Estimation of "
            "HgCdTe Band-Gap Variations by Differentiation of the Absorption "
            "Coefficient, Applied Physics Letters 66, 2101-2103 (1995)."
        ),
        doi="10.1063/1.113916",
        record_scope=(
            "uploaded full text audited; room-temperature FTIR transmission, "
            "absorption extraction, smoothing, first- and second-derivative "
            "figures, and source-level grading estimates"
        ),
        same_specimen=EvidenceState.CONFIRMED,
        same_spatial_region=EvidenceState.NOT_APPLICABLE,
        numerical_data_available=EvidenceState.ABSENT,
        independent_effective_scale_count=1,
        reusable_high_resolution_map=EvidenceState.ABSENT,
        declared_filterable_scale_count=0,
        kernel_characterized=EvidenceState.UNKNOWN,
        spatial_registration=EvidenceState.NOT_APPLICABLE,
        thickness_characterized=EvidenceState.CONFIRMED,
        depth_model_declared=EvidenceState.CONFIRMED,
        uncertainty_characterized=EvidenceState.ABSENT,
        observable_defined=EvidenceState.CONFIRMED,
        preprocessing_declared=EvidenceState.CONFIRMED,
        modality_count=1,
        spatial_map_reported=EvidenceState.ABSENT,
        rendered_figure_available=EvidenceState.CONFIRMED,
        depth_profile_observation_model=EvidenceState.CONFIRMED,
        notes=(
            "Room-temperature FTIR transmission is converted to absorption coefficient alpha(E), smoothed to reduce noise and interference fringes, and differentiated with respect to photon energy.",
            "The first-derivative maximum is used as an approximate average-gap marker; extrema of the second derivative are used to estimate Eg_min, Eg_max, and Delta Eg = Eg_max - Eg_min under a linearly graded depth model.",
            "The declared depth average is alpha(E) = (1/d) integral_0^d alpha_local[E, Eg(z)] dz.",
            "Bulk samples were 500 micrometres thick; epitaxial layers were 10-25 micrometres thick.",
            "The paper reports bulk band-gap variations below 0.005 eV and LPE-layer Delta Eg approximately 0.02 eV.",
            "The LPE built-in field is reported as approximately 10-20 V/cm and the MOCVD field around 30 V/cm, conditional on linear grading.",
            "The CdTe/HgCdTe graded interface is neglected only for layers thicker than 15 micrometres and cannot be neglected below that thickness.",
            "The authors state that the simplified Urbach/Kane model may have quantitative error from band nonparabolicity, Burstein-Moss shift, and a transition that is not exactly at Eg.",
            "Excessive smoothing can shift derivative peak positions, and the derivative peaks do not provide precise numerical band-gap values.",
            "No lateral coordinates, spatial raster, aperture or PSF, same-region scale sweep, numerical spectra, repeats, or uncertainty covariance are supplied.",
        ),
    )


def candidate_records() -> tuple[ValidationCandidate, ...]:
    """Return the prior portfolio plus the Ariel depth-observation record."""

    records = prior_candidate_records() + (ariel_1995_candidate(),)
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
            "nearest_depth_observation_model_context": (
                "ariel_1995_derivative_depth_grading"
            ),
            "depth_observation_temperature_k": 300.0,
            "bulk_sample_thickness_micrometre": 500.0,
            "epitaxial_layer_thickness_range_micrometre": [10.0, 25.0],
            "interface_grading_non_negligible_below_micrometre": 15.0,
            "bulk_band_gap_variation_upper_bound_ev": 0.005,
            "lpe_band_gap_variation_approximate_ev": 0.02,
            "lpe_linear_grading_field_range_v_per_cm": [10.0, 20.0],
            "mocvd_linear_grading_field_approximate_v_per_cm": 30.0,
            "decision": (
                "Ariel 1995 supplies a source-bounded depth-averaged FTIR "
                "observation operator and preprocessing sensitivity, not lateral "
                "mapping or probe-scale evidence. Gopal 1992 and Phillips 2003 "
                "retain their prior benchmark roles, and R04 remains externally "
                "data-blocked rather than analytically blocked."
            ),
            "minimum_data_upgrade_for_ariel_1995": [
                "original transmission, absorption, and derivative arrays",
                "exact smoothing and fringe-removal operator with parameters",
                "beam aperture or measured spatial PSF",
                "physical measurement coordinates if any lateral claim is made",
                "repeat uncertainty or observation covariance",
                "independent depth-profile validation for Eg(z)",
            ],
        }
    )
    return {
        "schema_version": "1.3",
        "portfolio_contribution": "R04",
        "parent_issue": 196,
        "implementation_issues": [250, 272, 281, 291],
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
            "A through-thickness Delta Eg estimate is not a lateral spatial variance or covariance statistic.",
            "One spatially averaged FTIR spectrum remains one effective lateral measurement kernel.",
            "Derivative peak positions are approximate observation-model markers, not precise intrinsic band-gap values.",
            "Reported built-in fields are conditional on linear grading and the declared layer thickness.",
            "Smoothing and fringe filtering can shift the derivative extrema used by the estimator.",
            "The CdTe/HgCdTe graded interface cannot be neglected for the reported layers thinner than 15 micrometres.",
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
