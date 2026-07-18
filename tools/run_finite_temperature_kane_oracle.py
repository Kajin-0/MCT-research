#!/usr/bin/env python3
"""Run the deterministic finite-temperature Kane matrix falsification oracle."""
from __future__ import annotations

import argparse
from dataclasses import fields
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p
from mct_research.thermal_kane import (
    RationalSelfEnergy,
    ThermalParameterScale,
    bose_thermal_factor,
    fit_extended_kane_parameters,
    fit_fixed_bose_scales,
    fit_one_p_kane_parameters,
    gamma_irrep_covariance_residual,
    gamma_irrep_matrix,
    linear_self_energy_for_target,
    linearized_quasiparticle_hamiltonian,
    linearized_scalar_pole,
    signed_thermal_moments,
    solve_quasiparticle_pole,
    thermal_extended_parameters,
)


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parameter_dict(parameters: ExtendedKaneParameters) -> dict[str, float]:
    return {
        item.name: float(getattr(parameters, item.name))
        for item in fields(ExtendedKaneParameters)
    }


def _edge_energies(parameters: ExtendedKaneParameters) -> dict[str, float]:
    return {
        "Gamma6": float(parameters.ev + parameters.eg),
        "Gamma8": float(parameters.ev),
        "Gamma7": float(parameters.ev - parameters.delta),
    }


def _relative_matrix_error(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.linalg.norm(np.asarray(left) - np.asarray(right), ord="fro")
        / max(np.linalg.norm(np.asarray(right), ord="fro"), np.finfo(float).eps)
    )


def analyze(contract_path: str | Path) -> dict[str, Any]:
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "finite_temperature_kane_matrix_oracle":
        raise ValueError("unexpected finite-temperature oracle stage")
    if contract.get("material_status") != (
        "synthetic_method_oracle_not_a_cdte_or_hgcdte_prediction"
    ):
        raise ValueError("oracle must be explicitly synthetic")

    base = ExtendedKaneParameters(**contract["base_parameters"])
    scales = [
        ThermalParameterScale(
            theta_k=float(record["theta_k"]),
            shifts={name: float(value) for name, value in record["shifts"].items()},
        )
        for record in contract["thermal_parameter_scales"]
    ]
    temperatures = np.asarray(contract["temperature_grid_k"], dtype=float)
    k_points = [
        np.asarray(item, dtype=float)
        for item in contract["k_points_inverse_angstrom"]
    ]
    thresholds = contract["thresholds"]

    derivative_spec = contract["quasiparticle_linearization"][
        "sigma_derivative_irreps"
    ]
    sigma_derivative = gamma_irrep_matrix(
        derivative_spec["Gamma6"],
        derivative_spec["Gamma8"],
        derivative_spec["Gamma7"],
    )
    reference_ev = float(contract["quasiparticle_linearization"]["reference_ev"])

    base_matrices = [hamiltonian_two_p(k_point, base) for k_point in k_points]
    base_edges = _edge_energies(base)
    temperature_records: list[dict[str, Any]] = []
    maximum_gamma_symmetry_residual = 0.0
    maximum_matrix_linearization_error = 0.0
    maximum_parameter_error = 0.0
    maximum_two_p_residual = 0.0
    minimum_one_p_residual = float("inf")
    maximum_dynamical_pole_error = 0.0

    dynamical = contract["dynamical_pole_oracle"]
    coupling_theta = float(dynamical["thermal_coupling_theta_k"])
    coupling_weight = float(dynamical["thermal_coupling_weight"])
    remote_offset = float(dynamical["remote_offset_ev"])
    bracket_half_width = float(dynamical["bracket_half_width_ev"])

    for temperature in temperatures:
        target_parameters = thermal_extended_parameters(
            base, scales, float(temperature)
        )
        target_matrices = [
            hamiltonian_two_p(k_point, target_parameters) for k_point in k_points
        ]
        matrix_errors = []
        gamma_sigma0 = None
        gamma_metric: dict[str, float] | None = None
        for index, (bare_matrix, target_matrix) in enumerate(
            zip(base_matrices, target_matrices, strict=True)
        ):
            sigma0 = linear_self_energy_for_target(
                bare_matrix,
                target_matrix,
                sigma_derivative,
                reference_ev,
            )
            recovered, metric_diagnostics = linearized_quasiparticle_hamiltonian(
                bare_matrix,
                sigma0,
                sigma_derivative,
                reference_ev,
            )
            error = _relative_matrix_error(recovered, target_matrix)
            matrix_errors.append(error)
            maximum_matrix_linearization_error = max(
                maximum_matrix_linearization_error, error
            )
            if index == 0:
                gamma_sigma0 = sigma0
                gamma_residual = gamma_irrep_covariance_residual(sigma0)
                maximum_gamma_symmetry_residual = max(
                    maximum_gamma_symmetry_residual, gamma_residual
                )
                gamma_metric = metric_diagnostics
        if gamma_sigma0 is None or gamma_metric is None:
            raise RuntimeError("Gamma point is missing from the oracle k-point set")

        recovered_parameters, two_p_diagnostics = fit_extended_kane_parameters(
            k_points, target_matrices
        )
        _, one_p_diagnostics = fit_one_p_kane_parameters(k_points, target_matrices)
        target_values = _parameter_dict(target_parameters)
        recovered_values = _parameter_dict(recovered_parameters)
        parameter_errors = {
            name: abs(recovered_values[name] - target_values[name])
            for name in target_values
        }
        maximum_parameter_error = max(
            maximum_parameter_error, max(parameter_errors.values())
        )
        maximum_two_p_residual = max(
            maximum_two_p_residual, float(two_p_diagnostics["relative_residual"])
        )
        minimum_one_p_residual = min(
            minimum_one_p_residual, float(one_p_diagnostics["relative_residual"])
        )

        target_edges = _edge_energies(target_parameters)
        pole_records = {}
        coupling_factor = np.sqrt(
            1.0
            + coupling_weight
            * bose_thermal_factor(coupling_theta, float(temperature))
        )
        for irrep, model_spec in dynamical["irreps"].items():
            bare_edge = base_edges[irrep]
            edge_offset = target_edges[irrep] - bare_edge
            self_energy = RationalSelfEnergy(
                reference_ev=bare_edge,
                offset_ev=edge_offset,
                slope=float(model_spec["slope"]),
                coupling_ev=float(model_spec["coupling_ev"])
                * float(coupling_factor),
                remote_ev=bare_edge + remote_offset,
            )
            exact_pole = solve_quasiparticle_pole(
                bare_edge,
                self_energy,
                (
                    bare_edge - bracket_half_width,
                    bare_edge + bracket_half_width,
                ),
            )
            linearized_pole = linearized_scalar_pole(
                bare_edge, self_energy, bare_edge
            )
            pole_error = abs(linearized_pole - exact_pole)
            maximum_dynamical_pole_error = max(
                maximum_dynamical_pole_error, pole_error
            )
            pole_records[irrep] = {
                "bare_edge_ev": bare_edge,
                "thermal_edge_offset_ev": edge_offset,
                "remote_pole_ev": self_energy.remote_ev,
                "coupling_ev": self_energy.coupling_ev,
                "exact_quasiparticle_pole_ev": exact_pole,
                "linearized_quasiparticle_pole_ev": linearized_pole,
                "linearization_error_ev": pole_error,
                "quasiparticle_weight": float(
                    1.0 / (1.0 - self_energy.derivative(exact_pole))
                ),
            }

        temperature_records.append(
            {
                "temperature_k": float(temperature),
                "target_parameters": target_values,
                "recovered_parameters": recovered_values,
                "maximum_parameter_absolute_error": max(parameter_errors.values()),
                "eta_p": float(target_parameters.eta_p),
                "edge_energies_ev": target_edges,
                "gap_shift_mev": float(
                    1000.0 * (target_parameters.eg - base.eg)
                ),
                "matrix_linearization_maximum_relative_error": max(matrix_errors),
                "gamma_self_energy_symmetry_residual": gamma_irrep_covariance_residual(
                    gamma_sigma0
                ),
                "gamma_metric_diagnostics": gamma_metric,
                "two_p_matrix_fit": two_p_diagnostics,
                "one_p_matrix_fit": one_p_diagnostics,
                "dynamical_poles": pole_records,
            }
        )

    reduction = contract["thermal_reduction"]
    target_name = str(reduction["target_parameter"])
    target_shifts = np.asarray(
        [
            record["target_parameters"][target_name] - getattr(base, target_name)
            for record in temperature_records
        ],
        dtype=float,
    )
    training_indices = [
        int(value) for value in reduction["training_temperature_indices"]
    ]
    holdout_indices = [
        int(value) for value in reduction["holdout_temperature_indices"]
    ]
    one_scales = [float(value) for value in reduction["one_scale_theta_k"]]
    two_scales = [float(value) for value in reduction["two_scale_theta_k"]]
    one_amplitudes, one_prediction, one_diagnostics = fit_fixed_bose_scales(
        temperatures, target_shifts, one_scales, training_indices
    )
    two_amplitudes, two_prediction, two_diagnostics = fit_fixed_bose_scales(
        temperatures, target_shifts, two_scales, training_indices
    )
    one_holdout_errors_mev = 1000.0 * np.abs(
        one_prediction[holdout_indices] - target_shifts[holdout_indices]
    )
    two_holdout_errors_mev = 1000.0 * np.abs(
        two_prediction[holdout_indices] - target_shifts[holdout_indices]
    )
    one_holdout_max = float(one_holdout_errors_mev.max())
    two_holdout_max = float(two_holdout_errors_mev.max())
    numerical_sigma = float(reduction["numerical_standard_uncertainty_mev"])
    improvement_sigma = (one_holdout_max - two_holdout_max) / numerical_sigma
    target_maximum_index = int(np.argmax(target_shifts))
    turnover_detected = bool(
        0 < target_maximum_index < len(target_shifts) - 1
        and target_shifts[-1] < target_shifts[target_maximum_index]
    )

    checks = {
        "gamma_self_energy_symmetry": bool(
            maximum_gamma_symmetry_residual
            <= float(thresholds["maximum_gamma_symmetry_residual"])
        ),
        "matrix_quasiparticle_linearization": bool(
            maximum_matrix_linearization_error
            <= float(thresholds["maximum_matrix_linearization_relative_error"])
        ),
        "dynamical_pole_linearization": bool(
            maximum_dynamical_pole_error
            <= float(thresholds["maximum_dynamical_pole_linearization_error_ev"])
        ),
        "extended_parameter_recovery": bool(
            maximum_parameter_error
            <= float(thresholds["maximum_extended_parameter_absolute_error"])
        ),
        "two_p_matrix_closure": bool(
            maximum_two_p_residual
            <= float(thresholds["maximum_two_p_matrix_relative_residual"])
        ),
        "one_p_rejected": bool(
            minimum_one_p_residual
            >= float(thresholds["minimum_one_p_matrix_relative_residual"])
        ),
        "one_scale_heldout_failure": bool(
            one_holdout_max
            >= float(thresholds["minimum_one_scale_holdout_error_mev"])
        ),
        "two_scale_heldout_recovery": bool(
            two_holdout_max
            <= float(thresholds["maximum_two_scale_holdout_error_mev"])
        ),
        "second_scale_improvement": bool(
            improvement_sigma
            >= float(thresholds["minimum_second_scale_improvement_sigma"])
        ),
        "signed_gap_turnover_detected": turnover_detected,
    }
    passed = all(checks.values())
    if not passed:
        failed = [name for name, value in checks.items() if not value]
        raise RuntimeError(f"finite-temperature matrix oracle failed: {failed}")

    return {
        "schema_version": "1.0",
        "status": "finite_temperature_kane_matrix_oracle_passed",
        "input_sha256": {"contract": _sha256(contract_path)},
        "material_status": contract["material_status"],
        "base_parameters": _parameter_dict(base),
        "temperature_records": temperature_records,
        "aggregate_diagnostics": {
            "maximum_gamma_self_energy_symmetry_residual": maximum_gamma_symmetry_residual,
            "maximum_matrix_linearization_relative_error": maximum_matrix_linearization_error,
            "maximum_dynamical_pole_linearization_error_ev": maximum_dynamical_pole_error,
            "maximum_extended_parameter_absolute_error": maximum_parameter_error,
            "maximum_two_p_matrix_relative_residual": maximum_two_p_residual,
            "minimum_one_p_matrix_relative_residual": minimum_one_p_residual,
        },
        "thermal_reduction": {
            "target_parameter": target_name,
            "temperatures_k": temperatures.tolist(),
            "target_shifts_mev": (1000.0 * target_shifts).tolist(),
            "training_indices": training_indices,
            "holdout_indices": holdout_indices,
            "one_scale": {
                "theta_k": one_scales,
                "amplitudes_ev": one_amplitudes.tolist(),
                "prediction_mev": (1000.0 * one_prediction).tolist(),
                "holdout_absolute_errors_mev": one_holdout_errors_mev.tolist(),
                "maximum_holdout_absolute_error_mev": one_holdout_max,
                "diagnostics": one_diagnostics,
                "signed_moments": signed_thermal_moments(
                    one_amplitudes, one_scales
                ),
            },
            "two_scale": {
                "theta_k": two_scales,
                "amplitudes_ev": two_amplitudes.tolist(),
                "prediction_mev": (1000.0 * two_prediction).tolist(),
                "holdout_absolute_errors_mev": two_holdout_errors_mev.tolist(),
                "maximum_holdout_absolute_error_mev": two_holdout_max,
                "diagnostics": two_diagnostics,
                "signed_moments": signed_thermal_moments(
                    two_amplitudes, two_scales
                ),
            },
            "second_scale_improvement_sigma": float(improvement_sigma),
            "turnover_detected": turnover_detected,
            "turnover_temperature_k": float(temperatures[target_maximum_index]),
        },
        "checks": checks,
        "decision": {
            "passed": passed,
            "matrix_pipeline_ready_for_real_input": True,
            "a1_electron_phonon_authorized": False,
            "interpretation": (
                "The synthetic oracle validates symmetry reduction, dynamical and "
                "linearized quasiparticle poles, full matrix parameter recovery, "
                "one-/two-P discrimination, and held-out thermal reduction. A real "
                "A1 calculation remains separately blocked by physical-response and "
                "execution gates."
            ),
            "next_authorized_task": (
                "Define the smallest real-input A1 export and physical sanity gates "
                "needed to populate this validated matrix pipeline."
            ),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.contract)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
