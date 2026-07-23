# R06 Phase 1C authorization

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Decision:** authorize the remaining Phase 1 material/statistics and deterministic-architecture work; production simulation remains gated

## Context

The broad theory novelty hypothesis and the stochastic-contact novelty hypothesis have both been rejected based on verified prior art. The program remains viable as a controlled reduction and error-bound study.

The interface literature now establishes:

- activated forward/reverse contact exchange;
- forward-minus-reverse mean flux and forward-plus-reverse covariance;
- nonlinear and linear fluctuation relations;
- dynamic interface-state sources and cross covariance;
- thermionic-emission contact noise coupled to drift-diffusion-Poisson transport;
- equilibrium Nyquist recovery with the required transfer cross terms.

## Authorized Phase 1C scope

1. HgCdTe band, statistics, and electrostatic parameter audit.
2. Carrier degeneracy and generalized Einstein analysis.
3. Mobility, trap, absorption, and interface parameter uncertainty ranges.
4. Deterministic boundary hierarchy and external-circuit specification.
5. Conservative one-dimensional finite-volume solver architecture.
6. Independent verification method selection.
7. Phase 2 executable test plan and repository layout.
8. Final Phase 1 proceed, reframe, or terminate gate.

## Explicit exclusions

- broad HgCdTe parameter sweeps;
- stochastic production solver implementation;
- predictive detector-noise claims;
- manuscript drafting;
- novelty claims based on contact fluctuations, dynamic traps, or finite-size spectra;
- arbitrary fitted source terms;
- three-dimensional simulation.

## Required decision metrics

The statistics closure must report the maximum relative error in:

- carrier density;
- carrier compressibility;
- generalized Einstein factor;
- Debye length;
- steady terminal current;
- differential conductance.

The parameter audit must distinguish established public relations, uncertain literature parameters, and exploratory controls.

The solver architecture must support exact discrete carrier conservation, flux-consistent contact boundaries, continuation in bias and illumination, and independent analytical or numerical verification.

## Phase 2 gate condition

Phase 2 may begin only after a decision record confirms:

1. a defensible carrier-statistics closure;
2. source-controlled parameter ranges;
3. a complete deterministic boundary model;
4. a conservative discretization;
5. executable analytical-limit tests;
6. acceptable numerical dependency and reproducibility plans;
7. at least one plausible uncertainty-robust reduction question.

## Stop rule

Terminate the paper objective or reframe as a benchmark package if the remaining parameter uncertainty prevents a stable regime boundary or if all proposed reductions are accurate throughout the physically plausible HgCdTe domain.