# Uniform optical pair generation in the reversible trap model

**Date:** 2026-07-23  
**Scope:** dimensionless steady one-dimensional verification model  
**Status:** Phase 1C numerical architecture only

## Generation convention

Let `G >= 0` denote a spatially uniform rate that creates one mobile electron and one mobile hole per event. Generation does not directly change trap occupancy and does not directly enter Poisson because the generated pair has zero net charge.

The accepted reversible trap rates remain

```text
A = C_n - E_n
B = C_p - E_p,
```

where `A` is net electron capture and `B` is net hole capture.

## Continuity residuals

With the established conventional-current signs,

```text
R_n = div(j_n) - A + G
R_p = div(j_p) + B - G
R_f = A - B.
```

The optical increments cancel locally:

```text
(+G) + (-G) + 0 = 0.
```

Consequently,

```text
R_n + R_p + R_f = div(j_n + j_p).
```

At a converged steady state, total conventional current remains spatially constant even though illumination changes the separate electron and hole currents.

## Integrated balances

Over uniform cells of width `h`,

```text
j_n,R - j_n,L = h sum(A) - h sum(G)

j_p,R - j_p,L = h sum(G) - h sum(B)

h sum(A - B) = 0
```

at steady state. These three balances are evaluated independently of residual assembly.

## Exact uniform illuminated state

For symmetric electron and hole trap kinetics, equal uniform carrier densities, and fixed trap occupancy, a uniform state is exact when

```text
A = B = G
```

and the fixed charge satisfies

```text
C = N + N_t f - P.
```

This benchmark isolates source signs from transport gradients.

## Jacobian

The present `G` is prescribed and state independent. Therefore it contributes no Jacobian entries:

```text
J_illuminated = J_trap.
```

A later absorption model depending on optical intensity, carrier state, temperature, or field would require additional derivatives and a separate gate.

## Claim boundary

This gate does not define optical absorption, photon energy, quantum efficiency, internal gain, responsivity, spectral cutoff, beam geometry, or radiative transfer. `G` is a dimensionless deterministic source used solely to verify generation-recombination balance.
