# R04/R05 literature ingestion batch 001

**Controlling issue:** #400  
**Source mode:** user-supplied published papers only  
**Batch decision:** `PARTIAL_REANALYSIS_FEASIBLE`  
**R05 material activation:** blocked

## Sources received

1. Y. Chang et al., *Composition and thickness distribution of HgCdTe molecular beam epitaxy wafers by infrared microscope mapping*, Journal of Crystal Growth 277, 78-84 (2005), DOI `10.1016/j.jcrysgro.2005.01.051`.
2. F. X. Zha et al., *Implication of exotic topography depths of surface nanopits in scanning tunneling microscopy of HgCdTe*, Applied Physics Letters 101, 141604 (2012), DOI `10.1063/1.4756938`.

The supplied PDFs are not committed. Their SHA-256 digests and bibliographic identities are preserved in the machine-readable record.

## Executive result

Neither paper contains the matched evidence required by #395. Together they materially improve two different nuisance-model components:

- Chang et al. constrain **coarse wafer-scale composition/thickness nonuniformity and the infrared-map measurement footprint**.
- Zha et al. constrain **HgCdTe-specific STM/STS artifacts**, especially tip-induced band bending, transport-limited tunneling, pit gap states, and non-geometric apparent topography.

The papers must remain separate. They describe different materials, growth methods, specimen states, spatial scales, and observables. Combining them into a synthetic matched specimen is prohibited.

## 1. Chang et al. — infrared microscope mapping

### Measurement chain

The HgCdTe layers were grown by MBE in a Riber 32P chamber. Transmission maps were acquired with a Thermo Nicolet Centaurus infrared microscope coupled to a Thermo Nicolet 870 FTIR. The reported stage-position precision is 1 um. The aperture could be reduced to 25 um at a 10 um wavelength, but the mapping measurements used a 100 um aperture to increase signal and reduce acquisition time.

The 100 um aperture is a stated integration footprint. It is not a measured optical point-spread function. The paper does not report the actual point-sampling pitch, raw point coordinates, repeated scans, or a PSF/MTF calibration.

Composition and thickness were fitted simultaneously using an interference-matrix transmission model, Levenberg-Marquardt minimization, and simulated annealing. The absorption edge was defined at `alpha = 1000 cm^-1`, and composition was obtained with the Hansen relation

```text
Eg = -0.302 + 1.93 x - 0.81 x^2 + 0.832 x^3
     + 5.35e-4 (1 - 2 x) T.
```

The stopping thresholds `delta x < 0.0001` and `delta d < 0.01 um` are numerical convergence criteria, not measurement uncertainties.

### CdZnTe-substrate specimen

```text
substrate:                  (211)B CdZnTe
mapped extent:              approximately 16 x 18 mm
mean x:                     0.2182
reported standard deviation:0.0006
relative standard deviation:0.27%
reported cutoff at 77 K:    11.03 um
cutoff standard deviation:  0.09 um
mean HgCdTe thickness:      7.84 um
thickness standard deviation:0.03 um
relative thickness deviation:0.38%
```

The figures show higher Cd composition in small corner regions and lower thickness in the same regions. The authors attribute this to corner heating, reduced Hg sticking, and substrate geometry. This is evidence of a deterministic, nonstationary wafer-scale field rather than a demonstrated stationary random field.

### CdTe/Si specimen

```text
substrate:                  (211)B CdTe/Si, 3-inch wafer
mapped extent:              66 x 20 mm
mean x:                     0.2340
reported standard deviation:0.0042
relative standard deviation:1.8%
reported cutoff at 77 K:    9.0 um
cutoff standard deviation:  0.46 um

central 20 x 20 mm:
mean x:                     0.2299
reported standard deviation:0.0008
relative standard deviation:0.35%
reported cutoff at 77 K:    9.45 um
cutoff standard deviation:  0.09 um

mean HgCdTe thickness:      7.15 um
thickness standard deviation:0.07 um
relative thickness deviation:0.56%
```

The large difference between the full-area and central-area composition standard deviations demonstrates that a single wafer-wide sigma is dominated by edge-to-center drift. It cannot be interpreted directly as local random-alloy variance.

### Reanalysis boundary

The plotted maps can support a bounded, explicitly figure-derived digitization of:

- coarse center-to-edge composition and thickness trends;
- approximate long-wavelength spatial structure;
- qualitative or coarse composition-thickness anticorrelation.

They cannot support:

- 10-500 nm covariance;
- a stationary local variance;
- a reliable correlation length below the map sampling and 100 um integration footprint;
- separation of material covariance from the unmeasured optical PSF;
- raw-data uncertainty propagation.

### Evidence gates

```text
local variance:      PARTIAL
correlation length:  FAIL
same population:     FAIL
near critical:       FAIL
resolution:          PARTIAL
matched null:        FAIL
robustness:          FAIL
decision changing:   PARTIAL
```

Chang et al. is useful for an R04 coarse-map stress test and for demonstrating the need to remove deterministic wafer trends before covariance inference. It is not R05 material evidence.

## 2. Zha et al. — nanopit STM/STS

### Specimen and preparation

```text
material:            vacancy-doped p-type Hg0.73Cd0.27Te
composition x:       0.27
reported Eg at 300 K:0.27 eV
growth:              liquid phase epitaxy
substrate:           CdZnTe
hole concentration:  3.0e16 cm^-3 at 77 K
surface preparation: Br2/methanol etch, pure methanol rinse
instrument:          Omicron UHV STM
base pressure:       approximately 1e-10 mbar
STM temperature:     not reported
```

Instrument calibration was checked against atom-resolved graphite, Au(111) terrace height, and carbon-nanotube height on gold. Those checks constrain scanner calibration but do not establish an energy-resolution kernel.

### Bias-dependent apparent topography

The same areas were imaged at `+0.4 V` and `-0.4 V` with a `0.8 nA` setpoint. Reported effects include:

- apparent pit-depth differences of approximately 20-30 nm between bias polarities;
- an approximately 30 nm apparent height step over flat regions when the bias polarity was switched during a scan;
- protrusion heights of approximately 34 and 13 nm that remained nearly unchanged while the surrounding baseline shifted.

The paper interprets the effect as a combination of transport-limited tunneling, tip-induced band bending, very small tunneling gaps, and tip-surface force effects. The practical conclusion is strong: **HgCdTe STM topography at a single bias cannot be presumed geometric**.

### Spectroscopy systematics

Flat-region I-V curves show a roughly `0.40 eV` zero-current plateau, compared with the reported `0.27 eV` bulk gap. The approximately `0.13 eV` excess is attributed to tip-induced band bending.

The pit spectra are different:

- pits A-C show finite slopes through the nominal gap, attributed to high densities of gap states;
- pit D shows a plateau approximately equal to the reported band gap;
- the plotted pit traces are vertically shifted for display.

The authors report approximately `2.5 nA` and `0.8 nA` at the two bias polarities, approximately a 3:1 ratio. Their model gives an approximately 60% current decrease when switching polarity at a fixed 0.9 nm gap and recovers the current by reducing the assumed tunneling gap from 0.9 to 0.2 nm.

### Missing spectroscopy metadata

The paper does not report:

- STM/STS measurement temperature;
- lock-in modulation amplitude or frequency;
- a dI/dV acquisition protocol;
- energy-axis calibration uncertainty;
- a measured effective energy-resolution kernel;
- raw spatially indexed spectra.

The curves therefore cannot be interpreted as quantitatively deconvolved local DOS.

### Reanalysis boundary

Figure digitization can support nuisance-model bounds for:

- apparent topographic changes under bias reversal;
- flat-region versus pit I-V behavior;
- a lower bound on TIBB-induced apparent-gap inflation;
- gap-state contamination in pit regions.

It cannot support:

- local mass/composition covariance;
- a measured DOS kernel;
- deconvolved local DOS;
- geometric pit depths from one bias polarity;
- same-population linkage to the Chang wafer maps.

### Evidence gates

```text
local variance:      FAIL
correlation length:  FAIL
same population:     PARTIAL
near critical:       FAIL
resolution:          FAIL
matched null:        FAIL
robustness:          PARTIAL
decision changing:   PARTIAL
```

Zha et al. is decision-relevant because it invalidates a naive interpretation of HgCdTe STM topography and apparent spectral gaps. It does not provide the near-critical matched data required to reopen R05.

## Aggregate decision

```text
PARTIAL_REANALYSIS_FEASIBLE
```

This decision means that selected figures may be digitized for bounded R04 nuisance-model and observability studies. It does not authorize physical validation, data fusion across papers, or R05 material activation.

No source in this batch provides:

```text
near-critical specimen
10-500 nm local covariance
measured spatial transfer function
matched low-energy spectroscopy
measured energy-resolution kernel
same-specimen linkage
raw calibration metadata
```

## Next papers requested

Priority remains:

1. `10.1103/PhysRevMaterials.9.054602` — near-critical HgCdTe quantum-well series.
2. `10.3724/SP.J.1010.2012.00222` — etched p-type HgCdTe tunneling spectra.
3. `10.1107/S1600577520013211` — Laue/SIMS/STEM-EDX spatial profiling.

## Stop rule

Do not:

- treat Chang's wafer-map sigma as nanoscale random-mass variance;
- treat the 100 um aperture as a measured PSF;
- infer a correlation length from contour smoothing;
- treat Zha's single-bias topography as geometry or composition;
- infer an energy kernel from the reported bulk gap or bias range;
- combine the two papers into a fictitious matched specimen;
- reactivate R05 from figure-derived constraints.
