"""Build the controlled R04 external validation-path qualification record."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Any

from mct_research.spatial_disorder_validation_path import (
    EvidenceState,
    ValidationCandidate,
    qualify_validation_portfolio,
)


def candidate_records() -> tuple[ValidationCandidate, ...]:
    """Return the source-bounded candidate records in stable identifier order."""

    return (
        ValidationCandidate(
            source_id="chang_2005_infrared_mapping",
            citation=(
                "Y. Chang et al., Composition and thickness distribution of "
                "HgCdTe molecular beam epitaxy wafers by infrared microscope "
                "mapping, Journal of Crystal Growth 277, 78-84 (2005)."
            ),
            doi="10.1016/j.jcrysgro.2005.01.051",
            record_scope="full text audited; published maps and summary statistics",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.ABSENT,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.NOT_APPLICABLE,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.CONFIRMED,
            uncertainty_characterized=EvidenceState.ABSENT,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.CONFIRMED,
            modality_count=1,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "The infrared microscope aperture was adjustable to approximately 25 micrometres at 10-micrometre wavelength.",
                "The published large-area maps used a 100-micrometre aperture for signal and acquisition-time reasons.",
                "No same-region aperture sweep, measured wavelength-dependent PSF, raw numerical map, repeat covariance, or variance-versus-scale curve was reported in the audited record.",
                "Published composition and thickness are model-conditioned transmission inversions, not direct microscopic composition measurements.",
            ),
        ),
        ValidationCandidate(
            source_id="furstenberg_2005_pl_transmission_mapping",
            citation=(
                "R. Furstenberg, J. O. White, and G. L. Olson, Spatially "
                "resolved photoluminescence and transmission spectra of "
                "HgCdTe, Journal of Electronic Materials 34, 791-794 (2005)."
            ),
            doi="10.1007/s11664-005-0022-8",
            record_scope="full text audited; published maps and summary statistics",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.CONFIRMED,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.CONFIRMED,
            thickness_characterized=EvidenceState.UNKNOWN,
            depth_model_declared=EvidenceState.ABSENT,
            uncertainty_characterized=EvidenceState.ABSENT,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.UNKNOWN,
            modality_count=2,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "PL and transmission were collected from the same location with representative 25-micrometre map resolution.",
                "The source explicitly reports excitation and collection dependence of PL observables and ambiguity between thickness, composition, and inclusions in transmission-derived optical path.",
                "No same-specimen spot-size sweep, measured excitation/collection PSF, raw registered arrays, or variance-versus-resolution curve was reported in the audited record.",
                "Two modalities at one lateral resolution do not constitute two probe scales.",
            ),
        ),
        ValidationCandidate(
            source_id="ruzhevich_2024_optical_microscopic_disorder",
            citation=(
                "M. S. Ruzhevich et al., Optical properties and disorder of "
                "HgCdTe films grown by molecular beam epitaxy, Journal of "
                "Optical Technology 91, 77-82 (2024)."
            ),
            doi="10.1364/JOT.91.000077; 10.17586/1023-5086-2024-91-02-23-33",
            record_scope="official abstract and bibliographic records; full text not retrieved",
            same_specimen=EvidenceState.UNKNOWN,
            same_spatial_region=EvidenceState.NOT_RETRIEVED,
            numerical_data_available=EvidenceState.NOT_RETRIEVED,
            independent_effective_scale_count=0,
            reusable_high_resolution_map=EvidenceState.NOT_RETRIEVED,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.NOT_RETRIEVED,
            spatial_registration=EvidenceState.NOT_RETRIEVED,
            thickness_characterized=EvidenceState.UNKNOWN,
            depth_model_declared=EvidenceState.UNKNOWN,
            uncertainty_characterized=EvidenceState.UNKNOWN,
            observable_defined=EvidenceState.UNKNOWN,
            preprocessing_declared=EvidenceState.NOT_RETRIEVED,
            modality_count=4,
            spatial_map_reported=EvidenceState.UNKNOWN,
            rendered_figure_available=EvidenceState.UNKNOWN,
            notes=(
                "The official abstract reports optical transmission, photoluminescence, scanning electron microscopy, and energy-dispersive X-ray spectroscopy.",
                "The abstract attributes x approximately 0.7 photoluminescence to carriers localized on large-scale composition fluctuations.",
                "The accessible record does not establish spatial resolution, registration, calibrated scale count, reusable numerical maps, PSF data, covariance, or a correlation-length statistic.",
                "Abstract-level evidence cannot be converted into a negative or positive spatial-kernel result.",
            ),
        ),
    )


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
        "schema_version": "1.0",
        "portfolio_contribution": "R04",
        "parent_issue": 196,
        "implementation_issue": 250,
        "status": portfolio.status,
        "direct_candidate_ids": list(portfolio.direct_candidate_ids),
        "qualification_classes": [
            "direct_multiresolution_validation",
            "single_scale_spatial_benchmark",
            "cross_modality_context",
            "source_bounded_figure_benchmark",
            "not_qualifiable_from_available_record",
        ],
        "direct_validation_requirements": [
            "same specimen and same spatial region",
            "three independently characterized effective scales or one reusable numerical high-resolution map filterable under three declared kernels",
            "original numerical arrays with coordinates",
            "measured or reconstructable kernel at every scale",
            "cross-scale spatial registration",
            "thickness and depth-weighting or absorption model",
            "observation uncertainty or covariance",
            "observable definition and preprocessing provenance",
        ],
        "candidates": [_jsonable(asdict(item)) for item in candidates],
        "qualifications": [
            _jsonable(asdict(item)) for item in portfolio.qualifications
        ],
        "minimum_next_action": list(portfolio.minimum_next_action),
        "headline": {
            "direct_validation_candidate_count": len(
                portfolio.direct_candidate_ids
            ),
            "decision": (
                "No audited candidate supplies a reusable numerical same-region "
                "dataset at three calibrated effective scales. R04 external "
                "validation is data-blocked, not analytically blocked."
            ),
            "minimum_author_or_experiment_request": [
                "raw numerical map or spectra with coordinates",
                "same region at three effective scales or one high-resolution map reusable under three declared kernels",
                "measured PSF/aperture/pixel/scan-bin kernels",
                "registration transform",
                "thickness and depth model",
                "repeat or covariance information",
                "observable and preprocessing definitions",
            ],
        },
        "claim_boundaries": [
            "Multiple modalities do not count as multiple probe scales.",
            "An adjustable aperture does not create a multiresolution dataset unless the same region is measured or reusable numerical data are supplied.",
            "Rendered map figures are not original numerical arrays and must not be represented as such.",
            "Source qualification does not infer a specimen point variance, correlation length, covariance family, or detector behavior.",
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
