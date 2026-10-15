# Symmetry qualification and the observed obstruction

## Exact density witness without a symmetry-closed reference assumption

**PROVEN:** let Theta be the spin-half antiunitary with Theta²=-I, P any finite
orthonormal reference columns, and D=Phi W Phi† a positive finite native source
density matrix. Put C=P†Phi and C_T=(Theta P)†Phi. Then

    P†(D-Theta D Theta^-1)P = C W C† - (C_T W C_T†)*.

The second term follows from antiunitarity, using Theta^-1P=-ThetaP. This requires
neither a common spectral gap nor a TR-invariant P. Its operator norm bounds the
full density's TR defect from below (divide by ||P||² if P has a Gram defect).
A scalar Rayleigh witness independently evaluated directly on the native spinors
is sufficient. In PW spin order, Theta(up(G),down(G))=(down*(-G),-up*(-G)); all
physical G and -G partners must exist. Native source occupations, not fitted
populations, are used. Uncomputed unoccupied bands are not invented: D is the
actual finite176-band source used by this QE calculation.

The initial shortcut P†ThetaP=J, treating P as exactly TR closed, was REFUSED:
the preserved reference has closure residual1.2864e-7, although J is unitary to
about1.7e-14. The exact C_T formula above removes that assumption entirely.
The original refused analysis log is retained; no old physical projector test
or numerical acceptance was changed. The actual scalar cross-check is in
symmetry_independent_checks.json. This is antiunitary linear algebra, not a
priority or material-magnetism claim.

## ACE covariance is independent of source exactness

**PROVEN UNDER ASSUMPTIONS:** if A=-V_x[D]>=0 commutes with Theta and the source
span S is Theta invariant, then A_ACE=A S(S†AS)^(-1)S†A commutes with Theta.
Its definition depends only on the source span; transform every factor by Theta
and use Theta S=S U for a unitary change of columns. Without source closure,
that conclusion does not follow, even though A_ACE S=A S. Direct/ACE agreement
on source columns is therefore not an operator symmetry certificate.

For the actual first176-column source, audit_ACE_TR.py reconstructs the global
spinor arrays by G labels and measures S†ThetaS, the source-span leakage, and

    V_ACE(Theta S) - Theta(V_ACE S).

The second term uses captured ACE source action, the first uses retained xi and
the original -xi xi† action. No new exchange or SCF run is needed. This is an
ACE/ACE commutator; it is NOT a direct/ACE comparison off the source span. The
exact direct action on ThetaS was not captured. These qualifications preserve
the earlier exact source-action equivalence result and its off-span warning.

**CALCULATED:** first-source TR leakage²0.81948; ACE TR commutator relative0.02818,
max column0.10055Ry, despite source action reconstruction5.44e-16. Thus the actual
finite ACE operator fails TR covariance. This is a numerical approximation/state
qualification obstruction, not proof that the exact HSE functional favors bulk
magnetism. The earlier fixed-source direct/ACE source-space results remain valid.

## Competing explanations and the minimum discriminating input

**CALCULATED:** the later native density develops a large exact TR witness while
the Gamma8 reference local block remains nearly scalar. Charge neutrality and
the monotone FD occupations pass. The Γ-only central quartet loses its fractional
half-occupation and becomes two almost filled/two almost empty states.

**HYPOTHESES, unresolved:** (i) fractional-shell Γ-only HSE instability,
(ii) ACE's nonclosed compression span seeding or biasing that trajectory,
(iii) further native exchange/TR implementation or discretization effects.
These alternatives cannot be collapsed into a claim of physical magnetism or
a reliable nonmagnetic Gamma8 edge. Finite FD conditioning gives response slope
1/(4 sigma)=250Ry^-1 at half occupation; an exchange feedback eigenvalue above
4sigma=.004Ry could destabilize a frozen-orbital quartet map. That conditional
linearization is not a measured full SCF Jacobian or a proof of the cause.

**Next smallest discriminating native input:** canonical first-source direct
Fock actions on P and ThetaP, and on the exactly time-reversed source ThetaPhi.
Kernel covariance requires V[ThetaD](ThetaP)=Theta(V[D]P), without assuming D is
TR invariant. Reproduce the retained original direct action on P as control.
This is a fixed-operator two-source probe, NOT a restarted SCF or new material
state. It can separate a native kernel covariance error from the already measured
ACE covariance defect. All source/FFT/kernel/weights/basis/operator inputs must
be admitted before such a run. No runtime permission or physical conclusion
follows solely from this design.

The established ACE construction is from [Lin, 2016](https://arxiv.org/abs/1601.07159)
([journal](https://doi.org/10.1021/acs.jctc.6b00092)); the native implementation and
all observer additions are SHA-pinned in build_results/native_changes. The paper
does not establish the current HgTe instability mechanism. No novelty is claimed.
