# Joint source closure and the state boundary — 2026-10-15

## PROVEN UNDER ASSUMPTIONS: invariant nearby space

Let P be a finite-rank orthogonal projector in the common finite plane-wave
Hilbert space. Let G contain the unitary crystal operations and an antiunitary
coset, acting by conjugation on Hermitian operators. The real-linear average
B = |G|^-1 sum_g U_g P U_g^-1 is Hermitian, 0 <= B <= I, and G-invariant.
Projective spin-lift signs cancel under conjugation. If ||B-P|| = delta < 1/2,
then P* = 1_(1/2,infinity)(B) has rank rank(P), is G-invariant, and

    ||P*-P|| <= delta/(1-delta).

Proof: Weyl separation puts the rank(P) upper eigenvalues in [1-delta,1]
and the rest in [0,delta]. Spectral calculus gives invariance, also for the
antiunitary coset because the cutoff is real. If V is an orthonormal basis
of the upper space and BV=V Lambda, then
(I-P)V=(I-P)(B-P)V Lambda^-1. Its norm is at most delta/(1-delta).
Equal ranks identify this principal-angle norm with ||P*-P||.

This is a nearby-space construction, NOT exact orbit completion preserving P.
The exact smallest invariant superspace is span{U_g range(P):g in G}.
Small nonzero directions cannot be dropped while claiming exact preservation.

## CALCULATED: finite native-space construction

`purify.py` applies projector averages and one subspace iteration successively
for Theta, primitive translations and all 24 Td operations. It does not compute
the exact spectral cutoff above. Its actual output is independently audited
against EVERY operation; measured residuals, not an assumed iteration theorem,
qualify its numerical closure. Spin and Miller-index actions are the existing
physical native actions. Old occupations are neither overwritten nor reassigned.

The purified 146-column positive-occupation space and purified 2+4 reference
spaces span dimension 152 (smallest union singular value 0.0020193). Audited
maximum Td, Theta and translation Frobenius leakage is 1.61e-14, hence bounds
the corresponding operator leakage. Original occupied-source coverage changes
by 4.65e-7 and original-reference coverage by 9.30e-7. BOTH exceed the old
1e-10 preservation gate. All old failures remain failures. No original density
or source-exact exchange result is inherited by this new basis.

## PROVEN: closure is insufficient for a Fermi-Dirac state

For sigma>0 and 0<D<I in a finite Hilbert space, the equation

    D = [I + exp((H[D]-mu I)/sigma)]^-1

is equivalent to the operator stationarity equation

    H[D]-mu I + sigma (log D - log(I-D)) = 0,

together with the charge constraint. In particular [D,H[D]]=0 is necessary.
This follows by spectral calculus, not by an assignment of eigenvalues to an
arbitrary invariant basis. On a Galerkin space it proves only projected
stationarity; a full-space claim also needs the off-space Hamiltonian residual
and a controlled omitted occupied tail. Exactly saturated numerical occupations
cannot be inverted through a finite logarithm without their own tail treatment.

Counterexample: D=diag(f(0),f(1)) and H=[[0,t],[t,1]] with t nonzero. Both may
act on a symmetry-invariant space, but their commutator is nonzero. More
strongly, with a trivial symmetry representation every such D and H passes
space-closure tests while failing FD stationarity. Symmetry alone cannot supply
the missing Hamiltonian or impose self-consistency. Averaging D over symmetry
also changes the variational state and exchange functional; it is not a basis
rotation of the original state.

## Exact missing input and decision

OPEN: native H[D] action on the NEW joint space, including local, kinetic,
nonlocal SOC and exchange terms, its off-space residual, consistent charge,
FD occupations/entropy and the self-consistency residual. Prior retained
`local0/local1` packets contain vloc action on six probes, NOT this full action.
The prior direct-Fock qualification applies to a DIFFERENT source ensemble.
No direct-Fock qualification or native FD bridge for this 152-space is claimed.

HSE native release remains NO-GO. This eliminates the assumption that rank
closure alone repairs HSE. It justifies pursuing the separately authorized
16-atom PBE composition experiment without repeating the broken HSE host.

These projector, representation and spectral-calculus facts are established
mathematics. No novelty claim or material inversion prediction is made.
