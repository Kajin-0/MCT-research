# R04 HgCdTe spatial-mapping and observation-model retrieval queue

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issues:** #281, #291  
**Constraint:** paper retrieval only; no experiments and no author contact

## Search objective

Locate published records that can upgrade R04 external evidence through at least one of the following:

1. the same registered HgCdTe region measured at three calibrated effective probe scales;
2. an original numerical high-resolution spatial map reusable under declared kernels;
3. machine-readable spectra or maps with coordinates, acquisition order, instrument kernel, and uncertainty;
4. a repeat of Gopal-style wide/focused transmission measurements with a third aperture;
5. a Phillips-style dense raster with downloadable arrays and a measured PSF;
6. a depth-resolved observation model that prevents through-thickness grading from being misidentified as lateral disorder.

A paper is not high priority merely because it reports “uniformity” or “band-gap variation.” Priority depends on whether its measurement geometry or observation operator changes the identifiability state.

## A. Audited anchor sources

### `10.1063/1.1625776`

**Phillips et al. 2003 — Uniformity of optical absorption in HgCdTe epilayer measured by infrared spectromicroscopy**

**Audit result:** nearest detector-pixel-scale spatial absorption benchmark.

```text
beam diameter                 approximately 9 micrometres
scan spacing                  10 micrometres
area map                      200 by 200 micrometres
reported spectra              400
effective lateral scales      1
qualification                 source_bounded_figure_benchmark
```

Continue citation chaining for original arrays, acquisition-order metadata, source-drift corrections, and repeated maps at other apertures.

### `10.1063/1.113916`

**Ariel et al. 1995 — Estimation of HgCdTe band-gap variations by differentiation of the absorption coefficient**

**Audit result:** depth-observation-model context, not lateral mapping evidence.

The full text reports room-temperature FTIR transmission, absorption extraction, smoothing, and first/second differentiation. It estimates average gap and through-thickness `Delta Eg` under a linearly graded `Eg(z)` model.

It does not report:

- different wafer positions;
- lateral coordinates or a raster;
- beam diameter, aperture, or PSF;
- multiple effective lateral scales;
- numerical spectra or derivative arrays;
- repeats or uncertainty covariance.

The earlier queue description anticipating measurements at different wafer positions is withdrawn.

```text
qualification                 depth_observation_model_context
lateral effective scales      1
portfolio effect              model discipline only
validation status             unchanged
```

Use this source to constrain depth averaging, smoothing sensitivity, and interface-grading confounds. Do not use its `Delta Eg` as lateral spatial variance.

## B. Priority 1 — retrieve next

### `10.1088/0268-1242/8/6S/006`

**Price and Boyd — Overview of compositional measurement techniques for HgCdTe with emphasis on IR transmission, energy-dispersive X-ray analysis and optical reflectance**

Why first: Ariel 1995 cites this review as the principal survey of HgCdTe composition and band-gap methods. It may expose older primary sources with explicit aperture, interaction-volume, lateral-resolution, and precision records.

Extract:

- every cited same-region beam-size comparison;
- aperture and interaction-volume definitions;
- reported precision versus spatial resolution;
- distinctions between lateral variation and depth grading;
- references to original mapping arrays or wafer-uniformity data.

### `10.1117/12.452272`

**Chu et al. 2002 — Optical and electronic characterization on HgCdTe materials**

Why high priority: the record describes thermal imaging of composition distributions and multiple optical characterization methods.

Check for:

- raster dimensions and physical coordinates;
- detector-pixel-scale maps;
- numerical composition distributions;
- aperture, PSF, or pixel integration;
- same-region measurements at multiple resolutions;
- downloadable or tabulated arrays.

### Exact-title unresolved DOI

**Monitoring HgCdTe layer uniformity by the differential absorption technique**

- Authors: V. Ariel, V. Garber, G. Bahir, S. Krishnamurthy, A. Sher
- Journal: Applied Physics Letters
- Volume/pages/year: 69, 1864-1866 (1996)

This is now the highest-priority direct descendant of Ariel 1995 because its title explicitly claims layer-uniformity monitoring.

Evidence target:

- whether multiple wafer positions were actually measured;
- lateral versus transverse band-gap fluctuations;
- aperture or spot size;
- map geometry and registration;
- reported method accuracy;
- original spectra or numerical position records.

Do not guess its DOI. Resolve it from exact bibliographic metadata.

## C. Priority 2 — observation-model and nonuniformity methods

### `10.1016/0020-0891(93)90037-8`

**Gopal, Ashokan, and Gupta 1993 — A general optical characterization method for determining the composition of Hg1-xCdxTe samples**

Look for extensions of the 1992 two-beam argument, additional spot sizes, or explicit lateral/depth separation.

### `10.1063/1.356464`

**Empirical rule of intrinsic absorption spectroscopy in Hg1-xCdxTe**

Look for aperture dependence, spatial-averaging assumptions, and error propagation from thickness or absorption-edge fitting into inferred composition.

### `10.1063/1.122377`

**Spectra analysis of annealed HgCdTe MBE films**

Look for pre/post-anneal spatial maps, changes in lateral variance, or numerical transmission spectra useful for testing the nonlinear observation model.

### `10.1007/BF02653091`

**Compositionally graded HgCdTe photodiodes: prediction of spectral response from transmission spectrum and the impact of grading**

Look for depth-profile parameterization, transmission-to-device cross-modality constraints, and whether multiple lateral positions were measured.

### Exact-title unresolved DOI

**Measurement of composition in Hg1-xCdxTe epilayers**

- Authors: K. Liu, J. Chu, B. Li, D. Tang
- Journal: Applied Physics Letters
- Volume/page/year: 64, 2818 (1994)

Evidence target: whether composition was mapped spatially, beam diameter, specimen registration, and numerical spectra.

### Exact-title unresolved DOI

**Study on the composition profile of a Hg1-xCdxTe epitaxy film by infrared transmission spectroscopy**

- Authors: B. Li, J. Chu, K. Liu, D. Tang
- Journal: Journal of Physics: Condensed Matter
- Year: 1995

Evidence target: lateral versus depth-profile separation, number of positions, aperture, and whether a full profile or only fitted coefficients is published.

## D. Priority 3 — multilayer and calibration context

### `10.1063/1.118710`

**Differential absorption characterization of multilayer HgCdTe structures**

Look for explicit limitations of derivative absorption under multiple layers, interface regions, and whether the method was applied spatially.

### `10.1007/s11664-005-0017-5`

**Improved model for the analysis of FTIR transmission spectra from multilayer HgCdTe structures**

Look for downloadable spectra, uncertainty propagation, and parameters needed to separate lateral field variation from depth-profile effects.

## E. Retrieval triage checklist

For each located paper, record before deeper analysis:

```text
same specimen across scales?                  yes / no / unknown
same registered region?                       yes / no / unknown
number of distinct effective kernels          integer
original numerical arrays available?          yes / no / unknown
physical coordinates and acquisition order?   yes / no / unknown
measured or reconstructable PSF?               yes / no / unknown
thickness and depth model?                     yes / no / unknown
repeat uncertainty or covariance?              yes / no / unknown
observable and preprocessing chain?            yes / no / unknown
depth grading separable from lateral effects?  yes / no / unknown
```

Stop early when a source is clearly another single rendered uniformity figure with no arrays or kernel metadata. Continue deeply when it contains a third scale, downloadable data, an explicit aperture sweep, a reusable numerical raster, or a well-declared depth operator that changes the nuisance model.

## F. Current decision boundary

The queue is a retrieval plan, not evidence. A bibliographic record does not change R04 status until its contents are audited.

```text
nearest partial multiresolution source       Gopal 1992
nearest detector-pixel-scale source          Phillips 2003
nearest depth-observation-model context      Ariel 1995
direct validation candidates                 0
portfolio status                             external_data_blocked
```
