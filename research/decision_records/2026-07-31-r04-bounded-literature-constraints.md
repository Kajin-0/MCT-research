# Decision record: bounded R04 literature constraints

**Date:** 2026-07-31  
**Controlling issue:** #403  
**Predecessor:** #400 and PRs #401–#402  
**Decision:** `BOUNDED_CONSTRAINT_PACKAGE_READY`

## Context

The completed literature recovery supplied four kinds of useful information:

1. a near-critical HgCdTe QW composition-thickness series;
2. wafer-scale composition nonuniformity summaries;
3. an experimentally inferred cross-sectional spatial response;
4. HgCdTe-specific STM/STS artifact magnitudes.

None of the sources supplies the complete matched evidence package required by R04/R05. Combining them as one specimen or one statistical population would be invalid.

## Decision

Translate the literature into a machine-readable, deterministic constraint package with explicit semantic roles:

```text
DESIGN_TARGET
DRIFT_STRESS_CASE
KERNEL_METHOD_BENCHMARK
STM_ARTIFACT_ENVELOPE
```

Do not assign probability distributions to the extracted values. Do not treat design envelopes or stress cases as measured local-disorder priors.

## Accepted constraints

- Bovkun QW boundary-design points: `(x, d) = (0.052, 10.3 nm)` and `(0.054, 10.2 nm)`.
- Chang drift stress cases: `sigma_x = 0.0006`, `0.0008`, and `0.0042`, with a full-map/center ratio of `5.25`.
- Biquard kernel benchmark: measured pseudo-Voigt depth-response FWHM `580 nm`, Lorentzian fraction `0.20`, versus nominal `500 nm`.
- Zha artifact envelope: apparent plateau excess `0.13 eV`, apparent/bulk gap ratio `1.4815`, and bias-dependent apparent pit-depth change `20–30 nm`.

## Rejected interpretations

- Bovkun composition range as a probability or confidence interval.
- Bovkun model broadening as a measured spectroscopy kernel.
- Chang wafer sigma as local random-mass variance.
- Biquard depth-response FWHM as lateral material correlation length.
- Zha apparent gap as calibrated local DOS or a universal TIBB correction.
- Zha single-bias topography as geometric surface height.
- Any cross-paper same-specimen synthesis.

## Consequences

The package may be used for:

- specimen-selection planning;
- deterministic drift and artifact stress tests;
- validation of response-matched modality comparison;
- measurement metadata and exclusion requirements.

The package does not authorize:

- matched experimental data ingestion;
- new or larger random-mass simulation;
- R05 material activation;
- full 8-band spatial-disorder computation;
- manuscript-level validation claims.

## Reopening condition

The decision may be revisited only when a new source provides raw or sufficiently digitizable same-population evidence for local lateral covariance, local low-energy spectroscopy, and measured spatial and energy kernels.
