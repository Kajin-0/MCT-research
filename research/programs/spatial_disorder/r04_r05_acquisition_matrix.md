# R04/R05 source-ranked acquisition matrix

**Controlling issue:** #395  
**Status:** PR1 feasibility specification; no qualifying dataset is asserted

## Ranking convention

- **A:** primary HgCdTe evidence or an official user-facility capability directly relevant to the required observable;
- **B:** primary adjacent-material method evidence or HgCdTe evidence missing decisive metadata/raw data;
- **C:** vendor or secondary capability description useful only for planning;
- **D:** not decision capable for #395.

A modality can be technically capable yet scientifically nonqualifying because it cannot be matched to the spectroscopy record, cannot recover the required transfer function, or does not measure a signed gap or convertible composition field.

## Acquisition matrix

| Candidate path | Spatial/energy scale | What it can contribute | Principal limitation for #395 | Rank | PR1 disposition |
|---|---:|---|---|---|---|
| Cryogenic UHV STM/STS on a near-critical HgCdTe surface | atomic lateral sampling; instrument-dependent sub-meV to meV spectroscopy | local DOS, topography, spatially registered spectra, direct measurement kernel | HgCdTe surface preparation, tip-induced band bending, gap states, pits, charging, and surface/bulk mismatch | A | preferred spectroscopy path, conditional on surface-systematics controls |
| Aberration-corrected STEM-EDX on HgCdTe/CdZnTe lamellae | sub-nm probe; practical composition resolution depends on lamella, beam spreading, counts, and quantification | local Hg/Cd/Zn composition, interface width, nanoscale gradients | destructive cross-section; lamella transfer function; beam sensitivity; usually not the same region as STS; a line profile is not a 2D stationary covariance map | A | strong composition-metrology candidate; same-population gate remains difficult |
| Atom probe tomography on HgCdTe or an adjacent specimen | sub-nm three-dimensional elemental reconstruction in principle | local 3D composition, clustering, anisotropy, covariance candidates | destructive needle geometry; reconstruction and detection-efficiency biases; Hg/Cd/Te field-evaporation behavior must be validated; cannot perform STS afterward | B | high-information partner experiment, not yet HgCdTe-qualified in the audited sources |
| High-resolution SIMS depth profiling | nm-to-tens-of-nm depth sensitivity depending on method | depthwise composition oscillations and anneal response | primarily one-dimensional depth information; crater mixing and transfer function; insufficient lateral covariance; destructive | A | useful for growth-process oscillations, insufficient alone for R05 reopening |
| Infrared microscope mapping with transmission fitting | typically micron-scale lateral mapping | wafer-scale composition and thickness fields, macroscopic uniformity, candidate-region selection | transfer band is generally too coarse for the provisional 10–500 nm correlation-length target; optical inversion mixes thickness and composition | A | screening and specimen selection only |
| Magneto-optical spectroscopy on near-critical HgCdTe/HgCdTe quantum wells | meV-scale transitions under field | mean band parameters, Kane velocity, phase-transition placement | not a local DOS measurement; requires full-Kane magnetic forward model; normally lacks local covariance on the same region | A | supports parameter calibration, not the first discriminating observable |
| Photoluminescence or transmission mapping | diffraction-limited unless near-field implementation is used | gap proxy, broadening, wafer-scale uniformity | optical kernel, excitonic/carrier effects, nonlocal recombination, and inability to isolate signed local mass without a forward model | B | admissible only as calibrated auxiliary data |
| Conductive AFM or scanning spreading resistance | nm-to-tens-of-nm electrical mapping | local conductance variations and defect screening | conductance is not a unique composition or mass proxy; contact mechanics and surface state dominate | B | auxiliary only; cannot satisfy local-variance gate without calibration |
| Manufacturer or grower composition tolerance | wafer or boule summary | nominal process control | not a local standard deviation, covariance, or signed-gap map | D | explicitly prohibited as `sigma_x` evidence |

## HgCdTe-specific literature anchors

### STM/STS feasibility and failure modes

Wang et al., “Scanning tunneling spectra for the etched surface of p-type HgCdTe,” *Journal of Infrared and Millimeter Waves* 31 (2012), DOI `10.3724/SP.J.1010.2012.00222`.

The reported HgCdTe STS demonstrates technical feasibility but also reports a larger apparent gap attributed to tip-induced band bending and finite in-gap slope in etched pits. These are direct reasons to require band-bending, surface-state, pit, and preparation metadata rather than treating `dI/dV` as bulk DOS without qualification.

### STEM-EDX on HgCdTe/CdZnTe structures

The submicronic Laue-diffraction study of HgCdTe/CdZnTe heterostructures includes local Cd, Zn, and Hg STEM-EDX profiles on a lamella thinner than 100 nm and uses the profile to resolve multilayer composition. DOI `10.1107/S1600577520013176`.

Ballet et al., “MBE growth and interfaces characterizations of strained HgTe/CdTe topological insulators,” *Journal of Crystal Growth* 425 (2015), DOI `10.1016/j.jcrysgro.2015.02.046`, reports nanometer-scale interdiffusion and combined EDX-STEM morphology/composition information.

These works establish relevance of STEM-EDX to local Hg/Cd profiling. They do not establish that an unprocessed 2D near-critical mass covariance dataset exists.

### SIMS evidence for residual composition oscillations

Kopytko et al., “Impact of Residual Compositional Inhomogeneities on the MCT Material Properties for IR Detectors,” *Materials* 17 (2024), DOI `10.3390/ma17092190`, reports high-resolution SIMS identification of IMP-growth-related depth oscillations and their reduction after annealing.

The paper is evidence that process-related composition structure can occur. Its depth profiles are not a substitute for a lateral covariance map matched to spectroscopy.

### Infrared microscope mapping

“Composition and thickness distribution of HgCdTe molecular beam epitaxy wafers by infrared microscope mapping,” *Journal of Crystal Growth* 277 (2005), DOI `10.1016/j.jcrysgro.2005.01.051`, demonstrates automated composition/thickness mapping from infrared transmission.

This is useful for wafer-scale region selection and exchangeability studies, but its transfer band must be measured before it can inform nanoscale `xi`.

### Near-critical structural and magneto-optical characterization

Kießling et al., “Topological phase diagram of mercury cadmium telluride quantum wells,” *Physical Review Materials* 9, 054602 (2025), DOI `10.1103/PhysRevMaterials.9.054602`, combines detailed structural and magneto-optical measurements with `k·p` modeling across Cd content.

This is a strong source lead for mean band parameters and specimen-state conventions. It is not, by itself, a matched local covariance plus local DOS dataset.

## Official facility capability leads

### Argonne Center for Nanoscale Materials

The CNM lists a UHV millikelvin STM with approximately `0.3–0.4 K` operation and stated energy resolution below `0.5 meV`, plus low-temperature STM/STS and in-situ preparation systems. This is instrumentally compatible with the exploratory R05 `1–2 meV` design scale, subject to a HgCdTe-compatible surface workflow.

Official capability pages:

- `https://cnm.anl.gov/group/Quantum-and-Energy-Materials`
- `https://cnm.anl.gov/instruments`

### Oak Ridge Center for Nanophase Materials Sciences

CNMS lists atomic-resolution structural and spectral mapping from `40 mK` to room temperature, UHV preparation, cryogenic four-probe STM/STS, and a user proposal program. These capabilities make CNMS a plausible partner for surface preparation, STS, and correlated transport measurements.

Official capability pages:

- `https://www.ornl.gov/group/scanning-tunneling-microscopy`
- `https://www.ornl.gov/content/millikelvin-scanning-tunneling-microscopy-mk-stm`
- `https://www.ornl.gov/content/4-probe-scanning-tunneling-microscopy`

### NIST and university electron microscopy/APT facilities

NIST documents aberration-corrected STEM with sub-nanometer chemical mapping and APT development for three-dimensional semiconductor composition metrology. The University of Texas JEOL NEOARM page lists atomic-level EDXS/EELS mapping and external-user access. These are capability leads, not evidence of HgCdTe acceptance, specimen survivability, or quantified Hg/Cd/Te accuracy.

Official capability pages:

- `https://www.nist.gov/programs-projects/aberration-corrected-scanning-transmission-electron-microscopy`
- `https://www.nist.gov/programs-projects/atom-probe-tomography-nanostructured-semiconductor-materials-interfaces-and`
- `https://www.tmi.utexas.edu/facilities/instrumentation/jeol-neoarm-low-kv-stem-corrected`

## Preliminary public-data status

The PR1 search found source leads but no open record that already combines all decisive elements:

```text
near-critical HgCdTe
local 2D/3D composition or signed-gap covariance
measured spatial transfer function
matched low-energy local spectroscopy
same-specimen or justified exchangeability metadata
raw data and calibration covariance
```

A 2025 Zenodo record for mK transport on HgTe/HgCdTe thin films contains data and code metadata but is access restricted and does not advertise the required local covariance or STS fields (`10.5281/zenodo.15753791`). It is therefore not qualifying evidence for #395.

## PR2 search priorities

1. request supplementary/raw files from the 2025 near-critical HgCdTe quantum-well phase-diagram work;
2. contact HgCdTe groups with both growth/structural characterization and low-temperature spectroscopy capability;
3. determine whether the 2012 HgCdTe STS authors retain spatially indexed raw spectra and preparation metadata;
4. search HgCdTe STEM-EDX studies for raw spectrum images rather than figure-only line profiles;
5. assess whether adjacent lamella/Apt specimens can be made quantitatively exchangeable with a pre-STS region;
6. identify a user facility willing to accept Hg-containing material and support UHV surface preparation.

## PR1 decision

```text
GO_PUBLIC_DATA_AUDIT
```

This decision means that plausible measurement paths and source leads exist. It does not mean that a qualifying public dataset exists, that a partner has accepted the work, or that R05 is reactivated.
