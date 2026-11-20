"""Zero-temperature, composition-only *null* model for the signed HgCdTe Gamma gap.

No energies, bowing coefficients or DFT fitting are built in. Inputs must be
provenance-qualified Gamma6 - Gamma8 eigenvalues from a *consistent* method.
Never substitute a band-count gap, indirect gap, or SQS sampled HO/LU proxy.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import copysign, isfinite, sqrt

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class RootSensitivity:
    x: float
    dgap_dx_ev: float
    dx_dhgte_ev_inverse: float
    dx_dcdte_ev_inverse: float
    dx_dbowing_ev_inverse: float


def _finite(*values: float) -> None:
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("All composition and energy inputs must be finite")


def signed_gamma_gap_ev(
    x: float, *, hgte_ev: float, cdte_ev: float, bowing_ev: float = 0.0
) -> float:
    """D(x) = (1-x)D_HgTe + x D_CdTe - b*x*(1-x), in eV.

    Sign convention: D = E_Gamma6 - E_Gamma8, negative for inverted HgTe.
    Positive b bows D downward relative to endpoint interpolation.
    """
    _finite(x, hgte_ev, cdte_ev, bowing_ev)
    if not 0.0 <= x <= 1.0:
        raise ValueError("Cd mole fraction x must be between zero and one")
    return (1.0 - x) * hgte_ev + x * cdte_ev - bowing_ev * x * (1.0 - x)


def critical_compositions(
    *, hgte_ev: float, cdte_ev: float, bowing_ev: float = 0.0
) -> tuple[float, ...]:
    """All real roots of signed D(x)=0 in the closed physical range [0,1].

    A zero polynomial has infinitely many critical compositions and raises.
    For a quadratic, use the cancellation-resistant q-formula.
    """
    _finite(hgte_ev, cdte_ev, bowing_ev)
    a, c, b = hgte_ev, cdte_ev, bowing_ev
    linear = c - a - b
    scale = max(1.0, abs(a), abs(c), abs(b))
    if abs(b) <= 1e-14 * scale:
        slope = c - a
        if abs(slope) <= 1e-14 * scale:
            if abs(a) <= 1e-14 * scale:
                raise ValueError("D(x) is identically zero: no unique transition")
            return ()
        candidates = (-a / slope,)
    else:
        disc = linear * linear - 4.0 * b * a
        if disc < 0.0:
            return ()
        sqrt_disc = sqrt(disc)
        q = -0.5 * (linear + copysign(sqrt_disc, linear))
        if q == 0.0:
            candidates = (0.0, -linear / b)
        else:
            candidates = (q / b, a / q)
    valid = sorted(min(1.0, max(0.0, r)) for r in candidates if -1e-12 <= r <= 1.0 + 1e-12)
    unique: list[float] = []
    for root in valid:
        if not unique or abs(root - unique[-1]) > 1e-10:
            unique.append(root)
    return tuple(unique)


def critical_composition_sensitivity(
    *, hgte_ev: float, cdte_ev: float, bowing_ev: float = 0.0
) -> RootSensitivity:
    """Local first-order derivatives for a *single simple* physical transition.

    Endpoint derivatives are evaluated holding the other endpoint and b fixed.
    These are derivatives of *x_c*, hence have units eV**-1.
    """
    roots = critical_compositions(hgte_ev=hgte_ev, cdte_ev=cdte_ev, bowing_ev=bowing_ev)
    if len(roots) != 1:
        raise ValueError(f"Exactly one transition required; found {len(roots)}")
    x = roots[0]
    slope = cdte_ev - hgte_ev - bowing_ev * (1.0 - 2.0 * x)
    if abs(slope) <= 1e-12 * max(1.0, abs(hgte_ev), abs(cdte_ev), abs(bowing_ev)):
        raise ValueError("Transition is tangent or ill-conditioned")
    return RootSensitivity(
        x=x,
        dgap_dx_ev=slope,
        dx_dhgte_ev_inverse=-(1.0 - x) / slope,
        dx_dcdte_ev_inverse=-x / slope,
        dx_dbowing_ev_inverse=x * (1.0 - x) / slope,
    )


def critical_composition_sigma(
    *, hgte_ev: float, cdte_ev: float, bowing_ev: float,
    covariance_ev2: ArrayLike
) -> float:
    """Local 1-sigma *linearized* propagation of 3x3 input covariance.

    Input order: [D_HgTe, D_CdTe, bowing], covariance in eV^2.
    This does NOT quantify functional bias, missing-physics errors, or
    non-Gaussian large-uncertainty behavior near a tangent transition.
    """
    s = critical_composition_sensitivity(hgte_ev=hgte_ev, cdte_ev=cdte_ev, bowing_ev=bowing_ev)
    cov = np.asarray(covariance_ev2, dtype=float)
    if cov.shape != (3, 3) or not np.all(np.isfinite(cov)):
        raise ValueError("Finite 3x3 parameter covariance required")
    if not np.allclose(cov, cov.T, atol=1e-14, rtol=1e-10):
        raise ValueError("Covariance must be symmetric")
    scale = max(1.0, float(np.max(np.abs(cov))))
    if float(np.linalg.eigvalsh(cov).min()) < -1e-12 * scale:
        raise ValueError("Covariance must be positive semidefinite")
    grad = np.asarray((s.dx_dhgte_ev_inverse, s.dx_dcdte_ev_inverse, s.dx_dbowing_ev_inverse))
    var = float(grad @ cov @ grad)
    return sqrt(max(var, 0.0))
