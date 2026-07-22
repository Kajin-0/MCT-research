# R04 external validation state

**Portfolio contribution:** R04  
**Controlling issues:** #196, #250, #272  
**State:** `external_data_blocked`  
**Manuscript impact:** no manuscript authorization

## Decision

The current audited source set contains one genuine but incomplete multiresolution benchmark and no direct validation path for the R04 inverse.

```text
partial multiresolution candidates = 1
direct validation candidates       = 0
```

This is a data-readiness decision, not a failed scientific prediction.

## Nearest available benchmark

Gopal, Ashokan, and Dhar (1992), DOI `10.1016/0020-0891(92)90053-V`, report transmission spectra from the same HgCdTe epilayer using nominal incident beam diameters of:

```text
wide beam       3 mm
focused beam    250 micrometres
scale ratio     12
```

For sample 90239, the two rendered spectra shift relative to one another. The authors identify the shift as evidence of lateral composition nonuniformity.

For control sample 90211, no noticeable spectral change was reported over the same beam-diameter change.

This establishes source-bounded qualitative scale dependence. It does not support covariance inversion because the source lacks:

- original numerical spectra;
- a third effective scale;
- measured PSFs rather than nominal diameters;
- registered beam-center coordinates;
- repeat uncertainty or covariance;
- complete sample-specific thickness and depth metadata.

**Qualification:** `partial_multiresolution_benchmark`

## Direct qualification boundary

Direct validation requires:

1. the same specimen and registered spatial region;
2. original numerical arrays or spectra with coordinates;
3. three independently characterized effective scales, or one reusable numerical high-resolution map filterable under three declared kernels;
4. measured or reconstructable kernels at every scale;
5. specimen thickness and a declared depth-weighting or absorption model;
6. uncertainty, repeats, or covariance sufficient for the observation model;
7. an explicit observable and preprocessing chain.

A source is not promoted by a weighted score when a mandatory item is absent.

## Current source disposition

| Candidate | Qualified use | Direct validation blocker |
|---|---|---|
| Gopal et al. 1992 | Partial multiresolution benchmark | Two rendered spectra, nominal beam diameters, no third scale, PSF, coordinates, or covariance |
| Chang et al. 2005 | Source-bounded figure benchmark | Published one 100-micrometre map; no raw same-region aperture sweep, measured PSF, or covariance |
| Furstenberg et al. 2005 | Cross-modality context | PL and transmission at one representative 25-micrometre resolution; modalities are not scales |
| Murakami et al. 1992 | Source-bounded figure benchmark | Rendered EPMA profiles; no arrays, kernel, or scale sweep |
| Parikh et al. 1996 | Source-bounded figure benchmark | Rendered lateral map and summary statistics; no grid, beam kernel, arrays, or covariance |
| Feldman et al. 1991 | Source-bounded figure benchmark | Microscopic vertical-interface mapping, not a lateral scale sweep |
| Aoki et al. 2004 | Source-bounded figure benchmark | HREM/Z-contrast interface figures; no reusable arrays or multiscale registration |
| Oda et al. 1992 | Method-comparison context only | FTIR, EPMA, and detector records are not registered maps of one region |
| Jeoung et al. 1996 | Transmission calibration context only | Bulk spectra without spatial mapping or scale variation |
| Ruzhevich et al. 2024 | Not qualifiable from available record | Official abstract only; full spatial, numerical, kernel, registration, and uncertainty record not retrieved |

The Ruzhevich classification is access bounded. It does not assert that the full article lacks the required information.

## Minimum next package

Proceed only after obtaining either:

```text
same registered region measured at >=3 calibrated effective scales
```

or:

```text
one original numerical high-resolution map
+ coordinates
+ calibration metadata
+ permission to apply >=3 declared numerical kernels
```

The package must additionally include:

- PSF, aperture, pixel, and scan-bin definitions;
- registration transform;
- thickness and depth model;
- repeat or covariance information;
- observable and preprocessing definitions;
- raster geometry and cross-scale sampling relationship.

For the Gopal benchmark specifically, the minimum upgrade is:

- original wide- and focused-beam spectra;
- beam-center coordinates;
- measured aperture/PSF descriptions;
- sample 90239 thickness and depth model;
- repeat uncertainty;
- one additional calibrated beam size.

## Permitted work while blocked

- treat Gopal 1992 as qualitative evidence that measured HgCdTe transmission can depend on probe diameter;
- use Chang, Murakami, Parikh, Feldman, and Aoki as rights-safe source-bounded spatial or microscopic benchmarks;
- use Furstenberg to test modality-specific forward-model requirements;
- use Oda and Jeoung for composition-extraction and observation-model context;
- update the Ruzhevich evidence state if lawful full text or numerical data become available;
- search for papers or supplements containing original registered arrays at three scales.

## Prohibited substitutions

- two scales for a three-scale covariance-family test;
- nominal beam diameter for a measured PSF;
- multiple modalities for multiple effective scales;
- adjustable aperture capability for an actual same-region aperture sweep;
- nominal pixel pitch for a measured PSF;
- digitized publication pixels for original arrays;
- deterministic smoothing of one rendered map for independent measurements;
- nominal raster pixels for independent repeats;
- absence from the accessible record for proof of source-level absence.

## Authorization consequence

The analytical and controlled synthetic R04 gates remain valid. The uploaded papers strengthen the external premise but do not authorize specimen covariance inference or manuscript writing. Direct external validation remains blocked until a source satisfies the qualification protocol and the merged joint model is run against the resulting numerical data package.
