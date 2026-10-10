import json
from pathlib import Path

import numpy as np
import pytest

from mct_research.sp3d5 import BinaryModel, bond_matrix, d_tensors, host_embedding, onsite, star_embedding, star_potential


@pytest.fixture
def parameters():
    return json.loads((Path(__file__).parents[1] / "data/materials/schindler2012_sp3d5.json").read_text())


def test_d_tensor_normalization_and_axial_bond_channels(parameters):
    q = d_tensors()
    np.testing.assert_allclose(np.einsum("iab,jab->ij", q, q), np.eye(5), atol=1e-14)
    p = parameters["HgTe"]
    h = bond_matrix(p, np.array([0, 0, 1]))[:9, :9]
    assert h[0, 8] == pytest.approx(p["sd"])
    assert h[3, 8] == pytest.approx(p["pd_sigma"])
    assert h[1, 6] == pytest.approx(p["pd_pi"])
    assert h[2, 5] == pytest.approx(p["pd_pi"])
    assert h[8, 3] == pytest.approx(-p["dp_sigma"])


def test_atomic_soc_convention_matches_j_multiplets(parameters):
    p = dict(parameters["CdTe"])
    h = onsite(p, "a")
    indices = [1, 2, 3, 10, 11, 12]
    eigenvalues = np.linalg.eigvalsh(h[np.ix_(indices, indices)])
    np.testing.assert_allclose(eigenvalues, [p["a_p"] - 2 * p["a_soc"]] * 2 + [p["a_p"] + p["a_soc"]] * 4)


def test_binary_bands_match_published_targets_without_alloy_input(parameters):
    for name, gap, xvb, xcb, lvb, lcb in (
        ("HgTe", -0.30, -1.72, 3.14, -0.85, 1.28),
        ("CdTe", 1.60, -0.80, 4.54, -0.40, 3.73),
    ):
        m = BinaryModel(parameters[name])
        sec = m.gamma_sectors()
        assert sec["E6"] - sec["E8"] == pytest.approx(gap, abs=0.005)
        assert sec["states6"].shape == (36, 2)
        assert sec["states8"].shape == (36, 4)
        ex = np.linalg.eigvalsh(m.bloch(2 * np.pi * np.array([1, 0, 0]))) - sec["E8"]
        el = np.linalg.eigvalsh(m.bloch(2 * np.pi * np.array([.5, .5, .5]))) - sec["E8"]
        np.testing.assert_allclose([ex[16], ex[18], el[16], el[18]], [xvb, xcb, lvb, lcb], atol=0.025)


def test_host_time_reversal_and_impurity_uniform_sum(parameters):
    h, c = BinaryModel(parameters["HgTe"], -1.54), BinaryModel(parameters["CdTe"], -1.56)
    v = star_potential(h, c)
    spin_flip = np.kron(np.array([[0, 1], [-1, 0]]), np.eye(9))
    j = np.zeros((36, 36)); j[:18, :18] = j[18:, 18:] = spin_flip
    for k in (np.zeros(3), np.array([1.1, -2.3, 0.4])):
        hk = h.bloch(k)
        np.testing.assert_allclose(hk, hk.conj().T)
        np.testing.assert_allclose(j @ hk.conj() @ j.T, h.bloch(-k))
        b = star_embedding(k)
        np.testing.assert_allclose(b.conj().T @ v @ b, c.bloch(k) - h.bloch(k), atol=1e-14)


def test_embedded_host_resolvent_high_frequency_sum_rule(parameters):
    embedding = host_embedding(BinaryModel(parameters["HgTe"]), mesh=2)
    np.testing.assert_allclose(embedding.modes @ embedding.modes.conj().T, np.eye(90), atol=2e-14)


def test_gamma_sector_tracking_at_exact_vca_crossing(parameters):
    def model(x):
        p = {k: (1 - x) * parameters["HgTe"][k] + x * parameters["CdTe"][k] for k in parameters["HgTe"]}
        return BinaryModel(p)
    lo, hi = 0, 1
    for _ in range(55):
        x = (lo + hi) / 2
        sec = model(x).gamma_sectors()
        if sec["E6"] < sec["E8"]:
            lo = x
        else:
            hi = x
    sec = model((lo + hi) / 2).gamma_sectors()
    assert abs(sec["E6"] - sec["E8"]) < 1e-13
    assert sec["states6"].shape[1] == 2
    assert sec["states8"].shape[1] == 4
    np.testing.assert_allclose(sec["states6"].conj().T @ sec["states8"], np.zeros((2, 4)), atol=1e-14)
