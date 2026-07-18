# Two-parameter Hansen–Padé provisional model decision

**Date:** 2026-07-18  
**Status:** promoted to leading provisional analytical model; production use not authorized

## Equation

The selected thermal form is

```text
Eg(x,T) = -0.302 + 1.93x - 0.81x^2 + 0.832x^3
          + alpha (1-2x) T^3/(T^2 + tau^2)
```

with the all-specimen shape fit

```text
alpha = 5.918273117836612e-4 eV/K
tau   = 18.059294367159467 K
```

The equation is implemented as `provisional_hansen_pade_gap_ev` rather than replacing Hansen or Laurenti.

## Why this form was selected

The rejected one-parameter version fixed `alpha` at Hansen's `5.35e-4 eV/K`. It improved Hansen but did not transfer nearly as well as the trained Seiler rational family.

Freeing `alpha` produces stable leave-one-specimen-out coefficients:

```text
alpha = 0.58648, 0.59827, 0.59460 meV/K
alpha max/min = 1.0201

tau = 22.8959, 17.5726, 14.6591 K
tau max/min = 1.5619
```

The coefficient stability is substantially better than the strongly correlated `A,B` decomposition of the unconstrained Seiler family.

## Validation evidence

```text
workflow run: 29652606029
artifact:     8431908170
digest:       sha256:99dbf84f4f532f9e2fea5d7d4e19bc34a45e10e6be58f158213cfdfbc43eb82a
validated head: db68c689e4e0634e88e652f208a477978a31b03e
```

### Specimen-level held-out thermal shape

```text
Hansen linear RMSE          = 1.82388 meV
published Seiler RMSE       = 1.06113 meV
trained Seiler RMSE         = 0.78622 meV
provisional Hansen–Padé     = 0.81258 meV
```

The provisional form is only `3.35%` above the trained two-parameter Seiler fit and beats the published Seiler coefficients.

### Strict absolute temperature-series prediction

`alpha,tau` were trained only on specimens 1 and 2 and then used to predict independently composed specimen 3 without an energy offset:

```text
Hansen RMSE          = 1.84640 meV
published Seiler     = 1.40383 meV
provisional Padé     = 1.03976 meV
```

The reported sample-3 composition uncertainty remains important: the provisional RMSE spans approximately `0.83–3.13 meV` over `x=0.259+/-0.0015`.

### Independently composed 2–10 K samples 3–5

At the 6 K midpoint:

```text
Hansen RMSE          = 3.88667 meV
published Seiler     = 4.91429 meV
Laurenti             = 11.75031 meV
provisional Padé     = 4.17616 meV
```

The candidate remains within the declared `0.5 meV` margin of Hansen, but sample 4 retains a `6.70 meV` nominal residual. This is not a thermal-kernel failure; at 2–10 K the candidate thermal correction is small. It exposes the inherited Hansen zero-temperature composition polynomial.

### Broader historical Table 2 screen

Across all 18 low-temperature points:

```text
Hansen:              RMSE 6.50175 meV, MAE 4.72326 meV
published Seiler:    RMSE 7.43996 meV, MAE 5.11154 meV
Laurenti:            RMSE 6.98184 meV, MAE 5.33006 meV
provisional Padé:    RMSE 6.59969 meV, MAE 4.41161 meV
```

The provisional form improves MAE and remains within `1.51%` of Hansen's RMSE. Most legacy compositions are not audited, so this is a catastrophic-extrapolation screen rather than a high-confidence fit target.

## Prior-art boundary

This is not a new functional family.

Seiler et al. introduced a rational temperature law proportional to

```text
(A + T^3)/(B + T^2).
```

The provisional equation is its constrained zero-anchored special case with `A=0`, `B=tau^2`, and a fitted prefactor `alpha`. The primary Seiler paper is DOI `10.1116/1.576952`.

Varshni and Pässler provide broader prior art for low-temperature-suppressed, high-temperature-linear semiconductor gap laws. Relevant DOIs are `10.1016/0031-8914(67)90062-6` and `10.1002/pssb.200301752`.

The defensible contribution is therefore not invention of a new analytical family. It is:

- a physically cleaner zero-temperature anchor;
- a stable two-coefficient reparameterization;
- specimen-level transfer testing;
- an independent-composition absolute test;
- explicit propagation of composition uncertainty;
- identification of the static composition law as the remaining bottleneck.

## Decision

- Retain the equation as the leading **provisional** temperature model.
- Do not call it novel or production-ready.
- Do not add another thermal coefficient.
- Move the main analytical effort to `Eg(x,0)` using independently composed low-temperature data and leakage-safe composition holdouts.
- Preserve Hansen and Laurenti as comparison baselines.

## Next static-law requirements

The next candidate must:

1. use the provisional thermal kernel without refitting it;
2. fit only a minimal correction to the Hansen zero-temperature composition polynomial;
3. prioritize independently composed samples;
4. propagate `x` uncertainty explicitly;
5. use composition holdouts rather than pointwise random splits;
6. reject corrections that improve sample 4 only by degrading the broader historical table;
7. retain endpoint or critical-composition constraints only when supported by independent data.

## Claim boundary

Only three Figure 7 temperature-series specimens are available, and the shape analysis profiles specimen offsets. Only one series has an independently reported composition. Most historical low-temperature compositions are not audited. The provisional coefficients are empirical effective parameters, not identified electron-phonon constants.
