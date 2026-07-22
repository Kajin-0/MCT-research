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
    SeparationStage,
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


def _stage(stage: SeparationStage) -> dict[str, object]:
    return {
        "squared_distance": stage.squared_distance,
        "distance": stage.distance,
        "rank": stage.rank,
        "condition_number": stage.condition_number,
        "covariance": np.asarray(stage.covariance).tolist(),
    }


def _result(result: FamilyConventionIdentifiability) -> dict[str, object]:
    return {
        "true_family": result.true_family,
        "true_matern_smoothness": result.true_matern_smoothness,
        "fitting_convention": result.fitting_convention,
        "true_variances": np.asarray(result.true_variances).tolist(),
        "fitted_variances": np.asarray(result.fitted_variances).tolist(),
        "fitted_point_variance": result.fitted_point_variance,
        "fitted_correlation_length": result.fitted_correlation_length,
        "true_log_observables": np.asarray(
            result.true_log_observables
        ).tolist(),
        "fitted_log_observables": np.asarray(
            result.fitted_log_observables
        ).tolist(),
        "log_observable_residuals": np.asarray(
            result.log_observable_residuals
        ).tolist(),
        "observation_only": _stage(result.observation_only),
        "calibration_added": _stage(result.calibration_added),
        "kernel_shape_added": _stage(result.kernel_shape_added),
        "full_envelope": _stage(result.full_envelope),
        "threshold_distance": result.threshold_distance,
        "decision": result.decision,
    }


def _screen(screen: JointIdentifiabilityScreen) -> dict[str, object]:
    specification = screen.observation_specification
    return {
        "observation_kind": specification.kind,
        "observation_specification": {
            "gap_slope_ev_per_fraction": specification.gap_slope_ev_per_fraction,
            "mean_gap_ev": specification.mean_gap_ev,
            "optical_thickness_cm": specification.optical_thickness_cm,
            "photon_energy_ev": specification.photon_energy_ev,
            "target_response": specification.target_response,
            "lower_energy_ev": specification.lower_energy_ev,
            "upper_energy_ev": specification.upper_energy_ev,
            "exponent": specification.exponent,
            "amplitude_cm_inverse_ev_power": (
                specification.amplitude_cm_inverse_ev_power
            ),
            "quadrature_order": specification.quadrature_order,
            "standard_deviation_limit": (
                specification.standard_deviation_limit
            ),
            "absolute_tolerance_ev": specification.absolute_tolerance_ev,
            "response_tolerance": specification.response_tolerance,
            "log_derivative_step": specification.log_derivative_step,
        },
        "equivalent_probe_sigmas": np.asarray(
            screen.equivalent_probe_sigmas
        ).tolist(),
        "depth_ratios": np.asarray(screen.depth_ratios).tolist(),
        "exact_gaussian_variances": np.asarray(
            screen.exact_gaussian_variances
        ).tolist(),
        "reduced_gaussian_variances": np.asarray(
            screen.reduced_gaussian_variances
        ).tolist(),
        "kernel_shape_log_shifts": np.asarray(
            screen.kernel_shape_log_shifts
        ).tolist(),
        "instrument_log_sensitivity": np.asarray(
            screen.instrument_log_sensitivity
        ).tolist(),
        "instrument_log_variance_covariance": np.asarray(
            screen.instrument_log_variance_covariance
        ).tolist(),
        "observation_log_standard_deviations": np.asarray(
            screen.observation_log_standard_deviations
        ).tolist(),
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
        "design": {
            "point_variance": POINT_VARIANCE,
            "lateral_correlation_length": LATERAL_CORRELATION_LENGTH,
            "depth_correlation_length": DEPTH_CORRELATION_LENGTH,
            "kernels": [
                {
                    "psf_sigma_x": item.psf_sigma_x,
                    "psf_sigma_y": item.psf_sigma_y,
                    "pixel_width_x": item.pixel_width_x,
                    "pixel_width_y": item.pixel_width_y,
                    "attenuation_coefficient": (
                        item.attenuation_coefficient
                    ),
                    "thickness": item.thickness,
                    "side": item.side,
                }
                for item in KERNELS
            ],
            "instrument_log_parameter_names": list(
                CompositeInstrumentKernel.log_parameter_names
            ),
            "instrument_log_standard_deviations": (
                INSTRUMENT_LOG_STANDARD_DEVIATIONS.tolist()
            ),
            "instrument_log_covariance": (
                INSTRUMENT_LOG_COVARIANCE.tolist()
            ),
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
