from __future__ import annotations

import numpy as np
import pytest

from mct_research import (
    UnifiedSpectrumJacobianDiagnostics,
    unified_response_spectrum,
    unified_spectrum_jacobian,
)

ENERGY_EV = np.linspace(0.08, 0.22, 281)
BASE_PARAMETERS = {
    "zero_density_gap_ev": 0.100,
    "uniform_carrier_shift_ev": 0.030,
    "gap_sigma_ev": 0.010,
    "intrinsic_exponent": 1.0,
    "absorption_amplitude_cm_inverse_ev_power": 30000.0,
    "effective_thickness_um": 10.0,
}


def numerical_rank(matrix: np.ndarray, tolerance: float = 1.0e-8) -> int:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.count_nonzero(singular_values / singular_values[0] > tolerance))


def test_public_unified_spectrum_exports() -> None:
    assert UnifiedSpectrumJacobianDiagnostics.__name__ == (
        "UnifiedSpectrumJacobianDiagnostics"
    )
    assert callable(unified_response_spectrum)
    assert callable(unified_spectrum_jacobian)


def test_gap_carrier_and_amplitude_thickness_equivalence() -> None:
    first = unified_response_spectrum(ENERGY_EV, **BASE_PARAMETERS)
    second = unified_response_spectrum(
        ENERGY_EV,
        zero_density_gap_ev=0.120,
        uniform_carrier_shift_ev=0.010,
        gap_sigma_ev=0.010,
        intrinsic_exponent=1.0,
        absorption_amplitude_cm_inverse_ev_power=15000.0,
        effective_thickness_um=20.0,
    )

    np.testing.assert_allclose(first, second, rtol=0.0, atol=2.0e-15)
    assert first.min() < 1.0e-7
    assert first.max() > 0.9


def test_unmarked_dense_spectrum_has_rank_three() -> None:
    diagnostics = unified_spectrum_jacobian(
        ENERGY_EV,
        **BASE_PARAMETERS,
        quadrature_order=256,
    )

    assert diagnostics.numerical_rank == 3
    assert diagnostics.relative_singular_values[3] < 1.0e-10
    assert diagnostics.relative_singular_values[4] < 1.0e-12
    np.testing.assert_allclose(
        diagnostics.relative_singular_values[:3],
        [1.0, 0.0148273884, 0.0017990556],
        rtol=5.0e-4,
    )


def test_exact_jacobian_column_invariances() -> None:
    diagnostics = unified_spectrum_jacobian(
        ENERGY_EV,
        **BASE_PARAMETERS,
        quadrature_order=256,
    )
    jacobian = diagnostics.jacobian

    np.testing.assert_allclose(jacobian[:, 0], jacobian[:, 1], rtol=0.0, atol=2.0e-10)
    np.testing.assert_allclose(jacobian[:, 3], jacobian[:, 4], rtol=0.0, atol=2.0e-10)


def test_external_constraints_remove_null_directions() -> None:
    diagnostics = unified_spectrum_jacobian(
        ENERGY_EV,
        **BASE_PARAMETERS,
        quadrature_order=256,
    )
    jacobian = diagnostics.jacobian

    # Known carrier shift: Eg, sigma, amplitude, thickness retain only A*d null.
    assert numerical_rank(jacobian[:, [0, 2, 3, 4]]) == 3
    # Known thickness: Eg and carrier shift retain the translation null.
    assert numerical_rank(jacobian[:, [0, 1, 2, 3]]) == 3
    # Known carrier shift and thickness: the remaining three parameters are full rank.
    assert numerical_rank(jacobian[:, [0, 2, 3]]) == 3


def test_nontranslational_carrier_marker_raises_rank_to_four() -> None:
    diagnostics = unified_spectrum_jacobian(
        ENERGY_EV,
        **BASE_PARAMETERS,
        carrier_marker_scale_cm_inverse_per_ev=1000.0,
        quadrature_order=256,
    )

    assert diagnostics.numerical_rank == 4
    assert diagnostics.relative_singular_values[3] == pytest.approx(
        0.0017362,
        rel=0.02,
    )
    assert diagnostics.relative_singular_values[4] < 1.0e-10

    # The marker breaks both simple pairwise column equalities.  The remaining
    # exact infinitesimal invariance is the combined direction
    # (Delta, -Delta, 0, -1, +1) for
    # (Eg, Delta, ln sigma, ln A, ln d).
    jacobian = diagnostics.jacobian
    assert not np.allclose(jacobian[:, 0], jacobian[:, 1], rtol=0.0, atol=1.0e-6)
    assert not np.allclose(jacobian[:, 3], jacobian[:, 4], rtol=0.0, atol=1.0e-6)
    carrier_shift = BASE_PARAMETERS["uniform_carrier_shift_ev"]
    null_vector = np.asarray(
        [carrier_shift, -carrier_shift, 0.0, -1.0, 1.0]
    )
    np.testing.assert_allclose(
        jacobian @ null_vector,
        0.0,
        rtol=0.0,
        atol=3.0e-10,
    )

    # Independently known thickness removes the combined null direction and
    # leaves Eg, carrier shift, sigma, and amplitude locally full rank.
    assert numerical_rank(jacobian[:, [0, 1, 2, 3]]) == 4


def test_unified_spectrum_input_validation() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        unified_response_spectrum(
            [0.1, 0.1],
            **BASE_PARAMETERS,
        )
    with pytest.raises(ValueError, match="gap_sigma_ev"):
        unified_response_spectrum(
            ENERGY_EV,
            **{**BASE_PARAMETERS, "gap_sigma_ev": 0.0},
        )
    with pytest.raises(ValueError, match="non-negative"):
        unified_response_spectrum(
            ENERGY_EV,
            **{
                **BASE_PARAMETERS,
                "carrier_marker_scale_cm_inverse_per_ev": 1000.0,
                "uniform_carrier_shift_ev": -0.01,
            },
        )
