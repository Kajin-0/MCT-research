# Decision record: R04/R05 evidence specification gate

**Date:** 2026-07-31  
**Controlling issue:** #395  
**Programs:** R04 primary; R05 dependent

## Decision

```text
GO_PUBLIC_DATA_AUDIT
```

This authorizes the bounded PR2 public-data feasibility audit defined in issue #395.

It does not establish that qualifying public data exist, that a facility or partner has accepted the experiment, or that R05 is reactivated.

## Question

Can the repository define a technically and scientifically sufficient evidence package for estimating

\[
g=\frac{\sigma_M\xi}{\hbar v_K}
\]

and testing the convolved R05 correlated model against the matched scalar null using one real near-critical HgCdTe specimen population?

## Reused foundations

R04 already provides:

- multiscale filtered-variance models;
- explicit PSF, pixel, and depth kernels;
- covariance-family alternatives;
- calibration-confounding results;
- finite-map effective information and bias;
- same-raster cross-scale covariance;
- joint identifiability and termination thresholds.

R05 already provides:

- the `M=Eg/2` convention;
- the matched one-point scalar null;
- the dimensionless controls `m` and `g`;
- an immutable one-dimensional effect benchmark;
- the nonuniversal threshold bracket `0.25<g<0.30` near zero mean mass;
- the final `REFRAME_AS_METHOD_BENCHMARK` decision and material reopening requirements.

No new random-mass solver was required for this gate.

## Deliverables completed

- normative evidence specification;
- source-ranked acquisition matrix;
- observability and identifiability memo;
- JSON Schema for matched spatial and spectroscopy evidence;
- nonclaiming machine-readable template;
- executable cross-field validator;
- deterministic validation tests;
- immutable machine-readable PR1 decision record.

## Source-ranked feasibility findings

### HgCdTe-specific methods

- Published HgCdTe STM/STS demonstrates feasibility but also reports tip-induced band bending and in-gap surface/pit contributions. These effects must be nuisance terms and falsification tests.
- HgCdTe/CdZnTe STEM-EDX studies demonstrate local composition profiling and nanometer-scale interface information, but destructive lamella geometry and same-population linkage remain limiting.
- High-resolution SIMS demonstrates process-related depth composition oscillations in HgCdTe, but not the required lateral covariance.
- Infrared microscope mapping can support wafer-scale region selection, but does not by itself establish a nanoscale correlation length.
- Near-critical structural and magneto-optical HgCdTe studies provide strong parameter and specimen-state leads, but not a matched local covariance plus local DOS record.

### Facility capabilities

Official Argonne and Oak Ridge user-facility pages document cryogenic UHV STM/STS systems compatible in principle with sub-meV to meV spectroscopy. NIST and university facility pages document sub-nanometer STEM chemical mapping and semiconductor APT capabilities.

Capability descriptions do not prove HgCdTe sample acceptance, survivability, quantitative Hg/Cd/Te accuracy, surface preparation success, or same-specimen compatibility.

## Structural result

The target products `m` and `g` are observable in principle only when:

1. local variance and correlation length are separated through multiple calibrated scales or a known full transfer function;
2. composition or gap is converted to signed mass with uncertainty;
3. spatial and spectroscopic observations share a specimen population;
4. the spectroscopy energy kernel is measured;
5. correlated and scalar models share the same one-point mass distribution and measurement kernel;
6. systematic uncertainty is not allowed to absorb the model difference.

The dominant bottleneck is external evidence quality, not missing analytical or numerical infrastructure.

## Preliminary public-data finding

No open record was identified in the PR1 search that already combines all of:

```text
near-critical HgCdTe
local 2D or 3D composition/signed-gap covariance
measured spatial transfer function
matched low-energy local spectroscopy
same-specimen or quantitative exchangeability metadata
raw data and calibration covariance
```

This result is preliminary. PR2 must conduct the source-by-source audit before returning `PUBLIC_DATA_FEASIBLE`, `PARTNER_DATA_REQUIRED`, or `EXTERNAL_DATA_BLOCKED`.

## Gate results

```text
specification gate                    PASS
machine-readable completeness         PASS
claim-boundary enforcement            PASS
plausible measurement modalities      PASS
qualifying public dataset             UNRESOLVED
confirmed partner experiment          UNRESOLVED
R05 material activation               BLOCKED
full-Kane necessity                   NOT DECISION CHANGING
```

## Authorized next work

PR2 may:

- search primary papers, supplementary files, and data repositories;
- contact or identify candidate data holders and facilities;
- score records against the schema;
- determine same-specimen compatibility and transfer-band coverage;
- return one of the predeclared public/partner data decisions.

PR2 may not:

- perform a larger R05 simulation;
- infer specimen parameters from figure-only values without uncertainty and transfer metadata;
- treat wafer tolerance as local `sigma_x`;
- promote source leads to material validation;
- authorize a manuscript or full-Kane disorder calculation.

## Stop rule

If no record can satisfy local variance, correlation length, same-population, and resolution requirements, return `PARTNER_DATA_REQUIRED` or `EXTERNAL_DATA_BLOCKED` and preserve R05 as a method benchmark.
