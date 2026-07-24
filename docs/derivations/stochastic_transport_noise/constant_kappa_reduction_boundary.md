# Exact constant-kappa reduction boundary for one reversible trap level

**Date:** 2026-07-23  
**Scope:** dimensionless steady trap elimination  
**Status:** Phase 1C reduction-error architecture

## Exact eliminated rate

Steady elimination of trap occupancy gives

```text
U_exact = kappa_eff(N,P) [N P - K_eq],
```

with

```text
kappa_eff(N,P)
  = N_t c_n c_p
    / [c_n N + c_p P + e_n + e_p].
```

Freeze the coefficient at a declared reference state `(N0,P0)`:

```text
kappa_0 = kappa_eff(N0,P0).
```

The reduced rate is

```text
U_reduced = kappa_0 [N P - K_eq].
```

Away from detailed balance, the relative pair-rate error is

```text
abs(U_reduced/U_exact - 1)
  = abs(kappa_0/kappa_eff - 1).
```

At `N P = K_eq`, both rates vanish and the coefficient ratio gives the continuous limiting diagnostic.

## Symmetric logarithmic state domain

Define

```text
N = N0 exp(xi_n)
P = P0 exp(xi_p)
|xi_n| <= r
|xi_p| <= r.
```

Let

```text
S = c_n N0 + c_p P0
E = e_n + e_p
D0 = S + E.
```

Since the denominator is affine and increasing in both carrier densities,

```text
D_min(r) = E + S exp(-r)
D_max(r) = E + S exp(+r).
```

The relative error is

```text
abs(D/D0 - 1).
```

For a requested tolerance `0 < epsilon < 1`, require

```text
D0(1-epsilon) <= D <= D0(1+epsilon).
```

The two exact radius limits are

```text
r_high = log([D0(1+epsilon)-E]/S)

r_low  = -log([D0(1-epsilon)-E]/S),
```

where the lower constraint is inactive if its logarithm argument is non-positive. The exact admissible radius is

```text
r = min(r_high, r_low).
```

No spatial sweep or optimizer is required.

## Finite uncertainty ensemble

For a declared finite set of trap-rate scenarios, compute the exact radius separately for each scenario and retain

```text
r_conservative = min_s r_s.
```

This is an exact worst case over the declared scenarios. It is not a continuous uncertainty proof outside that finite set.

## Structural observations

`N_t` cancels from the relative error because it multiplies both `kappa_eff` and `kappa_0`. It changes the pair-rate magnitude but not the constant-coefficient validity domain.

The boundary depends on the relative weighting of carrier-dependent capture and state-independent emission terms. Strong emission weighting generally enlarges the carrier-density domain over which a frozen coefficient remains accurate.

## Claim boundary

The present uncertainty ensemble is synthetic and dimensionless. A material-valid HgCdTe boundary requires source-audited capture coefficients, defect densities, equilibrium occupancies, correlations, and temperature/composition dependence.
