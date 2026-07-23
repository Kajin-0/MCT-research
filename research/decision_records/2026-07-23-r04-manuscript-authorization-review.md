# R04 manuscript authorization review

**Date:** 2026-07-23  
**Issue:** #327  
**Decision:** `AUTHORIZE_RESTRICTED_MANUSCRIPT`

## Executive decision

R04 supports one concise theory and methodology manuscript under a restricted
claim set.

The authorization is based on the completed analytical hierarchy, bounded
primary-source prior-art audit, explicit public HgCdTe data stop, and one
restricted cross-material real-map demonstration. It is not based on HgCdTe
specimen validation.

Authorized now:

```text
manuscript outline and figure planning     yes
restricted manuscript drafting             yes
submission                                 no
final claim audit before submission        required
new R04 mechanism                           no
new external-data search                    no
R05                                         inactive
```

## Why authorization is defensible

### 1. The contribution is an integrated information hierarchy

Finite-aperture mapping, spatial variation, adjustable apertures, PL and
transmission mapping, and model-conditioned composition/thickness inversion are
established prior art. R04 must not claim those elements as new.

The candidate distinct contribution is the integrated consequence of asking
what finite-resolution HgCdTe maps can identify when all of the following are
kept explicit:

```text
kernel-filtered variance
probe-scale calibration
covariance-family closure
misspecification and fitting convention
optical / pixel / depth integration
finite field of view
within-map correlation
same-raster cross-scale dependence
measurement allocation
observation-operator limits
```

Individual formulas come from established Gaussian-process, inverse-problem,
quadratic-form, and optimal-design mathematics. The manuscript must say so. The
candidate contribution is their closed HgCdTe measurement-design consequence,
not the invention of those mathematical tools separately.

### 2. The analytical program has reached a coherent stopping point

The current R04 hierarchy establishes, within declared models:

- one scale cannot identify both point variance and correlation length;
- two scales can estimate a Gaussian model but cannot test the family;
- a third scale provides the first Gaussian-family closure test;
- common absolute scale calibration is exactly confounded with absolute
  correlation length;
- forcing a wrong covariance family produces scale- and fit-dependent
  parameters;
- a realistic optical/pixel/depth kernel can differ materially from a
  moment-matched Gaussian;
- nominal raster pixels can greatly overstate effective information;
- variance estimates at numerical or physical scales observing the same field
  are correlated;
- allocation for parameter precision differs from allocation for family
  falsification.

This is a coherent theorem-to-design sequence. Adding another disconnected
mechanism would weaken rather than strengthen the paper.

### 3. The public real-map demonstration is useful without being validation

The public CdSeTe demonstration uses a frozen `24 x 24` Gaussian-fitted PL
peak-wavelength field. Added numerical Gaussian smoothing reduced map variance
from `13.7373 nm^2` to `1.54435 nm^2`, retaining `11.24%` at four pixels.

Under the fitted descriptive Gaussian field model, adjacent low-scale variance
estimators have correlations `0.9983` and `0.9898`. The full parameter covariance
volume is `16.98x` the false independent-pixel and independent-scale result.

The strongest result is also the strongest limitation:

```text
periodic versus reflect boundary        72.63%
central crop versus full field           72.74%
nearest versus reflect boundary         37.71%
planar detrending versus primary         19.81%
```

These effects are larger than the descriptive family separation. The map
therefore demonstrates why finite-map and edge conventions must be predeclared;
it does not identify a material covariance family.

## Why a second public dataset is not a prerequisite

A second cross-material map lacking a calibrated native kernel would not resolve
the blocked HgCdTe validation or physical-correlation-length gate. It would add
an example without changing the central evidence state.

The small-map boundary sensitivity is not merely a defect to hide. It is a
methodological result directly aligned with the R04 finite-map theory.

A second dataset may be added later only if a bounded public source directly
changes one of these conditions:

- materially larger registered field;
- source-native spectral cube;
- bounded native sample-plane kernel;
- repeat or drift information;
- a decision-changing reduction in finite-field ambiguity.

No multi-gigabyte acquisition or open-ended dataset search is authorized by this
review.

## Authorized manuscript concept

### Provisional title

> What Finite-Resolution HgCdTe Maps Can Identify: Measurement Kernels,
> Calibration, and Correlated-Raster Information

### One-sentence contribution claim

> Finite-resolution HgCdTe maps identify a kernel-filtered and
> calibration-limited spatial field whose recoverable variance, correlation
> scale, covariance-family closure, and effective information require explicit
> treatment of the measurement kernel, finite field of view, and same-raster
> cross-scale dependence.

### Article type and audience

```text
article type    theory and methodology
primary field   infrared material characterization
secondary       semiconductor optical mapping and metrology
```

### Minimum main-text result set

1. Kernel-filtered variance, recoverability, and the absolute scale-calibration
   floor.
2. Three-scale family closure and covariance-misspecification consequences.
3. Finite-map information and same-raster cross-scale covariance.
4. Restricted CdSeTe real-map demonstration of scale and finite-field
   sensitivity.

Secondary operation-order, allocation, and instrument stress-grid details should
move to appendices or supplementary material unless needed to support one of the
four main claims.

### Four-figure ceiling

```text
Figure 1  measurement kernel, variance-versus-scale, calibration confounding
Figure 2  third-scale closure and misspecification
Figure 3  finite-map bias, effective information, cross-scale covariance
Figure 4  CdSeTe map, added-scale variance, closure residuals, sensitivity
```

## Reviewer-risk disposition

### Established mathematics

**Risk:** High. Reviewers may see the paper as a collection of known formulas.

**Disposition:** Manageable only if the manuscript separates established
mathematics from the integrated R04 consequence and avoids claiming each theorem
as a standalone mathematical novelty.

### No qualifying HgCdTe external validation

**Risk:** High.

**Disposition:** Manageable for a theory/methodology article, fatal for any
material-validation claim. The limitation must appear in the abstract,
introduction, and discussion rather than only in supplementary material.

### One small cross-material map

**Risk:** Medium-high.

**Disposition:** Manageable because the real-data role is illustrative. It must
not be described as validation, prediction, or covariance-family selection.

### Unknown native PSF

**Risk:** High.

**Disposition:** Fatal for physical correlation length or deconvolution. Report
added numerical scales and descriptive pixel-space quantities only.

### PL peak wavelength is not composition

**Risk:** High.

**Disposition:** Manageable by calling the field a PL observation throughout and
keeping latent material interpretation outside the demonstrated inference.

### Numerical scales are dependent

**Risk:** High if ignored; central result if treated correctly.

**Disposition:** Use the exact same-raster covariance analysis and call the
held-out scale a closure test, not independent predictive validation.

### Scope

**Risk:** High.

**Disposition:** Enforce the four-result and four-figure ceiling. Do not add R05,
new mechanisms, first-principles work, or a broad detector-performance survey.

## Explicit unsupported claims

The manuscript may not report or imply:

- a specimen-specific HgCdTe point variance;
- a physical HgCdTe or CdSeTe correlation length;
- a universal Gaussian or Matérn covariance law;
- composition inferred directly from the CdSeTe PL peak-wavelength map;
- independent experimental validation from numerically smoothed scales;
- empirical repeat covariance from model-conditioned map statistics;
- a universal optical PSF or pixel model;
- random-mass Kane, percolation, domain-wall, or topological conclusions.

## Strongest anticipated objection and stopping rule

The strongest objection is that the paper combines established statistical
identities and lacks a qualifying HgCdTe multiresolution dataset.

The response must be the integrated information hierarchy and its explicit
measurement-design consequences. The CdSeTe example remains illustrative.

If a target venue requires HgCdTe experimental validation as a condition of
publication, the correct action is to withdraw from that venue or reclassify the
work as not ready. The claims must not be expanded and the validation gate must
not be weakened.

## Final authorization boundary

```text
restricted manuscript drafting                 authorized
manuscript submission                           not yet authorized
separate final claim audit                      mandatory
HgCdTe validation claim                         prohibited
physical correlation-length claim               prohibited
covariance-family selection                     prohibited
new data search                                 not authorized
new R04 mechanism                               not authorized
R05                                             inactive
```
