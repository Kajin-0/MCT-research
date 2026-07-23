# R01 state addendum: Scott 1969 fixed-alpha temperature coefficient

**Date:** 2026-07-23  
**Program:** R01 — empirical bandgap reconstruction  
**Issue:** #312  
**Source reconstruction:** Issue #303 / merged PR #304

## Precedence

This addendum supersedes only the Scott 1969 subsection and Scott-specific roadmap statements in `research/programs/empirical_bandgap/state.md` that describe Figure 2 numerical reconstruction as blocked.

All non-Scott source histories, decisions, limitations, and roadmap entries in the parent state file remain unchanged.

## Current Scott evidence state

```text
source PDF SHA256
7b2e5790745897ecd75bd22134e5d9293397820c3b7851eb5a9e648a5c441324

Figure 2 marker CSV SHA256
6fd672cb9469d16d0dce2dc4657af99391e1652b79a2e59cd4661d03bdebc851

70 direct Figure 2 markers
9 measured-composition specimen series
17 axis-calibration references
0 Figure 5 numerical observations
0 Equation (3) curve samples
0 fitted source-equation parameters
```

Every admitted point remains classified as

```text
fixed_absorption_optical_edge_alpha_500_cm_inverse
signed_gap_eligible = false
intrinsic_gap_eligible_without_observation_operator = false
pointwise_experimental_covariance = not_reported
```

The coordinate-extraction half-widths are `+/-1.75 K` and `+/-4.7 meV`. Scott's density-composition precision is `+/-0.005` in fractional `x`. These are deterministic sensitivity bounds, not Gaussian standard deviations.

## Temperature-slope result

The compared models are

```text
S0  independent centered linear slope per specimen
S1  b(x) = b0 + b1 x, with a free intercept per specimen
SH  b_H(x) = 5.35e-4 (1 - 2x) eV/K, with a free intercept per specimen
```

Across all nine specimens, the S1 central coefficients are

```text
b0 =  5.49783543e-4 eV/K
b1 = -1.076209537e-3 eV/K per unit x
```

and are numerically close to the Hansen coefficients

```text
b0,H =  5.35e-4 eV/K
b1,H = -1.07e-3 eV/K per unit x.
```

That numerical proximity does not pass the predeclared deterministic box or held-out gates.

For the controlling unflagged within-range core

```text
x = {0.23, 0.31, 0.35, 0.405, 0.46}
41 markers
5 specimens
```

the results are

```text
S1 maximum normalized box residual       1.418088512811
S1 maximum held-out box residual          1.628014211258
SH maximum normalized box residual       1.820916077360
SH maximum held-out box residual          1.820916077360
```

Neither S1 nor SH is completely box-feasible. Hansen's coefficient pair remains inside the S1 nonprobabilistic linearized sensitivity envelope:

```text
b0 in [ 3.91485115e-4,  8.16260353e-4] eV/K
b1 in [-1.809474839e-3, -6.61098865e-4] eV/K per unit x.
```

## Controlling decision

```text
non_identifiable_at_figure_precision
```

The result is not `Hansen-compatible` because the Hansen-fixed model fails the controlling in-sample and leave-one-specimen-out box gates.

The result is not `observable-specific correction required` because the free linear slope model also fails those gates and the Hansen coefficients remain inside its linearized sensitivity envelope.

## Authorization state

```text
Scott source metrology and specimen registry          validated
Scott Figure 2 fixed-alpha marker ledger              validated
Scott specimen-centered central slopes                validated
Scott deterministic box qualification                 validated
Scott leave-one-specimen-out prediction               validated
Hansen temperature-coefficient compatibility          unresolved
fixed-alpha observation-specific correction           unresolved
absolute Hansen polynomial validation                 not authorized
new universal HgCdTe equation                         not authorized
manuscript or production-equation claim               not authorized
```

## Roadmap consequence

The Scott public-source path is closed at current figure precision. Do not reopen it by:

- sampling Equation (3) or Figure 5 curves;
- substituting fit-required compositions;
- adding nonlinear temperature terms to manufacture compatibility;
- treating extraction bounds as pointwise covariance;
- pooling Scott with incompatible measurement classes.

Reopening requires a materially higher-resolution or source-native numerical record with adequate uncertainty semantics. No author or institutional correspondence is permitted.
