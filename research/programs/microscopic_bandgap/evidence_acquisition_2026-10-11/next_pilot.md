# One staged low-cost next calculation: an archival interior ordering bracket

**Status: proposal only; not run, queued or contacted.** The output would be a
specimen-specific magneto-optical ordering interval at measured low temperature,
not an exact projected alloy mass, physical 0 K xc, disorder coefficient or
topological invariant. This proposal deliberately addresses the next observable
that inexpensive existing data could discriminate. It cannot close all four
certification gates in [the memo](decision_memo.md).

## Observable and specimen points

Reanalyse **already acquired** polarization-resolved interband and intraband
magnetotransmission on existing bulk-like specimens with nominal Cd fractions
`xL=0.150`, `xR=0.185`; use `xM=0.1675` only if the first two pass. The middle
point is the arithmetic midpoint, not a zero obtained from a gap-law fit. These
targets select a region where published ordering evidence exists; they do not
predict these specimens' gaps. Accept archived specimens within ±0.002 of each
target and report their actual independent assays; otherwise fail intake.

Primary observables are photon energies, fields, polarization-dependent branch
assignments, zero-field convergence and line shapes. Infer each signed interaction
gap `EΓ6−EΓ8` separately with the source-supported Landau-level observation
operator. No composition polynomial, bowing term, susceptibility, disorder
strength, HSE parameter or x-dependent model coefficient is fitted to alloy gaps.
Inversion must be identified by sign-sensitive transition selection/ordering;
an energy equation containing only the squared gap cannot establish a sign.

Use measured temperature near 2 K, with existing 4.2 K repetitions if available.
Repeated low-temperature agreement is a stability check, not a rigorous T→0
bound. Preserve the finite-temperature label unless an independently justified
zero-temperature correction envelope is provided later.

## Stages and stopping rules

| Stage | Work | Accept to next stage | Reject/stop |
|---|---|---|---|
| 0: archival intake, no fit | Locate raw spectra, field/photon calibration, dark/reference scans, instrument response, specimen identity, colocated independent Cd assay, carrier/strain records | Two endpoint specimens from one declared growth/state family; actual x intervals known, half-width ≤0.002 including spatial variation and calibration; raw uncertainty data support ≤1 meV energy resolution; sign-sensitive transitions visible | Missing raw data or independent assay; composition inferred from optical cut-on; strong unknown grading/strain; only fitted figures available. Stop without new growth or a replacement computation. |
| 1: two-specimen reconstruction | Bound each signed gap using field/energy calibration intervals, carrier filling, branch assignments and alternative simplified-Kane/eight-band descriptions; preserve linewidths and correlated errors | A conservative total gap interval with half-width ≤5 meV for each specimen, and robust opposite signs; held-out transition families agree within the same envelope | Sign ambiguity, nuisance degeneracy, unbounded model discrepancy, interval including zero at either endpoint, or resource cap. Report unresolved bracket; do not widen the experiment. |
| 2: conditional midpoint only | Apply the identical observation operator to the one archived midpoint specimen; no additional composition points | Robust midpoint sign and continuity assumption explicitly justified for the same state family allow a narrower **operational** bracket | Midpoint interval straddles zero: retain the two-point bracket. Missing third specimen: stop at two. Do not extrapolate to a unique root. |
| Final qualification | Preserve raw provenance, individual x/gap intervals and residuals | Admit the finite-temperature experimental sign information as partial B evidence | Reject promotion to T16 unless D, S and uniform physical U are independently supplied. Three sampled secants never certify all-pairs m>0. |

Use interval envelopes rather than silently treating all error sources as Gaussian.
Where calibration/systematic bounds cannot be justified, mark them unknown and
fail the total-interval gate. A model discrepancy cannot be set to zero because
two fits agree. Hold out at least one transition family from inference and use
it to test the observation operator; fit all points only after it passes.
No measured optical linewidth is identified with a single-particle alloy Γ
linewidth without an independently established mapping.

## Predicted discriminating power, conditional on fidelity

These are design calculations, **not material predictions**:

- With a justified ±5 meV total gap envelope, a signed gap whose magnitude
  exceeds 5 meV is sign-resolved. Two hypotheses separated by more than 10 meV
  at a specimen are distinguishable through disjoint such envelopes, provided
  the hypotheses concern the same measured state and operator.
- With `xL=0.150±0.002` and `xR=0.185±0.002`, robust opposite ordering signs
  and independently justified continuity give an operational existence bracket
  `[0.148,0.187]`, width 0.039. A robust midpoint sign permits one of
  `[0.148,0.1695]` or `[0.1655,0.187]`, each width 0.0215. Actual assays replace
  these nominal intervals. This brackets at least one reversal; uniqueness is
  not inferred. It is not the R07 target precision Δx=0.003.
- For feasibility context only, the historical Part II observations at
  approximately 0.150 and 0.185 have different ordering signs. They do not
  establish achievable uncertainties on new specimens or an expected numeric
  gap in this pilot. See [P12](source_evidence_matrix.md).
- The pilot can reject a sharp, sign-resolved observation operator if unresolved
  widths/branch multiplicity dominate its 5 meV budget. A successful sign bracket
  still cannot certify absence of spectral support, an all-pairs composition
  modulus, or a frozen-ion/physical-zero-temperature equivalence.

## Fidelity and bounded resources

This is an existing-data calculation; **no instrument time, new specimens or
new electronic-structure job is assumed**. If independent metrology and raw
spectra are absent, the cheap proposal fails at stage 0. A measurement campaign
would require a separate scope and cost justification; none is created here.

Cap the admitted digital data at 100 MiB, 31 field values per specimen and
10,000 photon-energy bins per field. Stream spectra; use small Landau blocks
no larger than 64×64 and at most 200 forward-model evaluations per specimen per
description, for two descriptions and at most three specimens (≤1,200 total).
There are no supercell Hamiltonians or FFT grids. One streamed double array of
31×10,000 bins is 2.48 MB; the maximum complex block is 64 KiB. Allowing data,
working copies, fit intervals and interpreter overhead, impose **512 MiB RSS,
one CPU core, 1,800 s CPU and 1,800 s wall time per stage-1/2 attempt**, with
stage 0 capped at 300 s. Overall attempt ceiling: **3,900 s wall and CPU,
1.0834 core-hours; 512 MiB RSS**. These are enforceable upper bounds on a future
attempt, not a prediction of convergence. If a faithful observation operator
needs larger blocks/evaluation counts, reject this cheap scope rather than
truncate physics to make the fit pass. The present investigation installs no
runner, monitor or supervisor for these limits.

The accepted product would be raw-source hashes, independent composition
intervals, sign-sensitive gap intervals, held-out residuals and a scoped
operational bracket. It would contain no inferred material coefficient or
advertised physical xc uncertainty. Stop after this single discriminating
question, irrespective of success.
