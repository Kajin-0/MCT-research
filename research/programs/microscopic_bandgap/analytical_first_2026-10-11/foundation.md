# Exact analytical foundation

All statements labeled **PROVEN UNDER ASSUMPTIONS** specify a model class.
They do not establish that HgCdTe satisfies that class. Energies are in eV,
x is dimensionless, and a lattice path must be specified separately.

## F1. The microscopic problem and averaging operation

Let H_ω be a static, self-adjoint electronic Hamiltonian in one physical Hilbert
space, with cation configuration ω drawn from a declared probability law μ_x.
Self-consistent electronic response may be encoded in H_ω, but it is held fixed
while its resolvent is evaluated. Independent Bernoulli occupation is an
assumption about μ_x, not a result of electronic symmetry. A prescribed global
lattice parameter or background response can make H_ω itself depend on x.

For Im z>0 define

    Ḡ(z,x) = E_x[(z-H_ω)^(-1)].

In general Ḡ is not (z-E_x H_ω)^(-1). Nor does averaging configuration-specific
Feshbach kernels produce the Feshbach kernel of Ḡ. Both operations are nonlinear.
Finite periodic cells provide an exact definition before an explicitly ordered
thermodynamic and retarded boundary limit. An η used in z=E+iη is not an observed
alloy linewidth.

## F2. Exact Γ symmetry reduction

Assume translation covariance of the ensemble and invariance under the Td double
group. With SOC and no magnetic symmetry breaking, retain one Γ6 doublet and one
Γ8 quartet, with projectors P6 and P8 and dimensions d6=2, d8=4. They are inequivalent
irreducible representations. Ensemble covariance implies

    U_g Ḡ_Γ U_g† = Ḡ_Γ.

Schur's lemma gives the exact reduction

    Ḡ_P(z,x) = g6(z,x) I2 ⊕ g8(z,x) I4.

Time reversal supplies the nonmagnetic setting; Schur's lemma supplies the
scalar blocks. A single substitution can break local Td without invalidating
ensemble Td. An unconverged, symmetry-broken host is not repaired physically by
invoking this ensemble statement.

For several copies of an irrep the commutant is A_α⊗I_dα, where A_α acts in the
copy space; it need not be scalar. Eliminate the other copies by a Schur
complement to obtain a specified single-copy g_α. This can introduce poles and
zeros. The selection and continuous tracking of a target branch remain necessary.
The reduction excludes a Γ6–Γ8 off-diagonal average at Γ; it does not exclude
finite-q intersector scattering.

## F3. Exact positive-measure representation

For clarity first use a bounded finite-volume H_ω. Form the configuration Hilbert
space L²(Ω,μ_x) and the self-adjoint multiplication operator

    (ℍψ)(ω) = H_ω ψ(ω).

Embed a physical state as a constant function of ω. The compressed resolvent is
exactly its configuration average. Let ℘ retain the six Γ spinors times that
constant configuration state and let ℚ=I-℘. Choose these Γ spinors as eigenstates
of the coherent Hamiltonian E_x H_ω, with coherent energies e6(x), e8(x).
Feshbach elimination now gives

    Ḡ_P = [z-e_P-𝒦(z,x)]^(-1),
    𝒦 = ℘ℍℚ (z-ℚℍℚ)^(-1) ℚℍ℘.

This is the kernel of the averaged response, not E_x K_ω. It includes all
configuration fluctuations, finite-q propagation and eliminated electronic
states. It is also different from the earlier finite-volume single-impurity K_P.
Symmetry makes its two blocks scalar, with the spectral theorem giving

    𝒦_α(z,x) = ∫ dν_α(t;x)/(z-t),     dν_α ≥ 0.
    ∫ dν_α = Tr[℘_αℍℚℍ℘_α]/d_α.                         (1)

The measures have units eV²; 𝒦 has units eV. They can differ despite identical
coherent energies. The proof is to insert the projection-valued spectral measure
of ℚℍℚ into the displayed Feshbach resolvent and take the normalized sector trace.
For Im z>0, -Im 𝒦_α≥0; for a real E separated from its measure support,

    -𝒦_α'(E) = ∫ dν_α/(E-t)² ≥ 0.                       (2)

There is no sign theorem for -∂_E Re 𝒦 inside the support. Boundary values or
unbounded operators require existence/domain conditions, not merely a finite
matrix proof. The augmented-space/Feshbach construction is established
[primary literature](literature.md), not a new disorder approximation.

**Sufficient reduced information:** e6,e8 and the two measures ν6,ν8 determine
the entire retained Γ Green function. Equivalently, two scalar functions g6,g8
do. This is an observable-level reduction, not an inexpensive reconstruction
of those functions from binary data, nor a finite-parameter theorem.

## F4. Reference invariance and endpoint derivatives

Changing the coherent reference Hb to Hb+ΔHb requires Σb→Σb-ΔHb, leaving Ḡ
unchanged. A global energy shift shifts z, all host energies and all measure
locations together; it leaves a signed gap invariant. Use fixed physical
projectors for all operator differences. Equal orbital labels are insufficient.

For full host-referenced dilute forward amplitudes τ_αH and τ_αC, whenever the
regular first-concentration expansion is valid,

    E_α'(0)=τ_αH + a'(0) ∂_a E_αH,
    E_α'(1)=-τ_αC + a'(1) ∂_a E_αC.

Common-mode mass projections are evaluated at the declared common energy;
gap slopes use the separate actual branch energies. They are distinct inputs.
For an affine mass chord, residuals are t_H=τ_mH-ΔM and t_C=τ_mC+ΔM at fixed
volume, with strain contributions added once. The existing host-invariant K_P
protocol may extract the required amplitudes after its physical-frame, window,
volume and continuation gates. It supplies no physical amplitude yet.

## F5. Which inversion is being predicted?

Write the scalar branch denominators as

    D6=z-C0-M0-Σ6=F_s-𝔐,
    D8=z-C0+M0-Σ8=F_s+𝔐,
    F_s=z-C0-Σ_s,       𝔐=M0+Σ_m,
    Σ_s=(Σ6+Σ8)/2,      Σ_m=(Σ6-Σ8)/2.                    (3)

| Observable | Defining condition | Additional conditions |
|---|---|---|
| Coherent eigenvalue ordering | e6=e8 | Describes E H, not the averaged quasiparticle poles |
| Sharp real pole coincidence | F_s=0 and 𝔐=0 at real E | Real self-energies in the relevant interval; isolated tracked poles |
| Coincident real inverse-Green roots | Re F_s=0 and Re 𝔐=0 | Defined from the retarded inverse; does not require equal damping |
| Shared complex pole | F_s(z)=𝔐(z)=0 | Same analytic sheet, nonzero pole residues; both complex equations must hold |
| Equal real parts of complex poles | Re z6=Re z8 | Can occur with unequal imaginary parts and nonzero complex 𝔐 |
| Γ spectral-peak crossing | Maxima of -Im g6 and -Im g8 have equal E | Specify peak choice when there are multiple maxima |
| Topological phase boundary | Change of a defined invariant or mobility-gap phase | Needs full momentum/real-space information and applicable gap/regularity conditions |

Two complex equations impose more real conditions than two real inverse-root
equations. A one-parameter real composition variation need not produce a shared
complex pole. Scalar symmetry does not imply a single peak or pole per sector.

For D=F+iΓ with Γ=-Im Σ≥0 at real energy, a spectral stationary point obeys

    Γ'(F²-Γ²)-2Γ F F'=0.                                (4)

At F=0 this requires Γ'=0 or Γ=0. Thus linewidth energy dependence is a
gap-relevant input for peak crossings. The repository already has explicit CPA
examples where the DOS edge, Γ maximum and Re D zero differ at order x².

A zero-frequency Green-function invariant for a gapped interacting system is
an established, separately conditioned construction. It does not prove that
the disorder-averaged Γ mass diagnoses a disordered sample's topology. HgTe's
inverted cubic band ordering and its semimetallic character require particular
care. Excluding other gap closings and specifying a mobility/spectral gap are
necessary for a Γ-only topological inference. No such inference is made here.

## F6. Scalar real-root theorem and uncertainty propagation

Select the real inverse-Green-root observable, or sharp real poles satisfying
the previous table. Use the Hermitian retarded self-energy for the former;
do not replace it by a principal-value T equation. If

    F_s(Ē(x),x)=0,     ∂_E F_s≥u>0,
    μ(x)=𝔐(Ē(x),x),

then simultaneous real roots occur exactly at μ=0, on the continuously
tracked branches. Differentiation gives

    Ē'=(C0'+∂_x Σ_s)/(1-∂_E Σ_s),
    μ'=M0'+∂_x Σ_m+∂_E Σ_m Ē'.                         (5)

For sharp poles at the crossing, with U=1-∂_EΣ_s and V=∂_EΣ_m,

    E_g'(x_c)=2U μ'/(U²-V²)=(Z6+Z8) μ'.                 (6)

This equation presumes simple poles U±V≠0. It does not turn a broadened peak
into a pole. The energy-linear generalized mass H_m-(B_m/B_s)H_s and its
quadratic residue correction remain valid under the earlier closure assumptions.

**Error certificate.** Suppose a candidate has uniformly bounded scalar and
mass-channel errors ε_s and ε_m in an energy/composition rectangle, including
its baseline errors. Suppose |∂_EΣ_m|≤L_m there. If the true and approximate
common roots lie in the rectangle, the mean-value theorem gives

    |Ē-Ē_app|≤ε_s/u,
    |μ-μ_app|≤ε_m+L_m ε_s/u ≡ ε_μ.                       (7)

If μ'≥m>0 between a candidate root and the true root, then

    |x_c-x_c,app|≤ε_μ/m.                                 (8)

Opposite signs exceeding ε_μ at two bracket endpoints certify a true root;
the derivative condition certifies uniqueness there. Small scalar uncertainty
has no first-order root effect when the mass self-energy is energy independent.
It can matter through L_m otherwise. Positivity of a model denominator alone
does not bound L_m or the true mass remainder.

For branch gap errors on simple sharp poles with |∂_E D_α|≥b_α>0,

    |δE_g|≤ε6/b6+ε8/b8.                                  (9)

Peak errors require additional curvature/damping control. These conditional
bounds specify consequential precision; they do not assume a material value
for m, u, b_α or L_m.
