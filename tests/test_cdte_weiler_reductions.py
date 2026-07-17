import numpy as np

from tools.analyze_cdte_weiler_reductions import (
    build_departure_basis,
    enumerate_reductions,
    summarize_frontier,
)
from tools.cdte_quadratic_invariant_space import (
    _conventional_span,
    _evaluate,
    build_quadratic_projector,
)
from tools.cdte_weiler_class_templates import build_weiler_class_basis


def test_exhaustive_reduction_frontier_requires_all_nonzero_departures():
    projector, tensors, hermitian, sectors, _ = build_quadratic_projector()
    classes, _ = build_weiler_class_basis(projector, sectors)
    _, conventional = _conventional_span(tensors, hermitian)
    departures = build_departure_basis(classes)
    full = np.column_stack((conventional, departures))
    assert np.linalg.norm(full.T @ full - np.eye(10)) < 1.0e-10
    assert np.linalg.norm(full @ full.T - projector) < 1.0e-10

    coefficients = np.arange(1.0, 11.0)
    target = full @ coefficients
    directions = {
        "001": np.asarray([0.0, 0.0, 1.0]),
        "111": np.asarray([1.0, 1.0, 1.0]) / np.sqrt(3.0),
        "110": np.asarray([1.0, 1.0, 0.0]) / np.sqrt(2.0),
    }
    observations = {
        name: _evaluate(target, direction, tensors, hermitian)
        for name, direction in directions.items()
    }
    records = enumerate_reductions(
        conventional,
        departures,
        observations,
        directions,
        ["001", "111"],
        tensors,
        hermitian,
    )
    assert len(records) == 64
    complete = next(item for item in records if item["departure_count"] == 6)
    assert complete["training_relative_residual"] < 1.0e-12
    assert complete["maximum_holdout_relative_residual"] < 1.0e-12
    assert all(
        item["maximum_training_or_holdout_relative_residual"] > 1.0e-3
        for item in records
        if item["departure_count"] == 5
    )

    frontier, thresholds = summarize_frontier(records, [1.0e-3])
    assert len(frontier) == 7
    assert thresholds["0.001"]["departure_count"] == 6
