# R04/R05 terminal evidence disposition

## Decision

```text
EVIDENCE_GATE_FAILED
R05_REACTIVATION_NOT_RECOMMENDED
```

The repository has reached the stop condition defined by issue #395. No qualifying matched data exist in the audited public and user-supplied literature, and outreach is disabled by user direction.

This is an evidence disposition. It is not a negative physical result.

## What is established

The repository contains a tested R04 measurement-kernel and spatial-inference framework and a tested R05 one-dimensional matched-null method benchmark. The primary-literature tranche adds four bounded roles:

```text
DESIGN_TARGET
DRIFT_STRESS_CASE
KERNEL_METHOD_BENCHMARK
STM_ARTIFACT_ENVELOPE
```

These roles improve experiment design, method validation, and rejection criteria. They do not create a specimen-level data product.

## Why every matched-data gate fails

### Local variance

No source supplies local signed-gap or mass variance for a near-critical specimen. Chang wafer-map standard deviations mix nonstationary macroscopic drift with any local fluctuation and cannot be promoted to nanoscale random-mass variance.

### Correlation length

No lateral covariance or PSD is available with enough raw spatial information and a measured transfer function to identify a material correlation length. Biquard's 580 nm pseudo-Voigt response is a measured cross-sectional depth-response benchmark, not a lateral material correlation length.

### Same population

The near-critical QW series, wafer maps, micro-Laue profiles, and STM specimens are unrelated specimen classes. Combining them would create a fictitious specimen.

### Near critical

Bovkun provides a useful near-critical design envelope, but not matched spatial covariance and local spectroscopy on those samples.

### Resolution

No matched low-energy spectroscopy record includes a measured effective energy-resolution kernel. Bovkun's `2 meV*sqrt(B[T])` broadening is a model convention, and Zha does not report the required spectroscopy kernel.

### Matched null

The R05 correlated-versus-scalar matched-null test cannot be applied to real evidence without a measured one-point mass distribution, spatial correlation, and matched spectroscopy.

### Robustness

Covariance-family, instrument, calibration, background, surface, and prior sensitivity cannot be evaluated at specimen level without the missing matched data.

### Decision changing

The present evidence cannot determine whether a higher-dimensional or full-Kane disorder calculation would change a material conclusion. Such calculations remain unauthorized.

## Retained assets

No code, theorem, numerical benchmark, literature extraction, or provenance record is discarded. The retained assets are available for immediate application if a future matched dataset appears.

## Program state

```text
R04 method framework:             RETAINED
R04 external validation:         PAUSED_UNTIL_NEW_MATCHED_DATA
R04 specimen-level claim:        NOT_SUPPORTED
R04 manuscript authorization:    DENIED
R05 method benchmark:             RETAINED
R05 material activation:         BLOCKED
R05 full-Kane calculation:       NOT_AUTHORIZED
```

## Reopening protocol

A reopening event requires genuinely new matched data from one specimen or a quantitatively justified exchangeable population. The minimum package must include:

1. local signed-gap/mass variance, or composition with uncertainty-propagated conversion;
2. lateral correlation length identifiable after measured transfer-function correction;
3. matched low-energy spectroscopy;
4. measured spectroscopy energy-resolution kernel;
5. near-critical metadata and same-population linkage.

The first action is immutable evidence ingestion and validation. A larger simulation, full-Kane calculation, assumed prior, nominal instrument specification, or cross-paper synthesis is not a reopening event.
