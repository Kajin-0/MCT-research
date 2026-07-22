# R04 public-data recovery audit

**Program:** R04 — measurement-kernel-aware spatial disorder  
**Parent issue:** #290  
**Recovery issues:** #297, #299, #307  
**Audit date:** 2026-07-22  
**State:** `external_data_blocked`

## Decision

The public-only recovery tranche has not located a source-native numerical package that satisfies the R04 external-validation contract.

```text
complete user-supplied PDFs audited       3
public source-native packages found       0
qualified direct-validation packages      0
analysis branches authorized              0
```

This is a public-data readiness result. It is not a failed prediction of the spatial-disorder model.

## Permanent communication policy

```text
No email.
No direct messages.
No author or institutional outreach.
No request-for-data communication through any platform.
```

Only already-public records may be searched or inspected.

## Asset audit

### Gopal, Ashokan, and Dhar 1992

**DOI:** `10.1016/0020-0891(92)90053-V`  
**Complete PDF SHA256:** `dda85e0b6f8ceece323ffe8436084868112e1fb2679c189a1e7563e3f4aabe34`

The seven-page PDF contains no embedded files or source-native spectra. Its pages are constructed from 300-dpi CCITT scan strips with an OCR/text overlay.

The article confirms:

```text
instrument                  FTS-40 FTIR
nominal beam diameters      3 mm and 250 micrometres
sample 90211                no noticeable spectral change
sample 90239                relative shift between rendered spectra
```

For sample 90239, `x=0.2255` and `x=0.2304` are the `Z_1/2` and `Z_i` composition estimators applied to the focused-beam spectrum. They are not compositions assigned independently to the two beam diameters and are not a two-scale variance datum.

**Disposition:** strongest physical two-scale lead; public direct-validation package not found.

### Chen, Zhu, and Shao 2019

**DOI:** `10.1063/1.5111788`  
**Complete PDF SHA256:** `84d849ee955a7580b59c8643714768b4080832249a032432d53070d72c52672d`

The nine-page PDF contains no embedded spectral cube, map arrays, spreadsheet, or supplementary archive.

The source supplies a strong instrument contract:

```text
pump spot diameter at 1/e^2        26.3 micrometres
pump spot diameter at half maximum 15.3 micrometres
raster step                        40 micrometres
stage translation resolution       1 micrometre
stage angular resolution           0.002 degree
LWIR map                           25 by 25 spectra over 960 by 960 micrometres
LWIR spectral resolution           12 cm^-1
LWIR SNR                           greater than 30
```

The mapped HgTe/HgCdTe superlattice PL field is not a direct composition field. The source identifies possible contributions from localized states, defects or impurities, layer-thickness fluctuation, interface roughness, and barrier-composition fluctuation.

**Disposition:** strongest measured pump-kernel and raster contract; public source-native cube not found.

### Furstenberg, White, and Olson 2005

**DOI:** `10.1007/s11664-005-0022-8`  
**Complete PDF SHA256:** `b77621b6c8093d8c1d3295f4172255f6abd118b3f5343c42481a5892ab8a3cb3`

The four-page PDF contains no embedded map arrays or spectra. Figure panels are publication raster images.

The paper reports same-region maps for sample `HRL3307`:

```text
area                         1200 by 1200 micrometres
reported resolution          25 micrometres
nominal grid                 approximately 48 by 48
modality 1                   transmission-fringe effective optical thickness
modality 2                   PL peak area
```

The effective optical-thickness field can conflate physical thickness, composition variation, and Te inclusions. PL peak area depends on excitation and collection efficiency. The two modalities are not two probe scales.

**Disposition:** strongest same-region cross-modality lead; public common-coordinate arrays not found.

## Public dissertation and report lineage

Robert Furstenberg's 2006 dissertation, *Photoluminescence Study of Defects in Mercury Cadmium Telluride*, is publicly indexed as `hdl:2142/34731`.

It confirms that paired PL and transmission/background interferograms were acquired in parallel, stored on a hard drive, coherently added, apodized, phase corrected, and Fourier transformed. It also reports a 48-by-48 map of the same 1.2-by-1.2 mm region at 300 K and 77 K.

The dissertation confirms that source-native data existed during the experiment. It does not expose the interferograms, coordinate exports, processed spectra, software, covariance records, or a public companion dataset.

The public MURI final report:

```text
title       Fundamental Research on Infrared Detection
report      MURI-UIUC-GIT-05
accession   ADA459422
grant       DAAD19-01-1-0591
release     approved for public release; distribution unlimited
```

confirms the instrument-program and dissertation lineage but has not exposed a source-native numerical package.

## Public lineage targets

The following exact sources remain bounded public searches, not data packages:

```text
10.1007/s11664-004-0071-4   Furstenberg high-resolution mapping
10.1063/1.2214931           Furstenberg mapping apparatus
10.1063/5.0164195           Chen-lineage As-doped HgCdTe PL mapping
10.1063/5.0244755           Chen-lineage approximately 2-micrometre system
```

No source-native package was located in the declared public searches associated with these identifiers.

## Qualification gate

A usable package still requires either:

```text
same registered specimen region
+ at least three calibrated effective scales
+ original numerical observations
+ complete kernel and uncertainty metadata
```

or:

```text
one original high-resolution numerical map
+ physical coordinates and acquisition order
+ calibration metadata
+ public rights to apply at least three declared numerical kernels
```

Both alternatives additionally require registration, kernels, a thickness/depth model, uncertainty or covariance, a declared observation and preprocessing chain, and rights compatible with the intended analysis.

## Stop decision

The present records support source-bounded instrument, scale, and cross-modality context only.

They do not authorize:

- publication-figure digitization as source data;
- `Q_G` evaluation;
- covariance-family fitting;
- recovery of `A` or `xi`;
- held-out prediction;
- a composition-field assignment;
- a new R04 mechanism;
- a manuscript;
- any R05 computation.

A public-data-not-found result is acceptable. Absence from the declared public searches does not prove that private or unindexed data do not exist.
