#!/usr/bin/env python3
"""Validate long-range polar vertex subtraction and restoration on synthetic truth."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.complex128]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("contract must be a JSON object")
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


def dielectric_tensor(values: Any, name: str) -> NDArray[np.float64]:
    tensor = np.asarray(values, dtype=float)
    if tensor.shape != (3, 3):
        raise ValueError(f"{name} must be 3x3")
    if not np.allclose(tensor, tensor.T, atol=1e-14, rtol=0.0):
        raise ValueError(f"{name} must be symmetric")
    if float(np.linalg.eigvalsh(tensor).min()) <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return tensor


def long_range_vertex(
    q: NDArray[np.float64], strength: float, epsilon: NDArray[np.float64], template: Matrix
) -> Matrix:
    q = np.asarray(q, dtype=float)
    denominator2 = float(q @ epsilon @ q)
    if q.shape != (3,) or denominator2 <= 0.0:
        raise ValueError("long-range vertex requires a nonzero three-component q")
    return np.asarray(strength * template / np.sqrt(denominator2), dtype=np.complex128)


def short_range_vertex(q: NDArray[np.float64], terms: list[Matrix]) -> Matrix:
    if len(terms) != 4:
        raise ValueError("affine short-range model requires four coefficient matrices")
    row = np.concatenate(([1.0], np.asarray(q, dtype=float)))
    return np.asarray(sum(row[index] * terms[index] for index in range(4)))


def fit_short_range(q_points: NDArray[np.float64], matrices: NDArray[np.complex128]) -> Matrix:
    design = np.column_stack((np.ones(len(q_points)), q_points))
    if design.shape[1] != 4 or np.linalg.matrix_rank(design) != 4:
        raise ValueError("training q points do not identify an affine model")
    coefficients, _, _, _ = np.linalg.lstsq(
        design, matrices.reshape(len(q_points), -1), rcond=None
    )
    return np.asarray(coefficients, dtype=np.complex128)


def evaluate_fit(coefficients: Matrix, q: NDArray[np.float64], dimension: int) -> Matrix:
    row = np.concatenate(([1.0], np.asarray(q, dtype=float)))
    return np.asarray((row @ coefficients).reshape(dimension, dimension))


def fan(vertex: Matrix, denominator_ev: float) -> Matrix:
    if denominator_ev <= 0.0:
        raise ValueError("Fan denominator must be positive")
    return np.asarray(vertex @ vertex.conjugate().T / denominator_ev)


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("stage") != "polar_vertex_subtract_restore_oracle":
        raise ValueError("unexpected oracle stage")
    model = contract["synthetic_model"]
    limits = contract["thresholds"]
    dimension = int(model["matrix_dimension"])
    if dimension != 8:
        raise ValueError("oracle must use the eight-band dimension")

    rng = np.random.default_rng(int(model["random_seed"]))
    terms = [
        float(model["short_range_scale"]) * normalized_hermitian(rng, dimension)
    ] + [
        float(model["short_range_directional_scale"])
        * normalized_hermitian(rng, dimension)
        for _ in range(3)
    ]
    template = terms[0] / np.linalg.norm(terms[0]) + 0.2 * normalized_hermitian(
        rng, dimension
    )
    template = 0.5 * (template + template.conjugate().T)
    template = np.asarray(template / np.linalg.norm(template))

    source_epsilon = dielectric_tensor(
        model["source_dielectric_tensor"], "source dielectric tensor"
    )
    target_epsilon = dielectric_tensor(
        model["target_dielectric_tensor"], "target dielectric tensor"
    )
    source_strength = float(model["source_long_range_strength"])
    target_strength = float(model["target_long_range_strength"])
    denominator = float(model["fan_denominator_ev"])
    training_q = np.asarray(model["training_q_points"], dtype=float)
    holdout_q = np.asarray(model["holdout_q_points"], dtype=float)

    exact_short = np.asarray([short_range_vertex(q, terms) for q in training_q])
    source_full = np.asarray(
        [
            short_range_vertex(q, terms)
            + long_range_vertex(q, source_strength, source_epsilon, template)
            for q in training_q
        ]
    )
    extracted_short = np.asarray(
        [
            source_full[index]
            - long_range_vertex(q, source_strength, source_epsilon, template)
            for index, q in enumerate(training_q)
        ]
    )
    coefficients = fit_short_range(training_q, extracted_short)
    fitted_training = np.asarray(
        [evaluate_fit(coefficients, q, dimension) for q in training_q]
    )
    training_error = relative_error(fitted_training, exact_short)

    records: list[dict[str, Any]] = []
    vertex_errors: list[float] = []
    naive_errors: list[float] = []
    closure_errors: list[float] = []
    cross_errors: list[float] = []
    model_differences: list[float] = []

    for index, q in enumerate(holdout_q):
        short_exact = short_range_vertex(q, terms)
        short_fit = evaluate_fit(coefficients, q, dimension)
        source_long = long_range_vertex(q, source_strength, source_epsilon, template)
        target_long = long_range_vertex(q, target_strength, target_epsilon, template)
        target_truth = short_exact + target_long
        restored = short_fit + target_long
        naive = short_exact + source_long + target_long

        sigma_full = fan(restored, denominator)
        sigma_short = fan(short_fit, denominator)
        sigma_long = fan(target_long, denominator)
        sigma_cross = (
            short_fit @ target_long.conjugate().T
            + target_long @ short_fit.conjugate().T
        ) / denominator

        vertex_error = relative_error(restored, target_truth)
        naive_error = relative_error(naive, target_truth)
        closure_error = relative_error(
            sigma_short + sigma_long + sigma_cross, sigma_full
        )
        cross_error = relative_error(sigma_short + sigma_long, sigma_full)
        model_difference = relative_error(source_long, target_long)
        vertex_errors.append(vertex_error)
        naive_errors.append(naive_error)
        closure_errors.append(closure_error)
        cross_errors.append(cross_error)
        model_differences.append(model_difference)
        records.append(
            {
                "index": index,
                "q": q.tolist(),
                "target_vertex_relative_error": vertex_error,
                "naive_addition_relative_error": naive_error,
                "fan_decomposition_closure_relative_error": closure_error,
                "missing_cross_term_relative_error": cross_error,
                "source_target_long_range_relative_difference": model_difference,
            }
        )

    metrics = {
        "short_range_training_relative_error": training_error,
        "maximum_target_vertex_holdout_relative_error": max(vertex_errors),
        "minimum_naive_addition_relative_error": min(naive_errors),
        "maximum_fan_decomposition_closure_relative_error": max(closure_errors),
        "minimum_missing_cross_term_relative_error": min(cross_errors),
        "minimum_source_target_long_range_difference": min(model_differences),
    }
    checks = {
        "short_range_source_subtraction_and_fit": training_error
        <= float(limits["maximum_short_range_training_relative_error"]),
        "target_long_range_restoration_on_holdout": max(vertex_errors)
        <= float(limits["maximum_target_vertex_holdout_relative_error"]),
        "fan_component_closure_with_cross_term": max(closure_errors)
        <= float(limits["maximum_fan_decomposition_closure_relative_error"]),
        "naive_addition_detected_as_double_counting": min(naive_errors)
        >= float(limits["minimum_naive_addition_relative_error"]),
        "missing_cross_term_detected": min(cross_errors)
        >= float(limits["minimum_missing_cross_term_relative_error"]),
        "source_and_target_long_range_models_are_distinct": min(model_differences)
        >= float(limits["minimum_source_target_long_range_difference"]),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"polar vertex oracle failed: {failed}")

    return {
        "schema_version": "1.0",
        "status": "polar_vertex_subtract_restore_oracle_passed",
        "metrics": metrics,
        "checks": checks,
        "holdout_records": records,
        "decision": {
            "fan_vertex_subtract_restore_architecture_ready": True,
            "restore_at_vertex_level_before_self_energy": True,
            "direct_self_energy_component_replacement_forbidden": True,
            "short_range_long_range_cross_term_required": True,
            "debye_waller_path_ready": False,
            "real_source_long_range_model_selected": False,
            "real_target_long_range_model_selected": False,
            "real_A1_authorized": False,
            "automatic_additional_compute_authorized": False,
            "next_required_design": "Specify provenance-complete source and target long-range vertices, corrected electronic denominators, phonon-mode mapping, and a Debye-Waller no-double-counting construction.",
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(
            "first_principles/matrix_oracle/polar_vertex_decomposition_contract.json"
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
