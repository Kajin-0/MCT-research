# R04/R05 public-data feasibility audit

**Controlling issue:** #395  
**Predecessor:** PR #396  
**Audit date:** 2026-07-31  
**Decision:** `PARTNER_DATA_REQUIRED`

## Decision-changing question

Does an accessible public record already contain enough evidence from one near-critical HgCdTe specimen, or a quantitatively justified exchangeable specimen population, to evaluate

\[
g=\frac{\sigma_M\xi}{\hbar v_K},
\qquad
m=\frac{\overline M\xi}{\hbar v_K},
\]

and compare the correlated model with the matched scalar local-gap null after measured spatial and spectroscopic kernels are applied?

The required package is not a collection of individually relevant figures. It must contain, or permit defensible recovery of:

1. local mass or convertible composition variance;
2. correlation length after PSF, pixel and finite-window correction;
3. same-specimen or quantitatively justified same-population linkage;
4. near-critical mean mass;
5. measured low-energy resolution kernel;
6. enough raw information to apply the same one-point distribution and measurement kernel to both models;
7. uncertainty and systematic-sensitivity information;
8. a result capable of changing the decision on higher-dimensional or full-Kane work.

## Search protocol

The audit searched exact titles, author names, material keywords and observable keywords across:

- Zenodo;
- RODARE;
- RepOD;
- Figshare;
- Mendeley Data;
- Dryad;
- OSF;
- institutional repositories;
- publisher article and supplementary-material pages;
- author and group publication pages.

Query families included:

```text
HgCdTe STM STS raw data
HgCdTe scanning tunneling spectroscopy repository
HgCdTe STEM EDX raw spectrum image
HgCdTe composition map dataset
HgCdTe SIMS raw data
near-critical HgCdTe magneto-optical data
HgTe HgCdTe transport dataset
exact article title + data/repository/supplementary
exact author set + Zenodo/RODARE/RepOD
```

The search was designed for high recall. Records were rejected only after evaluating their actual observable, specimen class, access state and decisive metadata.

## Result

No qualifying complete public record was identified.

This is not a statement that no useful HgCdTe data are public. Several records provide high-quality partial evidence. The failure is specifically the joint-evidence requirement:

```text
near-critical material
+ local covariance
+ measured spatial transfer function
+ matched low-energy local spectroscopy
+ measured energy kernel
+ same-population linkage
+ raw calibration metadata
```

No audited record supplies this combination.

## Candidate-level findings

### 1. Bovkun et al. 2025 near-critical HgCdTe quantum-well phase diagram

**Source:** Physical Review Materials 9, 054602; DOI `10.1103/PhysRevMaterials.9.054602`.

The article is open and directly relevant to the near-critical composition regime. It combines structural characterization, magneto-optical measurements and k.p modeling for approximately 10 nm HgCdTe quantum wells.

Useful evidence:

- near-critical specimen series;
- mean composition and thickness calibration;
- topological-transition placement;
- magneto-optical band-parameter constraints.

Disqualifying gaps:

- no linked raw-data repository was identified through exact-title and author searches;
- no local two-dimensional or three-dimensional mass/composition covariance;
- no measured local-map transfer function;
- no local DOS spectroscopy;
- no same-region covariance-spectroscopy linkage.

This is the strongest near-critical partner lead, but it is not a public-data solution.

### 2. Wang et al. 2012 HgCdTe STM/STS

**Source:** “Scanning tunneling spectra for the etched surface of p-type HgCdTe,” DOI `10.3724/SP.J.1010.2012.00222`.

This paper establishes technical feasibility of STM and STS on etched LPE HgCdTe. It also demonstrates why the R04/R05 evidence standard must be strict: the reported apparent gap is altered by tip-induced band bending, while etched pits exhibit finite in-gap slope attributed to gap states.

Useful evidence:

- HgCdTe surface topography;
- HgCdTe tunneling spectra;
- explicit surface and electrostatic failure modes.

Disqualifying gaps:

- no raw spatially indexed spectra located;
- no measured energy-resolution kernel located;
- near-critical composition not established for the R05 use case;
- no local composition or mass map;
- no same-region spectroscopy-composition registration.

The article is an author-contact lead, not a qualifying dataset.

### 3. Biquard et al. 2021 HgCdTe/CdZnTe Laue and STEM-EDX

**Source:** Journal of Synchrotron Radiation 28, 181–187; DOI `10.1107/S1600577520013211`.

The work combines submicronic strain profiling with SIMS or STEM-EDX composition profiles in complex HgCdTe/CdZnTe detector heterostructures. The dual-band sample includes local Hg, Cd and Zn concentration information from a thin lamella.

Useful evidence:

- local chemical profiling;
- interface and layer composition;
- strain-composition correlation;
- a demonstrated HgCdTe STEM-EDX workflow.

Disqualifying gaps:

- the reported EDX result is a cross-sectional profile, not a stationary lateral covariance field;
- no raw spectrum-image repository was identified;
- the architecture is not the required near-critical specimen;
- no low-energy spectroscopy is linked to the lamella or parent region;
- destructive sampling prevents automatic same-region equivalence.

This is a composition-metrology and author-contact lead.

### 4. Sobieski et al. 2024 residual composition oscillations

**Source:** Sensors 24, 2837; DOI `10.3390/s24092837`.

The open article reports high-resolution SIMS depth oscillations in IMP-MOCVD HgCdTe and their reduction after annealing, with associated electrical and photoelectric changes. Its data-availability statement says the original contributions are included in the article and additional information can be requested from the authors.

Useful evidence:

- direct process-related compositional structure;
- depth-scale oscillations;
- annealing response;
- linkage to device properties.

Disqualifying gaps:

- depth profile rather than lateral covariance;
- no local two-dimensional mass field;
- no near-critical mean-mass condition;
- no matched local low-energy spectroscopy;
- no standalone raw-data package identified.

This is a growth-process lead, not an R05 reopening record.

### 5. Chang et al. 2005 infrared microscope mapping

**Source:** Journal of Crystal Growth 277, 78–84; DOI `10.1016/j.jcrysgro.2005.01.051`.

The article demonstrates automated HgCdTe composition and thickness mapping from infrared transmission. It reports wafer-scale map statistics and is useful for specimen selection and exchangeability assessment.

Disqualifying gaps:

- the lateral transfer band is too coarse or insufficiently specified for the provisional 10–500 nm design range;
- no measured local-map PSF suitable for nanoscale xi recovery;
- no local low-energy spectroscopy;
- no raw map repository identified.

Wafer-scale map standard deviation cannot be substituted for the local sigma_x required by R05.

### 6. Open RODARE HgTe spectroscopy records

Two high-quality open records were audited:

- `10.14278/rodare.2453`, giant THz nonlinearity in topological and trivial HgTe-based heterostructures;
- `10.14278/rodare.3885`, broadband THz upconversion with Dirac materials.

They contain raw spectroscopy, processing code, calculations and sample information. They demonstrate good public-data practice and provide useful pipeline references.

They do not contain:

- near-critical HgCdTe local mass covariance;
- local DOS spectroscopy;
- registered composition maps;
- a matched scalar-null comparison.

Open global THz response is not interchangeable with the local DOS observable required by the present R05 benchmark.

### 7. Restricted Zenodo mK transport record

**Source:** `10.5281/zenodo.15753791`.

The record describes data, metadata and code for mK transport on HgTe/HgCdTe thin films, but the files are restricted. Even if access were granted, the advertised record does not provide the required local covariance or local DOS fields.

It is a relevant group and specimen-capability lead, not a qualifying public record.

### 8. HgCdTe noise record with unresolved repository identifier

The open article “Temperature and electron concentration dependences of 1/f noise in Hg1-xCdxTe” states that raw datasets are available from RepOD, but its data-availability link resolves only to the repository home page rather than a persistent dataset record. Exact-title and author searches did not resolve the record during this audit.

The underlying noise data would still be nonqualifying for #395 because it does not advertise local mass covariance, local DOS spectroscopy or same-region linkage. The broken or incomplete repository citation is nevertheless recorded as a reproducibility defect.

## Gate matrix

| Evidence gate | Public audit result | Reason |
|---|---|---|
| Local variance | `FAIL` | No record provides a qualifying local mass or convertible lateral composition field with uncertainty. |
| Correlation length | `FAIL` | No record supports xi after measured PSF, pixel and finite-window correction. |
| Same population | `FAIL` | No record links qualifying spatial and low-energy spectroscopy measurements on one specimen population. |
| Near critical | `PARTIAL` | The 2025 quantum-well series is near critical, but lacks local covariance and local DOS. |
| Resolution | `FAIL` | No matched local-DOS record includes a measured energy kernel. |
| Matched null | `FAIL` | No record supports a correlated-versus-scalar comparison with shared P(M) and kernel. |
| Robustness | `FAIL` | No complete evidence package exists on which systematic variants can be tested. |
| Decision changing | `FAIL` | No public record can authorize higher-dimensional or full-Kane R05 work. |

## Why the decision is not `PUBLIC_DATA_FEASIBLE`

Digitizing article figures would not recover:

- raw spatial covariance;
- PSF or pixel transfer functions;
- raw spectroscopy kernels;
- same-specimen identifiers;
- calibration covariance;
- surface-preparation history;
- systematic variants.

Combining a near-critical magneto-optical specimen, an unrelated HgCdTe STS specimen and a separate detector EDX lamella would violate the same-population gate. It would create a synthetic composite specimen rather than test a physical specimen.

## Why the decision is not `EXTERNAL_DATA_BLOCKED`

The audit found technically demonstrated components and identifiable acquisition routes:

- HgCdTe STM/STS has been performed;
- HgCdTe STEM-EDX and SIMS have been performed;
- near-critical HgCdTe quantum wells with structural and magneto-optical characterization exist;
- relevant HgTe groups publish open raw spectroscopy and code;
- cryogenic STM/STS and advanced chemical microscopy are available at user facilities identified in PR1.

The missing step is coordinated access, not absence of any plausible method.

## Final PR2 decision

```text
PARTNER_DATA_REQUIRED
```

The minimum next action is an author/facility acquisition campaign, not additional R05 simulation.

## Minimum partner package

A partner request must ask for, or propose acquisition of:

1. raw spatially indexed HgCdTe STS curves and topography;
2. setpoint, temperature, modulation, tip-state and surface-preparation metadata;
3. raw or minimally processed Hg/Cd/Te composition map or spectrum image;
4. pixel coordinates, detector response, dwell time, lamella thickness and quantification uncertainty;
5. specimen identifiers linking the two modalities, or a predeclared exchangeability design;
6. near-critical mean composition or signed-gap calibration;
7. measured spatial and energy transfer functions;
8. permission to preserve immutable raw and derived records.

## Authorized next work

- prepare concise data-request packets for the strongest author groups;
- prepare a user-facility measurement concept with Hg handling and surface-preparation constraints;
- resolve whether archived 2012 STS and 2021 EDX raw records still exist;
- request data or collaboration from the 2025 near-critical quantum-well group;
- stop and return `EXTERNAL_DATA_BLOCKED` only if these partner routes are explicitly unavailable or technically infeasible.

## Work not authorized

- R05 reactivation;
- 2D or 3D random-mass production simulation;
- full 8-band spatial disorder;
- manuscript drafting;
- physical validation from digitized figures;
- treating open THz or transport data as local-DOS evidence.

## Claim boundary

This negative public-data result does not falsify correlated-mass physics. It establishes only that the existing public evidence cannot test the material claim under the predeclared standards.
