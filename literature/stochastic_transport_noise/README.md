# R06 stochastic transport and noise literature audit

**Program:** stochastic transport and finite-size noise  
**Current controlling issue:** #341  
**Foundational setup issue:** #339

## Purpose

This directory records source-level evidence for the deterministic equations, stochastic covariance, HgCdTe material relations, contact models, limiting cases, numerical methods, and novelty boundary of R06.

A citation is not accepted merely because its title or abstract appears relevant. Important equations and claims must be checked against the source itself and recorded with enough location information to be independently verified.

## Current audit status

The initial Phase 1A search has already falsified the broad claim that finite-size drift-diffusion-Poisson GR-noise theory is absent.

Verified or strongly supported prior work already covers:

- finite-size GR noise with diffusion, Poisson correlation, and terminal displacement current;
- finite-length current and voltage spectra with coupled carrier and trap dynamics;
- bipolar Langevin population sources and boundary-condition effects;
- impedance-field and Green-function terminal transfer;
- finite contact recombination velocity;
- HgCdTe blocking-contact modification of GR noise and responsivity;
- HgCdTe deep-trap contributions;
- two-dimensional limitations of one-dimensional contact models.

The current narrowed question is documented in:

- `prior_art_phase1a.md`;
- `../../research/decision_records/2026-07-23-r06-phase1a-initial-prior-art-gate.md`.

No novelty claim is authorized.

## Required search domains

The Phase 1 audit must cover at least:

1. HgCdTe generation-recombination noise;
2. HgCdTe photoconductor transport and gain;
3. HgCdTe surface and contact recombination;
4. stochastic drift-diffusion and semiconductor Langevin theory;
5. impedance-field, Green-function, adjoint, and transfer-function noise methods;
6. finite-size generation-recombination noise;
7. space-charge fluctuation and dielectric-relaxation theory;
8. contact injection, extraction, and recombination noise;
9. fluctuation-dissipation relations in semiconductor devices;
10. numerical discretization of stochastic drift-diffusion-Poisson systems;
11. modal, non-normal, and distributed-relaxation interpretations of device noise;
12. practical geometry limits of one-dimensional HgCdTe contact models.

Searches must include terminology outside infrared-detector literature. Equivalent theory may be indexed under semiconductor device noise, diffusion noise, impedance-field methods, reaction-diffusion fluctuations, stochastic transport, or nonequilibrium thermodynamics.

## Source priority

Preferred order:

1. original peer-reviewed derivation;
2. authoritative review or monograph;
3. official technical report or dissertation containing a complete derivation;
4. author or institutional repository copy of the published paper;
5. later paper that reproduces and checks the result;
6. secondary summary used only for orientation.

For HgCdTe material relations, record whether the source reports direct measurements, fitted empirical relations, compiled values, or model inference.

## Verification statuses

Use one of the following explicit statuses or a more precise documented variant:

- `verified_full_text`: equations and relevant assumptions checked in the full source;
- `partially_verified_full_text`: full text accessible but only specified sections checked;
- `verified_abstract_and_metadata`: bibliographic record and abstract checked; equations not verified;
- `partially_verified_abstract`: abstract supports only the recorded high-level claim;
- `verified_metadata`: title, authors, venue, year, and DOI checked only;
- `inaccessible`: source identified but substantive content unavailable;
- `contradicted`: source does not support the claim for which it was proposed;
- `superseded`: retained for history but replaced by a more authoritative derivation.

A source with abstract-only verification may establish that an overlap risk exists, but it cannot support implementation of an equation or covariance.

## Required source fields

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
- covariance basis;
- PSD convention;
- main assumptions;
- limitations;
- direct relevance to R06;
- novelty implication;
- claim status.

Do not infer an equation from a paper that only cites another source. Trace the equation to the earliest accessible authoritative derivation where practical.

## Novelty audit

The novelty search must test whether prior work already combines:

- self-consistent drift-diffusion-Poisson electrostatics;
- both electron and hole populations;
- explicit trap occupancy;
- finite contact recombination or injection;
- stochastic contact exchange;
- frequency-domain Langevin transport;
- an externally conserved terminal-current observable;
- optical generation;
- HgCdTe material physics;
- finite-device GR-noise prediction;
- dimensionless failure criteria for a lumped Lorentzian model.

Novelty is evaluated by physics and observable, not by exact composition, geometry, numerical package, or parameter values.

### Rejected broad statement

The following is no longer acceptable:

> Existing HgCdTe GR-noise treatments are spatially uniform, so resolving finite size, diffusion, Poisson coupling, and contacts is new.

Finite-size space-charge/diffusion theory, bipolar finite-device theory, finite-contact theory, and HgCdTe contact/trap theory already exist.

### Current narrowed hypothesis

The unresolved candidate contribution is:

> A thermodynamically closed, bipolar HgCdTe photoconductor model with explicit trap kinetics, stochastic finite-contact exchange, optical generation, a conserved terminal circuit observable, and dimensionless error bounds may identify when terminal GR amplitude, corner frequency, and apparent spectral slope cease to represent one bulk lifetime.

This is a search target, not a claim.

## Evidence classes

Use:

- `source-established`: explicitly derived or measured in the cited source;
- `source-established_abstract`: supported only at abstract level;
- `source-established_metadata`: bibliographic or provenance fact only;
- `project-derivation`: derived within R06 from stated assumptions;
- `model-conditioned`: follows only for the selected closure or boundary model;
- `sensitivity-case`: exploratory parameter choice;
- `synthetic-validation`: numerical recovery using generated data;
- `material-validation`: comparison with independent HgCdTe measurements;
- `unresolved`: evidence is incomplete or conflicting.

## Files

- `literature_matrix.csv` — one row per source/model combination;
- `prior_art_phase1a.md` — current overlap and novelty assessment;
- later claim-level notes should use stable filenames keyed by first author and year;
- inaccessible sources remain listed with status `inaccessible` and are not cited as verified equation evidence.

## Highest-priority full-text acquisitions

1. Zocchi 2006 — `10.1103/PhysRevB.73.035203`;
2. Park 2022 — `10.1063/5.0111954`;
3. Smith 1984 — `10.1063/1.334155`;
4. Iverson and Smith 1985 — `10.1063/1.335666`;
5. Bonani and Ghione 1999 — `10.1016/S0038-1101(98)00253-6`;
6. Bulashenko et al. 1998 — `10.1063/1.367023`.

## Phase 1 completion rule

The literature gate is not complete until the matrix supports decisions on:

1. deterministic state equations;
2. contact and terminal boundary conditions;
3. primitive stochastic processes and covariance;
4. equilibrium fluctuation-dissipation test;
5. HgCdTe parameter ranges and uncertainty classes;
6. prior-art boundary;
7. the dimensional role and limitation of the 1D geometry;
8. whether Phase 2 should proceed, be narrowed, or terminate.

Production simulation remains prohibited until a decision record closes these items.
