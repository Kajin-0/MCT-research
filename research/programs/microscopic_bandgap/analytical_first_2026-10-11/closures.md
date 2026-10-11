# Competing analytical closures and attempts to falsify them

These are candidate predictive approximations conditional on independent
microscopic inputs. None is an established HgCdTe composition law. Their exact
limits, bounds and failures are more informative than adding interpolation
coefficients. The shared observable definitions are in [foundation.md](foundation.md).

## S. Nonperturbative spectral-measure closure with a local error certificate

Start with the exact augmented-space Feshbach measures ν_α of F3. At a real
reference E* outside their supports define four microscopic quantities

    C_α(x)=∫ dν_α/(E*-t),
    A_α(x)=∫ dν_α/(E*-t)²≥0,             α=6,8.          (21)

Let d_α be a certified lower distance from E* to supp ν_α and let h=E-E*,
|h|<d_α. The exact scalar identity

    1/(a+h)=1/a-h/a²+h²/[a²(a+h)]

gives the **PROVEN UNDER ASSUMPTIONS**, nonperturbative bound

    𝒦_α(E)=C_α-A_α h+R_α(E),
    |R_α(E)|≤ A_α h²/(d_α-|h|).                         (22)

It is nonperturbative in the scattering strength: it bounds energy truncation,
not Born order. An independent derivative certificate follows from
|1/(a+h)²-1/a²|≤(2|h|/d_α+h²/d_α²)/(1-|h|/d_α)² ×1/a²,
although the value bound (22) is sufficient for the root budget below.

The candidate poles are the generalized eigenvalues

    B_α=1+A_α,    H_α=e_α+C_α+A_α E*,
    E_α,S=H_α/B_α,
    E_g,S=2(B_s H_m-B_m H_s)/(B_s²-B_m²).              (23)

This is the gauge-invariant two-branch energy-linear formula, with no assumption
that A6=A8. Insert (22) into F6 to obtain a certified mass/root interval,
provided the reference rectangle and simple-root inequalities hold. The pole
value error also satisfies |E_α-E_α,S|≤ε_α/b_α if both roots lie there and the
true inverse derivative has lower bound b_α. Off the eliminated spectrum the
exact derivative is 1+A_α(E)≥1. Continuation into its support loses that bound.

In the requested coherent-plus-disorder form the same predictive approximation is

    E_g,S = (e6-e8) + ΔE_disorder,S,
    ΔE_disorder,S = [C6-A6(e6-E*)]/(1+A6)
                  -[C8-A8(e8-E*)]/(1+A8).              (23a)

Every correction in (23a) is a microscopic spectral moment. They are functions
of composition until a separately justified closure supplies that dependence;
they are not regression coefficients. Equations (22) and (7)–(9) quantify when
this compact equation is predictive rather than simply a reparameterization.

**Required inputs:** coherent energies; four moments in (21) over the relevant
composition interval, certified support distances, and errors on these inputs.
For x_c alone, the common and mass contractions with F6 bounds can suffice;
the full local covariance and all individual SOC tensor amplitudes need not
be separately computed. First-principles host-edge forward kernels are a
possible input adapter, subject to their existing gates. Their single-impurity
values are not automatically the full composition-dependent ν_α moments.

**Additional two-constant specialization.** Imposing affine binary energies,
pair-static mass Ck, equal branch energy derivatives Ak, and an appropriate
common-mode reduction yields

    E_g,R=[E_H+(E_C-E_H)x+Ck]/[1+Ak],  k=x(1-x).         (24)

Its endpoint slope algebra, differential fingerprint and unique-root theorem
are valid identities within (24). The binary gap span amplifies a dynamic Ak
term into the endpoint cubic coefficient A(E_C-E_H)/2. None of these identities
establishes the assumed composition dependence of the moments. Strain can
contribute to the same endpoint coefficients. A_slope is consequently not
automatically an energy-derivative susceptibility.

**Limiting behavior:** ν=0 gives the coherent gap exactly. At h=0 the linearized
kernel value and derivative are exact. With fixed total norm and increasing
remote separation its correction decreases. Pure endpoints have no disorder
measure if P retains coherent eigenstates and no residual electronic self-energy
has been assigned there.

**Attempted falsification:** I5 gives positive, equally normalized measures with
identical C,A and different x_c. Thus an *exact* two-constant inference from
those moments is **FALSIFIED**. A known d and a small energy window can instead
keep the disagreement within (22); the bounded approximation survives this
test. As d tends to zero or a resonance enters the window, the certificate
fails. It cannot be rescued by inserting a fitted A or choosing η to produce
a desired value. The previously calculated Γ8 threshold is a real obstruction
to presuming such a d for every relevant channel.

**Interpretation and literature:** static signed inverse moments can cancel
while positive squared inverse moments add. This explains how modest mass
corrections can coexist with substantial dynamic response under the applicable
Hermitian assumptions. Spectral moments, Feshbach theory and rational spectral
reductions are established. The present contribution is the explicit minimum
input/error gate, not a priority claim for these methods.

**Disposition:** analytically strongest for a local error budget if a separated
spectral window exists; physical applicability remains **OPEN**.

## W. Symmetry-contracted covariance closure with a rigorous weak-contrast regime

Let H_ω=H_c+W_ω with E W=0 and a uniform ||W_ω||≤w. At a complex or real
energy z a positive distance d0 from spec H_c, put G_c=(z-H_c)^(-1) and r=w/d0.
For r<1 the Neumann expansion converges in operator norm for every configuration.
Averaging cancels its linear term and gives

    Ḡ=G_c+G_c B G_c+R_G,
    B=E(W G_c W),
    ||R_G||≤(1/d0) r³/(1-r).                           (25)

This is a uniform bound independent of a numerical mesh. It is valid in a
thermodynamic model when the stated operator bounds hold. Td reduces B to the
two contractions (16). For the oriented Te cluster hierarchy, use

    E |δH)(δH| = Σ_(S≠∅) k^|S| |C_S)(C_S|,

with the composite physical one-body vertex and the previously proven white
m≥2 configurational factors. Propagation remains electronic and momentum
dependent. Count-symmetric Bernstein derivative terms provide only part of
this covariance; I3 forbids dropping a surviving directional term.

The usual second-Born Dyson candidate resums B:

    g_α,W=[z-e_α-b_α(z,x)]^(-1).                        (26)

To avoid presenting that resummation as exact, bound its additional geometric
terms. Since |g_α,c b_α|≤r², the difference between (26) and its quadratic
series is at most (1/d0)r⁴/(1-r²). Therefore

    |g_α,true-g_α,W|≤e_G,
    e_G=(1/d0)[r³/(1-r)+r⁴/(1-r²)].                    (27)

When e_G<|g_α,W| the exact inverse error is bounded by

    |Σ_α,true-b_α|≤e_G/[|g_α,W|(|g_α,W|-e_G)].          (28)

This follows directly from the inverse difference identity; it explicitly
excludes near-zero projected Green functions. The bound can feed F6 only in a
rectangle where all its hypotheses hold.

**Required inputs:** coherent finite-q G_c, two covariance contractions,
uniform w, distances d0, projector errors and a chosen observable. Individual
directional coefficients can be replaced by the two weighted norms (17) only
under its isotropic atomic propagator assumption. General finite-q kernels
need the contractions themselves. Strong binary onsite/hopping contrasts
invalidate a weak-scattering assumption unless demonstrated otherwise.

**Limits and causality:** W=0 gives the coherent spectrum. Scaling W→λW gives
the exact leading λ² correction. B is causal because -Im G_c≥0 and W is
Hermitian; (26) then preserves upper-half-plane resolvent causality. The
independent bounds establish approximation accuracy only for r<1.

**Attempted falsification:** r diverges at a real host band edge. For z=E+iη
inside its continuum d0≤η, so a small continuation η gives no uniform
weak-contrast certificate for a fixed nonzero w. This does not prove every
Born coefficient inaccurate; it disproves transferring (25)'s control to the
physical η→0 inversion without additional infrared estimates. The archived
binary-derived model supplies a stronger material-specific negative diagnostic:
second Born and exact T both retain a severe static error. The suppressive
screening family was separately falsified and is not reinstated.

**Interpretation and literature:** covariance scattering with full finite-q
propagation is the lowest-order disorder correction. Dyson/Neumann expansions
and covariance contraction are established. This closure competes with S:
it truncates scattering strength, while S truncates energy dependence after
nonperturbative elimination.

**Disposition:** retain as a certified off-spectrum/small-contrast benchmark;
reject an unqualified real-edge HgCdTe application.

## C. Nonperturbative single-site CPA as a falsifiable comparison model

For a specified binary onsite model with fixed hopping H_hop(k), onsite
operators U_H,U_C and one common physical frame, define a site-coherent Σ(z,x),

    g(z,x)=∫_BZ [z-H_hop(k)-Σ(z,x)]^(-1)_site dk,
    t_i=[I-(U_i-Σ)g]^(-1)(U_i-Σ),
    (1-x)t_H+x t_C=0.                                  (29)

Matrix factor ordering matters. Hopping contrast, induced neighboring Te
response and correlated environments require a generalized model and are
not represented by simply changing U_i. Solve the causal branch that connects
to the pure references. A fixed-g quadratic root is not a complete CPA solution.

**Required inputs:** binary onsite matrices in a physical frame, the complete
host hopping/BZ propagator, concentration statistics and the observable. This
model needs less environment information precisely because it neglects it.

**Exact special case:** in the atomic scalar limit g=1/(z-Σ), (29) produces

    Ḡ=(1-x)/(z-U_H)+x/(z-U_C),

the exact single-site ensemble resolvent. Thus CPA has an independently
checkable exact limit and pure endpoints. Finite-dimensional lattice CPA is
not exact in general; no rigorous error bar for actual HgCdTe follows from
its self-consistency. Its dilute fixed-host T expansion applies only where
the relevant expansion and branch are regular.

**Analyticity gate and falsification:** the archived quadratic-threshold
benchmark has isolated-host x^(3/2) but CPA edge and Γ-peak x² corrections.
The leading cluster indicator tends to one at the CPA edge, so lowering x
does not prove omitted clusters negligible in that layer. CPA regularization
is neither a proof of the true power nor a cure for missing directional
environment response. Its atomic mixture also has two poles and can switch
dominant peaks with x; one scalar self-energy does not guarantee a smooth
single band edge. Real-root, peak and support observables must be evaluated
separately. Violation of retarded causality or the pure limits rejects a
solution even before physical comparison.

**Interpretation and literature:** repeated scattering from a site is resummed
in a self-consistent medium. [Soven 1967](literature.md) is the founding
effective-medium model; [Hass–Ehrenreich–Velický 1983](literature.md) is direct
HgCdTe precedent. The existing threshold audit locates relevant cluster
applicability literature. No novelty is claimed for CPA.

**Disposition:** use as an established competing model, not the default exact
microscopic answer. No new CPA sweeps are needed for this analytical package.

## Endpoint hierarchies across all three closures

Hermite and rational endpoint identities are preserved as boundary identities.
Their bounded remainders require the indicated higher derivatives or a separate
analyticity certificate. For smooth μ, the cubic satisfies

    μ=μ3+k² R_μ,

but endpoint data alone do not bound R_μ. Independent-host fractional threshold
terms can make it unbounded; self-consistency can change that exponent. The
four-neighbor coherent polynomial theorem applies to E H with fixed local
matrices, not to E[(z-H)^(-1)] or its nonlinear poles. R33 matching values,
slopes and curvatures does not supply a microscopic truncation bound.

The proposed four-way equality of A_slope, T' and two pair-curvature values
is retained only as a **conditional closure test** with identical reference,
volume, observable and regularity conventions. It is not an exact universal
identity. Already known threshold, strain and full/residual-T corrections
prevent declaring those four quantities interchangeable.
