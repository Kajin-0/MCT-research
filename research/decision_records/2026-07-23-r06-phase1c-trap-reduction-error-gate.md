# R06 Phase 1C constant-kappa trap-reduction error gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06

## Decision

Retain the constant-coefficient mass-action source as a controlled local reduction of the reversible trap model. Quantify its validity using the exact state dependence of the eliminated coefficient rather than treating the approximation as globally exact.

## Error definition

For

```text
U_exact = kappa_eff(N,P) [N P - K_eq]
```

and

```text
U_reduced = kappa_0 [N P - K_eq],
```

use

```text
epsilon_rel = abs(kappa_0/kappa_eff - 1).
```

Away from detailed balance this equals the relative pair-rate error. At detailed balance it remains the continuous limiting diagnostic while both rates vanish.

## Exact boundary

For the symmetric logarithmic domain

```text
N/N0, P/P0 in [exp(-r), exp(+r)],
```

the denominator extrema occur at the equal-sign corners. The largest admissible radius for a requested tolerance is therefore available analytically, without a numerical optimizer or state sweep.

## Declared ensemble result

A four-scenario dimensionless rate ensemble is committed as a machine-readable configuration. It samples balanced, electron-fast, hole-fast, and shifted-equilibrium architectures.

For a 10% relative pair-rate tolerance, the conservative result is

```text
r = 0.1823215567939546

0.8333333333333334 <= N/N0 <= 1.2

0.8333333333333334 <= P/P0 <= 1.2.
```

The balanced scenario controls this finite ensemble.

## Executable evidence

The focused local reduction harness reports 11 passed tests. The complete local deterministic harness reports 44 passed tests.

Verified locally:

- reference coefficient construction;
- exact shared mass-action numerator;
- equality between pair-rate and coefficient-ratio relative errors;
- analytical corner-saturating radius;
- violation immediately outside the radius;
- dense-grid compliance inside the radius;
- monotonic radius growth with tolerance;
- cancellation of trap density from the relative domain;
- conservative finite-ensemble minimum;
- corner compliance for every declared scenario;
- explicit invalid-input rejection.

GitHub Actions remains authoritative for the committed branch head.

## Scientific boundary

The finite uncertainty ensemble is synthetic and dimensionless. It is a structural robustness test, not an empirical distribution of HgCdTe defects. The result must not be described as a material-valid density, bias, temperature, or composition range.

## Authorization after this gate

If current-head CI passes, the deterministic architecture has a concrete reduction-error boundary suitable for the Phase 1 decision package.

The next work should return to unresolved material provenance:

- source-exact Kane/nonparabolic statistics;
- low-temperature mobility;
- static permittivity;
- defensible contact ranges;
- material-grounded uncertainty scenarios.

Do not yet authorize stochastic PSD implementation or predictive detector claims.
