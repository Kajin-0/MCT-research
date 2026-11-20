"""Algebraic/unit tests only. Example endpoints are not new DFT measurements."""
from math import sqrt

import numpy as np
import pytest

from mct_research.inversion_baseline import (
    critical_composition_sensitivity,
    critical_composition_sigma,
    critical_compositions,
    signed_gamma_gap_ev,
)
from mct_research.kane8 import KaneParameters, hamiltonian

A, C = -0.27, 1.34  # illustrative literature-scale numbers, not project DFT results


def test_endpoints_and_sign_convention():
    assert signed_gamma_gap_ev(0, hgte_ev=A, cdte_ev=C, bowing_ev=0.4) == A
    assert signed_gamma_gap_ev(1, hgte_ev=A, cdte_ev=C, bowing_ev=0.4) == C
    assert signed_gamma_gap_ev(0.5, hgte_ev=A, cdte_ev=C, bowing_ev=0.4) == pytest.approx(0.5*(A+C)-0.1)


def test_linear_critical_composition():
    x = critical_compositions(hgte_ev=A, cdte_ev=C)
    assert len(x) == 1
    assert x[0] == pytest.approx(-A/(C-A), abs=1e-13)


@pytest.mark.parametrize('bowing', [-2.0, -0.75, -0.001, 0.0, 0.2, 2.0])
def test_quadratic_root_satisfies_signed_gap(bowing):
    roots = critical_compositions(hgte_ev=A, cdte_ev=C, bowing_ev=bowing)
    assert len(roots) == 1
    assert abs(signed_gamma_gap_ev(roots[0], hgte_ev=A, cdte_ev=C, bowing_ev=bowing)) < 1e-12


def test_two_transitions_are_not_hidden():
    expected = ((1-sqrt(.5))/2, (1+sqrt(.5))/2)
    assert critical_compositions(hgte_ev=1, cdte_ev=1, bowing_ev=8) == pytest.approx(expected)
    with pytest.raises(ValueError, match='Exactly one'):
        critical_composition_sensitivity(hgte_ev=1, cdte_ev=1, bowing_ev=8)


def test_no_transition_and_degenerate_polynomial():
    assert critical_compositions(hgte_ev=0.3, cdte_ev=1.1) == ()
    with pytest.raises(ValueError, match='identically zero'):
        critical_compositions(hgte_ev=0, cdte_ev=0)


def test_positive_bowing_pushes_critical_x_higher_for_this_endpoints():
    assert critical_compositions(hgte_ev=A, cdte_ev=C, bowing_ev=0.2)[0] > critical_compositions(hgte_ev=A, cdte_ev=C)[0]


def test_first_order_sensitivities_against_finite_difference():
    base = [A, C, 0.20]
    sens = critical_composition_sensitivity(hgte_ev=base[0], cdte_ev=base[1], bowing_ev=base[2])
    analytic = [sens.dx_dhgte_ev_inverse, sens.dx_dcdte_ev_inverse, sens.dx_dbowing_ev_inverse]
    delta = 1e-6
    for i in range(3):
        p, m = base.copy(), base.copy()
        p[i] += delta
        m[i] -= delta
        fp = critical_compositions(hgte_ev=p[0], cdte_ev=p[1], bowing_ev=p[2])[0]
        fm = critical_compositions(hgte_ev=m[0], cdte_ev=m[1], bowing_ev=m[2])[0]
        assert analytic[i] == pytest.approx((fp-fm)/(2*delta), rel=1e-7)


def test_independent_covariance_propagation_and_validation():
    s = critical_composition_sensitivity(hgte_ev=A, cdte_ev=C, bowing_ev=0.2)
    cov = np.diag([0.01**2, 0.02**2, 0.03**2])
    actual = critical_composition_sigma(hgte_ev=A, cdte_ev=C, bowing_ev=0.2, covariance_ev2=cov)
    expected = sqrt((s.dx_dhgte_ev_inverse*.01)**2+(s.dx_dcdte_ev_inverse*.02)**2+(s.dx_dbowing_ev_inverse*.03)**2)
    assert actual == pytest.approx(expected)
    with pytest.raises(ValueError, match='positive semidefinite'):
        critical_composition_sigma(hgte_ev=A, cdte_ev=C, bowing_ev=.2, covariance_ev2=np.diag([1., 1., -1.]))


def test_gamma_eigenenergies_embed_into_existing_eight_band_kane():
    for x in [0, .13, .17, .25, 1]:
        gap = signed_gamma_gap_ev(x, hgte_ev=A, cdte_ev=C, bowing_ev=.2)
        params = KaneParameters(eg=gap, delta=.95, p=8.0, ev=0.0)
        expected = sorted([-0.95]*2+[0.0]*4+[gap]*2)
        got = np.linalg.eigvalsh(hamiltonian((0,0,0), params))
        assert got == pytest.approx(expected, abs=1e-12)


def test_invalid_composition_and_nonfinite():
    for x in (-0.001, 1.001, float('nan')):
        with pytest.raises(ValueError):
            signed_gamma_gap_ev(x, hgte_ev=A, cdte_ev=C)
