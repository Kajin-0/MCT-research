# Uploaded HgCdTe spatial-source audit

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issue:** #272  
**Status:** full-text source audit; external benchmark strengthened, direct validation still blocked

## 1. Scope

Nine user-supplied full-text PDFs were reviewed against the R04 validation-path protocol. The audit asks whether each source provides:

1. genuine variation of measurement scale on the same specimen;
2. original numerical arrays or spectra;
3. measured or reconstructable kernels;
4. spatial registration;
5. thickness and depth-model metadata;
6. uncertainty or covariance information;
7. enough scales to test covariance-family closure.

Rendered figures are treated as source evidence, not as raw numerical data. No figure is digitized into a purported experimental dataset.

## 2. Decision-changing source: Gopal et al. 1992

**DOI:** `10.1016/0020-0891(92)90053-V`

Gopal, Ashokan, and Dhar explicitly compare transmission spectra measured with wide and focused incident IR beams.

### 2.1 Uniform control specimen

For sample 90211, the authors report no noticeable change when the incident beam diameter is varied from `3 mm` to `250 micrometres`. They interpret this as evidence that the epilayer is laterally uniform at the sensitivity of the comparison.

The same specimen was also etched from `22 micrometres` to `14 micrometres`, supplying a separate thickness-direction check. That etch comparison is not an additional lateral probe scale.

### 2.2 Nonuniform specimen

For sample 90239, the paper reports spectra measured with nominal beam diameters of:

```text
wide beam       3 mm
focused beam    250 micrometres
scale ratio     12
```

Figure 6 shows a relative shift of the two measured transmission curves. The authors identify the shift itself as the first indication of lateral composition nonuniformity. Their subsequent disagreement between compositions inferred from the `Z_1/2` and zero-intercept conventions is used as evidence that the specimen also contains depth nonuniformity.

### 2.3 R04 significance

This is the closest source found to the R04 scale-dependence premise:

```text
same HgCdTe specimen
+ same observable
+ two nominal lateral beam sizes
+ reported resolution-dependent edge shift
```

It is stronger than an adjustable-aperture statement or a multimodal comparison at one resolution.

### 2.4 Why it is not direct validation

The source does not provide:

- a third effective scale;
- original numerical spectral arrays;
- coordinates proving the same sampled center or region;
- a measured optical PSF or aperture-transfer kernel;
- repeat measurements or observation covariance;
- a reported thickness for sample 90239;
- a sample-specific depth profile;
- a variance-versus-scale curve;
- a spatial raster or cross-scale registration record.

Two curves can establish qualitative scale dependence. They cannot test the Gaussian reciprocal-linearity closure or distinguish covariance families. The nominal beam diameters also cannot be substituted for calibrated Gaussian widths without an optical model.

**Classification:**

```text
partial_multiresolution_benchmark
```

## 3. Chang et al. 2005

**DOI:** `10.1016/j.jcrysgro.2005.01.051`

The source reports an infrared microscope with an aperture adjustable down to approximately `25 micrometres` at `10 micrometres` wavelength. The published large-area composition and thickness maps used a `100 micrometre` aperture for signal and acquisition-time reasons.

The paper provides rendered maps and summary statistics but no same-region aperture sweep, original numerical arrays, measured wavelength-dependent PSF, repeat covariance, or variance-versus-scale curve.

**Classification:**

```text
source_bounded_figure_benchmark
```

## 4. Furstenberg, White, and Olson 2005

**DOI:** `10.1007/s11664-005-0022-8`

The paper reports same-location PL and transmission mapping, normally at `25 micrometre` spatial resolution. The highest attainable resolution is stated as approximately `10 micrometres`, but the published maps do not constitute a registered resolution sweep.

The source is particularly important for observation-operator boundaries:

- PL depends on excitation intensity and collection efficiency;
- focused excitation broadens PL;
- transmission-derived optical path can reflect thickness, composition, or inclusions;
- PL and transmission features correlate only in some regions.

Two modalities and two temperatures at one nominal map resolution are not multiple effective scales.

**Classification:**

```text
cross_modality_context
```

## 5. Oda et al. 1992

**DOI:** `10.1016/0022-0248(92)90743-3`

The source compares:

```text
FTIR transmission       nominal 500 micrometre beam
EPMA-WDX                nominal 1-2 micrometre interaction region
photodiode response     77 K device spectral response
```

It reports method agreement near `plus or minus 0.002` for the preferred composition convention. These measurements do not form registered maps of the same spatial region. Their different interaction volumes therefore cannot be treated as a probe-size sweep.

**Classification:**

```text
not_qualifiable_from_available_record
```

Permitted use is composition-method and observation-scale context only.

## 6. Gopal-related transmission calibration: Jeoung et al. 1996

**DOI:** `10.1016/1350-4495(95)00125-5`

Jeoung et al. calibrate bulk HgCdTe composition from the wavenumber at `50 percent` of maximum transmission and sample thickness. The paper reports agreement near `plus or minus 0.002` over the declared composition range and includes measured spectra for multiple bulk specimens.

It does not report a spatial map, registered scale sweep, or spatial covariance statistic.

**Classification:**

```text
not_qualifiable_from_available_record
```

Its value is in the transmission observation model and edge-convention history.

## 7. Murakami et al. 1992

**DOI:** `10.1016/0022-0248(92)90712-R`

The source presents EPMA composition profiles versus wafer position for different MOCVD nozzle and susceptor-rotation configurations. The line profiles show deterministic large-scale composition gradients and support a growth-flow model. The source states EPMA composition accuracy within approximately `5 percent` and shows representative profiles for a roughly `7 micrometre` layer.

The figures are not original arrays and the EPMA interaction kernel, sampling coordinates, repeats, and covariance are not supplied.

**Classification:**

```text
source_bounded_figure_benchmark
```

## 8. Parikh et al. 1996

**DOI:** `10.1016/0022-0248(95)00846-2`

The paper includes a rendered spatial composition map over a `15 by 15 mm` sample. It reports:

```text
mean x                         approximately 0.2270
sample-map standard deviation approximately 0.00053 across several samples
mean thickness                 approximately 7.85 micrometres
```

SIMS supplies vertical-profile context. The lateral FTIR beam size, raster coordinates, original map, and within-map covariance are not supplied.

**Classification:**

```text
source_bounded_figure_benchmark
```

## 9. Feldman et al. 1991

**DOI:** `10.1557/PROC-216-113`

The paper reports quantitative TEM chemical mapping of HgCdTe/CdTe multiple quantum wells and annealing-dependent interdiffusion. It concerns nanoscale vertical interfaces rather than a lateral alloy map or lateral probe-size sweep.

**Classification:**

```text
source_bounded_figure_benchmark
```

This source can inform microscopic interface and depth-disorder context, but not the current lateral covariance inverse.

## 10. Aoki et al. 2004

**DOI:** `10.1017/S1431927604882175`

HREM and Z-contrast measurements report interface-transition widths of approximately:

```text
as grown                 15.4-15.7 angstrom
250 C, 30 minute anneal  24.1-24.7 angstrom
```

The evidence concerns superlattice-interface degradation and annealing, not a lateral same-region multiresolution map.

**Classification:**

```text
source_bounded_figure_benchmark
```

## 11. Portfolio conclusion

The new source set changes the nearest benchmark but not the external readiness state.

```text
nearest scale-dependent source   Gopal et al. 1992
partial multiresolution sources  1
direct validation sources        0
portfolio status                 external_data_blocked
```

The external claim can now be stated more strongly and precisely:

> Resolution-dependent HgCdTe transmission behavior has been reported on the same specimen using two nominal beam diameters, but the available record does not contain the numerical, kernel, uncertainty, registration, and third-scale information required to recover or falsify a covariance model.

## 12. Minimum useful next source

A paper or supplement becomes decision-changing if it supplies either:

1. the same registered region at three calibrated effective scales with original spectra or maps; or
2. one original numerical high-resolution map with coordinates and sufficient metadata to apply three declared kernels.

For the Gopal specimen specifically, the minimum upgrade would be:

- original wide- and focused-beam spectra;
- beam-center coordinates;
- measured aperture/PSF descriptions;
- sample 90239 thickness and depth model;
- repeat uncertainty;
- one additional calibrated beam size.

## 13. Claim restrictions

This audit does not support:

- digitizing the rendered Gopal curves as original experimental data;
- inferring a correlation length from the two beam diameters;
- treating nominal beam diameter as Gaussian kernel standard deviation;
- assigning a covariance family;
- treating FTIR/EPMA/PL modality differences as a scale sweep;
- manuscript authorization or a positive novelty claim.
