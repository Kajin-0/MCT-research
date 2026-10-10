import numpy as np
import pytest

from mct_research.scalar_cpa_threshold import (
    cpa_at_w, cpa_gamma_peak, cpa_inner_green, cpa_lower_edge, host_green, host_green_prime,
    pair_scattering_indicator, threshold_constants,
)
from mct_research.threshold_impurity import below_edge_green, below_edge_green_prime


def test_complex_host_green_matches_independent_quadrature_and_below_edge():
    nodes, weights = np.polynomial.legendre.leggauss(300)
    t, w = (nodes+1)/2, weights/2
    for z in [-.1+0j, .3+.1j, 1.2+.02j, -.003+.001j]:
        g = np.sum(w*3*t*t/(z-t*t))
        gp = np.sum(w*-3*t*t/(z-t*t)**2)
        np.testing.assert_allclose(host_green(z), g, atol=2e-13)
        np.testing.assert_allclose(host_green_prime(z), gp, atol=2e-12)
    assert host_green(-.001).real == pytest.approx(below_edge_green(.001))
    assert host_green_prime(-.001).real == pytest.approx(below_edge_green_prime(.001))
    assert host_green(.1+1e-9j).imag < 0


def test_cpa_solution_satisfies_original_binary_scattering_equation():
    for x in [.001, .02, .08]:
        for w in [-.01, .003+.01j, .3+.1j]:
            sigma, derivative = cpa_at_w(w, x, -.1)
            g = host_green(w)
            condition = (1-x)*(-sigma)/(1+g*sigma)+x*(-.1-sigma)/(1-g*(-.1-sigma))
            assert abs(condition) < 1e-15
            step = 1e-7
            numerical = (cpa_at_w(w+step, x, -.1)[0]-cpa_at_w(w-step, x, -.1)[0])/(2*step)
            np.testing.assert_allclose(derivative, numerical, atol=2e-9)


def test_self_consistent_edge_has_x_squared_not_ata_x_three_halves():
    c = threshold_constants(-.1)
    detuning_errors, energy_errors = [], []
    for x in [1e-3, 1e-4, 1e-5]:
        edge = cpa_lower_edge(x, -.1)
        assert edge["fold_residual"] < 1e-12
        detuning_errors.append(abs(edge["w"]/(x*x)/(-c["a"]**2/4)-1))
        energy_errors.append(abs((edge["energy"]-x*c["t0"])/(x*x)/c["cpa_edge_x2"]-1))
    for errors in [detuning_errors, energy_errors]:
        assert errors[-1] < 1e-4
        assert all(errors[i]/errors[i+1] > 8 for i in range(2))


def test_gamma_peak_matches_distinct_universal_threshold_coefficient():
    c = threshold_constants(-.1)
    peak = cpa_gamma_peak(.0001, -.1)
    assert peak["x2_coefficient"] == pytest.approx(c["gamma_peak_x2"], rel=5e-4)
    edge = cpa_lower_edge(.0001, -.1)
    assert peak["energy"] > edge["energy"]


def test_dilution_does_not_control_pair_indicator_inside_threshold_layer():
    x, v = 1e-4, -.1
    c = threshold_constants(v)
    edge = cpa_lower_edge(x, v)
    peak = cpa_gamma_peak(x, v)
    scaled_energy = (peak["energy"]-x*c["t0"])/(x*x)+1j*peak["external_eta"]/(x*x)
    w_peak = 1/cpa_inner_green(x, scaled_energy, v)
    assert pair_scattering_indicator(edge["w"], x, v) == pytest.approx(1, rel=5e-4)
    assert pair_scattering_indicator(w_peak, x, v) == pytest.approx(np.sqrt(3)/2, rel=5e-4)
