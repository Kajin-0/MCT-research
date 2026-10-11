# P2 — uniform reference-window control, and its impurity boundary

## U1. Concentrated-sector transport bound

**PROVEN UNDER ASSUMPTIONS.** Let P/d be a fixed normalized rank-d projector
state. In H0 its probability measure mu0 is supported on an identified branch
set J0. In a second Hermitian operator H1 let the identified branch projector
Q1 capture tr(P Q1)/d >=1-epsilon, with all its energies in J1. Suppose
`max_{s in J0,t in J1}|s-t|<=delta`. Both operators/projectors use the same
physical space and reference; Q1 is a genuine orthogonal spectral projector.
For bounded Lipschitz f, with M=||f||infinity and L=Lip(f), at every eta>0,

```text
|F_f^eta(mu1)-F_f^eta(mu0)| <= L delta + 2 M epsilon.
```

Proof: split mu1 into its in-branch and out-of-branch positive measures of
masses q and 1-q. Couple the in-branch normalized measure to mu0 by any product
coupling: every paired displacement <=delta. Poisson convolution preserves
M and L. The in-branch difference is <=q L delta, the remaining difference
<=2(1-q)M; use q<=1 and 1-q<=epsilon. Arbitrary unbounded outside energies,
continuum support, and unknown out-of-branch moments are permitted. No common
gap D or eigenvalue-derivative bound is needed.

If Phi and Psi are exact orthonormal branch frames and the minimum singular
value of Psi*Phi is >=s, then tr(P Q1)/d>=s², so epsilon<=1-s². This is a
subspace-overlap hypothesis; equal labels or sorted energies do not supply it.
Errors in native eigenpairs, NC metric, alignment and frame transport must
enlarge epsilon/delta separately. The existing data do not certify those
errors relative to the exact HSE operator or the physical many-body material.

## U2. Explicit quartic-window constants

For `chi=[1-((E-r)/W)^2]^2` inside the window and zero outside, and
`f_n=(E-r)chi`, direct differentiation gives

```text
M_m=1,                  L_m=8/(3 sqrt(3) W),
M_n=16 W/(25 sqrt(5)),  L_n=1.
epsilon_m <= [8/(3 sqrt(3)W)]delta+2 epsilon,
epsilon_n <= delta+[32 W/(25 sqrt(5))]epsilon.
```

The derivative of f_n is `1-6u²+5u⁴`, whose range is [-4/5,1]; the largest
|u|(1-u²)² occurs at |u|=1/sqrt(5). Units are respectively 1, eV^-1, eV, 1.
This uses the smoothing contraction from S1, not a continuum resolvent inverse.

For any positive mass floor p shared by mu0 and mu1, S5 implies

```text
|C1-C0| <= [(1+8/(3sqrt(3)))delta
           +(2+32/(25sqrt(5)))W epsilon]/p.
```

This is **uniform in eta** subject to the independently established floor.
It does not recover spectral peaks or prove a commuting zero-resolution limit.

## U3. A floor for this binary reference family

If every J0 level satisfies |t-r|<=b<a<W, then chi>=q_a=(1-a²/W²)² on
[-a+r,a+r]. For 0<eta<=eta_max, its Lorentz probability is bounded below by
`(2/pi)atan((a-b)/eta_max)`, since the centered subinterval [t-(a-b),t+(a-b)]
lies within that covered interval. Hence

```text
m0 >= q_a*(2/pi)atan((a-b)/eta_max),
m1 >= m0-epsilon_m.
```

For W in [W_min,W_max], take a=W_min/2 and q_a>=9/16. This yields a uniform
floor across all those widths and eta in (0,eta_max], without assuming
monotonicity of the exact tapered mass in eta. It relies on concentration of
the **known binary Gamma reference** and says nothing about alloy concentration
or the continuum weight induced by substitution.

## Existing-data evaluation and error budget

[reference_bound.json](reference_bound.json) evaluates U1–U3 from the P1
energies/overlaps. A declared test envelope W in [0.5,5] eV,
0<eta<=0.1 eV is a numerical reference qualification, **not a chosen physical
alloy observation window**. Reference r is its native branch midpoint.
Rounded input controls are delta6=2.504 micro-eV, delta8=4.216 micro-eV;
epsilon6=1.842e-12, epsilon8=3.466e-12; b=0.144882 eV. These enclose the saved
reported scalars but do not bound native residual or material errors.

The exact-input formula is propagated with the prior package's outward Decimal
arithmetic; sqrt constants use correctly rounded Decimal sqrt plus adjacent
endpoints. A conservative rational substitute would give the same qualification
without extra precision. The record separates:

1. Source-conditioned numerical cutoff/window transfer bound and floor.
2. **OPEN** native eigenpair/SCF/resolution/physical-model residuals.
3. **MISSING** self-consistent impurity/interior spectral response.

No zero value is assigned to categories 2 or 3. The small category-1 bound cannot
be added as a complete physical error budget. In particular, the earlier
pointwise inverse-kernel certificate and the full-grid sorted spectral values
remain qualified exactly as before.

## F1. Perfect binary controls need not control substitution

**PROVEN counterexample.** In fixed P=span(e1,e2), let

```text
H_A=diag(.2,-.2,-1,+1), H_B=diag(.2,-.2,+1,-1),
V=.4*(|e1><e3|+|e3><e1|).
```

The binary operators have exactly identical sorted spectra and identical
P-projected Green functions for every complex energy, with identical P frames.
After adding the same physical V, the P-irreducible first-sector kernels are
`.16/(z+1)` and `.16/(z-1)`. Their real parts at z=i eta have opposite signs;
both obey causal -Im K>=0. The unmeasured **relative orientation of the Q
operator and substitution vertex** matters. Simultaneously rotating both H and
V would be a harmless representation change; that is not this counterexample.

Therefore perfect binary Gamma cutoff/projection controls, even supplemented
by every sorted eigenvalue, do not certify an impurity finite-q error. No
positive chemical/static compensation or material norm may be inferred from
the small measured binary cutoff difference. Dense ambient resolvents and
independent Schur inverses check this witness without any native calculation.

**Decision:** reference-window conditioning can be demonstrated cheaply.
Physical impurity transfer is still unqualified; proceed to P3's minimum
acquisition analysis rather than refining an already negligible reference digit.
Underlying probability, subspace and resolvent mathematics is established;
no novelty or physical inversion is claimed.
