# R06 stochastic transport and noise literature audit

**Program:** stochastic transport and finite-size noise  
**Controlling issue:** #339

## Purpose

This directory records source-level evidence for the deterministic equations, stochastic covariance, HgCdTe material relations, contact models, limiting cases, numerical methods, and novelty boundary of R06.

A citation is not accepted merely because its title or abstract appears relevant. Important equations and claims must be checked against the source itself and recorded with enough location information to be independently verified.

## Required search domains

The Phase 1 audit must cover at least:

1. HgCdTe generation-recombination noise;
2. HgCdTe photoconductor transport and gain;
3. HgCdTe surface and contact recombination;
4. stochastic drift-diffusion and semiconductor Langevin theory;
5. impedance-field, Green-function, and transfer-function noise methods;
6. finite-size generation-recombination noise;
7. space-charge fluctuation and dielectric-relaxation theory;
8. contact injection, extraction, and recombination noise;
9. fluctuation-dissipation relations in semiconductor devices;
10. numerical discretization of stochastic drift-diffusion-Poisson systems;
11. modal, non-normal, and distributed-relaxation interpretations of device noise.

Searches must include terminology outside the infrared-detector literature. Equivalent theory may be indexed under semiconductor device noise, diffusion noise, impedance-field methods, reaction-diffusion fluctuations, stochastic transport, or nonequilibrium thermodynamics.

## Source priority

Preferred order:

1. original peer-reviewed derivation;
2. authoritative review or monograph;
3. official technical report or dissertation containing a complete derivation;
4. later paper that reproduces and checks the result;
5. secondary summary used only for orientation.

For HgCdTe material relations, record whether the source reports direct measurements, fitted empirical relations, compiled values, or model inference.

## Verification requirements

For every important source, record:

- full title;
- authors;
- year;
- journal, book, report, or thesis;
- DOI or stable report identifier;
- exact page, equation, figure, table, or section used;
- physical model and geometry;
- carrier statistics;
- recombination mechanism;
- electrostatic approximation;
- contact and terminal boundary conditions;
- stochastic primitive processes;
- PSD convention;
- main assumptions;
- limitations;
- direct relevance to R06;
- claim status: verified, partially verified, inaccessible, contradicted, or superseded.

Do not infer an equation from a paper that only cites another source. Trace the equation to the earliest accessible authoritative derivation where practical.

## Novelty audit

The novelty search must specifically test whether prior work already combines:

- self-consistent drift-diffusion-Poisson electrostatics;
- finite contact recombination or injection;
- frequency-domain Langevin transport;
- an externally conserved terminal-current observable;
- HgCdTe material physics;
- finite-device generation-recombination noise prediction.

Novelty must be evaluated by physics and observable, not by exact material composition, geometry, numerical package, or parameter values.

The provisional differentiating statement is:

> Existing HgCdTe GR-noise treatments often use quasi-neutral or spatially uniform carrier fluctuations, whereas R06 seeks to resolve coupled charge, electric-field, diffusion, recombination, and contact modes and identify the dimensionless boundaries where the lumped terminal-noise approximation fails.

This is a hypothesis to test, not an accepted claim.

## Evidence classes

Use the following labels:

- `source-established`: explicitly derived or measured in the cited source;
- `project-derivation`: derived within R06 from stated assumptions;
- `model-conditioned`: follows only for the selected closure or boundary model;
- `sensitivity-case`: exploratory parameter choice;
- `synthetic-validation`: numerical recovery using generated data;
- `material-validation`: comparison with independent HgCdTe measurements;
- `unresolved`: evidence is incomplete or conflicting.

## Files

- `literature_matrix.csv` — one row per source/model combination;
- later claim-level notes should use stable filenames keyed by first author and year;
- inaccessible sources must remain listed with status `inaccessible`; they must not be cited as verified evidence.

## Phase 1 completion rule

The literature gate is not complete until the matrix supports decisions on:

1. deterministic state equations;
2. contact and terminal boundary conditions;
3. primitive stochastic processes and covariance;
4. equilibrium fluctuation-dissipation test;
5. HgCdTe parameter ranges and uncertainty classes;
6. prior-art boundary;
7. whether Phase 2 should proceed, be narrowed, or terminate.