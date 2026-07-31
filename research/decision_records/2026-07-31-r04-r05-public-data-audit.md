# Decision record: R04/R05 public-data audit

**Date:** 2026-07-31  
**Issue:** #395  
**Stage:** PR2 public-data feasibility audit  
**Decision:** `PARTNER_DATA_REQUIRED`

## Question

Does an accessible public dataset already contain the matched spatial-covariance and low-energy spectroscopy evidence required to evaluate the R05 method benchmark in a real near-critical HgCdTe specimen?

## Frozen qualification rule

A record qualifies only if it supports all eight gates:

```text
local variance
correlation length
same population
near critical
resolution
matched null
robustness
decision changing
```

The record must support the same one-point mass distribution and the same measured kernel in the correlated and scalar calculations. Figure digitization cannot replace raw transfer-function, calibration or specimen-linkage metadata.

## Audit result

The audit examined publisher records, supplementary materials, institutional repositories and general research-data repositories for HgCdTe/HgTe STM/STS, STEM-EDX, SIMS, infrared maps, magneto-optics, THz spectroscopy, transport and noise data.

Strong partial records exist:

- a 2025 near-critical HgCdTe quantum-well structural and magneto-optical series;
- a 2012 HgCdTe STM/STS study with explicit surface-systematic observations;
- HgCdTe/CdZnTe STEM-EDX and Laue profiling;
- high-resolution SIMS depth oscillations in detector material;
- wafer-scale infrared composition mapping;
- open RODARE HgTe spectroscopy data and code;
- restricted mK HgTe/HgCdTe transport data.

No record combines:

```text
near-critical specimen
local mass or convertible composition covariance
measured spatial transfer function
matched local low-energy spectroscopy
measured energy kernel
same-population linkage
raw calibration metadata
```

## Gate result

```text
local variance: FAIL
correlation length: FAIL
same population: FAIL
near critical: PARTIAL
resolution: FAIL
matched null: FAIL
robustness: FAIL
decision changing: FAIL
```

## Rejected decisions

### `PUBLIC_DATA_FEASIBLE`

Rejected because no candidate passes all eight gates. Combining unrelated article figures would violate the same-population rule and would not recover the missing transfer functions.

### `EXTERNAL_DATA_BLOCKED`

Rejected because the component measurements are technically demonstrated and identifiable groups and facilities provide plausible acquisition paths. Partner acceptance, archived-data retention and Hg-compatible workflows remain unconfirmed, but are not known to be impossible.

## Decision

```text
PARTNER_DATA_REQUIRED
```

## Consequence

R05 remains a method benchmark. Material reactivation, larger random-mass simulation, full 8-band spatial disorder and manuscript drafting remain unauthorized.

The next stage is a bounded acquisition campaign directed at:

1. archived spatially indexed HgCdTe STS;
2. raw Hg/Cd/Te composition maps or spectrum images;
3. the 2025 near-critical quantum-well specimen group;
4. a coordinated cryogenic STS plus local-composition facility workflow;
5. explicit specimen identity and transfer-function metadata.

Return `EXTERNAL_DATA_BLOCKED` only after the plausible partner paths are explicitly unavailable, data are no longer retained, Hg handling is rejected, or the required same-population workflow is technically infeasible.

## Claim boundary

The absence of a qualifying public dataset does not falsify correlated-random-mass physics. It establishes that the material claim cannot presently be tested from public evidence under the predeclared standards.
