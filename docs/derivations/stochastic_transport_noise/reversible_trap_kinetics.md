# Reversible single-level trap kinetics for the R06 deterministic gate

**Date:** 2026-07-23  
**Scope:** dimensionless steady one-dimensional verification model  
**Status:** Phase 1C numerical architecture only

## Charge convention

A trap is neutral when empty and carries one electron-like negative charge when occupied. Let

- `N_t` be the normalized trap density;
- `f` be the occupied fraction, with `0 < f < 1`;
- `N_t f` be the trapped-electron density.

The bipolar Poisson charge term becomes

```text
N + N_t f - P - C.
```

This is the same sign as the free-electron contribution because an occupied trap carries electron-like charge.

The numerical unknown is the logit

```text
z = log(f / (1 - f)),
```

so reconstruction through the logistic map preserves the occupancy bounds.

## Four reversible channels

The volumetric channel rates are

```text
C_n = N_t c_n N (1 - f)    electron capture
E_n = N_t e_n f            electron emission
C_p = N_t c_p P f          hole capture
E_p = N_t e_p (1 - f)      hole emission
```

Define

```text
A = C_n - E_n
B = C_p - E_p.
```

Positive `A` removes free electrons and fills traps. Positive `B` removes free holes and empties traps.

## Detailed balance

A declared equilibrium state `(N_eq, P_eq, f_eq)` fixes the emission coefficients:

```text
e_n = c_n N_eq (1 - f_eq) / f_eq

e_p = c_p P_eq f_eq / (1 - f_eq).
```

Therefore

```text
C_n = E_n
C_p = E_p
```

at the declared equilibrium state. The two reversible channel pairs satisfy detailed balance independently.

## Residual signs

Using the accepted conventional-current signs, the steady residuals are

```text
R_n = div(j_n) - A
R_p = div(j_p) + B
R_f = A - B.
```

The source terms cancel locally:

```text
(-A) + (+B) + (A - B) = 0.
```

Hence

```text
R_n + R_p + R_f = div(j_n + j_p).
```

At a converged steady state, the total conventional current is spatially constant. Separate carrier-current changes are balanced by trap charging and discharging.

## Steady occupancy elimination

Setting `R_f = 0` gives

```text
f_ss = (c_n N + e_p) / (c_n N + e_p + e_n + c_p P).
```

The common steady pair rate is

```text
U_ss = A = B
     = N_t (c_n c_p N P - e_n e_p)
       / (c_n N + e_p + e_n + c_p P).
```

Detailed balance implies

```text
e_n e_p = c_n c_p N_eq P_eq.
```

Therefore

```text
U_ss = kappa_eff(N, P) (N P - K_eq),

K_eq = N_eq P_eq,

kappa_eff(N, P)
  = N_t c_n c_p
    / (c_n N + e_p + e_n + c_p P).
```

The mass-action numerator is exact, but the coefficient is state dependent. The constant-coefficient pair source merged in PR #359 is consequently a local reduction of this four-channel model, not a globally exact elimination.

## Jacobian contributions

With `df/dz = f(1-f)`, the local derivatives are

```text
dA/d(log N) = N_t c_n N (1 - f)

dA/dz = -N_t (c_n N + e_n) f(1-f)

dB/d(log P) = N_t c_p P f

dB/dz = N_t (c_p P + e_p) f(1-f).
```

These enter the electron, hole, trap, and Poisson rows with the residual signs above.

## Claim boundary

This gate does not identify a physical HgCdTe defect or infer a lifetime. It does not add time integration, stochastic occupancy fluctuations, generation-recombination PSD, optical generation, interface traps, multiple trap levels, or material-specific capture cross sections.
