# Decision record: flagship distributional band-edge manuscript analytical core

**Date:** 2026-07-21  
**Issue:** #179  
**Status:** candidate controlling manuscript decision pending PR validation

## Decision

Stop expanding the distributional band-edge program as a sequence of isolated mechanism milestones. Consolidate the merged transition-distribution, spectral-tail, detector-cutoff, carrier-filling, and unified-rank results into one flagship manuscript:

> **From latent bandgap to measured edge in HgCdTe: distributional observation operators and structural identifiability**

The manuscript is distinct from Paper I. Paper I establishes that historical evidence does not identify a universal bandgap-law ranking at the claimed precision. The flagship manuscript provides the constructive forward theory and exact identifiability limits.

## Central publication claim

Under the declared unified single-state spectrum model,

```text
latent zero-density gap
uniform carrier translation
local gap width
absorption amplitude
effective thickness
```

enter the spectrum through only

```text
translated mean gap
gap width
amplitude-thickness product
```

so the five-parameter spectral Jacobian has structural rank at most three.

This is the principal theorem. It is supported by:

1. exact analytical invariances;
2. a machine-precision spectral-equivalence counterexample;
3. numerical SVD verification on a dense spectrum;
4. external-constraint submatrix tests;
5. a marked-spectrum extension that raises rank to four but leaves one combined invariance.

## Supporting theorem hierarchy

1. local composition-to-gap and critical-temperature propagation;
2. Gaussian-gap spectral scale form;
3. exact exponential-tail thickness law;
4. tail-only cutoff rank bound of two;
5. exact Kane-type nonparabolic filling solution and parabolic-error criterion;
6. unified unmarked-spectrum rank bound of three;
7. marked-spectrum combined invariance and rank bound of four.

Stable labels and proof summaries are recorded in:

```text
manuscript/distributional_band_edge/theorem_index.md
```

## Evidence architecture

Every manuscript claim must map to:

- an exact theorem;
- a deterministic numerical verification;
- a source-conditioned reproduction;
- a bounded synthetic sensitivity;
- or an external material validation.

The controlling evidence map is:

```text
manuscript/distributional_band_edge/claim_matrix.md
```

Synthetic cases remain synthetic. A real-specimen property may not be inferred merely because the illustrative parameters are in a source-relevant regime.

## Figure architecture

Approve a seven-figure structure:

1. forward hierarchy and evidence classes;
2. near-critical transition broadening and censoring;
3. Gaussian-gap tail reproduction and fit-window non-uniqueness;
4. thickness-defined cutoff and tail-only rank limit;
5. nonparabolic carrier filling and density-series conditioning;
6. exact spectral equivalence and unified structural rank;
7. measurement design and external-validation boundary.

The human-readable and machine-readable specifications are:

```text
manuscript/distributional_band_edge/figure_plan.md
manuscript/distributional_band_edge/figure_manifest.json
```

Final figure rendering remains a later milestone and must read immutable data rather than copy values from prose.

## External validation decision

Do not delay drafting until a collaborator or new experiment is available.

External collaborators are not a dependency. The approved acquisition routes are:

- public or author-provided full texts and supplements;
- source-native numerical data when available;
- auditable digitization with explicit calibration and uncertainty;
- same-specimen series already published in the literature;
- user-assisted paper retrieval by DOI.

At least one calibrated real-spectrum or same-specimen multi-state validation remains the preferred pre-submission strengthening result.

If no qualifying dataset can be obtained after the documented acquisition program, a later decision may authorize submission as an analytical theorem/methods paper. That reframing must be explicit and may not imply specimen-level validation.

## DOI acquisition decision

Maintain an exact DOI queue tied to blocked claims. Highest-priority sources are:

```text
10.1016/0038-1098(85)90315-1   Dingrong carrier-filled spectrum
10.1007/s11664-007-0162-0       Chang nonparabolic-Urbach and cutoff
10.1063/1.2245220                Chang 2006 short form
10.1016/0022-0248(92)90851-9    Herrmann multimodal broadening
10.1016/j.physb.2009.08.210     Ivanov-Omskii PL and annealing
10.1038/ncomms12576              Teppe near-critical series and supplement
10.1016/0020-0891(91)90110-2    Chu intrinsic absorption spectroscopy
```

The complete acquisition instructions and expected payoff are in `submission_gap.md`.

## Journal positioning

Position the work as semiconductor optical metrology and structural identifiability, not as:

- a new universal HgCdTe bandgap equation;
- a converged first-principles material calculation;
- a universal disorder-width inversion;
- or a production detector-correction formula.

The final venue will be selected after the validation route determines whether the dominant framing is applied physics, semiconductor characterization, or measurement science.

## Authorized conclusions

- The merged analytical components form one coherent publication argument.
- Exact forward-model invariances are the strongest manuscript contribution.
- Better signal-to-noise cannot remove structural null directions.
- Fit-window, thickness, carrier state, and latent-law choice create quantitatively significant but distinct observation effects.
- Independent carrier and optical-scale information are necessary for latent-gap recovery under the base model.
- Drafting and publication packaging can proceed independently of collaborators.

## Unauthorized conclusions

- The current manuscript has not externally validated a complete real-specimen unified model.
- The synthetic Chang and carrier cases are not fits to published specimens.
- Herrmann `s`, `sigma_G`, Urbach energy, composition variance, and PL FWHM are not interchangeable.
- The generic carrier marker is not a physical free-carrier absorption law.
- Local gap-sign probability is not a bulk topological invariant.
- The analytical framework is not a replacement universal gap equation.
- Production AHC, SQS, CPA, or SCBA work is not authorized without a decision-changing validation target.

## Merge gates

The analytical-core PR may merge only when it contains:

- complete manuscript draft;
- theorem index;
- claim/evidence matrix;
- figure plan and machine-readable manifest;
- submission-gap and DOI acquisition record;
- controlling program-state update;
- current README asset inventory;
- clean repository CI.

## Next decision after merge

Proceed in this order:

1. implement the manuscript asset builder and regression checks;
2. execute the DOI acquisition queue and audit any retrieved papers;
3. select one external validation route;
4. integrate the validation result without changing exact theorem claims;
5. complete bibliography, journal formatting, and archival release.