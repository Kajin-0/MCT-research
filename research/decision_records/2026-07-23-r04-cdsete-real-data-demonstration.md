# R04 CdSeTe real-data demonstration decision

**Date:** 2026-07-23  
**Issue:** #317  
**Source qualification:** PR #319  
**Result:** `RESTRICTED_REAL_DATA_DEMONSTRATION_COMPLETE`

## Decision

The existing R04 finite-map and added-kernel machinery has been exercised on one
public source-data-derived semiconductor map without experimental equipment,
private data, or external outreach.

The demonstration succeeds as a **restricted methodology result**. It does not
satisfy the HgCdTe external-validation gate.

## Source field

```text
material       Cl-treated CdSe_xTe_1-x film with 200 nm CdSe underlayer
observable     Gaussian-fitted PL peak wavelength
source file    Datasets/Figure 3e.csv
map            24 x 24
coordinate FOV 0 to 12.545 micrometres on each axis
native PSF     unmeasured and unbounded
mean           844.8215104166667 nm
sample SD      3.706389778873072 nm
range          837.0 to 862.5 nm
```

The source field remains a PL observation. It is not relabeled as alloy
composition, local bandgap truth, or an HgCdTe field.

## Frozen added-kernel result

For isotropic added Gaussian standard deviations

```text
[0, 0.5, 1, 2, 4] pixels
```

with reflect boundaries, ordinary map variance was

```text
[13.7373252, 11.3744081, 7.8299696, 4.3497793, 1.5443547] nm^2.
```

The largest added kernel retained only `0.1124203` of the unsmoothed map
variance. This is direct real-map evidence that reported spatial variance is
strongly measurement-scale dependent. Because the native instrument kernel is
unknown, the result is a scale-dependence demonstration rather than a physical
deconvolution.

## Covariance-family closure

Using the predeclared training scales and holding out the one-pixel added scale:

```text
family               training log RMS    held-out relative error
Gaussian             0.0330701           +13.5181%
Matern nu=1/2        0.0838957            -6.4781%
Matern nu=3/2        0.00998593           +4.8241%
Matern nu=5/2        0.0112856            +8.0179%
```

Matérn `nu=3/2` is the smallest-residual descriptive fit under the frozen primary
analysis. It is **not** selected as a material covariance law. The scales are
deterministic transforms of one map, the native kernel is unknown, and the
field-of-view and boundary sensitivities are larger than the differences among
the family fits.

The Gaussian reciprocal-linearity fit has maximum relative variance residual
`0.118631`, so the map does not satisfy exact Gaussian closure under the chosen
finite-map convention.

## Same-raster dependence

Under the fitted descriptive Gaussian field model, adjacent added-scale
variance estimators are extremely correlated:

```text
corr(s=0, s=0.5)   0.998303
corr(s=0.5, s=1)   0.989826
```

The model-conditioned moment-matched effective variance degrees of freedom fall
from `49.19` at the unsmoothed scale to `7.55` at the four-pixel scale, despite
there being 576 raster cells.

Relative to the false independent-pixel and independent-scale treatment, the
parameter covariance determinant is larger by `16.98x`. The individual
standard-deviation ratios are parameter dependent (`4.525` and `0.906`), so the
result must be reported as a full covariance change rather than as a universal
scalar uncertainty multiplier.

These quantities are exact Gaussian quadratic-form consequences conditional on
the fitted descriptive Gaussian model. They are not empirical repeat
covariance.

## Finite-field sensitivity

The largest variance-curve changes relative to the primary reflect convention
are:

```text
periodic versus reflect boundary        72.63%
nearest versus reflect boundary         37.71%
central 16 x 16 crop versus full field  72.74%
planar detrending versus primary        19.81%
```

This is the principal caution from the demonstration. On a finite 24 x 24 map,
field-of-view selection, boundary treatment, and low-order trend handling can
change the apparent multiscale variance more than the descriptive family
separation. A family claim from this map would therefore be unjustified.

## Phase-randomized control

The Fourier phase-randomized surrogate preserves the periodic smoothing curve
to a maximum relative residual of `2.53e-14`, as required by its preserved
discrete power spectrum. Its reflect-boundary curve differs from the source
map, showing that boundary interaction and spatial phase arrangement matter in
the finite nonperiodic analysis.

## Scientific consequence

The cross-material real-data demonstration establishes that the R04 software can
reproduce, on a public semiconductor map, the qualitative effects predicted by
the analytical program:

- apparent variance falls strongly with measurement scale;
- numerical scales from one raster are highly dependent;
- nominal pixel count is not the relevant information count;
- finite-map and boundary choices can dominate covariance-family diagnostics;
- a held-out numerical scale from the same raster is a closure check, not
  independent external validation.

It does not establish:

- HgCdTe experimental validation;
- a physical CdSeTe or HgCdTe correlation length;
- a universal Gaussian or Matérn covariance family;
- a composition field;
- empirical repeat covariance;
- R05 readiness;
- manuscript authorization.

## Program status

```text
R04 analytical and synthetic framework       complete at current scope
public-data recovery                          complete; HgCdTe package not found
cross-material real-data demonstration        complete, restricted
HgCdTe external validation                    blocked
new R04 mechanism                             not authorized
R05                                           inactive
manuscript                                    requires separate claim review
```
