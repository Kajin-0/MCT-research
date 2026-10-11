# Minimum physical inputs, uncertainty budget and decision

This is an information plan, not a calculation queue. **No additional DFT,
MPI, supercell, HSE, or expensive model work is authorized or launched by this
package.** Existing detached supervisors retain their earlier bounded rules;
neither their files nor processes are modified here.

## What a precision requirement must establish

First select the observable. For a sharp/real-denominator inversion the operative
certificate is

    ε_m+(L_m/u)ε_s ≤ m Δx_target.                        (30)

For a sharp signed gap it is ε6/b6+ε8/b8≤ΔE_target. Include baseline, impurity,
spectral-window, physical-frame, model-truncation and continuation errors in the
same budget. A micro-eV eigenvalue convergence is not consequential while an
unresolved physical operator changes the reference by 129 meV or while the
chosen approximation has no finite edge certificate. For peaks, include damping
and peak curvature errors; neither (30) nor a bare T derivative is enough.

The prior targets Δx_target=0.003 and ΔE_target=5 meV remain scientific goals,
not observed inputs. As an **illustrative budget only**, a certified m=0.5 eV
per unit x would require ε_μ≤1.5 meV; m=1 eV would allow 3 meV. No material
mass-slope bound is assigned by this illustration. Numerical tolerances must
be derived from measured/calculated m, u, L_m and model errors, not chosen first.

For a candidate local interval |E-E*|≤h_max, S contributes a known upper
energy-truncation error A_α h_max²/(d_α-h_max). If that already exceeds the
budget, finer eigenpairs cannot make that closure predictive. Reduce the
energy window, retain the full scalar energy function, or reject the model.

## Ranked computational-input matrix

Ranking concerns expected information per cost and logical dependency; it is
not permission to acquire any missing expensive row now. Costs are estimates
for future proposals. Existing values are diagnostics with their original
qualifications, not automatically accepted inputs.

| Rank | Quantity / units | Role and sensitivity | Existing availability | Analytical alternative / minimum fidelity | Cost estimate / error contribution |
|---|---|---|---|---|---|
| 0 | Observable, lattice/background path, branch/projector conventions | Defines what x_c means; avoids comparisons of different crossings | Exact continuum, strain and host-projector derivations exist | Specify by reasoning; reject ambiguous comparison | No native calculation; no RAM/CPU scaling issue |
| 1 | Two symmetry-contracted Γ kernels as functions on the required energy window / eV | Determines static mass and common energy; δx bounded by (30) | No accepted physical self-consistent impurity amplitude; archived binary-derived vertex rejected | Extract invariant forward contractions directly; full common-Wannier operator is sufficient but unnecessary for the endpoint observable | Future matched static operators expensive; numerical extraction once available is small; allocate ε_m, ε_s from (30) |
| 1a | Certified support/threshold information d_α / eV, weighted low-q power and nonzero coupling | Decides whether moment closure and endpoint derivatives exist | Conditional Γ8 kernel and self-consistent scalar threshold audits exist, physical weighted channel unresolved | Symmetry may force a coupling to vanish; otherwise keep a nonanalytic channel instead of differentiating at a threshold | Existing-data/analytical review first, MB-scale; no blanket new grid; if d=0 the finite-window S certificate is unavailable |
| 2 | Local derivative/bracket bounds m / eV per x, u and L_m / dimensionless | Converts input errors into a root interval; certifies uniqueness locally | Exact formulas, no material lower bound | Interval bounds from a declared microscopic model; endpoint slopes alone do not certify an interior lower bound | Small analytical/interval operations; an unbounded uncertainty invalidates the prediction rather than demanding more digits |
| 3 | Binary e6,e8 and energy alignment / eV | Sets baseline mass/common energy | Published sp3d5 binaries; qualified HSE references with quadrature/core uncertainties | Use an explicitly approximate binary Hamiltonian for theorem/model tests; require compatible physical operators for prediction | Reuse existing qualified outputs first; binary error enters ε_m, ε_s; no new reference sweep |
| 4 | Full endpoint mass projections τ_mH, τ_mC / eV per dilute fraction | Supplies endpoint slopes; residuals subtract ±ΔM once | Unresolved physical values; archived full-T values are not predictive | Host-invariant reaction kernel avoids full Wannier tomography; two slopes suffice only for a boundary interpolant | Conditional proposal below; forward-mass tolerance follows (30), not a universal 1-meV rule |
| 4a | Branch-pole shifts τ6(E6), τ8(E8) / eV, including imaginary parts | Gap endpoint derivatives; damping and branch/common distinction | Archived diagnostic values only | Preserve complex values; compare with mass route only under explicit sharp-pole/closure conditions | Same matched spectrum may supply them; near-edge derivative/η extrapolation not automatically cheap or regular |
| 5 | Directional covariance contractions (16), or the two atomic weighted norms (17) / eV² | Needed only when nonzero in the mass/gap map | Exact p/SOC tensor basis and frozen audits, no physical coefficients | Quotient the covariance by its Γ kernel; symmetry-forbidden amplitudes need no computation | Small extraction from an already available oriented operator; a new environment SCF is expensive and not currently justified |
| 6 | Homogeneous deformation corrections a'∂_a e_α / eV per x | Endpoint volume-path correction; changes mass and slope-derived A | Chain-rule protocol exists; physical corrections unavailable | Fix one lattice for the whole model, or bound rather than assume these terms negligible | Future binary strain inputs only if omitted strain exceeds (30); cost/convergence requires a separate operator-qualified pilot |
| 7 | Connected mass pair response / eV per concentration² | Bounds failure of endpoint closure; scalar pair delayed in regular endpoint mass expansion | No physical pair value; fixed local tomography theorem exists | I1 proves some mixed input or a bound is necessary; under fixed n=4 count symmetry one curvature fixes coherent H2 | Future pair SCF not authorized; resources unknown until a qualified base impurity exists; no broad pair survey |
| 8 | Γ damping function Γ_α(E,x) / eV and derivative / dimensionless | Essential for peak definition via F4, not for a sharp Hermitian mass equation | Existing scalar counterexample; no physical alloy damping | Show a sharp-pole regime with a quantitative error bound or change the reported observable | Cannot infer from finite η; use the same causal kernel if available; otherwise prediction remains conditional |
| 9 | Full momentum/real-space topology and mobility-gap evidence | Required for a topological phase boundary | No current material validation | Restrict claim to Γ ordering until a global invariant is justified | Outside this minimal Γ-gap package; no new computation proposed |

The ranks 1 and 4 are different tasks: the former is sufficient functional
information for a controlled composition model; the latter supplies endpoint
asymptotics. Endpoint information is economical, but I1 shows why it needs an
interior remainder/body-order certificate before it becomes an x_c prediction.

## Conditional justification for the only plausible next expensive input

**Disposition: proposal only; not executed, queued, or authorized as a new run.**

1. **Unresolved analytical question:** does a physical fixed-ion Cd-in-HgTe
   operator provide a well-defined forward mass contraction and a regular
   enough common-energy window to support the chosen real-root observable?
   Binary data and symmetry cannot determine its nonzero mixed response (I1/I3).
2. **Minimum quantity:** a matched-host/substitution spectrum projected onto
   the same six actual host Γ spinors, retaining real and absorptive sector
   kernels in a narrow declared window, with unresolved-weight and continuation
   bounds. Do not require a complete 208-orbital Wannier reconstruction, an
   arbitrarily precise full-band spectrum, or an automatic T' at a threshold.
3. **Uncertainty impact:** bounded errors feed (30). A successful single endpoint
   gives asymptotic information, not a global error bar. A fixed-locality or
   remainder bound is still needed; stop if the resulting budget cannot meet
   the target even with exact input.
4. **Why a theorem or cheaper calculation cannot supply the coefficient:** I1
   and I3 permit independent mixed-response amplitudes. The exact extraction
   identities reduce the required projection but do not compute a material
   operator. First inspect any qualified outputs produced by the existing
   supervisors and assess the spectral gate; no additional reference run is
   needed to learn that a gate already failed.
5. **Acceptance/rejection:** accept only identical static operator conventions,
   NC physical space, symmetry-qualified reference, captured native convergence,
   common electrostatic alignment, a valid omitted-window certificate, and a
   budget derived from (30). A 16-atom periodic fraction 1/8 is not a dilute
   limit. Reject physical endpoint interpretation if volume/continuation error
   is unbounded, the required common-energy observable is undefined, or a
   threshold is forced into a smooth moment closure. Preserve failed results.
6. **Resources:** the existing matched n2/k2/q2 f120 dry estimates are 21.27/
   21.32 GiB on six ranks; they are not full-SCF peaks or an operator-accuracy
   validation. Default f360 estimates 78.44/78.49 GiB exceed 31.34 GiB physical
   RAM and are rejected. A hypothetical capped member of 3600 s plus 1800 s
   checkpoint grace would consume at most approximately 9 core-hours on six
   occupied cores; a matched two-member attempt approximately 18 core-hours.
   This estimates a capped attempt, **not time to convergence**. Additional
   iterations, a truly dilute cell and memory scaling are unknown; no affordable
   completed dilute calculation can currently be promised. The already
   supervised reference sequences remain untouched.

A subsequent connected-pair proposal is premature until this input has a
qualified physical interpretation and its uncertainty decomposition demonstrates
that a pair term, rather than a threshold or baseline error, limits prediction.
It would require its own six-part justification and measured pilot resources.
This document creates no such work queue.

## Decision report

**Established:** binary-only and finite-endpoint reconstruction is not unique
in the allowed fixed-interaction model class; coherent-invisible directional
response can enter the mass; exact Γ symmetry needs two scalar functions;
positivity and two moments do not determine them; a local spectral separation
and derivative bounds can certify a reduced approximation and root accuracy.

**Recommendation:** option 2, **continue analytical development** of the
threshold-aware common/mass functional reduction and its error bounds. Option
3, **acquire a specific missing input**, is conditional on a future separately
justified, approved physical forward-kernel extraction. The already available
data should first be reviewed against the support/observable gate. Do not
advance any current candidate as a validated HgCdTe prediction (option 1).

**Reject/terminate (option 4):** the archived binary-derived quarter-share Te
vertex remains rejected as a physical predictor; its resummation did not cure
the static failure. Reject the universal endpoint-only or exact two-constant
claim. Preserve these artifacts as diagnostics. Do not reject the conditional
Hermite, symmetry, SOC, host-kernel, threshold or rational identities themselves.

**Remaining open:** actual mixed electronic response, applicability of a sharp
mass crossing, the spectral support and regularity needed for S, a controlled
cluster remainder near the edge, background dependence, and a global topological
interpretation. No new physical gap, x_c, empirical validation, or priority
claim follows from the synthetic checks. Temperature remains deferred.
