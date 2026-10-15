# B1. A continuum-compatible sufficient sharp-branch certificate

**PROVEN UNDER ASSUMPTIONS.** This connects a *pre-existing spectral atom* to a
real inverse-Green-function root. It does not infer an atom from finite-resolution
data, assume an eliminated-measure support gap D, or define topology. General
Stieltjes and inverse perturbation theory are established; historical novelty
of these particular conservative constants is UNVERIFIED.

## Object, normalization and hypotheses

After the thermodynamic/disorder limit, fix one normalized, physically tracked
Gamma-sector spectral measure

    dmu = Z delta_e + dmu_b,   0 < Z <= 1,   mu_b(R) = W = 1-Z,
    g(z) = Z/(z-e) + r(z),    r(z) = integral dmu_b(t)/(z-t).

The background is any positive measure. It may have continuum support through
e, a threshold singularity, other atoms, or unbounded support. The atom is a
sharp spectral branch; with continuum at e it need not be an isolated
meromorphic pole. For a single-copy cubic irrep the normalized sector trace is
scalar by Schur's lemma; multiple irrep copies require an independently
specified matrix reduction. The residue Z belongs to this specified projector.
An eta-broadened finite-cell peak or a finite Ritz eigenvector is not evidence
that this thermodynamic decomposition has nonzero Z.

Fix eta>0 (energy resolution, not intrinsic linewidth), E=e+t, and

    f_eta(E) = Re[1/g(E+i eta)].

Positivity gives -Im g>0, hence g never vanishes here. Direct multiplication,
without a boundary-value expansion, yields

    f_eta(e+t) = N(t)/|Z+(t+i eta) r(e+t+i eta)|^2,
    N(t) = Z t + (t^2+eta^2) Re r(e+t+i eta).                 (B1.1)

## General background certificate

On |t|<=h suppose |r|<=B and |r'|<=B1, in inverse-energy and
inverse-energy-squared units. If

    m = Z h - B(h^2+eta^2) > 0,
    a = Z - 2h B - (h^2+eta^2) B1 > 0,                     (B1.2)

then f_eta has exactly one zero e_eta in [e-h,e+h]. Indeed N(-h)<0<N(h)
and N'>=a. Multiplication by the positive denominator preserves zeros/signs,
so the intermediate-value theorem and strict monotonicity of N prove the claim.
The function f itself need not have a global positive derivative.

No smoothness of the real-axis continuum has been used: for a positive
background at positive eta, universally

    B = W/eta,     B1 = W/eta^2.                            (B1.3)

These follow by bounding the integrands of r and r' separately. They remain
valid at a heavy-hole threshold, although they deteriorate as eta decreases.

## Explicit gap-free sufficient condition

If **Z>=3/4**, set rho=W/Z and h=2 rho eta. For W>0,

    m = W eta (1-4 rho^2) > 0,
    a >= Z - W(1+2rho)^2 >= 2Z/27 > 0.

The last inequality uses rho<=1/3 and monotonicity of rho(1+2rho)^2.
Consequently

    |e_eta-e| <= 2(1-Z) eta/Z.                              (B1.4)

For W=0, f=E-e and the root is exactly e. This is sufficient, deliberately
nonoptimal and projector dependent; Z<3/4 is not a no-atom theorem. Uniform
Z>=Zmin>=3/4 gives a uniform O(eta) correspondence along composition without
D. Better O(eta^2) behavior can follow from independent uniform B,B1 bounds
in (B1.2), but cannot be assumed from a bounded density alone: its Hilbert
transform or derivative can diverge. No eta, thermodynamic, composition or
disorder-limit interchange has been made.

## Independent input and numerical error

Suppose a supplied approximation g_tilde obeys a uniform |g_tilde-g|<=delta_g
on the same box, with

    ell = Z eta/(h^2+eta^2),   delta_g < ell.

The atom alone gives |g|>=-Im g>=ell. Therefore

    |Re(1/g_tilde)-f_eta| <= epsilon_f
       = delta_g/[ell(ell-delta_g)].                        (B1.5)

Let Dmax2=[Z+sqrt(h^2+eta^2) B]^2. Endpoint signs and at least one
approximate zero in the box follow if epsilon_f < m/Dmax2. Every such zero
e_tilde_eta satisfies

    |e_tilde_eta-e_eta| <= Dmax2 epsilon_f/a,
    |e_tilde_eta-e| <= d = h+Dmax2 epsilon_f/a.              (B1.6)

Proof: |N(E)|=|f(E)| |Z+(t+i eta)r|^2<=epsilon_f Dmax2 at an approximate
zero; N' >= a bounds its distance to the true inverse root. An arbitrary
continuous approximation can oscillate, so approximate-root *uniqueness*
requires an extra derivative certificate and is not asserted. Branch tracking
must select roots inside the certified box. delta_g must include operator,
tail, projection, disorder/model and numerical errors actually being claimed;
a native floating-point allowance alone is not a material error budget.

## Conditional composition interval, not an interpolation law

Assume two eligible sharp branches e6(x),e8(x), continuous on a declared
composition interval, with independently certified uniform d6,d8 from above.
Let Delta=e6-e8 and Delta_tilde_eta=e6_tilde_eta-e8_tilde_eta. Then

    |Delta_tilde_eta-Delta| <= epsilon_Delta = d6+d8.        (B1.7)

If Delta_tilde_eta(xL)+epsilon_Delta<0 and
Delta_tilde_eta(xR)-epsilon_Delta>0, a true signed-order zero lies between.
If also Delta(y)-Delta(x)>=s(y-x), s>0, for all y>x in the interval, the
zero is unique. Any approximate zero in that interval has

    |x_tilde-x_c| <= epsilon_Delta/s.                      (B1.8)

More generally replace s distance by an independently established strictly
increasing transversality modulus omega(distance). Units: delta_g is eV^-1,
epsilon_f and d are eV, s is eV per unit Cd fraction. No material values for
Z, delta_g, s or x_c are supplied here. A common composition-dependent energy
shift translates both branches and the probe coordinate; Delta is invariant.
Changing projectors is a physical-input uncertainty, not an energy gauge.

The earlier finite-eta K6-K8 at ONE common finite304 chemical potential is
neither this difference of independently tracked root locations nor a sharp
mass. Even coincident atoms can give unequal Re(1/g_alpha) at a finite eta and
an arbitrary common E when their backgrounds/residues differ. The synthetic
checks explicitly exhibit this counterexample.

## Falsification boundary

A Lorentzian continuous measure has g(z)=1/(z-e+i gamma) in the upper half
plane. Re(1/g(E+i eta))=E-e at every eta, but it has **no spectral atom**.
Two such sectors can share every real inverse root while having different
complex resonance poles e-i gamma. Thus precise inverse roots, stable peaks,
or the sign of a smoothed ordering cannot establish the atom hypothesis.
The pre-existing narrow-continuum/atom finite-eta indistinguishability result
also applies. Neither B1 nor a real mass-zero equation proves bulk topology,
an absorption threshold or a transport boundary.
