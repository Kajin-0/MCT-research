# Ariel et al. 1995 depth-grading observation-model audit

**Program:** measurement-kernel-aware spatial disorder (R04)  
**Issue:** #291  
**Source:** V. Ariel, V. Garber, D. Rosenfeld, and G. Bahir, *Estimation of HgCdTe Band-Gap Variations by Differentiation of the Absorption Coefficient*, Applied Physics Letters 66, 2101-2103 (1995)  
**DOI:** `10.1063/1.113916`  
**Evidence state:** uploaded full text audited

## Qualification decision

```text
qualification = depth_observation_model_context
```

The paper supplies a declared room-temperature FTIR observation chain for estimating average band gap and through-thickness band-gap grading from a spatially averaged transmission spectrum.

It does not supply lateral mapping, a calibrated lateral kernel, a same-region aperture sweep, or numerical arrays suitable for direct R04 covariance inversion.

The source therefore constrains the depth and observation-operator side of R04 without changing the external-validation status.

## Experimental and processing chain

The source procedure is:

```text
room-temperature FTIR transmission
-> extract absorption coefficient alpha(E)
-> smooth measured data
-> suppress noise and interference fringes
-> compute d alpha / dE
-> compute d2 alpha / dE2
```

The preprocessing is scientifically material. The paper states that noise can produce large derivative oscillations and that excessive smoothing can move the derivative peaks.

No numerical smoothing kernel, bandwidth, polynomial order, or complete filter transfer function is published.

## Declared absorption model

The qualitative model separates two absorption regimes.

For photon energy below the gap, the Urbach region is approximated by

```text
alpha(E) proportional to exp[(E - Eg) / Et].
```

For photon energy above the gap, the fundamental Kane region is approximated by

```text
alpha(E) proportional to sqrt(E - Eg).
```

The first derivative therefore rises in the Urbach region and decreases in the simplified Kane region. For a uniform material, the source associates the resulting derivative maximum with the vicinity of the band gap.

This is an approximate observation marker. The source explicitly states that:

- the simplified model may be quantitatively inaccurate for HgCdTe;
- band nonparabolicity is omitted;
- the Burstein-Moss shift is omitted;
- the transition between regimes need not occur exactly at `E = Eg`;
- a more precise mathematical formulation was outside the paper;
- derivative peaks do not provide a precise numerical band gap.

## Depth-averaged graded-layer operator

For an epitaxial layer of thickness `d`, the paper declares the spatially averaged absorption coefficient as

```text
alpha(E) = (1/d) integral from 0 to d of alpha_local[E, Eg(z)] dz.
```

The source then assumes a linearly graded depth profile between

```text
Eg_min and Eg_max.
```

Under this model:

- the first-derivative peak broadens as the depth range of band gaps increases;
- extrema of the second derivative are associated with `Eg_min` and `Eg_max`;
- the separation of those extrema estimates

```text
Delta Eg = Eg_max - Eg_min.
```

Figures 1-4 are theoretical illustrations of this operator. Figure 5 shows representative experimental second derivatives for bulk, LPE, and MOCVD material.

## Samples and thicknesses

The paper reports three source classes:

```text
bulk material     Cominco
LPE layers        Fermionics
MOCVD layers      Soreq NRC
```

Thickness records are:

```text
bulk samples                     500 micrometres
epitaxial-layer thickness range  10-25 micrometres
```

Epitaxial thickness was inferred from transmission-fringe locations.

## Reported source-level results

The paper reports:

```text
bulk band-gap variation          less than 0.005 eV
LPE Delta Eg                     approximately 0.02 eV
LPE built-in field               approximately 10-20 V/cm
MOCVD built-in field             around 30 V/cm
```

The electric-field values are conditional on a linear grading assumption. The source does not publish a specimen-level table of thickness, `Eg_min`, `Eg_max`, `Delta Eg`, smoothing parameters, or uncertainty for every measured layer.

The MOCVD statement is a field estimate, not a printed universal `Delta Eg` value. No MOCVD `Delta Eg` is reconstructed from the figure in this audit.

## Interface-grading boundary

The source neglects the graded CdTe/HgCdTe transition region in the simplified model for HgCdTe layers thicker than 15 micrometres.

It explicitly states that for layers thinner than 15 micrometres the interface contribution cannot be neglected.

This matters because the reported epitaxial-layer range extends down to 10 micrometres. A complete observation operator for the thinner specimens must therefore include the interface region rather than treating the inferred derivative width as bulk-layer grading alone.

## Spatial-evidence audit

The paper does not report:

- lateral measurement coordinates;
- a raster, line scan, or wafer map;
- measurements at multiple wafer positions;
- beam diameter, aperture, numerical aperture, or measured PSF;
- repeated measurements at multiple effective lateral scales;
- original numerical transmission, absorption, or derivative arrays;
- acquisition order;
- repeat uncertainty or observation covariance.

The prior DOI queue description that anticipated measurements at different wafer positions is not supported by this full text and is corrected by this audit.

The record contains several specimens and growth techniques. Specimen count is not probe-scale count, and growth-technique diversity is not spatial registration.

## R04 interpretation

The source is useful for R04 because it demonstrates that an apparent spectral width can contain a depth-distribution effect before any lateral covariance is considered.

The measurement can be represented schematically as

```text
latent depth profile Eg(z)
-> depth-averaged alpha(E)
-> transmission extraction
-> smoothing / fringe suppression
-> derivative extrema
-> reported average-gap and Delta Eg markers.
```

This chain is distinct from the lateral filtering relation

```text
latent lateral composition field
-> optical / pixel kernel
-> sampled spatial map
-> multiscale variance statistics.
```

A future joint model must not assign all measured edge width to lateral disorder when through-thickness grading, interface grading, carrier-filling effects, and preprocessing can produce similar broadening or peak displacement.

## Permitted uses

- constrain a source-bounded depth-averaged absorption observation operator;
- test sensitivity of inferred derivative extrema to smoothing and fringe filtering;
- represent linear depth grading as an explicit nuisance or alternative model;
- enforce the 15-micrometre interface-grading boundary;
- separate depth grading from lateral spatial covariance in future joint analyses;
- use the source-level magnitude ranges as historical method context.

## Prohibited uses

- treat `Delta Eg` as lateral spatial variance;
- convert one spectrum into multiple effective probe scales;
- infer lateral correlation length or covariance family;
- treat derivative maxima as exact intrinsic band gaps;
- treat the LPE or MOCVD field estimates as model-independent measurements;
- infer missing specimen values by digitizing Figure 5 as though it were original data;
- claim direct external validation, detector prediction, novelty, or manuscript authorization.

## Minimum upgrade package

To use the Ariel method quantitatively in a modern joint inference, obtain:

1. original transmission spectra;
2. the extracted absorption arrays;
3. exact smoothing and fringe-removal algorithms and parameters;
4. specimen-specific thickness and interface-profile metadata;
5. a measured or reconstructable lateral beam kernel;
6. physical measurement coordinates and acquisition order;
7. repeated spectra or an observation covariance model;
8. an independent depth-profile measurement for `Eg(z)` or composition;
9. carrier-density metadata sufficient to assess Burstein-Moss effects;
10. a forward model that includes nonparabolicity and the relevant interface region.

## Portfolio consequence

```text
nearest partial multiresolution benchmark  Gopal 1992
nearest detector-pixel-scale benchmark     Phillips 2003
nearest depth-observation-model context    Ariel 1995
direct validation candidates               0
portfolio status                           external_data_blocked
```

The source improves model discipline but does not remove the external-data block.
