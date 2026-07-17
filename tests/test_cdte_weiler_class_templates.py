import numpy as np

from tools.cdte_quadratic_invariant_space import (
    _evaluate,
    _fit_subspace,
    build_quadratic_projector,
)
from tools.cdte_weiler_class_templates import (
    CLASS_NAMES,
    build_weiler_class_basis,
    conventional_relation_diagnostics,
)


def test_weiler_classes_span_projector_and_recover_synthetic_coordinates():
    projector, tensors, hermitian, sectors, _ = build_quadratic_projector()
    classes, diagnostics = build_weiler_class_basis(projector, sectors)
    assert CLASS_NAMES == (
        "F",
        "N2",
        "G",
        "G_prime",
        "gamma1",
        "gamma2",
        "gamma3",
        "gamma2_prime",
        "gamma3_prime",
        "gamma1_prime",
    )
    assert classes.shape == (384, 10)
    assert diagnostics["gram_residual"] < 1.0e-10
    assert diagnostics["projector_residual"] < 1.0e-10

    relations = conventional_relation_diagnostics(tensors, hermitian, classes)
    assert relations["normalized_relation_residual"] < 1.0e-10

    directions = {
        "001": np.asarray([0.0, 0.0, 1.0]),
        "111": np.asarray([1.0, 1.0, 1.0]) / np.sqrt(3.0),
        "110": np.asarray([1.0, 1.0, 0.0]) / np.sqrt(2.0),
    }
    planted = np.asarray([1.2, -0.7, 2.1, 0.4, -1.3, 0.8, 1.7, -2.2, 0.9, 1.5])
    observations = {
        name: sum(
            planted[index]
            * _evaluate(classes[:, index], direction, tensors, hermitian)
            for index in range(10)
        )
        for name, direction in directions.items()
    }
    fit = _fit_subspace(
        classes,
        observations,
        directions,
        ["001", "111"],
        tensors,
        hermitian,
    )
    assert fit["design_rank"] == 10
    assert fit["condition_number"] < 2.0
    assert fit["training_relative_residual"] < 1.0e-12
    assert fit["direction_relative_residuals"]["110"] < 1.0e-12
    np.testing.assert_allclose(
        fit["orthonormal_basis_coefficients_ev_angstrom2"],
        planted,
        atol=1.0e-12,
    )
