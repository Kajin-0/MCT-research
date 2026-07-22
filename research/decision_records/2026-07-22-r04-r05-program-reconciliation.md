# Research decision memo: R04 external validation and the R05 activation gate

**Date:** 2026-07-22  
**Issue:** #279  
**Primary program:** R04 — measurement-kernel-aware spatial disorder  
**Affected program:** R05 — correlated random-mass Kane regime  
**Decision class:** repository and literature audit; no new scientific calculation  
**Manuscript impact:** no manuscript authorization

## Executive decision

Do **not** begin the broad Stage 1 implementation sequence described in the new two-stage brief. Current `main` already contains most of that sequence as the R04 theorem and inference hierarchy.

Do **not** activate R05. The repository does not yet possess an independently supported HgCdTe composition-correlation-length range near the normal--inverted transition, and no observable has been shown to require finite-correlation-length random-mass Kane physics rather than the existing scalar distributional and finite-kernel models.

The next decision-changing milestone is external validation of R04 using one qualifying numerical multiresolution data package. R04 is analytically mature but remains `external_data_blocked`:

```text
partial multiresolution candidates = 1
direct validation candidates       = 0
```

The immediate research question is therefore not whether the kernel-aware theory can be implemented. It is whether a real HgCdTe specimen, measured with characterized kernels at sufficient scales, exhibits a scale dependence that identifies or falsifies a covariance model after instrument, finite-map, and cross-scale covariance are included.

The new brief also assumes that a distributional flagship manuscript is near submission. That assumption is incompatible with current repository governance. The earlier PR #194 manuscript bundle is retired, no active R03 or R04 manuscript is authorized, and there is no repository-wide flagship submission path to preserve.

## What is already solved

### 1. Stationary Gaussian field and arbitrary Gaussian kernel

R04 implements the stationary anisotropic Gaussian covariance

```text
C(h) = A exp[-0.5 h^T Lambda^-1 h]
```

and a normalized Gaussian measurement kernel with covariance `Sigma_w`. The exact filtered variance is

```text
V_w = A sqrt[det(Lambda) / det(Lambda + 2 Sigma_w)].
```

For the isotropic `D`-dimensional benchmark,

```text
V(s) = A [1 + 2 s^2/xi^2]^(-D/2).
```

This is the requested arbitrary-kernel effective-variance result for the Gaussian/Gaussian benchmark, including anisotropy and stable log-determinant evaluation.

### 2. Scalar limit, one-scale no-go theorem, and exact multiscale inversion

The point-probe limit recovers the scalar realization variance. One scale identifies only

```text
A [1 + 2 s^2/xi^2]^(-D/2)
```

and cannot separately identify point variance and correlation length.

Two distinct scales recover `A` and `xi` exactly within the declared Gaussian model. The implementation also quantifies loss of conditioning when scales are nearly equal or occupy the same asymptotic regime. Algebraic invertibility is kept distinct from practical recoverability.

### 3. Covariance-family falsification and misspecification

R04 supports Gaussian covariance and half-integer Matérn alternatives:

```text
nu = 1/2, 3/2, 5/2.
```

For the isotropic two-dimensional Gaussian family,

```text
1/V(s) = 1/A + 2 s^2/(A xi^2).
```

Two scales fit this line exactly and therefore cannot test the family. A third scale supplies the first exact reciprocal-linearity closure test.

In the committed broad five-scale synthetic design, forcing Matérn `nu=1/2` truth through a Gaussian inverse produces:

```text
pairwise point-variance spread       2.820x
pairwise correlation-length spread  3.418x
best Gaussian A_fit/A_true           0.8351
best Gaussian xi_fit/ell             1.0406
```

Thus a fitted Gaussian correlation length is scale-design- and loss-function-dependent when the covariance family is wrong.

### 4. Finite thickness and penetration-depth weighting

R04 implements normalized finite-slab Beer--Lambert depth kernels, front/back reflection, exact semi-infinite Gaussian and exponential limits, an exact finite-slab exponential-covariance result, and deterministic Gauss--Legendre reference quadrature.

For a stationary homogeneous slab, front/back reflection leaves the filtered variance unchanged. Front/back observable differences require a depth-dependent mean, covariance, optical law, or collection model; they cannot be manufactured from a stationary homogeneous field.

### 5. Composite instrument kernels

The implemented representative instrument combines:

```text
elliptical Gaussian optical PSF
convolved with rectangular pixel or scan-bin integration
multiplied by finite-slab exponential depth weighting.
```

For axis-aligned separable Gaussian covariance, the measured-to-point variance ratio factorizes as

```text
V_measured/A = F_x F_y F_z.
```

In the controlled reference case, the complete kernel transmits `0.162585` of point variance. Replacing the lateral kernel by a moment-matched Gaussian changes the result by `1.116%`, while the declared instrument-calibration budget contributes `5.35%` relative uncertainty. Across the declared 42-case stress grid, 18 cases exceed 1% equivalent-Gaussian error and the maximum reaches `9.045%`.

### 6. Gap propagation and observation operators

The repository already contains:

- second-order propagation of filtered composition variance through declared signed-gap laws;
- exact bounded Gaussian quadrature and local sign probability;
- Gaussian local-gap convolution into controlled absorption models;
- transmission averaging with the correct operation order;
- fixed-response detector-cutoff operators;
- source-bounded unified-spectrum and detector models.

For lateral heterogeneous columns,

```text
alpha_T(E) = -log E[exp(-d alpha(E|G))]/d
```

is kept distinct from

```text
E[alpha(E|G)].
```

Jensen's inequality gives `alpha_T <= E[alpha]`. The corresponding fixed-response detector cutoff from transmission averaging occurs at equal or higher photon energy than the mean-absorption closure. This directly implements the noncommutation required by the new brief.

### 7. Calibration, uncertainty, and recoverability

A common multiplicative probe-scale calibration error is exactly confounded with absolute correlation length. Under the declared independent broad-prior conditions,

```text
Var(log xi_absolute)
=
Var(log xi_relative) + tau_scale^2.
```

The result has both a local Fisher derivation and an exact nonlinear posterior factorization. Finite prior boundaries are explicitly tested as a failure mode.

The joint R04 envelope combines observation covariance, instrument-calibration covariance, kernel-reduction bias, and operation-order uncertainty. For the controlled three-scale design with 3% observation uncertainty, the committed full-envelope family distances are:

```text
true family       full-distance range       decision
Matérn nu=1/2       6.187 to 6.571          resolved
Matérn nu=3/2       3.030 to 3.113          resolved, marginal
Matérn nu=5/2       1.954 to 1.987          observation limited
```

These are design-level Mahalanobis separations, not specimen results, posterior model probabilities, or discovery significances.

### 8. Finite-map and same-raster covariance

For a Gaussian map vector `y ~ N(0,C)` and centering projector `P`, R04 implements the exact moments

```text
E[s_naive^2] = tr(P C)/(n-1)
Var(s_naive^2) = 2 tr[(P C)^2]/(n-1)^2.
```

For two resolutions measured on the same raster,

```text
Cov(q_i,q_j)
=
2 tr(P C_ij P C_ji)/(n-1)^2.
```

The controlled `10 x 10` raster has only `1.7377` effective samples for the map mean and a naive-variance expectation equal to `0.4288` of the marginal filtered variance. Treating all 100 pixels as independent understates the controlled parameter uncertainty by:

```text
SD(log A) inflation                 4.4397x
SD(log xi) inflation                2.8677x
parameter covariance determinant   404.6855x
```

Increasing nominal pixel count by `4x` at approximately fixed field of view improves full-covariance `log xi` precision by only `0.393%`, whereas the independent-pixel approximation predicts `50.188%`.

### 9. Measurement design

For the declared homoscedastic Gaussian model, the locally D-optimal two-scale allocation places equal weight at the smallest and largest feasible scales. Two endpoints estimate the Gaussian parameters but cannot test the family. The implemented three-scale optimizer reserves an interior scale while enforcing a D-efficiency floor.

The existing framework therefore already answers most of the requested questions about the minimum number, placement, calibration, and covariance treatment of probe scales.

## Strongest unsolved question

The strongest unresolved question is:

> After correcting for measured PSF, pixel integration, finite depth, map geometry, within-map covariance, and same-raster cross-scale covariance, does a real HgCdTe specimen exhibit a reproducible variance-versus-scale curve that identifies or falsifies a declared covariance family and predicts a second modality from the same latent spatial field?

This question is stronger than adding another synthetic covariance family or observation operator. It directly determines whether R04 is a material result or only a rigorous design framework.

## Precise novelty opportunity

The defensible candidate contribution is narrow:

> A calibrated multiresolution HgCdTe metrology theory that separates microscopic point variance, probe-filtered variance, map-estimator bias, effective information, covariance-family closure, and modality-specific reported edges, then validates those distinctions on one registered numerical specimen dataset.

General covariance filtering, Gaussian convolution, Matérn covariance, Fisher information, quadratic-form moments, finite-aperture mapping, PL/transmission mapping, and disorder-broadened optical edges are prior art. The remaining potential novelty lies in the integrated HgCdTe inference and falsification consequence, not in any one mathematical ingredient.

A targeted current search did not locate an HgCdTe paper that already combines measured multiscale kernels, covariance-family testing, full map covariance, and cross-modal prediction. This is not proof of absence and must remain a bounded candidate distinction until a claim-level review accompanies any manuscript authorization.

## Nearest prior art

### Measurement-scale HgCdTe evidence

1. **Gopal, Ashokan, and Dhar (1992), DOI `10.1016/0020-0891(92)90053-V`.** Same epilayer measured with nominal `3 mm` and `250 micrometre` incident beams. Sample 90239 shows a rendered transmission shift interpreted as lateral composition nonuniformity; sample 90211 is a qualitative control. This is the nearest same-specimen scale-dependent benchmark, but it lacks original arrays, a third scale, measured PSFs, registration, repeat covariance, and complete depth metadata.

2. **Chang et al. (2005), DOI `10.1016/j.jcrysgro.2005.01.051`.** Establishes finite-aperture transmission mapping and model-conditioned composition/thickness maps. It does not report a same-region aperture sweep or covariance inverse.

3. **Furstenberg, White, and Olson (2005), DOI `10.1007/s11664-005-0022-8`.** Establishes spatially resolved PL and transmission and documents excitation, collection, thickness, composition, and inclusion ambiguities. Multiple modalities are not multiple probe scales.

4. **Ruzhevich et al. (2024), DOI `10.1364/JOT.91.000077`.** The accessible abstract establishes composition-regime-dependent optical interpretation and localization language. The full spatial and numerical method remains access bounded in the repository audit.

### Random-mass and topological context

1. **Krishtopenko et al. (2022), DOI `10.1103/PhysRevB.105.195408`.** Provides the nearest HgCdTe disorder/topology reference identified in the audit: an uncorrelated-disorder SCBA treatment in a reduced Kane model. Reproducing that limit would be Stage 2 validation, not novelty.

2. Correlated random-mass Dirac models and disorder-driven topological transitions are established in broader systems. Their existence does not establish mesoscopic topological domains in HgCdTe.

No full Stage 2 claim is currently defensible because the missing HgCdTe input is not Hamiltonian code; it is a supported physical correlation-length range and a decision-changing observable beyond the scalar R03/R04 portfolio.

## Minimum viable Stage 1 model

The minimum viable Stage 1 model is the existing R04 hierarchy, not a new parallel implementation:

```text
stationary covariance family
+ measured lateral PSF and pixel/scan-bin kernel
+ finite-slab depth weighting
+ registered raster geometry
+ exact within-map and cross-scale covariance
+ declared gap law
+ one primary observation operator
+ one held-out modality or scale
+ uncertainty-aware covariance-family closure test.
```

Do not add non-Gaussian fields, bimodality, grading, PL localization, or additional mechanisms until one qualifying dataset is analyzed and a residual requires them.

The first real-data analysis should use the smallest model that can fail:

1. Gaussian covariance baseline;
2. Matérn `nu=1/2, 3/2, 5/2` alternatives already implemented;
3. measured instrument kernels at three scales;
4. full raster and cross-scale covariance;
5. one source-appropriate observation operator;
6. predeclared family-separation and residual thresholds.

## First falsifiable prediction

For one registered specimen region measured at at least three calibrated effective scales, define the inferred filtered composition or gap variances `V_i` after applying the declared observation operator and uncertainty model.

Under the isotropic two-dimensional Gaussian covariance benchmark,

```text
Y_i = 1/V_i
X_i = s_i^2
```

must be affine after the complete kernel correction. Equivalently, the second divided difference of `(X_i,Y_i)` must vanish within the propagated full covariance.

Predeclare:

```text
H0: Gaussian covariance closure
R3: covariance-weighted reciprocal-linearity residual
reject H0 when Delta_G > 3
```

where `Delta_G` is the rank-aware standardized residual using observation, calibration, kernel, map, and cross-scale covariance.

This produces three decision-changing outcomes:

1. **Reject Gaussian covariance.** The scalar one-width interpretation is falsified, and the scale dependence determines which existing Matérn alternatives remain viable.
2. **Fail to reject Gaussian covariance but retain poor recoverability.** Report only filtered variance combinations; do not report a specimen correlation length.
3. **Pass closure with adequate conditioning.** Infer `A` and `xi`, then predict a held-out scale or second modality without refitting the latent covariance. Failure of the held-out prediction falsifies the composed observation model.

This is more informative than claiming an apparent Urbach width or PL linewidth equals a microscopic disorder parameter.

## Required public or author-supplied datasets

A qualifying package must provide either:

```text
same registered specimen region measured at >=3 calibrated effective scales
```

or

```text
one original numerical high-resolution map
+ physical coordinates
+ permission to apply >=3 declared numerical kernels.
```

Mandatory metadata:

- original numerical spectra or map arrays;
- specimen and region identity;
- beam centers or registration transform;
- measured or reconstructable PSF at each scale and wavelength;
- aperture, pixel, scan-bin, and sampling definitions;
- film thickness and depth-weighting or absorption model;
- repeats, uncertainty, or covariance;
- observable definition and preprocessing chain;
- raster geometry and cross-scale sampling relationship.

For the Gopal 1992 path, the minimum upgrade is:

- original wide- and focused-beam spectra;
- beam-center coordinates;
- measured aperture/PSF descriptions;
- sample 90239 thickness and depth model;
- repeat uncertainty;
- one additional calibrated beam size.

Rendered publication pixels, nominal beam diameters, multiple modalities, or nominal raster pixels are not substitutes.

## Major scientific risks

1. **External-data nonavailability.** The current source portfolio may never supply original arrays and instrument covariance.
2. **Insufficient scale leverage.** Available probe sizes may all lie in one asymptotic regime, making `xi` practically unrecoverable despite finite algebraic rank.
3. **Instrument uncertainty dominates family differences.** PSF or depth calibration may erase covariance-family separation.
4. **Nonstationarity.** Mean grading, wafer-scale drift, discrete inclusions, or mixed populations may dominate the stationary covariance signal.
5. **Observation-model mismatch.** Thickness, free-carrier absorption, interference, excitation, collection, or detector physics may dominate the apparent edge.
6. **Finite-map information collapse.** Dense raster pixels may supply little independent information.
7. **Prior-art compression.** A broader literature audit may reduce the candidate contribution to a measurement-design note.
8. **R05 physical gate failure.** Recovered or bounded `xi` may be far from any electronic length scale for which finite-correlation-length random mass changes an observable.
9. **R02 readiness.** Existing 8-band infrastructure is validated as software foundation, but current endpoint first-principles polar-response work is not a converged material basis for production alloy or disorder calculations.

## Computational cost estimate

### R04 qualifying-data analysis

For a small set of spectra or summary variances at `m <= 10` scales, the current forward, inverse, quadrature, and joint-envelope calculations are CPU-only and low cost: typically matrix operations below `100 x 100` plus one-dimensional deterministic quadrature. No accelerator or cluster allocation is justified.

For a raster with `n` registered centers and `m` scales, dense block construction requires approximately

```text
unique covariance blocks = m(m+1)/2
storage per dense block   = 8 n^2 bytes
construction work         = O(m^2 n^2)
quadratic-form moments    = O(m^2 n^2)
```

Representative storage:

```text
n = 2,500   one block about 50 MB
m = 3       six unique blocks about 300 MB before overhead
n = 10,000  one block about 800 MB
```

Therefore:

- begin with source-native spectra or rasters no larger than approximately `n=2,500` for direct dense validation;
- use stationarity-aware FFT, Toeplitz, sparse, or stochastic trace methods before scaling to `n=10,000` or above;
- do not use full 8-band real-space computation for an R04 data-fit question.

### R05

Current authorized cost is zero production computation. A future activation tranche must first reproduce a homogeneous limit and one uncorrelated SCBA reference with an explicit basis and unit contract. Large real-space Kane calculations, finite-size scaling, and topological diagnostics remain unauthorized.

## Stop conditions

### Stop or publish R04 as a bounded metrology framework if any condition holds

1. No qualifying numerical dataset can be obtained after a documented source and author-data search.
2. All accessible scale designs are practically rank deficient or have `SD(log xi)` above the predeclared useful threshold.
3. Instrument, map, and cross-scale covariance reduce every supported family separation below `Delta=3`.
4. A held-out scale or modality cannot be predicted without adding unidentifiable nuisance mechanisms.
5. Prior art establishes the same integrated HgCdTe multiscale covariance and information result.
6. The result remains only a synthetic sensitivity study with no falsifiable external path.

A negative data-readiness or recoverability result is publishable only if it establishes a general, quantitatively useful measurement-design or non-identifiability conclusion. It is not experimental validation.

### Do not activate or terminate R05 if any condition holds

1. No independently supported HgCdTe `xi_x` range exists near the target composition and temperature.
2. The resulting `kappa = xi_x/ell_K` remains asymptotically small or large over all plausible parameter bounds and finite correlation length does not change a measurable prediction.
3. The candidate anomaly is explained by R03/R04 scalar distributional, finite-kernel, carrier, defect, or observation-operator effects.
4. The full Kane structure does not alter the reduced controlled prediction.
5. The uncorrelated SCBA reference cannot be reproduced under matched conventions.
6. No defensible topological diagnostic and no experimentally falsifiable consequence are available.
7. Prior art already establishes the finite-correlation-length result under equivalent assumptions.

Local opposite-sign probability, connected sign domains, or a visually suggestive mass map do not satisfy the topological gate.

## Proposed issue and pull-request sequence

### Tranche 0 — current decision record

- **Issue #279:** reconcile the new brief with current R04/R05 state.
- **PR:** add this documentation-only memo.
- No code, numerical record, program state, manuscript, or first-principles file changes.

### Tranche 1 — qualifying data acquisition

Open one issue for either:

- Gopal 1992 author-data recovery; or
- an equivalent same-region three-scale dataset; or
- one reusable numerical high-resolution map with full calibration metadata.

Deliverables: immutable source inventory, rights and provenance record, qualification decision, and explicit missing-field report. Stop if mandatory fields are absent.

### Tranche 2 — instrument and observation contract

Create one specimen-specific instrument specification containing PSF, pixel/aperture, depth kernel, thickness, registration, preprocessing, observable, and covariance. Add no new mechanism.

### Tranche 3 — external R04 validation

Run the existing Gaussian/Matérn hierarchy against the qualifying data. Add:

- exact source-native forward calculation;
- full within-map and cross-scale covariance;
- covariance-family closure;
- conditioning and uncertainty;
- held-out scale or modality prediction;
- immutable validation record and CI.

Terminate if the data cannot distinguish the declared alternatives.

### Tranche 4 — R04 publication decision

Perform a claim-level prior-art refresh and create a theorem-and-data figure plan. Authorize a manuscript only if the external result is decision changing and the claim remains distinct.

### Tranche 5 — separate R05 gate audit, only if activated by Tranche 3

Open a new controlling R05 issue only if R04 supplies or independently corroborates a physically meaningful `sigma_E` and `xi_x` range. The issue must define:

- target composition and temperature;
- `eta` and `kappa` bounds;
- observable not explained by R03/R04;
- nearest correlated and uncorrelated prior art;
- homogeneous and SCBA validation targets;
- maximum basis/grid size;
- topological diagnostic;
- predeclared termination criterion.

No R05 branch should be created before that issue passes review.

## Claim boundaries

This memo supports:

- the conclusion that most requested Stage 1 analytical infrastructure already exists in R04;
- the conclusion that direct external validation is presently blocked by data and instrument metadata;
- the conclusion that R05 activation gates are not satisfied;
- a non-duplicative issue sequence centered on one qualifying data package.

This memo does not support:

- a specimen point variance, correlation length, covariance family, or random-mass field;
- an experimental validation claim;
- an Urbach, PL, cutoff, or topological interpretation from one latent width;
- a major novelty claim;
- manuscript or submission authorization;
- any production SCBA, real-space Kane, finite-size, percolation, or topological computation.

## Final recommendation

Concentrate the next research effort on obtaining one high-quality registered multiresolution numerical dataset and applying the existing R04 machinery without adding mechanisms. Treat inability to obtain or identify such a dataset as a formal R04 stop decision.

Keep R05 inactive. Reassess it only after an independent HgCdTe length-scale bound and an observable beyond R03/R04 are established.
