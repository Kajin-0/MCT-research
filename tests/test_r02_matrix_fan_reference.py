from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tools.matrix_fan import (
    fan_matrix,
    fan_matrix_derivative,
    hermitian_part,
    linewidth_matrix,
    rotate_external_contributions,
    rotate_intermediate_contribution,
    scalar_diagonal_reference,
    symmetrized_on_shell_hermitian,
)

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PATH = (
    ROOT / "first_principles/b0/r02_matrix_fan_reference_result.json"
)


def _unitary_2() -> np.ndarray:
    angle = 0.37
    phase = np.exp(0.31j)
    return np.array(
        [
            [np.cos(angle), -phase.conjugate() * np.sin(angle)],
            [phase * np.sin(angle), np.cos(angle)],
        ],
        dtype=complex,
    )


def _contribution(
    vertex: np.ndarray,
    *,
    q_weight: float,
    intermediate_energies_ev: list[float] | None = None,
    occupations: list[float] | None = None,
) -> dict:
    return {
        "vertex_ev": np.asarray(vertex, dtype=complex),
        "intermediate_energies_ev": (
            [-0.3, 0.2, 0.7]
            if intermediate_energies_ev is None
            else intermediate_energies_ev
        ),
        "occupations": [1.0, 0.0, 0.0] if occupations is None else occupations,
        "phonon_energy_ev": 0.04,
        "bose_occupation": 0.3,
        "q_weight": q_weight,
    }


def _reference_contributions() -> list[dict]:
    return [
        _contribution(
            np.array(
                [
                    [0.10 + 0.02j, 0.03 - 0.01j],
                    [0.02 + 0.04j, -0.08 + 0.01j],
                    [0.05 - 0.03j, 0.07 + 0.02j],
                ]
            ),
            q_weight=0.4,
        ),
        _contribution(
            np.array(
                [
                    [0.0 + 0.02j, 0.03],
                    [0.01, 0.0 + 0.04j],
                    [0.03, 0.02],
                ]
            ),
            q_weight=0.6,
        ),
    ]


def _measured_metrics() -> dict[str, float]:
    contributions = _reference_contributions()
    energy = 0.11
    eta = 0.012
    matrix = fan_matrix(contributions, energy, eta)
    diagonal = max(
        abs(
            matrix[index, index]
            - scalar_diagonal_reference(contributions, index, energy, eta)
        )
        for index in range(2)
    )

    unitary = _unitary_2()
    rotated = fan_matrix(
        rotate_external_contributions(contributions, unitary), energy, eta
    )
    external_covariance = np.max(
        np.abs(rotated - unitary.conj().T @ matrix @ unitary)
    )

    intermediate_unitary = np.eye(3, dtype=complex)
    intermediate_unitary[:2, :2] = unitary
    intermediate = _contribution(
        contributions[0]["vertex_ev"],
        q_weight=0.4,
        intermediate_energies_ev=[0.2, 0.2, 0.7],
        occupations=[0.0, 0.0, 1.0],
    )
    intermediate_rotated = rotate_intermediate_contribution(
        intermediate,
        intermediate_unitary,
        energy_ev=0.1,
        eta_ev=0.02,
    )
    intermediate_invariance = np.max(
        np.abs(
            fan_matrix([intermediate], 0.1, 0.02)
            - fan_matrix([intermediate_rotated], 0.1, 0.02)
        )
    )

    linewidth = linewidth_matrix(matrix)
    common = hermitian_part(matrix)
    step = 1.0e-6
    analytic = fan_matrix_derivative(contributions, energy, eta)
    numerical = (
        fan_matrix(contributions, energy + step, eta)
        - fan_matrix(contributions, energy - step, eta)
    ) / (2.0 * step)

    external_energies = [-0.1, -0.1]
    on_shell = symmetrized_on_shell_hermitian(
        [contributions[0]], external_energies, 0.02
    )
    on_shell_rotated = symmetrized_on_shell_hermitian(
        rotate_external_contributions([contributions[0]], unitary),
        external_energies,
        0.02,
    )

    zero = _contribution(
        np.zeros((3, 2), dtype=complex),
        q_weight=0.4,
    )
    return {
        "diagonal_equivalence_max_abs_ev": float(diagonal),
        "external_covariance_max_abs_ev": float(external_covariance),
        "intermediate_invariance_max_abs_ev": float(intermediate_invariance),
        "linewidth_hermiticity_max_abs_ev": float(
            np.max(np.abs(linewidth - linewidth.conj().T))
        ),
        "linewidth_minimum_eigenvalue_ev": float(
            np.min(np.linalg.eigvalsh(linewidth))
        ),
        "common_hermiticity_max_abs_ev": float(
            np.max(np.abs(common - common.conj().T))
        ),
        "derivative_finite_difference_max_abs": float(
            np.max(np.abs(analytic - numerical))
        ),
        "on_shell_hermiticity_max_abs_ev": float(
            np.max(np.abs(on_shell - on_shell.conj().T))
        ),
        "on_shell_degenerate_covariance_max_abs_ev": float(
            np.max(
                np.abs(
                    on_shell_rotated
                    - unitary.conj().T @ on_shell @ unitary
                )
            )
        ),
        "zero_coupling_max_abs_ev": float(
            np.max(np.abs(fan_matrix([zero], 0.1, 0.02)))
        ),
    }


def test_immutable_reference_metrics_reproduce() -> None:
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    measured = _measured_metrics()
    for name, expected in reference["measured_residuals"].items():
        assert measured[name] == pytest.approx(expected, rel=1.0e-12, abs=1.0e-15)


def test_immutable_reference_decision_remains_restricted_and_fail_closed() -> None:
    reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    assert reference["status"] == "all_mandatory_synthetic_gates_pass"
    assert reference["decision"]["classification"] == "RESTRICTED_GO"
    assert reference["decision"]["backend_vertex_export_validated"] is False
    assert reference["decision"]["material_self_energy_validated"] is False
    assert reference["decision"]["automatic_followup_authorized"] is False
    assert all(value is False for value in reference["authorization"].values())
