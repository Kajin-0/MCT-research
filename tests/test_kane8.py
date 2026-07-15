from __future__ import annotations

import numpy as np
import pytest

from mct_research.kane8 import KaneParameters, hamiltonian, time_reversal_residual
from mct_research.projection import PARAMETER_NAMES, closure_residual, fit_parameters


@pytest.fixture
def hg_te_like() -> KaneParameters:
    return KaneParameters.from_ep(
        ev=0.0,
        eg=-0.303,
        delta=1.08,
        ep=18.8,
        f=0.0,
        gamma1=4.1,
        gamma2=0.5,
        gamma3=1.3,
    )


def representative_k_grid() -> list[tuple[float, float, float]]:
    k_values = (0.0, 0.004, 0.009, 0.015)
    directions = np.asarray(
        [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0),
        ],
        dtype=float,
    )
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    points: list[tuple[float, float, float]] = [(0.0, 0.0, 0.0)]
    for magnitude in k_values[1:]:
        points.extend(tuple(magnitude * direction) for direction in directions)
    return points


def test_gamma_edges_and_degeneracies(hg_te_like: KaneParameters) -> None:
    h = hamiltonian((0.0, 0.0, 0.0), hg_te_like)
    expected = np.array(
        [
            hg_te_like.eg,
            hg_te_like.eg,
            0.0,
            0.0,
            0.0,
            0.0,
            -hg_te_like.delta,
            -hg_te_like.delta,
        ]
    )
    np.testing.assert_allclose(np.diag(h).real, expected, atol=1e-14)
    np.testing.assert_allclose(h - np.diag(np.diag(h)), 0.0, atol=1e-14)


@pytest.mark.parametrize(
    "k",
    [
        (0.002, -0.004, 0.007),
        (0.012, 0.003, -0.005),
        (-0.008, -0.006, 0.004),
    ],
)
def test_hermiticity(k: tuple[float, float, float], hg_te_like: KaneParameters) -> None:
    h = hamiltonian(k, hg_te_like)
    residual = np.linalg.norm(h - h.conjugate().T, ord="fro")
    assert residual < 1e-13


@pytest.mark.parametrize(
    "k",
    [
        (0.002, -0.004, 0.007),
        (0.012, 0.003, -0.005),
        (-0.008, -0.006, 0.004),
    ],
)
def test_time_reversal(k: tuple[float, float, float], hg_te_like: KaneParameters) -> None:
    assert time_reversal_residual(k, hg_te_like) < 1e-13


def test_synthetic_parameter_recovery(hg_te_like: KaneParameters) -> None:
    k_points = representative_k_grid()
    matrices = [hamiltonian(k, hg_te_like) for k in k_points]
    recovered, diagnostics = fit_parameters(k_points, matrices)

    for name in PARAMETER_NAMES:
        expected = getattr(hg_te_like, name)
        actual = getattr(recovered, name)
        assert actual == pytest.approx(expected, rel=2e-12, abs=2e-12)

    assert diagnostics["relative_residual"] < 1e-12
    assert diagnostics["condition_number"] < 1e5
    assert closure_residual(k_points, matrices, recovered) < 1e-12


def test_projection_detects_non_kane_perturbation(hg_te_like: KaneParameters) -> None:
    k_points = representative_k_grid()
    matrices = [hamiltonian(k, hg_te_like) for k in k_points]

    # Add a symmetry-breaking k-linear Gamma6-Gamma7 coupling that is absent
    # from the declared Kane manifold. The residual must not be fitted away.
    perturbed: list[np.ndarray] = []
    for k, matrix in zip(k_points, matrices, strict=True):
        modified = matrix.copy()
        amplitude = 0.2 * k[0]
        modified[0, 6] += amplitude
        modified[6, 0] += amplitude
        perturbed.append(modified)

    recovered, diagnostics = fit_parameters(k_points, perturbed)
    rho = closure_residual(k_points, perturbed, recovered)
    assert diagnostics["relative_residual"] > 1e-5
    assert rho > 1e-5


def test_axis_only_grid_cannot_identify_gamma3(hg_te_like: KaneParameters) -> None:
    axis_points = [
        (0.0, 0.0, 0.0),
        (0.01, 0.0, 0.0),
        (0.0, 0.01, 0.0),
        (0.0, 0.0, 0.01),
    ]
    matrices = [hamiltonian(k, hg_te_like) for k in axis_points]

    from mct_research.projection import ProjectionError

    with pytest.raises(ProjectionError, match="rank-deficient"):
        fit_parameters(axis_points, matrices)


def test_mixed_direction_grid_restores_full_rank() -> None:
    from mct_research.projection import design_diagnostics

    axis_only = [
        (0.0, 0.0, 0.0),
        (0.01, 0.0, 0.0),
        (0.0, 0.01, 0.0),
        (0.0, 0.0, 0.01),
    ]
    mixed = axis_only + [(0.01 / np.sqrt(2), 0.01 / np.sqrt(2), 0.0)]

    assert design_diagnostics(axis_only)["rank"] == 7
    assert design_diagnostics(mixed)["rank"] == 8
