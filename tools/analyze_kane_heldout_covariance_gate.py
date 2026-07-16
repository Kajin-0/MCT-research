#!/usr/bin/env python3
"""Full-covariance held-out gate for the eight-parameter Kane projection.

This is a deterministic synthetic protocol check in normalized curvature units.
It is not a physical CdTe or HgCdTe result.
"""

from __future__ import annotations

import json
import math

import numpy as np

PARAMETERS = ("Eg", "Delta", "P8", "P7", "F", "gamma1", "gamma2", "gamma3")
TRUE = np.asarray([0.12, 0.95, 8.4, 7.9, -0.35, 4.3, 1.2, 1.55], dtype=float)

TRAIN_DESIGN = np.asarray(
    [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, 0, 0, 0, -1, -2, 0],
        [0, 0, 0, 0, 0, -1, 0, 2],
        [0, 0, 0, 0, 0, -1, 0, -2],
    ],
    dtype=float,
)


def training_covariance() -> np.ndarray:
    sigma = np.asarray([0.002, 0.004, 0.05, 0.05, 0.02, 0.03, 0.03, 0.03, 0.03])
    covariance = np.diag(sigma**2)
    covariance[5, 6] = covariance[6, 5] = 0.4 * sigma[5] * sigma[6]
    covariance[7, 8] = covariance[8, 7] = 0.4 * sigma[7] * sigma[8]
    for first in (5, 6):
        for second in (7, 8):
            covariance[first, second] = covariance[second, first] = 0.1 * sigma[first] * sigma[second]
    return covariance


def generalized_least_squares(
    design: np.ndarray, observations: np.ndarray, covariance: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    precision = np.linalg.inv(covariance)
    parameter_covariance = np.linalg.inv(design.T @ precision @ design)
    parameters = parameter_covariance @ design.T @ precision @ observations
    return parameters, parameter_covariance


def holdout_110(parameters: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gamma1, gamma2, gamma3 = parameters[5], parameters[6], parameters[7]
    splitting = math.sqrt(gamma2**2 + 3.0 * gamma3**2)
    prediction = np.asarray([-gamma1 + splitting, -gamma1 - splitting])

    jacobian = np.zeros((2, len(PARAMETERS)), dtype=float)
    jacobian[:, 5] = -1.0
    jacobian[0, 6] = gamma2 / splitting
    jacobian[1, 6] = -gamma2 / splitting
    jacobian[0, 7] = 3.0 * gamma3 / splitting
    jacobian[1, 7] = -3.0 * gamma3 / splitting
    return prediction, jacobian


def chi_square(residual: np.ndarray, covariance: np.ndarray) -> float:
    return float(residual.T @ np.linalg.inv(covariance) @ residual)


def analyze() -> dict[str, object]:
    train_covariance = training_covariance()
    train_observations = TRAIN_DESIGN @ TRUE
    fitted, fitted_covariance = generalized_least_squares(
        TRAIN_DESIGN, train_observations, train_covariance
    )

    prediction, jacobian = holdout_110(fitted)
    prediction_covariance = jacobian @ fitted_covariance @ jacobian.T
    holdout_measurement_covariance = np.asarray(
        [[0.03**2, 0.25 * 0.03**2], [0.25 * 0.03**2, 0.03**2]],
        dtype=float,
    )
    total_holdout_covariance = holdout_measurement_covariance + prediction_covariance

    compatible_observation = prediction + np.asarray([0.010, -0.008])
    incompatible_observation = prediction + np.asarray([0.120, -0.120])
    compatible_chi2 = chi_square(
        compatible_observation - prediction, total_holdout_covariance
    )
    incompatible_chi2 = chi_square(
        incompatible_observation - prediction, total_holdout_covariance
    )

    maximum_parameter_error = float(np.max(np.abs(fitted - TRUE)))
    parameter_sigma = np.sqrt(np.diag(fitted_covariance))
    holdout_sigma = np.sqrt(np.diag(total_holdout_covariance))

    if maximum_parameter_error > 1.0e-12:
        raise RuntimeError("GLS failed to recover the exact synthetic training model")
    if compatible_chi2 >= 5.991:
        raise RuntimeError("compatible two-dimensional holdout was incorrectly rejected")
    if incompatible_chi2 <= 5.991:
        raise RuntimeError("injected non-Kane holdout term was not rejected")

    return {
        "status": "analytical_protocol_only_not_physical_HgCdTe_data",
        "parameters": dict(zip(PARAMETERS, fitted.tolist(), strict=True)),
        "parameter_standard_deviations": dict(
            zip(PARAMETERS, parameter_sigma.tolist(), strict=True)
        ),
        "maximum_parameter_recovery_error": maximum_parameter_error,
        "training_rank": int(np.linalg.matrix_rank(TRAIN_DESIGN)),
        "training_rows": 9,
        "training_directions": ["Gamma", "[001]", "[111]"],
        "holdout_direction": "[110]",
        "holdout_prediction": prediction.tolist(),
        "holdout_total_standard_deviations": holdout_sigma.tolist(),
        "compatible_holdout_chi_square": compatible_chi2,
        "incompatible_holdout_chi_square": incompatible_chi2,
        "chi_square_95_percent_threshold_two_dof": 5.991,
        "decision": (
            "A training-perfect eight-parameter fit is insufficient. Propagate the "
            "full training covariance through the nonlinear [110] prediction, add "
            "the independent holdout covariance, and reject closure when the "
            "correlated holdout chi-square exceeds the predeclared threshold."
        ),
    }


def main() -> int:
    print(json.dumps(analyze(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
