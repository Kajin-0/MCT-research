# Program state: measurement-kernel-aware spatial disorder

**Portfolio contribution:** R04  
**State:** active-result and candidate work; manuscript gate not yet passed

## Objective

Determine how a spatially correlated HgCdTe composition field combines with finite lateral and depth measurement kernels, instrument calibration, covariance-family uncertainty, observation operators, and finite-map sampling to control apparent composition variance, gap width, optical response, detector cutoff, and recoverable information.

## Controlling issues

- #196 — scale-dependent spatial-disorder theorem and replacement scientific core;
- #215 — probe-scale calibration limits in multiscale disorder inference;
- #218 — three-scale covariance-family falsification;
- #220 — exact nonlinear common-scale posterior propagation;
- #224 — Gaussian-surrogate bias and pairwise drift under covariance misspecification;
- #228 — composite optical, pixel, and finite-depth instrument kernel;
- #230 — optimal multiscale repeat allocation;
- #232 — joint instrument, covariance-family, fitting, and observation-operator identifiability;
- #234 — correlated-map effective sample size and variance-estimator bias.

## Completed implementation tranches

- PR #199 — Gaussian covariance and Gaussian-kernel core;
- PR #202 — finite-depth kernels and slab limits;
- PR #204 — multiscale Fisher and recoverability diagnostics;
- PR #207 — lateral transmission operation-order benchmark;
- PR #210 — detector-cutoff operation-order benchmark;
- PR #212 — end-to-end multiscale disorder-to-cutoff design;
- PR #216 — probe-scale calibration theorem and nuisance marginalization;
- PR #219 — reciprocal-linearity family test and half-integer Matérn alternatives;
- PR #221 — exact nonlinear posterior factorization and bounded-prior failure;
- PR #227 — pairwise Gaussian-parameter drift and global-surrogate bias;
- PR #229 — composite optical-PSF, pixel, and absorption-depth kernel;
- PR #231 — optimal repeat allocation and three-scale precision/falsification compromise;
- PR #233 — joint identifiability envelope across instrument, family, fit, and observation operators;
- PR #236 — exact filtered-map cross covariance, effective sample size, and correlated sample-variance moments.

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
src/mct_research/spatial_disorder_covariance_bias.py
src/mct_research/spatial_disorder_instrument.py
src/mct_research/spatial_disorder_allocation.py
src/mct_research/spatial_disorder_joint_identifiability.py
src/mct_research/spatial_disorder_map_sampling.py
src/mct_research/spatial_disorder_posterior.py
```

## Established results within declared models

### Gaussian filtering and scale calibration

For the isotropic two-dimensional Gaussian benchmark,

$$
V(s)=\frac{A}{1+2s^2/\xi^2}.
$$

One scale cannot identify both $A$ and $\xi$. Two admissible scales recover them exactly within the model, while three or more scales can test the covariance family.

The probe-scale and correlation-length sensitivities satisfy

$$
\frac{\partial V}{\partial\log s}
=-\frac{\partial V}{\partial\log\xi}.
$$

A common multiplicative scale-calibration error is exactly confounded with absolute correlation length. With independent common log-scale calibration variance $\tau_s^2$,

$$
\operatorname{Var}(\log\xi_{\rm absolute})
=
\operatorname{Var}(\log\xi_{\rm relative})+\tau_s^2.
$$

The nonlinear posterior factorization extends this variance floor beyond the local Fisher approximation when the absolute log-length prior is translation invariant and does not couple relative length to calibration.

### Covariance-family falsification and misspecification

Gaussian covariance requires reciprocal linearity:

$$
\frac{1}{V(s)}
=
\frac{1}{A}+\frac{2}{A\xi^2}s^2.
$$

Two scales estimate Gaussian parameters but cannot test the family. A third scale supplies the first exact closure test.

For the declared broad five-scale misspecification design, Matérn $\nu=1/2$ truth forced through a Gaussian inverse gives:

```text
pairwise point-variance spread       2.820x
pairwise correlation-length spread  3.418x
best Gaussian A_fit/A_true           0.8351
best Gaussian xi_fit/ell             1.0406
```

The inferred Gaussian parameters are scale-selection- and fitting-convention-dependent when the covariance family is wrong.

### Composite instrument kernel

The declared representative instrument is

```text
elliptical Gaussian optical PSF
convolved with rectangular pixel or scan-bin integration
multiplied by finite-slab exponential depth weighting.
```

For axis-aligned separable Gaussian covariance,

$$
\frac{\operatorname{Var}(X_w)}{A}=F_xF_yF_z.
$$

In the controlled reference case, the complete kernel transmits `0.162585` of point variance. Replacing the lateral kernel by a moment-matched Gaussian changes the result by `1.116%`, while the declared instrument calibration budget produces `5.35%` relative uncertainty.

Across the declared 42-case stress grid, 18 cases exceed 1% moment-matched-Gaussian error and the maximum reaches `9.045%`. Kernel shape must remain explicit in pixel-dominated regimes.

### Optimal repeat allocation

For homoscedastic single-repeat log-variance uncertainty, the local Gaussian Fisher determinant is proportional to the weighted variance of the scale sensitivities. Over a bounded feasible scale interval, the continuous D-optimal design places equal weight at the two endpoint scales; the exact integer allocation is

```text
floor(N/2), ceil(N/2).
```

This endpoint design estimates Gaussian parameters efficiently but cannot test the covariance family. The three-scale optimizer therefore reserves an interior scale while enforcing a declared D-efficiency floor.

For scales $s/\xi=[0.1,1,2]$, 3% single-repeat relative uncertainty, and minimum D-efficiency 0.8:

```text
total repeats   allocation       D-efficiency   worst Matérn z
12              [5, 3, 4]        0.8082         2.4024
30              [11, 7, 12]      0.8007         3.7816
60              [24, 15, 21]     0.8045         5.4040
```

Repeat allocation cannot remove the absolute scale-calibration floor.

### Joint identifiability envelope

PR #233 combines, in observable space,

$$
C_{\rm total}
=
C_{\rm observation}
+D C_{\rm instrument}D^T
+b_{\rm kernel}b_{\rm kernel}^T
+b_{\rm operator}b_{\rm operator}^T.
$$

For each supported covariance family and Gaussian fitting convention, it reports

$$
\Delta^2=r^T C_{\rm total}^{+}r.
$$

The declared design uses three equivalent lateral probe scales

```text
s = [0.23094, 1.15470, 4.61880]
relative observation uncertainty = 3% at each scale
threshold distance = 3
```

with shared PSF, pixel, absorption, and thickness calibration uncertainty.

Full-envelope distances across direct variance, transmission-effective absorption, and fixed-response cutoff are:

```text
true family       full-distance range       classification
Matérn nu=1/2       6.187 to 6.571          resolved
Matérn nu=3/2       3.030 to 3.113          resolved, marginal
Matérn nu=5/2       1.954 to 1.987          observation limited
```

The classification is unchanged between weighted log-variance and weighted reciprocal-variance fitting at the declared threshold, although the fitted Gaussian parameters differ by convention.

For this controlled design:

- instrument calibration modestly reduces separation;
- exact-versus-moment-matched kernel shape modestly reduces separation;
- transmission and cutoff operation-order uncertainty modestly reduce separation;
- the smooth Matérn $\nu=5/2$ alternative is already below threshold with observation noise alone.

This is a design-level conclusion, not a specimen covariance-family result. The Matérn calculation uses supported lateral covariance families with a common Gaussian finite-depth factor; it is not an exact rectangular-pixel three-dimensional Matérn theorem.

### Correlated finite-map sampling

For Gaussian material covariance matrix $\Lambda$, Gaussian kernel covariance matrices $\Sigma_i$ and $\Sigma_j$, and measurement-center displacement $\Delta\mathbf r$,

$$
\operatorname{Cov}(X_i,X_j)
=
A\sqrt{\frac{\det\Lambda}{\det(\Lambda+\Sigma_i+\Sigma_j)}}
\exp\left[-\frac12\Delta\mathbf r^T
(\Lambda+\Sigma_i+\Sigma_j)^{-1}\Delta\mathbf r\right].
$$

The equal-kernel zero-separation limit recovers the established filtered-variance theorem.

For a Gaussian map vector $\mathbf y\sim\mathcal N(0,C)$ and centering matrix $P=I-\mathbf1\mathbf1^T/n$,

$$
\operatorname{Var}(\bar y)=\frac{\mathbf1^TC\mathbf1}{n^2},
$$

$$
\mathbb E[s_{\rm naive}^2]=\frac{\operatorname{tr}(PC)}{n-1},
$$

and

$$
\operatorname{Var}(s_{\rm naive}^2)
=\frac{2\operatorname{tr}[(PC)^2]}{(n-1)^2}.
$$

The controlled `10 x 10` map with point composition standard deviation `0.005`, $\ell=2\,\mu\mathrm m$, Gaussian probe standard deviation `1 µm`, and `0.5 µm` pixel spacing gives:

```text
nominal pixels                         100
map-mean effective sample count       1.7377
E[naive map variance]/marginal        0.4288
variance effective degrees freedom    3.4783
```

Thus the ordinary map variance underestimates the marginal filtered variance by approximately 57% in this dense controlled case.

At approximately fixed field of view, increasing from `10 x 10` pixels at `0.5 µm` spacing to `20 x 20` pixels at `0.25 µm` spacing raises nominal pixel count by `4x` but increases map-mean effective information by only `0.290%`.

The repeat counts in the allocation theorem represent independent realizations or covariance-weighted information. Nominal raster pixels must not be substituted as independent repeats.

The effective variance degrees of freedom are moment matched. They are not an exact chi-square law for an arbitrary correlated covariance spectrum.

## Current scientific interpretation

The analytical and synthetic infrastructure now specifies what a credible experiment must report:

1. at least three independently characterized effective scales;
2. measured or specified PSF and pixel integration rather than nominal pitch alone;
3. thickness and absorption-depth calibration;
4. a covariance-family closure test before reporting Gaussian parameters;
5. fitting-convention sensitivity under misspecification;
6. observation-operator ordering for transmission or cutoff;
7. shared calibration covariance across scales;
8. sample-center geometry and the full within-map covariance, or independently justified sampling separation;
9. independent-map or covariance-weighted information counts rather than nominal pixel counts;
10. a predeclared separation or termination threshold.

The main bottleneck is no longer missing analytical machinery. It is external specification and validation.

## Manuscript status

No manuscript is currently authorized.

Completed controlled gates:

- Gaussian filtering and multiscale identifiability;
- local and nonlinear common-scale calibration limits;
- covariance-family falsification and misspecification bias;
- representative composite instrument kernel;
- optimal repeat allocation;
- joint calibration/family/fit/operator uncertainty envelope;
- exact Gaussian finite-map covariance and correlated-sampling diagnostics.

Remaining authorization gates:

1. complete the finite-aperture full-text prior-art audit;
2. obtain or declare one experimentally specified PSF, pixel geometry, thickness, absorption coefficient, calibrated scale range, raster geometry, and sampling covariance;
3. identify one public-data or experimentally specified multiresolution validation path;
4. test the combined model against that path;
5. prepare a concise theorem-centered figure and claim plan.

## Authorized next gates

- complete PR #223 or explicitly record the unavailable-source boundary;
- define an experimental specification record for one real or planned instrument and map geometry;
- ingest or construct a provenance-controlled multiresolution dataset;
- run the joint envelope with measured instrument covariance, observation uncertainty, and map covariance;
- test whether multiple modalities from one specimen can be predicted from one latent spatial field;
- reassess manuscript authorization only after those results.

## Unsupported claims

This program does not currently support:

- a specimen-specific point variance or correlation length;
- a universal Gaussian or Matérn covariance law;
- a universal Gaussian optical PSF or rectangular-pixel model;
- replacing a measured point-spread function with nominal pixel pitch;
- treating nominal raster pixel count as independent repeat count;
- treating moment-matched effective degrees of freedom as an exact chi-square distribution;
- interpreting failure to reject Gaussian covariance as proof of Gaussian covariance;
- interpreting pairwise parameter spread as a confidence interval;
- reporting a misspecified Gaussian parameter without declaring the fitting loss and scale design;
- treating a moment-matched Gaussian as exact outside a verified regime;
- treating the joint Mahalanobis distance as a posterior probability or discovery significance;
- applying the exact common-scale posterior convolution when an active bounded absolute-length prior couples relative length and calibration;
- identifying optical tail energy with microscopic composition variance;
- treating controlled cutoff shifts as measured detector behavior;
- a topological or random-mass Kane conclusion;
- manuscript submission readiness.

## Shared dependencies

This program uses empirical gap slopes, distributional absorption and cutoff operators, literature records, and validation infrastructure shared with other works.

The covariance-family, bias, instrument, allocation, joint-identifiability, map-sampling, and posterior modules are additive shared infrastructure. They reuse established Gaussian prediction, recovery, depth filtering, family filtering, optical operators, and calibration definitions.

## Stage-2 boundary

Correlated random-mass Kane physics is a separate program. It is not automatically activated by progress in this workstream.
