from __future__ import annotations

import numpy as np

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p
from tools.cdte_spectral_closure import analyze_conventional_spectral_closure


def _contract() -> dict[str, object]:
    return {
        "pairs": {
            "001": {
                "unit_direction": [0.0, 0.0, 1.0],
                "radius_inverse_angstrom": 0.01,
                "plus_h": 2,
                "minus_h": 3,
                "plus_h_over_2": 4,
                "minus_h_over_2": 5,
            },
            "111": {
                "unit_direction": [1.0 / np.sqrt(3.0)] * 3,
                "radius_inverse_angstrom": 0.01,
                "plus_h": 6,
                "minus_h": 7,
                "plus_h_over_2": 8,
                "minus_h_over_2": 9,
            },
            "110": {
                "unit_direction": [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0), 0.0],
                "radius_inverse_angstrom": 0.01,
                "plus_h": 10,
                "minus_h": 11,
                "plus_h_over_2": 12,
                "minus_h_over_2": 13,
            },
        },
        "training_directions": ["001", "111"],
        "holdout_directions": ["110"],
        "thresholds": {
            "maximum_spectral_training_relative_residual": 1.0e-7,
            "maximum_spectral_holdout_relative_residual": 1.0e-7,
        },
    }


def _points(contract: dict[str, object]) -> np.ndarray:
    result = [np.zeros(3)]
    for name in ("001", "111", "110"):
        spec = contract["pairs"][name]
        direction = np.asarray(spec["unit_direction"], dtype=float)
        h = float(spec["radius_inverse_angstrom"])
        result.extend((h * direction, -h * direction, 0.5 * h * direction, -0.5 * h * direction))
    return np.asarray(result)


def test_exact_conventional_spectrum_is_recovered_from_perturbed_quadratic_start() -> None:
    contract = _contract()
    points = _points(contract)
    exact = ExtendedKaneParameters(
        ev=0.1,
        eg=0.8,
        delta=0.9,
        p8=7.2,
        p7=6.4,
        f=-0.08,
        gamma1=1.5,
        gamma2=-0.25,
        gamma3=0.15,
    )
    lower = np.linspace(-20.0, -2.0, 30)
    upper = np.asarray([5.0, 7.0])
    blocks = []
    for index, point in enumerate(points, start=1):
        selected = np.linalg.eigvalsh(hamiltonian_two_p(point, exact))
        blocks.append(
            {
                "index": index,
                "eigenvalues_ev": np.concatenate((lower, selected, upper)).tolist(),
            }
        )
    payload = {"blocks": blocks}
    starting = {
        "ev": exact.ev,
        "eg": exact.eg,
        "delta": exact.delta,
        "p8": exact.p8,
        "p7": exact.p7,
        "f": 0.05,
        "gamma1": 1.2,
        "gamma2": -0.1,
        "gamma3": 0.3,
    }

    result = analyze_conventional_spectral_closure(
        payload, points, contract, starting
    )

    assert result["gauge_status"] == "unitary_basis_invariant_spectral_observable"
    assert result["passed_declared_spectral_gate"]
    assert result["training"]["relative_residual"] < 1.0e-7
    assert result["maximum_holdout_relative_residual"] < 1.0e-7
