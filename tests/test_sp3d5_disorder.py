import json
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("scipy")

from mct_research.sp3d5 import BinaryModel, RECIPROCAL
from mct_research.sp3d5_disorder import (
    PRIMITIVE, lanczos_spectrum, periodic_neighbors, random_occupation,
    supercell_hamiltonian, uniform_gamma_states,
)


@pytest.fixture
def models():
    p = json.loads((Path(__file__).parents[1] / "data/materials/schindler2012_sp3d5.json").read_text())
    raw = {n: BinaryModel(p[n]) for n in ["HgTe", "CdTe"]}
    return [BinaryModel(p[n], -raw[n].gamma_sectors()["E8"] - (.4 if n == "CdTe" else 0)) for n in raw]


def test_neighbor_geometry_and_pure_bloch_cell(models):
    h, c = models
    neighbors = periodic_neighbors(2)
    assert all(np.unique(neighbors[:, mu]).size == 8 for mu in range(4))
    for eta, model in [(0, h), (1, c)]:
        full = supercell_hamiltonian(h, c, 2, np.full(8, eta)).toarray()
        kpoints = np.array([[a, b, d] for a in [0, .5] for b in [0, .5] for d in [0, .5]]) @ RECIPROCAL
        expected = np.sort(np.concatenate([np.linalg.eigvalsh(model.bloch(k)) for k in kpoints]))
        np.testing.assert_allclose(np.linalg.eigvalsh(full), expected, atol=4e-14)


def test_one_cell_recovers_binary_gamma_and_positive_resolvent(models):
    h, c = models
    for eta, m in [(0, h), (1, c)]:
        full = supercell_hamiltonian(h, c, 1, np.array([eta])).toarray()
        np.testing.assert_allclose(full, m.bloch(np.zeros(3)), atol=1e-14)
        a = m.gamma_sectors()["states6"][:, 0]
        spectrum = lanczos_spectrum(full, a, 30)
        assert len(spectrum.diagonal) == 1
        assert spectrum.green(0.3 + .1j).imag < 0


def test_exact_spectral_centroid_is_vca_for_each_configuration(models):
    h, c = models
    eta = random_occupation(2, .3, 412)
    x = eta.mean()
    m = BinaryModel({k: (1-x)*h.parameters[k] + x*c.parameters[k] for k in h.parameters}, (1-x)*h.shift + x*c.shift)
    full = supercell_hamiltonian(h, c, 2, eta)
    for sector in [6, 8]:
        a = uniform_gamma_states(m.gamma_sectors()[f"states{sector}"], 8)
        expected = m.gamma_sectors()[f"E{sector}"] * np.eye(a.shape[1])
        np.testing.assert_allclose(a.conj().T @ (full @ a), expected, atol=2e-14)


def test_lanczos_matches_exact_random_cell_resolvent(models):
    h, c = models
    full = supercell_hamiltonian(h, c, 2, random_occupation(2, .3, 891))
    a = uniform_gamma_states(h.gamma_sectors()["states6"], 8)[:, 0]
    dense = full.toarray()
    for reorthogonalize in [False, True]:
        spectrum = lanczos_spectrum(full, a, len(a), reorthogonalize=reorthogonalize)
        for z in [.1 + .03j, -.3 + .01j, 2 + .1j]:
            expected = np.vdot(a, np.linalg.solve(z*np.eye(len(a)) - dense, a))
            np.testing.assert_allclose(spectrum.green(z), expected, atol=1e-11)
