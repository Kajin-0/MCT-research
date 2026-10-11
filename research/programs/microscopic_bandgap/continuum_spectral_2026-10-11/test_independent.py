"""Small exact baths and causal counterexamples; no material fit or native jobs.

Tests evaluate independent dense resolvents, analytic continuum transforms and
quadrature against the written bounds. Passing them is not a proof of material
input availability, or a numerical replacement for the proofs in bounds.md.
"""

from fractions import Fraction
import hashlib
import json
from math import atan, log, pi, sqrt
from pathlib import Path
import re

import numpy as np
import pytest


def poisson(e, t, eta):
    return eta / (pi * ((np.asarray(e) - t)**2 + eta**2))


def poisson_prime(e, t, eta):
    u = np.asarray(e) - t
    return -2*eta*u / (pi*(u*u + eta*eta)**2)


def uniform_green(z, half_width=2.0):
    return (np.log(z+half_width)-np.log(z-half_width))/(2*half_width)


def uniform_spectrum(e, eta, half_width=2.0):
    return (np.arctan((half_width-e)/eta) +
            np.arctan((half_width+e)/eta))/(2*pi*half_width)


def integration_rule(width, reference=0.0):
    nodes, weights = np.polynomial.legendre.leggauss(160)
    return reference+width*nodes, width*weights


def window(e, width, reference=0.0):
    u = (np.asarray(e)-reference)/width
    result = np.zeros_like(u)
    inside = abs(u) < 1
    result[inside] = np.exp(1-1/(1-u[inside]**2))
    return result


def moments(spectrum, width, reference=0.0):
    e, w = integration_rule(width, reference)
    chi = window(e, width, reference)
    weighted = w*chi*spectrum(e)
    m = np.sum(weighted)
    n = np.sum((e-reference)*weighted)
    return m, n, reference+n/m


def bisect(function, lo, hi):
    flo, fhi = function(lo), function(hi)
    assert flo*fhi < 0
    for _ in range(55):
        mid = (lo+hi)/2
        fm = function(mid)
        if flo*fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo+hi)/2


def test_dense_bath_measure_normalization_feshbach_and_causality():
    bath = np.diag([-0.8, 0.25, 1.1])
    coupling = np.array([0.07, 0.10, 0.04])
    h = np.zeros((4, 4))
    h[0, 0], h[1:, 1:] = 0.03, bath
    h[0, 1:] = h[1:, 0] = coupling
    energies, vectors = np.linalg.eigh(h)
    weights = abs(vectors[0, :])**2
    assert sum(weights) == pytest.approx(1)
    assert np.dot(weights, energies) == pytest.approx(h[0, 0])
    for z in [0.0+0.08j, 0.25+0.05j, -0.4+0.2j]:
        dense = np.linalg.inv(z*np.eye(4)-h)[0, 0]
        spectral = np.sum(weights/(z-energies))
        kernel = coupling @ np.linalg.solve(z*np.eye(3)-bath, coupling)
        assert dense == pytest.approx(spectral, abs=2e-14)
        assert dense == pytest.approx(1/(z-h[0, 0]-kernel), abs=2e-14)
        assert dense.imag < 0 and kernel.imag < 0
        assert abs(dense) <= 1/z.imag


def test_continuum_transform_inside_support_against_quadrature():
    nodes, w = np.polynomial.legendre.leggauss(160)
    length = 2.0
    for z in [0.0+0.2j, 0.3+0.3j]:
        direct = np.sum(w/(z-length*nodes))/2
        assert direct == pytest.approx(uniform_green(z, length), abs=2e-12)
        assert -direct.imag/pi == pytest.approx(
            uniform_spectrum(z.real, z.imag, length), abs=2e-12)
        assert direct.imag < 0


def test_operator_projector_and_law_errors_bound_dense_derivatives():
    h = np.array([[0.1, 0.04], [0.04, -0.2]])
    dh = np.array([[0.001, -0.0004], [-0.0004, 0.0007]])
    theta = 0.002
    v = np.array([np.cos(theta), np.sin(theta)])
    rho, rhot = np.diag([1.0, 0.0]), np.outer(v, v)
    delta, q = np.linalg.norm(dh, 2), np.linalg.norm(rho-rhot, "nuc")
    eta, z = 0.12, 0.05+0.12j
    r, rt = np.linalg.inv(z*np.eye(2)-h), np.linalg.inv(z*np.eye(2)-h-dh)
    for k in [0, 1]:
        factor = 1 if k == 0 else -1
        actual = abs(factor*np.trace(rho @ np.linalg.matrix_power(r, k+1)) -
                     factor*np.trace(rhot @ np.linalg.matrix_power(rt, k+1)))
        bound = (k+1)*delta/eta**(k+2)+q/eta**(k+1)  # k! = 1 here
        assert actual <= bound
    g1, g2 = np.trace(rho@r), np.trace(rho@rt)
    probability_change = 0.003
    assert abs(probability_change*(g1-g2)) <= 2*probability_change/eta


def test_measure_tv_and_transport_bound_functional_quadrature():
    eta, width = 0.12, 2.0
    e, w = integration_rule(width)
    f = window(e, width)*np.sin(e)
    s, shift = 0.003, 0.02
    changed_weight = s*(poisson(e, 0.7, eta)-poisson(e, -0.4, eta))
    assert abs(np.sum(w*f*changed_weight)) <= 2*s  # ||f||inf <= 1
    moved_atom = poisson(e, 0.2+shift, eta)-poisson(e, 0.2, eta)
    # Direct derivative of this smooth bounded f is safely bounded by 4.
    assert abs(np.sum(w*f*moved_atom)) < 4*shift


def test_tail_certificate_protects_window_but_not_unbounded_moment():
    eta, sigma, margin = 0.1, 0.02, 0.5
    e = np.linspace(-0.5, 0.5, 41)
    tail = sigma*(0.4*poisson(e, -2, eta)+0.6*poisson(e, 3, eta))
    assert np.max(tail) <= sigma*eta/(pi*(margin**2+eta**2))
    derivative = sigma*(0.4*poisson_prime(e, -2, eta)+
                        0.6*poisson_prime(e, 3, eta))
    assert np.max(abs(derivative)) <= 2*sigma*eta/(pi*margin**3)
    # The original (unsmoothed) measure has a perfectly finite but huge moment.
    far_energy = 1e8
    assert sigma*far_energy > 1e6
    assert 2*sigma < 0.1  # small measure TV does not bound that moment


def test_centroid_bound_using_independent_spectral_value_errors():
    width, eta, shift = 1.5, 0.12, 0.0003
    exact = lambda e: 0.8*poisson(e, 0.2, eta)+0.2*uniform_spectrum(e, eta)
    changed = lambda e: 0.8*poisson(e, 0.2+shift, eta)+0.2*uniform_spectrum(e, eta)
    m, n, c = moments(exact, width)
    mt, nt, ct = moments(changed, width)
    e, w = integration_rule(width)
    chi = window(e, width)
    error_a = 0.8*shift/(pi*eta**2)  # dense resolvent identity, scalar shift
    error_m, error_n = np.sum(w*chi)*error_a, np.sum(w*abs(e)*chi)*error_a
    floor = mt-error_m
    assert floor > 0.1
    assert abs(m-mt) <= error_m and abs(n-nt) <= error_n
    assert abs(c-ct) <= (error_n+width*error_m)/floor


def test_resolution_error_has_logarithmic_obstruction_and_finite_eta_budget():
    eta = 0.01
    # Exact integral for f=min(|E|,1) against a Cauchy measure at zero.
    exact = eta/pi*log(1+1/eta**2)+2/pi*atan(eta)
    written_bound = eta/pi*log(1+1/eta**2)+4/pi*atan(eta)
    assert exact <= written_bound
    finer = 1e-8
    fine_value = finer/pi*log(1+1/finer**2)+2/pi*atan(finer)
    assert fine_value/finer > 3*exact/eta
    e, w = integration_rule(1.5)
    f = window(e, 1.5)
    eta2 = 0.012
    actual = abs(np.sum(w*f*(poisson(e, 0.2, eta)-poisson(e, 0.2, eta2))))
    assert actual <= abs(log(eta/eta2))


def test_no_mass_floor_allows_order_one_conditional_centroid_shift():
    eta, width, s = 0.1, 1.5, 1e-5
    far = 1e6
    a = lambda e: (1-s)*poisson(e, far, eta)+s*poisson(e, -1, eta)
    b = lambda e: (1-s)*poisson(e, far, eta)+s*poisson(e, 1, eta)
    ma, _, ca = moments(a, width)
    mb, _, cb = moments(b, width)
    assert max(ma, mb) < s
    assert cb-ca > 1.5
    assert 2*s < 1e-4


def test_equal_full_centroids_and_endpoint_jets_do_not_fix_window_ordering():
    eta, width, b = 0.08, 1.5, 0.05
    plus = lambda e: b*uniform_spectrum(e, eta)+(1-b)*(
        0.8*poisson(e, 1, eta)+0.2*poisson(e, -4, eta))
    minus = lambda e: b*uniform_spectrum(e, eta)+(1-b)*(
        0.8*poisson(e, -1, eta)+0.2*poisson(e, 4, eta))
    assert Fraction(4, 5)-4*Fraction(1, 5) == 0
    m1, _, c1 = moments(plus, width)
    m2, _, c2 = moments(minus, width)
    assert m1 == pytest.approx(m2)
    assert c1 == pytest.approx(-c2)
    assert c1 > 0.6 and c2 < -0.6
    # h=16*x^2*(1-x)^2 has exact zero value/first derivative at both ends.
    coefficients = [0, 0, 16, -32, 16]
    assert sum(coefficients) == sum(i*a for i, a in enumerate(coefficients)) == 0
    assert coefficients[0] == coefficients[1] == 0


def test_isolated_peak_height_and_derivative_certificates():
    eta, shift = 0.2, 1e-5
    radius = eta/4
    isolation = poisson(0, 0, eta)-poisson(radius, 0, eta)
    error0, error1 = shift/(pi*eta**2), 2*shift/(pi*eta**3)
    kappa = 2*eta*(eta**2-3*radius**2)/(pi*(eta**2+radius**2)**3)
    assert 2*error0 < isolation
    # Independent stationary roots: no implementation of the written bound.
    actual_peak = bisect(lambda e: poisson_prime(e, shift, eta), -radius, radius)
    assert actual_peak == pytest.approx(shift, abs=1e-14)
    assert abs(actual_peak) <= 2*sqrt(error0/kappa)
    assert abs(actual_peak) <= error1/kappa


def test_curved_but_tied_peaks_switch_under_tiny_causal_error():
    eta, s = 0.08, 1e-6
    e = np.linspace(-1.2, 1.2, 2401)
    a = (0.5+s)*poisson(e, -1, eta)+(0.5-s)*poisson(e, 1, eta)
    b = (0.5-s)*poisson(e, -1, eta)+(0.5+s)*poisson(e, 1, eta)
    assert e[np.argmax(a)] < -0.9 and e[np.argmax(b)] > 0.9
    assert np.max(abs(a-b)) <= 4*s/(pi*eta)
    tied = (poisson(e, -1, eta)+poisson(e, 1, eta))/2
    assert tied[np.argmin(abs(e+1))] == pytest.approx(tied[np.argmin(abs(e-1))])


def test_peak_and_real_inverse_root_differ_inside_a_causal_continuum():
    eta, b = 0.1, 0.05
    def green(e):
        z = e+1j*eta
        return b*uniform_green(z)+(1-b)*(0.8/z+0.2/(z-0.5))
    def derivative(e):
        uniform_prime = eta/(4*pi)*(1/(eta**2+(2+e)**2)-
                                      1/(eta**2+(2-e)**2))
        return b*uniform_prime+(1-b)*(
            0.8*poisson_prime(e, 0, eta)+0.2*poisson_prime(e, 0.5, eta))
    peak = bisect(derivative, -0.03, 0.03)
    inverse_root = bisect(lambda e: (1/green(e)).real, -0.03, 0.03)
    assert inverse_root-peak > 0.003
    assert green(peak).imag < 0


def test_finite_eta_does_not_distinguish_an_atom_from_a_narrow_continuum():
    h, eta = 0.001, 0.1
    z = 0.03+1j*eta
    actual = uniform_green(z, h)
    assert abs(actual-1/z) <= h*h/(3*eta**3)
    # Same causal family, two different joint volume/resolution limits.
    n = 1e6
    assert poisson(0, 1/n, n**(-3)) < 1e-5
    assert poisson(0, 1/n, n**(-0.5)) > 100


def test_composition_root_budget_and_tangency_counterexample():
    root, slope, error = 0.23, 0.8, 0.001
    changed_root = bisect(lambda x: slope*(x-root)+error, 0.1, 0.4)
    assert abs(changed_root-root) == pytest.approx(error/slope)
    small = 1e-9
    tangent_root = root+(small/slope)**(1/3)
    assert slope*(tangent_root-root)**3 == pytest.approx(small)
    assert tangent_root-root > 1e5*small


def test_gauge_reference_units_and_physical_copy_ambiguity():
    h = np.diag([0.2, -0.3])
    angle = 0.2
    u = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    rho = np.diag([1.0, 0.0])
    z = 0.05+0.12j
    g = np.trace(rho@np.linalg.inv(z*np.eye(2)-h))
    rotated = np.trace((u@rho@u.T)@np.linalg.inv(z*np.eye(2)-u@h@u.T))
    assert g == pytest.approx(rotated)
    # Changing the physical injection, rather than rotating both, changes it.
    assert abs(np.trace((u@rho@u.T)@h)-np.trace(rho@h)) > 0.01
    eta, width = 0.1, 1.5
    c = moments(lambda e: poisson(e, 0.2, eta), width)[2]
    shifted = moments(lambda e: poisson(e, 2.2, eta), width, reference=2)[2]
    assert shifted-c == pytest.approx(2)
    scaled = moments(lambda e: poisson(e, 200, 100), 1500)[2]
    assert scaled == pytest.approx(1000*c)


def test_identical_gamma_matrices_leave_a_global_topology_degree_undetermined():
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]])
    sz = np.diag([1.0, -1.0])
    def h(kx, ky, c):
        return np.sin(kx)*sx+np.sin(ky)*sy+(1-c*(2-np.cos(kx)-np.cos(ky)))*sz
    np.testing.assert_array_equal(h(0, 0, 0), h(0, 0, 1))
    # Preimages of the north pole are among the four sin-zero momenta.
    degree = []
    for c in [0, 1]:
        count = 0
        for kx, ky in [(0, 0), (pi, 0), (0, pi), (pi, pi)]:
            z_mass = h(kx, ky, c)[0, 0].real
            assert abs(z_mass) >= 1
            if z_mass > 0:
                count += int(round(np.cos(kx)*np.cos(ky)))
        degree.append(count)
    assert degree == [0, 1]


def test_package_links_and_scope_controls():
    package = Path(__file__).resolve().parent
    for path in package.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (path.parent/target.split("#", 1)[0]).resolve().is_file(), target
    assert "MATERIAL NO-GO" in (package/"cycles_and_decision.md").read_text()
    assert "Sharp inversion remains **OPEN**" in (package/"foundation.md").read_text()


def test_prior_results_remain_byte_identical():
    package = Path(__file__).resolve().parent
    root = package.parents[3]
    ledger = json.loads((package/"provenance.json").read_text())
    assert ledger["analytic_cycles"] == 3
    assert ledger["physical_xc"] is ledger["new_material_ordering_interval"] is None
    assert all(value == 0 for value in ledger["declared_controls"].values())
    for record in ledger["preserved_inputs"]:
        data = (root/record["path"]).read_bytes()
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
