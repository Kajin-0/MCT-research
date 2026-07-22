# Primary-source audit: finite-aperture and spatially resolved HgCdTe mapping

## Status

**Bounded audit complete. No positive novelty decision.**

Primary program: measurement-kernel-aware spatial disorder (R04).  
Controlling issue: #222.  
Contribution impact: prior-art boundary only; no manuscript authorization.

The audit asks whether existing HgCdTe work already establishes the R04 claim chain

```text
spatial covariance
-> finite measurement kernel
-> resolution-dependent apparent variance
-> multiscale inversion / family test
-> absolute-scale calibration floor
-> correlated-raster information accounting
```

Finite-resolution mapping and spatial variation are established prior art. They are not R04 novelty claims.

## Source-state table

| Source | DOI | Audit state | Rights-safe use | Current conclusion |
|---|---|---|---|---|
| Chang et al., *Composition and thickness distribution of HgCdTe molecular beam epitaxy wafers by infrared microscope mapping* | `10.1016/j.jcrysgro.2005.01.051` | Full text audited | Claim-level paraphrase and numerical provenance; no redistribution | Establishes finite-aperture transmission mapping and model-converted composition/thickness maps, but not a multiresolution covariance inverse |
| Furstenberg, White, and Olson, *Spatially resolved photoluminescence and transmission spectra of HgCdTe* | `10.1007/s11664-005-0022-8` | Full text audited | Claim-level paraphrase and numerical provenance; no redistribution | Establishes 25-micrometre PL/transmission mapping and explicit optical ambiguities, but not covariance or correlation-length recovery |
| Ruzhevich et al., *Optical properties and disorder of HgCdTe films grown by molecular beam epitaxy* | `10.1364/JOT.91.000077`; Russian edition `10.17586/1023-5086-2024-91-02-23-33` | Official abstract and bibliographic records audited; full text unavailable to this workstream | Abstract-level claims only | Establishes composition-regime-dependent interpretation and a large-scale localization statement; does not support a claim-level conclusion about spatial kernels or correlation-length inference |

### Ruzhevich source-state decision

The official Optica and *Opticheskii Zhurnal* records expose the abstract and bibliographic metadata. The publisher full-article/PDF endpoints require access that was not available to this workstream. A renewed search of the uploaded-file index returned no matching Ruzhevich full text; this is not evidence that the user does not possess a copy elsewhere.

The source is therefore classified as:

```text
identified primary source
abstract audited
full text not retrieved
claim-level spatial-method conclusion unauthorized
```

This bounded state is explicit and closes the acquisition loop for the present audit. It does not convert an abstract-only source into negative novelty evidence.

## 1. Chang et al. 2005

### 1.1 Measurement geometry

The mapping system combined a Thermo Nicolet Centaur infrared microscope with an FTIR spectrometer and a computerized lateral translation stage.

Source-reported geometry:

```text
stage position precision                  1 micrometre
minimum adjustable beam aperture         25 micrometres at 10-micrometre wavelength
aperture used for large-area maps        100 micrometres
```

The paper states why the larger aperture was selected: stronger signal and shorter mapping time.

### 1.2 Reported observable and inversion

The primary measurement is transmission through a multilayer sample. Composition and thickness are not directly imaged quantities.

The source applies:

- multilayer interference-matrix transmission calculations;
- randomized substrate-phase averaging;
- Fourier-domain initialization of layer thickness;
- Levenberg--Marquardt fitting plus simulated annealing;
- self-consistent composition/thickness iteration;
- an absorption-edge convention of `alpha = 1000 cm^-1`;
- the Hansen composition/temperature gap equation to convert the operational edge to composition.

Thus each reported composition pixel is a model-conditioned inverse result at the selected aperture, not a direct microscopic composition measurement.

### 1.3 Source statistics

For one mapped CdTe/Si wafer, the source reports approximately:

```text
scan region                 66 x 20 mm^2
mean composition            0.2340
composition standard dev.   0.0042
converted cutoff            9 micrometres
converted cutoff std.       0.46 micrometre
```

For a central `20 x 20 mm^2` region:

```text
mean composition            0.2299
composition standard dev.   0.0008
converted 77 K cutoff       9.45 micrometres
converted cutoff std.       0.09 micrometre
```

These statistics depend on the 100-micrometre aperture, scan sampling, model fit, selected region, operational edge definition, and Hansen conversion. They are not the microscopic point variance `C_x(0)`.

### 1.4 Kernel and covariance audit

The source establishes that the beam aperture is adjustable, but the audited text does not provide:

- a measured optical point-spread function at each wavelength;
- an aperture sweep on the same specimen;
- variance as a function of aperture or resolution;
- a spatial autocorrelation, structure function, power spectrum, or correlation length;
- deconvolution of the map by a measured kernel;
- a separation of aperture width from wavelength-dependent diffraction and collection response;
- an accounting of within-map or cross-scale sample covariance.

The paper therefore anticipates the experimental premise of R04—a finite and adjustable probe—but not the R04 covariance-filter inversion.

## 2. Furstenberg, White, and Olson 2005

### 2.1 Measurement geometry

The source reports scanning, spectrally resolved mid-infrared PL and transmission measurements on nominal `Hg0.7Cd0.3Te` epilayers.

Representative source conditions include:

```text
map resolution                         25 micrometres
representative map size                400 x 400 micrometres
sample temperatures                    300 K and 77 K
same-location modalities               PL and transmission
```

The source emphasizes that lower-temperature operation improves signal-to-noise ratio and feature visibility.

### 2.2 PL observation boundaries

The paper explicitly warns that PL intensity depends on collection efficiency and excitation power. It recommends spectral parameters such as PL FWHM and a half-maximum wavelength for run-to-run comparison because they are less directly dependent on collection efficiency.

The source also reports that focused high excitation intensity broadens the PL peak. An as-grown sample had average PL FWHM near `58 meV`, decreasing to `50 meV` after annealing, but the authors state that the focused excitation contributes to the unusually large widths.

This is important prior art for R04: an apparent width can depend on the measurement operator even before spatial covariance is considered.

### 2.3 Defect-size inference is not a correlation length

Low-PL features were mostly confined to single 25-micrometre pixels. The source therefore treats `25 micrometres` as an upper limit on defect size and, assuming negligible defect PL, estimates an average defect size near `10 micrometres` from a roughly 20% pixel-level intensity decrease.

That estimate is an object-size inference under a contrast assumption. It is not:

- a composition autocorrelation length;
- a covariance-kernel inversion;
- a measured point-spread function;
- a variance-versus-resolution result.

### 2.4 Transmission ambiguity

The transmission map is described as an optical-path or effective-thickness map under the assumption of uniform composition and refractive index.

The authors explicitly retain alternatives:

- actual thickness variation;
- composition fluctuation;
- Te inclusions.

They also report that some optical-path variations correlate with PL changes and others do not. This is source-level evidence that modalities and nuisance variables cannot be collapsed into one latent disorder width without a forward model.

### 2.5 Kernel and covariance audit

The audited paper does not provide:

- a same-specimen resolution or spot-size sweep;
- a measured excitation/collection point-spread function;
- variance as a function of resolution;
- spatial autocorrelation or power-spectrum inference;
- a recovered composition correlation length;
- deconvolution of PL or transmission maps by a measurement kernel;
- an effective-sample or cross-scale covariance calculation.

The paper therefore establishes spatially resolved multimodal mapping and interpretation limits, not the R04 multiscale covariance theorem.

## 3. Ruzhevich et al. 2024

### 3.1 Official abstract-level findings

The official records describe MBE-grown HgCdTe films with CdTe fraction approximately `0.3` to `0.7`, studied by:

- optical transmission;
- photoluminescence;
- scanning electron microscopy;
- energy-dispersive X-ray spectroscopy.

The abstract distinguishes composition regimes. For `x approximately 0.3`, optical properties are described as suitable for estimating bandgap and composition. For `x approximately 0.7`, PL up to room temperature is attributed to transitions involving carriers localized on large-scale composition fluctuations; transmission and ellipsometry are treated as more reliable for gap/composition extraction.

These statements support the R04 requirement to keep modality and composition regime explicit. They do not establish a measurement-scale covariance result.

### 3.2 Questions that remain unauthorized without full text

The accessible records do not establish:

- the spatial resolution of each modality;
- whether the same region was measured at multiple resolutions;
- whether `large-scale` was quantified by a correlation length or object-size statistic;
- whether EDX/SEM spatial scales were registered to optical maps;
- whether any point-spread function was measured or deconvolved;
- whether an autocorrelation, structure function, or power spectrum was calculated;
- whether nominal pixels were treated as independent observations.

No positive or negative R04 novelty conclusion is authorized from the abstract alone.

## 4. Claim-level synthesis

### Established before R04

The audited literature establishes:

1. HgCdTe composition, thickness, PL, and optical-path maps are finite-resolution observables.
2. Infrared microscope aperture can be varied and mapping is feasible from tens to hundreds of micrometres.
3. Map values can depend on edge conventions, thickness fits, optical constants, excitation power, collection efficiency, and modality.
4. Optical-path changes can be non-unique with respect to thickness, composition, and inclusions.
5. PL width and intensity can contain instrumental and excitation-dependent contributions.
6. Spatial feature-size estimates can be limited by pixel or spot resolution.
7. Composition regime can change which optical modality is reliable for gap/composition interpretation.

### Not established in the audited full texts

The two audited full texts do not establish:

1. a measured variance curve versus probe scale on the same specimen;
2. a kernel-filtered covariance equation applied to HgCdTe maps;
3. microscopic variance and correlation-length recovery from multiple resolutions;
4. an absolute-scale calibration floor on inferred correlation length;
5. a three-scale covariance-family falsification invariant;
6. an exact nonlinear calibration-posterior convolution;
7. finite-map effective sample counts or naive-variance bias;
8. cross-scale covariance of same-raster map statistics;
9. a multimodal latent-field prediction validated across independent operators.

### Current defensible R04 distinction

R04 must not claim novelty for spatial mapping, adjustable apertures, PL/transmission comparison, composition/cutoff uniformity statistics, optical-method disagreement, or localization at composition fluctuations.

The candidate distinct contribution is narrower:

> an explicit kernel-aware covariance, calibration, and finite-map information framework that states what finite-resolution HgCdTe maps identify; specifies the calibrated scales required to recover or falsify covariance parameters; and distinguishes nominal pixels, independent realizations, microscopic disorder, and modality-specific observables.

This is a candidate distinction, not an exhaustive novelty guarantee.

## 5. Gate disposition

The present audit is complete within its declared source-access boundary.

What is closed:

- the two highest-priority historical mapping papers were audited in full;
- established finite-aperture and spatially resolved mapping claims were removed from the candidate novelty set;
- Ruzhevich 2024 was identified, abstract-audited, and assigned an explicit unavailable-full-text state;
- the R04 claim boundary was narrowed accordingly.

What remains open at program level:

- full-text audit of Ruzhevich 2024 if a lawful copy becomes available;
- search for equivalent earlier aperture-sweep, spatial-covariance, structure-function, or resolution-dependent-variance analyses;
- experimental or public-data validation of the R04 framework.

The bounded audit does not authorize manuscript writing or a positive novelty declaration. It removes the unresolved source-acquisition state from the immediate R04 execution path while preserving it as a future literature update.
