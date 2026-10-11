# Continuum prescription and the meaning of a Gamma crossing

Date: 2026-10-11. Exact scattering algebra under the stated assumptions,
with an archived-model numerical audit. No physical endpoint coefficient,
new inversion prediction, temperature input or novelty claim is supplied.

## Hermitian retarded T and principal-value reactance differ

Let V be a fixed Hermitian impurity potential and the embedded retarded
host resolvent be

    g = h-i gamma, h=h*, gamma=gamma*>=0.

For finite positive eta these are the exact Hermitian and absorptive parts
of g(E+i eta). Only after a specified converged limit can h be identified
with a principal-value host resolvent. Define the support-space reactance

    K_h = (I-V h)^(-1) V.

Assume the displayed denominator is nonsingular. K_h is Hermitian,
including for singular V. Factoring the retarded denominator gives

    I-V g = (I-V h)(I+i K_h gamma),

and hence **PROVEN**

    T[g] = (I+i K_h gamma)^(-1) K_h
         = K_h (I+i gamma K_h)^(-1).

The factors cannot be reordered freely for matrix-valued channels. No
inverse of V or K_h is needed. This K_h is a support-space reactance;
it differs from the host-edge P-irreducible Feshbach kernel K_P used in
the [native extraction protocol](host_invariant_reaction_kernel.md).
Reactance/T-matrix methods are established scattering mathematics; see,
for example, [Le Ru, Somerville and Auguie](https://arxiv.org/abs/1210.0936)
for a related general scattering formulation with its own conventions.
The Hamiltonian signs and normalization here are derived explicitly above.

For one scalar channel, let k_h be real and gamma>=0. Exactly,

    T = k_h/(1+i gamma k_h),
    Re(T) = k_h/[1+(gamma k_h)^2],
    -Im(T) = gamma k_h^2/[1+(gamma k_h)^2].

Thus **PROVEN**

    Herm(T[g]) generally differs from T[Herm(g)].

This difference changes the static projection as well as the imaginary
part. A reactance pole can even coexist with a finite retarded amplitude.
Choosing a principal-value scattering equation is not equivalent to
taking the Hermitian part of the physical retarded answer afterward.
In a real host gap gamma vanishes and the two coincide, away from poles.

For small absorptive coupling the ordered series begins

    T = K_h-i K_h gamma K_h-K_h gamma K_h gamma K_h+...,
    Herm(T) = K_h-K_h gamma K_h gamma K_h+... .

The causal identity remains

    -Im(T) = T* gamma T >=0.

It does not establish -d_E Herm(T)>=0 inside a continuum. Nor does
replacing g by its Hermitian/principal-value part reinstate the bounded
off-continuum squared-resolvent theorem. The continuum resolvent and its
energy derivative require their own limiting definition.

## A shared complex pole is stronger than a real-energy ordering crossing

The exact sector pole equations retain the algebraic decomposition

    D6=F_s-Mfrak, D8=F_s+Mfrak.

**PROVEN:** if the two full poles coincide at the same energy z_c,
then F_s(z_c,x_c)=0 and Mfrak(z_c,x_c)=0, and conversely. This remains
true for complex energy. Both equations then concern complex quantities.

The stronger interpretation that a real scalar mass zero always locates
the crossing of the real parts of two broadened poles does not follow.
A simple exact counterexample uses energy-independent sector self-energies

    Sigma6=c6-i gamma6, Sigma8=c8-i gamma8,
    gamma6,gamma8>=0.

Its poles are

    z6=C+M+c6-i gamma6,
    z8=C-M+c8-i gamma8.

Their real parts coincide when 2M+c6-c8=0. At that point the common-mode
mass is -i(gamma6-gamma8)/2 and need not vanish. Unequal linewidths
therefore allow a real ordering crossing without a shared complex pole.
No claim about the linewidths of actual HgCdTe is made by this example.

For real energy one can instead define the Hermitian inverse-Green channels

    F_s,H(E,x)=E-C-Herm(Sigma_s),
    M_H(E,x)=M+Herm(Sigma_m).

Simultaneous zeros of these scalar sector quantities locate a coincident
real-denominator crossing. They need not locate the crossing of spectral
maxima when broadening and energy dependence are appreciable. A disorder
topological invariant is a further observable and is not inferred from
this condition alone. With real sharp quasiparticle poles the distinction
disappears and the original exact crossing-mass theorem applies directly.

## Computational consequence

On inverted HgTe, the planned common-mode evaluation must name the
observable and preserve both Hermitian and absorptive branch matrices.
A retarded real-part mass, principal-value reactance mass, real-denominator
crossing and complex-pole coalescence cannot be interchanged as one exact
definition. The branch-pole route should retain complex shifts and report
linewidths before applying a real two-susceptibility reduction. Numerical
eta is a continuation parameter, not a measured alloy linewidth.

The archived binary-derived model audit explicitly distinguishes
T[g(E+i eta)], Herm(T[g]), and T[Herm(g)]. It tests their exact ordered
conversion, with CdTe real mid-gap as an off-continuum equality control.
The model remains rejected as a physical impurity predictor: no new x_c
is computed and no continuum prescription is selected by matching data.

**HYPOTHESIS:** sharp enough physical Gamma branches may make the real
mass reduction useful near the transition. This needs the self-consistent
impurity/averaged spectral calculation; the present analysis does not
establish it. **NOVELTY CANDIDATE:** none. The result tightens the observable
and continuation gates of the no-fit composition program.
