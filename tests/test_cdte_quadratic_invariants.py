import numpy as np

from tools.cdte_quadratic_invariant_space import (
    SECTORS,
    _conventional_span,
    _fit_subspace,
    _orthonormalize,
    _projected_basis,
    build_quadratic_projector,
)


def test_complete_quadratic_space_dimensions_and_synthetic_closure():
    projector, tensors, hermitian, hermitian_sectors, diagnostics = (
        build_quadratic_projector()
    )
    assert diagnostics["symmetry_residual"] < 1.0e-10
    assert diagnostics["idempotency_residual"] < 1.0e-10
    assert diagnostics["group_time_reversal_commutator"] < 1.0e-10
    np.testing.assert_allclose(diagnostics["trace"], 10.0, atol=1.0e-10)

    sector_bases = {}
    for sector in SECTORS:
        indices = [
            tensor * 64 + matrix
            for tensor in range(6)
            for matrix, matrix_sector in enumerate(hermitian_sectors)
            if matrix_sector == sector
        ]
        sector_bases[sector] = _projected_basis(projector, indices)
    assert {name: basis.shape[1] for name, basis in sector_bases.items()} == {
        "66": 1,
        "68": 2,
        "67": 1,
        "88": 3,
        "87": 2,
        "77": 1,
    }

    conventional_raw, conventional = _conventional_span(tensors, hermitian)
    assert conventional.shape == (384, 4)
    assert max(
        np.linalg.norm((np.eye(384) - projector) @ conventional_raw[:, index])
        / np.linalg.norm(conventional_raw[:, index])
        for index in range(4)
    ) < 1.0e-10

    gamma_span = _orthonormalize(
        [conventional_raw[:, index] for index in range(1, 4)]
    )
    valence = np.column_stack(
        [sector_bases["88"], sector_bases["87"], sector_bases["77"]]
    )
    valence_extra = _orthonormalize(
        [column - gamma_span @ (gamma_span.T @ column) for column in valence.T]
    )
    groups = {
        "conventional": conventional,
        "Gamma6-Gamma8": sector_bases["68"],
        "Gamma6-Gamma7": sector_bases["67"],
        "valence-extra": valence_extra,
    }
    complete = np.column_stack(list(groups.values()))
    assert complete.shape == (384, 10)
    assert np.linalg.norm(complete @ complete.T - projector) < 1.0e-10

    directions = {
        "001": np.asarray([0.0, 0.0, 1.0]),
        "111": np.asarray([1.0, 1.0, 1.0]) / np.sqrt(3.0),
        "110": np.asarray([1.0, 1.0, 0.0]) / np.sqrt(2.0),
    }
    coefficients = np.asarray([1.3, -2.1, 0.7, 1.8, 2.2, -1.4, 1.1, 0.9, -1.7, 2.5])

    from tools.cdte_quadratic_invariant_space import _evaluate

    observations = {
        name: sum(
            coefficients[index]
            * _evaluate(complete[:, index], direction, tensors, hermitian)
            for index in range(10)
        )
        for name, direction in directions.items()
    }
    full = _fit_subspace(
        complete, observations, directions, ["001", "111"], tensors, hermitian
    )
    assert full["design_rank"] == 10
    assert full["condition_number"] < 2.0
    assert full["training_relative_residual"] < 1.0e-12
    assert full["direction_relative_residuals"]["110"] < 1.0e-12

    for omitted in ("Gamma6-Gamma8", "Gamma6-Gamma7", "valence-extra"):
        reduced = np.column_stack(
            [basis for name, basis in groups.items() if name != omitted]
        )
        fit = _fit_subspace(
            reduced, observations, directions, ["001", "111"], tensors, hermitian
        )
        assert fit["direction_relative_residuals"]["110"] > 1.0e-3
