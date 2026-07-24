# R06 Phase 1C low-temperature mobility gate

**Date:** 2026-07-24  
**Issue:** #346  
**Decision:** `SPECIMEN_CONDITIONED_ELECTRON_ANCHORS_ACCEPTED_UNIVERSAL_MOBILITY_CLOSURE_BLOCKED`

## Decision

Accept direct 77 K electron-mobility measurements only as specimen-conditioned anchors. Retain the established `mu_n=2e5 cm^2/(V s)`, `mu_p=500 cm^2/(V s)` detector pair only as a model-conditioned benchmark.

Do not authorize universal electron or hole mobility relations for predictive HgCdTe transport.

## Evidence accepted

- Wiley-Dexter 77 K electron-mobility measurements for seven specimens from `x=0.135` to `x=0.203`;
- measured mobility range of approximately `1.8e5` to `6.4e5 cm^2/(V s)` with carrier density retained;
- Elliott et al. variable-field evidence showing regime-dependent p-type electron/hole extraction;
- Smith 1984 and Iverson-Smith 1985 model consistency for the `2e5/500` benchmark pair;
- corrected identity of Yoo-Kwack as a 1997 theoretical calculation.

## Blocking evidence

- no accepted primary hole-mobility relation spanning detector-relevant composition and 77 K operation;
- no audited Scott equation and specimen domain;
- no equation-level Yoo-Kwack implementation;
- no correlated uncertainty model for composition, density, compensation and process dependence;
- no project-specific Hall data connected to the source classes.

## Authorization

Authorized:

- use of the Wiley table as immutable direct-measurement reference data;
- dimensionless sensitivity studies around explicitly labeled Tier B values;
- targeted recovery of Scott, Yoo-Kwack and primary hole-mobility sources;
- future source-conditioned uncertainty ensembles.

Not authorized:

- composition-only interpolation through the Wiley specimens;
- treating `2e5/500 cm^2/(V s)` as universal;
- averaging direct measurements and theoretical calculations;
- predictive responsivity, noise or detectivity claims based on nominal mobility values.

## Phase effect

The electron-mobility source gate is partially closed at the specimen-anchor level. The hole-mobility and predictive material-closure gates remain open.
