# R06 Phase 1C uniform optical-generation gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06

## Decision

Proceed with a prescribed, spatially uniform, state-independent mobile-pair generation source as the next deterministic architecture gate.

Use equal electron-hole generation with no direct trap or Poisson source. Retain the reversible trap kinetics and all previously accepted charge conventions.

## Accepted equations

For net electron capture `A`, net hole capture `B`, and generation `G`, use

```text
R_n = div(j_n) - A + G
R_p = div(j_p) + B - G
R_f = A - B.
```

The generation terms cancel from the local charge balance. The analytical Jacobian is unchanged because `G` is prescribed and state independent.

## Executable evidence

The focused local optical harness reports 10 passed tests. The complete deterministic local harness reports 33 passed tests.

Verified locally:

- invalid generation rates are rejected;
- exact dark residual reduction;
- exact dark Jacobian reduction;
- electron and hole generation signs;
- local generation-source cancellation;
- an exact uniform illuminated generation-recombination balance;
- zero-iteration termination for the exact illuminated state;
- analytical Jacobian agreement with centered finite differences;
- independently closed global electron, hole, trap, and total-current balances;
- converged contact-extracted photogeneration with spatially constant total current.

GitHub Actions remains authoritative for the committed branch head.

## Rejected alternatives

1. **Direct Poisson generation source** — rejected because a generated electron-hole pair has zero net charge.
2. **Direct trap-generation source** — rejected because occupancy changes only through the four declared capture/emission channels.
3. **State-dependent absorption without derivatives** — rejected because it would invalidate the accepted Jacobian.
4. **Immediate optical gain or responsivity claims** — rejected because the source has no photon-energy, absorption, or calibration model.
5. **Immediate stochastic photon or generation-recombination noise** — rejected until the deterministic illuminated operating point and linearized conservation structure are validated.

## Authorization after this gate

If current-head CI passes, authorize a reduction-error study comparing the full steady trap elimination with a constant-coefficient mass-action source over a declared dimensionless state domain.

Do not yet authorize:

- material-specific absorption coefficients;
- spectral or temperature-dependent optical generation;
- photon shot noise;
- stochastic trap sources;
- terminal PSD calculations;
- predictive responsivity, gain, NEP, or detectivity claims.
