"""Bulk 8-band Kane Hamiltonians for zincblende HgCdTe-like materials.

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
The Kane couplings therefore have units eV*angstrom.

The implementation is the homogeneous-bulk reduction of the standard
8-band envelope-function Hamiltonian. Position-ordering, strain,
magnetic-field, and bulk-inversion-asymmetry terms are intentionally absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

ALPHA_EV_A2 = 3.8099821161548597
ComplexMatrix = NDArray[np.complex128]


@dataclass(frozen=True)
class KaneParameters:
    """Parameters of the conventional homogeneous bulk 8-band Kane model."""

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


@dataclass(frozen=True)
class ExtendedKaneParameters:
    """Two-coupling extension used to test closure of the one-P model."""

    ev: float = 0.0
    eg: float = 0.0
    delta: float = 0.0
    p8: float = 0.0
    p7: float = 0.0
    f: float = 0.0
    gamma1: float = 0.0
    gamma2: float = 0.0
    gamma3: float = 0.0

    @property
    def ec(self) -> float:
        return self.ev + self.eg

    @property
    def eta_p(self) -> float:
        denominator = abs(self.p8) + abs(self.p7)
        if denominator == 0.0:
            return 0.0
        return 2.0 * abs(self.p8 - self.p7) / denominator

    @classmethod
    def from_standard(cls, params: KaneParameters) -> "ExtendedKaneParameters":
        return cls(
            ev=params.ev,
            eg=params.eg,
            delta=params.delta,
            p8=params.p,
            p7=params.p,
            f=params.f,
            gamma1=params.gamma1,
            gamma2=params.gamma2,
            gamma3=params.gamma3,
        )


def _as_k(k: Iterable[float]) -> tuple[float, float, float]:
    values = tuple(float(v) for v in k)
    if len(values) != 3:
        raise ValueError(f"k must contain exactly three components, got {len(values)}")
    if not np.all(np.isfinite(values)):
        raise ValueError("k components must be finite")
    return values  # type: ignore[return-value]


def _hamiltonian(
    k: Iterable[float],
    *,
    ev: float,
    eg: float,
    delta: float,
    p8: float,
    p7: float,
    f: float,
    gamma1: float,
    gamma2: float,
    gamma3: float,
) -> ComplexMatrix:
    kx, ky, kz = _as_k(k)
    k2 = kx * kx + ky * ky + kz * kz
    kp = kx + 1j * ky
    km = kx - 1j * ky

    a = ALPHA_EV_A2
    rt2 = np.sqrt(2.0)
    rt3 = np.sqrt(3.0)
    rt6 = np.sqrt(6.0)

    t = ev + eg + a * (1.0 + 2.0 * f) * k2
    u = ev - a * gamma1 * k2
    v = -a * gamma2 * (kx * kx + ky * ky - 2.0 * kz * kz)
    r = a * rt3 * (gamma2 * (kx * kx - ky * ky) - 2.0j * gamma3 * kx * ky)
    s_minus = -2.0 * a * rt3 * gamma3 * km * kz
    s_plus = -2.0 * a * rt3 * gamma3 * kp * kz

    h = np.zeros((8, 8), dtype=np.complex128)
    h[0, 0] = t
    h[1, 1] = t

    h[0, 2] = -p8 * kp / rt2
    h[0, 3] = p8 * np.sqrt(2.0 / 3.0) * kz
    h[0, 4] = p8 * km / rt6
    h[0, 5] = 0.0
    h[1, 2] = 0.0
    h[1, 3] = -p8 * kp / rt6
    h[1, 4] = p8 * np.sqrt(2.0 / 3.0) * kz
    h[1, 5] = p8 * km / rt2

    h[0, 6] = -p7 * kz / rt3
    h[0, 7] = -p7 * km / rt3
    h[1, 6] = -p7 * kp / rt3
    h[1, 7] = p7 * kz / rt3

    h[2, 2] = u + v
    h[3, 3] = u - v
    h[4, 4] = u - v
    h[5, 5] = u + v
    h[6, 6] = u - delta
    h[7, 7] = u - delta

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

    upper = np.triu(h, k=1)
    return np.diag(np.diag(h)) + upper + upper.conjugate().T


def hamiltonian(k: Iterable[float], params: KaneParameters) -> ComplexMatrix:
    return _hamiltonian(
        k,
        ev=params.ev,
        eg=params.eg,
        delta=params.delta,
        p8=params.p,
        p7=params.p,
        f=params.f,
        gamma1=params.gamma1,
        gamma2=params.gamma2,
        gamma3=params.gamma3,
    )


def hamiltonian_two_p(k: Iterable[float], params: ExtendedKaneParameters) -> ComplexMatrix:
    return _hamiltonian(
        k,
        ev=params.ev,
        eg=params.eg,
        delta=params.delta,
        p8=params.p8,
        p7=params.p7,
        f=params.f,
        gamma1=params.gamma1,
        gamma2=params.gamma2,
        gamma3=params.gamma3,
    )


def time_reversal_unitary() -> ComplexMatrix:
    u = np.zeros((8, 8), dtype=np.complex128)
    u[1, 0] = 1.0
    u[0, 1] = -1.0
    u[5, 2] = 1.0
    u[4, 3] = -1.0
    u[3, 4] = 1.0
    u[2, 5] = -1.0
    u[7, 6] = 1.0
    u[6, 7] = -1.0
    return u


def _time_reversal_residual(
    matrix_at_k: ComplexMatrix,
    matrix_at_minus_k: ComplexMatrix,
) -> float:
    u = time_reversal_unitary()
    transformed = u @ matrix_at_minus_k.conjugate() @ u.conjugate().T
    scale = max(np.linalg.norm(matrix_at_k, ord="fro"), 1.0)
    return float(np.linalg.norm(matrix_at_k - transformed, ord="fro") / scale)


def time_reversal_residual(k: Iterable[float], params: KaneParameters) -> float:
    kv = np.asarray(_as_k(k), dtype=float)
    return _time_reversal_residual(hamiltonian(kv, params), hamiltonian(-kv, params))


def time_reversal_residual_two_p(
    k: Iterable[float], params: ExtendedKaneParameters
) -> float:
    kv = np.asarray(_as_k(k), dtype=float)
    return _time_reversal_residual(
        hamiltonian_two_p(kv, params), hamiltonian_two_p(-kv, params)
    )
