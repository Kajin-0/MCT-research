# R06 Phase 1C constant-kappa reduction-error targets

**Status:** executable deterministic reduction gate  
**Scope:** steady elimination of one reversible trap level  
**Controlling issue:** #346

## K0 — reference coefficient

The frozen coefficient must be evaluated at a declared positive reference state. By default, use the scenario's declared equilibrium carrier densities.

## K1 — exact shared numerator

The exact and reduced rates must share

```text
N P - K_eq.
```

At detailed balance, both rates vanish exactly.

## K2 — relative error identity

Away from detailed balance,

```text
abs(U_reduced / U_exact - 1)
  = abs(kappa_0 / kappa_eff - 1).
```

The coefficient ratio remains the limiting diagnostic at detailed balance.

## K3 — exact symmetric log-domain radius

For

```text
N = N0 exp(xi_n)
P = P0 exp(xi_p)
|xi_n| <= r
|xi_p| <= r,
```

the returned radius must be the largest value satisfying the requested relative error everywhere in the rectangle.

## K4 — corner saturation

At the exact radius, at least one corner must attain the requested tolerance to numerical precision.

## K5 — exterior violation

A strictly larger radius must violate the tolerance at one or more corners.

## K6 — dense-grid verification

A dense interior grid must remain within tolerance at the analytical radius.

## K7 — monotonicity

The admissible radius must increase strictly with the requested tolerance over the tested range.

## K8 — trap-density cancellation

Changing `N_t` must rescale both exact and reduced rates but must not change the relative-error domain.

## K9 — finite uncertainty ensemble

For a declared finite set of rate scenarios, the conservative boundary must equal the minimum exact radius over the scenarios.

## K10 — scenario-wide verification

The conservative radius must satisfy the tolerance at every corner of every declared scenario.

## K11 — invalid-input rejection

Invalid tolerances, reference densities, radii, duplicate scenario names, and empty ensembles must be rejected explicitly.

## Reference structural result

For the declared four-scenario dimensionless ensemble and a 10% relative pair-rate tolerance,

```text
r_conservative = 0.1823215567939546

0.8333333333333334 <= N/N0 <= 1.2

0.8333333333333334 <= P/P0 <= 1.2.
```

The balanced scenario controls this particular ensemble.

## Acceptance boundary

Passing K0–K11 validates the reduction-error algebra, exact domain construction, and finite-ensemble conservatism only. It does not establish a physical HgCdTe validity range because the ensemble is not derived from measured defect-parameter distributions.
