# Decision record: Scott 1969 fixed-alpha temperature coefficient

**Date:** 2026-07-23  
**Program:** R01 — empirical bandgap reconstruction  
**Issue:** #312  
**Source tranche:** PR #304 / merge `06a2a9c526e2967850d7c1f323ce28a76f479917`

## Decision

```text
non_identifiable_at_figure_precision
```

The reconstructed Scott 1969 Figure 2 temperature series do not support either a positive Hansen-compatibility decision or a resolved fixed-alpha observation-specific correction.

## Evidence object

```text
path
  data/validation/scott1969_temperature_coefficient_test.json

source CSV SHA256
  6fd672cb9469d16d0dce2dc4657af99391e1652b79a2e59cd4661d03bdebc851

candidate workflow run
  29974393772

candidate artifact
  8550871821

candidate artifact digest
  sha256:1c0568e17bd27a0f3970466d62d5faf9d71bd2769aba34d67d0b90f7d96b279a

committed JSON SHA256
  2137d0e1e5cbd594b36b069b54449e4603f756904d7b6f61041673960ebaf5e3
```

The workflow generated the compact result twice and compared the files byte-for-byte before publication.

## Observation boundary

The source observable remains

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse
```

with

```text
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
pointwise_experimental_covariance = not_reported
```

The `+/-1.75 K`, `+/-4.7 meV`, and `+/-0.005 in x` quantities are bounded coordinate or source-precision sensitivities. They are not treated as Gaussian standard deviations.

## Models

```text
S0  independent centered linear slope for each specimen
S1  b(x) = b0 + b1 x with an unconstrained intercept per specimen
SH  b_H(x) = 5.35e-4 (1 - 2x) eV/K with an unconstrained intercept per specimen
```

No absolute composition-polynomial term is evaluated.

## Full central trend

Across all nine specimens,

```text
S1 b0 =  5.49783543e-4 eV/K
S1 b1 = -1.076209537e-3 eV/K per x

SH b0 =  5.35e-4 eV/K
SH b1 = -1.07e-3 eV/K per x.
```

The central coefficients are numerically close. That proximity does not pass the predeclared gate:

```text
full S1 maximum normalized box residual  1.483597188054
full SH maximum normalized box residual  1.820916077360
full S1 held-out maximum                 2.305028838147
full SH held-out maximum                 1.820916077360.
```

## Controlling core

The controlling unflagged within-range subset is

```text
x = {0.23, 0.31, 0.35, 0.405, 0.46}
41 markers
5 specimens.
```

Results:

```text
S1 b0                                    6.03872734e-4 eV/K
S1 b1                                   -1.235286852e-3 eV/K per x
S1 maximum normalized box residual       1.418088512811
S1 maximum held-out box residual         1.628014211258
S1 complete box feasibility              false

SH maximum normalized box residual       1.820916077360
SH maximum held-out box residual         1.820916077360
SH complete box feasibility              false.
```

Hansen's coefficient pair remains inside the nonprobabilistic S1 linearized box-sensitivity envelope:

```text
b0 in [ 3.91485115e-4,  8.16260353e-4] eV/K
b1 in [-1.809474839e-3, -6.61098865e-4] eV/K per x.
```

## Gate evaluation

```text
S1_core_box_feasible                            false
S1_core_leave_one_specimen_out_box_feasible     false
SH_core_box_feasible                            false
SH_core_leave_one_specimen_out_box_feasible     false
Hansen outside S1 sensitivity envelope          false
Hansen monotone residual-sign pattern           false
```

Therefore:

- `Hansen-compatible` is not authorized because SH fails both core gates.
- `observable-specific correction required` is not authorized because S1 also fails both core gates and Hansen is not excluded by the sensitivity envelope.
- the fail-closed residual category is `non_identifiable_at_figure_precision`.

## Scientific interpretation

The source figure contains a real composition-dependent thermal trend, and the all-specimen central fit happens to be close to Hansen. The marker-resolution and within-specimen deviations are too large to determine whether the Hansen coefficient is correct for this fixed-alpha observation or whether a distinct observation-specific coefficient is required.

The coefficient sensitivity is dominated by marker-energy extraction rather than Scott's density-composition precision. Further polynomial flexibility would fit publication-coordinate detail without resolving the observation operator or measurement covariance.

## Portfolio consequence

R01 gains a numerical, specimen-preserving fixed-alpha temperature-series result, but not a new production gap law.

The Scott path should now stop. Reopening requires a materially higher-resolution or source-native numerical record with adequate uncertainty semantics. It must not be reopened by:

- adding nonlinear temperature terms;
- sampling Scott Equation (3) or Figure 5 curves;
- substituting fit-required compositions;
- treating extraction bounds as statistical covariance;
- pooling another measurement class to manufacture precision.

## Authorization state

```text
Scott fixed-alpha central slopes              validated
Scott deterministic box qualification         validated
Scott leave-one-specimen-out test             validated
Hansen temperature coefficient compatibility  unresolved
fixed-alpha correction coefficient             unresolved
absolute Hansen polynomial validation          not authorized
new universal HgCdTe equation                  not authorized
manuscript or production equation              not authorized
```
