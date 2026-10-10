"""Diagnostic reconstruction of Schindler (2012), Table 2.2.

9 real orbitals per atom, spin-major ordering, 36 states per primitive cell.
Bloch phases include atomic positions. Distances use a=1 and momenta a^-1.
Binary parameters do not uniquely determine a self-consistent alloy impurity.
"""

from dataclasses import dataclass
from itertools import product

import numpy as np
from numpy.typing import NDArray

from .impurity_tmatrix import SpectralEmbedding


BONDS = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / 4
RECIPROCAL = 2 * np.pi * np.array([[-1, 1, 1], [1, -1, 1], [1, 1, -1]])


def d_tensors() -> NDArray:
    q = np.zeros((5, 3, 3))
    for i, (a, b) in enumerate(((0, 1), (1, 2), (2, 0))):
        q[i, a, b] = q[i, b, a] = 1 / np.sqrt(2)
    q[3] = np.diag([1, -1, 0]) / np.sqrt(2)
    q[4] = np.diag([-1, -1, 2]) / np.sqrt(6)
    return q


def bond_matrix(parameters: dict, direction: NDArray) -> NDArray:
    """Rows: cation orbitals; columns: anion orbitals; direction cation->anion."""
    n = np.asarray(direction) / np.linalg.norm(direction)
    q = d_tensors()
    qn = q @ n
    sigma_d = np.sqrt(1.5) * (qn @ n)
    pi_pd = np.sqrt(2) * (qn - (qn @ n)[:, None] * n).T
    sigma_pd = np.outer(n, sigma_d)
    h = np.zeros((9, 9))
    h[0, 0] = parameters["ss"]
    h[0, 1:4] = parameters["sp"] * n
    h[1:4, 0] = -parameters["ps"] * n
    h[1:4, 1:4] = (parameters["pp_pi"] * np.eye(3)
                      + (parameters["pp_sigma"] - parameters["pp_pi"]) * np.outer(n, n))
    h[0, 4:] = parameters["sd"] * sigma_d
    h[4:, 0] = parameters["ds"] * sigma_d
    h[1:4, 4:] = parameters["pd_sigma"] * sigma_pd + parameters["pd_pi"] * pi_pd
    h[4:, 1:4] = -(parameters["dp_sigma"] * sigma_pd + parameters["dp_pi"] * pi_pd).T
    return np.kron(np.eye(2), h)


def onsite(parameters: dict, sublattice: str, shift: float = 0) -> NDArray:
    p = sublattice
    diagonal = [parameters[p + "_s"]] + [parameters[p + "_p"]] * 3
    diagonal += [parameters[p + "_dt"]] * 3 + [parameters[p + "_de"]] * 2
    h = np.kron(np.eye(2), np.diag(diagonal)).astype(complex)
    # L_i[j,k]=-i epsilon_ijk, H_SO = Delta L.sigma (Eq. 1.15).
    l = np.zeros((3, 9, 9), dtype=complex)
    for axis, (a, b) in enumerate(((2, 3), (3, 1), (1, 2))):
        l[axis, a, b] = -1j
        l[axis, b, a] = 1j
    pauli = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]])
    for axis in range(3):
        h += parameters[p + "_soc"] * np.kron(pauli[axis], l[axis])
    return h + shift * np.eye(18)


@dataclass(frozen=True)
class BinaryModel:
    parameters: dict
    shift: float = 0

    def bloch(self, k: NDArray) -> NDArray:
        h = np.zeros((36, 36), dtype=complex)
        h[:18, :18] = onsite(self.parameters, "c", self.shift)
        h[18:, 18:] = onsite(self.parameters, "a", self.shift)
        for d in BONDS:
            h[:18, 18:] += np.exp(1j * np.dot(k, d)) * bond_matrix(self.parameters, d)
        h[18:, :18] = h[:18, 18:].conj().T
        return h

    def gamma_sectors(self) -> dict:
        h = self.bloch(np.zeros(3))
        # Separate s and p/d sectors before diagonalization so the identification
        # remains valid at the sixfold Gamma6/Gamma8 crossing.
        s_rows = np.array([0, 9, 18, 27])
        pd_rows = np.array([i for i in range(36) if i not in s_rows])
        if np.linalg.norm(h[np.ix_(s_rows, pd_rows)]) > 1e-12:
            raise ValueError("Gamma s versus p/d block symmetry failed")
        s_energies, s_vectors = np.linalg.eigh(h[np.ix_(s_rows, s_rows)])
        states6 = np.zeros((36, 2), dtype=complex)
        states6[s_rows] = s_vectors[:, -2:]
        energies, pd_vectors = np.linalg.eigh(h[np.ix_(pd_rows, pd_rows)])
        states = np.zeros((36, 32), dtype=complex)
        states[pd_rows] = pd_vectors
        # Gamma8 top valence quartet: degeneracy plus p character, not highest occupied index.
        groups = []
        begin = 0
        for end in range(1, 33):
            if end == 32 or abs(energies[end] - energies[begin]) > 1e-7:
                groups.append(np.arange(begin, end))
                begin = end
        candidates = [g for g in groups if len(g) == 4]
        anion_p_weight = np.sum(np.abs(states[[19, 20, 21, 28, 29, 30]]) ** 2, axis=0)
        if not candidates:
            raise ValueError("Cannot identify unique Gamma6/Gamma8 sectors")
        g8 = max(candidates, key=lambda g: np.mean(anion_p_weight[g]))
        return {"E6": float(np.mean(s_energies[-2:])), "E8": float(np.mean(energies[g8])),
                "states6": states6, "states8": states[:, g8]}


def star_embedding(k: NDArray) -> NDArray:
    """Embed cell Bloch amplitudes on one cation plus its four anion neighbors."""
    embed = np.zeros((90, 36), dtype=complex)
    embed[:18, :18] = np.eye(18)
    for i, d in enumerate(BONDS):
        embed[18 * (i + 1):18 * (i + 2), 18:] = np.exp(1j * np.dot(k, d)) * np.eye(18)
    return embed


def star_potential(host: BinaryModel, replacement: BinaryModel, te_share: float = 0.25) -> NDArray:
    """Explicit binary-derived partition; te_share=1/4 reproduces uniform VCA.

    Other values are sensitivity diagnostics, not self-consistent environment models.
    """
    v = np.zeros((90, 90), dtype=complex)
    v[:18, :18] = onsite(replacement.parameters, "c", replacement.shift) - onsite(host.parameters, "c", host.shift)
    da = onsite(replacement.parameters, "a", replacement.shift) - onsite(host.parameters, "a", host.shift)
    for i, d in enumerate(BONDS):
        sl = slice(18 * (i + 1), 18 * (i + 2))
        v[sl, sl] = te_share * da
        v[:18, sl] = bond_matrix(replacement.parameters, d) - bond_matrix(host.parameters, d)
        v[sl, :18] = v[:18, sl].conj().T
    return v


def host_embedding(model: BinaryModel, mesh: int, shift: float = 0.5) -> SpectralEmbedding:
    """Uniform primitive reciprocal parallelepiped quadrature, mesh^3 points.

    Midpoint shift on an even mesh avoids an artificial Gamma pole. Convergence in mesh and
    broadening must be tested jointly; this is not a continuum extrapolation.
    """
    coordinates = (np.arange(mesh) + shift) / mesh - 0.5
    energies = np.empty((mesh**3, 36))
    modes = np.empty((90, mesh**3, 36), dtype=complex)
    for i, q in enumerate(product(coordinates, repeat=3)):
        k = np.array(q) @ RECIPROCAL
        energies[i], states = np.linalg.eigh(model.bloch(k))
        modes[:, i] = star_embedding(k) @ states / np.sqrt(mesh**3)
    return SpectralEmbedding(energies.reshape(-1), modes.reshape(90, -1))
