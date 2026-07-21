# Decision record: measurement-kernel-aware spatial disorder

**Date:** 2026-07-21  
**Issue:** #195  
**Decision:** proceed with Stage 1 specification and low-cost analytical implementation; do not proceed to Stage 2  
**Status:** accepted for review in this specification PR

## Context

The merged distributional band-edge program established that several latent parameters collapse into fewer identifiable combinations after scalar observation operators are applied. That result is scientifically frozen and should not be diluted by adding a broad new mechanism branch to the submission-critical manuscript.

One unresolved variable remains material to both the physics and the interpretation of measurements: spatial scale. The present scalar width does not distinguish point disorder from probe-averaged disorder, and it does not encode the correlation length of the underlying composition field. Published HgCdTe work demonstrates spatially resolved absorption, composition, thickness, and band-edge mapping, but the repository does not yet contain a theory connecting one latent covariance field to measurements made with different lateral and depth kernels.

## Options considered

### Option A — stop after the scalar distributional paper

Advantages:

- no new research risk;
- preserves submission focus;
- avoids another potentially generic disorder model.

Disadvantages:

- leaves probe-size dependence unexplained;
- cannot separate disorder amplitude from correlation length;
- cannot state when two modalities should infer different effective widths from one field.

### Option B — proceed directly to correlated random-mass Kane calculations

Advantages:

- potentially high novelty near the inverted/normal transition;
- directly connects spatial disorder to spectral and topological observables.

Disadvantages:

- correlation length is not presently established for a suitable near-critical specimen;
- uncorrelated HgCdTe disorder and disorder-renormalized Kane mass are already established prior art;
- generic correlated random-mass Dirac physics is also established outside HgCdTe;
- a large calculation could become assumption-heavy without changing an experimentally accessible conclusion.

### Option C — first build a measurement-kernel-aware spatial-disorder theory

Advantages:

- closes a specific gap in the current repository;
- begins with exact analytical benchmarks;
- produces a falsifiable multiscale prediction;
- can identify whether correlation length is measurable before microscopic escalation;
- creates an evidence gate for any later correlated Kane calculation.

Disadvantages:

- the generic filtered-variance identity is established mathematics and is not independently publishable as a novelty claim;
- suitable public same-field multiscale data may not exist;
- nonlinear modality operators and unknown point-spread functions can dominate the uncertainty.

## Decision

Select **Option C**.

Proceed with Stage 1 as a separate follow-on program with these constraints:

1. The flagship manuscript, figures, results, and claims remain unchanged.
2. The first executable work is limited to covariance kernels, exact benchmarks, identifiability, and synthetic validation.
3. Absorption and detector-cutoff coupling must preserve nonlinear operation order.
4. No experimental correlation length may be claimed without raw spatial data and a defensible specimen-plane kernel.
5. Stage 2 remains closed until both disorder amplitude and correlation length are independently bounded in a near-critical HgCdTe regime.

## Why this is the highest-value next step

The decisive question is not whether disorder broadens an HgCdTe edge; that is established. The useful unresolved question is whether controlled measurement scale can separate the amplitude and length scale of disorder and thereby predict modality-dependent reported edges.

The exact two-dimensional Gaussian benchmark

```text
V(s) = sigma_x^2/(1 + 2 s^2/xi^2)
```

turns that question into a direct measurement design. It also exposes two practical null regimes:

```text
s << xi  => V(s) ~= sigma_x^2
s >> xi  => V(s) ~= sigma_x^2 xi^2/(2 s^2).
```

Measurements restricted to either regime cannot reliably separate `sigma_x` and `xi`. A useful experiment must span `s/xi = O(1)` or report bounds rather than a fitted correlation length.

## Evidence classification

### Source-established

- HgCdTe composition and thickness have been mapped spatially using infrared microscopy and fitted transmission spectra.
- Detector-scale infrared spectromicroscopy has measured spatial absorption variation with a micrometre-scale beam.
- HgCdTe PL mapping can reveal in-plane variation of band-edge-related transitions.
- Uncorrelated impurity and composition-fluctuation disorder has been treated in an HgCdTe Kane framework using self-consistent Born approximation.
- Correlated random-mass Dirac models exist in other physical settings.

### Project-derived

- the determinant formula for a Gaussian covariance filtered by a Gaussian probe, as adopted under the repository's parameter conventions;
- the exact two-scale inversion under the isotropic two-dimensional Gaussian model;
- the identifiability classification for one, two, and three-or-more probe scales;
- the proposed operation-order hierarchy for coupling the spatial field to existing repository observables;
- the Stage 2 `kappa` gate and termination thresholds.

### Assumptions requiring audit

- stationarity over the analyzed region;
- separability of lateral and depth covariance where used;
- a known specimen-plane point-spread function;
- adequate weak-disorder linearization for scalar effective-width closure;
- negligible or separately modeled carrier, defect, strain, thickness, and processing covariates;
- equivalence between controlled coarse-graining and direct measurements only when kernels are correctly matched.

## Falsification and termination criteria

Terminate or narrow Stage 1 when:

1. available data do not preserve raw spatial information or kernel provenance;
2. inferred scale dependence is smaller than PSF, fitting, detrending, or calibration uncertainty;
3. three or more scales reject all declared covariance families without a physically justified extension;
4. apparent correlation length changes primarily with fitting window, detrending, or processing artifact;
5. the work cannot move beyond the generic variance-filtering identity to an HgCdTe-specific, modality-aware, falsifiable result.

Stage 2 remains terminated unless a formal gate record establishes a credible near-critical regime with `kappa = xi/(2 hbar v_K/sigma_E)` capable of changing an observable above both `5%` and experimental uncertainty, or another explicitly decision-changing condition.

## Consequences

### Positive

- the repository gains a precise next research direction without reopening submission-critical work;
- analytical and numerical work can be tested against exact closed forms before external data are used;
- a future experimental collaboration can be specified in terms of probe scales, PSF, map extent, and uncertainty rather than a vague request for uniformity data;
- Stage 2 becomes evidence-driven rather than computationally opportunistic.

### Negative

- Stage 1 may end as a methods-only result if no suitable map is available;
- a realistic optical forward model will be more complex than replacing one scalar variance;
- covariance-family conclusions will remain model-conditioned.

## Required follow-up sequence

1. merge the specification-only PR;
2. open the covariance-core benchmark issue;
3. implement exact lateral benchmarks and tests;
4. implement depth kernels and finite slabs;
5. perform multiscale identifiability and experiment-design analysis;
6. couple to absorption, then detector cutoff;
7. perform source-bounded validation or record a no-data stop;
8. make a Stage 1 publication decision;
9. make a separate formal Stage 2 proceed/terminate decision.

## Review trigger

Revisit this decision only when one of the following becomes available:

- a same-specimen map at multiple known effective resolutions;
- a high-resolution raw map that can be synthetically coarse-grained with a validated PSF;
- near-critical HgCdTe composition or band-edge covariance with independent calibration;
- evidence that the proposed scale dependence is dominated by a non-composition field requiring the program to be reformulated.