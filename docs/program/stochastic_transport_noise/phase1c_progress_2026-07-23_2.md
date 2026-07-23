# R06 Phase 1C deterministic-kernel progress — 2026-07-23

## Completed

- implemented a dimensionless steady unipolar Poisson-continuity prototype;
- used logarithmic density unknowns to preserve positivity;
- implemented stable Bernoulli functions and derivatives;
- implemented Scharfetter-Gummel fitted electron face current;
- assembled a dense analytical residual Jacobian;
- added residual-independent current-conservation metrics;
- specified D0-D10 deterministic-kernel benchmarks;
- recorded the deterministic-kernel decision gate;
- updated the authoritative R06 program state.

## Validation

Combined local validation of the statistics and deterministic prototypes reports 46 passed tests.

The new deterministic tests verify:

- Bernoulli symmetry and derivatives;
- positive density reconstruction;
- exact uniform equilibrium;
- exact biased uniform-resistor current;
- zero-field diffusion;
- telescoping continuity balance;
- analytical Jacobian agreement with finite differences;
- configuration validation.

## Remaining

1. damped Newton solver for exact and manufactured benchmarks;
2. mesh-refinement and continuation tests;
3. sparse Jacobian representation;
4. bipolar deterministic block specification;
5. connection to the selected equilibrium statistics closure;
6. low-temperature mobility and static-permittivity audits;
7. material-uncertainty stability test;
8. final Phase 1 decision.

No production HgCdTe simulation or stochastic implementation is authorized.