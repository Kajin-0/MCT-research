"""Build the R04 pixel-scale external-source extension record."""

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
from tools.build_spatial_disorder_validation_path_reference import (
    candidate_records as prior_candidate_records,
)


def phillips_2003_candidate() -> ValidationCandidate:
    """Return the source-bounded detector-pixel-scale absorption record."""

    return ValidationCandidate(
        source_id="phillips_2003_pixel_scale_absorption_mapping",
        citation=(
            "J. D. Phillips et al., Uniformity of Optical Absorption in HgCdTe "
            "Epilayer Measured by Infrared Spectromicroscopy, Applied Physics "
            "Letters 83, 3701-3703 (2003)."
        ),
        doi="10.1063/1.1625776",
        record_scope=(
            "open full text audited; rendered 2 mm line scan, 200 by 200 "
            "micrometre area maps, histograms, and summary statistics"
        ),
        same_specimen=EvidenceState.CONFIRMED,
        same_spatial_region=EvidenceState.NOT_APPLICABLE,
        numerical_data_available=EvidenceState.ABSENT,
        independent_effective_scale_count=1,
        reusable_high_resolution_map=EvidenceState.ABSENT,
        declared_filterable_scale_count=0,
        kernel_characterized=EvidenceState.UNKNOWN,
        spatial_registration=EvidenceState.CONFIRMED,
        thickness_characterized=EvidenceState.CONFIRMED,
        depth_model_declared=EvidenceState.CONFIRMED,
        uncertainty_characterized=EvidenceState.ABSENT,
        observable_defined=EvidenceState.CONFIRMED,
        preprocessing_declared=EvidenceState.CONFIRMED,
        modality_count=1,
        spatial_map_reported=EvidenceState.CONFIRMED,
        rendered_figure_available=EvidenceState.CONFIRMED,
        notes=(
            "The infrared beam diameter was determined to be approximately 9 micrometres and spectra were sampled at 10-micrometre spacing.",
            "The source reports a 2 mm line scan and a 200 by 200 micrometre area map containing 400 measured spectra at one effective scale.",
            "At 1558 cm^-1, the reported absorption coefficient mean is 887 cm^-1 and standard deviation is 24.6 cm^-1, or 2.8 percent.",
            "The extracted composition mean is x = 0.2256 with standard deviation 3.0e-4.",
            "The authors warn that extracted composition conflates thickness, alloy composition, absorption, and interface reflections, and that one apparent spatial drift may be measurement drift.",
            "No machine-readable arrays, full PSF, repeat covariance, or second probe scale are supplied in the article record.",
        ),
    )


def candidate_records() -> tuple[ValidationCandidate, ...]:
    """Return the prior portfolio plus the Phillips detector-pixel record."""

    records = prior_candidate_records() + (phillips_2003_candidate(),)
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
    return {
        "schema_version": "1.2",
        "portfolio_contribution": "R04",
        "parent_issue": 196,
        "implementation_issues": [250, 272, 281],
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
        "headline": {
            "direct_validation_candidate_count": len(
                portfolio.direct_candidate_ids
            ),
            "partial_multiresolution_candidate_count": len(
                portfolio.partial_multiresolution_candidate_ids
            ),
            "nearest_partial_multiresolution_benchmark": (
                "gopal_1992_two_beam_transmission"
            ),
            "nearest_partial_scale_diameters_micrometre": [3000.0, 250.0],
            "nearest_partial_scale_ratio": 12.0,
            "nearest_detector_pixel_scale_benchmark": (
                "phillips_2003_pixel_scale_absorption_mapping"
            ),
            "pixel_scale_beam_diameter_micrometre": 9.0,
            "pixel_scale_scan_spacing_micrometre": 10.0,
            "pixel_scale_area_micrometre": [200.0, 200.0],
            "pixel_scale_reported_spectrum_count": 400,
            "decision": (
                "Gopal 1992 remains the nearest partial multiresolution "
                "benchmark. Phillips 2003 is the nearest detector-pixel-scale "
                "spatial absorption benchmark, but its 400 spectra share one "
                "effective probe scale and the article does not expose "
                "machine-readable arrays. R04 remains externally data-blocked, "
                "not analytically blocked."
            ),
            "minimum_data_upgrade_for_phillips_2003": [
                "original numerical spectra with physical coordinates",
                "measured or reconstructable wavelength-dependent PSF",
                "repeat uncertainty or observation covariance",
                "at least two additional calibrated effective scales for family closure",
                "provenance for source-intensity drift and spatial-drift correction",
            ],
        },
        "claim_boundaries": [
            "A dense raster at one measurement kernel remains one effective probe scale.",
            "Four hundred spectra do not constitute four hundred independent probe scales.",
            "Two measured scales can establish qualitative scale dependence but cannot test covariance-family closure.",
            "Rendered spectra and map figures are not original numerical arrays and must not be represented as such.",
            "A reported beam diameter is not a full measured point-spread function.",
            "Source qualification does not infer specimen point variance, correlation length, covariance family, or detector behavior.",
            "The external-data decision does not authorize a novelty claim or manuscript writing.",
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
