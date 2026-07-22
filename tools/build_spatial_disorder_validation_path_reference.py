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
            source_id="aoki_2004_superlattice_microscopy",
            citation=(
                "T. Aoki et al., Microstructural Characterization of HgTe/HgCdTe "
                "Superlattices, Microscopy and Microanalysis 10(Suppl. 2), 48-49 (2004)."
            ),
            doi="10.1017/S1431927604882175",
            record_scope="full text supplied; published HREM and Z-contrast figures",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.UNKNOWN,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.UNKNOWN,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.NOT_APPLICABLE,
            uncertainty_characterized=EvidenceState.ABSENT,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.UNKNOWN,
            modality_count=2,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "HREM and Z-contrast report interface transition widths near 15 angstrom as grown and near 25 angstrom after 250 C annealing.",
                "The evidence concerns vertical superlattice-interface interdiffusion, not a lateral composition-covariance map.",
                "No original image arrays, transfer functions, registered multiscale observation, or uncertainty covariance are supplied.",
            ),
        ),
        ValidationCandidate(
            source_id="chang_2005_infrared_mapping",
            citation=(
                "Y. Chang et al., Composition and thickness distribution of "
                "HgCdTe molecular beam epitaxy wafers by infrared microscope "
                "mapping, Journal of Crystal Growth 277, 78-84 (2005)."
            ),
            doi="10.1016/j.jcrysgro.2005.01.051",
            record_scope="full text supplied; published maps and summary statistics",
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
                "No same-region aperture sweep, measured wavelength-dependent PSF, raw numerical map, repeat covariance, or variance-versus-scale curve was reported in the supplied record.",
                "Published composition and thickness are model-conditioned transmission inversions, not direct microscopic composition measurements.",
            ),
        ),
        ValidationCandidate(
            source_id="feldman_1991_mqw_chemical_mapping",
            citation=(
                "R. D. Feldman et al., HgCdTe/CdTe Multiple Quantum Wells: Growth, "
                "Stability, and Optical Properties, MRS Symposium Proceedings 216, 113-123 (1991)."
            ),
            doi="10.1557/PROC-216-113",
            record_scope="full text supplied; published TEM chemical-mapping and spectroscopy figures",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.UNKNOWN,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.UNKNOWN,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.NOT_APPLICABLE,
            uncertainty_characterized=EvidenceState.ABSENT,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.UNKNOWN,
            modality_count=2,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "Quantitative TEM chemical mapping is used to assess HgCdTe/CdTe multiple-quantum-well interdiffusion.",
                "The source is a microscopic vertical-interface benchmark, not a same-region lateral probe-scale sweep.",
                "No reusable numerical map, microscope transfer function, cross-scale registration, or map covariance is supplied.",
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
            record_scope="full text supplied; published maps and summary statistics",
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
                "The highest attainable resolution was reported as approximately 10 micrometres, but the published maps shown use 25 micrometres and do not form a same-region scale sweep.",
                "The source explicitly reports excitation and collection dependence of PL observables and ambiguity between thickness, composition, and inclusions in transmission-derived optical path.",
                "Two modalities or two temperatures at one lateral resolution do not constitute multiple probe scales.",
            ),
        ),
        ValidationCandidate(
            source_id="gopal_1992_two_beam_transmission",
            citation=(
                "V. Gopal, R. Ashokan, and V. Dhar, Compositional Characterization "
                "of HgCdTe Epilayers by Infrared Transmission, Infrared Physics 33, 39-45 (1992)."
            ),
            doi="10.1016/0020-0891(92)90053-V",
            record_scope="full text supplied; two rendered same-specimen transmission spectra",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.UNKNOWN,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=2,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.UNKNOWN,
            thickness_characterized=EvidenceState.UNKNOWN,
            depth_model_declared=EvidenceState.UNKNOWN,
            uncertainty_characterized=EvidenceState.ABSENT,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.CONFIRMED,
            modality_count=1,
            spatial_map_reported=EvidenceState.ABSENT,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "Sample 90239 was measured with nominal incident IR beam diameters of 3 mm and 250 micrometres.",
                "The published spectra shift relative to one another; the authors identify this as evidence of lateral composition nonuniformity.",
                "A second sample, 90211, showed no noticeable spectral change over the same beam-diameter change, providing a qualitative uniform-sample control.",
                "The source provides only two scales, rendered curves, nominal beam diameters rather than measured PSFs, no registered coordinates, no repeat covariance, and no third scale for covariance-family closure.",
            ),
        ),
        ValidationCandidate(
            source_id="jeoung_1996_bulk_transmission_calibration",
            citation=(
                "Y. Jeoung et al., New Method for the Estimation of Bulk HgCdTe "
                "Composition by Infrared Transmission, Infrared Physics and Technology 37, 445-450 (1996)."
            ),
            doi="10.1016/1350-4495(95)00125-5",
            record_scope="full text supplied; bulk transmission spectra and calibration table",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.NOT_APPLICABLE,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.NOT_APPLICABLE,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.CONFIRMED,
            uncertainty_characterized=EvidenceState.CONFIRMED,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.CONFIRMED,
            modality_count=1,
            spatial_map_reported=EvidenceState.ABSENT,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "The paper calibrates bulk composition from the 50 percent maximum-transmission wavenumber and specimen thickness.",
                "It reports composition accuracy near plus or minus 0.002 over the declared range but no spatial map or scale sweep.",
                "This is observation-model context, not external spatial-covariance validation.",
            ),
        ),
        ValidationCandidate(
            source_id="murakami_1992_mocvd_composition_profile",
            citation=(
                "S. Murakami et al., Compositional Profile of HgCdTe in a MOCVD "
                "System with Multinozzles, Journal of Crystal Growth 117, 33-36 (1992)."
            ),
            doi="10.1016/0022-0248(92)90712-R",
            record_scope="full text supplied; rendered EPMA line profiles and simulations",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.NOT_APPLICABLE,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.NOT_APPLICABLE,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.NOT_APPLICABLE,
            uncertainty_characterized=EvidenceState.CONFIRMED,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.UNKNOWN,
            modality_count=1,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "EPMA line profiles show composition versus wafer position for different nozzle and rotation conditions.",
                "The source reports EPMA composition accuracy within approximately 5 percent and a representative 7-micrometre epilayer thickness.",
                "Rendered profiles can support source-bounded large-scale-growth context but do not provide raw coordinates, probe kernels, or a same-region scale sweep.",
            ),
        ),
        ValidationCandidate(
            source_id="oda_1992_composition_method_comparison",
            citation=(
                "N. Oda et al., Composition Characterization Methods for HgCdTe "
                "Epilayers Grown by Molecular Beam Epitaxy, Journal of Crystal Growth 117, 193-196 (1992)."
            ),
            doi="10.1016/0022-0248(92)90743-3",
            record_scope="full text supplied; FTIR, EPMA, and photodiode method comparison",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.UNKNOWN,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.ABSENT,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.CONFIRMED,
            uncertainty_characterized=EvidenceState.CONFIRMED,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.CONFIRMED,
            modality_count=3,
            spatial_map_reported=EvidenceState.ABSENT,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "FTIR used a nominal 500-micrometre beam while EPMA used a 1-2-micrometre interaction region, and photodiode spectral response was measured at 77 K.",
                "The measurements compare composition-estimation methods across epilayers and devices, not registered maps of one spatial region.",
                "The reported plus or minus 0.002 method agreement does not constitute probe-scale variance data.",
            ),
        ),
        ValidationCandidate(
            source_id="parikh_1996_mombe_spatial_uniformity",
            citation=(
                "A. Parikh et al., Growth and Characterization of HgCdTe "
                "Heterostructures by Metalorganic Molecular Beam Epitaxy, "
                "Journal of Crystal Growth 159, 1152-1156 (1996)."
            ),
            doi="10.1016/0022-0248(95)00846-2",
            record_scope="full text supplied; rendered lateral map, summary statistics, and SIMS context",
            same_specimen=EvidenceState.CONFIRMED,
            same_spatial_region=EvidenceState.NOT_APPLICABLE,
            numerical_data_available=EvidenceState.ABSENT,
            independent_effective_scale_count=1,
            reusable_high_resolution_map=EvidenceState.ABSENT,
            declared_filterable_scale_count=0,
            kernel_characterized=EvidenceState.ABSENT,
            spatial_registration=EvidenceState.NOT_APPLICABLE,
            thickness_characterized=EvidenceState.CONFIRMED,
            depth_model_declared=EvidenceState.UNKNOWN,
            uncertainty_characterized=EvidenceState.CONFIRMED,
            observable_defined=EvidenceState.CONFIRMED,
            preprocessing_declared=EvidenceState.CONFIRMED,
            modality_count=2,
            spatial_map_reported=EvidenceState.CONFIRMED,
            rendered_figure_available=EvidenceState.CONFIRMED,
            notes=(
                "A rendered 15 by 15 mm lateral composition map reports mean x near 0.2270 and lateral standard deviation near 0.00053 across several samples.",
                "SIMS supplies vertical-composition context, but the lateral map grid, FTIR beam kernel, original arrays, and map covariance are not supplied.",
                "The source is useful for source-bounded uniformity magnitudes, not multiscale inversion.",
            ),
        ),
        ValidationCandidate(
            source_id="ruzhevich_2024_optical_microscopic_disorder",
            citation=(
                "M. S. Ruzhevich et al., Optical Properties and Disorder of "
                "HgCdTe Films Grown by Molecular Beam Epitaxy, Journal of "
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
        "schema_version": "1.1",
        "portfolio_contribution": "R04",
        "parent_issue": 196,
        "implementation_issues": [250, 272],
        "status": portfolio.status,
        "direct_candidate_ids": list(portfolio.direct_candidate_ids),
        "partial_multiresolution_candidate_ids": list(
            portfolio.partial_multiresolution_candidate_ids
        ),
        "qualification_classes": [
            "direct_multiresolution_validation",
            "partial_multiresolution_benchmark",
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
            "partial_multiresolution_candidate_count": len(
                portfolio.partial_multiresolution_candidate_ids
            ),
            "nearest_available_benchmark": "gopal_1992_two_beam_transmission",
            "nearest_benchmark_scale_diameters_micrometre": [3000.0, 250.0],
            "nearest_benchmark_scale_ratio": 12.0,
            "decision": (
                "Gopal 1992 supplies genuine two-scale same-specimen qualitative "
                "evidence of a transmission-edge change with probe diameter, but "
                "no candidate supplies a reusable numerical same-region dataset "
                "at three calibrated effective scales. R04 remains externally "
                "data-blocked, not analytically blocked."
            ),
            "minimum_data_upgrade_for_gopal_1992": [
                "original numerical wide- and focused-beam spectra",
                "coordinates proving the same sampled region",
                "measured or reconstructable beam kernels rather than nominal diameters alone",
                "specimen thickness and depth model for sample 90239",
                "repeat uncertainty or covariance",
                "a third calibrated scale for covariance-family closure",
            ],
        },
        "claim_boundaries": [
            "Two measured scales can establish qualitative scale dependence but cannot test covariance-family closure.",
            "Multiple modalities do not count as multiple probe scales.",
            "An adjustable aperture does not create a multiresolution dataset unless the same region is measured or reusable numerical data are supplied.",
            "Rendered spectra and map figures are not original numerical arrays and must not be represented as such.",
            "Nominal beam diameters are not measured point-spread functions.",
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
