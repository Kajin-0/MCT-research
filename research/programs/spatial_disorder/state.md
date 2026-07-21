# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels to control apparent composition variance, gap width, optical response, and detector cutoff.

## Controlling issues

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core;
- #215 — probe-scale calibration limits in multiscale disorder inference;
- #218 — three-scale covariance-family falsification.

## Completed foundations

Merged or current implementation tranches include:

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design;
- PR #216 — probe-scale calibration theorem and nuisance marginalization;
- PR #219 — reciprocal-linearity family test and half-integer Matérn alternatives.

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
src/mct_research/spatial_disorder_covariance_families.py
```

Established within declared models:

- exact covariance filtering by normalized kernels;
- one-scale non-identifiability of point variance and correlation length;
- exact two-scale inversion and conditioning diagnostics;
- finite-depth analytical benchmarks;
- Jensen-consistent transmission and cutoff operation ordering;
- controlled forward prediction from probe scale to filtered gap width and cutoff;
- exact confounding of common multiplicative probe calibration with correlation length;
- analytical marginalization of arbitrary Gaussian log-probe calibration modes;
- exact reciprocal-linearity condition for the Gaussian covariance/probe family;
- stable Gaussian-probe filtering for Matérn `nu=1/2, 3/2, 5/2` alternatives.

## Probe-scale calibration result

For the Gaussian benchmark

$$
V(s)=\frac{A}{1+2s^2/\xi^2},
$$

$$
\frac{\partial V}{\partial\log s}
=-\frac{\partial V}{\partial\log\xi}.
$$

A common multiplicative probe-scale error is indistinguishable from the opposite change in correlation length. If the common log-scale calibration prior has variance $\tau_s^2$, the local covariance of $(\log A,\log\xi)$ gains exactly

$$
\begin{pmatrix}
0&0\\
0&\tau_s^2
\end{pmatrix}.
$$

This establishes an absolute correlation-length precision floor within the model. Independent or shape-changing probe errors can degrade both recovered parameters.

## Covariance-family result

The same Gaussian benchmark obeys

$$
\boxed{
\frac{1}{V(s)}
=\frac{1}{A}+\frac{2}{A\xi^2}s^2.
}
$$

Thus two admissible scales recover two Gaussian parameters but cannot test the covariance family. A third scale must lie on the same reciprocal line. For ordered scales, the exact Gaussian invariant is

$$
\boxed{
\frac{V_3^{-1}-V_2^{-1}}{s_3^2-s_2^2}
-
\frac{V_2^{-1}-V_1^{-1}}{s_2^2-s_1^2}
=0.
}
$$

For the dimensionless design

```text
s/ell = [0.1, 1, 2]
relative variance uncertainty = 3%
```

forcing the Gaussian family through the endpoint scales gives:

```text
true family       middle prediction error      standardized residual
Matern nu=1/2          17.482%                         4.120
Matern nu=3/2           8.086%                         2.012
Matern nu=5/2           5.207%                         1.319
```

The rough family is distinguishable at this uncertainty; the smoothest family is not. Failure to reject Gaussian covariance does not establish Gaussian covariance.

For six scales

```text
s/ell = [0.05, 0.1, 0.3, 1, 2, 5],
```

the corresponding reduced chi-square values of the best weighted Gaussian reciprocal fit are `18.795`, `3.519`, and `1.363` for `nu=1/2`, `3/2`, and `5/2`.

Very large probes are weak family discriminators because the supported standard Matérn families share the same leading inverse-area attenuation.

## Unresolved scientific questions

- whether available HgCdTe data contain enough multi-resolution information to estimate a correlation length;
- whether experimentally achievable uncertainty resolves Gaussian versus smooth Matérn covariance;
- how lateral and depth kernels combine in specific instruments and devices;
- how uncertainty in kernel shape differs from uncertainty in one effective Gaussian width;
- whether local Fisher conclusions remain accurate under nonlinear posterior propagation;
- whether the predicted scale effect survives thickness, carrier, defect, calibration, and covariance-family nuisance variables jointly;
- whether the full contribution is sufficiently distinct from existing finite-aperture mapping and random-field literature.

## Manuscript status

No manuscript is currently authorized. A candidate paper becomes writeable only after:

1. full-text prior-art audit;
2. realistic uncertainty propagation beyond the completed local observation/probe-scale layer;
3. one public-data or experimentally specified validation path;
4. a representative instrument kernel and calibrated scale range;
5. a concise theorem-centered figure and claim plan.

The three-scale covariance-family stress-test gate is completed for the declared Gaussian and half-integer Matérn families. It does not establish which family a specimen follows.

## Authorized next gates

- complete full-text audits for the highest-priority finite-aperture sources;
- build representative instrument and detector kernels with declared scale and shape uncertainty;
- compare local Fisher predictions against nonlinear synthetic posterior recovery;
- combine calibration and covariance-family uncertainty in one design calculation;
- test whether distinct modalities can be predicted from one latent field;
- identify one public-data or experimentally specified validation path.

## Unsupported claims

This program does not currently support:

- a specimen-specific correlation length;
- a universal Gaussian or Matérn covariance law;
- replacing a measured point-spread function with nominal pixel pitch;
- interpreting a low reciprocal-linearity residual as proof of Gaussian covariance;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- treating a local Fisher covariance as a global nonlinear posterior;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

The covariance-family module is additive shared infrastructure. It reuses the existing Gaussian multiscale prediction and exact two-scale recovery definitions without changing their numerical behavior.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.
