# Bowman et al. 2024 CdSeTe open-data audit

## Decision

```text
RESTRICTED_GO
```

The public archive supplies source-data-derived numerical PL maps with physical
coordinate axes. It does not supply the raw per-pixel PL cube or a bounded native
sample-plane point-spread function. The data can therefore exercise R04's
same-raster numerical-kernel and finite-map machinery, but cannot establish a
latent physical correlation length or validate HgCdTe material covariance.

## Bibliographic record

```text
A. R. Bowman et al.
Spatially resolved photoluminescence analysis of the role of Se in
CdSe_xTe_1-x thin films
Nature Communications 15, 8729 (2024)
Article DOI 10.1038/s41467-024-52889-z
Dataset DOI 10.5281/zenodo.13869384
License CC BY 4.0
```

## Acquisition and archive integrity

The exact public `Datasets.zip` archive was downloaded by the Phase-1 workflow.

```text
Zenodo size          15.0 MB displayed
observed bytes       14969970
Zenodo MD5           1401ee9b5372edb78f888d152940fc79
observed MD5         1401ee9b5372edb78f888d152940fc79
observed SHA-256     cc3e1ce1a02266da2d0e0f301464a9d8a519855f33a597adeb7f16048684c9a6
archive members      61
uncompressed bytes   41274666
```

The archive contains 54 CSV files, five PNG files, one JPG file, and one
`Thumbs.db`. No nested archive, MATLAB container, HDF5 cube, TIFF stack, NPY/NPZ
array, executable code, or serialized scientific object is present.

## Article-defined PL observation contract

The article reports that PL and PLQY were measured on a Renishaw inVia Raman
microscope using 488 nm excitation. Maps were acquired by snake-scanning a
focused diffraction-limited spot while moving the sample on an MS20 stage with
real-time linear-encoder feedback. The PL collection objective was 100x with
NA 0.85. The article defines spot size using the `1/e^2` intensity boundary but
does not provide a measured numerical two-dimensional sample-plane PSF or a
numerical spot diameter for the admitted map.

For Figure 3, the article states that the peak wavelength was obtained by fitting
the PL data from each pixel with a Gaussian. The source archive publishes the
resulting peak-wavelength and PLQY maps, not the underlying spectrum at every
pixel or the fit covariance.

## Relevant source-data fields

The main-text source files include:

```text
Figure 3b.csv   0 nm CdSe, fitted PL peak-wavelength map
Figure 3c.csv   0 nm CdSe, central-region PLQY map
Figure 3e.csv   200 nm CdSe, fitted PL peak-wavelength map
Figure 3f.csv   200 nm CdSe, central-region PLQY map
Figure 4b.csv   0 nm CdSe, long/central normalized PLQY-ratio map
Figure 4d.csv   200 nm CdSe, long/central normalized PLQY-ratio map
```

Each Figure 3/4 numerical map is a complete `24 x 24` field with coordinate axes
in micrometres. The nominal spacing is approximately `0.54545 micrometre`, and
the axes extend from `0` to `12.545 micrometres`.

The supplementary source files include additional fitted peak-wavelength, PLQY,
temperature, and implied-voltage maps on the same map format, along with
spatially resolved absorption tables and large two-dimensional optical source
data. They do not repair the missing native PL spectra, PSF, repeats, or fit
uncertainty.

## Primary-field freeze

Before evaluating any multiscale residual, Phase 2 fixes:

```text
path           Datasets/Figure 3e.csv
article panel  Figure 3e
sample         Cl-treated film fabricated with a 200 nm CdSe underlayer
observable     Gaussian-fitted PL peak wavelength
units          nm
shape          24 x 24
x range        0 to 12.545 micrometres
y range        0 to 12.545 micrometres
missing        0
value range    837.0 to 862.5 nm
```

Selection is based on source completeness and the article's explicit observation
operator, not on a covariance-family residual. The field remains a PL
peak-wavelength observation. Although the article interprets the 200 nm map as
evidence of lower local bandgaps near grain boundaries, R04 does not relabel it
as an alloy-composition field.

## Missing mandatory fields

```text
raw spectrum at every primary-map pixel                  absent
raw interferograms                                       absent
per-pixel Gaussian-fit covariance                        absent
measured native two-dimensional excitation PSF           absent
collection PSF                                            absent
pixel or dwell-bin integration function                  absent
repeat maps of the same registered region                absent
timestamps and full acquisition-order array              absent
drift records                                             absent
repeat or observation covariance                         absent
analysis and fitting code                                 absent
```

The article supplies snake-scan intent and encoder tracking, but the CSV does not
preserve timestamps or acquisition order. These statements therefore do not
supply a drift covariance.

## Authorized interpretation

The admitted field can test whether the existing R04 implementation can perform,
on one real semiconductor map:

- a predeclared added numerical-kernel sweep;
- variance-versus-added-scale calculation;
- finite-field map-variance diagnostics;
- same-raster cross-scale variance-estimator covariance;
- full-covariance versus false independent-pixel/scale comparisons;
- a descriptive held-out added-scale closure check;
- crop, mask, and edge-convention sensitivity;
- phase-randomized or covariance-matched synthetic controls.

The added numerical scales are deterministic transformations of one field. They
are not independent experimental resolutions.

## Prohibited interpretation

This source does not support:

- HgCdTe experimental validation;
- an HgCdTe point variance or correlation length;
- deconvolution of the unmeasured native instrument kernel;
- a latent physical CdSeTe correlation length;
- identification of a universal semiconductor covariance family;
- conversion of PL peak-wavelength variation into composition without an
  independent observation model;
- treating pixels as independent repeats;
- treating numerically smoothed maps as independent measurements;
- manuscript authorization or R05 activation.

## Consequence for R04

HgCdTe external validation remains `blocked`. A cross-material real-data
methodology demonstration is now authorized in restricted form. Its result must
remain subordinate to the analytical R04 claims and must be labeled as a
source-data-derived CdSeTe PL-map demonstration.
