# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels to control apparent composition variance, gap width, optical response, and detector cutoff.

## Controlling issues

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core;
- #215 — probe-scale calibration limits in multiscale disorder inference.

## Completed foundations

Merged or current implementation tranches include:

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design;
- PR #216 — probe-scale calibration theorem and nuisance marginalization.

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
- exact confounding of common multiplicative probe calibration with correlation length;
- analytical marginalization of arbitrary Gaussian log-probe calibration modes.

## Probe-scale calibration result

For the Gaussian benchmark

$$
V(s)=\frac{A}{1+2s^2/\xi^2},
$$

$$
\frac{\partial V}{\partial\log s}
=-\frac{\partial V}{\partial\log\xi}.
$$

A common multiplicative probe-scale error is therefore indistinguishable from the opposite change in correlation length. If the common log-scale calibration prior has variance $\tau_s^2$, the local covariance of $(\log A,\log\xi)$ gains exactly

$$
\begin{pmatrix}
0&0\\
0&\tau_s^2
\end{pmatrix}.
$$

This establishes an absolute correlation-length precision floor within the model. Independent or shape-changing probe errors are not pure common modes and can degrade both recovered parameters.

## Unresolved scientific questions

- whether available HgCdTe data contain enough multi-resolution information to estimate a correlation length;
- how covariance-family misspecification affects recovered parameters;
- how lateral and depth kernels combine in specific instruments and devices;
- how uncertainty in kernel shape differs from uncertainty in one effective Gaussian width;
- whether local Fisher conclusions remain accurate under nonlinear posterior propagation;
- whether the predicted scale effect survives thickness, carrier, defect, and calibration nuisance variables jointly;
- whether the full contribution is sufficiently distinct from existing finite-aperture mapping and random-field literature.

## Manuscript status

No manuscript is currently authorized. A candidate paper becomes writeable only after:

1. full-text prior-art audit;
2. realistic uncertainty propagation beyond the completed local observation/probe-scale layer;
3. covariance-family stress tests using at least three scales;
4. one public-data or experimentally specified validation path;
5. a concise theorem-centered figure and claim plan.

## Authorized next gates

- complete full-text audits for the highest-priority finite-aperture sources;
- quantify covariance-family misspecification under at least three scales;
- build representative instrument and detector kernels with declared scale and shape uncertainty;
- compare local Fisher predictions against nonlinear synthetic posterior recovery;
- test whether distinct modalities can be predicted from one latent field;
- identify one public-data or experimentally specified validation path.

## Unsupported claims

This program does not currently support:

- a specimen-specific correlation length;
- a universal Gaussian covariance law;
- replacing a measured point-spread function with nominal pixel pitch;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- treating a local Fisher covariance as a global nonlinear posterior;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.
