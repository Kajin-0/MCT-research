# C. What is identifiable, and what would suffice for an inversion interval?

## C1. Exact obstruction after the actual N2 experiment

**PROVEN UNDER ASSUMPTIONS.** In the fixed, count-symmetric four-neighbor local
operator class H_N, N=0..4, the accepted binaries and all retained PBE/HSE
specimens have no Te N=3 environment. The original x=.125 cell has N=0,1;
the x=.25 unshared cell has N=1; the sharing cell has N=0,1,2. Thus for any
Hermitian, Td/Theta-compatible local V3,

    H_N -> H_N + 1_(N=3) V3                                (C1.1)

leaves the COMPLETE operators on every such specimen unchanged, not just its
printed eigenvalues. The new N2 data remove an old blind environment but do
not remove this one. Its Bernoulli coherent change is

    delta Hbar(x) = 4 x^3(1-x) V3.                         (C1.2)

The probability is positive in every interior composition. For an atomic
Gamma6/Gamma8 model an exact causal witness is

    g6_lambda(z,x) = sum_N P_N(x)/(z-e_N-lambda 1_(N=3)),
    d_lambda g6_lambda = P3(x)/(z-e3-lambda)^2.             (C1.3)

Therefore even the exact averaged Gamma function is not identified by these
specimen operators. Arbitrary directional/environment/nonlocal interactions
can add further invisible variables; their gap effects are already established
by `analytical_first_2026-10-11/identifiability.md` I3 and the SOC tetrahedral
analysis. Symmetry does not set V3 to zero. Fitting it to an alloy gap would
replace the missing input rather than derive it.

This is a *data/model-class* no-go, not nonuniqueness of a completely specified
many-electron Coulomb problem. Nor does a changed averaged Green function
prove that every possible sharp-branch crossing changes: (C1.3) can redistribute
satellites while leaving a dominant atom unchanged. In particular we DO NOT
claim a new complete316-query HSE complement counterexample or an opposite
physical gap sign. Earlier artificial complements did not flip their tested
finite-eta signs. Their narrower result remains intact.

## C2. Further indispensable information is observable dependent

- Coherent count averages alone miss directional disorder affecting the mass
  channel (prior I3). Separate scalar and mass variances also miss their cross
  contraction (A3 in `chemical_disorder.md`). This concerns the spectral/mass
  channel itself, not only optical vertices or linewidth.
- Independent specimen EF recentering loses aligned common/mass correlation.
  A common energy gauge is harmless; a different unrecorded random scalar
  offset per specimen/configuration changes the average propagator. The A3
  atomic counterexample has identical own-reference spectra and opposite
  aligned mass-channel kernels. Aligned chemical potential/electrostatics
  and lattice-path conventions are physical inputs.
- A finite list of moments, finite-eta values or endpoint jets cannot in the
  unrestricted class identify sharp atoms or composition roots. The existing
  moment/finite-jet and narrow-continuum counterexamples apply. Positivity
  supplies bounds, not uniqueness. None is weakened by H304.
- Finite query actions constrain that fixed-D operator. Native FD
  nonstationarity prevents replacing it by a physical self-consistent host.
  Native controls do not enclose all query-action arithmetic, omitted
  plane-wave/occupied weight, functional or zero-point error.

There is no universal number of scalar coefficients that closes all these
unknown functions. There IS a sufficient finite parameter set only after a
specific finite operator/interaction class and statistical law are supplied.
For example the earlier four-neighbor Bernstein tomography is exact for fixed
local matrices and auxiliary configurational derivatives, but is not a theorem
for nonlinear quasiparticle gaps or host-dependent self-consistent matrices.

## C3. Sufficient conditions, not an endpoint interpolation

**Model uniqueness.** A complete configuration-to-self-adjoint-operator map
H_omega, common physical projectors/reference and probability law determine
E[(z-H_omega)^-1] uniquely at Im z>0. This is a definition of a fully specified
model, not a low-cost alloy closure or proof of material accuracy. Interacting
models additionally need the physical many-body state/propagator convention.

**Continuum-to-sharp prediction.** Two physical, uniformly controlled averaged
sector functions on an interior composition interval, independently certified
tracked atom residues/backgrounds, projection transport and a transversality
modulus suffice for B1's signed-order bracket and root budget. Only the two
sector contractions need be supplied if their scalar single-copy symmetry
reduction is valid. Full orbital covariance need not be reconstructed when
these response contractions and errors are known independently. Conversely,
the two functions are not thereby two *constants*, and neither B1 nor symmetry
determines them from the endpoints. Global topology requires further global
information even if these two functions are exact.

**Two candidate closures and their disposition.**

1. A correlated Kane weak-contrast closure retains the heavy-hole propagator,
   the aligned mean Hamiltonian and the covariance contractions S_+,S_- from
   A3, rather than imposing independent scalar/mass disorder. A controlled
   second-Born resolvent expansion requires r=w/d0<1, where w uniformly bounds
   the contrast and d0 the distance to the coherent spectrum. The existing
   bound is

       ||Gbar-G_Born-Dyson|| <= (1/d0)
         [r^3/(1-r)+r^4/(1-r^2)].                         (C3.1)

   At complex energy d0>=eta is available, so w/eta<1 is sufficient, not
   necessary. It gives a candidate delta_g for B1 only if the atom and error
   gates separately pass. Demanding small eta for a tight sharp-root budget
   and eta>w for this conservative expansion can make the *certificate*
   infeasible; that is not a proof the material lacks quasiparticles. SCBA
   without a controlled omitted-diagram/error bound is an approximation, not
   a substitute certificate. Genuine Bernoulli/cluster/hopping correlations
   must be supplied; N3 and directional no-gos remain.

2. An exact/controlled causal sector-response closure supplies g6,g8 (or the
   total Schur kernels) with uniform errors, without D or a Born truncation.
   It can predict bounded finite-resolution responses immediately. It predicts
   a sharp signed order only under B1 eligibility; B2 can falsify that route
   at a threshold. Inputs may come from a qualified configuration calculation
   with controlled thermodynamic/statistical errors or independently aligned
   spectroscopy with a validated observation operator. Neither is currently
   available. Finite-eta inversion of the retained ordered spectra does not
   supply the missing random-alloy functions.

Both are physically interpretable candidates; both are currently **NO-GO for
physical x_c**. They do not assert exact CPA/SCBA, a quartic gap law, or constant
A. The support-separated spectral-moment closure and its real-root error
certificate in the 2026-10-11 package remain valid conditionally on D, but B1
is a distinct sufficient route that does not require it.

## C4. Exact common/mass reduction, with its eligibility gate visible

For a scalar single-copy sector define the TOTAL projected kernel by

    D_alpha(z,x)=1/g_alpha=z-h_alpha(x)-K_alpha(z,x).

K includes chemical Schur terms and configuration self-energy consistently as
in A1/A2. With s/m denoting half-sum/half-difference, at a real boundary energy

    F_s(E,x)=E-h_s-Re K_s(E+i0,x),
    m(E,x)=h_m+Re K_m(E+i0,x),
    Gamma_alpha=-Im K_alpha(E+i0,x).

Then Re D6=F_s-m and Re D8=F_s+m. A coincident **sharp eligible** pair obeys
F_s=m=0, Gamma6=Gamma8=0 and finite, nonzero normalization. A common zero of
the two real parts alone is insufficient: B2 may exclude normalization, or
Gamma may be nonzero. Solving the same real equations then defines only a
real-inverse crossover. A complex pole coincidence instead needs both complex
denominators to vanish on a justified analytic sheet. No one-real-equation
topology theorem follows.

If on a verified rectangle F_s has a common-energy root with
partial_E F_s>=u>0, and the mass has energy Lipschitz constant L_m, independent
errors epsilon_s,epsilon_m give

    |Ebar-Ebar_tilde| <= epsilon_s/u,
    |mu(x)-mu_tilde(x)| <= epsilon_m+L_m epsilon_s/u,        (C4.1)
    mu(x)=m(Ebar(x),x).

With physical eligibility and mu(y)-mu(x)>=s_mu(y-x)>0, a root-error bound is
(epsilon_m+L_m epsilon_s/u)/s_mu. Endpoint/sign existence margins and membership
in the rectangle are also required. These are the earlier F6 implicit-root
bounds restated with the observable gate; u,L_m,s_mu are independent inputs,
not consequences of causality inside a continuum. If real derivatives fail,
use B1's finite-eta uniform bounds or an explicit continuity modulus, not a
formal Taylor series across a threshold.

## C5. Why no physical interval can be reported now

The current evidence supplies neither a physical random-alloy pair of causal
functions nor sharp-branch eligibility nor uniform composition transversality.
It contains no accepted sign bracket in that domain. A finite ordered-cell
PBE multiplet separation, or a negative fixed-D HSE inverse response, cannot
replace all three. Therefore B1/C4 have missing hypotheses, not a numerical
x_c waiting to be inserted. Smoothness/symmetry/endpoints alone cannot supply
an error bar; earlier invisible-cluster simple-root shifts explicitly falsify
such inference in the stated coherent-model class. Tangential cubic-root
crossings separately defeat linear transversality bounds.

**STOP this prediction trajectory at that boundary.** No material sharp gap,
random-alloy x_c interval, topological transition or converged HSE is inferred.
