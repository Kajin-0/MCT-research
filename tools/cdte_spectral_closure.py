"""Gauge-invariant spectral closure diagnostics for the CdTe Kane smoke."""
from __future__ import annotations

from typing import Any

import numpy as np

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p

QUADRATIC_NAMES = ("f", "gamma1", "gamma2", "gamma3")


def _selected_eigenvalues(payload: dict[str, Any]) -> np.ndarray:
    blocks = payload.get("blocks", [])
    if len(blocks) != 13:
        raise ValueError("expected 13 exact eigenvalue blocks")
    selected = []
    for expected_index, block in enumerate(blocks, start=1):
        if int(block.get("index", -1)) != expected_index:
            raise ValueError("eigenvalue blocks are not in exact k-point order")
        values = np.asarray(block["eigenvalues_ev"], dtype=float)
        if values.shape != (40,):
            raise ValueError("expected 40 eigenvalues per k point")
        selected.append(np.sort(values[30:38]))
    return np.asarray(selected)


def _indices_for_directions(
    contract: dict[str, Any], names: list[str]
) -> list[int]:
    indices: list[int] = []
    for name in names:
        spec = contract["pairs"][name]
        indices.extend(
            int(spec[key]) - 1
            for key in (
                "plus_h",
                "minus_h",
                "plus_h_over_2",
                "minus_h_over_2",
            )
        )
    return indices


def _parameter_object(
    fixed: dict[str, float], quadratic: np.ndarray
) -> ExtendedKaneParameters:
    values = {**fixed, **dict(zip(QUADRATIC_NAMES, quadratic.tolist(), strict=True))}
    return ExtendedKaneParameters(**values)


def _spectral_shift_residual(
    quadratic: np.ndarray,
    fixed: dict[str, float],
    cartesian: np.ndarray,
    target_eigenvalues: np.ndarray,
    indices: list[int],
) -> tuple[np.ndarray, np.ndarray]:
    parameters = _parameter_object(fixed, quadratic)
    model_gamma = np.linalg.eigvalsh(hamiltonian_two_p(np.zeros(3), parameters))
    target_gamma = target_eigenvalues[0]
    residual = []
    target = []
    for index in indices:
        model_shift = (
            np.linalg.eigvalsh(hamiltonian_two_p(cartesian[index], parameters))
            - model_gamma
        )
        target_shift = target_eigenvalues[index] - target_gamma
        residual.extend(model_shift - target_shift)
        target.extend(target_shift)
    return np.asarray(residual), np.asarray(target)


def _finite_difference_jacobian(
    quadratic: np.ndarray,
    fixed: dict[str, float],
    cartesian: np.ndarray,
    target_eigenvalues: np.ndarray,
    indices: list[int],
) -> np.ndarray:
    base, _ = _spectral_shift_residual(
        quadratic, fixed, cartesian, target_eigenvalues, indices
    )
    jacobian = np.empty((base.size, quadratic.size), dtype=float)
    for column in range(quadratic.size):
        step = 1.0e-5 * max(1.0, abs(float(quadratic[column])))
        plus = quadratic.copy()
        minus = quadratic.copy()
        plus[column] += step
        minus[column] -= step
        plus_residual, _ = _spectral_shift_residual(
            plus, fixed, cartesian, target_eigenvalues, indices
        )
        minus_residual, _ = _spectral_shift_residual(
            minus, fixed, cartesian, target_eigenvalues, indices
        )
        jacobian[:, column] = (plus_residual - minus_residual) / (2.0 * step)
    return jacobian


def _fit_quadratic_spectrum(
    initial: np.ndarray,
    fixed: dict[str, float],
    cartesian: np.ndarray,
    target_eigenvalues: np.ndarray,
    indices: list[int],
    *,
    maximum_iterations: int = 80,
) -> tuple[np.ndarray, dict[str, Any]]:
    quadratic = np.asarray(initial, dtype=float).copy()
    damping = 1.0e-6
    residual, target = _spectral_shift_residual(
        quadratic, fixed, cartesian, target_eigenvalues, indices
    )
    cost = float(residual @ residual)
    accepted_steps = 0
    converged = False
    iteration = 0
    for iteration in range(1, maximum_iterations + 1):
        jacobian = _finite_difference_jacobian(
            quadratic, fixed, cartesian, target_eigenvalues, indices
        )
        normal = jacobian.T @ jacobian + damping * np.eye(quadratic.size)
        gradient = jacobian.T @ residual
        try:
            step = np.linalg.solve(normal, -gradient)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(normal, -gradient, rcond=None)[0]
        candidate = quadratic + step
        candidate_residual, _ = _spectral_shift_residual(
            candidate, fixed, cartesian, target_eigenvalues, indices
        )
        candidate_cost = float(candidate_residual @ candidate_residual)
        if candidate_cost < cost:
            previous = cost
            quadratic = candidate
            residual = candidate_residual
            cost = candidate_cost
            accepted_steps += 1
            damping = max(damping / 3.0, 1.0e-12)
            fractional_improvement = (previous - cost) / max(previous, 1.0e-30)
            if np.linalg.norm(step) < 1.0e-9 or fractional_improvement < 1.0e-10:
                converged = True
                break
        else:
            damping = min(damping * 10.0, 1.0e12)
    relative = float(
        np.linalg.norm(residual)
        / max(np.linalg.norm(target), np.finfo(float).eps)
    )
    return quadratic, {
        "converged": converged,
        "iterations": iteration,
        "accepted_steps": accepted_steps,
        "final_damping": float(damping),
        "relative_residual": relative,
        "absolute_residual_ev": float(np.linalg.norm(residual)),
        "maximum_absolute_error_ev": float(np.max(np.abs(residual))),
        "target_shift_norm_ev": float(np.linalg.norm(target)),
    }


def analyze_conventional_spectral_closure(
    eigenvalue_payload: dict[str, Any],
    cartesian: np.ndarray,
    contract: dict[str, Any],
    matrix_fit_parameters: dict[str, float],
) -> dict[str, Any]:
    """Fit conventional quadratic parameters to eigenvalue shifts only.

    The fixed zone-center and linear parameters come from the polar-gauge matrix
    extraction. Only ``f, gamma1, gamma2, gamma3`` are refit. The objective uses
    sorted eigenvalue shifts and is therefore invariant under unitary changes of
    basis within the selected eight-band manifold.
    """
    target = _selected_eigenvalues(eigenvalue_payload)
    fixed = {
        name: float(matrix_fit_parameters[name])
        for name in ("ev", "eg", "delta", "p8", "p7")
    }
    initial = np.asarray(
        [matrix_fit_parameters[name] for name in QUADRATIC_NAMES], dtype=float
    )
    training_names = list(contract["training_directions"])
    holdout_names = list(contract["holdout_directions"])
    training_indices = _indices_for_directions(contract, training_names)
    fitted, diagnostics = _fit_quadratic_spectrum(
        initial, fixed, cartesian, target, training_indices
    )

    heldout = {}
    for name in holdout_names:
        indices = _indices_for_directions(contract, [name])
        residual, target_shift = _spectral_shift_residual(
            fitted, fixed, cartesian, target, indices
        )
        heldout[name] = {
            "relative_residual": float(
                np.linalg.norm(residual)
                / max(np.linalg.norm(target_shift), np.finfo(float).eps)
            ),
            "absolute_residual_ev": float(np.linalg.norm(residual)),
            "maximum_absolute_error_ev": float(np.max(np.abs(residual))),
            "target_shift_norm_ev": float(np.linalg.norm(target_shift)),
        }
    maximum_holdout = max(
        record["relative_residual"] for record in heldout.values()
    )
    thresholds = contract["thresholds"]
    passed = (
        diagnostics["relative_residual"]
        <= float(thresholds["maximum_spectral_training_relative_residual"])
        and maximum_holdout
        <= float(thresholds["maximum_spectral_holdout_relative_residual"])
    )
    return {
        "metric": "sorted_selected_eigenvalue_shifts_relative_l2",
        "gauge_status": "unitary_basis_invariant_spectral_observable",
        "fixed_parameters": fixed,
        "initial_matrix_fit_quadratic_parameters": dict(
            zip(QUADRATIC_NAMES, initial.tolist(), strict=True)
        ),
        "spectral_fit_quadratic_parameters": dict(
            zip(QUADRATIC_NAMES, fitted.tolist(), strict=True)
        ),
        "training": diagnostics,
        "heldout": heldout,
        "maximum_holdout_relative_residual": maximum_holdout,
        "passed_declared_spectral_gate": passed,
        "interpretation": (
            "The conventional tied quadratic model is tested against basis-invariant "
            "selected-band dispersions, not only against polar-gauge matrix entries."
        ),
    }
