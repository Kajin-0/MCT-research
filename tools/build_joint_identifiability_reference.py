"""Build the controlled R04 joint-identifiability reference record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from mct_research.spatial_disorder_instrument import CompositeInstrumentKernel
from mct_research.spatial_disorder_joint_identifiability import (
    JointIdentifiabilityScreen,
    ObservationOperatorSpecification,
    evaluate_observation_operator,
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


def _screen_record(screen: JointIdentifiabilityScreen) -> dict[str, object]:
    operator = evaluate_observation_operator(
        screen.reduced_gaussian_variances,
        screen.observation_specification,
    )
    results = []
    gaussian_distances = []
    for item in screen.results:
        if item.true_family == "gaussian":
            gaussian_distances.append(item.full_envelope.distance)
            continue
        results.append(
            {
                "true_family": item.true_family,
                "fitting_convention": item.fitting_convention,
                "fitted_point_variance": item.fitted_point_variance,
                "fitted_correlation_length": (
                    item.fitted_correlation_length
                ),
                "observation_only_distance": (
                    item.observation_only.distance
                ),
                "calibration_added_distance": (
                    item.calibration_added.distance
                ),
                "kernel_shape_added_distance": (
                    item.kernel_shape_added.distance
                ),
                "full_envelope_distance": (
                    item.full_envelope.distance
                ),
                "decision": item.decision,
            }
        )
    return {
        "observation_kind": screen.observation_specification.kind,
        "operator_log_variance_sensitivities": np.asarray(
            operator.log_variance_sensitivities
        ).tolist(),
        "operator_closure_log_shifts": np.asarray(
            operator.closure_log_shifts
        ).tolist(),
        "maximum_gaussian_self_distance": max(gaussian_distances),
        "convention_sensitive_families": list(
            screen.convention_sensitive_families
        ),
        "results": results,
    }


def _distance_range(
    screens: tuple[JointIdentifiabilityScreen, ...],
    family: str,
) -> list[float]:
    distances = [
        item.full_envelope.distance
        for screen in screens
        for item in screen.results
        if item.true_family == family
    ]
    return [min(distances), max(distances)]


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
    screens = (direct, transmission, cutoff)
    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 232,
        "portfolio_contribution": "R04",
        "status": (
            "controlled_joint_identifiability_not_specimen_inference"
        ),
        "model": {
            "lateral_covariance_families": [
                "Gaussian",
                "Matern nu=1/2",
                "Matern nu=3/2",
                "Matern nu=5/2",
            ],
            "depth_covariance": "common Gaussian finite-depth factor",
            "kernel_reduction": (
                "moment-matched Gaussian with exact composite-Gaussian "
                "shift retained as a systematic"
            ),
            "fitting_conventions": [
                "weighted log variance",
                "weighted reciprocal variance",
            ],
            "separation_metric": "rank-aware Mahalanobis distance",
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
            "log_variance": _screen_record(direct),
            "log_transmission_effective_absorption": (
                _screen_record(transmission)
            ),
            "log_cutoff_energy": _screen_record(cutoff),
        },
        "headline": {
            "matern_0.5_full_distance_range": _distance_range(
                screens, "matern_0.5"
            ),
            "matern_1.5_full_distance_range": _distance_range(
                screens, "matern_1.5"
            ),
            "matern_2.5_full_distance_range": _distance_range(
                screens, "matern_2.5"
            ),
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
            "The exact composite-kernel versus moment-matched Gaussian discrepancy is represented as a declared systematic direction.",
            "Rank-one systematic covariance terms are an envelope convention, not a unique probability model.",
            "Mahalanobis distance is a standardized design separation, not a posterior probability or discovery significance.",
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
