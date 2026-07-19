# Chu 1994 Kane-region absorption candidate

**Date:** 2026-07-19  
**Primary model source:** Chu, Li, Liu, and Tang, *Journal of Applied Physics* **75**, 1234-1235 (1994), DOI `10.1063/1.356464`  
**Status:** prior-art observation-model candidate; not material-gap fit authority

## Source law

The prior-art intrinsic absorption law above the HgCdTe gap is

```text
alpha(E) = alpha_g * exp(sqrt(beta(x,T) * (E - Eg)))
```

with the composition- and temperature-dependent curvature

```text
beta(x,T) = -1 + 0.083*T + (21 - 0.13*T)*x.
```

At the two commonly quoted temperatures this reduces to approximately

```text
beta(x,300 K) = 24 - 18x
beta(x,77 K)  = 5.4 + 11x.
```

`beta` has inverse-energy units under the declared expression. `alpha_g` is the fitted absorption scale at the extrapolated edge.

The source family covers approximately

```text
0.170 <= x <= 0.443
77 K <= T <= 300 K.
```

The repository does not use this law outside that range.

## Why this belongs in the observation contract

The existing absorption uncertainty contract evaluates:

1. fractional-power candidates `alpha=A*(E-Eg)^p/E`;
2. fixed absorption thresholds.

The Chu 1994 law is structurally different. It encodes a Kane-region square-root exponential and fixes its curvature from declared specimen composition and temperature. Omitting it would leave an established HgCdTe-specific observation model outside the candidate ensemble.

This model does not replace Hansen, Laurenti, Seiler, or the provisional Hansen-Pade material-gap law. It maps a measured absorption spectrum to an inferred edge parameter.

## Fit architecture

For declared `x` and `T`, calculate fixed

```text
beta = beta(x,T).
```

For each candidate edge `Eg` in the declared search grid,

```text
ln(alpha_i) = ln(alpha_g) + sqrt(beta * (E_i - Eg)).
```

The optimal `ln(alpha_g)` at that edge is the mean residual offset:

```text
ln(alpha_g) = mean_i[ln(alpha_i) - sqrt(beta * (E_i - Eg))].
```

The selected candidate minimizes mean squared residual in `ln(alpha)`. The result reports:

- fitted `Eg`;
- fitted `alpha_g`;
- fixed `beta(x,T)`;
- log-space mean-square residual;
- source DOI and exact model expressions;
- source validity range.

The grid and fit window remain explicit contract assumptions.

## Fail-closed gates

The candidate is opt-in through

```text
include_chu_1994_kane_region: true
```

and is rejected when:

- composition is absent;
- `x < 0.170` or `x > 0.443`;
- `T < 77 K` or `T > 300 K`;
- the calculated `beta` is nonpositive;
- the declared edge grid intersects the fitted energy range;
- fewer than the contract minimum spectral points survive the absorption window.

Existing contracts that omit the flag retain their previous candidate ensemble and behavior.

## Synthetic validation

A spectrum generated from

```text
x       = 0.21
T       = 80 K
Eg      = 0.100 eV
alpha_g = 700 cm^-1
beta    = 7.866 eV^-1
```

is recovered within the deterministic edge-grid resolution:

```text
|Eg_fit - Eg_true| <= 2e-5 eV
relative alpha_g error <= 2e-4
log-space MSE < 1e-10.
```

The endpoint reductions of `beta(x,T)` are also tested, together with domain rejection at `T=40 K` and `x=0.60`.

## Contract behavior

When enabled, the model adds one candidate:

```text
candidate_id = chu_1994_kane_region
```

It contributes to the model-family and combined sensitivity envelopes. It is never selected as a recommended or corrected gap, and the contract continues to report the full ensemble.

## Decision

- add the prior-art model as an optional candidate: **yes**;
- preserve the source-supported domain: **yes**;
- infer missing composition or temperature: **no**;
- extrapolate `beta(x,T)` outside the source range: **no**;
- select the Chu candidate as a production edge: **no**;
- treat fitted `Eg` as an independently validated material gap: **no**;
- use the candidate to quantify observation-model sensitivity: **yes**.

## Files

- `src/mct_research/absorption_edge_uncertainty.py`
- `src/mct_research/__init__.py`
- `data/templates/absorption_edge_uncertainty_input.schema.json`
- `tests/test_absorption_edge_uncertainty_contract.py`

## Claim boundary

This implementation reproduces an established observation law and adds it to a sensitivity ensemble. It does not recover the primary point-level gap table, validate the source composition metrology, introduce a new absorption law, or authorize a universal HgCdTe band-gap equation.
