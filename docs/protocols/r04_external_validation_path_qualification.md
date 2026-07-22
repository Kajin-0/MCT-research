# R04 protocol: external multiresolution validation-path qualification

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #196, #250, #272  
**Status:** source-readiness protocol; not specimen inference

## 1. Purpose

The R04 analytical chain can propagate finite measurement kernels, calibration covariance, covariance-family misspecification, nonlinear observation operators, correlated raster sampling, and same-raster cross-scale covariance. The remaining question is whether an external dataset contains the information required to exercise that chain.

This protocol prevents four common substitutions:

```text
multiple modalities      != multiple effective probe scales
adjustable aperture      != same-region aperture sweep
rendered map figure      != reusable numerical map
nominal beam diameter    != measured point-spread function
```

A source can provide meaningful partial evidence without qualifying for direct multiresolution validation.

## 2. Direct-validation routes

A candidate can qualify through either of two routes.

### 2.1 Independent measured scales

The same specimen and spatial region are measured at three or more independently characterized effective lateral scales.

The count is a count of distinct measurement kernels, not a count of modalities, wavelength channels, temperatures, pixels, or repeated fits to one map.

### 2.2 Reusable high-resolution numerical map

One original numerical high-resolution map is available with coordinates and calibration metadata. At least three declared kernels may be applied to that map numerically.

Rasterizing or digitizing a rendered publication figure does not recreate the underlying samples, noise covariance, dynamic range, or preprocessing history.

## 3. Common mandatory evidence

Both direct routes require all of the following:

1. **Specimen identity.** Every scale refers to the same specimen.
2. **Spatial identity.** Every scale observes the same registered region.
3. **Numerical data.** Original arrays or spectra with coordinates are available.
4. **Kernel characterization.** The PSF, aperture, pixel, scan-bin, or equivalent kernel is measured or reconstructable for every scale.
5. **Registration.** A common coordinate system or explicit transform is available.
6. **Thickness and depth model.** Thickness and depth weighting or absorption are declared whenever the observable is depth sensitive.
7. **Uncertainty.** Repeats, pointwise uncertainty, or a covariance model support construction of observation covariance.
8. **Observable definition.** The reported quantity is operationally defined.
9. **Preprocessing provenance.** Smoothing, fitting, interpolation, background removal, and edge conventions are recorded.

The qualification test is conjunctive. One missing mandatory item prevents direct validation.

## 4. Qualification classes

### 4.1 `direct_multiresolution_validation`

All common evidence is confirmed and one direct route is satisfied.

Permitted:

- multiscale recovery and covariance-family closure testing;
- joint instrument, observation, finite-map, and cross-scale uncertainty propagation.

This class still does not establish a universal covariance family or eliminate model dependence.

### 4.2 `partial_multiresolution_benchmark`

The same specimen is reported at two or more effective scales, but one or more direct requirements are missing.

This class is appropriate for sources such as two rendered same-specimen spectra at distinct nominal beam diameters.

Permitted:

- establish source-bounded qualitative dependence on measurement scale;
- identify whether the reported direction of change is consistent with a finite-kernel premise;
- define the missing third scale, kernel calibration, uncertainty, and registration requirements.

Prohibited:

- three-scale covariance-family closure;
- specimen covariance recovery from rendered curves;
- treating two scales as direct validation;
- replacing a measured PSF with nominal beam diameter.

### 4.3 `single_scale_spatial_benchmark`

A numerical spatial map and its kernel are available at one effective scale.

Permitted:

- one-scale forward prediction;
- finite-map bias and effective-information checks;
- preprocessing and observable-chain validation.

Prohibited:

- separate recovery of point variance and correlation length;
- covariance-family closure from fewer than three scales.

### 4.4 `cross_modality_context`

Two or more modalities observe the same specimen region, but the evidence does not supply three effective scales.

Permitted:

- modality-conditioned forward-model comparisons;
- design of a future registered multimodal experiment.

Prohibited:

- treating modality count as scale count;
- assuming equal nominal pixel pitch implies equal measurement kernels.

### 4.5 `source_bounded_figure_benchmark`

A spatial figure or published summary statistics are available, but original numerical arrays or required kernel metadata are not.

Permitted:

- claim-level source audit;
- explicitly bounded figure-recoverability studies;
- qualitative map-structure comparison.

Prohibited:

- representing digitized pixels as original source data;
- direct multiresolution parameter inference.

### 4.6 `not_qualifiable_from_available_record`

The accessible record does not establish enough evidence even for a controlled quantitative spatial benchmark. Unknown and not-retrieved states remain explicit rather than being replaced by assumptions.

## 5. Deterministic decision rule

Let `R_common` denote confirmation of all nine common requirements. Let `N_scale` be the number of independently characterized measured scales, and `N_filter` the number of declared kernels applicable to a reusable numerical high-resolution map.

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

Partial multiresolution qualification requires:

```text
same specimen confirmed
and
N_scale >= 2
and
(numerical data or a rendered scale-comparison figure available)
and
not direct-validation ready.
```

No weighted score can compensate for a failed mandatory requirement. This is a readiness decision, not a ranking exercise.

## 6. Current candidate disposition

| Source | Key evidence | Qualification |
|---|---|---|
| Gopal et al. 1992 | Same sample measured with nominal 3 mm and 250 micrometre beams; scale-dependent shift for sample 90239 and no noticeable shift for control sample 90211 | `partial_multiresolution_benchmark` |
| Chang et al. 2005 | Adjustable aperture, but published maps use one 100 micrometre setting | `source_bounded_figure_benchmark` |
| Furstenberg et al. 2005 | Same-region PL and transmission at representative 25 micrometre resolution | `cross_modality_context` |
| Murakami et al. 1992 | Rendered EPMA wafer-position profiles | `source_bounded_figure_benchmark` |
| Parikh et al. 1996 | Rendered 15 by 15 mm composition map and summary statistics | `source_bounded_figure_benchmark` |
| Feldman et al. 1991 | TEM chemical mapping of vertical MQW interfaces | `source_bounded_figure_benchmark` |
| Aoki et al. 2004 | HREM and Z-contrast interface-width figures | `source_bounded_figure_benchmark` |
| Oda et al. 1992 | FTIR, EPMA, and detector-response method comparison without registered maps | `not_qualifiable_from_available_record` |
| Jeoung et al. 1996 | Bulk transmission composition calibration without spatial mapping | `not_qualifiable_from_available_record` |
| Ruzhevich et al. 2024 | Abstract-level multimodal record; full text not retrieved | `not_qualifiable_from_available_record` |

Detailed evidence is recorded in `literature/notes/uploaded_hgcdte_mapping_source_audit.md` and the immutable validation record.

## 7. Gopal 1992 boundary

The Gopal source changes the nearest external benchmark because it contains genuine scale variation of one observable on one HgCdTe specimen.

Reported nominal beam diameters:

```text
wide beam       3000 micrometres
focused beam     250 micrometres
ratio              12
```

The source is still not direct validation because it lacks:

- original numerical spectra;
- a third scale;
- measured PSFs;
- registered beam-center coordinates;
- repeat uncertainty or covariance;
- complete sample-specific thickness and depth metadata.

The rendered curves must not be digitized and treated as original experimental arrays.

## 8. Portfolio decision

No current candidate satisfies the direct-validation rule.

```text
partial multiresolution candidates = 1
direct validation candidates       = 0
portfolio status                    = external_data_blocked
```

This means the theory is not directly externally testable from the currently available records. It does not mean the theory failed.

## 9. Minimum data upgrade

The next valid package must provide:

1. original numerical maps or spectra with physical coordinates;
2. the same registered region at three calibrated effective scales, or one high-resolution numerical map reusable under three declared kernels;
3. measured or reconstructable PSF, aperture, pixel, and scan-bin kernels;
4. a registration transform;
5. specimen thickness and the depth-weighting or absorption model;
6. repeat information, pointwise uncertainty, or full observation covariance;
7. the exact observable definition and preprocessing chain.

For Gopal sample 90239, the specific upgrade is:

- original wide- and focused-beam spectra;
- beam-center coordinates;
- measured aperture/PSF descriptions;
- sample thickness and depth model;
- repeat uncertainty;
- one additional calibrated beam size.

## 10. Claim restrictions

This protocol does not establish:

- a specimen point variance or correlation length;
- a covariance family;
- that an optical map equals microscopic composition;
- that a rendered figure is a numerical dataset;
- that multiple modalities are independent scales;
- that two scales are sufficient for family closure;
- that nominal beam diameter is a Gaussian standard deviation;
- novelty or manuscript authorization.
