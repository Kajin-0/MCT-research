# Threshold-aware causal Γ reduction: proofs and domains

All results below are **PROVEN UNDER ASSUMPTIONS**. They are conditional
mathematics, not a determination of material coefficients. Use the previous
[F1–F5 foundation](../analytical_first_2026-10-11/foundation.md): static
self-adjoint configuration operators, ensemble Td symmetry, fixed physical
projectors and one retained copy of each Γ6/Γ8 irrep. The exact inverse is

    D_α(z,x)=z-e_α(x)-K_α(z,x),
    K_α(z,x)=∫ dν_α(t;x)/(z-t),       dν_α>=0.             (T1)

Here K is the augmented-space kernel of the averaged resolvent, not an average
of individual kernels and not the full host-referenced single-impurity T.
The old full/residual, strain and reference corrections still apply to any
adapter supplying inputs. Threshold claims about an isolated impurity do not
automatically establish the density of the exact alloy kernel in (T1).

## T2. Isolate a fractional threshold with its retarded branch

At fixed x, assume a one-sided absolutely continuous part at t0, parametrized
by t=t0+σ ε, σ=+1 for a lower edge and -1 for an upper edge. For 0<ε<Λ let

    ρ(ε)=c ε^ν+r(ε),     c>=0, 0<ν<1,
    |r(ε)|<=B ε^p,      p=ν+β, β>0.                     (T2)

The density ρ has units energy, c has units energy^(1-ν), and B has units
energy^(1-p). Λ is an energy cutoff, not a fitted material parameter. The
rest of the positive measure has distance at least d>0 from t0 and total
weight at most S (energy²). No atom/resonance at t0 is admitted by (T2).

In a specified low-q channel with dispersion ε~q^z and amplitude ~q^ℓ,
phase-space counting gives ν=(d_space+2ℓ)/z-1. Three quadratic dimensions
with nonzero constant amplitude give ν=1/2. Channel selection, physical
linear BIA and the actual weighted coupling must be checked; a bare DOS
does not establish the measure in T1. In the earlier nonresonant isolated
Γ8 impurity theorem, -T8'~τ8² k8/√δ would correspond to
c=2τ8² k8/π. Its binary k8 alone does not fix τ8, and this isolated-host
relation is not assigned to the exact composition-dependent alloy kernel.

Set w=z-t0 and a=-σw. Define I_ν(a)=∫_0^Λ ε^ν/(ε+a) dε. On the slit plane
a∉(-∞,0], the branch is positive for a>0. Subtraction of the threshold value
and the beta integral ∫_0^∞ u^(ν-1)/(1+u) du=π/sin(πν) give

    I_ν(a)=Λ^ν/ν - [π/sin(πν)]a^ν
            + a∫_Λ^∞ ε^(ν-1)/(ε+a) dε,
    K_lead(z)=-σ cΛ^ν/ν + σ[πc/sin(πν)]a^ν
               -σ c Σ_(n>=1) (-1)^(n-1)a^n Λ^(ν-n)/(n-ν).    (T3)

The series converges for |a|<Λ. It makes the entire infrared nonanalyticity
of this specified leading density explicit; the cutoff tail is analytic.
After its constant/linear terms the analytic-tail error on |a|<=h<Λ obeys

    |R_tail|<=c h² Λ^(ν-2)/[(2-ν)(1-h/Λ)].             (T4)

Proof: expand 1/(ε+a) in a/ε for ε>=Λ; use n-ν>=2-ν for n>=2 and sum the
geometric tail. A finite second-derivative bound is
2cΛ^(ν-2)/[(2-ν)(1-h/Λ)^3], by termwise differentiation and the sum of
n(n-1)(h/Λ)^(n-2). It concerns the cutoff tail, not the fractional term.

For a lower edge, z=t0+s+i0 with s>0 gives a^ν=s^ν exp(-iπν). For an upper
edge, z=t0-s+i0 gives a^ν=s^ν exp(+iπν). In either case the nonanalytic
term has Im K=-πc s^ν: the two orientations obey the same retarded sign.
This is the Cauchy transform of a positive measure, not a principal-value
reactance substituted for a retarded scattering amplitude.

For ν=1/2 the exact finite-cutoff transform is elementary:

    K_lead=-2σc[√Λ-√a atan(√Λ/√a)].                    (T5)

Thus a finite value at an edge can have -K'~πc/(2√δ) on the gap side
(a=δ>0). No finite constant-A derivative can represent that limit.

## T3. Uniform regular remainder, including the critical exponent

If p>1, the signed residual transform has finite constant and linear moments
at t0. For a=δ>=0 its exact remainder after those moments is

    R_r=-σ δ²∫_0^Λ r(ε)/[ε²(ε+δ)] dε.                 (T6)

Its uniform bound is Q_p(B,δ,Λ), where

    Q_p = Bπ δ^p/sin[π(p-1)]                  (1<p<2),
          Bδ² log(1+Λ/δ)                     (p=2),
          Bδ²Λ^(p-2)/(p-2)                   (p>2).     (T7)

Set Q_p(B,0,Λ)=0. For 1<p<2 extend the positive integral in (T6) to infinity
and scale ε=δu; for p=2 integrate 1/(ε+δ); for p>2 bound 1/(ε+δ)<=1/ε.
Also |K_r'|<=BΛ^(p-1)/(p-1) throughout the real gap-side interval.
These are value and C¹ bounds: for 1<p<=2 the second derivative can still
diverge. Calling the complement regular does not imply it is analytic.

For complex a with |arg(a)|<=π-θ, θ>0, one has
|ε+a|>=κ(ε+|a|), κ=sin(θ/2). Consequently the complex value remainder is
bounded by Q_p(B,|a|,Λ)/κ and its first derivative by
BΛ^(p-1)/[(p-1)κ²]. This sector estimate excludes approach along the interior
of the cut. A pointwise density envelope alone cannot provide a uniform
retarded/PV interior bound; the counterexample is in the cycle ledger.

Uniformity in composition requires a declared interval I, uniformly bounded
c(x), B(x), S(x), a common cutoff Λ (or certified positive cutoff limits),
fixed exponents with p>1 bounded away from 1, and a remote separation
d(x)>=d0>h. For the gap-side derivative the remote contribution is bounded
by S/(d0-h)². Moving t0(x) is allowed: all estimates use the moving energy
w=z-t0(x). No x derivatives of t0 or c are supplied by these energy estimates.
A uniform composition root slope remains a separate requirement.

## T4. Preserve causality when subtracting an infrared contribution

Subtracting cε^ν can leave a signed residual. Its energy-linear approximation
need not be causal, even though the complete kernel is. There is an elementary
positive subtraction when (T2) is known. Choose a cutoff satisfying
BΛ^(p-ν)<=c and retain

    ρ_IR(ε)=c ε^ν-B ε^p>=0,
    ρ_R(ε)=ρ(ε)-ρ_IR(ε)=r(ε)+Bε^p,
    0<=ρ_R(ε)<=2B ε^p.                                (T8)

The remote measure belongs to ν_R as well. If c vanishes, no nonzero lower
envelope is asserted: use the positive density bound directly if it has
p>1, or revise the threshold analysis. For a uniform nonzero infrared
extraction require c>=c_min>0 and a cutoff satisfying the inequality for
the worst B. This is a sufficient construction, not a unique physical split.

Let K_IR be the exact finite-cutoff Cauchy transform of (T8), and define

    C_R=∫ dν_R(t)/(t0-t),
    A_R=∫ dν_R(t)/(t0-t)²>=0,
    K_T(z)=K_IR(z)+C_R-A_R(z-t0).                       (T9)

For Im z>0, -Im K_T=-Im K_IR+A_R Im z>=0. Hence D_T=z-e-K_T and
g_T=D_T^-1 preserve retarded causality everywhere in the upper half-plane.
Constant C_R is real. Unlike a globally claimed physical Dyson approximation,
accuracy is asserted only on the domain of the remainder estimates.

Causality is not a global normalization certificate: for A_R>0 this local
energy-linear closure has g_T(z)~1/[(1+A_R)z] at large |z|, whereas the
exact retained resolvent has coefficient 1/z. Thus it cannot be used for
global spectral weights/centroids without a causal remote-bath completion.
No such completion is uniquely fixed by the displayed moments; the moment
counterexample remains relevant. This limitation does not invalidate the
local value/error theorem or the root residual certificate.

In the real gap-side window 0<=δ<=h<d0,

    |K-K_T|<=Q_p(2B,h,Λ)+A_remote h²/(d0-h)=:ε_α,
    A_remote<=S/d0²,
    |K_R'|<=2BΛ^(p-1)/(p-1)+S/(d0-h)².                 (T10)

The remote error is the earlier exact partial-fraction bound. The near-edge
error is (T7) applied to (T8). Thus the entire complement has a finite,
uniform first derivative, while the divergent leading threshold is retained.
The causal Γ equations are

    D_α,T=(1+A_α,R)z-[e_α+C_α,R+A_α,R t_α]-K_α,IR(z). (T11)

They can be solved as scalar implicit equations without computing raw
T'(t_α). No Born, dilute, or CPA approximation is used to derive (T10).
Supplying their exact alloy measures remains a substantive material problem.
Multiple channels can be added with the same positive-measure construction
and summed error budgets when their stated domains overlap; no uniform
overlap across merging continua is presumed.

## T5. Joint common/mass secant theorem without divergent derivatives

At fixed x let J_x be a real interval whose interior is disjoint from both
measure supports. Allow finite continuous kernel values at its threshold
endpoints. For E2>E1 in J_x put h=E2-E1. Direct subtraction in (T1) yields

    b_α=[K_α(E1)-K_α(E2)]/h
       =∫ dν_α/[(E1-t)(E2-t)]>=0.                    (T12)

The factors have equal sign because the support does not lie between E1
and E2. At a finite threshold endpoint take the one-sided limit; each finite
secant is still finite. Define F_s=(D6+D8)/2 and M=(D8-D6)/2, so that

    ΔF_s=h[1+(b6+b8)/2],
    ΔM=h(b8-b6)/2,
    ΔM=r_sec ΔF_s,
    r_sec=(b8-b6)/(2+b6+b8),        |r_sec|<1.          (T13)

Consequently |ΔM|<=|ΔF_s|, and F_s is strictly increasing with secant slope
at least 1. No separate bound on either raw energy derivative is needed.
In an interior differentiable point this is |∂_E M|/(∂_E F_s)<=1. The
integrated proof, rather than a ratio of two infinities, covers endpoints.

Suppose the exact common root Ebar and an approximate common root Ea lie
in J_x. Let δD_α=D_α-D_α,app at Ea, and μ(x)=M(Ebar,x),
μ_app(x)=M_app(Ea,x). Then F_s(Ea)=(δD6+δD8)/2 and (T13) implies

    μ-μ_app=[(1-r_sec)δD8-(1+r_sec)δD6]/2,
    |μ-μ_app|<=max(ε6,ε8)=:ε                         (T14)

when |δD_α|<=ε_α. The coefficients are nonnegative and sum to one in
absolute value. Correlated scalar/mass errors retain this sharper branch
norm. With only independent ε_s, ε_m one instead obtains ε_m+ε_s.
It is incorrect to assign a new divergent error from an infinite mass
derivative while ignoring the compensating common inverse in this domain.

**Existence gate:** approximate F_s of opposite signs at the endpoints of
J_x with margins exceeding (ε6+ε8)/2 certifies the true common root by
continuity and monotonicity. A vanishing gap interval provides no such
finite margin; perturbations may enter a continuum and void the certificate.
Neither symmetry nor a formal mass zero establishes the domain gate.

## T6. Inversion-root certificate and its indispensable transversality

Assume common roots exist as above on a composition bracket I and μ is
continuous there. Opposite approximate mass signs with magnitudes >ε at
the bracket endpoints certify a true zero. If, in addition,

    μ(x2)-μ(x1)>=m(x2-x1),       x2>x1, m>0,           (T15)

then the zero is unique in I. For an approximate zero xa in I, (T14) gives

    |x_c-xa|<=max(ε6,ε8)/m.                           (T16)

Proof: |μ(xa)|<=ε and the lower secant slope gives
|μ(xa)-μ(xc)|>=m|xa-xc|. Uniform differentiability is unnecessary.
Baseline, strain, physical-frame, spectral-window and approximation errors
must all enter ε_α. A certified nonvanishing mass slope does not follow
from pure endpoint gaps or positive dynamic susceptibilities.

If only a monotone lower modulus |μ(x)-μ(xc)|>=m_p|x-xc|^p is established,
the bound is (ε/m_p)^(1/p). A cubic mass tangency shows why a linear bound
cannot be asserted without (T15). For truly isolated sharp branch poles
in J_x, their energy errors are <=ε_α because D_α has secant slope >=1,
so a signed gap error is <=ε6+ε8. A zero at a branch point need not be a
simple pole and can have zero residue; this pole-error interpretation then
fails, even though the finite real inverse/common-root identities survive.

The theorems concern sharp gap-side or real inverse crossings meeting the
support-free hypotheses. They do not predict continuum peak crossings,
shared complex poles or topological transitions. Those observables retain
the qualifications and additional inputs of the earlier foundation.

## T7. A mass-sign bracket without solving the common energy numerically

Once existence of the common root in J_x is independently certified, (T13)
also applies between that root and **any** trial energy E* in J_x:

    μ(x)=[(1-r_sec)D8(E*,x)-(1+r_sec)D6(E*,x)]/2.       (T17)

Thus D8(E*,x)>0 and D6(E*,x)<0 imply μ(x)>0; reversing both signs implies
μ(x)<0. With computed denominator values replace the signs by margins
exceeding their respective error bounds. Opposite patterns at two trial
compositions, plus continuity, certify an inversion bracket without evaluating
T', recovering both full kernels, or numerically locating Ebar. A lower mass
modulus is needed for the additional residual/sensitivity bound, but not for
existence of a bracket. These sign patterns by themselves do **not** certify
common-root existence in J_x, uniqueness, or physical applicability.

Proof: the coefficients of D8 and -D6 in (T17) are nonnegative and sum to
one; finite distinct-energy secants give strict weights. If the trial energy
is the common root, F_s=0 and the same conclusion holds directly. This is
an observable-focused sufficient input certificate, not a universal count
of microscopic parameters needed for an arbitrary alloy Hamiltonian.
