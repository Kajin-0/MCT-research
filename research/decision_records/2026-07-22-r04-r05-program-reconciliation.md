# Research decision memo: R04 external validation and the R05 activation gate

**Date:** 2026-07-22  
**Issue:** #279  
**Primary program:** R04 — measurement-kernel-aware spatial disorder  
**Affected program:** R05 — correlated random-mass Kane regime  
**Decision class:** repository and literature reconciliation; no new scientific calculation  
**Manuscript impact:** no manuscript authorization

## Executive decision

Do **not** reopen the broad two-stage implementation plan. Current `main` already contains most of the proposed Stage 1 analytical, numerical, uncertainty, and observation-operator hierarchy under R04.

Do **not** activate R05. The repository does not yet contain an independently supported HgCdTe composition-correlation-length range near the normal--inverted transition, bounded random-mass control parameters, or an observable shown to require finite-correlation-length Kane physics rather than existing R03/R04 models.

The next decision-changing milestone is external validation of R04 on one registered specimen region using original numerical data and characterized measurement kernels. R04 remains externally data blocked:

```text
partial multiresolution candidates = 1
direct validation candidates       = 0
```

The controlling question is:

> After accounting for measured kernels, scale calibration, finite-map covariance, same-raster cross-scale covariance, and the declared observation operator, does a real HgCdTe specimen exhibit a variance-versus-scale relation that closes under a declared covariance family, yields practically recoverable parameters, and predicts an unused scale or modality without refitting?

No new R04 mechanism is authorized before one qualifying dataset is analyzed. No R05 computation is authorized.

## Repository reconciliation

R04 already provides, under explicit model boundaries:

- stationary anisotropic Gaussian covariance and Gaussian measurement kernels;
- exact Gaussian/Gaussian variance filtering;
- point-probe and scalar limits;
- one-scale non-identifiability and exact two-scale inversion;
- conditioning, Fisher information, and common-scale calibration limits;
- Gaussian covariance-family closure and Matérn `nu=1/2, 3/2, 5/2` alternatives;
- covariance-family misspecification diagnostics;
- finite-slab Beer--Lambert depth weighting and exact asymptotic benchmarks;
- composite optical-PSF, rectangular pixel or scan-bin, and depth kernels;
- transmission and detector-cutoff observation operators;
- exact finite-map Gaussian quadratic-form moments;
- exact same-raster cross-scale covariance;
- experiment allocation and joint identifiability under observation, instrument, kernel, and operator uncertainty.

Representative exact results already implemented include

```text
V_w = A sqrt[det(Lambda) / det(Lambda + 2 Sigma_w)]
```

and, for the isotropic `D`-dimensional benchmark,

```text
V(s) = A [1 + 2 s^2/xi^2]^(-D/2).
```

For an isotropic two-dimensional field,

```text
1/V(s) = 1/A + 2 s^2/(A xi^2).
```

Two scales determine this affine line exactly and cannot test the covariance family. A third calibrated scale provides the first residual degree of freedom.

The external state, not missing theory, is controlling. The nearest source-level benchmark remains Gopal, Ashokan, and Dhar (1992): one epilayer was measured with nominal incident beam diameters of `3 mm` and `250 micrometres`, and one specimen showed a rendered spectral shift. The source lacks original numerical spectra, a third scale, measured PSFs, registration, repeat covariance, and complete depth metadata. It is therefore a partial multiresolution benchmark, not direct validation.

## Exact Gaussian covariance-family closure test

### Declared observation vector

For `m` calibrated effective scales, define

\[
y_i = \frac{1}{V_i},
\qquad
x_i = s_i^2,
\]

and

\[
\mathbf y =
\begin{bmatrix}
y_1\\
\vdots\\
y_m
\end{bmatrix},
\qquad
X =
\begin{bmatrix}
1 & x_1\\
\vdots & \vdots\\
1 & x_m
\end{bmatrix}.
\]

Here `V_i` is the inferred filtered composition or gap variance after applying the declared measurement-kernel and observation-operator contract. The reciprocal transformation must be propagated from the native observation space; it must not be assigned an ad hoc independent error bar.

Conditional on fixed `s_i`, let `C_y` be the complete covariance of `y`. It must include every applicable response-side contribution and cross term from:

- observation uncertainty;
- repeated-measurement covariance;
- instrument calibration that affects the inferred response at fixed scale;
- kernel uncertainty other than unresolved uncertainty in the scale coordinates themselves;
- finite-map covariance;
- same-raster cross-scale covariance;
- observation-operator uncertainty.

Material uncertainty in `s_i` changes the design matrix and is handled as an errors-in-variables problem below. It may enter `C_y` only through a verified approximation demonstrating adequate coverage and negligible decision-changing bias.

Rank-one systematic terms, common calibration terms, and same-raster cross-scale terms generally make `C_y` non-diagonal. Nominal raster pixels and different resolutions of one material realization are not independent repeats.

### Generalized least squares

For fixed calibrated scales and positive-definite `C_y`, define

\[
\widehat{\boldsymbol\beta}
=
\left(X^T C_y^{-1}X\right)^{-1}
X^T C_y^{-1}\mathbf y,
\]

where

\[
\boldsymbol\beta =
\begin{bmatrix}
\beta_0\\
\beta_1
\end{bmatrix}
=
\begin{bmatrix}
1/A\\
2/(A\xi^2)
\end{bmatrix}.
\]

For an interior physically admissible fit,

\[
\widehat A = \frac{1}{\widehat\beta_0},
\qquad
\widehat\xi =
\sqrt{\frac{2\widehat\beta_0}{\widehat\beta_1}}.
\]

A negative intercept or slope is not a valid Gaussian material estimate. If positivity constraints become active, calibrate the constrained statistic using a predeclared parametric bootstrap or posterior-predictive calculation.

Define

\[
\mathbf r_G = \mathbf y-X\widehat{\boldsymbol\beta}
\]

and the Gaussian-family closure statistic

\[
\boxed{
Q_G = \mathbf r_G^T C_y^{-1}\mathbf r_G
}.
\]

Under the declared linear-Gaussian closure assumptions, with fixed scales, correctly specified `C_y`, full column rank of `X`, an interior parameter point, and no data-dependent model selection,

\[
Q_G \sim \chi^2_{m-2}.
\]

For exactly three scales,

\[
Q_G \sim \chi^2_1.
\]

Only in this one-residual-degree-of-freedom case define

\[
\Delta_G = \sqrt{Q_G}.
\]

Because a squared standard normal variate has a `chi-square_1` distribution, the predeclared rule

```text
reject Gaussian covariance closure when Delta_G > 3
```

is an approximately two-sided three-standard-deviation rule under the assumptions above. Report the exact `chi-square_1` tail probability.

For `m > 3`, `sqrt(Q_G)` is not a Gaussian z score. Use the `chi-square_(m-2)` tail probability or a predeclared critical value for `m-2` residual degrees of freedom. It may be reported only as a distance magnitude, not as a number of standard deviations.

If `C_y` is positive semidefinite rather than positive definite, use declared rank-aware whitening or a Moore--Penrose pseudoinverse after removing numerically null directions. The reference degrees of freedom follow the retained residual rank, not automatically `m-2`. Predeclare the eigenvalue threshold and any regularization. When covariance is estimated with material uncertainty or the asymptotic chi-square approximation is doubtful, calibrate `Q_G` by simulation under the complete null model.

The closure statistic establishes only whether measured scale dependence is compatible with the declared covariance/kernel model. Passing closure does not prove that the covariance is uniquely Gaussian, that `A` and `xi` are recoverable, that a held-out observation is predicted, or that the latent field is composition.

## Scale uncertainty is an errors-in-variables problem

The chi-square reference above conditions on fixed calibrated `s_i`. Material uncertainty in effective scales changes `X` and must not automatically be absorbed into `C_y` as if only the response were uncertain.

Distinguish:

1. **Relative scale spacing.** Ratios and separations among `s_i` control covariance-family shape information and closure power.
2. **Absolute scale calibration.** The common physical length scale controls inferred absolute `xi`.
3. **Common-mode calibration uncertainty.** A multiplicative error shared by all scales is exactly confounded with absolute correlation length under the established R04 assumptions.
4. **Scale-specific calibration uncertainty.** Independent or partially correlated errors distort relative spacing and can alter closure and family discrimination.

The retained common-mode result is

\[
\operatorname{Var}(\log\xi_{\rm absolute})
=
\operatorname{Var}(\log\xi_{\rm relative})
+
\tau_{\rm scale}^2
\]

under the declared independent broad-prior conditions. Repeats cannot remove this absolute calibration floor.

When scale uncertainty is material, use one of:

- joint nuisance-parameter inference for effective `s_i`;
- generalized total least squares;
- an errors-in-variables likelihood;
- posterior-predictive integration over scale calibration;
- Monte Carlo propagation through the complete PSF, pixel, depth, and observation model.

A first-order reduction of scale uncertainty into response covariance is acceptable only after verification against the nonlinear kernel model over the declared uncertainty range. The verification must demonstrate acceptable bias, closure-tail probability, and parameter coverage. Otherwise retain scale variables explicitly.

## Three scales, four scales, and held-out validation

```text
three calibrated scales
= minimum Gaussian covariance-family closure test
```

because two scales determine the affine line exactly.

```text
four calibrated scales
= preferred minimum for an internal held-out-scale prediction
```

when a predeclared subset fits the covariance model and at least one unused scale is reserved for validation.

An equally strong alternative is

```text
three calibrated scales
+ one independently modeled second modality
```

where the latent covariance is inferred without the held-out modality and the second modality is predicted without refitting `A`, `xi`, or covariance-family identity.

A three-scale closure test performed on the same three observations is a family-falsification test. It is not independent external predictive validation.

The qualifying external-data threshold remains at least three calibrated scales, but acquisition priority is:

1. four or more calibrated scales;
2. three calibrated scales plus a held-out independently modeled modality;
3. three calibrated scales only, as the minimum family-closure package.

## Four evidential levels

### Level 1 — Model closure

Does the variance-versus-scale curve satisfy the declared covariance-family relation under the complete covariance and kernel model?

Primary evidence: `Q_G`, its degrees of freedom, and its calibrated tail probability, plus corresponding tests for supported alternative families.

### Level 2 — Parameter recoverability

Are `A` and `xi` practically estimable with acceptable uncertainty and conditioning?

Required evidence includes full parameter covariance or posterior, conditioning, parameter correlation, sensitivity to calibration and fitting convention, physical admissibility, and predeclared useful-precision thresholds. Finite algebraic rank does not establish recoverability.

### Level 3 — Held-out predictive validation

Can the inferred latent covariance predict an unused scale or second modality without refitting covariance amplitude, correlation length, or family?

A closure pass on fitting observations does not establish this level.

### Level 4 — Material interpretation

Can inferred `A`, `xi`, and covariance family be assigned to a physically meaningful HgCdTe composition field rather than thickness variation, carrier variation, defects, inclusions, excitation or collection variation, interference processing, or another latent field?

This requires independent specimen evidence, cross-modal consistency, nuisance discrimination, and source provenance. Passing Levels 1--3 does not by itself establish composition disorder.

Each level is necessary but not sufficient for the next.

## Predeclared held-out prediction rule

Partition observations before analysis into fitting set `F` and held-out set `H`.

Predeclare:

- which scales or modalities belong to `F` and `H`;
- the covariance family fitted on `F`;
- which observations estimate `A` and `xi`;
- which instrument and observation-operator quantities are independently calibrated;
- which quantities are frozen before revealing `H`;
- the complete covariance blocks `C_FF`, `C_FH`, `C_HF`, and `C_HH`;
- the acceptance statistic and critical value.

After fitting on `F`, freeze covariance-family identity, `A`, `xi`, all shared latent parameters, and the fitting convention. The held-out result must not be used to re-estimate those quantities.

Instrument or modality-specific nuisance quantities may enter the prediction only when independently calibrated, fixed by a source contract, or integrated over a prior established without using the held-out measurement. A nuisance inferred from `H` weakens or invalidates the held-out test and must be reported as such.

For jointly Gaussian observation errors and fixed fitted parameters, retain same-specimen correlation. The conditional predictive mean and covariance are

\[
\boldsymbol\mu_{H\mid F}
=
\boldsymbol\mu_H
+
C_{HF}C_{FF}^{-1}
\left(\mathbf y_F-\boldsymbol\mu_F\right),
\]

\[
C_{H\mid F}
=
C_{HH}-C_{HF}C_{FF}^{-1}C_{FH}.
\]

Let `J_F` and `J_H` be fitting and held-out mean Jacobians with respect to fitted latent parameters `theta`. If covariance blocks are treated as parameter independent, the conditional prediction Jacobian is

\[
\widetilde J_H
=
J_H-C_{HF}C_{FF}^{-1}J_F.
\]

A verified first-order predictive covariance is

\[
C_{\rm pred}
\simeq
C_{H\mid F}
+
\widetilde J_H C_{\theta\mid F}\widetilde J_H^T.
\]

If covariance depends materially on `theta`, the model is nonlinear, scale uncertainty is material, constraints are active, or parameter/error correlations invalidate this approximation, use posterior-predictive or Monte Carlo integration through the complete model.

Define

\[
\mathbf r_H
=
\mathbf y_H-\widehat{\boldsymbol\mu}_{H\mid F}
\]

and

\[
Q_H
=
\mathbf r_H^T C_{\rm pred}^{-1}\mathbf r_H.
\]

Under a fixed correctly specified linear-Gaussian prediction with known covariance, compare `Q_H` with the appropriate chi-square distribution for retained predictive rank. Otherwise use a predeclared posterior-predictive or simulation-calibrated tail probability.

A valid held-out test does not refit `A`, `xi`, covariance-family identity, or shared latent-field parameters after observing `H`.

## Minimum viable external R04 analysis

The first real-data analysis must use the smallest existing hierarchy that can fail:

1. Gaussian covariance baseline;
2. Matérn `nu=1/2, 3/2, 5/2` alternatives already implemented;
3. measured instrument kernels at available scales;
4. explicit scale-calibration model;
5. full within-map and same-raster cross-scale covariance;
6. one source-appropriate observation operator;
7. GLS, errors-in-variables, or posterior closure test as warranted;
8. conditioning and practical recoverability analysis;
9. one predeclared held-out scale or modality when the package permits it.

Do not add non-Gaussian fields, bimodality, grading, PL localization, or other mechanisms until a qualifying dataset leaves a decision-changing residual that requires them.

## Preferred external package

A qualifying package must contain either

```text
same registered specimen region measured at >=3 calibrated effective scales
```

or

```text
one original numerical high-resolution map
+ physical coordinates
+ calibration metadata
+ permission to apply >=3 declared numerical kernels.
```

Preferred acquisition order is:

1. **Four or more calibrated scales** on one registered region, allowing closure plus a held-out scale.
2. **Three calibrated scales plus one independently modeled modality**, allowing closure plus cross-modal prediction.
3. **Three calibrated scales only**, allowing the minimum covariance-family closure test but not independent predictive validation.

Mandatory metadata are:

- original numerical spectra or map arrays;
- specimen and registered region identity;
- beam centers or a registration transform;
- measured or reconstructable PSF at every scale and relevant wavelength;
- aperture, pixel, scan-bin, and sampling definitions;
- absolute and relative scale-calibration covariance;
- film thickness and depth-weighting or absorption model;
- repeats, observation uncertainty, and repeated-measurement covariance;
- observable definition and preprocessing chain;
- raster geometry and cross-scale sampling relationship;
- independently calibrated modality-specific nuisance parameters when a held-out modality is proposed.

For the Gopal 1992 path, the minimum upgrade remains original wide- and focused-beam spectra, beam-center coordinates, measured aperture/PSF descriptions, sample 90239 thickness and depth model, repeat uncertainty, and at least one additional calibrated beam size.

Rendered publication pixels, nominal beam diameters, multiple unregistered modalities, or nominal raster pixels are not substitutes.

## Decision-changing outcomes

The first qualifying analysis has four possible outcomes:

1. **Reject Gaussian closure.** Report `Q_G`, degrees of freedom, tail probability, covariance assumptions, and which existing alternatives remain viable. Do not infer a Gaussian `xi`.
2. **Fail to reject closure but fail recoverability.** Report only identifiable filtered combinations or bounds. Do not report a specimen correlation length.
3. **Pass closure and recoverability but fail held-out prediction.** The composed kernel or observation model is falsified or incomplete; do not promote the result to external validation.
4. **Pass closure, recoverability, and held-out prediction.** Proceed to Level 4 material-interpretation tests and a claim-level prior-art refresh. Do not automatically identify the latent field as composition.

## Computational discipline

For source-native spectra or summary variances at `m <= 10` scales, the existing forward, inverse, quadrature, and covariance calculations are CPU-only and low cost. No accelerator or cluster allocation is justified.

For a raster with `n` registered centers and `m` scales, dense covariance storage and construction scale as

```text
unique covariance blocks = m(m+1)/2
storage per dense block   = 8 n^2 bytes
construction work         = O(m^2 n^2)
quadratic-form moments    = O(m^2 n^2)
```

Begin direct dense validation near `n <= 2,500`. Use stationarity-aware FFT, Toeplitz, sparse, low-rank, or stochastic trace methods before scaling above that range. Do not use full 8-band real-space computation for an R04 data-fit question.

Every external result must include dimensional checks, limiting cases, covariance positive-semidefiniteness checks, scale-unit invariance, convergence or approximation verification, immutable inputs and outputs, and a predeclared failure criterion.

## R04 stop and publication conditions

Stop the external inversion path, or retain R04 as a bounded metrology framework, if:

1. no qualifying numerical dataset is obtained after a documented source and author-data search;
2. all available designs are practically rank deficient or exceed the useful uncertainty threshold for `xi`;
3. scale uncertainty cannot be controlled by an adequate errors-in-variables treatment;
4. instrument, map, and cross-scale covariance remove family discrimination;
5. no held-out scale or modality can be predicted without fitting unidentifiable nuisance parameters to the held-out result;
6. Level 4 cannot distinguish composition from competing latent fields;
7. prior art establishes the same integrated HgCdTe inference and validation result;
8. the result remains synthetic with no falsifiable external path.

A negative data-readiness, closure, or recoverability result is publishable only if it establishes a general and quantitatively useful metrology or non-identifiability conclusion. It is not experimental material validation.

## R05 remains inactive

No R05 implementation or production calculation is authorized. Specifically prohibited are:

- SCBA implementation;
- finite-correlation-length self-energy calculations;
- real-space Kane calculations;
- percolation calculations;
- domain-wall calculations;
- topological-invariant calculations;
- production first-principles alloy calculations.

A separate R05 gate issue is required before any branch or computational tranche. It must establish all of:

1. an independently supported HgCdTe correlation-length range near the target composition and temperature;
2. bounded `eta = sigma_E/|mean(E_g)|`;
3. bounded `kappa = xi_x/ell_K` under a declared Kane-length convention;
4. an observable not explained by R03/R04 scalar, finite-kernel, carrier, defect, or observation-operator models;
5. a matched homogeneous and uncorrelated-disorder validation target;
6. a defensible topological diagnostic with a stated domain of validity;
7. a predeclared computation budget, convergence metric, and termination criterion.

The gate must also define target composition, temperature, basis, units, maximum grid or basis size, and the decision that would change if the calculation succeeds.

A local sign probability, connected sign map, percolating-looking realization, or visually suggestive random-mass domain pattern does not satisfy this gate and does not establish a bulk topological invariant.

Current authorized R05 production cost is zero.

## Tranche sequence

### Tranche 0 — decision record

- Issue #279 and PR #280 record this documentation-only decision.
- No source, tests, validation JSON, program state, manuscript, first-principles, or active-program file is changed.

### Tranche 1 — qualifying data acquisition

Open one focused issue for Gopal 1992 author-data recovery or an equivalent multiresolution numerical package. Deliver an immutable source inventory, rights and provenance record, qualification decision, and explicit missing-field report. Stop if mandatory fields are absent.

### Tranche 2 — specimen-specific instrument and validation contract

Record fitting and held-out observations, PSFs, scale covariance, pixel or aperture geometry, depth model, registration, preprocessing, observation operator, nuisance-parameter policy, `Q_G`, held-out statistic, and critical values. Add no new physical mechanism.

### Tranche 3 — external R04 validation

Run the existing Gaussian/Matérn hierarchy with complete covariance and errors-in-variables treatment. Report Levels 1--4 separately. Add immutable validation records and CI only for source-native analysis.

### Tranche 4 — publication decision

Refresh claim-level prior art and authorize a manuscript only if the external result is decision changing, predictively validated, materially interpretable, and distinct.

### Tranche 5 — separate R05 gate audit

Open only if independent evidence establishes the complete R05 activation requirements above. No R05 branch should exist before that gate passes review.

## Claim boundaries

This memo supports:

- the conclusion that most proposed Stage 1 infrastructure already exists under R04;
- the conclusion that R04 is blocked by qualifying external data and instrument metadata;
- a mathematically defined Gaussian covariance-family closure statistic;
- an errors-in-variables requirement for uncertain effective scales;
- separation of closure, recoverability, held-out prediction, and material interpretation;
- a preferred four-scale or three-scale-plus-modality external package;
- the conclusion that R05 activation requirements are not satisfied.

This memo does not support:

- a specimen point variance, correlation length, covariance family, or random-mass field;
- independent validation from a three-scale fit-and-test on the same observations;
- identification of composition from a latent variance curve alone;
- an Urbach, PL, cutoff, or topological interpretation from one latent width;
- a major novelty claim;
- manuscript or submission authorization;
- any SCBA, self-energy, real-space Kane, finite-size, percolation, domain-wall, topological, or production alloy computation.

## Final recommendation

Concentrate the next R04 effort on acquiring one registered numerical package with characterized kernels and scale covariance. Prefer four or more scales, then three scales plus a held-out modality, and accept three scales alone only as the minimum family-closure package.

Apply the existing R04 hierarchy with the formally defined closure test, explicit errors-in-variables treatment, separate evidential levels, and predeclared held-out prediction. Treat failure to obtain such a package as a formal data-access stop decision.

Keep R05 inactive. Reassess it only through a separate gate after independent HgCdTe length-scale and energy-disorder bounds establish a decision-changing regime beyond R03/R04.
