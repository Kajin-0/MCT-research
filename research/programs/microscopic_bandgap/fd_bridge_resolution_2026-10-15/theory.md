# A state bridge requires Hamiltonian information, not six new occupations

## What the retained native basis actually adds

CALCULATED: form R=(I-UU*)Q using the orthonormalized176native source U and the
NEW joint152basis Q. Six singular values are .9782--.999999; at1e-8 there are
136nonzero numerical residual directions, not exactly six. The six leading
directions have40.10--40.33Ry kinetic Ritz values; the occupied146space has
kinetic Ritz maximum8.362Ry. See native_basis_result.json for all singular
values and high-G probabilities. These kinetic values are NOT eigenvalues of
H[D], a lower bound on its spectrum, or a justification for discarding states.
Local and nonlocal potentials may compensate kinetic energy.

The source union's small singular value .002019 means that normalized
differences between close physical reference/occupied spaces become additional
unit directions. They are legitimate auxiliary coverage vectors. Assigning
them native band occupations or interpreting them as six low-energy bands is
unjustified. Three types must remain distinct: solved eigenstates, weighted
natural source orbitals, and unoccupied compression/reference auxiliaries.
All old152preservation,146crystal and176/364ACE failures stand unchanged.

## PROVEN: the explicitly constrained variational equation

Let T be the real-linear orthogonal twirl on Hermitian matrices under a finite
unitary/antiunitary symmetry group. Under ReTr inner product, T*=T=T^2 and it
preserves trace and positivity. Let S be a FIXED invariant Galerkin space.
For differentiable electronic energy E with gradient H[D], define

    F(X)=E(TX)+sigma Tr s(TX),   s(t)=t log t+(1-t)log(1-t).

On 0<TX<I its real Hermitian derivative is

    dF(X)[Y] = ReTr {T[H[TX]+sigma logit(TX)] Y}.

This follows by the chain rule, the trace spectral derivative and T*=T.
With invariant D in S and a fixed charge, stationarity is

    D=f_sigma( P_S T(H[D]) P_S -mu I_S ).

If the native functional and discretization are exactly covariant at invariant
D, T(H[D])=H[D]. Otherwise replacing H by its twirl is an explicitly NEW
constrained variational numerical model, not native-equivalent arithmetic.
Forces would additionally differentiate a moving S; no force claim is made.
At boundaries0/1 the logarithm is singular; rounded saturation cannot provide
a certified stationarity residual. The new twirled trial's trace/entropy and
space symmetry alone do not test this equation.

## PROVEN: gap-free finite-FD residual bound

For Hermitian A,B and scalar L-Lipschitz f, diagonalize each independently.
Unitary overlap completeness gives the exact identities

    ||f(A)-f(B)||_F^2 = sum_ij |f(a_i)-f(b_j)|^2 |<u_i,v_j>|^2,
    ||A-B||_F^2       = sum_ij |a_i-b_j|^2       |<u_i,v_j>|^2.

Thus ||f(A)-f(B)||_F <= L||A-B||_F. No operator-norm version is inferred.
For FD, L=1/(4sigma) on the entire real line, including continua sampled in
a finite basis and level degeneracies. If0<D<I, set
K=mu I-sigma logit(D); then D=f_sigma(K-mu I). Therefore

    ||D-f_sigma(H[D]-mu I)||_F
       <= ||H[D]-mu I+sigma logit(D)||_F/(4sigma).

This is an a posteriori fixed-state residual bound, NOT a contraction theorem
for D->f(H[D]), and NOT a guarantee of which stationary state is physical.
At sigma .001Ry its multiplier is250/Ry. An energy-only SCF tolerance cannot
replace the required full operator residual or eigenpair residuals.

## PROVEN UNDER ASSUMPTIONS: off-space and occupied-tail budget without a gap

Write H_S=P_S H P_S, H_Q=P_Q H P_Q and B=P_Q H P_S. Block-diagonalizing H
and applying the preceding identity gives

    ||f_sigma(H-mu)-[f_sigma(H_S-mu) directsum f_sigma(H_Q-mu)]||_F
       <= sqrt(2)||B||_F/(4sigma).

If H_Q>= (mu+L)I_Q, q=dim(Q), the omitted FD block has Frobenius norm
<=sqrt(q)/(1+exp(L/sigma)) and trace<=q/(1+exp(L/sigma)). Add the in-space
FD residual bound to obtain an error for a Galerkin trial extended by zero.
This requires a COMPLEMENT lower bound, not a spectral gap aroundmu or a
support-free eliminated measure. No such native complement bound is supplied
by the observed kinetic energies. In infinite dimension q cannot be used:
one needs an independently finite FD spectral-tail trace bound.

At fixed charge a chemical-potential error additionally requires a verified
susceptibility lower bound chi_min>0 along the relevant interval:
|delta_mu|<=|delta_N|/chi_min. Native oldC1fourhalfoccupations givechi=1000/Ry
at THAT retained state; they do not establish a bound for the unknown newHSE
Hamiltonian, its entire path or its complement. No eta/sigma->0 limit is taken.

## PROVEN: precise data obstruction and counterexample

If HU=A is retained and Q=UC+R with U*R=0, then

    HQ=AC+HR.

Known eigenvalues/action on U do not determine HR. The six near-unit residual
directions show that small *occupied-source coverage error* is not a small
error bound for the full152Hamiltonian action. If ||H||<=M were independently
known, the missing action could be bounded byM||R||; here||R||~1. In fact the
retained176actions are DIRECT FOCK, not full H, so even AC is not a complete
nativeHSE Hamiltonian input. The retained local0/local1 actions apply only
vloc to six probes (`pilot_native.inc:128`); native `h_psi.f90` additionally
applies kinetic, nonlocal-SOC projector and exchange terms. No full H[D] on
the new density or its off-space residual has been exported.

An independent exact symmetry counterexample: take two copies of the same
Gamma8 representation (including Theta), U=the first copy, and H=diag(eI4,bI4).
All actions/eigenvalues on U, its symmetry, charge of a specified old trial,
and any separately fixed local action are identical for every b; H is fully
Td/Theta invariant. Yet the second-copy FD weight and chemical potential at
fixed total charge depend on b. This is an inverse-information counterexample,
not a claim of distinct physical Coulomb Hamiltonians for fixed atoms/PPs.
It does not assert that the actual noisy176native subspace is exactly invariant
or that this abstract perturbation preserves unmeasured native constraints.

## One ranked missing acquisition and acceptance

RANK1 is a **same-trial-density complete native H[D] action/readback** on the
new invariant solved space and physical6frame, with off-space action retained;
the frozen trial must specify source natural occupations, reciprocal/real
charge, XC/Hartree/nonlocal-SOC and direct Fock from that SAME D. Do not mix
oldPBE eigenvalues, oldHSE direct actions and a newtwirled density. This one
input permits charge/entropy/eigenstate/stationarity and compression checks;
a physical self-consistent result still requires verified outer convergence.
Known direct rate~.875s/trial is only a cost forecast, not a resource admission.
No newHSE job is qualified from these offline results.

Established context: [Lin's ACE method](https://arxiv.org/abs/1601.07159) and
[Lin/Lindsey compression convergence analysis](https://arxiv.org/abs/1703.05441)
distinguish interpolation and nonlinear eigenproblems. The finite-dimensional
twirl, entropy derivative and FD Lipschitz facts above are established
mathematics, independently proved here. No historical novelty is claimed.
