# R04 HgCdTe spatial-mapping DOI retrieval queue

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issue:** #281  
**Constraint:** paper retrieval only; no experiments and no author contact

## Search objective

Locate published records that can upgrade R04 external evidence through at least one of the following:

1. the same registered HgCdTe region measured at three calibrated effective probe scales;
2. an original numerical high-resolution spatial map reusable under declared kernels;
3. machine-readable spectra or maps with coordinates, acquisition order, instrument kernel, and uncertainty;
4. a repeat of Gopal-style wide/focused transmission measurements with a third aperture;
5. a Phillips-style dense raster with downloadable arrays and a measured PSF.

A paper is not high priority merely because it reports “uniformity.” Priority depends on whether its measurement geometry changes the identifiability state.

## A. Verified DOI queue

### Priority 1 — retrieve first

#### `10.1063/1.1625776`

**Phillips et al. 2003 — Uniformity of optical absorption in HgCdTe epilayer measured by infrared spectromicroscopy**

Already audited from open full text. Retain as the anchor for citation chaining and supplementary-data searches.

Look for:

- later papers using the same infrared spectromicroscope;
- theses or conference papers exposing the 400-spectrum array;
- repeated maps at other apertures or numerical apertures;
- acquisition-order and source-drift corrections.

#### `10.1063/1.113916`

**Ariel et al. 1995 — Estimation of HgCdTe band-gap variations by differentiation of the absorption coefficient**

Why high priority: differential absorption was applied at different wafer positions and was intended to expose band-gap variations. Determine whether the full paper provides spatial coordinates, aperture size, repeated measurements, or quantitative lateral fluctuation statistics.

#### `10.1088/0268-1242/8/6S/006`

**Price and Boyd — Overview of compositional measurement techniques for HgCdTe with emphasis on IR transmission, energy-dispersive X-ray analysis and optical reflectance**

Why high priority: this review should consolidate older spatial-resolution limits, calibration equations, and primary references that are not discoverable by title search alone.

Extract:

- every cited same-region beam-size comparison;
- aperture and interaction-volume definitions;
- reported precision versus spatial resolution;
- references to raw mapping or wafer-uniformity data.

#### `10.1117/12.452272`

**Chu et al. 2002 — Optical and electronic characterization on HgCdTe materials**

Why high priority: the record describes thermal imaging of composition distributions and multiple optical characterization methods. Check whether the paper reports raster dimensions, detector-pixel-scale maps, or numerical composition distributions.

### Priority 2 — observation-model and nonuniformity methods

#### `10.1016/0020-0891(93)90037-8`

**Gopal, Ashokan, and Gupta 1993 — A general optical characterization method for determining the composition of Hg1-xCdxTe samples**

Look for extensions of the 1992 two-beam argument, additional spot sizes, or explicit lateral/depth separation.

#### `10.1063/1.356464`

**Empirical rule of intrinsic absorption spectroscopy in Hg1-xCdxTe**

Look for aperture dependence, spatial-averaging assumptions, and error propagation from thickness or absorption-edge fitting into inferred composition.

#### `10.1063/1.122377`

**Spectra analysis of annealed HgCdTe MBE films**

Look for pre/post-anneal spatial maps, changes in lateral variance, or numerical transmission spectra useful for testing the nonlinear observation model.

#### `10.1007/BF02653091`

**Compositionally graded HgCdTe photodiodes: prediction of spectral response from transmission spectrum and the impact of grading**

Look for depth-profile parameterization, transmission-to-device cross-modality constraints, and whether multiple lateral positions were measured.

### Priority 3 — broader calibration and multilayer context

#### `10.1063/1.118710`

**Differential absorption characterization of multilayer HgCdTe structures**

Look for explicit limitations of differential absorption under multiple layers and whether the method was applied spatially.

#### `10.1007/s11664-005-0017-5`

**Improved model for the analysis of FTIR transmission spectra from multilayer HgCdTe structures**

Look for downloadable spectra, uncertainty propagation, and model parameters needed to separate lateral field variation from depth-profile effects.

## B. Bibliographically confirmed leads with DOI still unresolved

Do not guess DOI values for these records. Search by exact title, author list, journal, volume, and first page.

### Monitoring HgCdTe layer uniformity by the differential absorption technique

- Authors: V. Ariel, V. Garber, G. Bahir, S. Krishnamurthy, A. Sher
- Journal: Applied Physics Letters
- Volume/page/year: 69, 1864-1866 (1996)

Evidence target: multiple wafer positions, lateral and transverse band-gap fluctuations, aperture size, map geometry, and reported method accuracy.

### Measurement of composition in Hg1-xCdxTe epilayers

- Authors: K. Liu, J. Chu, B. Li, D. Tang
- Journal: Applied Physics Letters
- Volume/page/year: 64, 2818 (1994)

Evidence target: whether composition was mapped spatially, beam diameter, specimen registration, and numerical spectra.

### Study on the composition profile of a Hg1-xCdxTe epitaxy film by infrared transmission spectroscopy

- Authors: B. Li, J. Chu, K. Liu, D. Tang
- Journal: Journal of Physics: Condensed Matter
- Year: 1995

Evidence target: lateral versus depth-profile separation, number of positions, aperture, and whether a full profile or only fitted coefficients is published.

## C. Retrieval triage checklist

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
```

Stop early when a source is clearly another single rendered uniformity map with no arrays or kernel metadata. Continue deeply when it contains a third scale, downloadable data, an explicit aperture sweep, or a reusable numerical raster.

## D. Current decision boundary

The DOI queue is a retrieval plan, not evidence. A bibliographic record does not change R04 status until its contents are audited.

```text
nearest partial multiresolution source = Gopal 1992
nearest detector-pixel-scale source    = Phillips 2003
direct validation candidates           = 0
portfolio status                        = external_data_blocked
```
