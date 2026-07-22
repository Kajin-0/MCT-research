# R04 source audit: Phillips et al. 2003 pixel-scale absorption mapping

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issue:** #281  
**Source:** J. D. Phillips, K. Moazzami, J. Kim, D. D. Edwall, D. L. Lee, and J. M. Arias, *Uniformity of Optical Absorption in HgCdTe Epilayer Measured by Infrared Spectromicroscopy*, Applied Physics Letters 83, 3701-3703 (2003).  
**DOI:** `10.1063/1.1625776`  
**Access state:** open full text audited through the University of Michigan repository  
**Qualification:** `source_bounded_figure_benchmark`

## 1. Why this source matters

This source is the closest published HgCdTe benchmark found so far to detector-pixel-scale spatial absorption characterization. It resolves the lateral field at approximately the dimensions of individual infrared detector elements rather than only reporting wafer-scale averages.

It does not vary the measurement kernel. It therefore complements, rather than replaces, Gopal et al. 1992:

```text
Gopal 1992     two nominal probe diameters, rendered spectra, no raster arrays
Phillips 2003  dense raster at one approximately 9 micrometre probe diameter
```

Gopal remains the nearest partial multiresolution benchmark. Phillips becomes the nearest detector-pixel-scale spatial benchmark.

## 2. Measurement record

The article reports an infrared spectromicroscopy system with a measured beam diameter of approximately **9 micrometres**. Spectra were acquired with **10 micrometre scan spacing**.

The published spatial records include:

- a line scan over approximately **2 mm**;
- a **200 by 200 micrometre** area map;
- **400 measured spectra** in that area map;
- rendered maps and histograms of absorption and inferred material quantities.

The article reports that the area-map dimensions are representative of typical infrared detector dimensions. The raster spacing is close to the reported beam diameter, so neighboring observations are not evidence of distinct probe kernels and should not be assumed independent without a sampling-covariance model.

## 3. Published source statistics

At a wavenumber of **1558 cm^-1**, the article reports:

```text
mean absorption coefficient       887 cm^-1
standard deviation                 24.6 cm^-1
relative standard deviation         2.8 percent
```

For composition extracted from the transmission model, it reports:

```text
mean x                             0.2256
standard deviation                 3.0e-4
```

These values are accepted only as source-published summary statistics. They are not reinterpreted as point-field covariance parameters.

## 4. Observable and inversion boundary

The measured quantity is a local infrared transmission spectrum. Absorption and composition are model-conditioned derived quantities.

The source explicitly warns that apparent composition variation can contain contributions from:

- epilayer thickness;
- alloy composition;
- absorption-coefficient variation;
- reflections at the sample interfaces;
- source or measurement drift.

The article notes that one apparent spatial trend may instead be temporal measurement drift. This is material to R04 because an unmodeled scan-time drift can be aliased into long-range spatial covariance.

## 5. Why 400 spectra remain one effective scale

The number of sampled positions and the number of measurement kernels are different quantities.

```text
sampled spectra                   400
reported effective probe scales    1
```

Moving one approximately 9 micrometre beam across 400 positions improves coverage of the filtered field. It does not create 400 independent resolutions. It also does not permit separation of point variance from correlation length without either additional calibrated kernels or an original reusable numerical map and a declared filtering protocol.

## 6. Missing evidence for direct R04 validation

The audited article record does not provide:

- machine-readable spectra or map arrays with physical coordinates;
- a full wavelength-dependent point-spread function;
- measurements of the same region at two additional effective scales;
- repeat measurements or observation covariance;
- a complete correction model for temporal source drift;
- cross-scale registration because no scale sweep was performed.

The published 9 micrometre diameter is useful instrument information but is not a complete PSF and must not be converted into a Gaussian standard deviation without an explicit optical model.

## 7. Permitted use

- detector-pixel-scale forward-model and sampling-design context;
- source-bounded comparison of published absorption and inferred-composition dispersion;
- identification of scan-drift and neighboring-pixel covariance requirements;
- design target for locating original numerical arrays or higher-resolution descendants.

## 8. Prohibited use

- digitizing the rendered maps and representing them as original measurements;
- treating 400 spectra as 400 effective probe scales or independent repeats;
- recovering specimen point variance, correlation length, or covariance family;
- claiming direct external validation of the R04 inverse;
- manuscript or novelty authorization.

## 9. Minimum data upgrade

A direct-use package based on this experiment would require:

1. original numerical spectra with physical coordinates and acquisition order;
2. measured or reconstructable wavelength-dependent PSF;
3. repeat or observation-covariance information;
4. at least two additional calibrated effective scales for covariance-family closure;
5. source-intensity and spatial-drift correction provenance;
6. specimen thickness and the exact transmission-to-absorption preprocessing chain.

## 10. Decision

Phillips et al. 2003 is accepted as the nearest detector-pixel-scale source-bounded HgCdTe absorption benchmark. It does not change the portfolio state:

```text
partial multiresolution candidates = 1
single-scale numerical candidates   = 0
source-bounded figure candidates    += 1
direct validation candidates        = 0
portfolio status                     = external_data_blocked
```
