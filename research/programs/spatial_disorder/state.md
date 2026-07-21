# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels to control apparent composition variance, gap width, optical response, and detector cutoff.

## Controlling issue

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core.

## Completed foundations

Merged implementation tranches include:

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design.

Representative modules:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
src/mct_research/spatial_disorder_optics.py
src/mct_research/spatial_disorder_cutoff.py
src/mct_research/spatial_disorder_design.py
```

Established within declared models:

- exact covariance filtering by normalized kernels;
- one-scale non-identifiability of point variance and correlation length;
- exact two-scale inversion and conditioning diagnostics;
- finite-depth analytical benchmarks;
- Jensen-consistent transmission and cutoff operation ordering;
- controlled forward prediction from probe scale to filtered gap width and cutoff.

## Unresolved scientific questions

- whether available HgCdTe data contain enough multi-resolution information to estimate a correlation length;
- how covariance-family misspecification affects recovered parameters;
- how lateral and depth kernels combine in specific instruments and devices;
- whether the predicted scale effect survives thickness, carrier, defect, and calibration nuisance variables;
- whether the full contribution is sufficiently distinct from existing finite-aperture mapping and random-field literature.

## Manuscript status

No manuscript is currently authorized. A candidate paper becomes writeable only after:

1. full-text prior-art audit;
2. realistic uncertainty propagation;
3. covariance-family stress tests using at least three scales;
4. one public-data or experimentally specified validation path;
5. a concise theorem-centered figure and claim plan.

## Authorized next gates

- update the dedicated workflow to include all spatial-disorder layers;
- complete full-text audits for the highest-priority finite-aperture sources;
- quantify experimental-design requirements under noise and kernel uncertainty;
- build representative instrument and detector kernels;
- test whether distinct modalities can be predicted from one latent field.

## Unsupported claims

This program does not currently support:

- a specimen-specific correlation length;
- a universal Gaussian covariance law;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.