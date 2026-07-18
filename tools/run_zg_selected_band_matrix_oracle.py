#!/usr/bin/env python3
"""Validate primitive eight-band reconstruction from synthetic ZG supercells."""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import fields
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from mct_research.kane8 import (
    ExtendedKaneParameters,
    hamiltonian_two_p,
    time_reversal_unitary,
)
from mct_research.thermal_kane import (
    ThermalParameterScale,
    fit_extended_kane_parameters,
    gamma_irrep_covariance_residual,
    thermal_extended_parameters,
)

Matrix = NDArray[np.complex128]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("ZG oracle contract must be a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_error(value: NDArray[Any], reference: NDArray[Any]) -> float:
    numerator = float(np.linalg.norm(np.asarray(value - reference).ravel()))
    denominator = max(float(np.linalg.norm(np.asarray(reference).ravel())), 1e-30)
    return numerator / denominator


def normalized_hermitian(rng: np.random.Generator, dimension: int) -> Matrix:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    matrix = 0.5 * (raw + raw.conjugate().T)
    return np.asarray(matrix / np.linalg.norm(matrix), dtype=np.complex128)


def random_unitary(rng: np.random.Generator, dimension: int) -> Matrix:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return np.asarray(q @ np.diag(phases.conjugate()), dtype=np.complex128)


def time_reverse(matrix: Matrix) -> Matrix:
    unitary = time_reversal_unitary()
    return np.asarray(unitary @ matrix.conjugate() @ unitary.conjugate().T)


def time_reversal_residual(matrix_plus: Matrix, matrix_minus: Matrix) -> float:
    return relative_error(matrix_plus, time_reverse(matrix_minus))


def project_gamma_irreps(matrix: Matrix) -> Matrix:
    candidate = np.asarray(matrix, dtype=np.complex128)
    if candidate.shape != (8, 8):
        raise ValueError("Gamma projection requires an 8x8 matrix")
    projected = np.zeros_like(candidate)
    for block in (slice(0, 2), slice(2, 6), slice(6, 8)):
        value = np.trace(candidate[block, block]).real / (block.stop - block.start)
        projected[block, block] = value * np.eye(block.stop - block.start)
    return projected


def randomize_degenerate_gauge(
    vectors: Matrix,
    eigenvalues: NDArray[np.float64],
    rng: np.random.Generator,
    tolerance_ev: float,
) -> Matrix:
    result = np.asarray(vectors, dtype=np.complex128).copy()
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while stop < len(eigenvalues) and abs(eigenvalues[stop] - eigenvalues[start]) <= tolerance_ev:
            stop += 1
        width = stop - start
        if width > 1:
            result[:, start:stop] = result[:, start:stop] @ random_unitary(rng, width)
        phases = np.exp(1j * rng.uniform(-np.pi, np.pi, width))
        result[:, start:stop] = result[:, start:stop] * phases[np.newaxis, :]
        start = stop
    return result


def primitive_reference(supercell_dimension: int, primitive_dimension: int) -> Matrix:
    if supercell_dimension < 2 * primitive_dimension:
        raise ValueError("synthetic supercell must contain a remote complement")
    reference = np.zeros((supercell_dimension, primitive_dimension), dtype=np.complex128)
    reference[:primitive_dimension, :] = np.eye(primitive_dimension)
    return reference


def simulate_supercell_eigenpairs(
    primitive_matrix: Matrix,
    *,
    rng: np.random.Generator,
    supercell_dimension: int,
    leakage_range: tuple[float, float],
    remote_energy_range: tuple[float, float],
    degeneracy_tolerance_ev: float,
) -> tuple[NDArray[np.float64], Matrix, Matrix]:
    dimension = primitive_matrix.shape[0]
    if supercell_dimension != 2 * dimension:
        raise ValueError("oracle currently requires one equal-size remote complement")
    eigenvalues, vectors = np.linalg.eigh(primitive_matrix)
    vectors = randomize_degenerate_gauge(
        vectors, eigenvalues, rng, degeneracy_tolerance_ev
    )
    remote_basis = random_unitary(rng, dimension)
    sine = rng.uniform(leakage_range[0], leakage_range[1], dimension)
    cosine = np.sqrt(1.0 - sine * sine)

    reference = primitive_reference(supercell_dimension, dimension)
    complement = np.zeros_like(reference)
    complement[dimension:, :] = np.eye(dimension)
    selected = (
        reference @ vectors @ np.diag(cosine)
        + complement @ remote_basis @ np.diag(sine)
    )
    remote = (
        -reference @ vectors @ np.diag(sine)
        + complement @ remote_basis @ np.diag(cosine)
    )
    full_vectors = np.column_stack((selected, remote))
    orthogonality = np.linalg.norm(
        full_vectors.conjugate().T @ full_vectors - np.eye(supercell_dimension)
    )
    if orthogonality > 1e-11:
        raise RuntimeError("synthetic supercell eigenvectors are not orthonormal")
    remote_energies = np.sort(
        rng.uniform(remote_energy_range[0], remote_energy_range[1], dimension)
    )
    full_energies = np.concatenate((eigenvalues, remote_energies))
    permutation = rng.permutation(supercell_dimension)
    return full_energies[permutation], full_vectors[:, permutation], reference


def reconstruct_selected_matrix(
    energies: NDArray[np.float64],
    eigenvectors: Matrix,
    reference: Matrix,
    primitive_dimension: int,
) -> tuple[Matrix, dict[str, float]]:
    projection = reference.conjugate().T @ eigenvectors
    weights = np.sum(np.abs(projection) ** 2, axis=0)
    selected_indices = np.argsort(weights)[-primitive_dimension:]
    selected_vectors = eigenvectors[:, selected_indices]
    selected_energies = energies[selected_indices]
    overlap = reference.conjugate().T @ selected_vectors
    left, singular_values, right_h = np.linalg.svd(overlap, full_matrices=False)
    polar = left @ right_h
    reconstructed = polar @ np.diag(selected_energies) @ polar.conjugate().T
    reconstructed = 0.5 * (reconstructed + reconstructed.conjugate().T)
    return np.asarray(reconstructed), {
        "minimum_selected_overlap_singular_value": float(singular_values.min()),
        "minimum_selected_reference_weight": float(weights[selected_indices].min()),
        "maximum_rejected_reference_weight": float(
            np.delete(weights, selected_indices).max()
        ),
    }


def parameter_dict(parameters: ExtendedKaneParameters) -> dict[str, float]:
    return {item.name: float(getattr(parameters, item.name)) for item in fields(parameters)}


def configuration_artifacts(
    *,
    rng: np.random.Generator,
    labels: list[str],
    pair_count: int,
    dimension: int,
    odd_scale: float,
    zero_mean_scale: float,
) -> tuple[dict[str, list[Matrix]], dict[str, list[Matrix]]]:
    odd: dict[str, list[Matrix]] = {}
    zero_mean: dict[str, list[Matrix]] = {}
    for label in labels:
        odd[label] = [odd_scale * normalized_hermitian(rng, dimension) for _ in range(pair_count)]
        first = [
            zero_mean_scale * normalized_hermitian(rng, dimension)
            for _ in range(pair_count - 1)
        ]
        last = -sum(first, np.zeros((dimension, dimension), dtype=np.complex128))
        zero_mean[label] = first + [last]
    return odd, zero_mean


def symmetry_artifacts(
    *,
    rng: np.random.Generator,
    labels: list[str],
    time_reversal_pairs: list[list[str]],
    dimension: int,
    scale: float,
) -> dict[str, Matrix]:
    artifacts = {
        label: np.zeros((dimension, dimension), dtype=np.complex128) for label in labels
    }
    gamma_raw = scale * normalized_hermitian(rng, dimension)
    artifacts["Gamma"] = gamma_raw - project_gamma_irreps(gamma_raw)
    for plus, minus in time_reversal_pairs:
        plus_artifact = scale * normalized_hermitian(rng, dimension)
        artifacts[plus] = plus_artifact
        artifacts[minus] = -time_reverse(plus_artifact)
    return artifacts


def restore_symmetry(
    matrices: dict[str, Matrix], time_reversal_pairs: list[list[str]]
) -> dict[str, Matrix]:
    restored = {label: matrix.copy() for label, matrix in matrices.items()}
    restored["Gamma"] = project_gamma_irreps(restored["Gamma"])
    for plus, minus in time_reversal_pairs:
        plus_matrix = matrices[plus]
        minus_matrix = matrices[minus]
        restored[plus] = 0.5 * (plus_matrix + time_reverse(minus_matrix))
        restored[minus] = 0.5 * (minus_matrix + time_reverse(plus_matrix))
    return restored


def symmetry_residual(
    matrices: dict[str, Matrix], time_reversal_pairs: list[list[str]]
) -> float:
    values = [gamma_irrep_covariance_residual(matrices["Gamma"])]
    values.extend(
        time_reversal_residual(matrices[plus], matrices[minus])
        for plus, minus in time_reversal_pairs
    )
    return max(values)


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("stage") != "zg_selected_band_matrix_reconstruction_oracle":
        raise ValueError("unexpected ZG reconstruction stage")
    model = contract["synthetic_model"]
    limits = contract["thresholds"]
    dimension = int(model["primitive_dimension"])
    supercell_dimension = int(model["supercell_dimension"])
    if dimension != 8:
        raise ValueError("oracle must exercise the eight-band primitive dimension")

    rng = np.random.default_rng(int(model["random_seed"]))
    base = ExtendedKaneParameters(**model["base_extended_kane_parameters"])
    scales = [ThermalParameterScale(**entry) for entry in model["thermal_scales"]]
    temperatures = [float(value) for value in model["temperatures_k"]]
    k_points = {
        label: np.asarray(value, dtype=float)
        for label, value in model["k_points_inverse_angstrom"].items()
    }
    labels = list(k_points)
    training_labels = list(model["training_labels"])
    holdout_labels = list(model["holdout_labels"])
    tr_pairs = [list(pair) for pair in model["time_reversal_pairs"]]
    pair_count = int(model["configuration_pair_count"])
    leakage_range = tuple(float(value) for value in model["selected_state_leakage_sine_range"])
    remote_range = tuple(float(value) for value in model["remote_energy_range_ev"])
    degeneracy_tolerance = float(model["degeneracy_tolerance_ev"])

    temperature_records: list[dict[str, Any]] = []
    global_reconstruction_errors: list[float] = []
    global_singular_values: list[float] = []
    global_unpaired_errors: list[float] = []
    global_paired_errors: list[float] = []
    global_pre_symmetry: list[float] = []
    global_post_symmetry: list[float] = []
    global_final_errors: list[float] = []
    global_parameter_errors: list[float] = []
    global_training_residuals: list[float] = []
    global_holdout_errors: list[float] = []
    global_naive_errors: list[float] = []

    for temperature in temperatures:
        target_parameters = thermal_extended_parameters(base, scales, temperature)
        targets = {
            label: hamiltonian_two_p(k_point, target_parameters)
            for label, k_point in k_points.items()
        }
        odd, zero_mean = configuration_artifacts(
            rng=rng,
            labels=labels,
            pair_count=pair_count,
            dimension=dimension,
            odd_scale=float(model["odd_displacement_artifact_scale_ev"]),
            zero_mean_scale=float(model["zero_mean_configuration_artifact_scale_ev"]),
        )
        symmetry = symmetry_artifacts(
            rng=rng,
            labels=labels,
            time_reversal_pairs=tr_pairs,
            dimension=dimension,
            scale=float(model["finite_supercell_symmetry_artifact_scale_ev"]),
        )

        pair_averages: dict[str, list[Matrix]] = {label: [] for label in labels}
        first_unpaired: dict[str, Matrix] = {}
        per_configuration_errors: list[float] = []
        minimum_singular = 1.0
        for label in labels:
            for config_index in range(pair_count):
                signed_matrices: list[Matrix] = []
                for sign in (+1.0, -1.0):
                    primitive_observation = (
                        targets[label]
                        + sign * odd[label][config_index]
                        + zero_mean[label][config_index]
                        + symmetry[label]
                    )
                    energies, vectors, reference = simulate_supercell_eigenpairs(
                        primitive_observation,
                        rng=rng,
                        supercell_dimension=supercell_dimension,
                        leakage_range=leakage_range,
                        remote_energy_range=remote_range,
                        degeneracy_tolerance_ev=degeneracy_tolerance,
                    )
                    reconstructed, diagnostics = reconstruct_selected_matrix(
                        energies, vectors, reference, dimension
                    )
                    per_configuration_errors.append(
                        relative_error(reconstructed, primitive_observation)
                    )
                    minimum_singular = min(
                        minimum_singular,
                        diagnostics["minimum_selected_overlap_singular_value"],
                    )
                    signed_matrices.append(reconstructed)
                    if config_index == 0 and sign > 0.0:
                        first_unpaired[label] = reconstructed
                pair_averages[label].append(0.5 * (signed_matrices[0] + signed_matrices[1]))

        raw_average = {
            label: sum(pair_averages[label], np.zeros((dimension, dimension), dtype=np.complex128))
            / pair_count
            for label in labels
        }
        restored = restore_symmetry(raw_average, tr_pairs)
        pre_symmetry = symmetry_residual(raw_average, tr_pairs)
        post_symmetry = symmetry_residual(restored, tr_pairs)
        unpaired_error = max(
            relative_error(first_unpaired[label], targets[label]) for label in labels
        )
        paired_error = max(
            relative_error(pair_averages[label][0], targets[label]) for label in labels
        )
        final_error = max(
            relative_error(restored[label], targets[label]) for label in labels
        )

        fitted, fit_diagnostics = fit_extended_kane_parameters(
            [k_points[label] for label in training_labels],
            [restored[label] for label in training_labels],
        )
        fitted_values = parameter_dict(fitted)
        target_values = parameter_dict(target_parameters)
        parameter_error = max(
            abs(fitted_values[name] - target_values[name]) for name in target_values
        )
        holdout_error = max(
            relative_error(
                hamiltonian_two_p(k_points[label], fitted), restored[label]
            )
            for label in holdout_labels
        )
        naive_matrices = {
            label: np.diag(np.linalg.eigvalsh(restored[label])).astype(np.complex128)
            for label in labels
        }
        naive_error = max(
            relative_error(naive_matrices[label], restored[label])
            for label in labels
            if label != "Gamma"
        )

        global_reconstruction_errors.append(max(per_configuration_errors))
        global_singular_values.append(minimum_singular)
        global_unpaired_errors.append(unpaired_error)
        global_paired_errors.append(paired_error)
        global_pre_symmetry.append(pre_symmetry)
        global_post_symmetry.append(post_symmetry)
        global_final_errors.append(final_error)
        global_parameter_errors.append(parameter_error)
        global_training_residuals.append(fit_diagnostics["relative_residual"])
        global_holdout_errors.append(holdout_error)
        global_naive_errors.append(naive_error)
        temperature_records.append(
            {
                "temperature_k": temperature,
                "target_parameters": target_values,
                "recovered_parameters": fitted_values,
                "minimum_selected_overlap_singular_value": minimum_singular,
                "maximum_per_configuration_reconstruction_relative_error": max(
                    per_configuration_errors
                ),
                "maximum_unpaired_configuration_relative_error": unpaired_error,
                "maximum_first_pair_relative_error": paired_error,
                "pre_restoration_symmetry_residual": pre_symmetry,
                "post_restoration_symmetry_residual": post_symmetry,
                "maximum_final_matrix_relative_error": final_error,
                "maximum_parameter_absolute_error": parameter_error,
                "training_fit_relative_residual": fit_diagnostics["relative_residual"],
                "maximum_holdout_matrix_relative_error": holdout_error,
                "maximum_naive_eigenvalue_only_matrix_relative_error": naive_error,
            }
        )

    metrics = {
        "minimum_selected_overlap_singular_value": min(global_singular_values),
        "maximum_per_configuration_reconstruction_relative_error": max(
            global_reconstruction_errors
        ),
        "minimum_unpaired_configuration_relative_error": min(global_unpaired_errors),
        "maximum_paired_configuration_relative_error": max(global_paired_errors),
        "minimum_pre_restoration_symmetry_residual": min(global_pre_symmetry),
        "maximum_post_restoration_symmetry_residual": max(global_post_symmetry),
        "maximum_final_matrix_relative_error": max(global_final_errors),
        "maximum_extended_parameter_absolute_error": max(global_parameter_errors),
        "maximum_training_fit_relative_residual": max(global_training_residuals),
        "maximum_holdout_matrix_relative_error": max(global_holdout_errors),
        "minimum_naive_eigenvalue_only_matrix_relative_error": min(global_naive_errors),
    }
    checks = {
        "selected_subspace_is_well_conditioned": metrics[
            "minimum_selected_overlap_singular_value"
        ]
        >= float(limits["minimum_selected_overlap_singular_value"]),
        "polar_reconstruction_recovers_each_configuration": metrics[
            "maximum_per_configuration_reconstruction_relative_error"
        ]
        <= float(limits["maximum_per_configuration_reconstruction_relative_error"]),
        "unpaired_special_displacement_is_rejected": metrics[
            "minimum_unpaired_configuration_relative_error"
        ]
        >= float(limits["minimum_unpaired_configuration_relative_error"]),
        "paired_configuration_is_bounded": metrics[
            "maximum_paired_configuration_relative_error"
        ]
        <= float(limits["maximum_paired_configuration_relative_error"]),
        "finite_supercell_symmetry_breaking_is_detected": metrics[
            "minimum_pre_restoration_symmetry_residual"
        ]
        >= float(limits["minimum_pre_restoration_symmetry_residual"]),
        "symmetry_restoration_closes": metrics[
            "maximum_post_restoration_symmetry_residual"
        ]
        <= float(limits["maximum_post_restoration_symmetry_residual"]),
        "final_primitive_matrix_is_recovered": metrics[
            "maximum_final_matrix_relative_error"
        ]
        <= float(limits["maximum_final_matrix_relative_error"]),
        "extended_parameters_are_recovered": metrics[
            "maximum_extended_parameter_absolute_error"
        ]
        <= float(limits["maximum_extended_parameter_absolute_error"]),
        "training_matrix_fit_closes": metrics[
            "maximum_training_fit_relative_residual"
        ]
        <= float(limits["maximum_training_fit_relative_residual"]),
        "unused_110_direction_is_predicted": metrics[
            "maximum_holdout_matrix_relative_error"
        ]
        <= float(limits["maximum_holdout_matrix_relative_error"]),
        "eigenvalue_only_reconstruction_is_rejected": metrics[
            "minimum_naive_eigenvalue_only_matrix_relative_error"
        ]
        >= float(limits["minimum_naive_eigenvalue_only_matrix_relative_error"]),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"ZG matrix reconstruction oracle failed: {failed}")

    return {
        "schema_version": "1.0",
        "status": "zg_selected_band_matrix_reconstruction_oracle_passed",
        "metrics": metrics,
        "checks": checks,
        "temperature_records": temperature_records,
        "decision": {
            "selected_band_supercell_reconstruction_ready": True,
            "displacement_pairing_required": True,
            "multiple_configuration_averaging_required": True,
            "Gamma_and_time_reversal_restoration_required": True,
            "eigenvalue_only_ZG_analysis_forbidden": True,
            "real_ZG_export_contract_design_authorized": True,
            "real_ZG_execution_authorized": False,
            "finite_size_polar_correction_ready": False,
            "configuration_count_stop_rule_ready": False,
            "automatic_additional_compute_authorized": False,
            "next_required_design": (
                "Define the real primitive/supercell overlap export, supercell-size and "
                "configuration-count convergence gates, and a polar finite-size correction "
                "before any ZG supercell calculation is authorized."
            ),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(
            "first_principles/matrix_oracle/zg_selected_band_matrix_reconstruction_contract.json"
        ),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(load_json(args.contract))
    result["input_sha256"] = {"contract": sha256(args.contract)}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
