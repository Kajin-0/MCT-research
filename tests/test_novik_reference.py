from __future__ import annotations

import numpy as np
import pytest

from mct_research.kane8 import ALPHA_EV_A2, KaneParameters, hamiltonian


DIRECTIONS = {
    "100": np.asarray((1.0, 0.0, 0.0)),
    "110": np.asarray((1.0, 1.0, 0.0)) / np.sqrt(2.0),
    "111": np.asarray((1.0, 1.0, 1.0)) / np.sqrt(3.0),
}


@pytest.fixture
def cd_te_novik() -> KaneParameters:
    """CdTe parameters from Table I of Novik et al."""

    return KaneParameters.from_ep(
        ev=0.0,
        eg=1.606,
        delta=0.91,
        ep=18.8,
        f=-0.09,
        gamma1=1.47,
        gamma2=-0.28,
        gamma3=0.03,
    )


def novik_bulk_reference(
    k: np.ndarray | tuple[float, float, float], params: KaneParameters
) -> np.ndarray:
    """Independent homogeneous-bulk specialization of Novik Eqs. (5)-(6).

    The matrix is written explicitly in the published basis. Position-dependent
    commutators vanish, so C=0 and Sbar=S_tilde.
    """

    kx, ky, kz = (float(value) for value in k)
    kp = kx + 1j * ky
    km = kx - 1j * ky
    k2 = kx * kx + ky * ky + kz * kz
    a = ALPHA_EV_A2
    rt2 = np.sqrt(2.0)
    rt3 = np.sqrt(3.0)
    rt6 = np.sqrt(6.0)

    t = params.ev + params.eg + a * (1.0 + 2.0 * params.f) * k2
    u = params.ev - a * params.gamma1 * k2
    v = -a * params.gamma2 * (kx * kx + ky * ky - 2.0 * kz * kz)
    r = a * rt3 * (
        params.gamma2 * (kx * kx - ky * ky)
        - 2.0j * params.gamma3 * kx * ky
    )
    s_minus = -2.0 * a * rt3 * params.gamma3 * km * kz
    s_plus = -2.0 * a * rt3 * params.gamma3 * kp * kz
    p = params.p

    return np.asarray(
        [
            [t, 0, -p * kp / rt2, p * np.sqrt(2.0 / 3.0) * kz, p * km / rt6, 0, -p * kz / rt3, -p * km / rt3],
            [0, t, 0, -p * kp / rt6, p * np.sqrt(2.0 / 3.0) * kz, p * km / rt2, -p * kp / rt3, p * kz / rt3],
            [-p * km / rt2, 0, u + v, -s_minus, r, 0, s_minus / rt2, -rt2 * r],
            [p * np.sqrt(2.0 / 3.0) * kz, -p * km / rt6, -np.conjugate(s_minus), u - v, 0, r, rt2 * v, -np.sqrt(3.0 / 2.0) * s_minus],
            [p * kp / rt6, p * np.sqrt(2.0 / 3.0) * kz, np.conjugate(r), 0, u - v, np.conjugate(s_plus), -np.sqrt(3.0 / 2.0) * np.conjugate(s_plus), -rt2 * v],
            [0, p * kp / rt2, 0, np.conjugate(r), s_plus, u + v, rt2 * np.conjugate(r), s_plus / rt2],
            [-p * kz / rt3, -p * km / rt3, np.conjugate(s_minus) / rt2, rt2 * v, -np.sqrt(3.0 / 2.0) * s_plus, rt2 * r, u - params.delta, 0],
            [-p * kp / rt3, p * kz / rt3, -rt2 * np.conjugate(r), -np.sqrt(3.0 / 2.0) * np.conjugate(s_minus), -rt2 * v, np.conjugate(s_plus) / rt2, 0, u - params.delta],
        ],
        dtype=np.complex128,
    )


def _kramers_pair_energies(matrix: np.ndarray) -> np.ndarray:
    eigenvalues = np.linalg.eigvalsh(matrix)
    return 0.5 * (eigenvalues[::2] + eigenvalues[1::2])


def _quadratic_coefficients(model, direction, params, step: float = 2.0e-5):
    zero = _kramers_pair_energies(model(np.zeros(3), params))
    plus = _kramers_pair_energies(model(step * direction, params))
    minus = _kramers_pair_energies(model(-step * direction, params))
    return (plus + minus - 2.0 * zero) / (2.0 * step * step)


@pytest.mark.parametrize("direction", DIRECTIONS.values(), ids=DIRECTIONS.keys())
def test_matrix_and_eigenvalues_match_published_novik_form(
    direction: np.ndarray, cd_te_novik: KaneParameters
) -> None:
    k = 0.013 * direction
    implemented = hamiltonian(k, cd_te_novik)
    reference = novik_bulk_reference(k, cd_te_novik)
    np.testing.assert_allclose(implemented, reference, rtol=2.0e-14, atol=2.0e-14)
    np.testing.assert_allclose(
        np.linalg.eigvalsh(implemented),
        np.linalg.eigvalsh(reference),
        rtol=2.0e-14,
        atol=2.0e-14,
    )


@pytest.mark.parametrize("direction", DIRECTIONS.values(), ids=DIRECTIONS.keys())
def test_effective_mass_curvatures_match_independent_novik_matrix(
    direction: np.ndarray, cd_te_novik: KaneParameters
) -> None:
    implemented = _quadratic_coefficients(hamiltonian, direction, cd_te_novik)
    reference = _quadratic_coefficients(
        novik_bulk_reference, direction, cd_te_novik
    )
    np.testing.assert_allclose(implemented, reference, rtol=1.0e-8, atol=2.0e-6)


def test_conduction_mass_matches_lowedin_second_order_formula(
    cd_te_novik: KaneParameters,
) -> None:
    p = cd_te_novik.p
    expected_coefficient = (
        ALPHA_EV_A2 * (1.0 + 2.0 * cd_te_novik.f)
        + (2.0 / 3.0) * p * p / cd_te_novik.eg
        + (1.0 / 3.0) * p * p / (cd_te_novik.eg + cd_te_novik.delta)
    )
    expected_mass_ratio = ALPHA_EV_A2 / expected_coefficient

    for direction in DIRECTIONS.values():
        coefficient = _quadratic_coefficients(
            hamiltonian, direction, cd_te_novik
        )[-1]
        mass_ratio = ALPHA_EV_A2 / coefficient
        assert coefficient == pytest.approx(
            expected_coefficient, rel=5.0e-7, abs=2.0e-5
        )
        assert mass_ratio == pytest.approx(expected_mass_ratio, rel=5.0e-7)
