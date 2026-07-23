# R06 Phase 1C bipolar nonlinear verification targets

**Status:** executable numerical-architecture gate  
**Scope:** dimensionless steady one-dimensional bipolar finite volume  
**Controlling issue:** #346

## Purpose

This benchmark contract determines whether the verified source-free bipolar
residual can be solved robustly and whether its spatial discretization recovers
smooth continuous solutions at the expected order.

It does not validate HgCdTe material parameters, recombination, traps, optical
generation, contacts, circuit loading, stochastic forcing, or detector-level
predictions.

## State and residual

The interior state is

\[
u=(\psi,\log N,\log P),
\]

with residual blocks

\[
R=(R_\psi,R_n,R_p).
\]

The nonlinear solve uses the analytical dense Jacobian already accepted for the
bipolar finite-volume block.

## BN0 — exact equilibrium

For zero bias, equal constant electron and hole densities, and zero fixed charge:

- the linear-reservoir state must have zero residual to roundoff;
- the solver must terminate without a Newton iteration;
- both terminal-current differences must vanish.

## BN1 — perturbed equilibrium recovery

A deterministic finite perturbation of all three state blocks must converge to
the equilibrium state.

Acceptance:

- explicit converged status;
- final residual no greater than the declared target;
- finite state and diagnostics;
- electron and hole global continuity mismatches below `1e-10`.

## BN2 — damping activation

A declared difficult initial state must require at least one accepted damping
factor below unity and still converge.

Each accepted iteration must reduce the residual infinity norm.

## BN3 — controlled line-search failure

With backtracking deliberately disabled and a strict sufficient-decrease test,
the solver must return

`line_search_failed`

rather than NaNs, an exception from an accepted state, or false convergence.

## BN4 — voltage continuation

Starting from zero bias, right-contact potential continuation must recover the
exact neutral bipolar resistor at the final bias.

Acceptance:

- every continuation point converges;
- potential is linear;
- both carrier densities remain constant;
- electron and hole face currents are spatially constant to roundoff.

## BN5 — continuous manufactured forcing

Use

\[
\psi=a_\psi x/L+b_\psi\sin(\pi x/L),
\]

\[
\log N=\log N_0+a_n\sin(\pi x/L),
\qquad
\log P=\log P_0+a_p\sin(\pi x/L).
\]

The continuous forcing is evaluated analytically from

\[
R_\psi=\psi''-\Lambda^2(N-P-C),
\]

\[
R_n=d_n\frac{d}{dx}(N'-N\psi'),
\]

\[
R_p=\frac{d}{dx}\left[-d_p(P'+P\psi')\right].
\]

The discrete residual of the sampled continuous state must decrease by
approximately four when the mesh spacing is halved.

## BN6 — manufactured-solution refinement

Solve the continuously forced problem on at least three successively refined
meshes.

Acceptance:

- every nonlinear solve converges;
- observed `L_inf` order exceeds `1.95` for potential;
- observed `L_inf` order exceeds `1.95` for electron density;
- observed `L_inf` order exceeds `1.95` for hole density.

The reference three-level local result is approximately:

- potential: `1.999`, `2.000`;
- electron density: `2.001`, `1.999`;
- hole density: `1.996`, `2.000`.

These values are numerical evidence for the declared manufactured case, not a
material prediction.

## BN7 — global continuity balance

For each carrier,

\[
j_R-j_L=h\sum_i S_i
\]

must hold independently, where `S_i` is the declared continuity forcing.

For source-free cases, this reduces to equality of the two terminal currents.
For manufactured cases, terminal-current difference must equal the integrated
volume forcing.

Acceptance: relative mismatch below `1e-11` for both carriers after convergence.

## BN8 — Jacobian storage equivalence

The dependency-free COO representation must reconstruct the dense analytical
bipolar Jacobian exactly when no entries are dropped.

This is a storage-layout test, not an independent sparse assembly or sparse
linear-solver claim.

## BN9 — diagnostics and rejection paths

The implementation must report:

- separate residual norms for Poisson, electron continuity, and hole continuity;
- accepted damping and backtrack count;
- Newton-step norm;
- Jacobian condition estimate;
- termination reason;
- carrier-specific current and continuity-balance diagnostics.

Invalid state dimensions, non-finite states, invalid continuation counts,
invalid forcing shapes, and non-positive manufactured boundary densities must be
rejected explicitly.

## BN10 — scientific boundary

Passing BN0–BN9 authorizes only the next deterministic model gate.

It does not authorize:

- material-accurate HgCdTe simulation;
- recombination or dynamic traps;
- optical generation;
- finite-rate contacts or external circuit state;
- stochastic linearization or PSD production;
- responsivity, detectivity, or terminal-noise predictions;
- novelty or manuscript claims.
