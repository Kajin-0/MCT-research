# R04 manuscript architecture decision

**Date:** 2026-07-23  
**Issue:** #330  
**Authorization dependency:** #327 / PR #329  
**Decision:** `ARCHITECTURE_READY_FOR_DRAFTING`

## Decision

The restricted R04 evidence can be organized as one coherent theory and
methodology article under a four-result and four-main-figure ceiling.

The paper is not a broad review and not a bundle of every R04 repository result.
Its argument is:

```text
finite measurement kernel
-> scale-dependent apparent variance
-> recoverability and absolute calibration limit
-> third-scale covariance-family closure
-> finite-map and same-raster information accounting
-> restricted real-map demonstration
-> measurement and reporting rules
```

## Authorized architecture

### Result group 1

Kernel-filtered variance, one- and two-scale recoverability, and the common
absolute scale-calibration floor.

### Result group 2

Three-scale Gaussian-family closure, supported Matérn alternatives, and
wrong-family parameter and fitting-convention dependence.

### Result group 3

Finite-map variance bias, effective information, and same-raster cross-scale
variance-estimator covariance.

### Result group 4

A restricted public CdSeTe PL peak-wavelength map demonstration showing strong
added-scale variance suppression, shared-raster dependence, and finite-field
sensitivity.

## Main figures

```text
Figure 1  kernel, recoverability, calibration
Figure 2  family closure and misspecification
Figure 3  finite-map and same-raster information
Figure 4  restricted CdSeTe demonstration
```

No fifth main figure is authorized. The composite-instrument stress grid,
operation-order calculations, allocation tables, joint uncertainty envelope,
and complete CdSeTe controls move to appendices or supplementary material.

## Claim-control result

The architecture contains a machine-readable ledger separating:

- established HgCdTe mapping prior art;
- established random-field, quadratic-form, and design mathematics;
- candidate integrated R04 contributions;
- synthetic design consequences;
- the cross-material real-map demonstration;
- explicit blocked claims.

Every positive claim records a stronger unsupported version that must not enter
the abstract, text, figures, captions, or conclusion.

## Abstract result

The abstract is constrained to six functions:

```text
problem
method
analytical result
real-map demonstration
limitation
practical consequence
```

It must state that the CdSeTe field is a cross-material method demonstration,
that numerical scales from one raster are dependent, and that no HgCdTe specimen
covariance family or physical correlation length is reported.

## Prior-art boundary

Finite-aperture mapping, adjustable apertures, spatial variation, and
PL/transmission mapping are established work. The manuscript may claim only the
candidate distinct integrated information and measurement-design hierarchy. The
bounded audit is not an exhaustive novelty guarantee.

## Real-data boundary

The Bowman Figure 3e field remains a Gaussian-fitted CdSeTe PL peak-wavelength
observation. It is not composition, intrinsic bandgap truth, or HgCdTe evidence.

The one-pixel held-out numerical scale is a closure diagnostic on a deterministic
transform of the same raster. It is not independent predictive validation.

The unknown native sample-plane kernel prevents physical correlation-length or
deconvolution claims.

## Drafting order

The technical and limitations sections should be drafted before the introduction
and abstract:

```text
measurement model
recoverability and calibration
closure and misspecification
finite-map information
real-map demonstration
limitations
introduction
design consequences
discussion and conclusion
abstract
```

This order reduces the risk that introductory novelty language outruns the
supported results.

## Files controlling the next tranche

```text
manuscript/r04/manuscript_architecture.md
manuscript/r04/claim_ledger.json
manuscript/r04/figure_plan.json
manuscript/r04/abstract_plan.json
```

## Continuing authorization

```text
full section drafting under the architecture    authorized
figure rendering from existing results          authorized
new scientific calculations                     not authorized
new data search                                  not authorized
fifth main figure                                not authorized
HgCdTe validation claim                          prohibited
physical correlation-length claim                prohibited
universal covariance-family claim                prohibited
R05                                              inactive
submission                                       not authorized
final pre-submission claim audit                 required
```
