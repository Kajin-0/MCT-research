# Finite-resolution matrix information and its limits

All energies below are in eV. This package uses the accepted finite native PBE
spectral data as input. Bounds are conditional on those eigenvalues/overlaps and
the stated IEEE allowance; they do not certify their eigenpair completeness,
SCF, functional, finite-cell, projector-choice or material errors. No common
real-axis spectral gap is assumed. No novelty claim is made.

## PROVEN UNDER ASSUMPTIONS: full matrix value bound

Let P have six orthonormal columns, with the original physical Gamma6/Gamma8
partition of dimensions 2/4. For specimen i put e_n=E_n-EF_i, C=P*U_ret and

    G_i(z)=C(z-e)^(-1)C*,   K_i(z)=zI-G_i(z)^(-1),   Im z=eta>0.

The omitted positive matrix measure has total S=I-CC* >=0. If ||S||<=r, then
the omitted Green function T obeys ||T||<=r/eta and ||T'||<=r/eta^2. These
follow by dilation to a spectral measure, or matrix Cauchy-Schwarz and the
resolvent norm. They apply within continua. The code inflates r by the prior
explicit 6rho rounding allowance, without asserting an eigenvalue-error bound.

Write A=G^-1, a=||A||, delta=r/eta, m=1-a delta. If m>0, then B=(G+T)^-1
satisfies ||B||<=a/m and

    ||K_full-K_ret|| <= a^2 delta/m.

Proof: B-A=-A T B, followed by the Neumann bound. For sharing-minus-unshared
contrasts add both specimens' bounds. The exact identity

    K_shared-K_unshared = G_shared^-1 (G_shared-G_unshared) G_unshared^-1

is checked independently. Normalized trace ordering is
l(K)=Re[tr(K66)/2-tr(K88)/4], with dual norm 2, so its error is at most twice
the matrix bound. Its half is an algebraic trace-mass coordinate, not the
common-mode crossing mass defined in the earlier causal work.

For a normalized positive spectral measure, Im K<=0 in the upper half-plane;
the omitted-mass contraction also has this property. The contrast of two such
kernels need not itself be a self-energy with positive damping. Eta is an
analytical resolution, not an intrinsic linewidth. Own-Fermi referencing makes
each input invariant under its energy-zero shift; it does not align absolute
electrostatic energies or establish an impurity-reaction/T-matrix identity.
Block-unitary changes of coordinates transform the full matrices covariantly
and leave the two normalized traces unchanged. This is not a bound for an
unknown physically different projector or for a nearby-frame transport.

## PROVEN UNDER ASSUMPTIONS: sharper derivative bound

The analytic derivatives are G'=-C(z-e)^(-2)C* and K'=I+A G'A. Let delta1 bound
||T'||, b=a/m and c=||A G'A||. The unstructured bound preregistered in
derivative_protocol.md is valid but unnecessarily large here. A separate
preconditioned estimate is

    ||K_full'-K_ret'|| <= delta(a+b)c/m + b^2 delta1.                 (1)

To prove (1), use B=(I+A T)^(-1)A, so ||B G'A||<=c/m. Then

    B G' B-A G'A = -A T B G'A - B G'A T B,

whose norm is <=delta(a+b)c/m. Add B T' B. No commutativity of the measure,
inverse or derivative is assumed. Noncommuting positive matrix completions in
verify.py independently test the bound. This is a resolvent bound, not an
identification of a physical alloy susceptibility A or an impurity T'.

At z=.05i the measured derivative contrast is -.0902443493 dimensionless.
The original unstructured matrix uncertainty is 15.239626; (1) reduces it to
.589217. Even the improved trace interval [-1.268679,+1.088190] is unresolved.
A well-resolved value contrast does not imply a well-resolved derivative.

An INDEPENDENT certificate that the omitted spectrum lies in [L,infinity)
replaces eta by dist(z,[L,infinity)) in delta and delta1. For the actual fixed
data, the sufficient trace-sign threshold is L>.206595624 relative to EACH
specimen's own EF. This is an information requirement computed from the error
budget, not a fitted physical parameter. Retained states may still lie at EF;
it is not a support-free domain for the complete eliminated measure.

The highest printed retained energies are about 7.96 eV. IF the retained bands
were independently certified as the exact lowest 352 of the same Hamiltonian,
this would more than suffice: the derivative matrix bound becomes .000482583.
Sorted Davidson output and scalar SCF convergence do not provide that spectral
ordering/completeness certificate, especially for approximate eigenpairs. No
such certificate is claimed here. One coarse omitted-support certificate would
be more informative than another high-precision derivative of the same partial
data. Eigenpair-error propagation would still be required for physical accuracy.

## PROVEN: partial spectral information does not determine a static moment

For a finite first moment, the exact Feshbach identity is

    K(z)=P*(H-EF)P + P*H Q [z-Q(H-EF)Q]^-1 QH P.

Thus K at finite eta is not its static first moment P*(H-EF)P. It combines
static and energy-dependent virtual couplings. For any observed omitted mass
S>=0, choose positive M<=S. Moving M from an omitted energy L to 2L preserves
the retained data and total measure, changes the first moment by L M, yet
changes G at fixed z by only M[(z-2L)^-1-(z-L)^-1]. The latter tends to zero as
L grows while the former grows without bound. Exact lowest-retained-band
ordering is respected whenever L exceeds the retained spectrum. A known global
Hamiltonian/upper-moment bound would restrict this example; positivity and
lower ordering alone do not. Finite-grid physical Hamiltonians have bounds,
but they are extra input, not recovered from these six partial spectral rows.

For the actual omitted masses, admissible 20/40 eV positive completions change
the trace first moment by 20.9277/22.5882 meV while changing the projected Green
function by only 2.62/2.82e-5 per eV. These are spectral-information
counterexamples, not alternative self-consistent Coulomb solutions for HgCdTe.

The zero-energy completions in tail_information.json show that derivative sign
is undetermined under BARE positive partial-measure assumptions. They are
explicitly inadmissible if exact lowest-352 ordering is supplied. The far/far
100 eV completion respects that ordering. A first-draft permission label was
wrong; its source/output are preserved and metadata_correction.json records the
correction. Numerical values did not change. No historical material verdict
was reclassified.

## Consequence for environment identifiability

A nonlinear projected inverse difference cannot uniquely be called a local N2
Hamiltonian increment. Complete static P H P actions would distinguish its
trace moment from virtual coupling; still they would not determine all local,
directional, background-dependent matrix elements or disorder covariance.
Taking coherent derivatives or a different scalar contraction does not supply
those missing quantities. The previous host-invariant reaction-kernel,
full/residual T, SOC tensor and directional-disorder negative results remain.

For a FIXED, background-independent, permutation-symmetric local Te operator,
count vectors determine only their linear span of H0,...,H4. Full operators for
rows 8H0, 8H4, 8H1 and 2H0+4H1+2H2 have rank four. An N3-bearing row
H0+3H1+3H2+H3 makes rank five. The accepted spectra are neither these complete
operators nor a proof of fixed-background locality. The rank theorem therefore
does not identify H3 from the present data or determine a random-alloy x_c.
