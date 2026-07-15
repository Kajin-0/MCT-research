"""Bulk 8-band Kane Hamiltonian for zincblende HgCdTe-like materials.

Conventions
-----------
Basis order::

    0: |Gamma6, +1/2>
    1: |Gamma6, -1/2>
    2: |Gamma8, +3/2>
    3: |Gamma8, +1/2>
    4: |Gamma8, -1/2>
    5: |Gamma8, -3/2>
    6: |Gamma7, +1/2>
    7: |Gamma7, -1/2>

Wave vector is supplied in inverse angstrom and energies are returned in eV.
The Kane matrix element ``p`` therefore has units eV*angstrom.

The implementation is the homogeneous-bulk reduction of the standard
8-band envelope-function Hamiltonian. Position-ordering, strain,
magnetic-field, and bulk-inversion-asymmetry terms are intentionally absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

# hbar^2 / (2 m_0), eV Angstrom^2
ALPHA_EV_A2 = 3.8099821161548597

ComplexMatrix = NDArray[np.complex128]


@dataclass(frozen=True)
class KaneParameters:
    """Parameters of the homogeneous bulk 8-band Kane model.

    Attributes
    ----------
    ev:
        Gamma8 valence-band reference energy in eV.
    eg:
        Signed Gamma6-Gamma8 gap in eV. Negative values are inverted.
    delta:
        Gamma8-Gamma7 spin-orbit splitting in eV.
    p:
        Kane momentum coupling in eV*angstrom.
    f:
        Remote-conduction-band parameter (dimensionless).
    gamma1, gamma2, gamma3:
        Modified Luttinger parameters (dimensionless), in the convention
        where explicit Gamma6 coupling is retained.
    """

    ev: float = 0.0
    eg: float = 0.0
    delta: float = 0.0
    p: float = 0.0
    f: float = 0.0
    gamma1: float = 0.0
    gamma2: float = 0.0
    gamma3: float = 0.0

    @property
    def ec(self) -> float:
        return self.ev + self.eg

    @property
    def ep(self) -> float:
        """Kane energy E_P = P^2 / alpha, in eV."""

        return self.p * self.p / ALPHA_EV_A2

    @classmethod
    def from_ep(
        cls,
        *,
        ep: float,
        ev: float = 0.0,
        eg: float = 0.0,
        delta: float = 0.0,
        f: float = 0.0,
        gamma1: float = 0.0,
        gamma2: float = 0.0,
        gamma3: float = 0.0,
    ) -> "KaneParameters":
        if ep < 0:
            raise ValueError("Kane energy ep must be nonnegative")
        return cls(
            ev=ev,
            eg=eg,
            delta=delta,
            p=float(np.sqrt(ALPHA_EV_A2 * ep)),
            f=f,
            gamma1=gamma1,
            gamma2=gamma2,
            gamma3=gamma3,
        )


def _as_k(k: Iterable[float]) -> tuple[float, float, float]:
    values = tuple(float(v) for v in k)
    if len(values) != 3:
        raise ValueError(f"k must contain exactly three components, got {len(values)}")
    if not np.all(np.isfinite(values)):
        raise ValueError("k components must be finite")
    return values  # type: ignore[return-value]


def hamiltonian(k: Iterable[float], params: KaneParameters) -> ComplexMatrix:
    """Return the 8x8 homogeneous bulk Kane Hamiltonian.

    Parameters
    ----------
    k:
        ``(kx, ky, kz)`` in inverse angstrom.
    params:
        Kane model parameters.
    """

    kx, ky, kz = _as_k(k)
    k2 = kx * kx + ky * ky + kz * kz
    kp = kx + 1j * ky
    km = kx - 1j * ky

    a = ALPHA_EV_A2
    rt2 = np.sqrt(2.0)
    rt3 = np.sqrt(3.0)
    rt6 = np.sqrt(6.0)

    # Scalar kernels.
    t = params.ec + a * (1.0 + 2.0 * params.f) * k2
    u = params.ev - a * params.gamma1 * k2
    v = -a * params.gamma2 * (kx * kx + ky * ky - 2.0 * kz * kz)
    r = a * rt3 * (
        params.gamma2 * (kx * kx - ky * ky)
        - 2.0j * params.gamma3 * kx * ky
    )
    s_minus = -2.0 * a * rt3 * params.gamma3 * km * kz
    s_plus = -2.0 * a * rt3 * params.gamma3 * kp * kz

    h = np.zeros((8, 8), dtype=np.complex128)

    # Gamma6 block.
    h[0, 0] = t
    h[1, 1] = t

    # Gamma6-(Gamma8,Gamma7) upper-right block.
    p = params.p
    h[0, 2] = -p * kp / rt2
    h[0, 3] = p * np.sqrt(2.0 / 3.0) * kz
    h[0, 4] = p * km / rt6
    h[0, 5] = 0.0
    h[0, 6] = -p * kz / rt3
    h[0, 7] = -p * km / rt3

    h[1, 2] = 0.0
    h[1, 3] = -p * kp / rt6
    h[1, 4] = p * np.sqrt(2.0 / 3.0) * kz
    h[1, 5] = p * km / rt2
    h[1, 6] = -p * kp / rt3
    h[1, 7] = p * kz / rt3

    # Valence diagonal terms.
    h[2, 2] = u + v
    h[3, 3] = u - v
    h[4, 4] = u - v
    h[5, 5] = u + v
    h[6, 6] = u - params.delta
    h[7, 7] = u - params.delta

    # Valence upper triangle in the bulk limit (C = 0; bar S = tilde S = S).
    h[2, 3] = -s_minus
    h[2, 4] = r
    h[2, 5] = 0.0
    h[2, 6] = s_minus / rt2
    h[2, 7] = -rt2 * r

    h[3, 4] = 0.0
    h[3, 5] = r
    h[3, 6] = rt2 * v
    h[3, 7] = -np.sqrt(3.0 / 2.0) * s_minus

    h[4, 5] = np.conjugate(s_plus)
    h[4, 6] = -np.sqrt(3.0 / 2.0) * s_plus
    h[4, 7] = -rt2 * v

    h[5, 6] = rt2 * np.conjugate(r)
    h[5, 7] = s_plus / rt2

    h[6, 7] = 0.0

    # Complete the Hermitian lower triangle.
    upper = np.triu(h, k=1)
    h = np.diag(np.diag(h)) + upper + upper.conjugate().T
    return h


def time_reversal_unitary() -> ComplexMatrix:
    """Return the unitary part of time reversal in the declared |J,m> basis."""

    u = np.zeros((8, 8), dtype=np.complex128)

    # J = 1/2, Gamma6.
    u[1, 0] = 1.0
    u[0, 1] = -1.0

    # Gamma8 phases in the declared basis.
    u[5, 2] = 1.0
    u[4, 3] = -1.0
    u[3, 4] = 1.0
    u[2, 5] = -1.0

    # Gamma7 phases in the declared basis.
    u[7, 6] = 1.0
    u[6, 7] = -1.0
    return u


def time_reversal_residual(k: Iterable[float], params: KaneParameters) -> float:
    """Normalized Frobenius residual for H(k)=U_T H(-k)^* U_T^dagger."""

    kv = np.asarray(_as_k(k), dtype=float)
    h_k = hamiltonian(kv, params)
    h_minus = hamiltonian(-kv, params)
    u = time_reversal_unitary()
    transformed = u @ h_minus.conjugate() @ u.conjugate().T
    scale = max(np.linalg.norm(h_k, ord="fro"), 1.0)
    return float(np.linalg.norm(h_k - transformed, ord="fro") / scale)
