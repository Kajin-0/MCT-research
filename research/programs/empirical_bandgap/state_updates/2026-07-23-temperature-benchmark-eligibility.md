# R01 state addendum: temperature-benchmark eligibility

**Date:** 2026-07-23  
**Program:** R01 — empirical bandgap reconstruction  
**Parent benchmark:** #8  
**Issue:** #320

## Precedence

This addendum supersedes only R01 and benchmark statements that describe the specimen-level temperature-data inventory as wholly unavailable or imply that currently reconstructed temperature series may be pooled across operational measurement classes.

All source-specific decisions, uncertainty boundaries, and non-temperature evidence in the parent state remain unchanged.

## Current inventory

```text
E1-eligible temperature-series sources     4
committed observations                   167
specimen temperature series               21
exact operational measurement classes      4
maximum independent sources per class      1
```

The counted sources are:

```text
Seiler 1990   TPMA modified-Pidgeon-Brown gap
Chu 1991      absorption turning-point edge
Scott 1969    alpha=500 cm^-1 fixed-absorption edge
Schmit 1969   detector half-peak cutoff
```

Each ledger is auditable and specimen preserving. None shares an exact measurement class with another counted source.

## Controlling decision

```text
class_specific_single_source_benchmarks_only
```

```text
E1 all source ledgers eligible             true
E2 exact-class source holdout               false
E3 exact-class absolute ranking             false
E4 universal model advancement              false
```

## Scientific consequence

R01 now has enough reconstructed evidence for several source-bounded tests, but not for one universal experimental ranking.

Permitted source-specific roles remain:

- Seiler: TPMA thermal shape, sample-3 absolute series, and samples 3–5 low-temperature composition anchors;
- Chu: intercept-profiled absorption-turning-point thermal increments;
- Scott: fixed-alpha temperature slopes with deterministic figure bounds;
- Schmit: specimen-preserving detector-cutoff analyses.

These roles cannot be treated as folds of one observation class.

## Parent #8 status

The executable benchmark infrastructure is available and the provenance requirement is no longer wholly data-blocked. The decisive source-held-out ranking gate remains blocked because no exact class contains two independent sources.

The following work is not justified under the current graph:

- pooled fitting of the 167 observations;
- another universal polynomial;
- oscillator-scale optimization on heterogeneous classes;
- source-offset or free-composition-shift reconciliation;
- a winner table assembled from class-specific residuals;
- manuscript authorization.

## Reopening condition

Reopen the source-held-out benchmark only when public evidence supplies either:

1. a second auditable specimen-level temperature source in one existing exact operational class; or
2. an independently validated observation operator declared before pooling.

No email, direct message, author contact, institutional outreach, or private-data request is permitted.
