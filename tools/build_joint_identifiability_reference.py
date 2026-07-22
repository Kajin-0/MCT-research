"""Build the controlled R04 joint-identifiability reference record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from mct_research.spatial_disorder_instrument import CompositeInstrumentKernel
from mct_research.spatial_disorder_joint_identifiability import (
    FamilyConventionIdentifiability,
    JointIdentifiabilityScreen,
    ObservationOperatorSpecification,
    joint_identifiability_screen,
)


POINT_VARIANCE = 2.5e-5
LATERAL_CORRELATION_LENGTH = 2.0
DEPTH_CORRELATION_LENGTH = 2.0
KERNELS = (
    CompositeInstrumentKernel(0.2, 0.2, 0.4, 0.4, 0.5, 10.0),
    CompositeInstrumentKernel(1.0, 1.0, 2.0, 2.0, 0.5, 10.0),
    CompositeInstrumentKernel(4.0, 4.0, 8.0, 8.0, 0.5, 10.0),
)
INSTRUMENT_LOG_STANDARD_DEVIATIONS = np.array(
    [0.05, 0.05, 0.01, 0.01, 0.10, 0.05]
)
INSTRUMENT_LOG_COVARIANCE = np.diag(
    INSTRUMENT_LOG_STANDARD_DEVIATIONS**2
)
OBSERVATION_LOG_STANDARD_DEVIATIONS = np.array([0.03, 0.03, 0.03])


def _result(result: FamilyConventionIdentifiability) -> dict[str, object]:
    return {
        "true_family": result.true_family,
        "fitting_convention": result.fitting_convention,
        "fitted_point_variance": result.fitted_point_variance,
        "fitted_correlation_length": result.fitted_correlation_length,
        "log_observable_residuals": np.asarray(
            result.log_observable_residuals
        ).tolist(),
        "distances": {
            "observation_only": result.observation_only.distance,
            "calibration_added": result.calibration_added.distance,
            "kernel_shape_added": result.kernel_shape_added.distance,
            "full_envelope": result.full_envelope.distance,
        },
        "full_covariance_rank": result.full_envelope.rank,
        "full_covariance_condition_number": (
            result.full_envelope.condition_number
        ),
        "decision": result.decision,
    }


def _screen(screen: JointIdentifiabilityScreen) -> dict[str, object]:
    specification = screen.observation_specification
    gaussian_reference = next(
        item
        for item in screen.results
        if item.true_family == "gaussian"
        and item.fitting_convention == "log_variance"
    )
    operator_evaluation = {
        "log_variance_sensitivities": (
            np.asarray(
                screen.instrument_log_sensitivity
            ).shape[0]
            * [None]
        ),
        "closure_log_shifts": (
            np.asarray(
                gaussian_reference.true_log_observables
                - gaussian_reference.true_log_observables
            ).tolist()
        ),
    }
    if specification.kind in {
        "log_transmission_effective_absorption",
        "log_cutoff_energy",
    }:
        from mct_research.spatial_disorder_joint_identifiability import (
            evaluate_observation_operator,
        )

        evaluated = evaluate_observation_operator(
            screen.reduced_gaussian_variances,
            specification,
        )
        operator_evaluation = {
            "log_variance_sensitivities": np.asarray(
                evaluated.log_variance_sensitivities
            ).tolist(),
            "closure_log_shifts": np.asarray(
                evaluated.closure_log_shifts
            ).tolist(),
        }
    elif specification.kind == "log_variance":
        operator_evaluation = {
            "log_variance_sensitivities": [1.0, 1.0, 1.0],
            "closure_log_shifts": [0.0, 0.0, 0.0],
        }
    else:
        operator_evaluation = {
            "log_variance_sensitivities": [0.5, 0.5, 0.5],
            "closure_log_shifts": [0.0, 0.0, 0.0],
        }

    return {
        "observation_kind": specification.kind,
        "operator_evaluation_at_reduced_gaussian_reference": (
            operator_evaluation
        ),
        "convention_sensitive_families": list(
            screen.convention_sensitive_families
        ),
        "results": [_result(item) for item in screen.results],
    }


def _build_screen(
    specification: ObservationOperatorSpecification,
) -> JointIdentifiabilityScreen:
    return joint_identifiability_screen(
        point_variance=POINT_VARIANCE,
        lateral_correlation_length=LATERAL_CORRELATION_LENGTH,
        depth_correlation_length=DEPTH_CORRELATION_LENGTH,
        kernels=KERNELS,
        instrument_parameter_log_covariance=INSTRUMENT_LOG_COVARIANCE,
        observation_log_standard_deviations=(
            OBSERVATION_LOG_STANDARD_DEVIATIONS
        ),
        observation_specification=specification,
        threshold_distance=3.0,
        depth_quadrature_order=128,
    )


def build_reference() -> dict[str, object]:
    direct = _build_screen(
        ObservationOperatorSpecification(kind="log_variance")
    )
    transmission = _build_screen(
        ObservationOperatorSpecification(
            kind="log_transmission_effective_absorption",
            gap_slope_ev_per_fraction=1.2,
            mean_gap_ev=0.10,
            optical_thickness_cm=0.012,
            photon_energy_ev=0.115,
            exponent=0.5,
            amplitude_cm_inverse_ev_power=1800.0,
            quadrature_order=128,
        )
    )
    cutoff = _build_screen(
        ObservationOperatorSpecification(
            kind="log_cutoff_energy",
            gap_slope_ev_per_fraction=1.2,
            mean_gap_ev=0.10,
            optical_thickness_cm=0.015,
            target_response=0.35,
            lower_energy_ev=0.07,
            upper_energy_ev=0.14,
            exponent=0.0,
            amplitude_cm_inverse_ev_power=300.0,
            quadrature_order=128,
            absolute_tolerance_ev=1.0e-10,
        )
    )
    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 232,
        "portfolio_contribution": "R04",
        "status": (
            "controlled_joint_identifiability_not_specimen_inference"
        ),
        "model": {
            "alternative_lateral_families": [
                "Gaussian",
                "Matern nu=1/2",
                "Matern nu=3/2",
                "Matern nu=5/2",
            ],
            "depth_family": "common Gaussian finite-depth factor",
            "kernel_reduction": (
                "axiswise moment-matched Gaussian scale with exact "
                "composite-Gaussian discrepancy retained separately"
            ),
            "fitting_conventions": [
                "weighted log variance",
                "weighted reciprocal variance",
            ],
            "separation_metric": (
                "rank-aware Mahalanobis distance under staged covariance"
            ),
        },
        "design": {
            "point_variance": POINT_VARIANCE,
            "lateral_correlation_length": LATERAL_CORRELATION_LENGTH,
            "depth_correlation_length": DEPTH_CORRELATION_LENGTH,
            "equivalent_probe_sigmas": np.asarray(
                direct.equivalent_probe_sigmas
            ).tolist(),
            "depth_ratios": np.asarray(direct.depth_ratios).tolist(),
            "kernel_shape_log_shifts": np.asarray(
                direct.kernel_shape_log_shifts
            ).tolist(),
            "kernels": [
                {
                    "psf_sigma": item.psf_sigma_x,
                    "pixel_width": item.pixel_width_x,
                    "attenuation_coefficient": (
                        item.attenuation_coefficient
                    ),
                    "thickness": item.thickness,
                }
                for item in KERNELS
            ],
            "instrument_log_parameter_names": list(
                CompositeInstrumentKernel.log_parameter_names
            ),
            "instrument_log_standard_deviations": (
                INSTRUMENT_LOG_STANDARD_DEVIATIONS.tolist()
            ),
            "instrument_log_variance_covariance": np.asarray(
                direct.instrument_log_variance_covariance
            ).tolist(),
            "observation_log_standard_deviations": (
                OBSERVATION_LOG_STANDARD_DEVIATIONS.tolist()
            ),
            "threshold_distance": 3.0,
        },
        "screens": {
            "log_variance": _screen(direct),
            "log_transmission_effective_absorption": _screen(
                transmission
            ),
            "log_cutoff_energy": _screen(cutoff),
        },
        "headline": {
            "matern_0.5_full_distance_range": [
                min(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_0.5"
                ),
                max(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_0.5"
                ),
            ],
            "matern_1.5_full_distance_range": [
                min(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_1.5"
                ),
                max(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_1.5"
                ),
            ],
            "matern_2.5_full_distance_range": [
                min(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_2.5"
                ),
                max(
                    item.full_envelope.distance
                    for screen in (direct, transmission, cutoff)
                    for item in screen.results
                    if item.true_family == "matern_2.5"
                ),
            ],
            "classification": (
                "Matern nu=1/2 and nu=3/2 remain resolved under the "
                "full declared envelope; nu=5/2 is observation limited"
            ),
            "convention_sensitive_families": sorted(
                set(direct.convention_sensitive_families)
                | set(transmission.convention_sensitive_families)
                | set(cutoff.convention_sensitive_families)
            ),
        },
        "claim_boundaries": [
            "The alternative-family calculation uses supported lateral Matérn covariance with a common Gaussian finite-depth factor.",
            "The exact composite-kernel versus moment-matched Gaussian discrepancy is represented as a declared systematic direction, not hidden or discarded.",
            "Rank-one systematic covariance terms are a conservative envelope convention, not a unique probability model.",
            "Mahalanobis distance is a standardized design separation, not a posterior model probability or discovery significance.",
            "No specimen covariance family, point variance, correlation length, experimental validation, novelty claim, or manuscript authorization is established."
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
