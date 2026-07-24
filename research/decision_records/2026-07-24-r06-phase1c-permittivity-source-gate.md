# R06 Phase 1C static-permittivity source gate

**Date:** 2026-07-24  
**Issue:** #346  
**Decision:** `STATIC_PERMITTIVITY_BENCHMARK_BRACKET_ACCEPTED_PRIMARY_ALLOY_FIT_LINEAGE_UNRESOLVED`

## Decision

Accept the common static-permittivity polynomial family only as a bounded architecture-level benchmark. Do not authorize a source-exact or predictive HgCdTe permittivity closure.

## Evidence accepted

- Baars-Sorger primary 77 K and 300 K reststrahlen spectra over `0<=x<=0.54`;
- composition-dependent optical-phonon modes suitable for Lyddane-Sachs-Teller checks;
- Tong-Ravindra traceability from dielectric composition curves to the Brice-Capper 1987 EMIS data review;
- consistent separation of low-frequency `epsilon_s` from high-frequency `epsilon_infinity`;
- the repeated static polynomial family with linear coefficient 15.5 or 15.6.

## Benchmark bracket

For `0<=x<=0.54` at the reference temperatures 77 K and 300 K:

```text
20.5 - 15.6*x + 5.7*x^2
    <= epsilon_s <=
20.5 - 15.5*x + 5.7*x^2
```

The midpoint may be used for architecture tests:

```text
epsilon_s,nominal = 20.5 - 15.55*x + 5.7*x^2.
```

The bracket is a transcription-lineage bracket, not a physical uncertainty interval.

## Blocking evidence

- the relevant Brice-Capper pages and original tabulated sources are not yet recovered;
- the 15.5 versus 15.6 coefficient difference is unresolved at the source page;
- physical composition and temperature uncertainty are unavailable;
- no source-controlled temperature law has been established;
- the high-frequency polynomial also exhibits a major secondary-source typographical variant.

## Authorization

Authorized:

- dimensionless Poisson and screening sensitivity calculations using the bracket;
- explicit reporting of lower, nominal, and upper benchmark results;
- primary-source reststrahlen reconstruction work.

Not authorized:

- predictive material simulations using a single exact permittivity value;
- extrapolation beyond the primary `x,T` support;
- substituting optical or oxide dielectric constants into Poisson's equation;
- interpreting the coefficient bracket as experimental uncertainty.

## Phase effect

The electrostatic architecture no longer lacks a declared benchmark range. The material-accurate permittivity gate remains open pending primary compiled-data recovery and physical uncertainty quantification.
