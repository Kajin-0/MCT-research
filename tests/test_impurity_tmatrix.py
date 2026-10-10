import numpy as np
import pytest

from mct_research.impurity_tmatrix import (
    SpectralEmbedding, endpoint_reference_shifts, mass_hermite, t_derivative, t_matrix,
)


def finite_host():
    rng = np.random.default_rng(341)
    a = rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))
    h = (a + a.conj().T) / 4
    e, u = np.linalg.eigh(h)
    p = np.eye(9)[[0, 3, 5]]
    v = np.array([[0.8, 0.1j, 0], [-0.1j, -0.3, 0], [0, 0, 0]])
    return h, p, v, SpectralEmbedding(e, p @ u)


def test_exact_impurity_dyson_identity_against_full_matrix_inverse():
    h, p, v, embedding = finite_host()
    z = 0.3 + 0.23j
    g = embedding.resolvent(z)
    t = t_matrix(v, g)
    perturbed = np.linalg.inv(z * np.eye(9) - h - p.T @ v @ p)
    np.testing.assert_allclose(p @ perturbed @ p.T, g + g @ t @ g, atol=2e-14)
    np.testing.assert_allclose(t, v + v @ g @ t, atol=2e-14)
    np.testing.assert_allclose(t - t.conj().T, t.conj().T @ (g - g.conj().T) @ t, atol=2e-14)
    assert np.linalg.eigvalsh(-(t - t.conj().T) / (2j)).min() > -1e-14


def test_embedded_derivative_retains_propagation_outside_support():
    h, p, v, embedding = finite_host()
    z = 0.3 + 0.23j
    g, gp = embedding.resolvent(z), embedding.resolvent(z, 1)
    full_g = np.linalg.inv(z * np.eye(9) - h)
    np.testing.assert_allclose(gp, -p @ full_g @ full_g @ p.T, atol=2e-14)
    assert np.linalg.norm(gp + g @ g) > 0.1
    step = 2e-6
    tp = t_derivative(t_matrix(v, g), gp)
    numerical = (t_matrix(v, embedding.resolvent(z + step)) - t_matrix(v, embedding.resolvent(z - step))) / (2 * step)
    np.testing.assert_allclose(tp, numerical, rtol=1e-8, atol=1e-9)
    vectors = np.array([[1, 0], [0, 1], [1j, 0.2]])
    np.testing.assert_allclose(embedding.derivative_contraction(z, vectors), vectors.conj().T @ gp @ vectors)


def test_off_continuum_derivative_positive_and_scattering_norm_identity():
    h, p, v, embedding = finite_host()
    z = float(np.linalg.eigvalsh(h).max() + 1)
    t = t_matrix(v, embedding.resolvent(z))
    a = -t_derivative(t, embedding.resolvent(z, 1))
    full_g = np.linalg.inv(z * np.eye(9) - h)
    cloud = full_g @ p.T @ t
    np.testing.assert_allclose(a, cloud.conj().T @ cloud, atol=2e-14)
    assert np.linalg.eigvalsh(a).min() > -1e-14


def test_retarded_real_derivative_is_not_protected_by_causality():
    embedding = SpectralEmbedding(np.array([0.0]), np.ones((1, 1)))
    v = np.array([[0.5]])
    z = 0.5 + 0.05j
    t = t_matrix(v, embedding.resolvent(z))
    assert t.imag[0, 0] < 0
    assert (-t_derivative(t, embedding.resolvent(z, 1))).real[0, 0] < 0


def test_positive_cloud_norm_is_imaginary_part_over_eta_not_real_derivative():
    h, p, v, embedding = finite_host()
    z = 0.3 + 0.23j
    t = t_matrix(v, embedding.resolvent(z))
    full_g = np.linalg.inv(z * np.eye(9) - h)
    cloud = full_g @ p.T @ t
    norm = cloud.conj().T @ cloud
    np.testing.assert_allclose(norm, -(t - t.conj().T) / (2j * z.imag), atol=2e-14)
    a_retarded = -t_derivative(t, embedding.resolvent(z, 1))
    assert np.linalg.norm(norm - (a_retarded + a_retarded.conj().T) / 2) > 0.1


def test_full_impurity_chord_limit_has_no_extra_mass_bowing():
    mh, mc = -0.15, 0.8
    delta = mc - mh
    x = np.linspace(0, 1, 101)
    np.testing.assert_allclose(mass_hermite(x, mh, mc, delta, -delta), mh + delta * x)
    assert endpoint_reference_shifts(delta, -delta, delta) == (0, 0)


def test_full_and_chord_residual_conventions_agree():
    mh, mc, full_h, full_c = -0.15, 0.8, 0.72, -1.12
    delta = mc - mh
    th, tc = endpoint_reference_shifts(full_h, full_c, delta)
    x = np.linspace(0, 1, 101)
    chord_residual_form = mh + delta * x + x * (1 - x) * ((1 - x) * th + x * tc)
    np.testing.assert_allclose(mass_hermite(x, mh, mc, full_h, full_c), chord_residual_form)
    step = 1e-6
    assert (mass_hermite(step, mh, mc, full_h, full_c) - mh) / step == pytest.approx(full_h, abs=2e-6)
    assert (mc - mass_hermite(1 - step, mh, mc, full_h, full_c)) / step == pytest.approx(-full_c, abs=2e-6)
