"""Exactly integrable 3D quadratic-edge counterexample to smooth endpoint closure.

rho(e)=3 sqrt(e)/(2 bandwidth^(3/2)), 0<e<bandwidth. An isolated
scalar impurity has a finite T at the edge (away from a resonance), but its
energy derivative diverges on approaching the edge from below. This is a
mathematical model, not a derived HgCdTe density of states or CPA solution.
"""

import numpy as np


def below_edge_green(delta: float | np.ndarray, bandwidth: float = 1) -> np.ndarray:
    """g(-delta), with the threshold at E=0."""
    delta = np.asarray(delta, dtype=float)
    if bandwidth <= 0 or np.any(delta <= 0):
        raise ValueError("Positive detuning and bandwidth are required")
    return 3 / bandwidth**1.5 * (-np.sqrt(bandwidth)
              + np.sqrt(delta) * np.arctan(np.sqrt(bandwidth / delta)))


def below_edge_green_prime(delta: float | np.ndarray, bandwidth: float = 1) -> np.ndarray:
    delta = np.asarray(delta, dtype=float)
    if bandwidth <= 0 or np.any(delta <= 0):
        raise ValueError("Positive detuning and bandwidth are required")
    return -3 / (2 * bandwidth**1.5) * (np.arctan(np.sqrt(bandwidth / delta)) / np.sqrt(delta)
                                                      - np.sqrt(bandwidth) / (bandwidth + delta))


def scalar_t_below_edge(delta: float | np.ndarray, potential: float, bandwidth: float = 1) -> np.ndarray:
    return potential / (1 - potential * below_edge_green(delta, bandwidth))


def threshold_t(potential: float, bandwidth: float = 1) -> float:
    return potential / (1 + 3 * potential / bandwidth)


def dilute_pole_below_edge(concentration: float, potential: float, bandwidth: float = 1) -> float:
    """Solve E=x T(E)<0 in independent-impurity closure, by bracketed bisection."""
    if concentration <= 0 or potential >= 0 or threshold_t(potential, bandwidth) >= 0:
        raise ValueError("This example requires x>0 and a nonresonant weak attractive impurity")
    lo, hi = -2 * concentration * abs(threshold_t(potential, bandwidth)), 0.0
    for _ in range(100):
        mid = (lo + hi) / 2
        residual = mid - concentration * scalar_t_below_edge(-mid, potential, bandwidth)
        if residual < 0:
            lo = mid
        else:
            hi = mid
    return float((lo + hi) / 2)
