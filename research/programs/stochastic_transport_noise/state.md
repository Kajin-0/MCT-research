# Stochastic transport and finite-size noise

**Last updated:** 2026-07-23  
**Program ID:** `stochastic_transport_noise`  
**Contribution:** R06  
**Controlling issue:** #339  
**Current phase:** Phase 1 — literature and model definition

## Objective

Develop a self-consistent stochastic drift-diffusion-Poisson theory for a finite one-dimensional HgCdTe photoconductor and determine how space charge, finite diffusion length, contact recombination, applied electric field, and optical generation modify:

1. nonlinear steady-state carrier, field, potential, recombination, and current distributions;
2. terminal resistance and current;
3. photoconductive responsivity;
4. terminal generation-recombination noise magnitude;
5. characteristic noise frequencies and modal bandwidths;
6. departures from a spatially uniform single-Lorentzian noise model.

The intended observable is the externally measurable terminal-current or terminal-voltage power spectral density under a declared electrical boundary condition and PSD convention. Local carrier-number fluctuations are intermediate state variables, not the final observable.

## Core scientific question

How do finite device dimensions, self-consistent electrostatics, contact boundary conditions, and carrier diffusion modify the terminal-current noise spectrum of an HgCdTe photoconductor relative to the conventional quasi-neutral, spatially uniform generation-recombination model?

## Current state

The program is a **gated active research program**. Phase 1 is authorized. Deterministic production simulations, stochastic parameter sweeps, manuscript drafting, and novelty claims are not authorized until the Phase 1 gate is passed.

No scientific result has yet been established. The current program state records scope, conventions to be fixed, verification requirements, prior-art risks, and termination criteria.

## Baseline geometry and physics

The baseline system is a one-dimensional slab on `x in [0,L]` with uniform cross-sectional area `A` and uniform HgCdTe composition.

Initial physical scope:

- temperature near 77 K;
- applied terminal voltage `V_b`;
- uniform or Beer-Lambert optical generation;
- electron and hole drift-diffusion transport;
- Poisson electrostatics;
- Shockley-Read-Hall recombination;
- Ohmic, finite-recombination, or blocking-contact limits;
- small-signal frequency-domain perturbations around the nonlinear steady state;
- bulk, transport, and contact Langevin sources only when their covariance follows from an authoritative derivation, local detailed balance, or fluctuation-dissipation consistency.

Radiative and Auger recombination are deferred until the SRH baseline and its equilibrium limit are verified.

## Baseline deterministic equations

The sign convention is provisional until the Phase 1 conventions document is accepted. The intended convention uses electrostatic potential `phi`, electric field `E = -d phi/dx`, positive conventional current in the `+x` direction, and positive elementary charge `q > 0`.

The baseline equations are:

```text
d/dx(epsilon dphi/dx)
    = -q(p - n + N_D^+ - N_A^- + rho_t/q)

E = -dphi/dx

J_n = q mu_n n E + q D_n dn/dx
J_p = q mu_p p E - q D_p dp/dx

partial n/partial t = +(1/q) partial J_n/partial x + G - R
partial p/partial t = -(1/q) partial J_p/partial x + G - R
```

The initial recombination law is:

```text
R_SRH = (n p - n_i^2)
        / [tau_p (n + n_1) + tau_n (p + p_1)]
```

The final Phase 1 formulation must specify:

- whether `R` denotes net recombination or total event rate;
- trap-charge closure and trap occupancy;
- Einstein relations under nondegenerate and degenerate statistics;
- carrier-density definitions under Fermi-Dirac statistics;
- electrostatic and carrier boundary conditions;
- voltage-driven versus current-driven terminal conditions;
- displacement-current contribution to the measured terminal current.

## Stochastic formulation target

The fields are decomposed as:

```text
n = n_0 + delta n
p = p_0 + delta p
phi = phi_0 + delta phi
```

and transformed using `partial/partial t -> j omega`.

The linearized problem should ultimately have the operator form:

```text
(j omega M - J) delta u = B xi

delta I = c(omega)^T delta u + d(omega)^T xi
```

where:

- `delta u` contains the discretized carrier and electrostatic perturbations;
- `M` is the dynamic mass matrix;
- `J` is the Jacobian of the deterministic residual;
- `xi` contains independently defined primitive stochastic processes;
- `Q_xi(omega)` is their covariance matrix or covariance operator;
- `delta I` is the conserved external terminal-current perturbation.

The resulting terminal PSD is expected to be evaluated as:

```text
S_I(omega) = H(omega) Q_xi(omega) H(omega)^H
```

with all factor-of-two and angular-frequency conversions controlled by the declared PSD convention.

No stochastic source may be introduced solely because it produces a desired spectral shape.

## Initial dimensionless groups

The initial scaling analysis must assess, reduce, and if necessary replace:

- `Pi_D = L/L_D`, where `L_D = sqrt(D_ref tau_ref)`;
- `Pi_E = q E_ref L/(k_B T)` or an equivalent applied-voltage parameter;
- `Pi_C,n = S_n L/D_n` and `Pi_C,p = S_p L/D_p`;
- `Pi_lambda = L/L_Debye`;
- `Pi_G = G_ref tau_ref/n_ref`;
- `Pi_mu = mu_n/mu_p`;
- optical depth `Pi_alpha = alpha L`;
- compensation and equilibrium-injection ratios;
- trap-energy and trap-density ratios;
- degeneracy parameters relative to the band edges;
- dielectric relaxation to recombination-time ratio;
- transit-time to recombination-time ratio;
- normalized external impedance where terminal loading is not ideal.

The program must distinguish independent control parameters from derived combinations and avoid device-by-device sweeps that obscure similarity structure.

## Required limiting cases

The model is not considered physically verified until the relevant implementation recovers, within stated numerical tolerances:

1. thermal equilibrium at zero applied bias;
2. equilibrium detailed balance and zero mean terminal current;
3. Johnson-Nyquist terminal noise under the declared one-sided or two-sided convention;
4. strong-screening quasi-neutrality;
5. uniform-field drift-dominated transport;
6. diffusion-dominated transport;
7. infinite surface/contact recombination;
8. blocking-contact behavior;
9. bulk or infinite-device generation-recombination noise;
10. low-frequency GR-noise plateau;
11. high-frequency modal roll-off;
12. spatial conservation of total conduction plus displacement current;
13. agreement between at least two independent numerical or analytical methods for selected cases.

## Phase 1 deliverables

Phase 1 must produce:

1. a verified literature matrix and claim-level source ledger;
2. final governing equations and state-variable definitions;
3. carrier, electrostatic, optical, and terminal boundary conditions;
4. sign, Fourier-transform, angular-frequency, and PSD conventions;
5. source-covariance requirements and fluctuation-dissipation strategy;
6. parameter and uncertainty table for HgCdTe;
7. reduced dimensionless formulation;
8. prior-art and novelty-risk assessment;
9. deterministic and stochastic solver architecture;
10. numerical acceptance tests and convergence metrics;
11. unresolved scientific questions;
12. a decision record authorizing, revising, or terminating Phase 2.

## Planned later phases

### Phase 2 — deterministic baseline

- equilibrium solution;
- biased dark solution;
- illuminated solution;
- conservation checks;
- mesh-convergence study;
- analytical-limit comparisons.

### Phase 3 — linearized stochastic model

- Jacobian and mass operators;
- primitive source covariance;
- frequency-domain transfer functions;
- terminal-current conservation;
- equilibrium fluctuation-dissipation verification.

### Phase 4 — dimensionless parameter study

Sweep the independent groups established in Phase 1 rather than arbitrary device parameter sets.

### Phase 5 — theory extraction

Identify scaling laws, asymptotic formulas, regime boundaries, failure criteria for the lumped model, and falsifiable experimental predictions.

### Phase 6 — paper preparation

Paper preparation remains unauthorized until the evidence, novelty, and reproducibility gates are passed.

## Verification metrics

Later numerical work must report, as applicable:

- nonlinear residual norms by equation block;
- mesh-convergence error for terminal and field observables;
- frequency-grid convergence;
- global and local charge-conservation error;
- terminal-current conservation error;
- conditioning or pseudospectral sensitivity of the linearized operator;
- sensitivity to boundary-condition discretization;
- equilibrium Johnson-Nyquist relative error;
- bulk-GR-limit relative error;
- cross-method discrepancy;
- uncertainty sensitivity for weakly constrained material parameters.

Solver convergence is not evidence of physical correctness.

## Completed foundations

At program creation:

- repository governance supports independent programs and contribution tracking;
- shared literature, validation, derivation, benchmark, and test directories exist;
- public HgCdTe gap-law and selected material-relation infrastructure may be reusable after dependency review;
- issue #339 records the Phase 1 authorization boundary.

No stochastic transport solver or validated noise result is claimed as complete.

## Shared dependencies

Expected initial dependencies:

- repository literature and source-provenance conventions;
- general validation and benchmark organization;
- HgCdTe composition/temperature material relations where their observable and validity range match this program;
- uncertainty and sensitivity conventions.

Existing band-edge, spatial-disorder, and Kane program modules are intentionally not scientific dependencies unless a later PR documents a direct need and tests the interface.

## Unresolved scientific questions

1. Which primitive Langevin sources form a nonredundant covariance representation after Poisson coupling and contact constraints are imposed?
2. What contact model permits finite recombination while remaining thermodynamically consistent at equilibrium?
3. Under voltage bias, which external-circuit degrees of freedom must be included for exact Johnson-Nyquist recovery?
4. Does the one-dimensional model require explicit trap-occupancy dynamics to represent HgCdTe GR noise rather than an algebraic SRH closure?
5. Under what regimes can quasi-neutral ambipolar reduction reproduce the full drift-diffusion-Poisson spectrum within controlled error?
6. Which HgCdTe lifetime, mobility, trap, and surface-recombination relations are sufficiently established for quantitative regime boundaries?
7. Can overlapping discrete transport-recombination modes mimic an apparent `1/f^alpha` interval over experimentally meaningful bandwidths without a broad trap distribution?
8. Which terminal observable is most directly comparable to common photoconductor noise measurements: current under ideal voltage bias, voltage under current bias, or loaded transimpedance output?

## Novelty status and risks

Novelty is unresolved. A provisional hypothesis is:

> Existing HgCdTe GR-noise treatments often use quasi-neutral or spatially uniform carrier fluctuations, whereas this program seeks a terminal-current theory resolving coupled charge, electric-field, diffusion, recombination, and contact modes and the dimensionless boundaries where a lumped approximation fails.

This statement is not a novelty claim. It must be revised or rejected after verified prior-art review.

Principal novelty risks:

- equivalent finite-device stochastic drift-diffusion theories may already exist in semiconductor noise literature outside HgCdTe-specific indexing;
- impedance-field and Green-function device-noise methods may already imply the proposed terminal transfer formulation;
- contact and diffusion eigenmodes may already be established for photoconductors under different terminology;
- the HgCdTe specialization may be parameter substitution rather than new physics;
- apparent multimode behavior may reduce to known distributed-recombination or transmission-line results.

## Authorized next gate

Complete Phase 1 documentation and source verification. Do not begin broad simulations until a decision record confirms:

- internally consistent equations and conventions;
- non-arbitrary stochastic covariance;
- a viable equilibrium fluctuation-dissipation test;
- sufficient material-parameter support;
- a defensible prior-art boundary;
- a numerical plan with independent verification.

## Prohibited or unsupported claims

Until later gates pass, do not claim:

- original theory;
- quantitative prediction of HgCdTe detector noise;
- recovery of Johnson-Nyquist noise;
- measured or material validation;
- universal failure of the Lorentzian model;
- emergence of true `1/f` noise;
- identification of microscopic lifetime from a terminal noise corner;
- manuscript readiness.

## Termination or pause criteria

Pause, merge into established theory, or terminate the program if:

- materially equivalent coupled theory and observables are already established;
- fluctuation-dissipation consistency cannot be achieved under the intended state and boundary variables;
- the one-dimensional observable is structurally non-identifiable;
- uncertain material parameters prevent falsifiable regime boundaries;
- a reduced analytical model reproduces all departures within controlled tolerances;
- numerical conditioning makes the claimed modal interpretation nonrobust over the physical parameter range.

## Manuscript status

No manuscript is authorized. R06 is a candidate-work concept pending Phase 1 completion, prior-art review, and a positive Phase 2 decision gate.