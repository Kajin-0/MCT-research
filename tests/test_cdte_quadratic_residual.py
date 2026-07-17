import json

import numpy as np

from tools.analyze_cdte_quadratic_residual import (
    _block_diagnostics,
    _quadratic_at_scales,
    _significant_rank,
)


def test_two_radius_quadratic_richardson_removes_k4_contamination():
    q = np.diag(np.linspace(1.0, 2.0, 8)).astype(complex)
    quartic = np.diag(np.linspace(-3.0, 4.0, 8)).astype(complex)
    h = 0.01
    matrices = [np.zeros((8, 8), dtype=complex) for _ in range(13)]
    for index, k in ((1, h), (2, -h), (3, h / 2.0), (4, -h / 2.0)):
        matrices[index] = q * k**2 + quartic * k**4
    spec = {
        "radius_inverse_angstrom": h,
        "plus_h": 2,
        "minus_h": 3,
        "plus_h_over_2": 4,
        "minus_h_over_2": 5,
    }
    coarse, fine, richardson = _quadratic_at_scales(matrices, spec)
    assert np.linalg.norm(coarse - q) > 1.0e-6
    assert np.linalg.norm(fine - q) > 1.0e-7
    assert np.allclose(richardson, q, atol=1.0e-12)


def test_block_energy_accounting_matches_full_hermitian_norm():
    residual = np.zeros((8, 8), dtype=complex)
    residual[0, 2] = 1.0 + 2.0j
    residual[2, 0] = residual[0, 2].conjugate()
    residual[2, 2] = 3.0
    residual[6, 6] = -1.5
    diagnostics = _block_diagnostics(residual)
    total = sum(item["full_matrix_energy_fraction"] for item in diagnostics.values())
    np.testing.assert_allclose(total, 1.0, atol=1.0e-12)
    assert diagnostics["Gamma6-Gamma8"]["full_matrix_energy_fraction"] > 0.0
    assert diagnostics["Gamma8-Gamma8"]["full_matrix_energy_fraction"] > 0.0
    assert diagnostics["Gamma7-Gamma7"]["full_matrix_energy_fraction"] > 0.0
    json.dumps(diagnostics)


def test_significant_rank_uses_relative_cutoff():
    singular_values = np.asarray([10.0, 2.0, 0.99, 0.01])
    assert _significant_rank(singular_values, 0.10) == 2
    assert _significant_rank(singular_values, 0.09) == 3
