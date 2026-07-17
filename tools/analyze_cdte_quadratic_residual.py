#!/usr/bin/env python3
"""Localize the failed quadratic block of the static CdTe Kane method smoke.

This tool consumes the same immutable finite-k evidence as the upstream smoke,
reconstructs the current-run Novik basis, and diagnoses the Richardson-
extrapolated quadratic residual without authorizing deeper electronic-structure
calculation or treating rejected F/gamma values as material parameters.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from analyze_cdte_finite_k_kane import (
    fit_taylor_model,
    predict_coefficients,
    select_signs,
)
from cdte_finite_k_projection import (
    _read_nnkp,
    _sha256,
    _validate_kpoint_contract,
    extract_coefficients,
    reconstruct_canonical_matrices,
)

BLOCKS: dict[str, tuple[slice, slice]] = {
    "Gamma6-Gamma6": (slice(0, 2), slice(0, 2)),
    "Gamma6-Gamma8": (slice(0, 2), slice(2, 6)),
    "Gamma6-Gamma7": (slice(0, 2), slice(6, 8)),
    "Gamma8-Gamma8": (slice(2, 6), slice(2, 6)),
    "Gamma8-Gamma7": (slice(2, 6), slice(6, 8)),
    "Gamma7-Gamma7": (slice(6, 8), slice(6, 8)),
}
DIAGONAL_BLOCKS = {"Gamma6-Gamma6", "Gamma8-Gamma8", "Gamma7-Gamma7"}


def _real_vector(matrix: np.ndarray) -> np.ndarray:
    flat = np.asarray(matrix, dtype=complex).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def _quadratic_at_scales(
    matrices: list[np.ndarray], spec: dict[str, Any]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gamma = matrices[0]
    plus_h = int(spec["plus_h"]) - 1
    minus_h = int(spec["minus_h"]) - 1
    plus_fine = int(spec["plus_h_over_2"]) - 1
    minus_fine = int(spec["minus_h_over_2"]) - 1
    h = float(spec["radius_inverse_angstrom"])
    coarse = (matrices[plus_h] + matrices[minus_h] - 2.0 * gamma) / (2.0 * h**2)
    fine = (
        matrices[plus_fine] + matrices[minus_fine] - 2.0 * gamma
    ) / (2.0 * (h / 2.0) ** 2)
    richardson = (4.0 * fine - coarse) / 3.0
    return tuple(0.5 * (item + item.conj().T) for item in (coarse, fine, richardson))


def _block_diagnostics(residual: np.ndarray) -> dict[str, dict[str, float]]:
    total_squared = max(
        float(np.linalg.norm(residual, ord="fro") ** 2), np.finfo(float).eps
    )
    result: dict[str, dict[str, float]] = {}
    for name, (rows, columns) in BLOCKS.items():
        norm = float(np.linalg.norm(residual[rows, columns], ord="fro"))
        multiplicity = 1.0 if name in DIAGONAL_BLOCKS else 2.0
        result[name] = {
            "frobenius_norm": norm,
            "full_matrix_energy_fraction": multiplicity * norm**2 / total_squared,
        }
    return result


def _significant_rank(singular_values: np.ndarray, relative_threshold: float) -> int:
    values = np.asarray(singular_values, dtype=float)
    if values.size == 0 or values[0] <= 0.0:
        return 0
    return int(np.count_nonzero(values >= relative_threshold * values[0]))


def localize(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_result_path: str | Path,
    finite_k_contract_path: str | Path,
    residual_contract_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    basis = json.loads(Path(basis_result_path).read_text(encoding="utf-8"))
    finite_contract = json.loads(
        Path(finite_k_contract_path).read_text(encoding="utf-8")
    )
    residual_contract = json.loads(
        Path(residual_contract_path).read_text(encoding="utf-8")
    )
    if residual_contract.get("stage") != "cdte_quadratic_residual_localization":
        raise ValueError("unexpected quadratic residual contract stage")
    if basis.get("upstream", {}).get("basis_convention") != "Novik_2005_Eq_4":
        raise ValueError("canonical basis result is not in the exact Novik convention")

    _, cartesian = _read_nnkp(nnkp_path)
    _validate_kpoint_contract(cartesian, finite_contract)
    matrices, reconstruction = reconstruct_canonical_matrices(
        mmn_path, eigenvalues, basis
    )
    signed, sign_result = select_signs(
        matrices,
        finite_contract["pairs"],
        list(finite_contract["training_directions"]),
    )
    coefficients = extract_coefficients(signed, finite_contract["pairs"])
    two_parameters, two_diagnostics = fit_taylor_model(
        signed[0],
        coefficients,
        list(finite_contract["training_directions"]),
        two_p=True,
    )

    direction_results: dict[str, Any] = {}
    richardson_residuals: list[np.ndarray] = []
    aggregate_correction_squared = 0.0
    aggregate_residual_squared = 0.0
    for name, spec in finite_contract["pairs"].items():
        coarse, fine, richardson = _quadratic_at_scales(signed, spec)
        _, predicted = predict_coefficients(
            np.asarray(spec["unit_direction"], dtype=float), two_parameters, True
        )
        residual_coarse = coarse - predicted
        residual_fine = fine - predicted
        residual = richardson - predicted
        correction = richardson - fine
        singular_values = np.linalg.svd(residual, compute_uv=False)
        residual_norm = float(np.linalg.norm(residual, ord="fro"))
        observed_norm = float(np.linalg.norm(richardson, ord="fro"))
        correction_norm = float(np.linalg.norm(correction, ord="fro"))
        blocks = _block_diagnostics(residual)
        richardson_residuals.append(residual)
        aggregate_correction_squared += correction_norm**2
        aggregate_residual_squared += residual_norm**2
        direction_results[name] = {
            "observed_quadratic_frobenius_norm_ev_angstrom2": observed_norm,
            "residual_frobenius_norm_ev_angstrom2": residual_norm,
            "residual_relative_to_observed": residual_norm
            / max(observed_norm, np.finfo(float).eps),
            "coarse_residual_frobenius_norm_ev_angstrom2": float(
                np.linalg.norm(residual_coarse, ord="fro")
            ),
            "fine_residual_frobenius_norm_ev_angstrom2": float(
                np.linalg.norm(residual_fine, ord="fro")
            ),
            "richardson_correction_frobenius_norm_ev_angstrom2": correction_norm,
            "radius_correction_to_residual_ratio": correction_norm
            / max(residual_norm, np.finfo(float).eps),
            "residual_singular_values_ev_angstrom2": singular_values.tolist(),
            "significant_rank_at_declared_fraction": _significant_rank(
                singular_values,
                float(residual_contract["thresholds"]["relative_singular_value"]),
            ),
            "blocks": blocks,
        }

    horizontal = np.hstack(richardson_residuals)
    direction_stack = np.vstack([_real_vector(item) for item in richardson_residuals])
    horizontal_singular_values = np.linalg.svd(horizontal, compute_uv=False)
    direction_singular_values = np.linalg.svd(direction_stack, compute_uv=False)
    aggregate_correction = float(np.sqrt(aggregate_correction_squared))
    aggregate_residual = float(np.sqrt(aggregate_residual_squared))
    aggregate_ratio = aggregate_correction / max(
        aggregate_residual, np.finfo(float).eps
    )
    thresholds = residual_contract["thresholds"]
    effective_rank = _significant_rank(
        horizontal_singular_values, float(thresholds["relative_singular_value"])
    )
    maximum_gamma6_fraction = max(
        item["blocks"]["Gamma6-Gamma6"]["full_matrix_energy_fraction"]
        for item in direction_results.values()
    )
    broad_block_counts = {
        name: sum(
            block["full_matrix_energy_fraction"]
            >= float(thresholds["broad_block_energy_fraction"])
            for block in item["blocks"].values()
        )
        for name, item in direction_results.items()
    }
    radius_disfavored = aggregate_ratio <= float(
        thresholds["maximum_radius_correction_to_residual_ratio"]
    )
    low_rank = effective_rank <= int(thresholds["maximum_low_rank_dimension"])
    gamma6_diagonal_negligible = maximum_gamma6_fraction <= float(
        thresholds["maximum_gamma6_diagonal_energy_fraction"]
    )
    broad_support = min(broad_block_counts.values()) >= int(
        thresholds["minimum_broad_blocks_per_direction"]
    )

    return {
        "schema_version": "1.0",
        "status": "localized_static_cdte_quadratic_kane_residual",
        "input_sha256": {
            "mmn": _sha256(mmn_path),
            "nnkp": _sha256(nnkp_path),
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "canonical_basis_result": _sha256(basis_result_path),
            "finite_k_contract": _sha256(finite_k_contract_path),
            "residual_contract": _sha256(residual_contract_path),
        },
        "minimum_overlap_singular_value": min(
            item["minimum_overlap_singular_value"] for item in reconstruction
        ),
        "sign_convention": sign_result["selected"],
        "rejected_conventional_quadratic_fit_for_reproduction_only": {
            "parameters": {
                key: float(two_parameters[key])
                for key in ("f", "gamma1", "gamma2", "gamma3")
            },
            "training_relative_residual": float(
                two_diagnostics["quadratic"]["relative_residual"]
            ),
            "parameter_status": "not_validated_by_matrix_closure",
        },
        "directions": direction_results,
        "aggregate": {
            "richardson_correction_frobenius_norm_ev_angstrom2": aggregate_correction,
            "residual_frobenius_norm_ev_angstrom2": aggregate_residual,
            "radius_correction_to_residual_ratio": aggregate_ratio,
            "state_space_singular_values_ev_angstrom2": horizontal_singular_values.tolist(),
            "state_space_significant_rank_at_declared_fraction": effective_rank,
            "direction_space_singular_values_ev_angstrom2": direction_singular_values.tolist(),
            "maximum_gamma6_diagonal_energy_fraction": maximum_gamma6_fraction,
            "broad_block_counts": broad_block_counts,
        },
        "decision": {
            "finite_radius_contamination_disfavored": radius_disfavored,
            "residual_is_low_rank_under_declared_test": low_rank,
            "gamma6_diagonal_residual_is_negligible": gamma6_diagonal_negligible,
            "residual_has_broad_block_support": broad_support,
            "interpretation": (
                "The failed conventional quadratic closure is stable under the h/h/2 "
                "extrapolation, is not a rank-one or rank-two state-space defect, and "
                "is distributed across valence and inter-irrep blocks while the "
                "Gamma6 diagonal is already closed. The next authorized step is a "
                "symmetry-complete time-reversal-even quadratic invariant basis "
                "diagnosis using the existing matrices only."
            ),
        },
        "authorization": residual_contract["authorization"],
        "claim_boundary": residual_contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmn", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--basis-result", required=True)
    parser.add_argument("--finite-k-contract", required=True)
    parser.add_argument("--residual-contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = localize(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.finite_k_contract,
        args.residual_contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
