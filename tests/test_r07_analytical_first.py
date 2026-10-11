"""Independent finite-Hamiltonian and exact algebra tests for R07 bounds."""

from fractions import Fraction
from itertools import product
from math import comb

import numpy as np
import pytest

from mct_research.analytical_gap_closure import (
    DiscreteFeshbachMeasure,
    covariance_resolvent_error_bound,
    mass_root_error_bound,
)


def test_measure_matches_dense_hermitian_feshbach_and_is_causal():
    energies = np.array([-1.3, -0.6, 0.9])
    coupling = np.array([0.14, 0.08, 0.21])
    measure = DiscreteFeshbachMeasure(energies, coupling**2)
    h = np.zeros((4, 4))
    h[0, 0] = 0.12
    h[1:, 1:] = np.diag(energies)
    h[0, 1:] = h[1:, 0] = coupling
    for z in [0.05+0.03j, -0.2+0.2j, 0.1]:
        dense = np.linalg.inv(z*np.eye(4)-h)[0, 0]
        reduced = 1/(z-h[0, 0]-measure.kernel(z))
        assert reduced == pytest.approx(dense, abs=2e-13)
        if np.imag(z) > 0:
            assert measure.kernel(z).imag < 0
    # Independent remote scattering norm, not a finite difference of the helper.
    e = 0.1
    assert -measure.derivative(e).real == pytest.approx(
        np.linalg.norm(np.linalg.solve(e*np.eye(3)-h[1:, 1:], coupling))**2)


def test_same_three_moments_do_not_identify_causal_kernel():
    u = [Fraction(-2), Fraction(-1), Fraction(1), Fraction(2)]
    d = [1, -2, 2, -1]
    assert all(sum(delta*value**order for delta, value in zip(d, u)) == 0
               for order in range(3))
    assert sum(delta*value**3 for delta, value in zip(d, u)) == -12
    t = np.array([0.5, 1, -1, -0.5])
    plus = DiscreteFeshbachMeasure(t, 0.02*(1+0.2*np.array(d)))
    minus = DiscreteFeshbachMeasure(t, 0.02*(1-0.2*np.array(d)))
    np.testing.assert_allclose(plus.moments(0), minus.moments(0), atol=1e-15)
    assert sum(plus.weights) == pytest.approx(sum(minus.weights))
    assert abs(plus.kernel(0.1)-minus.kernel(0.1)) > 0.001


@pytest.mark.parametrize("reference,width", [(0, 0.2), (0.1, 0.15)])
def test_energy_linearization_bound_against_exact_resolvent(reference, width):
    measure = DiscreteFeshbachMeasure(np.array([-0.5, 0.7, 1.8]),
                                      np.array([0.03, 0.01, 0.08]))
    c, a, _ = measure.moments(reference)
    bound = measure.linearization_bound(reference, width)
    for energy in np.linspace(reference-width, reference+width, 91):
        actual = abs(measure.kernel(energy)-c+a*(energy-reference))
        assert actual <= bound+1e-15


def test_bound_has_correct_energy_units_and_energy_reference_invariance():
    measure = DiscreteFeshbachMeasure(np.array([-0.5, 0.7]), np.array([0.03, 0.01]))
    shifted = DiscreteFeshbachMeasure(measure.energies+2, measure.weights)
    assert measure.kernel(0.1) == pytest.approx(shifted.kernel(2.1))
    scale = 1000.0  # eV -> meV: weights scale as energy squared.
    scaled = DiscreteFeshbachMeasure(measure.energies*scale, measure.weights*scale**2)
    c, a, d = measure.moments(0)
    cs, ass, ds = scaled.moments(0)
    assert cs == pytest.approx(c*scale)
    assert ass == pytest.approx(a)
    assert ds == pytest.approx(d*scale)
    assert scaled.linearization_bound(0, 0.2*scale) == pytest.approx(
        scale*measure.linearization_bound(0, 0.2))


def test_threshold_and_invalid_inputs_cannot_receive_a_false_certificate():
    measure = DiscreteFeshbachMeasure(np.array([0.0, 1.0]), np.ones(2))
    with pytest.raises(ValueError):
        measure.moments(0)
    with pytest.raises(ValueError):
        measure.linearization_bound(0.5, 0.5)
    with pytest.raises(ValueError):
        DiscreteFeshbachMeasure(np.ones(2), np.array([1, -1]))
    with pytest.raises(ValueError):
        covariance_resolvent_error_bound(1, 1)
    with pytest.raises(ValueError):
        mass_root_error_bound(0.1, 0.1, 1, 1, 0)


def test_common_mode_error_certificate_can_be_saturated_by_independent_roots():
    # True common energy is zero. Approximate 2E=delta_s, with mass error
    # delta_m and true mass energy slope ell. Solve both mass equations directly.
    delta_s, delta_m, ell, slope, root = 0.002, 0.001, 0.4, 0.5, 0.2
    true_common_energy = 0.0
    approximate_common_energy = np.linalg.solve(np.array([[2.0]]), [delta_s])[0]
    true_root = root-ell*true_common_energy/slope
    approximate_root = root-(ell*approximate_common_energy+delta_m)/slope
    bound = mass_root_error_bound(delta_s, delta_m, 2, ell, slope)
    assert abs(approximate_root-true_root) == pytest.approx(bound)


def test_covariance_bound_controls_independent_dense_disorder_average():
    h0 = np.array([[0.2, 0.04], [0.04, -0.3]])
    w = np.array([[0.02, 0.01], [0.01, -0.03]])
    z = 1.2+0.1j
    g0 = np.linalg.inv(z*np.eye(2)-h0)
    exact = sum(np.linalg.inv(z*np.eye(2)-h0-sign*w) for sign in [-1, 1])/2
    born = w@g0@w
    candidate = np.linalg.inv(z*np.eye(2)-h0-born)
    distance = min(abs(z-np.linalg.eigvalsh(h0)))
    bound = covariance_resolvent_error_bound(np.linalg.norm(w, 2), distance)
    assert np.linalg.norm(exact-candidate, 2) < bound


def test_hidden_interaction_has_exactly_vanishing_endpoint_jets():
    # Direct expansion of a balanced six-neighbor event, independent exact ints.
    r, n, order = 3, 6, 2
    coefficients = [0]*(n+1)
    for j in range(r+1):
        coefficients[r+j] = comb(n, r)*comb(r, j)*(-1)**j
    for derivative in range(order+1):
        at_zero = coefficients[derivative]
        at_one = sum(coefficients[j]*np.prod(range(j-derivative+1, j+1))
                     for j in range(derivative, n+1))
        assert at_zero == at_one == 0
    assert sum(Fraction(c, 2**j) for j, c in enumerate(coefficients)) > 0


def test_atomic_cpa_has_exact_binary_resolvent_limit():
    # Independent algebraic substitution in CPA, with no root-selection solver.
    for x in [0, 0.17, 0.5, 1]:
        z, uh, uc = 0.2+0.1j, -0.3, 0.8
        average = (1-x)/(z-uh)+x/(z-uc)
        sigma = z-1/average
        th = (uh-sigma)/(1-(uh-sigma)*average)
        tc = (uc-sigma)/(1-(uc-sigma)*average)
        residual = abs((1-x)*th+x*tc)
        cancellation_scale = 1+abs((1-x)*th)+abs(x*tc)
        assert residual < 50*np.finfo(float).eps*cancellation_scale


def test_hidden_tetrahedron_changes_exact_spectrum_but_no_single_impurity():
    x, z, strength = 0.5, 0.2+0.1j, 0.07
    baseline, changed = 0j, 0j
    for configuration in product((0, 1), repeat=4):
        n = sum(configuration)
        energy = -0.3+1.1*n/4
        shift = strength if n == 2 else 0
        # Both pure and either dilute single-substitution environment coincide.
        if n in (0, 1, 3, 4):
            assert shift == 0
        probability = x**n*(1-x)**(4-n)
        baseline += probability/(z-energy)
        changed += probability/(z-energy-shift)
    expected = 6*x**2*(1-x)**2*(1/(z-0.25-strength)-1/(z-0.25))
    assert changed-baseline == pytest.approx(expected, abs=2e-15)
    assert abs(changed-baseline) > 0.5
    assert comb(4, 2) > max(comb(4, n) for n in (0, 1, 3, 4))
