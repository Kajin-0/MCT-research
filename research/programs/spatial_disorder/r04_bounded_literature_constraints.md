# R04 bounded literature constraint package

**Controlling issue:** #403  
**Predecessor:** #400 and PRs #401–#402  
**Decision:** `BOUNDED_CONSTRAINT_PACKAGE_READY`  
**R05 material activation:** `BLOCKED`

## Purpose

The recovered papers improve experimental design and model checking, but they do not provide a measured local-disorder distribution or a matched covariance-plus-spectroscopy dataset. This package therefore assigns every quantitative result one of four semantic roles:

```text
DESIGN_TARGET
DRIFT_STRESS_CASE
KERNEL_METHOD_BENCHMARK
STM_ARTIFACT_ENVELOPE
```

These are deterministic constraints. None is assigned a probability distribution.

## 1. Near-critical QW design target

Bovkun et al. provide a controlled approximately 10 nm Hg1-xCdxTe quantum-well series spanning the observed topological transition. The two samples nearest the reported boundary are:

| Cd fraction x | QW thickness |
|---:|---:|
| 0.052 | 10.3 nm |
| 0.054 | 10.2 nm |

The package freezes these as a **joint specimen-selection envelope**, not as a confidence interval or local composition distribution.

Allowed uses:

- choose discrete design points near the reported QW transition;
- retain composition and thickness jointly;
- stratify future measurements by actual specimen calibration.

Prohibited uses:

- infer a continuous probability law over x;
- equate the QW boundary with the bulk HgCdTe critical composition;
- infer local composition variance or lateral covariance.

The paper's Gaussian broadening convention,

```text
sigma(B) = 2 meV * sqrt(B[T]),
```

is retained only to reproduce that calculation. It is not an STS energy-resolution kernel or measured linewidth.

## 2. Wafer-scale drift stress cases

Chang et al. report three useful composition nonuniformity summaries:

| Case | Reported sigma_x | Spatial context |
|---|---:|---|
| CdZnTe whole map | 0.0006 | 16 x 18 mm map |
| CdTe/Si center | 0.0008 | central 20 x 20 mm |
| CdTe/Si full scan | 0.0042 | 66 x 20 mm |

The full-scan to center-only ratio is:

```text
0.0042 / 0.0008 = 5.25
```

This large region dependence is itself the useful result: deterministic edge-to-center structure materially changes the reported sigma. The values are therefore encoded as **drift stress cases**, not random-mass amplitudes.

The mapping used a 100 um aperture. That aperture is an integration footprint, not a measured PSF. The paper does not report raw coordinates, an explicit sampling pitch, repeated maps, or a calibrated spatial response.

Authorized tests:

- detrending sensitivity;
- center-versus-full-region sensitivity;
- failure of stationary covariance estimators under deterministic drift;
- composition-thickness anticorrelation diagnostics.

No nanoscale variance or correlation length may be inferred from these values.

## 3. Spatial-kernel method benchmark

Biquard et al. directly infer a micro-Laue depth-response kernel from the Hg fluorescence transition at an abrupt interface:

```text
nominal beam diameter: 500 nm
measured FWHM:         580 nm
kernel family:         pseudo-Voigt
Lorentzian fraction:   0.20
measured/nominal:      1.16
```

The decisive methodological result is that the higher-resolution SIMS and STEM-EDX profiles are convolved with the measured 580 nm response before comparison with micro-Laue strain.

This is a valid **kernel-method benchmark** for R04. It demonstrates that nominal spot size is insufficient and that modality comparison must occur after response matching.

It is not:

- a lateral correlation length;
- a 2D composition covariance measurement;
- a universal PSF for unrelated instruments;
- a measurement on the Bovkun near-critical QW series.

## 4. HgCdTe STM artifact envelope

Zha et al. provide HgCdTe-specific tunneling and topography failure cases:

```text
reported bulk gap:                  0.27 eV
flat-region zero-current plateau:   0.40 eV
apparent excess:                    0.13 eV
apparent/bulk ratio:                1.4815
bias-dependent apparent pit change: 20-30 nm
imaging conditions:                 +/-0.4 V, 0.8 nA
```

The paper attributes the enlarged apparent gap to tip-induced band bending and the bias-dependent topography to transport limitation and tip-surface interaction. Pit spectra can contain dense in-gap states.

These values form an **STM artifact envelope**, not a correction model. They require future workflows to:

- record temperature and modulation settings;
- measure or bound the effective energy-resolution kernel;
- repeat topography under both bias polarities;
- separate flat regions, pits, and protrusions;
- model or bound tip-induced band bending and transport limitation.

The 0.13 eV excess must not be subtracted universally, and a single-bias topograph must not be converted directly into geometry or composition.

## Frozen unsupported quantities

The literature set does not determine:

```text
local random-mass variance
lateral correlation length
measured STS energy-resolution kernel
same-specimen covariance-to-DOS linkage
probability distribution for local composition or mass
validated matched-null effect size
```

## Decision

The translation is scientifically unambiguous only when semantic roles remain explicit. The package is therefore ready for use in experiment planning, pipeline validation, and deterministic stress testing.

It does not authorize matched-data ingestion, a larger random-mass simulation, R05 activation, full 8-band spatial-disorder work, or a manuscript-level experimental claim.
