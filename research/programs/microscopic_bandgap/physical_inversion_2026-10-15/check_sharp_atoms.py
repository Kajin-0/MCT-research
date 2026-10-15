"""Independent small causal models of B1/B2; no material or native calculation.

Run with the existing DFT venv's NumPy/SciPy, BLAS threads=1.
Complex quadrature and analytic Stieltjes transforms are compared independently.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent


def cq(fun, lo, hi):
    return quad(lambda u: complex(fun(u)).real, lo, hi, epsabs=2e-11,
                epsrel=2e-11)[0] + 1j * quad(
        lambda u: complex(fun(u)).imag, lo, hi, epsabs=2e-11,
        epsrel=2e-11)[0]


def bg(z, lo=-.4, hi=.8):
    return (np.log(z-lo)-np.log(z-hi))/(hi-lo)


def bgp(z, lo=-.4, hi=.8):
    return (1/(z-lo)-1/(z-hi))/(hi-lo)


def certificate(Z, eta):
    W = 1-Z
    rho = W/Z
    h = 2*rho*eta
    B, B1 = W/eta, W/eta**2
    m = Z*h-B*(h*h+eta*eta)
    a = Z-2*h*B-(h*h+eta*eta)*B1
    D2 = (Z+np.sqrt(h*h+eta*eta)*B)**2
    ell = Z*eta/(h*h+eta*eta)
    assert m > 0 and a >= 2*Z/27-1e-14
    return h, B, B1, m, a, D2, ell


def main():
    # Exact rational boundary constants, independent of floating examples.
    Z0, W0, rho0 = F(3, 4), F(1, 4), F(1, 3)
    assert Z0-W0*(1+2*rho0)**2 == 2*Z0/27 == F(1, 18)
    assert W0*(1-4*rho0**2) == F(5, 36)
    records = []
    # The background has continuum through e; there is no support-free box.
    e = .17
    for Z in [.75, .8, .95]:
        for eta in [.02, .1]:
            h, B, B1, m, a, D2, ell = certificate(Z, eta)
            r = lambda z: (1-Z)*bg(z)
            rp = lambda z: (1-Z)*bgp(z)
            g = lambda E: Z/(E-e+1j*eta)+r(E+1j*eta)
            f = lambda E: (1/g(E)).real
            root = brentq(f, e-h, e+h, xtol=1e-15)
            assert abs(root-e) <= h
            identity_err = 0.
            min_derivative = 1e99
            for t in np.linspace(-h, h, 41):
                z = e+t+1j*eta
                N = Z*t+(t*t+eta*eta)*r(z).real
                dN = Z+2*t*r(z).real+(t*t+eta*eta)*rp(z).real
                identity_err = max(identity_err,
                    abs(f(e+t)-N/abs(Z+(t+1j*eta)*r(z))**2))
                min_derivative = min(min_derivative, dN)
                assert dN >= a-1e-13 and abs(g(e+t)) >= ell-1e-12
            assert identity_err < 1e-14 and f(e-h) < 0 < f(e+h)
            quadrature_error = abs(bg(e+1j*eta)-cq(
                lambda u: 1/(e+1j*eta-u)/1.2, -.4, .8))
            assert quadrature_error < 1e-11
            # A separate positive causal perturbation, with a uniform bound.
            eps = 1e-7
            gt = lambda E: (1-eps)*g(E)+eps/(E+1.3+1j*eta)
            delta_g = 2*eps/eta
            ef = delta_g/(ell*(ell-delta_g))
            assert ef < m/D2
            rt = brentq(lambda E: (1/gt(E)).real, e-h, e+h,
                        xtol=1e-15)
            root_error = D2*ef/a
            assert abs(rt-root) <= root_error
            records.append(dict(Z=Z, eta=eta, sharp_atom=e,
                inverse_root=root, atom_root_distance=abs(root-e),
                guaranteed_radius=h, numerator_derivative_min=min_derivative,
                certified_derivative_lower=a, quadrature_error=quadrature_error,
                identity_error=identity_err, perturbed_root=rt,
                perturbation_root_bound=root_error,
                actual_perturbed_root_error=abs(rt-root)))

    # A positive spectral background with integrable square-root divergence
    # at the atom. This is dmu_b, NOT the eliminated coupling measure dnu.
    Z, eta = .8, .03
    h, *rest = certificate(Z, eta)
    rth = lambda z: (1-Z)*cq(lambda u: 1/(z-u*u), 0., 1.)
    gth = lambda E: Z/(E+1j*eta)+rth(E+1j*eta)
    threshold_root = brentq(lambda E: (1/gth(E)).real, -h, h,
                            xtol=1e-14)
    assert abs(threshold_root) <= h

    # An independent finite bath: direct matrix inverse vs spectral B1.1.
    energies = np.array([.17, -.23, .61])
    weights = np.array([.8, .13, .07])
    q0 = np.sqrt(weights)
    Q, _ = np.linalg.qr(np.column_stack([q0, [1., 0., 0.], [0., 1., 0.]]))
    H = Q.T@np.diag(energies)@Q
    bath_errors = []
    for E in np.linspace(.13, .21, 5):
        z = E+.07j
        gd = np.linalg.inv(z*np.eye(3)-H)[0, 0]
        gs = sum(weights/(z-energies))
        bath_errors.append(abs(gd-gs))
    assert max(bath_errors) < 1e-12
    z = .15+.07j
    energy_shift = 2.4
    bath_gauge_error = np.linalg.norm(
        np.linalg.inv((z+energy_shift)*np.eye(3)-(H+energy_shift*np.eye(3)))
        - np.linalg.inv(z*np.eye(3)-H))
    assert bath_gauge_error < 1e-11 and abs(sum(weights)-1) < 1e-15

    # Missing atom hypothesis: exact continuous Lorentzian measure.
    eta, ee = .04, .2
    gamma6, gamma8 = .03, .17
    roots = []
    for gamma in [gamma6, gamma8]:
        gc = lambda E: 1/(E-ee+1j*(eta+gamma))
        rt = brentq(lambda E: (1/gc(E)).real, ee-1, ee+1)
        roots.append(rt)
        assert abs(rt-ee) < 1e-14
    assert gamma6 != gamma8  # different resonance poles, equal real roots
    bounded_continuous_center = (1/bg(ee+1j*eta, ee-.3, ee+.3)).real
    assert abs(bounded_continuous_center) < 1e-14

    # Equal sharp atoms, unequal finite-eta inverse values at common E=0.
    eta = .1
    g6 = 1/(1j*eta)
    g8 = .8/(1j*eta)+.2/(1j*eta-1)
    common_inverse_difference = (1/g6-1/g8).real
    assert abs(common_inverse_difference) > 1e-4

    # Conditional x certificate with independently specified synthetic slope.
    # Neither slope nor root in this model is a material estimate.
    Z6, Z8, eta, xc, slope = .9, .85, .005, .43, .8
    error_Delta = sum(2*(1-z)/z*eta for z in [Z6, Z8])
    def approximate_delta(x):
        out = []
        for Z, ee in [(Z6, slope*(x-xc)/2),
                      (Z8, -slope*(x-xc)/2)]:
            h, *_ = certificate(Z, eta)
            gg = lambda E: Z/(E-ee+1j*eta)+(1-Z)*bg(
                E+1j*eta, -.7, 1.1)
            out.append(brentq(lambda E: (1/gg(E)).real,
                              ee-h, ee+h, xtol=1e-15))
        return out[0]-out[1]
    xL, xR = .35, .52
    assert approximate_delta(xL)+error_Delta < 0
    assert approximate_delta(xR)-error_Delta > 0
    xapprox = brentq(approximate_delta, xL, xR, xtol=1e-14)
    assert abs(xapprox-xc) <= error_Delta/slope

    # Exact power integrals, cross-checked by independent quadrature at IR cut.
    infrared = []
    for p in [.5, 1., 1.5]:
        vals = []
        for cutoff in [1e-2, 1e-4]:
            exact = -np.log(cutoff) if p == 1 else (
                1-cutoff**(p-1))/(p-1)
            numerical = quad(lambda u: u**(p-2), cutoff, 1.,
                             epsabs=1e-9, epsrel=1e-11)[0]
            assert abs(numerical-exact) < 1e-8
            vals.append(dict(IR_cutoff=cutoff, S=exact))
        infrared.append(dict(p=p, integrals=vals,
                             finite_at_zero=(p > 1)))
    # A threshold atom constructed by satisfying the scalar equation with
    # finite S (p=1.5); p=.5 has the same formal scalar equation but no norm.
    # c=.1, Lambda=1: epsilon0=c/p, S=c/(p-1).
    p, c = 1.5, .1
    S = c/(p-1)
    epsilon0 = c/p
    scalar_residual = epsilon0-c/p
    target_weight = 1/(1+S)
    assert scalar_residual == 0 and target_weight >= .75

    out = dict(status='PASS', native_jobs=0, material_validation=False,
        physical_xc=None, theorem_constants_sufficient_not_optimal=True,
        continuum_atom_checks=records,
        threshold_spectral_background_root=threshold_root,
        threshold_spectral_background_radius=2*.2/.8*.03,
        independent_Hermitian_bath_max_error=max(bath_errors),
        independent_bath_reference_invariance_error=float(bath_gauge_error),
        bounded_no_atom_center_inverse=bounded_continuous_center,
        continuous_no_atom_equal_real_roots=roots,
        resonance_widths=[gamma6, gamma8],
        coincident_atom_common_inverse_difference=common_inverse_difference,
        synthetic_composition=dict(true_root=xc, approximate_root=xapprox,
            uniform_ordering_error=error_Delta,
            root_error_bound=error_Delta/slope,
            actual_error=abs(xapprox-xc)),
        coupling_measure_IR_checks=infrared,
        synthetic_threshold_atom=dict(p=p, c=c, epsilon0=epsilon0,
            S=S, Z=target_weight, scalar_equation_residual=scalar_residual))
    (HERE/'sharp_atom_checks.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
