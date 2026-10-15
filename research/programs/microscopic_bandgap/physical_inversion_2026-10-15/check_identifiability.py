"""Actual geometry intake plus independent causal/no-atom synthetic checks."""
from pathlib import Path
import json
from math import comb
from fractions import Fraction as F
import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parent


def main():
    geom = json.loads((PROGRAM/'pair_environment_2026-10-15/geometry_result.json').read_text())
    nn = geom['Te_nn_cation_indices']
    cases = {'host': [], 'Cd_x125': [0], 'unshared_x25': [0, 7],
             'shared_x25': [0, 1]}
    histograms = {}
    for name, Cd in cases.items():
        counts = [sum(j in Cd for j in n) for n in nn]
        hist = [counts.count(n) for n in range(5)]
        assert hist[3] == 0
        histograms[name] = hist
    assert histograms['shared_x25'][2] == 2
    assert histograms['unshared_x25'] == [0, 8, 0, 0, 0]

    # Exact rational Bernoulli mean weight, then independent finite retarded
    # mixture: all measured local configurations agree but averaged G differs.
    x = F(1, 4)
    probs = [F(comb(4, n))*x**n*(1-x)**(4-n) for n in range(5)]
    assert sum(probs) == 1 and probs[3] == F(3, 64)
    ee = np.array([-.4, -.3, -.1, .2, .6])
    shifted = ee.copy(); shifted[3] += .1
    pp = np.array([float(p) for p in probs])
    z = .12+.07j
    g0 = sum(pp/(z-ee)); g1 = sum(pp/(z-shifted))
    exact = float(probs[3])*(1/(z-ee[3]-.1)-1/(z-ee[3]))
    assert abs(g1-g0-exact) < 1e-13 and g0.imag < 0 and g1.imag < 0
    assert np.max(abs(ee[[0, 1, 2, 4]]-shifted[[0, 1, 2, 4]])) == 0

    # Two positive threshold Hamiltonians with a formal D(0)=Gamma(0)=0.
    # Compare a direct coupling integral with closed-form resolvents below
    # the common threshold, not an inferred pole from a finite eta peak.
    c = .1
    threshold = []
    for p in [.5, 1.5]:
        row = []
        for delta in [1e-2, 1e-4, 1e-8]:
            sq = np.sqrt(delta)
            at = np.arctan(1/sq)
            denominator_factor = (1+2*c*at/sq if p == .5
                                  else 1+2*c-2*c*sq*at)
            D_closed = -delta*denominator_factor
            # Independent t=u^2 quadrature, split on its IR scale.
            integrand = lambda u: 2*c*u**(2*p+1)/(-delta-u*u)
            K = quad(integrand, 0., sq, epsabs=1e-13)[0]+quad(
                integrand, sq, 1., epsabs=1e-13, epsrel=1e-12)[0]
            epsilon0 = c/p
            D_integral = -delta-epsilon0-K
            assert abs(D_integral-D_closed) < 1e-11
            atom_indicator = 1/denominator_factor
            row.append(dict(delta=delta, minus_delta_g=atom_indicator,
                            inverse_identity_error=abs(D_integral-D_closed)))
        if p == .5:
            assert row[-1]['minus_delta_g'] < .001
            exact_Z = 0.
        else:
            exact_Z = 1/(1+2*c)
            assert abs(row[-1]['minus_delta_g']-exact_Z) < 1e-4
        threshold.append(dict(p=p, epsilon0=c/p, c=c, sharp_weight=exact_Z,
            formal_threshold_inverse_zero=True,
            zero_boundary_damping=True, finite_delta_checks=row))

    # Without transversality, cubic zeros move by epsilon^(1/3), not O(eps).
    epsilon = 1e-9
    shift = epsilon**(1/3)
    assert shift > 1e5*epsilon
    out = dict(status='PASS', native_jobs=0, physical_xc=None,
        actual_retained16_geometry_histograms=histograms,
        N3_invisible_on_all_sampled_environments=True,
        Bernoulli_x25_P3_exact=str(probs[3]),
        causal_N3_synthetic_green_difference=[(g1-g0).real, (g1-g0).imag],
        N3_identity_error=abs(g1-g0-exact),
        threshold_inverse_zero_atom_counterexamples=threshold,
        no_transversality_counterexample=dict(uniform_perturbation=epsilon,
            root_displacement=shift), material_validation=False)
    (HERE/'identifiability_checks.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
