# Discovery/falsification cycles and the physical-information boundary

No repeated numerical search or material parameter sweep was used. Three
distinct mathematical cycles were completed, with their unsuccessful
extensions retained. Established operator, Cauchy-transform and moment
mathematics are distinguished from possible originality of this R07 synthesis.

## Cycle 1: extract the threshold, then try to make the remainder regular

**PROVEN UNDER ASSUMPTIONS:** [T2–T4](derivation.md) isolate a specified
positive fractional threshold and supply explicit uniform C¹/value bounds
when the subleading weighted density exponent p>1 and the remote spectrum is
separated. A positive lower envelope makes the retained-IR/linear-complement
closure causal even when the signed density error changes sign. Keeping the
finite-cutoff IR transform avoids evaluating a divergent threshold derivative.

**Candidate T, governing equation:** (T11). Required inputs are e_α(x),
t_α(x), the channel exponent/amplitude/envelope, C_α,R, A_α,R and the stated
uniform error/support certificates. Coefficients are microscopic functions,
not empirical bowing constants. This is nonperturbative in the supplied
spectral measure but truncated in the regular energy dependence. Zero
measure gives the coherent gap; zero regular complement gives the exact
finite-cutoff threshold bath. Pure limits require the disorder measure to
vanish at the endpoints, as in the earlier augmented-space construction.

**Attempted extensions and negative results:**

- For r=Bε with p=1, the remainder's first moment ∫r/ε² diverges logarithmically.
  A finite static kernel does not supply a finite regular slope. For 1<p<2,
  the C¹ complement generally has a fractional δ^p remainder; an O(δ²) or
  analytic remainder is not proved. The strict p conditions are necessary
  for this density-envelope argument.
- A density bound alone gives no uniform interior retarded/PV bound. Let
  0<a<b<Λ and r(ε)=B a^p for ε∈[a,b], zero otherwise. This satisfies |r|<=Bε^p, is positive,
  and is identically zero near the original threshold. Its Cauchy transform
  is B a^p log[(z-a)/(z-b)], whose real boundary part diverges at a and b.
  Smooth approximations have arbitrarily large constants without a uniform
  density regularity bound. Gap-side and fixed-slit-sector estimates survive;
  an η-independent full-continuum estimate is **FALSIFIED**.
- A threshold resonance changes the leading kernel class. In the earlier
  unit-bandwidth host g(-δ)=-3+(3π/2)√δ+O(δ), choosing v=-1/3 makes
  T=v/(1-vg)~-[2/(3π)]δ^(-1/2). Nonresonant finite C is unavailable.
  A known bare quadratic dispersion alone does not establish the full
  scattering/exact-alloy weighted density in (T2).
- Individual asymptotics at each x do not supply uniform c,B,S,d bounds.
  Nor do they bound the composition derivative or identify the self-consistent
  concentration power. The archived independent-host x^(3/2) versus CPA x²
  counterexample remains decisive.

**Disposition:** retain T with its explicit domain and rejection gates; reject
an automatic analytic remainder or a continuum extension based only on a
density power. No physical Γ8 envelope or amplitude is assigned.

## Cycle 2: avoid the raw derivative in the inversion uncertainty

**PROVEN UNDER ASSUMPTIONS:** (T12–T16) couple the common/mass secants through
positivity, giving |δx_c|<=max(ε6,ε8)/m. This strictly reduces required input:
raw threshold T' or a finite mass-energy Lipschitz constant is unnecessary
for this certificate. Branch residual values, a common support-free energy
domain and a lower composition mass modulus suffice. The certificate can
be applied to any candidate satisfying its hypotheses, including T or the
prior separated spectral closure S.

**Attempted continuum extension:** take an exactly positive finite bath
dν6=b dt on [-L,L], zero outside, and ν8=0. For |E|<L,

    Re K6=b log[(L+E)/(L-E)],
    (Re K6)'(0)=2b/L.

Choose b/L=0.9. Then at 0 the real common inverse slope is 0.1 but the mass
energy slope is 0.9. Their ratio is 9, violating (T13), despite causality and
a positive common inverse slope. The finite bath is realizable by a bounded
static Friedrichs operator. The gap-side sign argument fails because the
Cauchy denominators straddle support. Retarded causality alone does not
protect -∂_E Re K inside a continuum. This extension is **FALSIFIED**.

**Attempted inference of transversality from positivity:** use ν6=ν8=0 and
coherent mass μ=v(x-x*)³, v>0. A constant mass error ε shifts the root by
(ε/v)^(1/3), so |δx|/ε diverges as ε→0. This causal, symmetry-compatible
coherent counterexample disproves a universal linear root certificate or a
positive composition slope derived from dynamic positivity alone. The lower
composition modulus is indispensable even in the absence of scattering.

**Disposition:** retain the joint certificate in a common gap, and keep the
older Lipschitz certificate when independently established in a continuum.
If neither domain/modulus certificate exists, report an unresolved crossing
instead of selecting a regularization η to manufacture one.

## Cycle 3: does knowing the infrared channel close prediction?

**Candidate M, competing closure:** retain the prior local spectral-moment
equations, K_α,M=C_α-A_α(z-E*), E_α,M=(e_α+C_α+A_αE*)/(1+A_α).
Its required inputs are four composition-dependent moments and positive
support distances. Its exact partial-fraction error is A_αh²/(d_α-h).
It is causal and reduces to the coherent problem when the measure vanishes.
It is cheaper than T when the complete measure is separated, but fails at
an unextracted threshold. T and M are not interchangeable: T keeps an IR
function, while M linearizes it along with everything else. CPA remains the
third established comparison, with its earlier unproved cluster-edge error.

**Strongest identifiability test:** shift the earlier four-pole measures to
t=E*+(0.5,1,-1,-0.5) eV and w_j^±=w0[1±q(1,-2,2,-1)_j], 0<q<1/2.
They have the same C at E*, A there, total weight and support. Add the same
positive finite-cutoff IR measure to both. All specified IR exponents,
amplitudes, thresholds and cutoffs now agree as well; regular C,A,S,d still
agree. The two causal functions nevertheless differ at generic E≠E*.

For a concrete exact sharp-root witness set e8=Ev, e6=Ev+2v(x-x0), and
couple only Γ6 to k(x)[ν_IR+ν_±], k=x(1-x). At E=Ev the crossing obeys

    2v(x_c-x0)+k_c[K_IR(Ev)+K_±(Ev)]=0.                (B1)

With Ev=0.1 eV, E*=t_IR=0.3 eV, Λ=0.4 eV, c=0.04 sqrt(eV), w0=0.02 eV²,
q=0.2, v=0.8 eV, x0=0.23, the two roots differ by more than 10^-4.
The moments are evaluated at the IR threshold itself, matching the input
reference in T9. These are synthetic parameters, not HgCdTe estimates. Small baths ensure
the relevant poles are simple and lie in their common support-free gap.
Each model is a self-adjoint finite-discrete-plus-continuum bath with positive
weights; multiplying by k preserves both binary endpoints. This effective
causal family is not claimed to reconstruct a fixed-interaction Bernoulli
alloy. The preceding [I1 fixed-local counterexample](../analytical_first_2026-10-11/identifiability.md)
already proves non-identifiability in that stronger microscopic class.

**Conclusion — PROVEN:** supplying the IR channel and finite regular moments
does not uniquely close an exact inversion. It can close a *bounded*
approximation via T10/T16. A gap/slope certificate is as consequential as
an extra moment. The exact-equation claim is **FALSIFIED**, not repaired by
fitting an interior coefficient.

## Precisely what missing physical information is indispensable?

For a declared real inverse-root observable define the material function

    μ_phys(x)=[e6(x)-e8(x)+K6(Ebar(x),x)-K8(Ebar(x),x)]/2,
    Ebar-(e6+e8)/2-[K6(Ebar,x)+K8(Ebar,x)]/2=0.        (B2)

An independently qualified value/bound of the **interior projected mass
contraction on this common trajectory**, or a microscopic restriction that
determines it with a uniform error bound, is indispensable. This is a
functional sufficiency statement; it does not imply that one universal
scalar measured at an endpoint identifies the full curve. The same material
input can be represented as two branch denominator values on a trial
common-energy domain, avoiding a full orbital covariance or Wannier survey.
Directional response enters only through these contractions; it cannot
be dropped if it changes them.

Proof of necessity: in (B1) the unseen parameter H=K_IR(Ev)+K_±(Ev) changes
the root, with exact sensitivity

    ∂x_c/∂H=-k_c/[2v+(1-2x_c)H].                     (B3)

Every supplied IR/regular moment input is identical in the two worlds. Any
deterministic estimator based only on those inputs returns the same number;
its maximum error is at least half the two-root separation. More broadly,
I1 hides mixed interactions from any fixed endpoint cluster order. Thus
physical endpoints plus symmetry cannot remove the missing mass information.
No physical error scale is inferred from the synthetic separation.

**Minimum sufficient interval information:** (i) a declared common support-free
energy domain with residual sign margins; (ii) branch denominators with known
uniform errors over a composition bracket; (iii) a continuous reduced mass
with a lower composition modulus. At desired accuracy Δx, the gap-side
requirement is max(ε6,ε8)<=mΔx, including all model/input errors. A certified
mass sign bracket narrower than Δx can suffice without determining the full
functions. T17 further shows that, after the common-root domain/existence
gate, opposite branch-denominator signs at one trial energy per composition
can certify that bracket without solving for the common energy. Endpoint
data without an interior-remainder certificate do not
provide that bracket. For a peak crossing or a topological boundary, (B2)
is insufficient and the prior damping/global-information gates remain.

## Ranked missing-input matrix: information gain before computational precision

This is a logical input plan, not a queue or an expensive-computation proposal.
No new DFT/HSE/MPI/supercell work is justified here. Existing rejected artifacts
do not become accepted because the analytical bounds improve.

| Rank | Input / units | Information gained and sensitivity | Availability / least costly alternative | Required fidelity / cost boundary |
|---|---|---|---|---|
| 0 | Observable and common energy support domain / eV | Determines whether T13–T16 apply at all | Conditional CdTe quadratic and HgTe continuum warnings; physical domain unestablished | Reasoning and qualified existing spectra first; no calculation authorized |
| 1 | Interior branch-denominator/mass contraction bounds / eV | Separates admissible worlds in B1; directly bounds x_c | No accepted physical forward impurity amplitude or controlled alloy mass remainder; T17 can use sign margins at one trial energy per composition after the common-root gate | max ε_α<=mΔx; invariant forward projections can suffice; expensive cost not estimated or authorized here |
| 2 | Mass lower secant modulus m / eV per x and sign bracket | Converts mass errors into root accuracy/existence; identifies tangencies | No physical interior modulus; endpoint slopes do not certify it | Analytical interval inequalities from a declared material model; small operations once inputs exist |
| 3 | Weighted IR edge t_α / eV, ν, c / energy^(1-ν), envelope B / energy^(1-p) | Decides finite moments and supplies singular energy function | Only conditional binary/isolated-impurity coefficients; exact alloy amplitude unknown | Compute none if a separated domain or existing bounds suffice; otherwise needs a qualified projected low-energy channel, not all finite-q tensors |
| 4 | Regular C_R / eV, A_R dimensionless, density exponent p and remote S/d | Predictive T11 and error T10 | No material values; synthetic coefficients are not inputs | Accept when Q_p(2B,h,Λ)+A_remote h²/(d-h) meets the branch budget; tighter digits beyond that budget have no value |
| 5 | Composition dependence/connected mixed remainder / eV | Prevents finite-endpoint interpolation from becoming a false global prediction | Fixed-local tomography is conditional; hidden-interaction theorem remains | Supply a rigorous remainder bound or a restricted microscopic interaction model; a pair datum alone is not universally sufficient |
| 6 | Damping/peak curvature or global mobility/topology information | Necessary only for those alternate observables | No physical peak or topology gate established | Cannot replace it with a finite η or Γ-only mass zero |

The new certificate removes unregularized threshold T' from the highest-priority
inversion input list in the common-gap regime. It does not eliminate static
mass response, spectral-domain information, composition transversality, strain
or model accuracy. In a continuum the same simplification has been disproved.

## Concise decision and discovery ledger

| Cycle / ID | Status | Retained result / decision |
|---|---|---|
| 1 / T2–T3 | PROVEN UNDER ASSUMPTIONS | Fractional term and uniform C¹/value remainder isolated with explicit coefficients and domain |
| 1 / T4 | PROVEN UNDER ASSUMPTIONS | Positive lower envelope preserves causal threshold-plus-regular closure |
| 1 / N1 | FALSIFIED | Density power alone implies an analytic remainder, no resonance, or a uniform interior-cut bound |
| 2 / T5–T6 | PROVEN UNDER ASSUMPTIONS | Joint secants remove the divergent raw derivative from a common-gap inversion certificate |
| 2 / T7 | PROVEN UNDER ASSUMPTIONS | Interior opposite branch signs can certify a mass-sign bracket without numerically solving the common energy, after its existence/domain gate |
| 2 / N2 | FALSIFIED | Causality alone extends that contraction into a continuum or ensures positive composition transversality |
| 3 / B1–B3 | PROVEN | Identical IR and regular finite-moment inputs can have distinct sharp crossings; a missing interior mass contraction matters |
| 3 / N3 | FALSIFIED | Those inputs force an exact universal two-susceptibility law |
| V | CALCULATED | Independent integrals, finite Hermitian baths and threshold/continuum counterexamples pass synthetic checks |
| H | HYPOTHESIS | A material-qualified narrow-window Γ contraction may achieve a useful conditional inversion interval with fewer inputs than full tomography |
| O | OPEN | Physical HgCdTe's kernel, common-gap applicability, bounded mixed remainder and root modulus |
| P | POTENTIAL NOVELTY — UNVERIFIED | Application of the joint threshold-safe branch residual certificate and positive-envelope closure to R07; underlying mathematics is established |

**Decision:** stop this analytical tranche at the proven missing-input boundary;
do not advance T or M as a physical HgCdTe equation. Both are reviewable
conditional predictive models. Reject continuum/two-moment universal claims,
retain the proofs and counterexamples, and require a physically qualified
mass/domain/error input before another prediction attempt. The user prohibited
new expensive acquisitions; this decision neither launches one nor modifies
existing detached supervision. No repetitive analytic or numerical retry is
queued. The broad persistent objective remains unresolved.
