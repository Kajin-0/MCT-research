# Identifiability results and counterexamples

The claims below distinguish the coherent Hamiltonian, the averaged resolvent,
and a chosen spectral gap. No synthetic Hamiltonian is a validated HgCdTe model.

## I1. Finite endpoint information does not identify fixed local interactions

**PROVEN UNDER ASSUMPTIONS.** Allow a bounded local response involving an
unspecified finite number n of independent binary neighbors, with coefficients
independent of composition. Binary endpoint operators, Td/TR symmetry and
endpoint configurational derivatives through any finite order m do not identify
the coherent response or the averaged resolvent in this class.

Here "composition independent" means fixed but not supplied mixed-interaction
coefficients. If every microscopic interaction and the configuration law are
already specified, the averaged resolvent is uniquely defined; the theorem does
not assert otherwise. Pure operators alone do not specify that complete map.

**Construction.** Choose r≥m+1 and n=2r. For an actual tetrahedrally covariant
neighbor set, choose even r so n is a union of four-site Td orbits; arbitrarily
many such orbits exist at finite radii on the zincblende cation lattice. In a
scalar Γ6 block introduce the local
operator λ times the indicator of exactly r Cd neighbors. It is a polynomial
in the binary occupations with fixed coefficients, respects every permutation
of these neighbors, and vanishes in either pure binary. Its mean is

    δe6(x)=λ binom(2r,r) x^r(1-x)^r.                     (10)

Every endpoint derivative through m vanishes. The neighbor set and its scalar
onsite response preserve spinful Td and time reversal. The coherent gap changes
at every interior x. More strongly, the added operator vanishes identically
in either host with any cluster of at most m minority substitutions: such a
configuration cannot contain r Cd and r Hg neighbors. Thus the entire endpoint
single/cluster impurity operators, including their full finite-q T matrices,
can also agree through that cluster order. This statement needs no concentration
series analyticity. If the coherent baseline has a
baseline has a simple root x*, the root derivative at λ=0 is

    ∂_λ x_c=-binom(2r,r) [x*(1-x*)]^r/E_g,coh'(x*).      (11)

This is a fixed many-body local interaction, not an empirical polynomial
added to the output gap. An a priori norm bound can bound λ, but cannot identify
it. Restricting the neighbor/body order is additional physical information.

**Exact spectral extension.** On an atomic, no-hopping lattice let each local
Γ6 energy be e_H+(e_C-e_H)N/n+λ 1_(N=r), and let Γ8 be a fixed quartet at zero.
Overlapping neighbor shells do not affect its one-site spectral measure. With
independent occupations the exact Γ6 averaged Green function is

    g6,λ(z,x)=Σ_(N=0)^n P_N(x)/[z-e_H-(e_C-e_H)N/n-λ1_(N=r)].

Thus

    g6,λ-g6,0=P_r(x) {1/[z-e_r-λ]-1/[z-e_r]},            (12)
    e_r=(e_H+e_C)/2.

For z off these poles this difference and all endpoint x derivatives through
m vanish. The **entire** binary operators and those endpoint resolvent jets
coincide, while interior poles and spectral weights differ. At x=1/2, N=r
has the unique largest binomial weight. With separated poles its dominant
Γ6 spectral peak tends to e_r+λ as the positive analysis broadening tends to
zero. The Γ8 peak stays at zero. Therefore the signed dominant-peak gap differs
even though the endpoint spectral data agree. For m=1 the counterexample
already uses four neighbors, with the missing 2+2 environment.

This example also shows that branch/peak switching need not give a smooth gap
law. It does not establish smooth concentration derivatives of a real HgCdTe
peak. A separate smooth coherent counterexample (10) proves that analyticity
alone, without a body-order or derivative-size bound, does not rescue endpoint
identifiability. No universal x_c error bound follows from finite jets alone.

## I2. When endpoint tomography is unique, and what it reconstructs

**PROVEN UNDER ASSUMPTIONS.** For fixed count-symmetric n-neighbor matrices
H_N, the coherent average is a degree-n Bernstein polynomial. n+1 independent
boundary constraints reconstruct it and every H_N. For n=4 the two values,
two slopes and one curvature suffice:

    H1=H0+M'(0)/4,
    H3=H4-M'(1)/4,
    H2=H0+M'(0)/2+M''(0)/12.                             (13)

These are **auxiliary configurational** derivatives with the matrices held
fixed. Opposite-host self-consistent impurity derivatives need not be these
derivatives when the matrices depend on the host background. Applying (13)
to nonlinear quasiparticle energies is also invalid without a separate proof.

For oriented Td-covariant spinful Te p onsite matrices, the earlier exact
classification gives fourteen endpoint-invisible parameters: six coherent and
eight directional. Three oriented mixed-environment representative matrices
and known group rotations suffice in that restricted sector. Averaged endpoint
derivatives reconstruct only the coherent part. Hoppings, other orbitals,
longer-range response and background dependence lie outside the fourteen-count
theorem. Neither finite classification is a finite-parameter theorem for the
full disorder-averaged gap.

## I3. Directional information can affect the signed-gap channel

**PROVEN UNDER ASSUMPTIONS.** Coherent-invisible directional response need not
be invisible to the Γ8 self-energy. The following nonmagnetic SOC example
connects the earlier covariance limitation directly to the spectral equation.

Let n_i be the four tetrahedral unit vectors and T_i=n_i n_i^T-I3/3, so
Σ_i T_i=0 and Σ_i ||T_i||_F²=8/3. In the local spinful p space define

    O(T)=T⊗I2, Q(T)=Σ_ij T_ij L_i⊗σ_j, S=L·σ,
    P8=(S+2I6)/3, P7=(I6-S)/3.

These are atomic angular projectors; they are not assumed to be the exact
HgCdTe Bloch projectors. Use the isotropic coherent atomic propagator

    g0(z)=P8/(z-e8)+P7/(z-e7)

and the fixed random operator

    W_ω=λ Σ_i η_i [2O(T_i)+Q(T_i)].                      (14)

It vanishes in both pure binaries, has E_x W=0 for every x, and is Td covariant
and time-reversal even. The previous SOC algebra proves that its P8–P8 and
P7–P7 blocks vanish, while its P8–P7 amplitude is 3λ times P8 O(T_i)P7.

For z at positive distance from the atomic poles and sufficiently small λ,
the independently derived second-order Dyson expansion gives

    Σ8^(2)(z,x)=4λ² x(1-x)/(z-e7),
    Σ7^(2)(z,x)=8λ² x(1-x)/(z-e8),       Σ6^(2)=0.       (15)

Here the Γ6 doublet is an uncoupled s spectator. To prove the first coefficient,
use centered-subset orthogonality, trace per quartet, and
||P8 O(T)P7||_F²=(2/3)||T||_F². The coefficient is
9λ² k (2/3)(8/3)/4=4λ²k. Schur's lemma then upgrades the trace to a scalar
block. The Γ7 trace divides by two instead. These coefficients are nonzero.
They change the mass Σ_m=(Σ6-Σ8)/2 and its energy dependence, not merely a
linewidth or an unobserved orbital tensor. Equivalently the exact second
spectral moment in the Γ8 block increases by 4λ²k I4. Since all coherent
derivatives vanish, none can reconstruct this response.

At finite λ the exact average of sixteen Hermitian six-state resolvents
also differs; the expansion is not asserted exact beyond order λ². Its
nonzero leading coefficient proves the models differ in a convergent analytic
neighborhood. Physical forward impurity T measurements can detect this tensor;
they are not coherent derivatives. This example does **not** preserve those
physical T slopes. The finite-resolvent-jet counterexample I1 supplies the
distinct limitation for actual endpoint spectral derivatives.

## I4. The covariance information needed by a gap is a quotient

**PROVEN UNDER ASSUMPTIONS.** In a second-order theory with fixed coherent
propagator G_c and zero-mean disorder W, the Γ correction is

    b_α(z,x)=Tr[P_α E_x(W G_c(z) W) P_α]/d_α.            (16)

For extended lattice disorder this includes its full finite-q contractions.
It is a linear map from the operator covariance to two scalar analytic
functions. Two covariances giving the same functions in (16) give the same
retained Γ Green function through second order. Covariance differences in
the common kernel of these maps are unobservable to this gap **at that order**.
They can affect transport, other momenta or higher orders.

Therefore full directional covariance tomography is sufficient but need not
be necessary for a gap. What cannot be omitted is a directional contraction
that survives (16), as (15) explicitly demonstrates. Without the propagator,
no universal covariance null space or scalar-strength replacement is identified.

**Two-invariant atomic example.** For the same isotropic p propagator, an
angular disturbance aO(T)+αQ(T) contributes trace per sector

    b8=||T||_F²/6 { (a-2α)²/(z-e8)+(a+α)²/(z-e7) },
    b7=||T||_F²/3 (a+α)²/(z-e8).                         (17)

After summing configurational channels with their weights, only the two
weighted quadratic norms in (17) are required. Chemical and SOC coefficients
need not be separately identified. In a general Bloch propagator E and T2
angular components, orbital weights and finite-q kernels differ; this atomic
compression then need not survive. The two norms are not the old static and
dynamic susceptibilities C,A.

## I5. Two moments, even with positivity and a total-weight constraint, are insufficient

**PROVEN.** At a real reference E*=0 consider two positive discrete Feshbach
measures on energies t=(1/2,1,-1,-1/2) eV. Let w0>0 have units eV² and set

    w_j^(±)=w0[1±ε d_j],     d=(1,-2,2,-1), 0<ε<1/2.

Since u_j=1/(E*-t_j)=(-2,-1,1,2) eV^-1,

    Σd_j=Σd_j u_j=Σd_j u_j²=0,
    Σd_j u_j³=-12 eV^-3.

Thus K_±(z)=Σ_j w_j^(±)/(z-t_j) have identical total weight 4w0,
K_±(0)=0 and -K_±'(0)=10w0/eV², but

    K_+''(0)-K_-''(0)=-48ε w0/eV³ ≠0.                   (18)

Each measure is exactly realizable by a finite Hermitian Feshbach bath with
couplings sqrt(w_j). Both are causal and have positive off-spectrum A.
Positivity therefore does not select a unique spectral function or gap law.

For an explicit crossing consequence, take a flat Γ8 level E_v=0.1 eV and
a Γ6 reference E_v+2v(x-x0), v>0. Couple only Γ6 to either bath with squared
couplings k w_j^(±), k=x(1-x). Both causal families preserve the same two binary
Γ energies, total scattering weight and C,A at E*=0 for every x. A sharp
crossing at E=E_v obeys

    2v(x_c-x0)+k_c K_±(E_v)=0.                          (19)

The values K_+(E_v) and K_-(E_v) differ, so their roots differ. Small w0
ensures a unique simple tracked root and remote separation. This is a causal
effective-Hamiltonian counterexample, not an assertion that its sqrt(k) bath
embedding is a complete fixed-interaction Bernoulli alloy. I1 independently
proves non-identifiability within that fixed-interaction class.

Consequently the reciprocal two-susceptibility law is not forced by symmetry,
endpoint preservation, spectral balancing or positivity. It is a closure with
additional energy/composition assumptions. Its mathematical monotonicity
theorem remains valid for its own parameters; it is not a uniqueness theorem
for the actual microscopic alloy.

## I6. Fixed-interaction Bernoulli spectral support is independent of concentration

**PROVEN UNDER ASSUMPTIONS; established random-operator phenomenon.** Let
H_ω be a uniformly bounded self-adjoint lattice operator with finite hopping
range and finite local dependence on a finite alphabet of species. Assume
translation covariance, composition-independent matrix coefficients and
independent occupations with positive probability for every species. Then,
for every 0<x<1,

    spec(H_ω) almost surely = closure(∪_periodic ω spec(H_ω)),               (20)

which is independent of the probabilities.

**Proof.** For any configuration and any spectral energy E, self-adjointness
and density of compactly supported vectors give finitely supported approximate
eigenvectors with arbitrarily small residual. Its residual depends on only
finitely many occupations, including a finite halo. Repeat that patch in a
sufficiently large periodic cell: the residual is unchanged. Hence every
configuration's spectrum is contained in the closed union on the right.
Conversely, every finite patch of a periodic configuration has positive
probability and occurs in arbitrarily distant disjoint boxes almost surely.
Independence and the Borel–Cantelli lemma justify this statement. Transport
compact approximate eigenvectors of each periodic operator to those boxes to
obtain a Weyl sequence for a typical random operator. There are countably many
periodic configurations; take a countable dense spectral subset for each,
then use closure. This proves the reverse inclusion on a common full-probability
event. The construction does not concern spectral weights or delocalization.

The pure configurations belong to the union. A rare pure-domain spectral
contribution can therefore persist for every nonzero concentration even when
its intensity is extremely small. Almost-sure support edges, dominant Γ peaks,
mobility edges and optical edges are distinct. Equation (20) does not imply
that a specific Γ-projected spectral measure contains every spectral energy.

Composition-dependent lattice geometry, globally self-consistent response,
long-range nonlocal operators without a continuity proof, or occupation laws
that forbid patterns invalidate the displayed assumptions. No claim is made
that physical HSE HgCdTe exactly satisfies (20). It does refute identifying a
smoothly varying observed alloy edge with the support edge of the unrestricted
fixed finite-range Bernoulli model. [Kirsch–Martinelli](literature.md) supplies
the established random-spectrum context; the finite-range proof is given here
to avoid extending their continuum theorem without its assumptions.

## Minimum sufficient information: qualified conclusions

| Question | Sufficient information | Why weaker information fails |
|---|---|---|
| Exact finite local coherent response | All allowed local operator coefficients, or equivalent independent tomography | Hidden mixed clusters I1; fixed n and background must be stated |
| Exact finite random model spectrum | Full static configuration-to-Hamiltonian map, geometry, probability law and boundary/limit prescription | Binary structures do not specify mixed chemistry, directions or correlations |
| Exact retained Γ response | e6,e8 and two spectral measures, or two scalar g_α functions | Schur's lemma removes matrices, not function dependence |
| Second-order Γ correction | Two contractions (16) over the required energies/compositions, plus a truncation bound | Full covariance has irrelevant directions; missing contractions can change mass |
| Bounded sharp/real-root prediction | Common/mass self-energy values with uniform errors, root bracket and derivative bounds F6 | Finite endpoint jets give no unrestricted interior error bound |
| Controlled local energy-linear spectrum | C6,C8,A6,A8 plus support separation and an energy-window bound | I5 leaves higher inverse moments undetermined |
| Spectral-peak or topological transition | Appropriate full spectral/damping or momentum/real-space information | A real scalar mass zero alone is insufficient |

These are sufficient sets under their definitions, not claims of a globally
unique minimal number of measurements for every model. Finite-dimensional
rank can establish minimal counts only after the microscopic model class is
fixed. The unrestricted exact problem needs functional information.
