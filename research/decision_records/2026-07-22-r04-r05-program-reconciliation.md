# Research decision memo: R04 external validation and the R05 activation gate

**Date:** 2026-07-22  
**Issue:** #279  
**Primary program:** R04 — measurement-kernel-aware spatial disorder  
**Affected program:** R05 — correlated random-mass Kane regime  
**Decision class:** repository and literature audit; no new scientific calculation  
**Manuscript impact:** no manuscript authorization

## Executive decision

Do **not** reopen the broad two-stage implementation plan. Current `main` already contains most of the proposed Stage 1 analytical, numerical, uncertainty, and observation-operator hierarchy under R04.

Do **not** activate R05. The repository does not yet contain an independently supported HgCdTe composition-correlation-length range near the normal--inverted transition, bounded random-mass control parameters, or an observable that has been shown to require finite-correlation-length Kane physics rather than the existing R03/R04 models.

The next decision-changing milestone is external validation of R04 on one registered specimen region using original numerical data and characterized measurement kernels. R04 remains analytically mature but externally data blocked:

```text
partial multiresolution candidates = 1
direct validation candidates       = 0
```

The governing question is now experimental and inferential:

> After accounting for measured kernels, scale calibration, finite-map covariance, same-raster cross-scale covariance, and the declared observation operator, does a real HgCdTe specimen exhibit a variance-versus-scale relation that closes under a declared covariance family, yields practically recoverable parameters, and predicts an unused scale or modality without refitting?

The earlier PR #194 manuscript bundle is retired. No active R03 or R04 manuscript is authorized, and no repository-wide flagship submission path exists to preserve.

## Repository reconciliation

The proposed Stage 1 work is not an unimplemented program. R04 already provides, under explicit model boundaries:

- stationary anisotropic Gaussian covariance and Gaussian measurement kernels;
- exact Gaussian/Gaussian variance filtering;
- point-probe and scalar limits;
- one-scale non-identifiability and exact two-scale inversion;
- conditioning, Fisher information, and common-scale calibration limits;
- Gaussian covariance-family closure and Matérn `nu=1/2, 3/2, 5/2` alternatives;
- covariance-family misspecification and fitting-convention diagnostics;
- finite-slab Beer--Lambert depth weighting and exact asymptotic benchmarks;
- composite optical-PSF, rectangular pixel or scan-bin, and depth kernels;
- transmission and detector-cutoff operation-order models;
- exact finite-map Gaussian quadratic-form moments;
- exact same-raster cross-scale covariance;
- experiment allocation and joint identifiability under observation, instrument, kernel, and operator uncertainty.

Representative exact results already implemented include

```text
V_w = A sqrt[det(Lambda) / det(Lambda + 2 Sigma_w)]
```

for anisotropic Gaussian covariance `Lambda` and Gaussian kernel covariance `Sigma_w`, and

```text
V(s) = A [1 + 2 s^2/xi^2]^(-D/2)
```

for the isotropic `D`-dimensional benchmark.

For an isotropic two-dimensional field,

```text
1/V(s) = 1/A + 2 s^2/(A xi^2).
```

Two scales determine the affine line exactly and cannot test the covariance family. A third calibrated scale provides the first residual degree of freedom.

The external state, not missing theory, is controlling. The nearest source-level benchmark remains Gopal, Ashokan, and Dhar (1992): the same epilayer was measured using nominal incident beam diameters of `3 mm` and `250 micrometres`, and one specimen showed a rendered spectral shift. The source lacks original numerical spectra, a third scale, measured PSFs, registration, repeat covariance, and complete depth metadata. It is therefore a partial multiresolution benchmark, not direct validation.

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

Material uncertainty in the `s_i` changes the design matrix and is handled as an errors-in-variables problem below. It may enter `C_y` only through a verified approximation that demonstrates adequate coverage and negligible decision-changing bias.

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

When the fitted coefficients are physically admissible,

\[
\widehat A = \frac{1}{\widehat\beta_0},
\qquad
\widehat\xi =
\sqrt{\frac{2\widehat\beta_0}{\widehat\beta_1}}.
\]

A negative intercept or slope is not a valid Gaussian material estimate. If positivity constraints become active, the ordinary interior chi-square reference below is no longer automatic; the constrained test must be calibrated by a predeclared parametric bootstrap or posterior-predictive calculation.

Define the closure residual

\[
\mathbf r_G
=
\mathbf y-X\widehat{\boldsymbol\beta}
\]

and the Gaussian-family closure statistic

\[
\boxed{
Q_G
=
\mathbf r_G^T C_y^{-1}\mathbf r_G.
}
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

is an approximately two-sided three-standard-deviation rule under the assumptions above. Its exact `chi-square_1` tail probability should be reported.

For `m > 3`, `sqrt(Q_G)` is not a Gaussian z score. Use the `chi-square_(m-2)` tail probability or a predeclared critical value for `m-2` residual degrees of freedom. The report may provide `sqrt(Q_G)` as a distance magnitude only if it is explicitly labeled as such and not interpreted as a number of standard deviations.

If `C_y` is positive semidefinite rather than positive definite, use a declared rank-aware whitening or Moore--Penrose pseudoinverse after removing numerically null directions. The reference degrees of freedom then follow the rank of the whitened residual subspace, not automatically `m-2`. The retained eigenvalue threshold and any regularization must be predeclared. When covariance is estimated with material uncertainty or the asymptotic chi-square approximation is doubtful, calibrate `Q_G` by simulation under the complete null model.

### What the closure test establishes

The closure statistic tests only the relation between measured scale dependence and the declared Gaussian covariance/kernel model. Passing closure does not prove that:

- the covariance is uniquely Gaussian;
- `A` and `xi` are well conditioned;
- an unused scale or modality is predicted;
- the latent field is composition rather than thickness, carriers, defects, or preprocessing structure.

Failure to reject Gaussian closure is not evidence of a universal Gaussian HgCdTe covariance law.

## Scale uncertainty is an errors-in-variables problem

The chi-square result above conditions on fixed calibrated `s_i`. Material uncertainty in the effective scales changes the design matrix `X` and must not automatically be absorbed into `C_y` as if only the response variable were uncertain.

Distinguish four scale-calibration components:

1. **Relative scale spacing.** Ratios and separations among the `s_i` control covariance-family shape information and closure power.
2. **Absolute scale calibration.** The common physical length scale controls the inferred absolute `xi`.
3. **Common-mode calibration uncertainty.** A multiplicative error shared by all scales is exactly confounded with absolute correlation length under the established R04 assumptions.
4. **Scale-specific calibration uncertainty.** Independent or partially correlated errors distort relative scale spacing and can alter both closure and family discrimination.

The retained exact common-mode result is

\[
\operatorname{Var}(\log\xi_{\rm absolute})
=
\operatorname{Var}(\log\xi_{\rm relative})
+
\tau_{\rm scale}^2
\]

under the declared independent broad-prior conditions. Repeats cannot remove this absolute calibration floor.

When scale uncertainty is material, use one of the following predeclared methods:

- joint nuisance-parameter inference for the effective `s_i`;
- generalized total least squares;
- an errors-in-variables likelihood;
- posterior-predictive integration over scale calibration;
- Monte Carlo propagation through the complete PSF, pixel, depth, and observation model.

A first-order reduction of scale uncertainty into response covariance is acceptable only after verification against the nonlinear kernel model over the declared uncertainty range. The verification must show that bias, closure-tail probability, and parameter uncertainty remain within predeclared tolerances. Otherwise, retain the scale variables explicitly.

## Three scales, four scales, and held-out validation

The acquisition and evidence hierarchy is:

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

Required evidence includes:

- full parameter covariance or posterior;
- conditioning and parameter correlation;
- sensitivity to scale calibration and fitting convention;
- physical admissibility of the inferred parameters;
- predeclared useful-precision thresholds.

Finite algebraic rank does not establish recoverability.

### Level 3 — Held-out predictive validation

Can the inferred latent covariance predict an unused scale or second modality without refitting the covariance amplitude, correlation length, or family?

A closure pass on the fitting observations does not establish this level.

### Level 4 — Material interpretation

Can the inferred `A`, `xi`, and covariance family be assigned to a physically meaningful HgCdTe composition field rather than thickness variation, carrier variation, defects, inclusions, excitation or collection variation, interference processing, or another latent field?

This level requires independent specimen evidence, cross-modal consistency, nuisance discrimination, and source provenance. Passing Levels 1--3 does not by itself establish composition disorder.

Each level is necessary but not sufficient for the next.

## Predeclared held-out prediction rule

Partition the observations before analysis into a fitting set `F` and a held-out set `H`.

The protocol must predeclare:

- which scales or modalities belong to `F` and `H`;
- the covariance family fitted on `F`;
- which observations estimate `A` and `xi`;
- which instrument and observation-operator quantities are independently calibrated;
- which quantities are frozen before revealing `H`;
- the complete joint covariance blocks `C_FF`, `C_FH`, `C_HF`, and `C_HH`;
- the acceptance statistic and critical value.

After fitting on `F`, freeze:

- covariance-family identity;
- `A`;
- `xi`;
- all shared latent-field parameters;
- any fitting convention or model-selection decision.

The held-out result must not be used to re-estimate those quantities.

Instrument or modality-specific nuisance quantities may enter the prediction only when they are independently calibrated, fixed by a source contract, or integrated over a prior established without using the held-out measurement. A nuisance parameter inferred from `H` weakens or invalidates the held-out test and must be reported as such.

For jointly Gaussian observation errors and fixed fitted parameters, the same-specimen correlation between fitting and held-out observations must be retained. The conditional predictive mean and covariance are

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

Let `J_F` and `J_H` be the fitting and held-out mean Jacobians with respect to the fitted latent parameters `theta`. If the covariance blocks are treated as parameter independent, the conditional prediction Jacobian is

\[
\widetilde J_H
=
J_H-C_{HF}C_{FF}^{-1}J_F.
\]

A verified first-order predictive covariance is then

\[
C_{\rm pred}
\simeq
C_{H\mid F}
+
\widetilde J_H C_{\theta\mid F}\widetilde J_H^T.
\]

If the covariance depends materially on `theta`, the model is nonlinear, scale uncertainty is material, constraints are active, or parameter/error correlations invalidate this approximation, use posterior-predictive or Monte Carlo integration through the complete model.

Define the held-out residual

\[
\mathbf r_H
=
\mathbf y_H-\widehat{\boldsymbol\mu}_{H\mid F}
\]

and the predictive statistic

\[
Q_H
=
\mathbf r_H^T C_{\rm pred}^{-1}\mathbf r_H.
\]

Under a fixed, correctly specified linear-Gaussian prediction with known covariance, `Q_H` is compared with the appropriate chi-square distribution for the retained predictive rank. Otherwise, use a predeclared posterior-predictive or simulation-calibrated tail probability.

A valid held-out test does not refit `A`, `xi`, covariance-family identity, or shared latent-field parameters after observing `H`.

## Minimum viable external R04 analysis

The first real-data analysis should use the smallest existing hierarchy that can fail:

1. Gaussian covariance baseline;
2. Matérn `nu=1/2, 3/2, 5/2` alternatives already implemented;
3. measured instrument kernels at the available scales;
4. explicit scale-calibration model;
5. full within-map and same-raster cross-scale covariance;
6. one source-appropriate observation operator;
7. GLS, errors-in-variables, or posterior closure test as warranted;
8. conditioning and practical recoverability analysis;
9. one predeclared held-out scale or modality when the package permits it.

Do not add non-Gaussian fields, bimodality, grading, PL localization, or other mechanisms until a qualifying dataset leaves a decision-changing residual that requires them.

## Preferred external package

A qualifying package must contain either:

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

For the Gopal 1992 path, the minimum upgrade remains:

- original wide- and focused-beam spectra;
- beam-center coordinates;
- measured aperture/PSF descriptions;
- sample 90239 thickness and depth model;
- repeat uncertainty;
- at least one additional calibrated beam size.

A fourth scale or independently modeled modality is preferred. Rendered publication pixels, nominal beam diameters, multiple unregistered modalities, or nominal raster pixels are not substitutes.

## Decision-changing outcomes

The first qualifying analysis has four possible outcomes:

1. **Reject Gaussian closure.** Report `Q_G`, degrees of freedom, tail probability, covariance assumptions, and which existing alternatives remain viable. Do not infer a Gaussian `xi`.
2. **Fail to reject closure but fail recoverability.** Report only identifiable filtered combinations or bounds. Do not report a specimen correlation length.
3. **Pass closure and recoverability but fail held-out prediction.** The composed kernel or observation model is falsified or incomplete; do not promote the result to external validation.
4. **Pass closure, recoverability, and held-out prediction.** Proceed to Level 4 material-interpretation tests and a claim-level prior-art refresh. Do not automatically identify the latent field as composition.

## Computational cost and numerical discipline

For source-native spectra or summary variances at `m <= 10` scales, the existing forward, inverse, quadrature, and covariance calculations are CPU-only and low cost. No accelerator or cluster allocation is justified.

For a raster with `n` registered centers and `m` scales, dense covariance storage and construction scale as

```text
unique covariance blocks = m(m+1)/2
storage per dense block   = 8 n^2 bytes
construction work         = O(m^2 n^2)
quadratic-form moments    = O(m^2 n^2)
```

Representative storage is approximately:

```text
n = 2,500   one dense block about 50 MB
m = 3       six unique blocks about 300 MB before overhead
n = 10,000  one dense block about 800 MB
```

Begin direct dense validation at approximately `n <= 2,500`. Use stationarity-aware FFT, Toeplitz, sparse, low-rank, or stochastic trace methods before scaling above that range. Do not use full 8-band real-space computation for an R04 data-fit question.

Every external result must include dimensional checks, limiting cases, covariance positive-semidefiniteness checks, scale-unit invariance, convergence or approximation verification, immutable inputs and outputs, and a predeclared failure criterion.

## Major scientific risks

1. **External-data nonavailability.** Original arrays and instrument covariance may remain inaccessible.
2. **Insufficient scale leverage.** All available scales may occupy one asymptotic regime.
3. **Errors-in-variables dominance.** Scale uncertainty may erase family closure or correlation-length information.
4. **Instrument uncertainty dominance.** PSF, pixel, or depth calibration may exceed family differences.
5. **Finite-map information collapse.** Dense raster pixels may supply few independent degrees of freedom.
6. **Nonstationarity.** Mean grading, drift, inclusions, or mixed populations may dominate a stationary covariance signal.
7. **Observation-model mismatch.** Thickness, free carriers, interference, excitation, collection, or detector physics may dominate the apparent edge.
8. **Material ambiguity.** A successful latent-field fit may not identify composition as the field.
9. **Prior-art compression.** Wider literature may reduce the contribution to a measurement-design result.
10. **R05 gate failure.** Any recovered or bounded `xi` may be irrelevant to electronic random-mass physics.

## R04 stop and publication conditions

Stop the external inversion path, or retain R04 as a bounded metrology framework, if any of the following holds:

1. No qualifying numerical dataset is obtained after a documented source and author-data search.
2. All available designs are practically rank deficient or exceed the predeclared useful uncertainty for `xi`.
3. Scale uncertainty cannot be controlled by an adequate errors-in-variables treatment.
4. Instrument, map, and cross-scale covariance remove family discrimination.
5. No held-out scale or modality can be predicted without fitting unidentifiable nuisance parameters to the held-out result.
6. Level 4 cannot distinguish composition from competing latent fields.
7. Prior art establishes the same integrated HgCdTe inference and validation result.
8. The result remains synthetic with no falsifiable external path.

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

A separate R05 gate issue is required before any branch or computational tranche. It must establish all of the following:

1. an independently supported HgCdTe correlation-length range near the target composition and temperature;
2. bounded
   \[
   \eta = \sigma_E/|\bar E_g|;
   \]
3. bounded
   \[
   \kappa = \xi_x/\ell_K;
   \]
   under a declared Kane-length convention;
4. an observable not explained by R03/R04 scalar, finite-kernel, carrier, defect, or observation-operator models;
5. a matched homogeneous and uncorrelated-disorder validation target;
6. a defensible topological diagnostic with a stated domain of validity;
7. a predeclared computation budget, convergence metric, and termination criterion.

The gate must also define the target composition, temperature, basis, units, maximum grid or basis size, and the decision that would change if the calculation succeeds.

A local sign probability, connected sign map, percolating-looking realization, or visually suggestive random-mass domain pattern does not satisfy this gate and does not establish a bulk topological invariant.

Current authorized R05 production cost is zero.

## Proposed issue and pull-request sequence

### Tranche 0 — current decision record

- Issue #279 and PR #280 refine this documentation-only decision.
- No source, tests, validation JSON, program state, manuscript, first-principles, or active-program file is changed.

### Tranche 1 — qualifying data acquisition

Open one focused issue for Gopal 1992 author-data recovery or an equivalent multiresolution numerical package. Deliver an immutable source inventory, rights and provenance record, qualification decision, and explicit missing-field report. Stop if mandatory fields are absent.

### Tranche 2 — specimen-specific instrument and validation contract

Record the fitting and held-out observations, PSFs, scale covariance, pixel or aperture geometry, depth model, registration, preprocessing, observation operator, nuisance-parameter policy, `Q_G`, held-out statistic, and critical values. Add no new physical mechanism.

### Tranche 3 — external R04 validation

Run the existing Gaussian/Matérn hierarchy with the complete covariance and errors-in-variables treatment. Report Levels 1--4 separately. Add immutable validation records and CI only for the source-native analysis.

### Tranche 4 — R04 publication decision

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

Apply the existing R04 hierarchy with a formally defined closure test, an explicit errors-in-variables treatment, separate evidential levels, and a predeclared held-out prediction. Treat failure to obtain such a package as a formal data-access stop decision.

Keep R05 inactive. Reassess it only through a separate gate after independent HgCdTe length-scale and energy-disorder bounds establish a decision-changing regime beyond R03/R04.