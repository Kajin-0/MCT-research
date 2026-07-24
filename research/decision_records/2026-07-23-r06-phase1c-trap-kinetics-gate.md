# R06 Phase 1C reversible trap-kinetics gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06

## Decision

Proceed with a single-level reversible deterministic trap-occupancy prototype under a strict architecture-only claim boundary.

Use an empty-neutral, occupied-negative trap convention. Represent occupancy by a logit variable. Derive electron and hole emission coefficients from a declared equilibrium state so both reversible channel pairs satisfy detailed balance independently.

## Accepted equations

The four channels are

```text
C_n = N_t c_n N (1-f)
E_n = N_t e_n f
C_p = N_t c_p P f
E_p = N_t e_p (1-f).
```

Define `A=C_n-E_n` and `B=C_p-E_p`. The accepted residuals are

```text
R_n = div(j_n) - A
R_p = div(j_p) + B
R_f = A - B.
```

Occupied traps enter Poisson through

```text
N + N_t f - P - C.
```

## Detailed-balance constraint

The emission coefficients are not independent fitting parameters in this gate:

```text
e_n = c_n N_eq (1-f_eq) / f_eq

e_p = c_p P_eq f_eq / (1-f_eq).
```

This guarantees exact equilibrium cancellation of each capture/emission pair.

## Reduction finding

Steady elimination of occupancy gives

```text
U_ss = kappa_eff(N,P) (N P - N_eq P_eq),
```

where

```text
kappa_eff(N,P)
  = N_t c_n c_p
    / (c_n N + e_p + e_n + c_p P).
```

The constant-coefficient mass-action source from PR #359 is therefore retained as a local reduced model. It is not promoted to an exact global representation of reversible trap kinetics.

This distinction creates a concrete reduction-error question: over what state domain can `kappa_eff(N,P)` be treated as constant within a declared tolerance?

## Executable evidence

The focused local harness reports 13 passed trap tests. The combined local harness, including the preceding pair-recombination tests, reports 23 passed tests.

Verified locally:

- bounded occupancy reconstruction;
- independent electron and hole detailed balance;
- exact charged equilibrium;
- exact zero-trap reduction of the mobile-carrier blocks;
- local source cancellation from the charge equation;
- analytical steady occupancy;
- exact state-dependent mass-action reduction;
- complete analytical Jacobian agreement with centered finite differences;
- independent global electron, hole, trap, and total-current balances;
- zero-iteration equilibrium termination;
- converged contact-supplied trap recombination with constant total current;
- explicit invalid-input rejection.

GitHub Actions remains authoritative for the committed branch head.

## Rejected alternatives

1. **Unconstrained occupancy unknown** — rejected because Newton steps can leave the physical interval.
2. **Independent emission-rate fitting** — rejected at this gate because it permits silent violation of detailed balance.
3. **Constant-coefficient mass action as exact trap elimination** — rejected because the exact eliminated coefficient depends on `N` and `P`.
4. **Immediate stochastic trap noise** — rejected until deterministic charge conservation and linearization are validated.
5. **Material-specific HgCdTe defect assignment** — rejected because no defect identity or capture-cross-section provenance has been established.

## Authorization after this gate

If current-head CI passes, authorize the next deterministic increment to add uniform optical pair generation and verify generation-recombination balance against the trap model.

Do not yet authorize:

- time-domain occupancy integration;
- stochastic Langevin sources;
- generation-recombination PSD;
- multiple or distributed trap levels;
- interface-specific traps;
- material-accurate HgCdTe trap parameters;
- predictive detector claims.
