#!/usr/bin/env python3
"""Validate polar electron-phonon vertex subtraction and restoration.

The oracle uses an exactly affine short-range Hermitian matrix vertex and two
distinct anisotropic long-range models. It verifies source subtraction,
short-range interpolation, target restoration, and Fan self-energy cross-term
preservation on q points not used for fitting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

ComplexMatrix = NDArray[np.complex128]
RealVector = NDArray[np.float64]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _normalized_hermitian(rng: np.random.Generator, dimension: int) -> ComplexMatrix:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    matrix = 0.5 * (raw + raw.conjugate().T)
    norm = np.linalg.norm(matrix, ord="fro")
    if norm == 0.0:
        raise RuntimeError("generated zero Hermitian matrix")
    return np.asarray(matrix / norm, dtype=np.complex128)


def _positive_definite_tensor(values: Any, name: str) -> NDArray[np.float64]:
    tensor = np.asarray(values, dtype=float)
    if tensor.shape != (3, 3):
        raise ValueError(f"{name} must have shape 3x3")
    if not np.allclose(tensor, tensor.T, atol=1e-14, rtol=0.0):
        raise ValueError(f"{name} must be symmetric")
    if float(np.linalg.eigvalsh(tensor).min()) <= 0.0:
        raise ValueError(f"{name} must be positive definite")
    return tensor


def long_range_vertex(
    q: RealVector,
    *,
    strength: float,
    dielectric_tensor: NDArray[np.float64],
    template: ComplexMatrix,
) -> ComplexMatrix:
    q = np.asarray(q, dtype=float)
    if q.shape != (3,):
        raise ValueError("q must contain three Cartesian components")
    denominator2 = float(q @ dielectric_tensor @ q)
    if denominator2 <= 0.0:
        raise ValueError("long-range vertex is undefined at q=0")
    return np.asarray(strength * template / np.sqrt(denominator2), dtype=np.complex128)


def short_range_vertex(
    q: RealVector,
    intercept: ComplexMatrix,
    directional: list[ComplexMatrix],
) -> ComplexMatrix:
    q = np.asarray(q, dtype=float)
    if q.shape != (3,) or len(directional) != 3:
        raise ValueError("short-range affine model requires a 3-vector and three slopes")
    result = intercept.copy()
    for index in range(3):
        result = result + q[index] * directional[index]
    return np.asarray(result, dtype=np.complex128)


def fit_affine_short_range(
    q_points: NDArray[np.float64], matrices: NDArray[np.complex128]
) -> NDArray[np.complex128]:
    if q_points.ndim != 2 or q_points.shape[1] != 3:
        raise ValueError("q_points must have shape (n, 3)")
    if matrices.ndim != 3 or matrices.shape[0] != q_points.shape[0]:
        raise ValueError("matrices must have shape (n, d, d)")
    design = np.column_stack((np.ones(q_points.shape[0]), q_points))
    if np.linalg.matrix_rank(design) != 4:
        raise ValueError("training q points do not identify an affine short-range model")
    coefficients, _, _, _ = np.linalg.lstsq(
        design, matrices.reshape(q_points.shape[0], -1), rcond=None
    )
    return np.asarray(coefficients, dtype=np.complex128)


def evaluate_affine(
    coefficients: NDArray[np.complex128], q: RealVector, dimension: int
) -> ComplexMatrix:
    row = np.concatenate(([1.0], np.asarray(q, dtype=float)))
    return np.asarray((row @ coefficients).reshape(dimension, dimension), dtype=np.complex128)


def _relative_error(value: ComplexMatrix, reference: ComplexMatrix) -> float:
    denominator = max(float(np.linalg.norm(reference, ord="fro")), 1e-30)
    return float(np.linalg.norm(value - reference, ord="fro") / denominator)


def fan_self_energy(vertex: ComplexMatrix, denominator_ev: float) -> ComplexMatrix:
    if denominator_ev <= 0.0:
        raise ValueError("synthetic Fan denominator must be positive")
    return np.asarray(vertex @ vertex.conjugate().T / denominator_ev, dtype=np.complex128)


def evaluate(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("stage") != "polar_vertex_subtract_restore_oracle":
        raise ValueError("unexpected polar-vertex oracle stage")

    model = contract["synthetic_model"]
    thresholds = contract["thresholds"]
    dimension = int(model["matrix_dimension"])
    if dimension != 8:
        raise ValueError("the oracle must exercise the declared eight-band matrix dimension")

    rng = np.random.default_rng(int(model["random_seed"]))
    short_scale = float(model["short_range_scale"])
    directional_scale = float(model["short_range_directional_scale"])
    intercept = short_scale * _normalized_hermitian(rng, dimension)
    directional = [
        directional_scale * _normalized_hermitian(rng, dimension) for _ in range(3)
    ]
    long_range_seed = intercept / np.linalg.norm(intercept, ord="fro")
    long_range_seed = long_range_seed + 0.2 * _normalized_hermitian(rng, dimension)
    long_range_template = 0.5 * (long_range_seed + long_range_seed.conjugate().T)
    long_range_template = long_range_template / np.linalg.norm(
        long_range_template, ord="fro"
    )

    source_epsilon = _positive_definite_tensor(
        model["source_dielectric_tensor"], "source dielectric tensor"
    )
    target_epsilon = _positive_definite_tensor(
        model["target_dielectric_tensor"], "target dielectric tensor"
    )
    source_strength = float(model["source_long_range_strength"])
    target_strength = float(model["target_long_range_strength"])
    training_q = np.asarray(model["training_q_points"], dtype=float)
    holdout_q = np.asarray(model["holdout_q_points"], dtype=float)
    denominator_ev = float(model["fan_denominator_ev"])

    full_source = []
    extracted_short = []
    exact_short = []
    for q in training_q:
        short = short_range_vertex(q, intercept, directional)
        source_long = long_range_vertex(
            q,
            strength=source_strength,
            dielectric_tensor=source_epsilon,
            template=long_range_template,
        )
        full = short + source_long
        full_source.append(full)
        extracted_short.append(full - source_long)
        exact_short.append(short)

    full_source_array = np.asarray(full_source, dtype=np.complex128)
    extracted_short_array = np.asarray(extracted_short, dtype=np.complex128)
    exact_short_array = np.asarray(exact_short, dtype=np.complex128)
    coefficients = fit_affine_short_range(training_q, extracted_short_array)
    fitted_training = np.asarray(
        [evaluate_affine(coefficients, q, dimension) for q in training_q]
    )
    training_error = _relative_error(fitted_training, exact_short_array)

    holdout_records: list[dict[str, Any]] = []
    target_vertex_errors: list[float] = []
    naive_errors: list[float] = []
    fan_closure_errors: list[float] = []
    missing_cross_errors: list[float] = []
    source_target_differences: list[float] = []

    for index, q in enumerate(holdout_q):
        exact_short_holdout = short_range_vertex(q, intercept, directional)
        fitted_short = evaluate_affine(coefficients, q, dimension)
        source_long = long_range_vertex(
            q,
            strength=source_strength,
            dielectric_tensor=source_epsilon,
            template=long_range_template,
        )
        target_long = long_range_vertex(
            q,
            strength=target_strength,
            dielectric_tensor=target_epsilon,
            template=long_range_template,
        )
        source_full = exact_short_holdout + source_long
        target_truth = exact_short_holdout + target_long
        restored_target = fitted_short + target_long
        naive_added = source_full + target_long

        target_error = _relative_error(restored_target, target_truth)
        naive_error = _relative_error(naive_added, target_truth)
        source_target_difference = _relative_error(source_long, target_long)

        sigma_full = fan_self_energy(restored_target, denominator_ev)
        sigma_short = fan_self_energy(fitted_short, denominator_ev)
        sigma_long = fan_self_energy(target_long, denominator_ev)
        sigma_cross = np.asarray(
            (
                fitted_short @ target_long.conjugate().T
                + target_long @ fitted_short.conjugate().T
            )
            / denominator_ev,
            dtype=np.complex128,
        )
        sigma_no_cross = sigma_short + sigma_long
        closure_error = _relative_error(sigma_short + sigma_long + sigma_cross, sigma_full)
        missing_cross_error = _relative_error(sigma_no_cross, sigma_full)

        target_vertex_errors.append(target_error)
        naive_errors.append(naive_error)
        fan_closure_errors.append(closure_error)
        missing_cross_errors.append(missing_cross_error)
        source_target_differences.append(source_target_difference)
        holdout_records.append(
            {
                "index": index,
                "q": q.tolist(),
                "target_vertex_relative_error": target_error,
                "naive_addition_relative_error": naive_error,
                "fan_decomposition_closure_relative_error": closure_error,
                "missing_cross_term_relative_error": missing_cross_error,
                "source_target_long_range_relative_difference": source_target_difference,
            }
        )

    metrics = {
        "short_range_training_relative_error": training_error,
        "maximum_target_vertex_holdout_relative_error": max(target_vertex_errors),
        "minimum_naive_addition_relative_error": min(naive_errors),
        "maximum_fan_decomposition_closure_relative_error": max(fan_closure_errors),
        "minimum_missing_cross_term_relative_error": min(missing_cross_errors),
        "minimum_source_target_long_range_difference": min(source_target_differences),
    }
    checks = {
        "short_range_source_subtraction_and_fit": training_error
        <= float(thresholds["maximum_short_range_training_relative_error"]),
        "target_long_range_restoration_on_holdout": max(target_vertex_errors)
        <= float(thresholds["maximum_target_vertex_holdout_relative_error"]),
        "fan_component_closure_with_cross_term": max(fan_closure_errors)
        <= float(thresholds["maximum_fan_decomposition_closure_relative_error"]),
        "naive_addition_detected_as_double_counting": min(naive_errors)
        >= float(thresholds["minimum_naive_addition_relative_error"]),
        "missing_cross_term_detected": min(missing_cross_errors)
        >= float(thresholds["minimum_missing_cross_term_relative_error"]),
        "source_and_target_long_range_models_are_distinct": min(source_target_differences)
        >= float(thresholds["minimum_source_target_long_range_difference"]),
    }
    passed = all(checks.values())
    if not passed:
        failed = [name for name, value in checks.items() if not value]
        raise RuntimeError(f"polar vertex decomposition oracle failed: {failed}")

    return {
        "schema_version": "1.0",
        "status": "polar_vertex_subtract_restore_oracle_passed",
        "metrics": metrics,
        "checks": checks,
        "holdout_records": holdout_records,
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
            "next_required_design": (
                "Specify provenance-complete source and target long-range vertices, "
                "corrected electronic denominators, phonon-mode mapping, and an explicit "
                "Debye-Waller no-double-counting construction before any real execution."
            ),
        },
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("first_principles/matrix_oracle/polar_vertex_decomposition_contract.json"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    contract = _load(args.contract)
    result = evaluate(contract)
    result["input_sha256"] = {"contract": _sha256(args.contract)}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
