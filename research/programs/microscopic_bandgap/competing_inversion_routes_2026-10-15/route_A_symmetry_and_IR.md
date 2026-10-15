# RouteA: which symmetry actually constrains heavy-hole scattering?

**PROVEN UNDER ASSUMPTIONS**, static finite-orbital electronic model and the
specified continuum limits. No material coupling or exponent is inferred from
permission by symmetry. This refines the conditional assumptions in the
preceding `physical_inversion_2026-10-15/threshold_eligibility.md` and preserves
its norm obstruction; it does not replace Born by exact alloy scattering.

## A1. A physical 8-state space before a 6-state reduction

Use a declared real Cartesian orbital gauge (s,px,py,pz) tensor spin1/2.
Gamma6 is s tensor spin. In p tensor spin define angular matrices
(L_i)_{ab}=-i epsilon_{iab}, S=sum_i L_i tensor sigma_i, and

    P8=(S+2I6)/3,   P7=(I6-S)/3.

They project onto j=3/2 and1/2. A cubic/TR-invariant zone-centre operator is
e6 P6+e8 P8+e7 P7 for these single copies; inequivalent irreps cannot mix.
Including other copies changes the copy-space matrix, not Schur's lemma.
The linear Kane coupling in this Cartesian gauge is iP k dot(s*,p) plus its
Hermitian conjugate. This gauge's time reversal is I_orb tensor i sigma_y K;
the repository Novik basis uses a conventional relative p phase. Projectors
are transformed unitarily, never compared by naive coefficient indices.

Dropping Gamma7 is controlled only with a certified resolvent separation or
an independently bounded downfolding remainder. If V7 bounds its coupling
and distance d7>0 to the target window is established, the Schur term is
bounded by ||V7||^2/d7. Small k alone does not certify an alloy fluctuation's
Gamma7 coupling or a uniform d7. The R02 8-state implementation is a useful
homogeneous convention check, not a spatial-disorder/optical completion.

In the spherical Gamma8 model

    P_hh(n)=[(J dot n)^2-I6/4]/2,   J=L tensor I+I tensor sigma/2,

has rank2 and lies inside P8; its orthogonal P8 part is light-hole. At q=0
HH and LH are one Gamma8 quartet, not separately fixed irreps. Direction n
must be specified as q->0. Cubic warping, BIA or degeneracy can change this
continuation. Do not impose an axial HH projector on a general native alloy.

## A2. Uniform selection is not a variance selection

For EACH locally Td-invariant analytic composite vertex, at q=0,

    P8 Gamma(0) P6=0,   P8 Gamma(0) P8=a8 P8.

The second expression allows Gamma8->HH constant weight a8^2/2 per incoming
quartet in the spherical model; symmetry does not require a8!=0. A generic
analytic cross-irrep amplitude is at most O(q) if its constant is zero. In the
special isotropic scalar Kane linear intertwiner, the q-linear s-to-p image
is longitudinal and P_hh(n) Gamma(q) P6=0 exactly: a linear-in-q coupling need
not have a nonzero HH angular norm. Higher terms/warping must be checked.

A real mixed local environment has its stabilizer subgroup, often smaller
than Td. In general only the ensemble is Td covariant:

    E(P8 V P6)=0 does NOT imply E[(P_hh V P6)* (P_hh V P6)]=0.    (A2.1)

The full self-consistent *isolated* substitution can retain site Td even when
each neighboring Te term does not. Sum all induced terms with their phases
and correlations before assigning an impurity q=0 vertex. Independent random
Te orientations are not automatically the physical one-cation disorder.

### Fixed, endpoint-invisible Bernoulli pair construction

Here is a counterexample with no arbitrary composition-dependent interaction.
For the four tetrahedral unit vectors n_i, let

    b_R(eta)=sum_{i<j in NN(R)} (n_i+n_j) eta_i eta_j,
    V_R=lambda [|s><b_R dot p|+h.c.] tensor I_spin.          (A2.2)

This is a fixed quadratic local chemistry, TR even, Td covariant as a family,
and zero at both pure endpoints (sum n_i=0). Every count-symmetric coherent
vector average is zero. Individual N2/N3 environments have lower site symmetry;
no fictitious enforced quartet is used. At Bernoulli x, with xi_i=eta_i-x and
k=x(1-x), exactly

    b_R=2x sum_i n_i xi_i + sum_{i<j}(n_i+n_j) xi_i xi_j.    (A2.3)

The one-body filtered vector has form factor A(q)=sum_i n_i exp(i q.d_i),
A(0)=0. Its q-leading term is longitudinal for d_i proportional to n_i, and
cannot be interpreted as an independent constant Γ6->HH vertex.

The pair field is orthogonal to every one-body occupation. Distinct Te
tetrahedra share at most one cation, so the existing zincblende white-cluster
theorem gives its exact second covariance

    E[b_pair(R) b_pair(R')^T]=delta_RR' (8/3) k^2 I3.      (A2.4)

Indeed sum_{i<j}(n_i+n_j)(n_i+n_j)^T=(8/3)I3. There is NO cancelling cross
covariance with the one-body part. Consequently its Gamma6-to-HH Born weight
per doublet is constant at small q:

    (1/2) Tr P6 E[V_pair P_hh(n) V_pair] P6
       = (8/3) lambda^2 k^2,                              (A2.5)

for every direction. The coherent cross-irrep matrix is zero for every x,
yet a finite, positive higher-cluster IR weight survives. This is a concrete
refutation of using ensemble q=0 Schur selection to infer a universal l>=1
for chemical disorder. A scalar/mass-only vertex class misses this channel.
It is a **model counterexample**, not measured HgCdTe lambda or proof that
this term is nonzero in the accepted native specimens. Arbitrary frozen
PBE/HSE spectral projections do not reconstruct this oriented local tensor.

## A3. When the exponent formula is actually valid

Suppose in d dimensions a finite-q cutoff model has an isolated one-sided
channel with epsilon(q)=a(n) q^z, 0<a_min<=a(n)<=a_max, and normalized
coupling weight b(n) q^(2l), b>=0, finite nonzero angular integral. The coarea
or radial delta integral yields

    rho(epsilon)=epsilon^p /[z(2pi)^d]
       integral_S b(n) a(n)^(-(d+2l)/z) dOmega,
    p=(d+2l)/z-1.                                       (A3.1)

The continuum expression is the infinite-volume limit of finite Hermitian
baths, not an asymptotic exponent of one finite cell's delta spectrum. Bounds
on higher terms, a_min, angular norm and cutoff must be uniform before this
becomes a uniform certificate. Finite-q orbital embedding and covariance both
contribute to b. For a density with p<=1 and certified positive lower envelope,
the earlier exact Feshbach norm integral diverges at threshold and excludes
a target spectral atom **if this is the exact/controlled eliminated measure**.

For the pair example with a positive quadratic HH curvature in3D, the Born
measure has p=1/2, prefactor proportional to lambda^2 k^2 a^(-3/2), despite
zero coherent cross-irrep response. The same weight integrated into a
Friedrichs closure has finite static threshold shift proportional to
c Lambda^(p)/p for p>0 and divergent normalization for p<=1. Thus modest
mass response and failure of a sharp atom are compatible. Direction of the
HH continuum (t0-epsilon rather than t0+epsilon) changes the signed static
shift, not the squared-denominator norm. A positive infrared contribution to
one branch is not by itself a sign theorem for the difference of two masses.

Second Born is not exact: at fixed eta a weak-contrast expansion can bound its
error, but as eta->0 its w/eta certificate generally fails. Resummation can
change the threshold/linewidth and exponent. A2.5 falsifies a forbidden-channel
claim at a specified order; it does not prove no physical atom in HgCdTe.

## A4. Counterexamples to careless exponent assignments

- **Anisotropic quadratic, uniformly definite:** the exponent remains1/2 for
  constant coupling, but the coefficient depends on the angular curvature.
  For epsilon=q^T A q the DOS coefficient is proportional to(det A)^(-1/2).
- **Curvature vanishes in a direction:** epsilon=qx^2+qy^2+qz^4 gives p=1/4,
  not1/2. In the separable homogeneous case a monomial amplitude with powers
  l_i gives p=sum_i(1+2l_i)/z_i-1. The angular positive-lower-bound assumption
  of A3.1 is absent.
- **Exactly flat HH:** the weighted measure is w delta_t0 and the kernel
  w/(z-t0), not epsilon^p d epsilon with a guessed z=infinity. For a finite
  momentum cutoff the a->0 quadratic measure collapses to this atom; its
  increasing coefficient and shrinking bandwidth must be kept together.
  eta->0, a->0 and volume limits cannot be interchanged by assumption.
- **Nonanalytic vertex:** set Gamma(0)=0 but for q!=0 let its real s-p vector
  be(qy qz,qz qx,qx qy)/|q|^2. This bounded, even-q, Td-covariant vertex has
  a nonzero transverse HH angular weight of orderq^0. Pointwise q=0 selection
  does not supply analyticity, so p=1/2 is again allowed in a quadratic bath.
  No claim that this is the actual screened chemical vertex is made.
- **Dark angular norm:** q-linear longitudinal Kane coupling has zero HH
  weight in the spherical model. Substituting l=1 with a positive coefficient
  is invalid until a nonzero angular norm is established.

## A5. A missing atom can hide below a parametrically small energy scale

This exact critical Friedrichs example sharpens the acquisition decision.
For the UPWARD bath density c sqrt(epsilon) on[0,Lambda], c>0, choose the
bare level epsilon0=2c sqrt(Lambda) so the real inverse vanishes at threshold.
At E=-delta<0 exactly

    D(-delta)=-delta-2c sqrt(delta) arctan sqrt(Lambda/delta),
    (-delta)g(-delta)=[1+2c arctan sqrt(Lambda/delta)/sqrt(delta)]^-1.

There is no target atom for ANY c>0. Yet for every fixed delta>=delta_min>0
the relative difference from the free threshold pole is bounded by

    |g(-delta)+1/delta|/(1/delta) <= pi c/sqrt(delta_min).   (A5.1)

There is also a positive-eta bound without a real support gap. At z=i eta,
write I(z)=integral_0^sqrt(Lambda) du/(z-u^2), so
g(z)=z^-1/[1-2c I(z)]. Scaling u=sqrt(eta)t and splitting at t=1 gives
|I(i eta)|<=2/sqrt(eta). If a_eta=4c/sqrt(eta)<1,

    |g(i eta)-1/(i eta)| / |1/(i eta)| <= a_eta/(1-a_eta).  (A5.2)

The bound is uniform for eta>=eta_min with a_eta_min<1. Arbitrarily close
finite-resolution transforms therefore do not certify a nonzero atom.

Thus finite-resolution/finite-offset response can look arbitrarily pole-like
while the exact atom is absent. The gap-side crossover scale for delta<<Lambda
is delta_IR~(pi c)^2; this is an asymptotic scale, not a new measured linewidth.
The static threshold shift2c sqrt(Lambda) tends to0 continuously while the
atom hypothesis is lost discontinuously. This is why a yes/no atom certificate
can be logically decisive but a poor first acquisition for a bounded operational
mass prediction. It does not show the physical mass or optical response is zero.

If one inserts the pair BORN weight c proportional to lambda^2 k^2 into this
particular fixed-bath closure, its singular scale is proportional to lambda^4
k^4. This is NOT an exact HgCdTe concentration exponent, a scattering-order
identification or a self-consistent SCBA prediction. Different resummations
can change it; the older CPA/host nonanalyticity warnings remain intact.
Downward HH edges are obtained by reflection with the same norm conclusion.

## RouteA decision-changing status

A true material infrared lower certificate would still decide sharp-branch
eligibility, but the preceding recommendation is **not currently reachable
from retained data** and is not universally the highest-value next acquisition.
It needs a stationary host/physical ensemble, the full composite/directional
vertex or exact eliminated response, valid HH continuation and a controlled
Born-to-exact adapter. Current fixed-D H304 and own-EF ordered spectra provide
none of these together. Pure symmetry cheaply rejects over-strong selection
claims but supplies neither a physical c8 nor its sign. RouteB must be evaluated
independently rather than waiting for a perhaps absent atom.
