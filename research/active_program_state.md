# Current research program state

**Last updated:** 2026-07-18  
**Current PR:** #114

This file is the current controlling state after PRs #99-#113. The older `research/active_progress.md` contains useful history but its authorization section is stale.

## Established

- Static finite-k extraction now uses the isospectral selected-band polar Hamiltonian.
- The complete linear and quadratic zincblende spaces are established and prior-art bounded.
- The finite-temperature matrix, polar-vertex, backend, and supercell-reconstruction oracles are implemented and tested.
- The present CdTe response setup is not authorized for production finite-temperature calculations.

## HgCdTe gap model

The constrained thermal candidate

`Eg(x,T) = Eg_Hansen(x,0) + alpha (1-2x) T^3/(T^2 + tau^2)`

uses `alpha = 5.918273117836612e-4 eV/K` and `tau = 18.059294367159467 K`.

It is a provisional model within the Seiler specimen regime, not a new functional family or a production equation.

## Evidence boundary

- Static corrections fitted to one historical source do not transfer to independently composed specimens from another source.
- Existing metadata do not identify a universal measurement correction.
- No new static polynomial or production observation correction is authorized.
- The audit-grade experimental target is eight paired specimens with independent composition, carrier-state, and defect-state evidence.

## Teppe primary benchmark

PR #114 admits five exact primary magneto-optical gap points from DOI `10.1038/ncomms12576`.

Sample A is reported as `x=0.175` in figures/text and `x=0.170` in Methods. This difference reverses the model ranking:

- at `x=0.175`, Laurenti gives `4.2005 meV` combined RMSE;
- at `x=0.170`, provisional Hansen-Pade gives `5.0665 meV` combined RMSE.

Therefore the provisional model is no longer described as globally leading. It remains the leading constrained model only in its Seiler validation regime. Laurenti is not promoted from the unresolved comparison.

## Authorized next work

1. Merge PR #114 after final tests pass.
2. Resolve the Teppe Sample A composition from primary records or independent metrology.
3. Recover additional primary point-level datasets with explicit composition and measurement provenance.
4. Convert matrix covariance storage from redundant 128D coordinates to 64 independent Hermitian coordinates.

## Not authorized

- further empirical gap coefficients from the current mixed-source evidence;
- universal model ranking from the unresolved Teppe composition;
- additional production finite-temperature calculations from the failed CdTe response state;
- claims of a new universal HgCdTe bandgap equation.
