# R04 protocol: external multiresolution validation-path qualification

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #250  
**Status:** source-readiness protocol; not specimen inference

## 1. Purpose

The R04 analytical chain can now propagate finite measurement kernels,
calibration covariance, covariance-family misspecification, nonlinear
observation operators, correlated raster sampling, and same-raster cross-scale
covariance. The remaining question is whether an external dataset contains the
information required to exercise that chain.

This protocol prevents three common substitutions:

```text
multiple modalities      != multiple effective probe scales
adjustable aperture      != same-region aperture sweep
rendered map figure      != reusable numerical map
```

A source can be scientifically relevant without qualifying for direct
multiresolution validation.

## 2. Direct-validation routes

A candidate can qualify through either of two routes.

### 2.1 Independent measured scales

The same specimen and spatial region are measured at three or more independently
characterized effective lateral scales.

The count is a count of distinct measurement kernels, not a count of modalities,
wavelength channels, temperatures, pixels, or repeated fits to one map.

### 2.2 Reusable high-resolution numerical map

One original numerical high-resolution map is available with coordinates and
calibration metadata. At least three declared kernels may be applied to that map
numerically.

This route is valid only when the map is an original numerical array. Rasterizing
or digitizing a rendered publication figure does not recreate the underlying
samples, noise covariance, dynamic range, or preprocessing history.

## 3. Common mandatory evidence

Both routes require all of the following.

1. **Specimen identity.** Every scale must refer to the same specimen.
2. **Spatial identity.** Every scale must observe the same registered region.
3. **Numerical data.** Original arrays or spectra with coordinates must be
   available.
4. **Kernel characterization.** The PSF, aperture, pixel, scan-bin, or equivalent
   kernel must be measured or reconstructable for every scale.
5. **Registration.** A common coordinate system or explicit registration
   transform must be available.
6. **Thickness and depth model.** Specimen thickness and depth weighting or
   absorption model must be declared whenever the observable is depth sensitive.
7. **Uncertainty.** Repeats, pointwise uncertainties, or a covariance model must
   support construction of observation covariance.
8. **Observable definition.** The reported quantity must be operationally
   defined.
9. **Preprocessing provenance.** Smoothing, fitting, interpolation, background
   removal, and edge conventions must be recorded.

The qualification test is conjunctive. One missing mandatory item prevents
direct validation.

## 4. Qualification classes

### 4.1 `direct_multiresolution_validation`

All common evidence is confirmed and one direct route is satisfied.

Permitted use:

- multiscale recovery and covariance-family closure testing;
- joint instrument, observation, finite-map, and cross-scale uncertainty
  propagation.

This class still does not establish a universal covariance family or eliminate
model dependence.

### 4.2 `single_scale_spatial_benchmark`

A numerical spatial map and its kernel are available at one effective scale.

Permitted use:

- one-scale forward prediction;
- finite-map bias and effective-information checks;
- preprocessing and observable-chain validation.

Prohibited use:

- separate recovery of point variance and correlation length;
- covariance-family closure testing from fewer than three scales.

### 4.3 `cross_modality_context`

Two or more modalities observe the same specimen region, but the evidence does
not supply three effective scales.

Permitted use:

- modality-conditioned forward-model comparisons;
- design of a future registered multimodal experiment.

Prohibited use:

- treating modality count as scale count;
- assuming that equal nominal pixel pitch implies equal measurement kernels.

### 4.4 `source_bounded_figure_benchmark`

A spatial figure or published summary statistics are available, but original
numerical arrays or required kernel metadata are not.

Permitted use:

- claim-level source audit;
- explicitly bounded figure-recoverability studies;
- qualitative map-structure comparison.

Prohibited use:

- representing digitized pixels as original source data;
- direct multiresolution parameter inference.

### 4.5 `not_qualifiable_from_available_record`

The accessible record does not establish enough evidence even for a controlled
quantitative benchmark. Unknown and not-retrieved states remain explicit rather
than being replaced by assumptions.

## 5. Deterministic decision rule

Let `R_common` denote confirmation of all nine common requirements. Let
`N_scale` be the number of independently characterized measured scales, and let
`N_filter` be the number of declared kernels applicable to a reusable numerical
high-resolution map.

Direct qualification is

```text
R_common
and
(
    N_scale >= 3
    or
    (reusable_numerical_map and N_filter >= 3)
).
```

No weighted score can compensate for a failed mandatory requirement. This is a
readiness decision, not a ranking exercise.

## 6. Current candidate disposition

### 6.1 Chang et al. 2005

The audited source establishes finite-aperture infrared transmission mapping and
reports an adjustable aperture down to approximately 25 micrometres at a
10-micrometre wavelength. The published large-area maps used a 100-micrometre
aperture.

The accessible record does not provide the same registered region at multiple
apertures, a measured wavelength-dependent PSF, original numerical map arrays,
repeat covariance, or variance versus scale.

Classification:

```text
source_bounded_figure_benchmark
```

### 6.2 Furstenberg, White, and Olson 2005

The audited source reports PL and transmission maps from the same region at a
representative 25-micrometre resolution. It also records important
modality-specific ambiguities.

The two modalities do not constitute two effective lateral scales, and the
accessible record does not provide a spot-size sweep, measured excitation and
collection kernels, original registered arrays, or variance versus scale.

Classification:

```text
cross_modality_context
```

### 6.3 Ruzhevich et al. 2024

The official abstract reports transmission, PL, SEM, and EDX and describes
large-scale composition fluctuations in one composition regime. The full text
was not retrieved by the bounded audit.

The accessible record does not establish spatial registration, calibrated scale
count, original numerical maps, PSF metadata, uncertainty covariance, or a
correlation-length statistic.

Classification:

```text
not_qualifiable_from_available_record
```

This is an access-bounded state. It is not negative evidence about what the full
article may contain.

## 7. Portfolio decision

No currently audited candidate satisfies the direct-validation rule.

```text
portfolio status = external_data_blocked
```

This means the theory is not externally testable from the currently available
records. It does not mean the theory failed.

## 8. Minimum author-data or experimental request

The next valid package must provide:

1. an original numerical map or spectra with physical coordinates;
2. the same registered region at three calibrated effective scales, or one
   high-resolution numerical map reusable under three declared kernels;
3. measured or reconstructable PSF, aperture, pixel, and scan-bin kernels;
4. a registration transform;
5. specimen thickness and the depth-weighting or absorption model;
6. repeat information, pointwise uncertainty, or full observation covariance;
7. the exact observable definition and preprocessing chain.

A planned experiment should additionally record raster geometry and cross-scale
sampling relationships so the merged finite-map and same-raster covariance
results can be applied.

## 9. Claim restrictions

This protocol does not establish:

- a specimen point variance or correlation length;
- a covariance family;
- that an optical map equals microscopic composition;
- that a rendered figure is a numerical dataset;
- that multiple modalities are independent scales;
- novelty or manuscript authorization.
