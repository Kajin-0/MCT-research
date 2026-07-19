#!/usr/bin/env python3
"""Regenerate Hamiltonian statistics after the 128D-to-64D correction."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.kane8 import KaneParameters, hamiltonian
from mct_research.matrix_coordinates import (
    complex_vector,
    hermitian_covariance_to_legacy,
    hermitian_embedding,
    hermitian_matrix,
    hermitian_vector,
)
from mct_research.projection import (
    PARAMETER_NAMES,
    fit_parameters,
    parameter_templates,
)

K_POINTS = (
    (0.0, 0.0, 0.0),
    (0.008, 0.0, 0.0),
    (0.0, 0.009, 0.0),
    (0.0, 0.0, 0.010),
    (0.007, 0.006, 0.0),
    (0.006, 0.005, 0.004),
)
TRUE = KaneParameters(
    ev=-0.04,
    eg=0.18,
    delta=0.95,
    p=7.2,
    f=0.12,
    gamma1=3.4,
    gamma2=1.1,
    gamma3=1.5,
)


def _synthetic_matrices() -> list[np.ndarray]:
    rng = np.random.default_rng(20260719)
    matrices = []
    for index, k_point in enumerate(K_POINTS):
        coordinates = rng.normal(size=64)
        # Remove the component representable by a simple common energy offset and
        # vary the scale so the residual is deterministic but nonzero.
        coordinates[:8] -= np.mean(coordinates[:8])
        perturbation = hermitian_matrix((1.0 + 0.15 * index) * 2.0e-5 * coordinates)
        matrices.append(hamiltonian(k_point, TRUE) + perturbation)
    return matrices


def _systems(matrices: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    old_rows: list[np.ndarray] = []
    old_targets: list[np.ndarray] = []
    new_rows: list[np.ndarray] = []
    new_targets: list[np.ndarray] = []
    zero = KaneParameters()
    for k_point, matrix in zip(K_POINTS, matrices, strict=True):
        templates = parameter_templates(k_point)
        old_rows.append(
            np.column_stack([complex_vector(templates[name]) for name in PARAMETER_NAMES])
        )
        new_rows.append(
            np.column_stack([hermitian_vector(templates[name]) for name in PARAMETER_NAMES])
        )
        residual = matrix - hamiltonian(k_point, zero)
        old_targets.append(complex_vector(residual))
        new_targets.append(hermitian_vector(residual))
    return (
        np.vstack(old_rows),
        np.concatenate(old_targets),
        np.vstack(new_rows),
        np.concatenate(new_targets),
    )


def _legacy_unweighted(matrices: list[np.ndarray]) -> dict[str, Any]:
    old_design, old_target, _, _ = _systems(matrices)
    solution, _, rank, singular_values = np.linalg.lstsq(old_design, old_target, rcond=None)
    residual = old_target - old_design @ solution
    sse = float(residual @ residual)
    dof = old_design.shape[0] - rank
    inverse_normal = np.linalg.pinv(old_design.T @ old_design, hermitian=True)
    covariance = inverse_normal * (sse / dof)
    standard_errors = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    return {
        "parameters": dict(zip(PARAMETER_NAMES, solution.tolist(), strict=True)),
        "rank": int(rank),
        "observation_count": int(old_design.shape[0]),
        "degrees_of_freedom": int(dof),
        "chi_square_numeric_sse": sse,
        "reduced_chi_square": sse / dof,
        "variance_scale": sse / dof,
        "parameter_standard_errors": dict(
            zip(PARAMETER_NAMES, standard_errors.tolist(), strict=True)
        ),
        "condition_number": float(singular_values[0] / singular_values[-1]),
    }


def _current_unweighted(matrices: list[np.ndarray]) -> dict[str, Any]:
    fitted, diagnostics = fit_parameters(K_POINTS, matrices)
    return {
        "parameters": {name: float(getattr(fitted, name)) for name in PARAMETER_NAMES},
        "rank": int(diagnostics["rank"]),
        "observation_count": int(diagnostics["observation_count"]),
        "degrees_of_freedom": int(diagnostics["degrees_of_freedom"]),
        "chi_square_numeric_sse": float(diagnostics["chi_square"]),
        "reduced_chi_square": float(diagnostics["reduced_chi_square"]),
        "variance_scale": float(diagnostics["variance_scale"]),
        "parameter_standard_errors": {
            name: float(value)
            for name, value in diagnostics["parameter_standard_errors"].items()
        },
        "condition_number": float(diagnostics["condition_number"]),
        "coordinate_system": diagnostics["coordinate_system"],
    }


def _absolute_covariance_equivalence(matrices: list[np.ndarray]) -> dict[str, Any]:
    old_design, old_target, new_design, new_target = _systems(matrices)
    sigma = 3.0e-5
    covariance_64 = sigma**2 * np.eye(64)
    covariance_128 = hermitian_covariance_to_legacy(covariance_64)
    precision_128 = np.linalg.pinv(covariance_128, hermitian=True)

    old_normal = np.zeros((len(PARAMETER_NAMES), len(PARAMETER_NAMES)))
    old_rhs = np.zeros(len(PARAMETER_NAMES))
    old_chi_square = 0.0
    for index in range(len(K_POINTS)):
        old_slice = slice(128 * index, 128 * (index + 1))
        design = old_design[old_slice]
        target = old_target[old_slice]
        old_normal += design.T @ precision_128 @ design
        old_rhs += design.T @ precision_128 @ target
    old_solution = np.linalg.solve(old_normal, old_rhs)
    for index in range(len(K_POINTS)):
        old_slice = slice(128 * index, 128 * (index + 1))
        residual = old_target[old_slice] - old_design[old_slice] @ old_solution
        old_chi_square += float(residual @ precision_128 @ residual)
    old_parameter_covariance = np.linalg.inv(old_normal)

    fitted, diagnostics = fit_parameters(
        K_POINTS,
        matrices,
        covariances=[covariance_64 for _ in K_POINTS],
    )
    new_solution = np.asarray([getattr(fitted, name) for name in PARAMETER_NAMES])
    new_parameter_covariance = np.asarray(diagnostics["parameter_covariance"])

    embedding = hermitian_embedding()
    embedding_residual = float(np.linalg.norm(embedding.T @ embedding - np.eye(64)))
    return {
        "sigma_per_hermitian_coordinate": sigma,
        "legacy_covariance_rank": int(np.linalg.matrix_rank(covariance_128)),
        "legacy_covariance_dimension": 128,
        "current_covariance_dimension": 64,
        "embedding_orthonormality_residual": embedding_residual,
        "maximum_parameter_difference": float(np.max(np.abs(old_solution - new_solution))),
        "chi_square_difference": float(abs(old_chi_square - diagnostics["chi_square"])),
        "parameter_covariance_frobenius_difference": float(
            np.linalg.norm(old_parameter_covariance - new_parameter_covariance)
        ),
        "legacy_pseudoinverse_chi_square": old_chi_square,
        "current_64d_chi_square": float(diagnostics["chi_square"]),
        "current_degrees_of_freedom": int(diagnostics["degrees_of_freedom"]),
        "current_reduced_chi_square": float(diagnostics["reduced_chi_square"]),
        "interpretation": (
            "A physically embedded rank-64 legacy covariance is equivalent to the 64D "
            "covariance when treated with its Moore-Penrose pseudoinverse. The former "
            "eigenvalue-floor interpretation of the 64 null directions was not calibrated."
        ),
    }


def _inventory(path: str | Path) -> dict[str, Any]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("statistics inventory is empty")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["disposition"]] = counts.get(row["disposition"], 0) + 1
    affected = [row["artifact_or_path"] for row in rows if row["disposition"] == "regenerated"]
    return {"row_count": len(rows), "counts_by_disposition": counts, "regenerated": affected, "rows": rows}


def analyze(inventory_path: str | Path) -> dict[str, Any]:
    matrices = _synthetic_matrices()
    old = _legacy_unweighted(matrices)
    new = _current_unweighted(matrices)
    parameter_difference = max(
        abs(old["parameters"][name] - new["parameters"][name]) for name in PARAMETER_NAMES
    )
    sse_difference = abs(old["chi_square_numeric_sse"] - new["chi_square_numeric_sse"])
    dof_ratio = old["degrees_of_freedom"] / new["degrees_of_freedom"]
    se_ratios = {
        name: new["parameter_standard_errors"][name] / old["parameter_standard_errors"][name]
        for name in PARAMETER_NAMES
    }
    expected_se_ratio = float(np.sqrt(dof_ratio))
    maximum_se_ratio_error = max(abs(value - expected_se_ratio) for value in se_ratios.values())
    absolute = _absolute_covariance_equivalence(matrices)
    inventory = _inventory(inventory_path)

    checks = {
        "point_estimates_preserved": parameter_difference <= 1.0e-10,
        "numeric_sse_preserved": sse_difference <= 1.0e-18,
        "old_observation_count_is_128_per_matrix": old["observation_count"] == 128 * len(K_POINTS),
        "new_observation_count_is_64_per_matrix": new["observation_count"] == 64 * len(K_POINTS),
        "new_dof_is_64N_minus_rank": new["degrees_of_freedom"] == 64 * len(K_POINTS) - new["rank"],
        "variance_scaled_standard_error_ratio_matches_dof": maximum_se_ratio_error <= 1.0e-10,
        "embedded_absolute_covariance_preserves_parameters": absolute["maximum_parameter_difference"] <= 1.0e-10,
        "embedded_absolute_covariance_preserves_chi_square": absolute["chi_square_difference"] <= 1.0e-8,
        "embedded_absolute_covariance_preserves_parameter_covariance": absolute["parameter_covariance_frobenius_difference"] <= 1.0e-10,
        "no_committed_physical_statistics_require_value_replacement": inventory["counts_by_disposition"].get("regenerated", 0) == 2,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"64D statistics regeneration audit failed: {failed}")

    return {
        "schema_version": "1.0",
        "analysis": "Hamiltonian statistics regeneration after 64D migration",
        "synthetic_matrix_count": len(K_POINTS),
        "parameter_count": len(PARAMETER_NAMES),
        "legacy_unweighted": old,
        "current_unweighted": new,
        "comparison": {
            "maximum_parameter_difference": parameter_difference,
            "numeric_sse_difference": sse_difference,
            "legacy_to_current_dof_ratio": dof_ratio,
            "expected_current_to_legacy_standard_error_ratio": expected_se_ratio,
            "standard_error_ratios": se_ratios,
            "maximum_standard_error_ratio_error": maximum_se_ratio_error,
            "reduced_chi_square_ratio_current_to_legacy": new["reduced_chi_square"] / old["reduced_chi_square"],
        },
        "absolute_covariance_equivalence": absolute,
        "repository_inventory": inventory,
        "validation_checks": checks,
        "decision": {
            "deterministic_static_point_estimates_retain_validity": True,
            "deterministic_frobenius_residuals_retain_validity": True,
            "legacy_hamiltonian_dof_retain_validity": False,
            "legacy_variance_scaled_standard_errors_retain_validity": False,
            "committed_physical_hamiltonian_statistical_values_replaced": False,
            "reason": (
                "The current committed physical static records are deterministic matrix "
                "fits without calibrated Hamiltonian covariance. Only the runtime projection "
                "statistics API and its synthetic validation required regeneration."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory-csv", required=True)
    parser.add_argument("--output-json")
    args = parser.parse_args()
    result = analyze(args.inventory_csv)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
