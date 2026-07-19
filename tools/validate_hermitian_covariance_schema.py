#!/usr/bin/env python3
"""Validate the independent-Hermitian covariance coordinate schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.dataio import COVARIANCE_COORDINATE_SYSTEM, SCHEMA_VERSION
from mct_research.hermitian import (
    LEGACY_COMPLEX_CARTESIAN_DIMENSION,
    OBSERVATION_DIMENSION,
    hermitian_linear_map,
    hermitian_vector,
    legacy_covariance_to_hermitian,
    matrix_from_hermitian_vector,
)


def _random_hermitian(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    return 0.5 * (raw + raw.conjugate().T)


def _random_unitary(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    phases = np.where(np.abs(diagonal) > 0.0, diagonal / np.abs(diagonal), 1.0)
    return q @ np.diag(np.conjugate(phases))


def analyze() -> dict[str, Any]:
    rng = np.random.default_rng(6408)
    first = _random_hermitian(rng)
    second = _random_hermitian(rng)
    first_vector = hermitian_vector(first)
    second_vector = hermitian_vector(second)
    reconstructed = matrix_from_hermitian_vector(first_vector)

    matrix_inner_product = float(np.trace(first.conjugate().T @ second).real)
    vector_inner_product = float(first_vector @ second_vector)

    unitary = _random_unitary(rng)
    mapping = hermitian_linear_map(
        lambda matrix: unitary.conjugate().T @ matrix @ unitary
    )
    orthogonality = mapping.T @ mapping - np.eye(OBSERVATION_DIMENSION)

    migrated_identity = legacy_covariance_to_hermitian(
        np.eye(LEGACY_COMPLEX_CARTESIAN_DIMENSION)
    )

    result = {
        "schema_version": SCHEMA_VERSION,
        "covariance_coordinate_system": COVARIANCE_COORDINATE_SYSTEM,
        "matrix_dimension": 8,
        "legacy_dimension": LEGACY_COMPLEX_CARTESIAN_DIMENSION,
        "independent_dimension": OBSERVATION_DIMENSION,
        "roundtrip_max_abs": float(np.max(np.abs(reconstructed - first))),
        "frobenius_inner_product_abs_error": abs(
            vector_inner_product - matrix_inner_product
        ),
        "unitary_map_orthogonality_frobenius": float(
            np.linalg.norm(orthogonality, ord="fro")
        ),
        "unitary_map_determinant_abs": float(abs(np.linalg.det(mapping))),
        "legacy_identity_covariance_max_abs_error": float(
            np.max(np.abs(migrated_identity - np.eye(OBSERVATION_DIMENSION)))
        ),
        "new_writes_accept_legacy_128d": False,
        "legacy_reads_project_to_64d": True,
        "nonhermitian_covariance_supported": False,
        "claim_boundary": (
            "This validates the coordinate algebra and schema migration only. "
            "It does not estimate physical matrix covariance or propagate gauge uncertainty."
        ),
    }

    gates = {
        "roundtrip_max_abs": 1.0e-12,
        "frobenius_inner_product_abs_error": 1.0e-12,
        "unitary_map_orthogonality_frobenius": 1.0e-11,
        "legacy_identity_covariance_max_abs_error": 1.0e-12,
    }
    failures = {
        key: {"value": result[key], "maximum": maximum}
        for key, maximum in gates.items()
        if float(result[key]) > maximum
    }
    result["gates"] = gates
    result["passed"] = not failures
    result["failures"] = failures
    if failures:
        raise RuntimeError(f"Hermitian covariance validation failed: {failures}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    result = analyze()
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
