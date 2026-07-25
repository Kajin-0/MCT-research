# R06 Phase 1C decision — Kane parameter-validation design

**Date:** 2026-07-24  
**Controlling issue:** #346  
**Decision:** accept the validation architecture; keep the HgCdTe material closure blocked

## Decision

The project-defined simplified-Kane closure now has a formal parameter-
identifiability and external-evidence gate.

The numerical architecture is accepted for Phase 1C because it makes the scale
and nonparabolicity directions explicit, detects rank-deficient designs, and
prevents synthetic regression points from being mistaken for HgCdTe material
validation.

No material parameter value is accepted.

## Structural result

For

```text
n = N_* I_n(eta, alpha k_B T),
chi_mu = N_* I_chi(eta, alpha k_B T)/(k_B T),
Theta = I_n/I_chi,
```

`N_*` is an absolute scale parameter while `Theta` is independent of that scale.
Consequently:

- repeated density at one identical condition is rank one;
- density plus `Theta` can be rank two;
- matched density and compressibility can be rank two;
- unknown `eta` prevents direct use of a material point unless a validated
  neutrality model supplies it.

## Minimum material evidence

A future evidence set must contain at least:

1. three positive uncertainty-bearing HgCdTe points;
2. two provenance groups;
3. two temperatures;
4. one absolute density-scale observable;
5. one scale-free or matched shape observable;
6. primary or independently generated status for every point;
7. known `eta` or validated neutrality for every point.

These are necessary metadata requirements, not an automatic acceptance rule.

## Why three density points are insufficient

Density alone can trade off `N_*` and `alpha`, particularly when conditions do
not provide independent shape sensitivity.  Repetition improves precision along
an existing sensitivity direction but does not create a missing direction.

At least one compressibility-derived or scale-free observable is therefore
required.

## Temperature interpretation

The current closure accepts `N_*` and `alpha` directly and does not define their
composition or temperature dependence.  Multi-temperature design calculations
must therefore be interpreted as tests of a declared parameterization.

Material work must state whether parameters are:

- local to each `(x,T)` state;
- governed by a source-grounded functional relation; or
- replaced by a full secular model.

## Simplified versus full three-band model

The simplified closure may be retained only over a restricted declared domain
if future hold-out residuals are statistically consistent and show no systematic
composition or temperature structure.

A full three-band model is required if density and compressibility cannot be fit
consistently, neutrality requires omitted bands, or one simplified
nonparabolicity parameter cannot represent the accepted references.

## Accepted now

- weighted log-sensitivity analysis;
- SVD rank and conditioning diagnostics;
- Fisher matrix reporting;
- explicit external-evidence metadata contract;
- machine-readable minimum evidence policy;
- synthetic design studies;
- future fitting work that remains explicitly non-material until external
  evidence passes the gate.

## Not accepted

- an HgCdTe value of `N_*`;
- an HgCdTe value of `alpha`;
- a universal `N_*(x,T)` or `alpha(x,T)` law;
- heavy-hole or split-off-band closure;
- intrinsic neutrality;
- material chemical compressibility;
- screening length;
- detector coupling;
- predictive transport or noise claims.

## Gate status

```text
validation_design_accepted_material_closure_not_accepted
```

The machine-readable accepted-evidence list is empty.  The next scientific work
must acquire or recover actual HgCdTe validation points rather than expanding
the deterministic solver.
