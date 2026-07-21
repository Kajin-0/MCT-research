# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels to control apparent composition variance, gap width, optical response, and detector cutoff.

## Controlling issues

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core;
- #215 — probe-scale calibration limits in multiscale inference.

## Completed foundations

Merged implementation tranches include:

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design;
- PR #217 — probe-scale calibration nuisance information and exact common-mode confounding.

Representative modules:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
src/mct_research/spatial_disorder_optics.py
src/mct_research/spatial_disorder_cutoff.py
src/mct_research/spatial_disorder_design.py
src/mct_research/spatial_disorder_calibration.py
```

Established within declared models:

- exact covariance filtering by normalized kernels;
- one-scale non-identifiability of point variance and correlation length;
- exact two-scale inversion and conditioning diagnostics;
- finite-depth analytical benchmarks;
- Jensen-consistent transmission and cutoff operation ordering;
- controlled forward prediction from probe scale to filtered gap width and cutoff;
- exact confounding between a common multiplicative probe-scale calibration and absolute correlation length;
- Schur-complement uncertainty diagnostics for common, independent, and correlated probe-log calibration modes.

## Probe-scale calibration result

For the isotropic two-dimensional Gaussian benchmark

```text
V(s)=A/(1+2s^2/xi^2),
```

the derivative identity

```text
dV/dlog(s_i) = -dV/dlog(xi)
```

is exact. Therefore an uncalibrated common multiplicative scale leaves `log xi` unidentified even when the relative multiscale design is otherwise informative.

With a Gaussian common log-scale calibration prior of variance `tau_s^2`, the local physical covariance satisfies

```text
Cov(log A, log xi)_calibrated
=
Cov(log A, log xi)_exact_scale
+ [[0, 0], [0, tau_s^2]].
```

Thus common absolute-scale uncertainty does not inflate `log A`, but adds exactly its prior variance to `log xi`. Independent or correlated per-scale errors can inflate both physical coordinates.

This is a local linear-Gaussian information result under the declared covariance and probe model. It is not an instrument calibration or specimen correlation-length estimate.

## Unresolved scientific questions

- whether available HgCdTe data contain enough multi-resolution information to estimate a correlation length;
- how covariance-family misspecification affects recovered parameters;
- how lateral and depth kernels combine in specific instruments and devices;
- whether the predicted scale effect survives thickness, carrier, defect, non-Gaussian, and operation-coupled nuisance variables;
- whether real instruments provide external absolute-scale calibration precise enough for useful `xi` recovery;
- whether the full contribution is sufficiently distinct from existing finite-aperture mapping and random-field literature.

## Manuscript status

No manuscript is currently authorized. A candidate paper becomes writeable only after:

1. full-text prior-art audit;
2. realistic uncertainty propagation beyond the completed local probe-calibration layer;
3. covariance-family stress tests using at least three scales;
4. one public-data or experimentally specified validation path;
5. a concise theorem-centered figure and claim plan.

## Authorized next gates

- complete full-text audits for the highest-priority finite-aperture sources;
- quantify covariance-family misspecification with three or more scales;
- build representative instrument and detector kernels with externally specified calibration uncertainties;
- test whether distinct modalities can be predicted from one latent field;
- verify the local calibration result against nonlinear simulation when calibration errors are not asymptotically small.

## Unsupported claims

This program does not currently support:

- a specimen-specific correlation length;
- a universal Gaussian covariance law;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- claiming that multiscale data determine an absolute correlation length without external probe-scale calibration;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

The calibration module is additive shared infrastructure. It reuses the existing multiscale prediction and Fisher definitions without changing their numerical behavior.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.
