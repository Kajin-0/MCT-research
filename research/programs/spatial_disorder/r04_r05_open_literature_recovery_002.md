# R04/R05 open-literature recovery 002

**Controlling issue:** #400  
**Predecessor:** PR #401  
**User constraint:** no author, facility, or partner outreach  
**Decision:** `PARTIAL_REANALYSIS_FEASIBLE`

## Scope

The three papers requested after PR #401 were reported unavailable to the user. A bounded public-source recovery found two full texts that can be assessed without outreach:

1. Bovkun et al. (2025), DOI `10.1103/PhysRevMaterials.9.054602`, open access under CC BY 4.0.
2. Biquard et al. (2021), DOI `10.1107/S1600577520013211`, official open PDF from IUCr.

The 2012 etched-surface STM/STS paper, DOI `10.3724/SP.J.1010.2012.00222`, has an author-uploaded copy listed publicly, but the file endpoint was not reliably retrievable. Its abstract-level conclusions were retained and compared with the quantitatively richer APL companion paper already ingested in PR #401.

No PDF is committed in this tranche.

## 1. Near-critical quantum-well constraints from Bovkun et al.

The study provides the strongest available specimen-selection prior for a deliberately near-critical HgCdTe series. It examines approximately 10 nm Hg1-xCdxTe quantum wells grown by MBE in Hg0.3Cd0.7Te barriers on CdTe. The wells are pseudomorphically strained to CdTe and span

```text
x = 0.040, 0.047, 0.049, 0.052, 0.054, 0.061
```

with measured QW thicknesses

```text
10.2, 9.9, 9.7, 10.3, 10.2, 10.0 nm
```

respectively. XRR model fitting determines thickness to approximately plus or minus one atomic layer. The paper's carrier-density estimates, in units of 1e10 cm^-2, are 8, 6, unreported, 6, 10, and 2, with an estimated uncertainty of 2 in the same units.

### Composition calibration boundary

The composition of the thin wells is not measured directly by XRD because their signal is too weak. Instead, Cd/Te beam-flux ratios are calibrated against 75 nm Hg1-xCdxTe layers whose composition is extracted from XRD under Vegard-law modeling. The resulting flux calibration is then transferred to the approximately 10 nm wells.

This is a credible sample-level composition chain, but it is not a local composition map and does not provide a spatial variance or covariance.

### Near-critical result

The series experimentally spans the QW topological transition. The paper states that for x greater than 0.054, the beta Landau-level transition lies above alpha at all fields, anticrossings disappear, and a direct trivial gap opens. For R04/R05 design purposes, the x=0.052, d=10.3 nm and x=0.054, d=10.2 nm specimens are the most relevant boundary candidates.

This does not establish the local mass detuning of any retained specimen. It supplies a controlled composition-thickness neighborhood in which a future near-critical specimen should be selected.

### Broadening convention

The k.p spectral calculation applies Gaussian occupation broadening

```text
sigma(B) = 2 meV * sqrt(B[T])
```

This is a model convention, not an experimentally measured STM/STS energy-resolution kernel. It cannot satisfy the R04/R05 spectroscopy-resolution gate.

### Bovkun evidence effect

```text
near-critical specimen-class prior:  materially improved
local variance:                      absent
local correlation length:            absent
local DOS:                            absent
same-population covariance + STS:     absent
```

## 2. Measurement-kernel constraints from Biquard et al.

The Biquard study is not a near-critical spectroscopy record. Its value is methodological: it demonstrates a measured spatial kernel and explicit cross-modality convolution in HgCdTe/CdZnTe heterostructures.

### Samples and modalities

The paper studies MBE material on 4 cm x 4 cm (211)B CdZnTe substrates containing approximately 4% Zn:

- a 4.5 um as-grown HgCdTe layer;
- material from the same wafer after a five-hour anneal under Hg pressure;
- an 11 um dual-band detector stack.

Composition is measured by SIMS for the single-layer samples and by STEM-EDX for the dual-band stack. The dual-band TEM lamella is thinner than 100 nm.

### Measured spatial response

The nominal white-beam diameter is approximately 500 nm. The authors infer the actual beam profile from the abrupt Hg-fluorescence transition at a layer/substrate interface and fit it with a pseudo-Voigt function containing 20% Lorentzian contribution:

```text
measured beam FWHM = 580 nm
```

This is the first paper in the R04/R05 literature set to supply an experimentally inferred spatial response rather than only a nominal aperture or spot size.

### Kernel-matched comparison

The paper reports:

- SIMS depth precision of approximately 10 nm;
- STEM-EDX depth precision of approximately 15 nm;
- convolution of both chemical profiles with the measured 580 nm pseudo-Voigt beam before comparison with micro-Laue strain;
- local strain sensitivity of approximately plus or minus 1.3e-5;
- local orientation resolution of approximately one arcsecond.

For the annealed interface, composition-derived strain agrees with micro-Laue through the interface after the SIMS profile is convolved with the measured beam. The dual-band STEM-EDX profiles are treated the same way.

This is directly relevant to R04 methodology: higher-resolution chemical data must be passed through the lower-resolution measurement kernel before modalities are compared.

### Why this does not recover the missing covariance

The chemical and strain records are cross-sectional depth profiles. They do not provide a two-dimensional lateral field or a stationary lateral covariance. The 580 nm FWHM is also slightly coarser than the preferred 10-500 nm design range.

The paper therefore supports the measurement-kernel procedure but not the required local random-mass statistics.

## 3. Etched-surface STM/STS paper status

The author-posted listing for DOI `10.3724/SP.J.1010.2012.00222` confirms:

- 3% bromine-methanol etching for 2.5 minutes;
- submicrometer pits with apparent depths from tens to hundreds of nanometers;
- flat-region apparent gaps enlarged by tip-induced band bending;
- pit spectra blurred by dense in-gap states.

Those statements reinforce the same nuisance model already established more quantitatively by the APL paper ingested in PR #401:

- apparent topography can be electrically induced and bias dependent;
- an apparent zero-current plateau is not the bulk gap;
- pit spectra can lose band-gap information because of defect states.

The missing full text is therefore not treated as a program blocker. It could refine the surface-preparation record, but it cannot supply near-critical composition covariance, a measured spectroscopy kernel, or same-specimen spatial linkage.

## Aggregate gate assessment

| Gate | Result | Reason |
|---|---|---|
| Local variance | FAIL | No source gives local lateral mass or composition variance. |
| Correlation length | FAIL | Depth transitions and beam width are not lateral material correlation length. |
| Same population | FAIL | Near-critical QWs, detector cross sections, and STM specimens are unrelated. |
| Near critical | PARTIAL | Bovkun supplies a near-critical QW series, not local detuning for a matched covariance/STS specimen. |
| Resolution | PARTIAL | Biquard measures a spatial kernel; no measured local-spectroscopy energy kernel exists. |
| Matched null | FAIL | No matched correlated-versus-scalar local-DOS comparison is possible. |
| Robustness | PARTIAL | The papers strengthen calibration and kernel treatment, but not the decisive joint inference. |
| Decision changing | PARTIAL | They sharpen specimen selection and experiment design, but cannot authorize R05 material activation. |

## Decision

```text
PARTIAL_REANALYSIS_FEASIBLE
```

The open-literature recovery improves two components:

1. the near-critical composition-thickness prior;
2. the measured spatial-kernel and convolution methodology.

It does not recover the decisive matched dataset. The remaining missing evidence is:

```text
2D lateral covariance on a near-critical HgCdTe specimen
+ local low-energy spectroscopy on the same specimen population
+ measured spectroscopy energy kernel
```

## Program state

```text
NO_OUTREACH
LITERATURE_RECOVERY_EXHAUSTED_UNLESS_NEW_USER_PAPERS_APPEAR
R05_BLOCKED
```

No further paper is required merely to complete this literature tranche. New user-supplied papers can still be assessed when they become available, but the program should not continue searching indefinitely or substitute a larger simulation for the missing experiment.
