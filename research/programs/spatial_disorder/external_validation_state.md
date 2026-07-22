# R04 external validation state

**Portfolio contribution:** R04  
**Controlling issues:** #196, #250  
**State:** `external_data_blocked`  
**Manuscript impact:** no manuscript authorization

## Decision

The current audited source set does not contain a direct multiresolution
validation path for the R04 inverse.

This is a data-readiness decision, not a failed scientific prediction.

## Qualification boundary

Direct validation requires:

1. the same specimen and registered spatial region;
2. original numerical arrays or spectra with coordinates;
3. three independently characterized effective scales, or one reusable
   numerical high-resolution map filterable under three declared kernels;
4. measured or reconstructable kernels at every scale;
5. specimen thickness and a declared depth-weighting or absorption model;
6. uncertainty, repeats, or covariance sufficient for the observation model;
7. an explicit observable and preprocessing chain.

A source is not promoted by a weighted score when a mandatory item is absent.

## Current candidates

| Candidate | Qualified use | Direct validation blocker |
|---|---|---|
| Chang et al. 2005 | Source-bounded figure benchmark | Published one 100-micrometre map; no raw same-region aperture sweep, measured PSF, or covariance |
| Furstenberg et al. 2005 | Cross-modality context | PL and transmission at one representative 25-micrometre resolution; modalities are not scales |
| Ruzhevich et al. 2024 | Not qualifiable from available record | Official abstract only; full spatial, numerical, kernel, registration, and uncertainty record not retrieved |

The Ruzhevich classification is access bounded. It does not assert that the full
article lacks the required information.

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

## Permitted work while blocked

- request original numerical data and instrument metadata from authors;
- specify a new multiresolution experiment;
- use Chang as a rights-safe claim-level or figure-recoverability benchmark;
- use Furstenberg to test modality-specific forward-model requirements;
- update the Ruzhevich evidence state if lawful full text or author data become
  available.

## Prohibited substitutions

- multiple modalities for multiple effective scales;
- adjustable aperture capability for an actual same-region aperture sweep;
- nominal pixel pitch for a measured PSF;
- digitized publication pixels for original arrays;
- deterministic smoothing of one map for independent measurements;
- nominal raster pixels for independent repeats;
- absence from the accessible record for proof of source-level absence.

## Authorization consequence

The analytical and controlled synthetic R04 gates remain valid. External
specimen validation and manuscript writing remain unauthorized until a source
or experiment satisfies the qualification protocol and the merged joint model
is run against the resulting data package.
