# R06 Phase 1C bipolar nonlinear verification gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** provisionally accept the restricted bipolar nonlinear verification package pending current-head CI

## Accepted scope

The package extends the previously accepted dimensionless source-free bipolar
finite-volume block with:

- residual-decreasing damped Newton iteration;
- explicit three-block residual diagnostics;
- controlled nonlinear failure reasons;
- right-contact voltage continuation;
- continuous manufactured Poisson, electron-continuity, and hole-continuity forcing;
- three-level mesh refinement and observed-order calculation;
- independent terminal-versus-volume continuity balance for each carrier;
- dependency-free COO serialization of the dense analytical Jacobian.

The state remains

\[
u=(\psi,\log N,\log P),
\]

so both carrier densities remain positive for every finite numerical state.

## Nonlinear globalization

At Newton iteration `k`, the analytical bipolar Jacobian is used in

\[
J(u_k)\Delta u_k=-R(u_k).
\]

The trial state is

\[
u_{k+1}=u_k+\alpha_k\Delta u_k,
\qquad 0<\alpha_k\leq1.
\]

Backtracking accepts a step only when the residual two-norm satisfies the
declared sufficient-decrease condition. Invalid or non-finite trial residuals
are rejected without changing the accepted state.

The implementation distinguishes:

- initial residual convergence;
- residual convergence;
- singular Jacobian;
- non-finite Newton step;
- line-search failure;
- step stagnation;
- maximum-iteration termination.

## Manufactured forcing

The accepted manufactured state uses sinusoidal log-density perturbations and a
linear-plus-sinusoidal potential. Continuous derivatives are evaluated
analytically before sampling on the finite-volume mesh.

Electron forcing is derived from

\[
\frac{d j_n}{dx}
=
d_n N\left[
(\log N)'((\log N)'-\psi')
+(\log N)''-\psi''
\right].
\]

Hole forcing is derived independently from

\[
\frac{d j_p}{dx}
=
-d_p P\left[
(\log P)'((\log P)'+\psi')
+(\log P)''+\psi''
\right].
\]

This preserves the previously accepted electron and hole current signs.

## Continuity balance

For each carrier, the diagnostic compares

\[
j_R-j_L
\]

with

\[
h\sum_i S_i.
\]

This is evaluated from reconstructed face currents independently of the
nonlinear residual norm. It therefore checks the conservative telescoping
identity for source-free and forced cases without assuming that face current is
constant when a volume source is present.

## Local verification evidence

A focused isolated test run reports **14 passed tests**.

Verified locally:

- exact equilibrium terminates without iteration;
- perturbed equilibrium converges;
- a declared difficult state activates damping and converges;
- disabling backtracking produces controlled `line_search_failed` termination;
- voltage continuation recovers the exact neutral bipolar resistor;
- source-free continuity telescopes for each carrier;
- the sampled continuous manufactured residual decreases by approximately four
  under each mesh halving;
- manufactured potential, electron density, and hole density converge at
  approximately second order;
- forced terminal-versus-volume balance closes below `1e-11` for both carriers;
- COO reconstruction equals the dense analytical Jacobian exactly;
- invalid states, forcing, continuation counts, and manufactured parameters are
  rejected.

Reference local observed `L_inf` orders:

- potential: approximately `1.999`, `2.000`;
- electron density: approximately `2.001`, `1.999`;
- hole density: approximately `1.996`, `2.000`.

GitHub Actions remains the repository-level authority for the committed head.

## Scientific interpretation

This gate validates nonlinear globalization and spatial-convergence architecture
for the restricted bipolar equations. It does not establish that these
Boltzmann, source-free, ideal-reservoir equations are quantitatively adequate
for HgCdTe.

The dense Jacobian remains a transparent verification implementation. COO
serialization demonstrates storage equivalence only; independent sparse
assembly and sparse linear solution remain future work.

## Authorization after green CI

Authorize next:

1. merge this nonlinear verification increment;
2. select the first deterministic physical source term;
3. specify equilibrium-consistent electron-hole recombination before adding it;
4. verify detailed balance and conservation with that source;
5. continue exact Kane statistics, mobility, and static-permittivity audits;
6. prepare the final Phase 1 proceed/reframe/terminate decision.

Still unauthorized:

- material-accurate HgCdTe device simulation;
- broad parameter sweeps;
- phenomenological lifetime insertion without an equilibrium gate;
- trap kinetics before the deterministic recombination sign and balance gate;
- optical generation before dark equilibrium is preserved;
- stochastic covariance assembly or PSD production;
- predictive responsivity, detectivity, or terminal-noise claims;
- manuscript or novelty claims.

## Failure and rollback conditions

Revise or reject this package if current-head CI shows that:

- the analytical bipolar Jacobian is incompatible with the nonlinear solve;
- any accepted iteration increases the required residual measure;
- manufactured convergence is below the declared threshold;
- electron or hole global balance fails independently;
- Python-version behavior changes the deterministic results;
- the package API breaks the previously merged unipolar or bipolar tests.

## Final gate condition

This decision becomes accepted only after all current-head repository workflows
complete successfully. Until then, the PR remains draft and no downstream
physical source model is authorized.
