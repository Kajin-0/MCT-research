# R06 Phase 1C nonlinear-verification targets

**Controlling issue:** #346  
**Scope:** restricted dimensionless steady unipolar finite-volume kernel  
**Status:** executable verification contract; not a material-accurate HgCdTe model

## N0 — exact equilibrium

For equal reservoir potentials and densities with density equal to the fixed background, the initial state must satisfy the nonlinear system without iteration.

Acceptance:

- residual infinity norm below `1e-12`;
- zero Newton steps;
- zero face-current variation to floating-point precision.

## N1 — perturbed equilibrium recovery

From smooth perturbations in potential and log density, damped Newton must recover the equilibrium state.

Acceptance:

- converged residual below the declared absolute/relative target;
- no non-finite state or residual;
- final state error below `1e-10` in infinity norm for the reference case.

## N2 — line-search globalization

A difficult but recoverable initial state must require at least one damping factor below unity and still converge.

A deliberately restricted line search must fail explicitly with termination reason `line_search_failed`; it must not return NaNs, negative density, or a false convergence result.

## N3 — voltage continuation

Starting from zero bias, continue the right reservoir potential in finite increments. For equal reservoir density and background density, recover the exact uniform-resistor solution:

\[
\psi(x)=Vx/L,
\qquad
N(x)=1,
\qquad
j=-d_nV/L.
\]

Acceptance:

- every continuation point converges;
- final potential and density agree with the exact state within `1e-12`;
- face current is spatially constant within `1e-11` relative variation.

## N4 — continuous manufactured solution

Use

\[
\psi(x)=ax+b\sin(\pi x/L),
\]

\[
N(x)=\exp[c\sin(\pi x/L)].
\]

The continuous forcing is derived from

\[
R_\psi=\psi''-\Lambda^2(N-N_B),
\]

\[
j=d_n(N'-N\psi'),
\qquad
R_n=j'.
\]

The forcing is evaluated analytically at interior nodes. It is not obtained by applying the discrete operator to the sampled exact state.

## N5 — mesh refinement

Solve the manufactured problem on at least three successively refined meshes.

Report:

- potential and density `L_inf` errors;
- potential and density discrete `L_2` errors;
- nonlinear iteration counts;
- observed consecutive convergence orders.

Acceptance for the current smooth uniform-mesh reference:

- observed potential `L_inf` order greater than `1.9`;
- observed density `L_inf` order greater than `1.9`;
- no growth in nonlinear iteration count that indicates mesh-dependent loss of robustness.

## N6 — residual block diagnostics

Each accepted Newton step must record:

- full residual infinity norm before and after the step;
- Poisson-block infinity norm;
- continuity-block infinity norm;
- Newton step infinity norm;
- accepted damping factor;
- number of backtracks;
- dense Jacobian condition estimate.

Termination must be explicit:

- `initial_residual_converged`;
- `residual_converged`;
- `singular_jacobian`;
- `nonfinite_newton_step`;
- `line_search_failed`;
- `step_stagnation`;
- `maximum_iterations`.

## N7 — positivity and finite-state handling

Density remains represented as `N=exp(nu)`. Trial states producing overflow, non-finite density, or non-finite residual are rejected by the line search.

No clipping of density is permitted because clipping would alter the residual and Jacobian semantics.

## N8 — coordinate sparse representation

Serialize the verified dense analytical Jacobian to a dependency-free COO representation and reconstruct it exactly.

This gate verifies sparse storage semantics only. It is not an independent sparse assembly and does not authorize a sparse production solver.

Acceptance:

- exact dense round-trip equality;
- stored entries fewer than dense matrix entries for the reference problem;
- no drop tolerance in the equality test.

## N9 — source-free conservation

For source-free converged states, compute face-current variation independently of residual assembly.

Acceptance:

\[
\frac{\max j-\min j}{\max(1,\max|j|)}<10^{-11}
\]

for the equilibrium and uniform-resistor verification cases.

For a manufactured problem with nonzero continuity forcing, spatially varying current is expected and must not be mislabeled as a conservation defect.

## Current local evidence

The focused nonlinear-verification test module reports 16 passing tests locally. Together with the previously merged 46 Phase 1C tests, the expected repository total increases by 16 tests. GitHub Actions remains authoritative for the branch head.

## Gate boundary

Passing N0-N9 authorizes specification of the bipolar deterministic block and an independent sparse assembly. It does not authorize:

- material-accurate HgCdTe simulation;
- traps, optical generation, or dynamic contacts;
- stochastic linearization or PSD production;
- predictive detector claims;
- manuscript drafting.
