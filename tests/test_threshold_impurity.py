import numpy as np
import pytest

from mct_research.threshold_impurity import (
    below_edge_green, below_edge_green_prime, dilute_pole_below_edge,
    scalar_t_below_edge, threshold_t,
)


def test_closed_green_function_against_independent_quadrature():
    # Substitute epsilon=t^2 to remove the integrable threshold singularity.
    nodes, weights = np.polynomial.legendre.leggauss(180)
    t = (nodes + 1) / 2
    w = weights / 2
    for delta in [0.01, 0.1, 1.0]:
        g = np.sum(w * -3 * t**2 / (delta + t**2))
        gp = np.sum(w * -3 * t**2 / (delta + t**2)**2)
        assert below_edge_green(delta) == pytest.approx(g, rel=1e-12)
        assert below_edge_green_prime(delta) == pytest.approx(gp, rel=1e-12)


def test_finite_t_and_divergent_positive_dynamic_susceptibility():
    v = -0.1
    t0 = threshold_t(v)
    delta = np.array([1e-8, 1e-10, 1e-12])
    t = scalar_t_below_edge(delta, v)
    a = -t**2 * below_edge_green_prime(delta)
    assert np.all(a > 0)
    # -T' ~ (3pi/4) T0^2 / sqrt(delta), for unit bandwidth.
    np.testing.assert_allclose(a * np.sqrt(delta), 3 * np.pi / 4 * t0**2, rtol=4e-4)
    np.testing.assert_allclose(t[-1], t0, rtol=1e-6)


def test_dilute_pole_has_x_three_halves_remainder_not_bounded_x_squared():
    v = -0.1
    t0 = threshold_t(v)
    expected = 3 * np.pi / 2 * t0**2 * np.sqrt(-t0)
    x = np.array([1e-6, 1e-8, 1e-10])
    e = np.array([dilute_pole_below_edge(float(c), v) for c in x])
    remainder = e - x * t0
    np.testing.assert_allclose(remainder / x**1.5, expected, rtol=1e-3)
    assert (remainder / x**2)[-1] > 90 * (remainder / x**2)[0]
