"""Independent integrals, Hermitian baths and falsification of R07 certificates."""

import math

import numpy as np
import pytest

from mct_research.analytical_gap_closure import DiscreteFeshbachMeasure
from mct_research.threshold_causal_closure import (
    causal_mass_root_error_bound,
    positive_quadratic_envelope_kernel,
    quadratic_threshold_kernel,
    subleading_density_remainder_bound,
)
from mct_research.threshold_impurity import below_edge_green_prime, scalar_t_below_edge


def quadrature_integral(function, cutoff=1.0):
    # epsilon=u^2 removes the half-power endpoint singularity.
    nodes, weights = np.polynomial.legendre.leggauss(180)
    u = (nodes+1)*math.sqrt(cutoff)/2
    return np.sum(weights*math.sqrt(cutoff)/2 * 2*u * function(u*u))


@pytest.mark.parametrize("orientation", [-1, 1])
def test_threshold_kernel_against_independent_retarded_quadrature(orientation):
    edge, cutoff, c = 0.3, 0.7, 0.2
    for z in [edge-orientation*0.05, edge+0.03+0.06j, edge-0.1+0.02j]:
        direct = quadrature_integral(
            lambda e: c*np.sqrt(e)/(z-edge-orientation*e), cutoff)
        actual = quadratic_threshold_kernel(z, edge, cutoff, c, orientation)
        assert actual == pytest.approx(direct, rel=2e-12, abs=2e-14)
        if np.imag(z) > 0:
            assert actual.imag < 0
    assert quadratic_threshold_kernel(edge, edge, cutoff, c, orientation) == pytest.approx(
        -orientation*2*c*math.sqrt(cutoff))


def test_extracted_fractional_term_has_uniform_analytic_cutoff_remainder():
    c, cutoff, h = 0.2, 0.7, 0.08
    bound = c*h*h*cutoff**(-1.5)/(1.5*(1-h/cutoff))
    for a in [0, 1e-10, 0.01, h, 0.04-0.02j]:
        k = quadratic_threshold_kernel(-a, 0, cutoff, c)
        extracted = -2*c*math.sqrt(cutoff)+math.pi*c*np.sqrt(a)-2*c*a/math.sqrt(cutoff)
        assert abs(k-extracted) <= bound+1e-15
    # The exact derivative diverges; the cutoff remainder remains bounded.
    assert -below_edge_green_prime(1e-12) > 1e6


@pytest.mark.parametrize("p", [1.5, 2.0, 2.5])
def test_uniform_subleading_bound_by_independent_integral(p):
    b, cutoff = 0.3, 0.7
    for delta in [0.001, 0.01, 0.08]:
        remainder = quadrature_integral(
            lambda e: b*delta**2*e**(p-2)/(e+delta), cutoff)
        assert remainder <= subleading_density_remainder_bound(delta, b, p, cutoff)*(1+2e-12)
    assert subleading_density_remainder_bound(0, b, p, cutoff) == 0


def test_lower_envelope_restores_positive_measure_causality():
    c, b, cutoff = 0.2, 0.05, 0.7
    for z in [-0.01, 0.1+0.06j, -0.03+0.02j]:
        direct = quadrature_integral(lambda e: (c*np.sqrt(e)-b*e**1.5)/(z-e), cutoff)
        envelope = positive_quadratic_envelope_kernel(z, 0, cutoff, c, b)
        assert envelope == pytest.approx(direct, rel=2e-12)
        if np.imag(z) > 0:
            assert envelope.imag < 0
    # Worst allowed true density is the upper envelope. Its residual density
    # is 2B epsilon**(3/2), with finite first moment but divergent second moment.
    delta = 0.03
    actual_remainder = quadrature_integral(
        lambda e: 2*b*delta**2/np.sqrt(e)/(e+delta), cutoff)
    assert actual_remainder <= subleading_density_remainder_bound(delta, 2*b, 1.5, cutoff)


def test_secant_mass_contraction_on_a_threshold_endpoint():
    # No finite mass Lipschitz constant exists on this closed interval.
    for energy in [-1e-4, -1e-8, -1e-12]:
        k6 = quadratic_threshold_kernel(energy, 0, 1, 0.3)
        k6_edge = quadratic_threshold_kernel(0, 0, 1, 0.3)
        delta_k6 = (k6_edge-k6).real
        delta_fs = -energy-delta_k6/2
        delta_mass = delta_k6/2
        assert abs(delta_mass) <= abs(delta_fs)
        assert abs(delta_mass/delta_fs) < 1
    # The ratio tends to 1 even though both derivative factors diverge.
    assert abs(delta_mass/delta_fs) > 0.99999


def test_branch_residual_bound_against_an_independent_dense_bath_root():
    energies, couplings = np.array([0.2, 0.7]), np.array([0.13, 0.09])
    bath = np.diag(energies)
    def kernel(e):
        return float(couplings @ np.linalg.solve(e*np.eye(2)-bath, couplings))
    e6, e8 = -0.15, -0.11
    lo, hi = -0.5, 0.0
    for _ in range(70):
        e = (lo+hi)/2
        fs = e-(e6+e8)/2-kernel(e)/2
        if fs < 0:
            lo = e
        else:
            hi = e
    true_energy = (lo+hi)/2
    candidate_energy = true_energy+0.002
    d6 = candidate_energy-e6-kernel(candidate_energy)
    d8 = candidate_energy-e8
    true_mass = (e6-e8+kernel(true_energy))/2
    fs_candidate, mass_candidate = (d6+d8)/2, (d8-d6)/2
    secant = ((kernel(candidate_energy)-kernel(true_energy))/2) / fs_candidate
    assert -1 <= secant <= 1
    assert true_mass == pytest.approx(mass_candidate-secant*fs_candidate)
    assert abs(true_mass) <= max(abs(d6), abs(d8))
    assert causal_mass_root_error_bound(abs(d6), abs(d8), 0.5) == max(abs(d6), abs(d8))/0.5


def test_finite_causal_continuum_falsifies_off_support_contraction():
    # Positive bounded bath density b on [-L,L]; interior Re K is increasing.
    b, length, energy = 0.9, 1.0, 0.001
    k = b*math.log((length+energy)/(length-energy))
    fs, mass = energy-k/2, k/2
    assert fs > 0
    assert abs(mass) > 8*abs(fs)
    # Direct continuum Cauchy integral is causal, not an arbitrary analytic toy.
    z = 0.01+0.1j
    nodes, weights = np.polynomial.legendre.leggauss(180)
    assert np.sum(weights*b/(z-nodes)).imag < 0


def test_root_certificate_is_sharp_in_a_divergent_threshold_limit():
    # Exact common root at the finite edge limit, with an otherwise linear
    # composition mass. Shift both candidate coherent energies equally, so
    # both branch residuals have magnitude eps but the mass has no direct error.
    c, v, root = 0.3, 0.8, 0.25
    edge_kernel = quadratic_threshold_kernel(0, 0, 1, c).real
    for detuning in [1e-6, 1e-10, 1e-12]:
        candidate_energy = -detuning
        kernel = quadratic_threshold_kernel(candidate_energy, 0, 1, c).real
        fs = candidate_energy+edge_kernel/2-kernel/2
        eps = -fs
        candidate_root = root-(kernel-edge_kernel)/(2*v)
        assert abs(candidate_root-root) <= causal_mass_root_error_bound(eps, eps, v)
    assert abs(candidate_root-root)/causal_mass_root_error_bound(eps, eps, v) > 0.99999


def test_cubic_mass_tangency_falsifies_uniform_linear_root_error():
    v, root = 0.8, 0.2
    errors = np.array([1e-3, 1e-6, 1e-9])
    shifted_roots = root+(errors/v)**(1/3)
    np.testing.assert_allclose(v*(shifted_roots-root)**3, errors, rtol=2e-12)
    assert (shifted_roots-root)[-1]/errors[-1] > 1e5


def test_fixed_ir_and_equal_regular_moments_still_have_distinct_crossings():
    reference = 0.3  # Match the IR threshold: exactly the regular moments in T9.
    t = reference+np.array([0.5, 1, -1, -0.5])
    null = np.array([1, -2, 2, -1])
    baths = [DiscreteFeshbachMeasure(t, 0.02*(1+s*0.2*null)) for s in [-1, 1]]
    np.testing.assert_allclose(baths[0].moments(reference), baths[1].moments(reference), atol=1e-15)
    ev, v, x0 = 0.1, 0.8, 0.23
    ir = quadratic_threshold_kernel(ev, 0.3, 0.4, 0.04).real
    roots = []
    for measure in baths:
        total = ir+measure.kernel(ev).real
        lo, hi = 0.2, 0.3
        for _ in range(70):
            x = (lo+hi)/2
            if 2*v*(x-x0)+x*(1-x)*total < 0:
                lo = x
            else:
                hi = x
        roots.append((lo+hi)/2)
    assert abs(roots[0]-roots[1]) > 1e-4


def test_threshold_resonance_changes_the_power_and_invalidates_finite_static_input():
    # g0=-3, so v=1/g0 is a threshold resonance in the unit-bandwidth host.
    delta = np.array([1e-8, 1e-10, 1e-12])
    scaled_t = scalar_t_below_edge(delta, -1/3)*np.sqrt(delta)
    np.testing.assert_allclose(scaled_t, -2/(3*math.pi), rtol=8e-5)


def test_units_reference_shifts_and_invalid_certificate_guards():
    z, edge, cutoff, c = -0.1+0.03j, 0.2, 0.7, 0.4
    actual = quadratic_threshold_kernel(z, edge, cutoff, c)
    assert quadratic_threshold_kernel(z+2, edge+2, cutoff, c) == pytest.approx(actual)
    scale = 1000.0
    assert quadratic_threshold_kernel(z*scale, edge*scale, cutoff*scale,
                                      c*math.sqrt(scale)) == pytest.approx(scale*actual)
    assert subleading_density_remainder_bound(0.01*scale, 0.3*scale**(-0.5),
                                              1.5, cutoff*scale) == pytest.approx(
        scale*subleading_density_remainder_bound(0.01, 0.3, 1.5, cutoff))
    with pytest.raises(ValueError):
        subleading_density_remainder_bound(0.01, 1, 1, 1)
    with pytest.raises(ValueError):
        positive_quadratic_envelope_kernel(-0.1, 0, 1, 0.1, 0.2)
    with pytest.raises(ValueError):
        quadratic_threshold_kernel(0.1, 0, 1, 0.2)
    with pytest.raises(ValueError):
        causal_mass_root_error_bound(0.01, 0.01, 0)
