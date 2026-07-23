# R06 Phase 1C deterministic-kernel benchmark targets

**Controlling issue:** #346  
**Status:** executable prototype targets; no production transport authorization

## D0 — Bernoulli function

Verify over small, moderate, and asymptotic arguments:

\[
B(z)=\frac{z}{e^z-1},
\qquad
B(-z)=B(z)+z.
\]

Required points include `z=0`, `±1e-7`, `±5`, and `±80`.

Verify the analytical derivative against centered finite differences over `-10 <= z <= 10`.

## D1 — positive state reconstruction

Use logarithmic interior density variables,

\[
N_i=e^{\nu_i},
\]

and verify that every finite state vector reconstructs positive density. Invalid boundary density and nonfinite states must be rejected.

## D2 — uniform thermal equilibrium

For

\[
\psi=0,
\qquad
N=N_B=1,
\]

require

\[
\|R\|_\infty<10^{-13}.
\]

Repeat for at least three mesh sizes after the first nonlinear solver is added.

## D3 — exact uniform resistor

For a domain of length `ell`, constant density, normalized voltage `U`, and diffusion ratio `d_n`, verify

\[
\psi(x)=-Ux/\ell,
\qquad
j_n=d_nU/\ell.
\]

Required checks:

- Poisson residual below `1e-12`;
- continuity residual below `1e-12`;
- face current relative variation below `1e-12`;
- current independent of mesh spacing to floating-point tolerance.

## D4 — zero-field diffusion limit

For constant potential, verify

\[
j_{i+1/2}
=\frac{d_n}{h}(N_{i+1}-N_i).
\]

This test fixes the diffusion sign independently of the drift benchmark.

## D5 — conservative telescoping identity

For an arbitrary finite state, verify

\[
h\sum_iR_{n,i}
=j_{right}-j_{left}
\]

to floating-point tolerance.

This is a discrete structural identity, not a convergence metric.

## D6 — analytical Jacobian

Compare the analytical residual Jacobian with centered finite differences at a nonuniform state containing:

- nonzero bias;
- nonuniform density;
- nonunit background density;
- nonunit diffusion ratio;
- nonzero screening strength.

Initial acceptance:

\[
\max|J_{analytic}-J_{FD}|<2\times10^{-8}
\]

with relative tolerance `3e-8` for the declared finite-difference step.

Before Phase 2 production work, add a complex-step or automatic-differentiation cross-check where compatible with the residual implementation.

## D7 — screening block

For a prescribed density perturbation and zero potential perturbation, verify the local Poisson derivative

\[
\frac{\partial R_{\psi,i}}{\partial\nu_i}
=-\Lambda^2N_i.
\]

When generalized statistics are connected, the physical screening response must be compared against the susceptibility-based closure rather than inferred solely from log density.

## D8 — nonlinear solve gate

A damped Newton solver is not yet part of this increment. Its first acceptance cases will be:

1. uniform equilibrium from perturbed initial states;
2. exact uniform resistor from voltage continuation;
3. zero-screening diffusion problem;
4. nonzero-screening problem with known manufactured solution.

Required reporting:

- residual history;
- step damping;
- Jacobian condition estimate where available;
- conservation metrics recomputed outside the residual function.

## D9 — mesh refinement

After the nonlinear solver is implemented, use at least four meshes with refinement ratio two. Report observed convergence for:

- potential;
- density;
- terminal current;
- integrated charge;
- residual-independent current variation.

The exact uniform resistor should exhibit no discretization error beyond roundoff. Nonuniform manufactured solutions should demonstrate the expected order of the selected Poisson and fitted-flux discretization.

## D10 — scope boundary

Passing D0–D9 supports only the deterministic numerical architecture. It does not validate:

- HgCdTe material parameters;
- bipolar transport;
- trap kinetics;
- stochastic covariance;
- terminal noise;
- responsivity or detectivity;
- a novelty claim.

Those gates remain separate.