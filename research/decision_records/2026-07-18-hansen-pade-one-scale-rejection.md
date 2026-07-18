# Hansen–Padé one-scale crossover decision

**Date:** 2026-07-18  
**Status:** one-parameter candidate rejected; two-parameter zero-anchored form advanced

## Candidate

The tested equation was

```text
Eg(x,T) = -0.302 + 1.93x - 0.81x^2 + 0.832x^3
          + 5.35e-4 (1-2x) T^3/(T^2 + tau^2)
```

with energy in eV and temperature in kelvin.

The thermal term is exactly zero at `T=0`, has zero initial slope, scales as `T^3` at low temperature, and recovers Hansen's linear coefficient at high temperature. Only the crossover `tau` is fitted.

## Validation design

The 34 Seiler Figure 7 markers were grouped by specimen. Each leave-one-specimen-out fold trained on two specimens and evaluated the third with one profiled additive energy offset. This is a thermal-shape transfer test.

The strict absolute test trained `tau` only on specimens 1 and 2, then predicted specimen 3 without an offset. Specimen 3 has independently reported composition `x=0.259 +/- 0.0015`.

## Evidence

```text
workflow run: 29652063833
artifact:     8431754615
digest:       sha256:d5f3812f7f3f10d662ad888f4f5b43ba49c7db1e9025d5b0ff970ec3e468d8ca
validated head: c85d22332dc2c8b655c61b4198ac2fff16a4b0b4
```

## Held-out thermal shape

```text
Hansen linear RMSE          = 1.82388 meV
published Seiler RMSE       = 1.06113 meV
trained Seiler RMSE         = 0.78622 meV
fixed-slope Padé RMSE       = 1.34320 meV
free-slope Padé diagnostic  = 0.81258 meV
```

The fixed-slope Padé improves on Hansen by `26.35%`, but remains approximately `70.8%` above the trained two-parameter Seiler family. It therefore fails the declared near-Seiler transfer gate.

The crossover itself is stable:

```text
fold tau = 20.1009, 17.7916, 17.8647 K
max/min = 1.1298
```

## Independent-composition absolute test

For sample 3 at nominal `x=0.259`:

```text
Hansen RMSE          = 1.84640 meV
published Seiler     = 1.40383 meV
fixed-slope Padé     = 0.93673 meV
```

The Padé candidate beats both established equations on this specimen. Across the reported composition interval, its RMSE ranges from `0.8642` to `2.9733 meV`, showing that composition uncertainty remains a controlling error source.

## Why the candidate is rejected

Four of five promotion gates pass. The failure is not instability or absolute prediction; it is insufficient transferred curvature when the high-temperature coefficient is fixed at Hansen's `0.535 meV/K`.

The diagnostic fit that frees the coefficient gives:

```text
fold alpha = 0.58648, 0.59827, 0.59460 meV/K
max/min = 1.0201
fold tau = 22.8959, 17.5726, 14.6591 K
max/min = 1.5619
pooled RMSE = 0.81258 meV
```

This is only `3.35%` above the trained Seiler RMSE, while retaining exact zero-temperature anchoring and one fewer nonlinear degree of freedom than the `A,B` Seiler parameterization.

## Decision

Reject the fixed-Hansen-slope one-parameter equation as the production candidate.

Advance the two-parameter zero-anchored form:

```text
Eg(x,T) = Eg0_Hansen(x)
          + alpha (1-2x) T^3/(T^2 + tau^2)
```

The next benchmark must:

1. fit global `alpha` and `tau` only inside each training fold;
2. test specimen-level thermal-shape transfer;
3. perform absolute prediction on independently composed samples;
4. compare coefficient stability with Seiler `A,B` stability;
5. include composition-uncertainty propagation;
6. search prior art before any novelty language.

## Claim boundary

The free-slope result is a diagnostic, not yet a promoted equation. Only three temperature-series specimens are available, and the shape test profiles specimen offsets. A fitted `alpha` and `tau` remain effective coefficients rather than identified microscopic quantities.
