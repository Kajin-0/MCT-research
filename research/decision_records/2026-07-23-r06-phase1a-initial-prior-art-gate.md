# R06 Phase 1A initial prior-art gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Decision:** continue Phase 1A with narrowed scope; production simulation remains unauthorized

## Evidence reviewed

The initial audit identified prior work that already covers:

- finite-size GR noise with drift, diffusion, Poisson correlation, and displacement current;
- finite-length current and voltage spectra with coupled carriers and traps;
- bipolar population-source Langevin methods and boundary-condition sensitivity;
- impedance-field or Green-function terminal-noise transfer;
- finite contact recombination velocity;
- HgCdTe blocking-contact modification of GR noise and responsivity;
- HgCdTe deep-trap effects on free and bound carrier noise;
- practical two-dimensional planar-contact limitations of one-dimensional effective contact models.

The detailed source record is in:

- `literature/stochastic_transport_noise/prior_art_phase1a.md`;
- `literature/stochastic_transport_noise/literature_matrix.csv`.

## Decision

The original broad differentiating statement is too broad and is rejected.

R06 must not claim originality for finite size, Poisson coupling, diffusion, trap dynamics, finite contact velocity, or frequency-domain terminal noise individually or in ordinary combinations.

The remaining candidate contribution is the verified intersection of:

1. bipolar HgCdTe transport;
2. explicit stochastic trap kinetics;
3. thermodynamically consistent finite-contact exchange;
4. optical generation;
5. a conserved terminal observable including the external circuit;
6. dimensionless error bounds for lumped GR interpretations.

This remains a hypothesis to audit, not a novelty claim.

## Authorization

Authorized:

- full-text comparison of the highest-overlap papers;
- stochastic covariance and contact detailed-balance derivation;
- dimensionless reduction;
- analytical benchmark design;
- numerical acceptance-test specification.

Not authorized:

- production deterministic or stochastic sweeps;
- manuscript drafting;
- novelty claims;
- empirical fitting;
- three-dimensional simulation.

## Stop rule

Reframe R06 as a benchmark and synthesis project, merge it into established theory, or terminate it if the complete literature audit shows that the remaining intersection and proposed outputs are already established or cannot be made falsifiable with public HgCdTe parameters.
