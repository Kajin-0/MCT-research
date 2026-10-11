# Program state: microscopic zero-temperature bandgap

**Portfolio contribution:** R07

**State:** reference/direct-alloy audits complete; physical frame unresolved; coarse HgTe quartet fails; finer exchange-grid control running; impurity inputs prepared

**Updated:** 2026-10-11

## Objective and scope

Derive an interpretable, no-alloy-gap-fit equation for the signed
Gamma6-minus-Gamma8 gap and its inversion. The user explicitly authorized this
research continuation on 2026-10-10. Related endpoint infrastructure is tracked
in issue #4; this work does not alter R02's thermal or first-principles gates.
Temperature and empirical coefficient tuning are outside this tranche.

## Current evidence

**CALCULATED:** the SG15 CdTe accurate-empty control reduces the projected
time-reversal defect from 6.37827 eV to 2.95137 meV, while the signed Gamma
gap changes by only 0.8884 micro-eV. The unchanged 1-meV gate still fails;
a 1e-10-Ry seeded SCF refinement was interrupted at its wall limit without
an outer checkpoint and is rejected. The longer-budget HgTe k4/q2 host
stops cleanly without exchange convergence and splits its Gamma8-derived
quartet by 311.9218 meV. A source-checked q=G=0 exchange feedback component
is 297.6848 meV at q2; its blind q4 prediction is 6.711425 meV. A fresh
q4 control is running, with all physical settings fixed. Its outcome is
pending; no signed HgTe gap is assigned. At X the two same-material
physical frames have minimum overlap singular value 0.109056 and a
same-label matrix difference of 6.30703 eV, invalid as an impurity operator.

**CALCULATED:** the matched fixed-ion 16-atom HgTe/Cd-in-HgTe inputs pass
native QE dry runs with estimated dynamical memory about 14.1 GB. No
self-consistent impurity result or dilute coefficient exists yet.

**CALCULATED:** native radial coefficient reconstruction matches Gamma and
X amplitudes to about 7e-13. The pinned QE 7.5 standalone interface uses
the numeric zona=1 as 1 inverse bohr; the earlier inverse-Angstrom metadata
description was inaccurate. The 26-band window captures only 0.0162204 of
the least-captured fixed physical trial direction at X. All 44 supplied
bands raise this to 0.469856. These are trial-norm fractions, not gap errors.
Identical ordered 208-spinor trial blocks are prepared for the paired cells.
A bounded, checkpoint-checked SCF runner is ready; DFT fast tests: 67 pass.

**CALCULATED:** the prepared Gamma-only n2/q1 supercell preserves the
primitive q2 exchange-feedback spacing. Matched n2/k2/q2 input decks are
prepared to match the finer k4/q4 reference-host spacings; their native
resource check is pending. The full 64-point, 44-band fixed-hydrogenic-trial
resolvent fails the sufficient inverse certificate (product 58.86078).
A different reference-UPF atomic s/p projector has a pointwise Gamma
omitted-window inverse bound 2.355045 meV, but a worst finite-q bound
484.115 meV. Reference-radial reconstruction and transport to the impurity
remain pending. The bound assumes exact eigenpairs; SCF/grid and residual
errors are separate. These are physical-projector controls, not a T-matrix.

**PROVEN:** fixed-physical-trial projected resolvents admit an omitted-band
error certificate from the unresolved spectral norm and distance to the
omitted spectrum. A separate energy-dependent effective inverse difference
must not be confused with the ambient physical impurity T-matrix.

**PROVEN:** actual host eigenstates provide an invariant physical projector
with exact R0. The impurity spectrum projected onto the same host spinors
then yields both full finite-volume T_P and the distinct P-irreducible
reaction kernel K_P. Full finite-box T can vanish on shell because of the
one exact host pole; reaction-kernel volume convergence or ordered volume
and energy limits are required. No physical endpoint value is computed yet.

**PROVEN under an isolated quadratic Gamma8 threshold and nonzero finite
forward amplitude:** the gap-side contribution to -T8' scales as
tau8^2 k8/sqrt(delta). **CALCULATED:** k8=0.5119895494464 eV^(-3/2) for
the published CdTe binary model, whose projected linear term vanishes.
Physical linear BIA and the inverted-HgTe continuum require separate checks;
this is not the physical total A. A finite A_slope cannot be equated to a
divergent unregularized endpoint derivative under those assumptions.

**PROVEN:** a composition-dependent volume path adds homogeneous-strain
terms to fixed-volume impurity endpoint slopes. These must be accounted
for before interpreting the boundary slope sum as dynamic susceptibility.

**PROVEN:** full host-referenced impurity T cannot also be added as a residual
to a binary chord. The correct residuals are t_H=tau_H-DeltaM and
t_C=tau_C+DeltaM. The handoff mass law is valid with these residuals.

**PROVEN:** for an embedded lattice Green function, g'=-P G^2 P*, generally
not -g^2. At complex energy the positive scattering-cloud norm is
-Im(T)/eta, generally different from -Re(T').

**PROVEN:** a three-dimensional quadratic threshold with nonzero constant
scattering amplitude allows finite T but divergent T'. An exactly integrable
independent-impurity example has an x^(3/2) pole correction, so bounded Hermite
remainders and finite endpoint curvatures need a regularity check.

**CALCULATED:** Schindler's published sp3d5 binary model has been rebuilt.
Gamma signed gaps are -0.3015709 and +1.5981345 eV. X and L checks, SOC,
time reversal, finite-q uniform-vertex closure and embedded sum rules pass.
Its VCA inversion is x=0.1816612.

**CALCULATED:** for the explicit quarter-share Te partition and 0.4 eV source
offset, exact single-impurity resummation retains a large static discrepancy.
On a 30^3 grid at eta=50 meV, the corrected common-mode cubic root is
0.3321358; the branch-pole reciprocal reduction root is 0.3496545.
Using full T twice instead gives 0.1646405, a spurious apparent success.
These are finite-broadening diagnostic interpolants, not physical x_c predictions.

**CALCULATED:** at the CdTe Gamma8 threshold the real gap-side derivative
grows from 13.58 to 63.02 as the even grid increases from 6^3 to 30^3,
while T8 remains finite (1.276 to 1.305 eV). Finite-gap detuning regularizes
the trend. This disfavors extracting a constant dynamic A from the unqualified
endpoint derivative of the full lattice T.

**CALCULATED:** explicit n=8 and n=12 random supercells of the same frozen
linear-substitution Hamiltonian give Gamma spectral-peak separation -138 meV
at x approximately 0.18, and a peak crossing near x=0.30. The latter is not
a topological-invariant determination. Iteration, two seeds, box size and
eta=5–50 meV controls support the large discrepancy beyond the endpoint
interpolation. No empirical gap coefficient was used.

**PROVEN:** every configuration of this linear model has the VCA Gamma
spectral centroid exactly; its spectral maximum need not coincide with it.

**PROVEN within scalar CPA:** self-consistency changes the declared
independent-host x^(3/2) threshold correction to x^2. CPA DOS edge, Gamma
spectral peak and real-denominator root have different x^2 coefficients.
The conventional omitted-cluster indicator remains order one in the same
layer. This is not a controlled asymptotic statement about exact HgCdTe.

**HYPOTHESIS:** a physical, self-consistent substitution potential may still
reduce the static discrepancy through environmental response and charge transfer.
The current test supplies no evidence that resummation alone is sufficient.

**NOVELTY CANDIDATE:** none established in this tranche. The value is the
specific falsification and corrected HgCdTe prediction protocol. Generic Dyson,
optical-theorem, threshold and interpolation mathematics is established.

## Artifacts

- [Calculation and interpretation](result_2026-10-10.md)
- [Direct-alloy and self-consistency result](result_2026-10-10_self_consistency.md)
- [Hybrid host capability and core-approximation gate](result_2026-10-10_hybrid_gate.md)
- [Completed host comparison and projected-frame failure](result_2026-10-10_projected_host.md)
- [Empty-state repair and physical-frame negative control](result_2026-10-11.md)
- [Portable hybrid host record](../../../data/calculated/static_hse_binary_gate_20261010.json)
- [Reference and threshold derivation](../../../docs/derivations/impurity_reference_and_threshold.md)
- [Endpoint volume-path correction](../../../docs/derivations/endpoint_volume_path.md)
- [Conditional Gamma8 threshold kernel](../../../docs/derivations/gamma8_threshold_kernel.md)
- [Frozen Gamma8 kernel](../../../data/calculated/gamma8_quadratic_threshold_20261011.json)
- [Fixed-trial resolvent and spectral-window certificate](../../../docs/derivations/fixed_trial_resolvent.md)
- [Host-invariant reaction kernel and finite-volume pole limits](../../../docs/derivations/host_invariant_reaction_kernel.md)
- [Coarse HgTe quartet and exchange-component figure](figures/hgte_quartet_feedback.pdf)
- [Self-consistent threshold and centroid derivation](../../../docs/derivations/self_consistent_threshold_and_centroid.md)
- [Frozen endpoint reductions](../../../data/calculated/sp3d5_endpoint_reductions.json)
- [Threshold convergence](../../../data/calculated/sp3d5_cdte_threshold.json)
- [Figure](figures/impurity_reference_and_threshold.pdf)
- [Direct-alloy and threshold figure](figures/self_consistent_threshold_and_alloy.pdf)

## Validation

Latest full repository suite: **1776 passed**, including three new independent
binary-curvature, spin-three-halves angular and radial threshold checks.
Independent checks include a full finite-Hamiltonian inverse, numerical T
derivatives, positive off-spectrum norms, the causal optical theorem, direct
threshold quadrature and a bracketed concentration-pole solve.
New checks include random-cell dense inversion versus Lanczos, exact folded
binary spectra, spectral-centroid closure, the full scalar CPA equation,
implicit derivatives, threshold coefficients and the pair indicator limits.

## Next decision-changing work

1. Finish the live SG15 HgTe finer-exchange control
   `hgte_hse_sg15_k4_q4_e90_fullacc_c1e-10_t3600_g1800` in the companion DFT
   repository before another MPI family. Both coarse CdTe HSE hosts
   converged: signed gaps 1.7048135 eV (PseudoDojo) and 1.5753656 eV (SG15),
   with independently assigned Gamma sectors and verified grid expansion.
   Their 129.4479-meV difference is not attributable to NLCC alone.
   Accurate empty states reduce the 26-spinor matrix defect by over 2000
   times, to 2.95137 meV, still above the unchanged 1-meV gate. DFT commit
   152e801 contains the completed controls, physical-frame overlaps,
   native trial-unit/capture audit, prepared pair and bounded SCF runner.
   It also records the rejected coarse HgTe quartet and the blind q4
   component prediction; see the [exchange-grid protocol](/home/User/opencode_workspace/DFT/docs/r07_hgte_exchange_grid.md).
   The stricter CdTe refinement was
   killed at its wall limit without a checkpoint and is rejected. It
   needs a new longer-budget calculation. After the live job ends, resource
   check the n2/k2/q2 prepared pair rather than silently reusing its coarse
   Gamma-only estimate. Compare the q4 quartet spread,
   occupations and orbital/symmetry identity before accepting a Gamma8
   edge. Restoration supports a coarse-grid cause; the component's isolated
   gain is not the full SCF Jacobian. Rerun the Gamma assignments,
   projection and native-wavefunction checks after HgTe converges. In
   smeared HgTe, a fixed lowest-36-band slice is not an occupied projector.
   No scattering host is accepted yet. A clean time-limited continuation
   must retain `--accurate-empty` and `--scf-threshold 1e-10`.
2. Obtain or compute a common-gauge, self-consistent Cd-in-HgTe potential and
   the reciprocal Hg-in-CdTe potential with defensible binary electronic structure.
   First test the host-invariant edge-spinor resolvent/reaction-kernel route,
   retaining full nonlocal HSE through the impurity spectrum. Certify its
   window and cell-size/continuation limits before interpreting an endpoint
   shift; the finite-box on-shell full T is not a dilute amplitude.
   Test frozen reference-potential atomic radial projectors and enlarge
   the supplied spectral window; do not identify native host/impurity
   atomic labels as one physical basis.
   The present PBE endpoint artifacts are not adequate meV-level inputs.
3. Use the corrected full/residual conventions and define the HgTe common-mode
   continuation explicitly. Declare the lattice path: fixed-volume impurity
   derivatives omit the endpoint homogeneous-strain terms when a(x) varies.
   Freeze branch values and mass roots before validation.
4. Determine the threshold channel selection, the intended spectral observable,
   and self-consistent linewidth
   before treating T' as a finite constant-A input or invoking endpoint pair
   curvatures. CdTe mid-gap mass evaluation is a cleaner control than its band edge.
5. Test local-background dependence and irreducible environment clusters only
   after the physical one-impurity problem; add no empirical bowing coefficients.

The existing binary-derived vertex is terminated as a candidate physical
predictor at this level. It is retained as a reproducible diagnostic and code test.
No manuscript, material validation, or replacement of Hansen is claimed.
