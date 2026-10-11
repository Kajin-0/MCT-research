# One discriminating acquisition design — unexecuted

**Terminal authorization amendment, 2026-10-11:** the user later approved one
staged host-then-Cd pilot. The first intake was a resource NO-GO; actual headroom
later increased and passed the same guard. The sole host ran and stopped during
exchange initialization at 26.72213-GiB family RSS, above its 26.63966-GiB cap.
Final HSE SCF/exchange FAILED; host projector gates NOT EVALUABLE; Cd NOT ADMITTED.
[Terminal evidence](../native_matched_pilot_2026-10-11/decision.md) preserves source
and old-supervisor pins. No retry, downgrade or queue. Design/estimates below
are the **historical pre-approval record**, not new launch authorization. The
interrupted peak is not a full peak bound or the missing physical response.

## 1. Precise question and minimum quantity

For one specified static-lattice SG15-HSE+SOC Cd-in-HgTe periodic operator,
does physical substitution produce a **certifiably nonzero P-to-Q coupling**
and resolvable projected mass/common response in the fixed host Gamma6/8 frame,
or is the closed-six-state approximation adequate within its observable budget?
The quantitative discriminator is L=-Im K/eta and its sector traces (A3),
together with finite-window m6,n6,m8,n8. No spectral gap D, raw T', ideal
reciprocity, or empirical alloy coefficient is an input.

The minimum new chemistry-bearing packet is the native substituted-cell
Gamma eigenvalues and cross-overlaps with **six fixed physical host spinors**,
with the unresolved positive spectral weight, source/residual metadata and
alignment. The full 6x6 projected R(z) can be retained to check symmetry rather
than silently averaging defects. Neither a full common-Wannier s/p/d vertex
nor separately guessed cation/Te potentials is required for this question.

## 2. Reference gate; honest number of native calculations

Reuse the already accepted primitive HgTe f120 k4/q4 reference for physical
spinor labels and commensurate embedding. The existing n2/k2/q2 f120 matched
pair is 16 atoms, eight cations, fixed a=6.46 Angstrom, Cd fraction 1/8,
288 electrons and 352 spinor bands, cutoffs 90/360/120 Ry, HSE+SOC, identical
NC potentials/geometry, accurate empty states and native SCF threshold 1e-10 Ry.

**Current minimum design has two native SCFs:** the matched pure-supercell
control and the substituted member. An independently proven uniform operator
equivalence/error certificate for primitive folding could replace the former.
The existing constructed CdTe folding negative control and matched exchange
spacing do **not** provide that proof for a self-consistent HgTe supercell.
Skipping the pure member would leave cell-dependent numerical exchange response
confounded with substitution. This is one paired question/design, not a claim
that one impurity job alone currently yields a qualified amplitude.

The f120 HSE operator is a specified approximate electronic model. Its impurity
exchange-cutoff, core, many-body and zero-point errors have not been qualified
as material errors; the binary reference bound does not supply them. A passing
pilot can inform this model's mechanism without qualifying material ordering.

Host spinors use the exact commensurate reciprocal embedding; coefficient
normalization must not receive a second 1/sqrt(8). Native full complex spinor
metric, origin, spin axes, cell, potential hashes and electrostatic convention
must match. Pure-supercell spectral prefixes must use a common global energy
ceiling across folded blocks; the union of 44-band blocks may have holes.
Preserve the reviewed Td/TR identities; require the previous 1-meV projected
numerical host gate, with observed symmetry defects budgeted rather than fitted.

For the A3 substitution discriminator, the actual retained P must commute
with the matched pure-supercell operator. Identify its six physical Gamma
states by native overlaps and symmetry, then hold that spectral projector fixed
for substitution and budget its change from the primitive labels. Failure to
track a unique qualified subspace is an intake rejection. If only the embedded
primitive frame is available, retain total-H leakage with an independently
bounded host-mixing error; a positive total trace alone does not establish
substitution-induced coupling. No continuum-isolated six-state cluster is
assumed merely from a band index.

## 3. Observable and precision budget

Predeclare a **numerical mechanism probe**, not physical inversion: source
native branch midpoint r, W=0.5 eV and eta=0.025 eV. It uses the earlier
native complex-energy control and retained six-state frame. Do not select
a window by fitting an alloy gap. Report known native energy-zero conventions
and any independently bounded alignment uncertainty; shift both spectra and
r jointly for gauge tests. The SCF smearing is separate from eta and from
zero-temperature/zero-point material physics.

A provisional numerical discrimination budget is **2 meV total Omega**,
with <=1 meV per sector. This is a declared pilot budget, not achieved physical
accuracy. At p=0.05, allocate <=0.5 meV per sector to omitted weight and
<=0.5 meV to other numerical source/frame/SCF/exchange-quadrature errors. The bounded
tail formula admits the conservative gate sigma<=3.887e-5; the outward
arithmetic in [acquisition_budget.json](acquisition_budget.json) gives the
exact conditional ceiling 3.88736983095e-5. More bands have no purpose once
the **measured** sigma and total budget pass. If the prefix fails, retain an
inconclusive result; do not automatically enlarge bands/cells or start a queue.

At the same W,eta,p, a blanket operator-norm estimate from S2 would require
roughly **0.141 micro-eV** for a 0.5-meV sector error. This very conservative
worst-case bound is **not** a demand for such numerical precision, and the
binary kernel difference cannot be substituted for it. Prefer independently
bounded *observable* residuals/convergence or a tighter structure-specific
estimate. An SCF total-energy threshold alone is not that error bound.
Unknown material/core/many-body/zero-point errors remain unknown, never zero.

## 4. Acceptance, rejection and expected information gain

| Gate / output | Acceptance | Failure interpretation |
|---|---|---|
| Native matched operators | Existing unchanged source/SCF and numerical host gates; full nonlocal HSE retained through native spectrum | Reject extraction; no chemical attribution |
| Fixed frame and spectral coverage | Native physical overlaps/metric pass; positive omitted weight and residual budget meet the declared allocation | Conditional/inconclusive response; no normalization repair or unbudgeted omitted tail |
| Coupling discriminator | Positive sector L exceeds beta_K/eta, if inverse conditioning passes | If below budget, cannot distinguish closed-P; if negative beyond budget, reject causality/adapter |
| Windowed response | Mass >=p and sector/value error budget passes | No numerical sign/response admission; raw periodic gap is insufficient |
| Static versus leakage diagnostics | Separate Re K mass/common traces and causal leakage with errors | Do not infer a positive constant A or repair old Born C by fitting |
| Physical endpoint/alloy prediction | Additional independent localization/image, law/background/cluster and material controls | Always OPEN after this one-cell pilot; do not label it t_H or x_c |

The gain is the **first independently self-consistent chemistry-bearing response
in the actual retained frame**, which binary controls cannot identify (F1).
It can falsify the closed-six-state mechanism, quantify the unresolved odd
window moments and test whether physical static and leakage responses separate.
No particular sign or A/C scale is forced; the old diagnostic scales are not
acceptance targets. It cannot determine a full Bernoulli alloy or sharp gap.

If the conditional gates pass, the unknown numerical finite-cell ordering
error at this predeclared probe becomes bounded by 2 meV. There is **no proven
reduction of the physical x_c uncertainty**: image/localization, material,
observable and composition-modulus errors remain unbounded. A null or failed
probe is retained as inconclusive; it creates no follow-up queue.

## 5. Why cheap alternatives cannot supply it

Native source review/frame transport is complete; algebra cannot reconstruct
Q/V orientation from binary Gamma spectra or sorted bands. The x=.20 PBE SQS
record lacks the projected packet and error budget. The binary-derived TB vertex
is rejected; fitting its response to a gap is not an input qualification.
Stage-0 raw independent assay/calibration data are unavailable. A generic
causality/endpoint theorem leaves opposite admissible spectra, and one periodic
cell leaves the exact aliasing ambiguity A1. No further source search or
high-precision binary refinement resolves the missing self-consistent density.

For **material operational ordering**, the sufficient minimum remains directly
certified interior moment contractions/sign numerator with physical frame,
composition law and model/probe errors. This pilot is the smallest available
numerical chemistry step, not a replacement for that information. Dilute T
additionally needs an independently controlled localization/periodic-image
remainder and ordered continuum/volume limits; a second size alone is not a
universal bound. True sharp inversion also retains its observable and
composition-modulus gates.

## 6. Honest resource estimate and stopping rule

| Resource | Existing evidence | Unexecuted planning limit / uncertainty |
|---|---|---|
| CPU | Existing preparations use six MPI ranks on eight logical cores | At most six ranks, sequential; no concurrent family or supervisor changes |
| RAM | Prior native f120 dry estimates 21.27 / 21.32 GiB; roughly 169 MiB dry peaks | Full-SCF peak unmeasured; prior 26.64-GiB family cap is a planning ceiling, not certified adequacy |
| Runtime | Native dry runs about 2.04 seconds; primitive controls do not identify substituted SCF cost | Successful full-SCF runtime **unknown**; illustrative fixed budget 3600 s +1800 s checkpoint grace per member; two members <=3 wall hours /18 rank-hours, no automatic continuation |
| Full-f360 alternative | Existing native default pair estimate 78.44 /78.49 GiB | Fails recorded 31.34-GiB machine budget; rejected |

The documented estimate is not permission to execute and not a promise that
the budget converges. A timeout/nonaccepted native result supplies no physical
response. A future explicitly approved run needs a current separate resource
and ownership review by its numerical owner; this research session neither
checks process state nor installs/takes over supervision.

The official [QE input specification](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
states that reducing ecutfock trades accuracy for speed and requires care for
metallic states. The [QE 7.5 memory estimator source](https://raw.githubusercontent.com/QEF/q-e/qe-7.5/PW/src/memory_report.f90)
is the primary source behind the pinned native memory records; a dry estimate
is not a measured SCF peak. Accessed 2026-10-11; no downloads/paid actions.

**Original decision: STOP at acquisition boundary.** No new SCF, native postprocessor, supercell
construction, allocation or job queue is launched. Further progress requires
the missing data packet or independently justified tighter physical restrictions.
