"""Self-consistent scalar CPA for the exact square-root DOS threshold model.

This is an executable single-site approximation benchmark, not an HgCdTe CPA model.
Binary site potentials are 0 and v, with concentrations 1-x and x. The host
DOS is the same normalized quadratic-edge model as threshold_impurity.py.
"""

import numpy as np


def host_green(z: complex, bandwidth: float = 1) -> complex:
    if bandwidth <= 0:
        raise ValueError("Positive bandwidth required")
    z = complex(z)
    if z == 0:
        return -3 / bandwidth
    if z.imag < 0:
        return host_green(z.conjugate(), bandwidth).conjugate()
    # sqrt(-z) is on the lower half plane for retarded z. This fixes the cut.
    root = np.sqrt(-z)
    return complex(3 / bandwidth**1.5 * (-np.sqrt(bandwidth)
                  + root * np.arctan(np.sqrt(bandwidth) / root)))


def host_green_prime(z: complex, bandwidth: float = 1) -> complex:
    z = complex(z)
    if z == 0:
        raise ValueError("The bare host derivative is singular at threshold")
    if z.imag < 0:
        return host_green_prime(z.conjugate(), bandwidth).conjugate()
    root = np.sqrt(-z)
    return complex(-3 / (2 * bandwidth**1.5) * (
        np.arctan(np.sqrt(bandwidth) / root) / root - np.sqrt(bandwidth) / (bandwidth-z)))


def cpa_at_w(w: complex, x: float, potential: float, bandwidth: float = 1) -> tuple[complex, complex]:
    """Return Sigma(w,x), dSigma/dw, with w=E-Sigma (not E).

    The branch is continuous from Sigma=0 at x=0. Used here only in the
    nonresonant weak-attractive small-x domain; global branch tracking is not
    claimed for arbitrary alloys or split bands.
    """
    if not 0 <= x <= 1:
        raise ValueError("Invalid concentration")
    g = host_green(w, bandwidth)
    d = 1-g*potential
    discriminant = np.sqrt(d*d+4*g*x*potential)
    if abs(discriminant-d) > abs(-discriminant-d):
        discriminant = -discriminant
    sigma = 2*x*potential / (d+discriminant)
    gp = host_green_prime(w, bandwidth)
    derivative = -gp * sigma * (sigma-potential) / (d+2*g*sigma)
    return complex(sigma), complex(derivative)


def threshold_constants(potential: float, bandwidth: float = 1) -> dict:
    g0 = -3 / bandwidth
    d0 = 1-g0*potential
    t0 = potential/d0
    if bandwidth <= 0 or not (potential < 0 and d0 > 0):
        raise ValueError("The benchmark requires a nonresonant weak attractive impurity")
    a = 3*np.pi/(2*bandwidth**1.5)*t0*t0
    b = -g0*t0*t0/d0
    return {"g0": g0, "d0": d0, "t0": t0, "a": a, "b": b,
            "cpa_edge_x2": b+a*a/4, "gamma_peak_x2": b+a*a/3,
            "ata_pole_x_three_halves": a*np.sqrt(-t0)}


def cpa_lower_edge(x: float, potential: float, bandwidth: float = 1) -> dict:
    """Locate the physical real-gap-side fold d[E(w)]/dw=0."""
    if x <= 0 or x > .1:
        raise ValueError("Use the declared dilute domain 0<x<=0.1")
    constants = threshold_constants(potential, bandwidth)
    scale = constants["a"]**2*x*x
    lo, hi = scale*1e-8, scale*100

    def slope(delta):
        return 1+cpa_at_w(-delta, x, potential, bandwidth)[1].real

    if slope(lo) >= 0 or slope(hi) <= 0:
        raise ValueError("CPA edge was not bracketed in the declared dilute regime")
    for _ in range(80):
        mid = (lo+hi)/2
        if slope(mid) < 0:
            lo = mid
        else:
            hi = mid
    w = -(lo+hi)/2
    sigma, derivative = cpa_at_w(w, x, potential, bandwidth)
    return {"w": w, "sigma": sigma.real, "energy": w+sigma.real,
            "fold_residual": abs(1+derivative)}


def cpa_inner_green(x: float, scaled_energy: complex, potential: float, bandwidth: float = 1) -> complex:
    """Gamma projected Green at E=x*t0+x^2*zeta, solved with full host g."""
    c = threshold_constants(potential, bandwidth)
    if x <= 0 or scaled_energy.imag <= 0:
        raise ValueError("Positive concentration and retarded scaled energy required")
    root = (c["a"]+np.sqrt(c["a"]**2-4*(scaled_energy-c["b"])))/2
    u = -root*root
    for _ in range(60):
        sigma, derivative = cpa_at_w(x*x*u, x, potential, bandwidth)
        residual = u+(sigma-x*c["t0"])/(x*x)-scaled_energy
        if abs(residual) < 2e-7:
            return 1/(x*x*u)
        correction = residual/(1+derivative)
        fraction = 1.0
        while (u-fraction*correction).imag <= 0 and fraction > 1e-6:
            fraction /= 2
        u -= fraction*correction
    raise ValueError("CPA threshold Newton solve did not converge")


def cpa_gamma_peak(x: float, potential: float, bandwidth: float = 1) -> dict:
    """Maximize calculated Gamma spectral density in the dilute threshold layer."""
    c = threshold_constants(potential, bandwidth)
    edge = cpa_lower_edge(x, potential, bandwidth)
    zedge = (edge["energy"]-x*c["t0"])/(x*x)
    eta_scaled = c["a"]**2*1e-6
    lo, hi = zedge+c["a"]**2*.001, zedge+c["a"]**2*2
    golden = (np.sqrt(5)-1)/2
    def density(z):
        return -cpa_inner_green(x, complex(z, eta_scaled), potential, bandwidth).imag*x*x
    for _ in range(48):
        left = hi-golden*(hi-lo)
        right = lo+golden*(hi-lo)
        if density(left) > density(right):
            hi = right
        else:
            lo = left
    zeta = (lo+hi)/2
    return {"energy": x*c["t0"]+x*x*zeta, "x2_coefficient": zeta,
            "scaled_peak_height": density(zeta), "external_eta": x*x*eta_scaled}


def pair_scattering_indicator(w: complex, x: float, potential: float, bandwidth: float = 1) -> float:
    """Leading dilute off-site cluster indicator x |t^2 sum_{R!=0} G_0R G_R0|.

    This is a conventional heuristic applicability indicator, not an exact
    relative CPA error or a rigorous bound. In a translational scalar host,
    the off-site sum is -g'(w)-g(w)^2, by the resolvent identity.
    """
    g = host_green(w, bandwidth)
    t = potential/(1-potential*g)
    return float(x*abs(t*t*(-host_green_prime(w, bandwidth)-g*g)))
