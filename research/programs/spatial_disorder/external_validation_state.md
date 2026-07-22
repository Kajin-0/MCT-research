# R04 external validation state

**Portfolio contribution:** R04  
**Controlling issues:** #196, #250, #272, #281, #291  
**State:** `external_data_blocked`  
**Manuscript impact:** no manuscript authorization

## Decision

The audited source set now contains:

```text
partial multiresolution candidates      = 1
nearest detector-pixel raster           = 1 source-bounded benchmark
depth-observation-model contexts        = 1
direct validation candidates            = 0
```

Gopal et al. 1992 remains the nearest multiresolution source. Phillips et al. 2003 remains the nearest detector-pixel-scale spatial absorption source. Ariel et al. 1995 becomes the nearest explicit depth-observation-model context.

None supplies the numerical, kernel, uncertainty, registration, and scale diversity required for direct R04 inversion.

This is a data-readiness decision, not a failed scientific prediction.

## Nearest partial multiresolution benchmark

Gopal, Ashokan, and Dhar (1992), DOI `10.1016/0020-0891(92)90053-V`, report transmission spectra from the same HgCdTe epilayer using nominal incident beam diameters of:

```text
wide beam       3 mm
focused beam    250 micrometres
scale ratio     12
```

For sample 90239, the two rendered spectra shift relative to one another. The authors identify the shift as evidence of lateral composition nonuniformity. Control sample 90211 shows no noticeable change over the same beam-diameter change.

**Qualification:** `partial_multiresolution_benchmark`

It remains incomplete because it lacks original arrays, a third scale, measured PSFs, registered beam centers, repeat covariance, and complete specimen-specific thickness/depth metadata.

## Nearest detector-pixel-scale benchmark

Phillips et al. (2003), DOI `10.1063/1.1625776`, report infrared spectromicroscopy using an approximately **9 micrometre** beam with **10 micrometre** scan spacing.

Published records include:

```text
line scan length                       2 mm
area map                               200 by 200 micrometres
measured spectra in area map           400
reported effective probe scales          1
```

At 1558 cm^-1 the paper reports mean absorption coefficient 887 cm^-1 with standard deviation 24.6 cm^-1, or 2.8 percent. Model-extracted composition has mean x = 0.2256 and standard deviation 3.0e-4.

The source warns that apparent composition variation can combine thickness, composition, absorption, interface reflections, and temporal measurement drift.

**Qualification:** `source_bounded_figure_benchmark`

The 400 spectra improve spatial coverage at one kernel. They do not create 400 independent probe scales or independent repeats.

## Nearest depth-observation-model context

Ariel et al. (1995), DOI `10.1063/1.113916`, report a room-temperature FTIR method with the chain:

```text
transmission
-> absorption coefficient alpha(E)
-> smoothing and fringe filtering
-> d alpha / dE
-> d2 alpha / dE2
```

The first-derivative maximum is used as an approximate average-gap marker. The second-derivative extrema are associated with `Eg_min` and `Eg_max`, and their separation estimates

```text
Delta Eg = Eg_max - Eg_min
```

under a linearly graded through-thickness model.

The declared depth average is

```text
alpha(E) = (1/d) integral from 0 to d of alpha_local[E, Eg(z)] dz.
```

Source-level records include:

```text
bulk sample thickness                     500 micrometres
epitaxial-layer thickness range           10-25 micrometres
bulk band-gap variation                   less than 0.005 eV
LPE Delta Eg                              approximately 0.02 eV
LPE linear-grading field                  approximately 10-20 V/cm
MOCVD linear-grading field                around 30 V/cm
```

The paper states that the CdTe/HgCdTe graded interface cannot be neglected for layers thinner than 15 micrometres. It also states that excessive smoothing can shift derivative peaks and that the simplified model omits nonparabolicity and Burstein-Moss effects.

**Qualification:** `depth_observation_model_context`

The paper does not report lateral coordinates, a raster, aperture or PSF, a same-region scale sweep, numerical arrays, repeats, or observation covariance. Its `Delta Eg` is a depth-grading estimate, not a lateral covariance statistic.

## Direct qualification boundary

Direct validation requires:

1. the same specimen and registered spatial region;
2. original numerical arrays or spectra with coordinates;
3. three independently characterized effective scales, or one reusable numerical high-resolution map filterable under three declared kernels;
4. measured or reconstructable kernels at every scale;
5. specimen thickness and a declared depth-weighting or absorption model;
6. uncertainty, repeats, or covariance sufficient for the observation model;
7. an explicit observable and preprocessing chain.

A source is not promoted by raster density, modality count, specimen count, growth-technique diversity, or a weighted score when a mandatory item is absent.

## Current source disposition

| Candidate | Qualified use | Direct validation blocker |
|---|---|---|
| Gopal et al. 1992 | Partial multiresolution benchmark | Two rendered spectra, nominal beam diameters, no third scale, PSF, coordinates, or covariance |
| Phillips et al. 2003 | Detector-pixel-scale source-bounded figure benchmark | 400 spectra at one approximately 9 micrometre scale; no arrays, full PSF, repeats, or scale sweep |
| Ariel et al. 1995 | Depth-averaged FTIR observation-model context | One spatially averaged spectrum per specimen; no lateral map, kernel, arrays, registration, scale sweep, or covariance |
| Chang et al. 2005 | Source-bounded figure benchmark | Published one 100-micrometre map; no raw same-region aperture sweep, measured PSF, or covariance |
| Furstenberg et al. 2005 | Cross-modality context | PL and transmission at one representative 25-micrometre resolution; modalities are not scales |
| Murakami et al. 1992 | Source-bounded figure benchmark | Rendered EPMA profiles; no arrays, kernel, or scale sweep |
| Parikh et al. 1996 | Source-bounded figure benchmark | Rendered lateral map and statistics; no grid, beam kernel, arrays, or covariance |
| Feldman et al. 1991 | Source-bounded figure benchmark | Microscopic vertical-interface mapping, not a lateral scale sweep |
| Aoki et al. 2004 | Source-bounded figure benchmark | HREM/Z-contrast interface figures; no reusable arrays or multiscale registration |
| Oda et al. 1992 | Method-comparison context only | FTIR, EPMA, and detector records are not registered maps of one region |
| Jeoung et al. 1996 | Transmission calibration context only | Bulk spectra without spatial mapping or scale variation |
| Ruzhevich et al. 2024 | Not qualifiable from available record | Official abstract only; full numerical, kernel, registration, and uncertainty record not retrieved |

## Minimum next package

Proceed to direct spatial validation only after obtaining either:

```text
same registered region measured at >=3 calibrated effective scales
```

or:

```text
one original numerical high-resolution map
+ physical coordinates and acquisition order
+ calibration metadata
+ permission to apply >=3 declared numerical kernels
```

The package must additionally include PSF/aperture/pixel definitions, registration, thickness/depth model, uncertainty covariance, exact observable, preprocessing, raster geometry, and cross-scale sampling relationships.

For Ariel 1995 specifically, a quantitative depth-operator upgrade requires:

- original transmission, absorption, and derivative arrays;
- exact smoothing and fringe-removal algorithms and parameters;
- specimen-specific thickness and interface-profile metadata;
- a measured or reconstructable lateral beam kernel;
- measurement coordinates and acquisition order;
- repeat uncertainty or observation covariance;
- independent depth-profile validation for `Eg(z)`;
- carrier-density information for Burstein-Moss assessment;
- a forward model including nonparabolicity and the relevant interface region.

## Permitted work while blocked

- treat Gopal 1992 as qualitative evidence that HgCdTe transmission can depend on probe diameter;
- use Phillips 2003 as detector-pixel-scale absorption and raster-sampling context;
- use Ariel 1995 to constrain depth averaging, derivative preprocessing, linear-grading, and interface-grading nuisance models;
- search the reprioritized DOI queue for original arrays, third-scale measurements, and instrument metadata;
- use other audited sources for bounded forward-model, growth-uniformity, and cross-modality context.

## Prohibited substitutions

- dense raster positions for distinct probe scales;
- 400 spectra for 400 independent repeats;
- two scales for a three-scale covariance-family test;
- through-thickness `Delta Eg` for lateral spatial variance;
- multiple specimens or growth methods for spatial registration;
- derivative peak positions for exact intrinsic band gaps;
- linear-grading field estimates for model-independent electric-field measurements;
- nominal beam diameter for a complete measured PSF;
- multiple modalities for multiple effective scales;
- adjustable aperture capability for an actual same-region aperture sweep;
- digitized publication pixels for original arrays;
- temporal scan drift for long-range spatial covariance;
- absence from an accessible record for proof of source-level absence.

## Authorization consequence

The analytical and controlled synthetic R04 gates remain valid. The papers strengthen the external premise and observation-model discipline but do not authorize specimen covariance inference, novelty claims, or manuscript writing. Direct external validation remains blocked until an audited source satisfies the qualification protocol and the merged joint model is run against the resulting numerical data package.
