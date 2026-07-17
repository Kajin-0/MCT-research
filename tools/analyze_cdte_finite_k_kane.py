#!/usr/bin/env python3
"""Reconstruct and gate the static CdTe finite-k Kane method smoke.

This tool consumes exact QE eigenvalues, the Wannier90 Gamma-star overlap file,
and the physical Gamma canonical intertwiners. It fixes only the remaining
discrete inter-irrep signs, applies two-radius matrix extrapolation, trains on
[001] and [111], and holds [110] out. The output is a method-smoke result, not a
converged CdTe parameter claim.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from cdte_finite_k_projection import (
    PARAMETER_GROUPS,
    _apply_signs,
    _coefficient_templates,
    _fit_group,
    _read_nnkp,
    _sha256,
    _validate_kpoint_contract,
    extract_coefficients,
    reconstruct_canonical_matrices,
)
from mct_research.kane8 import (
    ExtendedKaneParameters,
    KaneParameters,
    hamiltonian,
    hamiltonian_two_p,
    time_reversal_unitary,
)


def fit_taylor_model(
    gamma: np.ndarray,
    coefficients: dict[str, dict[str, Any]],
    training: list[str],
    *,
    two_p: bool,
) -> tuple[dict[str, float], dict[str, Any]]:
    parameter_type = ExtendedKaneParameters if two_p else KaneParameters
    model = hamiltonian_two_p if two_p else hamiltonian
    linear_names = PARAMETER_GROUPS["linear_two_p" if two_p else "linear_one_p"]

    zero_templates, zero_base = _coefficient_templates(
        np.asarray([0.0, 0.0, 1.0]),
        parameter_type,
        model,
        PARAMETER_GROUPS["zone_center"],
    )
    zone, zone_diag = _fit_group(
        [gamma],
        [
            {
                name: zero_templates[name][0]
                for name in PARAMETER_GROUPS["zone_center"]
            }
        ],
        [zero_base[0]],
        PARAMETER_GROUPS["zone_center"],
    )

    linear_observations = []
    linear_templates = []
    linear_base = []
    quadratic_observations = []
    quadratic_templates = []
    quadratic_base = []
    for name in training:
        direction = coefficients[name]["direction"]
        wanted = linear_names + PARAMETER_GROUPS["quadratic"]
        item, base = _coefficient_templates(direction, parameter_type, model, wanted)
        linear_observations.append(coefficients[name]["linear"])
        linear_templates.append({key: item[key][1] for key in linear_names})
        linear_base.append(base[1])
        quadratic_observations.append(coefficients[name]["quadratic"])
        quadratic_templates.append(
            {key: item[key][2] for key in PARAMETER_GROUPS["quadratic"]}
        )
        quadratic_base.append(base[2])
    linear, linear_diag = _fit_group(
        linear_observations, linear_templates, linear_base, linear_names
    )
    quadratic, quadratic_diag = _fit_group(
        quadratic_observations,
        quadratic_templates,
        quadratic_base,
        PARAMETER_GROUPS["quadratic"],
    )
    parameters = {**zone, **linear, **quadratic}
    return parameters, {
        "zone_center": zone_diag,
        "linear": linear_diag,
        "quadratic": quadratic_diag,
    }


def _parameter_object(parameters: dict[str, float], two_p: bool):
    return (
        ExtendedKaneParameters(**parameters)
        if two_p
        else KaneParameters(**parameters)
    )


def predict_coefficients(
    direction: np.ndarray, parameters: dict[str, float], two_p: bool
) -> tuple[np.ndarray, np.ndarray]:
    model = hamiltonian_two_p if two_p else hamiltonian
    params = _parameter_object(parameters, two_p)
    plus = model(direction, params)
    minus = model(-direction, params)
    gamma = model(np.zeros(3), params)
    return (
        0.5 * (plus - minus),
        0.5 * (plus + minus - 2.0 * gamma),
    )


def _holdout(
    coefficients: dict[str, dict[str, Any]],
    holdouts: list[str],
    parameters: dict[str, float],
    two_p: bool,
) -> dict[str, Any]:
    records = {}
    for name in holdouts:
        observed = coefficients[name]
        linear, quadratic = predict_coefficients(
            observed["direction"], parameters, two_p
        )
        linear_error = float(np.linalg.norm(observed["linear"] - linear))
        quadratic_error = float(np.linalg.norm(observed["quadratic"] - quadratic))
        records[name] = {
            "linear_absolute_error_ev_angstrom": linear_error,
            "linear_relative_error": linear_error
            / max(float(np.linalg.norm(observed["linear"])), np.finfo(float).eps),
            "quadratic_absolute_error_ev_angstrom2": quadratic_error,
            "quadratic_relative_error": quadratic_error
            / max(
                float(np.linalg.norm(observed["quadratic"])),
                np.finfo(float).eps,
            ),
            "linear_richardson_correction_ev_angstrom": observed[
                "linear_richardson_correction"
            ],
            "quadratic_richardson_correction_ev_angstrom2": observed[
                "quadratic_richardson_correction"
            ],
        }
    return records


def select_signs(
    matrices: list[np.ndarray],
    pairs: dict[str, dict[str, Any]],
    training: list[str],
) -> tuple[list[np.ndarray], dict[str, Any]]:
    candidates = []
    for gamma8 in (1, -1):
        for gamma7 in (1, -1):
            signed = _apply_signs(matrices, gamma8, gamma7)
            coefficients = extract_coefficients(signed, pairs)
            parameters, diagnostics = fit_taylor_model(
                signed[0], coefficients, training, two_p=True
            )
            candidates.append(
                {
                    "gamma8_sign": gamma8,
                    "gamma7_sign": gamma7,
                    "p8_ev_angstrom": parameters["p8"],
                    "p7_ev_angstrom": parameters["p7"],
                    "linear_relative_residual": diagnostics["linear"][
                        "relative_residual"
                    ],
                    "quadratic_relative_residual": diagnostics["quadratic"][
                        "relative_residual"
                    ],
                    "matrices": signed,
                }
            )
    positive = [
        item
        for item in candidates
        if item["p8_ev_angstrom"] > 0.0 and item["p7_ev_angstrom"] > 0.0
    ]
    if len(positive) != 1:
        raise RuntimeError(
            f"expected one P8>0, P7>0 sign convention, got {len(positive)}"
        )
    selected = positive[0]
    matrices = selected["matrices"]
    summary = [
        {key: value for key, value in item.items() if key != "matrices"}
        for item in candidates
    ]
    selected_summary = {
        key: value for key, value in selected.items() if key != "matrices"
    }
    return matrices, {"selected": selected_summary, "candidates": summary}


def analyze(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_result_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    basis = json.loads(Path(basis_result_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "cdte_static_finite_k_kane_method_smoke":
        raise ValueError("unexpected finite-k Kane smoke contract stage")
    if basis.get("upstream", {}).get("basis_convention") != "Novik_2005_Eq_4":
        raise ValueError("canonical basis result is not in the exact Novik convention")
    reduced, cartesian = _read_nnkp(nnkp_path)
    kpoint_diagnostics = _validate_kpoint_contract(cartesian, contract)
    matrices, reconstruction = reconstruct_canonical_matrices(
        mmn_path, eigenvalues, basis
    )
    minimum_overlap = min(
        item["minimum_overlap_singular_value"] for item in reconstruction
    )
    if minimum_overlap < float(
        contract["thresholds"]["minimum_overlap_singular_value"]
    ):
        raise RuntimeError("selected finite-k subspace fails the overlap closure gate")

    training = list(contract["training_directions"])
    holdouts = list(contract["holdout_directions"])
    signed, sign_result = select_signs(matrices, contract["pairs"], training)
    coefficients = extract_coefficients(signed, contract["pairs"])
    one_parameters, one_diagnostics = fit_taylor_model(
        signed[0], coefficients, training, two_p=False
    )
    two_parameters, two_diagnostics = fit_taylor_model(
        signed[0], coefficients, training, two_p=True
    )
    one_holdout = _holdout(coefficients, holdouts, one_parameters, False)
    two_holdout = _holdout(coefficients, holdouts, two_parameters, True)

    tr = time_reversal_unitary()
    pair_residuals = {}
    for name, spec in contract["pairs"].items():
        for scale in ("h", "h_over_2"):
            plus = int(spec[f"plus_{scale}"]) - 1
            minus = int(spec[f"minus_{scale}"]) - 1
            pair_residuals[f"{name}_{scale}"] = float(
                np.linalg.norm(
                    signed[plus]
                    - tr @ signed[minus].conj() @ tr.conj().T
                )
            )

    eta_p = 2.0 * abs(two_parameters["p8"] - two_parameters["p7"]) / (
        abs(two_parameters["p8"]) + abs(two_parameters["p7"])
    )
    maximum_linear_holdout = max(
        record["linear_relative_error"] for record in two_holdout.values()
    )
    maximum_quadratic_holdout = max(
        record["quadratic_relative_error"] for record in two_holdout.values()
    )
    thresholds = contract["thresholds"]
    if max(pair_residuals.values()) > float(
        thresholds["maximum_time_reversal_pair_residual_ev"]
    ):
        raise RuntimeError("canonical finite-k matrices fail time reversal")

    linear_training = float(two_diagnostics["linear"]["relative_residual"])
    quadratic_training = float(two_diagnostics["quadratic"]["relative_residual"])
    linear_passed = (
        linear_training
        <= float(thresholds["maximum_linear_training_relative_residual"])
        and maximum_linear_holdout
        <= float(thresholds["maximum_linear_holdout_relative_residual"])
    )
    quadratic_passed = (
        quadratic_training
        <= float(thresholds["maximum_quadratic_training_relative_residual"])
        and maximum_quadratic_holdout
        <= float(thresholds["maximum_quadratic_holdout_relative_residual"])
    )
    closure_passed = linear_passed and quadratic_passed
    one_linear = float(one_diagnostics["linear"]["relative_residual"])
    two_linear = float(two_diagnostics["linear"]["relative_residual"])
    one_to_two_improvement = one_linear / max(two_linear, np.finfo(float).eps)

    return {
        "schema_version": "1.0",
        "status": (
            "static_cdte_finite_k_kane_method_smoke_"
            "not_converged_material_parameters"
        ),
        "input_sha256": {
            "mmn": _sha256(mmn_path),
            "nnkp": _sha256(nnkp_path),
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "canonical_basis_result": _sha256(basis_result_path),
            "contract": _sha256(contract_path),
        },
        "k_points_reduced": reduced.tolist(),
        "k_points_cartesian_inverse_angstrom": cartesian.tolist(),
        "kpoint_contract_diagnostics": kpoint_diagnostics,
        "minimum_overlap_singular_value": minimum_overlap,
        "maximum_time_reversal_pair_residual_ev": max(pair_residuals.values()),
        "time_reversal_pair_residuals_ev": pair_residuals,
        "sign_convention": sign_result,
        "two_radius_corrections": {
            name: {
                key: value
                for key, value in record.items()
                if key.endswith("change") or key.endswith("correction")
            }
            for name, record in coefficients.items()
        },
        "one_p": {
            "parameters": one_parameters,
            "diagnostics": one_diagnostics,
            "heldout": one_holdout,
        },
        "two_p": {
            "parameters": two_parameters,
            "eta_p": eta_p,
            "diagnostics": two_diagnostics,
            "heldout": two_holdout,
        },
        "closure_decision": {
            "passed_declared_static_smoke_thresholds": closure_passed,
            "linear_two_p": {
                "passed": linear_passed,
                "training_relative_residual": linear_training,
                "maximum_holdout_relative_error": maximum_linear_holdout,
                "one_p_to_two_p_training_residual_ratio": one_to_two_improvement,
                "parameter_status": (
                    "static_method_smoke_supported_not_converged_material_values"
                    if linear_passed
                    else "rejected_at_declared_static_smoke_threshold"
                ),
            },
            "quadratic_conventional_kane": {
                "passed": quadratic_passed,
                "training_relative_residual": quadratic_training,
                "maximum_holdout_relative_error": maximum_quadratic_holdout,
                "parameter_status": (
                    "static_method_smoke_supported_not_converged_material_values"
                    if quadratic_passed
                    else "F_and_gamma_values_not_validated_by_matrix_closure"
                ),
            },
            "interpretation": (
                "The complete declared static two-P Kane manifold passes the "
                "training and unused [110] smoke gates."
                if closure_passed
                else "At least one Kane parameter block fails the declared "
                "matrix-closure gate. Retain passing blocks only as method-smoke "
                "estimates, reject failed parameter blocks, and do not increase "
                "computational depth automatically."
            ),
        },
        "reconstruction": reconstruction,
        "covariance_status": (
            "not_available_for_physical_parameter_uncertainty_in_this_static_smoke"
        ),
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmn", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--basis-result", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
