# Program state: microscopic zero-temperature bandgap

**Portfolio contribution:** R07

**State:** analytical-first identifiability and symmetry reduction established; three conditional closures documented; physical gap prediction unresolved; existing bounded numerical supervision left untouched

**Updated:** 2026-10-11

## Objective and scope

Derive an interpretable, no-alloy-gap-fit equation for the signed
Gamma6-minus-Gamma8 gap and its inversion. The user explicitly authorized this
research continuation on 2026-10-10. Related endpoint infrastructure is tracked
in issue #4; this work does not alter R02's thermal or first-principles gates.
Temperature and empirical coefficient tuning are outside this tranche.

## Analytical-first directive and current decision

The user's 2026-10-11 directive supersedes the computational priority list below.
No additional DFT/MPI/HSE calculations or queues are launched. Existing detached
supervisors retain their established stopping rules and are not modified.
The previous numerical evidence is preserved as a dated snapshot, not upgraded
or reinterpreted by this analytical tranche.

The [analytical package](analytical_first_2026-10-11/README.md) establishes:

- **PROVEN UNDER ASSUMPTIONS:** finitely many endpoint derivatives, and even
  full endpoint impurity operators through any fixed cluster order, fail to
  identify unrestricted fixed local mixed interactions. An exact atomic
  Bernoulli model has unchanged binary/single-impurity data and changed Γ spectra.
- **PROVEN UNDER ASSUMPTIONS:** ensemble Td reduces the retained Γ6/Γ8 problem
  to two scalar causal functions, representable by positive augmented-space
  Feshbach measures. This is a functional reduction, not a two-constant theory.
- **PROVEN UNDER ASSUMPTIONS:** coherent-invisible directional Te/SOC response
  can enter the Γ8 mass self-energy. Gap-relevant covariance contracts to two
  functions at second order; full covariance reconstruction need not be required.
- **PROVEN:** equal static/dynamic moments and total spectral weight do not fix
  the full self-energy or an inversion root. An exact universal two-susceptibility
  prediction from these inputs is **FALSIFIED**; its conditional rational
  identities are preserved.
- **PROVEN UNDER ASSUMPTIONS:** spectral separation gives the nonperturbative
  linearization bound A h²/(d-|h|). A real mass root has conditional error
  [ε_m+(L_m/u)ε_s]/m. Thresholds can invalidate the needed separation/regularity.
- **PROVEN UNDER ASSUMPTIONS:** full-support, finite-range fixed-interaction
  Bernoulli spectral support is x-independent inside (0,1); this established
  phenomenon further separates support edges from measured Γ peaks.

**Decision:** continue threshold-aware analytical development and a quantified
common/mass uncertainty budget. The [ranked input plan](analytical_first_2026-10-11/inputs_and_decision.md)
specifies physical forward contractions as missing information; it creates no
calculation queue. Spectral-moment, weak-covariance and CPA closures each retain
explicit gates and falsification conditions. No physical E_g(x), x_c, material
validation, priority claim or manuscript promotion is established.

## Preserved numerical and analytical evidence from preceding tranches

**CALCULATED:** the SG15 CdTe accurate-empty control reduces the projected
time-reversal defect from 6.37827 eV to 2.95137 meV, while the signed Gamma
gap changes by only 0.8884 micro-eV. The unchanged 1-meV gate still fails;
a 1e-10-Ry seeded SCF refinement was interrupted at its wall limit without
an outer checkpoint and is rejected. The longer-budget HgTe k4/q2 host
stops cleanly without exchange convergence and splits its Gamma8-derived
quartet by 311.9218 meV. A source-checked q=G=0 exchange feedback component
is 297.6848 meV at q2; its blind q4 prediction is 6.711425 meV. A fresh
q4 control stops cleanly with native Gamma6/Gamma8 identity and a 1.052622
micro-eV quartet spread, but exchange error 2.315e-5 Ry fails the unchanged
criterion. An identical-physics continuation is running; no signed HgTe
gap is accepted. At X the two same-material
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
A bounded, checkpoint-checked SCF runner is ready; DFT fast tests: 85 pass.

**CALCULATED:** the prepared Gamma-only n2/q1 supercell preserves the
primitive q2 exchange-feedback spacing. Matched n2/k2/q2 input decks are
prepared to match the finer k4/q4 reference-host spacings; their native
dry checks estimate 78.44/78.49 GiB, exceeding 31.34078 GiB physical RAM.
No full SCF is launched for those decks. Explicit matched Fock-cutoff
120-Ry native dry checks now estimate 21.27/21.32 GiB, within the sampled
total/available-memory budgets. Their seven-process dry peaks are about
169 MiB; these are not full-SCF peaks. The f120 approximation still
requires a matching accepted primitive reference and physical operator
comparison. It cannot modify an existing restart. The full 64-point,
44-band fixed-hydrogenic-trial
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

**CALCULATED:** native same-host extraction in the actual six Gamma6/Gamma8
spinors gives reaction-kernel norm 2.5819e-15 eV. Physical reciprocal-vector
transport handles permutation and integer Bloch relabeling, with mismatched
NC spaces rejected. The 44-band prefix leaves unresolved projector norm
3.6086e-15. This passes a zero-substitution negative control and does not
upgrade material accuracy or calculate a physical impurity coefficient.

**PROVEN under static localized-substitution assumptions:** unresolved
fixed-host-edge projector norm is bounded by
sum_a ||V Phi_a||^2/(Lambda-E_a)^2. Its conditional O(1/Ncell) scaling
explains a possible window advantage over local atomic trials; actual
self-consistent localization and continuum/volume limits remain untested.

**PROVEN continuum qualification:** Herm(T[g^R]) generally differs from
T[Herm(g^R)]. A common complex mass zero characterizes a shared complex
pole; a real-energy ordering crossing can occur with unequal linewidths
without such a shared pole. The real-denominator, spectral-peak and complex
pole observables must be distinguished before using a mass-route x_c.
**CALCULATED:** the archived-model 21-row continuation audit verifies the
ordered reactance/retarded conversion to 5.64e-16 relative error, with a
real mid-gap CdTe equality control. It predicts no new physical coefficient
or inversion composition. See the [continuum gate](../../../docs/derivations/continuum_prescription_and_crossing.md).

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

**PROVEN under fixed tetrahedral covariance:** coherent Bernstein derivatives
determine order-averaged orbital vertices. Full local covariance adds a
positive directional term that those derivatives cannot determine. In the
restricted real spin-independent Te p-onsite sector, three coherent scalars
and four directional coefficients reconstruct all 16 environments from
three oriented representative matrices. Directional one-body Frobenius
scattering has the complementary filter (2/9)(16-|F(q)|^2). It is zero at
q=0 and maximal at scalar form-factor zeros; pair/triplet configurational
channels remain white. Exact stabilizer ranks and exhaustive covariance,
tomography and Fourier audits pass to 3.55e-15. No physical coefficient,
linewidth or susceptibility is inferred.

**PROVEN for the local time-reversal-even spinful p sector:** the oriented
closure has 14 endpoint-invisible coefficients, six coherent and eight
directional. For a chemical quadrupole a(T tensor I) plus a directional
SOC quadrupole alpha Q(T), the angular j=3/2 intra-sector amplitude is
a-2alpha while j=3/2-to-j=1/2 amplitude is a+alpha. Vanishing intra-sector
anisotropy does not imply vanishing inter-sector coupling. The spinful
proper/improper rotation and angular audit passes to 1.48e-15. These
are local angular projectors, not the complete Bloch branch T-matrix.

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
- [Continuum prescription and broadened crossing qualification](../../../docs/derivations/continuum_prescription_and_crossing.md)
- [Archived-model continuum audit](../../../data/calculated/sp3d5_continuum_prescription.json)
- [Coarse HgTe quartet and exchange-component figure](figures/hgte_quartet_feedback.pdf)
- [Finer quartet and impurity memory control](figures/hgte_grid_control.pdf)
- [General oriented tetrahedral response](../../../docs/derivations/oriented_tetrahedral_response.md)
- [Oriented Te p-tensor tomography](../../../docs/derivations/te_p_tensor_tomography.md)
- [Frozen directional identity audit](../../../data/calculated/te_p_tensor_tomography_audit.json)
- [Relativistic onsite tensor closure](../../../docs/derivations/te_p_soc_tensor_tomography.md)
- [Frozen spinful audit](../../../data/calculated/te_p_soc_tensor_audit.json)
- [Self-consistent threshold and centroid derivation](../../../docs/derivations/self_consistent_threshold_and_centroid.md)
- [Frozen endpoint reductions](../../../data/calculated/sp3d5_endpoint_reductions.json)
- [Threshold convergence](../../../data/calculated/sp3d5_cdte_threshold.json)
- [Figure](figures/impurity_reference_and_threshold.pdf)
- [Direct-alloy and threshold figure](figures/self_consistent_threshold_and_alloy.pdf)

## Validation

Latest full repository suite: **1787 passed**, including eleven independent
analytical-first spectral-bound, hidden-interaction, causal finite-bath,
reference/unit-invariance, root-certificate and atomic-CPA checks. The frozen
[synthetic audit and verification](analytical_first_2026-10-11/verification.md)
establish mathematical behavior only. The preceding **1776 passed** included
three independent
binary-curvature, spin-three-halves angular and radial threshold checks.
Independent checks include a full finite-Hamiltonian inverse, numerical T
derivatives, positive off-spectrum norms, the causal optical theorem, direct
threshold quadrature and a bracketed concentration-pole solve.
New checks include random-cell dense inversion versus Lanczos, exact folded
binary spectra, spectral-centroid closure, the full scalar CPA equation,
implicit derivatives, threshold coefficients and the pair indicator limits.

## Historical computational agenda — superseded as current priorities

The following list is preserved to document the earlier numerical route and
its unresolved gates. It is not authorization to launch, restart or take over
any calculation under the current analytical-first directive.

1. Finish the live SG15 HgTe finer-exchange control
   `hgte_hse_sg15_k4_q4_e90_fullacc_c1e-10_t3600_g1800_restart_cee66000` in the companion DFT
   repository before another MPI family. Both coarse CdTe HSE hosts
   converged: signed gaps 1.7048135 eV (PseudoDojo) and 1.5753656 eV (SG15),
   with independently assigned Gamma sectors and verified grid expansion.
   Their 129.4479-meV difference is not attributable to NLCC alone.
   Accurate empty states reduce the 26-spinor matrix defect by over 2000
   times, to 2.95137 meV, still above the unchanged 1-meV gate. DFT commit
   6a1f9f8 contains the completed controls, physical-frame overlaps,
   native trial-unit/capture audit, prepared pair and bounded SCF runner.
   It also records the rejected coarse HgTe quartet and the blind q4
   component prediction; see the [exchange-grid protocol](/home/User/opencode_workspace/DFT/docs/r07_hgte_exchange_grid.md).
   The stricter CdTe refinement was
   killed at its wall limit without a checkpoint and is rejected. It
   needs a new longer-budget calculation. The completed finer-pair native
   default-cutoff memory estimates exceed RAM; f120 pair dry checks now
   fit. Compare matched primitive Fock-cutoff controls
   before any physical extraction. The first q4 terminal control restores
   native Gamma8 identity with a 1.05-micro-eV spread. Exchange convergence
   remains required before accepting that edge. Restoration supports a
   coarse-grid cause; the component's isolated
   gain is not the full SCF Jacobian. Rerun the Gamma assignments,
   projection and native-wavefunction checks after HgTe converges. In
   smeared HgTe, a fixed lowest-36-band slice is not an occupied projector.
   No scattering host is accepted yet. A clean time-limited continuation
   must retain `--accurate-empty` and `--scf-threshold 1e-10`.
   The preceding wrapper exited 143 while its ranks survived. Detached
   supervision preserved the missing native OS status and observed a
   clean stop with six freshly written checkpoints; that run remains
   unaccepted. Its terminal exchange error 2.8e-9 Ry exceeds the unchanged
   1e-10-Ry criterion. The dry probes completed and a fresh unchanged SCF
   now captures its native exit status with full MPI-family supervision.
   DFT commit 82628b7 preserves the terminal and resource records and the
   physical-frame Fock comparison. Its native same-operator CdTe control
   gives a 1.84e-15-eV residual, not an f120 accuracy result.
   A second acknowledged detached owner waits for the exact numerical
   queue, allows at most two unchanged f120 continuation chunks if needed,
   and compares only accepted references through native spinor overlaps
   and window certificates. Both owners enforce one MPI family. These
   bounded numerical sequences start no full impurity SCF; physical
   finite-q operator, isolated-cell and material accuracy remain pending.
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
   Preserve common-frame orbital tensors and bond-resolved hopping directions
   in that extraction before taking any coherent tetrahedral average.

The existing binary-derived vertex is terminated as a candidate physical
predictor at this level. It is retained as a reproducible diagnostic and code test.
No manuscript, material validation, or replacement of Hansen is claimed.
