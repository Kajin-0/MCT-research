"""Explicit random-alloy supercells of the frozen binary-derived sp3d5 model.

This implements the SAME Hamiltonian as the quarter-share isolated star:
cation species determine their onsite and bond matrices; Te onsite/SOC is the
arithmetic mean of its four neighbors' binary matrices. No self-consistent
electronic response is added. scipy is an optional dependency for sparse cells.
"""

from dataclasses import dataclass
from itertools import product

import numpy as np

from .sp3d5 import BONDS, BinaryModel, bond_matrix, onsite


PRIMITIVE = np.array([[0, .5, .5], [.5, 0, .5], [.5, .5, 0]])


def periodic_neighbors(side: int) -> np.ndarray:
    """neighbor[i,mu] is the anion cell bonded to cation cell i."""
    coords = np.array(list(product(range(side), repeat=3)))
    shifts = np.array([[0, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])
    neighbors = (coords[:, None, :] + shifts[None, :, :]) % side
    return np.ravel_multi_index(neighbors.reshape(-1, 3).T, (side, side, side)).reshape(-1, 4)


def random_occupation(side: int, composition: float, seed: int) -> np.ndarray:
    """Fixed-count random placement; local statistics approach Bernoulli as size grows."""
    if not 0 <= composition <= 1 or side < 1:
        raise ValueError("Invalid composition or side")
    eta = np.zeros(side**3, dtype=int)
    eta[:round(composition * side**3)] = 1
    np.random.default_rng(seed).shuffle(eta)
    return eta


def supercell_hamiltonian(host: BinaryModel, guest: BinaryModel, side: int, occupation: np.ndarray):
    from scipy.sparse import coo_matrix

    eta = np.asarray(occupation)
    cells = side**3
    if eta.shape != (cells,) or np.any((eta != 0) & (eta != 1)):
        raise ValueError("One binary cation occupation per cell is required")
    neighbor = periodic_neighbors(side)
    te_count = np.zeros(cells)
    for mu in range(4):
        te_count[neighbor[:, mu]] += eta
    rows, columns, entries = [], [], []

    def append_blocks(left, right, matrices, weights=None, adjoint=False):
        base, contrast = matrices
        pattern = (np.abs(base) > 1e-13) | (np.abs(contrast) > 1e-13)
        a, b = np.nonzero(pattern)
        values = base[a, b][None, :] + weights[:, None] * contrast[a, b][None, :]
        rr = left[:, None] + a[None, :]
        cc = right[:, None] + b[None, :]
        rows.append(rr.reshape(-1)); columns.append(cc.reshape(-1)); entries.append(values.reshape(-1))
        if adjoint:
            rows.append(cc.reshape(-1)); columns.append(rr.reshape(-1)); entries.append(values.conj().reshape(-1))

    offsets = np.arange(cells) * 36
    for sublattice, delta_offset, weights in [("c", 0, eta), ("a", 18, te_count / 4)]:
        h0 = onsite(host.parameters, sublattice, host.shift)
        dh = onsite(guest.parameters, sublattice, guest.shift) - h0
        append_blocks(offsets + delta_offset, offsets + delta_offset, (h0, dh), weights)
    for mu, d in enumerate(BONDS):
        t0 = bond_matrix(host.parameters, d)
        dt = bond_matrix(guest.parameters, d) - t0
        append_blocks(offsets, offsets[neighbor[:, mu]] + 18, (t0, dt), eta, adjoint=True)
    return coo_matrix((np.concatenate(entries), (np.concatenate(rows), np.concatenate(columns))),
                      shape=(36 * cells, 36 * cells)).tocsr()


def uniform_gamma_states(states: np.ndarray, cells: int) -> np.ndarray:
    return np.tile(states, (cells, 1)) / np.sqrt(cells)


@dataclass(frozen=True)
class LanczosSpectrum:
    diagonal: np.ndarray
    off_diagonal: np.ndarray

    def green(self, z: np.ndarray | complex) -> np.ndarray:
        z = np.asarray(z, dtype=complex)
        denominator = z - self.diagonal[-1]
        for i in range(len(self.diagonal) - 2, -1, -1):
            denominator = z - self.diagonal[i] - self.off_diagonal[i]**2 / denominator
        return 1 / denominator


def lanczos_spectrum(hamiltonian, state: np.ndarray, steps: int, reorthogonalize: bool = False) -> LanczosSpectrum:
    """Hermitian Lanczos continued fraction; convergence must be checked in steps."""
    q = np.asarray(state, dtype=complex).copy()
    q /= np.linalg.norm(q)
    previous = np.zeros_like(q)
    beta = 0.0
    diagonal, off_diagonal, basis = [], [], []
    for iteration in range(min(steps, len(q))):
        if reorthogonalize:
            basis.append(q.copy())
        residual = hamiltonian @ q - beta * previous
        alpha = np.vdot(q, residual)
        if abs(alpha.imag) > 1e-10:
            raise ValueError("Lanczos encountered a non-Hermitian Hamiltonian")
        residual -= alpha.real * q
        if reorthogonalize:
            vectors = np.stack(basis)
            for _ in range(2):
                residual -= (vectors.conj() @ residual) @ vectors
        next_beta = float(np.linalg.norm(residual))
        diagonal.append(float(alpha.real))
        if next_beta < 1e-12 or iteration + 1 == min(steps, len(q)):
            break
        off_diagonal.append(next_beta)
        previous, q = q, residual / next_beta
        beta = next_beta
    return LanczosSpectrum(np.array(diagonal), np.array(off_diagonal))
