# Decision record: R06 Phase 1C mobility and permittivity source gate

**Date:** 2026-07-24  
**Controlling issue:** #346  
**Decision:** proceed with benchmark-only controls; block predictive material closures

## Context

The deterministic R06 architecture now requires defensible electron mobility, hole mobility, and static-permittivity inputs before it can be described as material grounded. Existing literature entries include direct measurements, model-conditioned detector values, and later compiled polynomial forms. These categories must not be conflated.

## Evidence accepted

### Electron mobility

Wiley and Dexter (1969) is accepted as a direct specimen-conditioned measurement source near 77 K for low-composition HgCdTe. Its measurements remain attached to specimen composition, carrier density, temperature, and method.

Scott (1972) is accepted as composition-trend and scattering-model evidence. Its exact data and fitted equations remain pending primary transcription.

### Hole mobility

Elliott et al. (1972) is accepted as primary evidence that low-temperature p-type transport can contain multiple populations, impurity-band conduction, and regime-dependent extraction. The numerical table needed for a reusable anchor remains pending.

The `500 cm^2 V^-1 s^-1` value used by Smith (1984) is retained only as a Tier-B detector-model benchmark.

### Static permittivity

Baars and Sorger (1972) is accepted as primary reststrahlen and phonon-mode evidence over its reported composition and temperature domain.

The two repository quadratic curves are retained as a coefficient-lineage bracket. Their separation is not interpreted as total physical uncertainty.

## Decision

R06 may proceed with:

- specimen-conditioned electron-mobility anchors;
- a clearly labeled Tier-B hole-mobility benchmark;
- dimensionless electron-to-hole mobility-ratio studies;
- paired static-permittivity benchmark curves for Poisson and screening sensitivity;
- unresolved-parameter flags in any material-facing configuration.

R06 may not yet proceed with:

- a universal electron-mobility law;
- a universal hole-mobility law;
- a predictive static-permittivity closure;
- detector-performance predictions based on these inputs;
- uncertainty claims derived only from the difference between the two quadratic permittivity forms.

## Rationale

The available evidence supports numerical architecture and sensitivity analysis, but it does not establish transferable scalar material laws independent of specimen density, compensation, processing, temperature, and measurement regime.

In particular, the narrow difference between the two quadratic permittivity forms is a source-lineage ambiguity. Treating it as physical uncertainty would substantially understate unresolved model and specimen uncertainty.

## Required next evidence

1. Scott (1972) tables and fitted relations.
2. Elliott et al. (1972) Table I with population and regime labels.
3. Brice-Capper dielectric-property pages and their cited primary sources.
4. Baars-Sorger numerical oscillator data sufficient for an independent dielectric reconstruction.
5. A material uncertainty ensemble based on source scatter, covariance, or explicitly separated specimen classes.

## Consequence for Phase 1

This gate does not terminate R06. It supports a **proceed-with-restrictions** decision:

- deterministic and reduction studies remain authorized;
- material-grounded parameter closure remains incomplete;
- stochastic and predictive detector claims remain unauthorized.
