# R04 external-evidence state overlay

**Program:** R04 — Measurement-kernel-aware spatial disorder  
**Controlling issue:** #405  
**Predecessor:** PR #404  
**State:** `PAUSED_UNTIL_NEW_MATCHED_DATA`  
**Evidence decision:** `EVIDENCE_GATE_FAILED`

This file is the authoritative overlay for the external-validation branch of R04. It does not replace the analytical and synthetic results preserved in `state.md`.

## Retained result

R04 remains a validated method and experimental-design framework for:

- finite lateral and depth measurement kernels;
- scale-calibration limits;
- covariance-family falsification and misspecification;
- multiscale allocation and joint identifiability;
- correlated finite-map sampling;
- same-raster cross-scale covariance;
- observation-operator and instrument uncertainty propagation.

The bounded literature package in PRs #401–#404 adds design targets, stress cases, a kernel-method benchmark, and STM artifact diagnostics. These are not specimen-level local-disorder measurements.

## External-evidence result

No qualifying source supplies one near-critical specimen, or one quantitatively justified exchangeable population, with all of:

1. local signed-gap/mass variance or convertible local composition variance;
2. identifiable lateral correlation length after measured transfer-function correction;
3. matched low-energy spectroscopy;
4. a measured spectroscopy energy-resolution kernel;
5. same-population linkage and sufficient specimen metadata.

Therefore R04 does not support a specimen-specific variance, correlation length, covariance family, or coupled spatial/spectroscopic claim.

## Authorization state

```text
outreach:                     DISABLED
new required literature search: NO
matched-data ingestion:       BLOCKED
specimen-level inference:     BLOCKED
manuscript authorization:     DENIED
```

No further synthetic refinement is authorized merely to compensate for absent evidence.

## Reopening condition

Reopen this external-validation branch only when genuinely new matched data satisfy the acquisition schema from issue #395. Reopening must begin with immutable evidence ingestion, transfer-function validation, and same-population verification.

A larger simulation, a new assumed prior, figure-only cross-paper synthesis, or a nominal instrument specification is not a reopening event.
