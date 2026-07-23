# R06 Phase 1A equation-audit gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Decision:** continue Phase 1A; accept the provisional dimensionless reduction and benchmark architecture; production simulation remains unauthorized

## Evidence added

This gate incorporates:

- equation-level audit notes for Iverson and Smith (1985);
- detailed source audit for Bonani and Ghione (1999);
- full-text methodological audit for Bulashenko et al. (1998);
- identification of Smith (1982) as a missing foundational intrinsic-photoconductor source;
- a reduced nondimensional formulation;
- a quantitative analytical/numerical benchmark ladder;
- a source-acquisition queue with exact known DOIs.

## Scientific decision

The program remains viable only as a narrowly defined quantitative study. The included physical mechanisms do not constitute novelty by themselves.

The following working objective is retained:

> Determine controlled, uncertainty-qualified error bounds for reducing a bipolar finite HgCdTe photoconductor with dynamic traps, space charge, finite stochastic contacts, optical generation, and an external terminal circuit to conventional quasineutral, ohmic-contact, or single-Lorentzian interpretations.

## Accepted provisional results

### 1. Primitive-source reference model

The fundamental implementation must use population/event sources for electron, hole, trap, transport, and contact processes. Equivalent-current sources are reduced alternatives and must not be enabled simultaneously for the same transition family.

### 2. Dynamic trap state

At least one explicit trap-occupancy variable is required in the reference stochastic model. Algebraic SRH may be used only after a controlled stochastic elimination derives its memory kernel and covariance.

### 3. Independent terminal solver

The project will require both:

- direct frequency-domain covariance propagation;
- an adjoint or impedance-field terminal-noise calculation.

Agreement is an acceptance test, not a novelty result.

### 4. Reduced baseline controls

For the nondegenerate isothermal baseline, the principal transport/electrostatic controls are provisionally:

- `Pi_D = L/sqrt(D_r tau_r)`;
- `Lambda = L/L_D,r`;
- `U = q V_b/(k_B T)`;
- bipolar mobility and equilibrium-density ratios;
- carrier- and contact-specific Biot numbers;
- optical depth and injection amplitude;
- trap-density, trap-energy, and nonredundant transition-rate ratios;
- normalized external impedance.

Transit and dielectric-relaxation ratios are treated as derived under this closure rather than independently swept.

### 5. Benchmark ladder

The B0–B9 sequence in `benchmarks/transport_noise/phase1a_benchmark_spec.md` is accepted as the provisional validation architecture.

## Not accepted

The following remain unresolved:

- final stochastic finite-contact covariance;
- exact overlap with Zocchi (2006);
- exact finite-contact treatment in Park (2022);
- exact blocking-contact HgCdTe limit in Smith (1984);
- the DOI and full derivation of Smith (1982);
- whether degenerate/nonparabolic generalized Einstein corrections materially shift the proposed regime boundaries;
- a defensible claim that any remaining quantitative output is novel.

## Required sources

Critical equation-level acquisitions:

1. Zocchi 2006 — `10.1103/PhysRevB.73.035203`;
2. Park 2022 — `10.1063/5.0111954`;
3. Smith 1984 — `10.1063/1.334155`;
4. Smith 1982 — Journal of Applied Physics 53, 7051–7060; DOI unresolved.

Useful clean copies:

- Bonani and Ghione 1999 — `10.1016/S0038-1101(98)00253-6`;
- Bulashenko et al. 1998 — `10.1063/1.367023`;
- Iverson and Smith 1985 — `10.1063/1.335666`;
- Shockley and Read 1952 — `10.1103/PhysRev.87.835`.

## Authorization

Authorized next:

- ingest and audit supplied sources;
- derive the stochastic finite-contact detailed-balance boundary;
- derive the generalized Einstein correction and a nondegenerate-validity metric;
- complete analytical benchmark equations and tolerances;
- prepare the final Phase 1 proceed/reframe/terminate decision.

Still not authorized:

- production parameter sweeps;
- paper drafting;
- claims of novelty;
- arbitrary fitted noise sources;
- three-dimensional simulation.

## Stop rule

Reframe R06 as a reproducible benchmark/synthesis contribution if the remaining sources already establish the finite stochastic contact closure and quantitative reduction-error results. Terminate the paper objective if public HgCdTe parameter uncertainty prevents at least one robust, falsifiable regime boundary.