# R06 Phase 1C deterministic-kernel gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** accept the restricted conservative unipolar finite-volume prototype; continue Phase 1C; production transport remains unauthorized

## Implemented scope

The accepted prototype contains:

- a uniform one-dimensional node mesh;
- dimensionless potential and positive log-density unknowns;
- one mobile electron population;
- fixed positive background charge;
- ideal fixed-potential/fixed-density reservoir values;
- Poisson residual;
- source-free conservative continuity residual;
- Scharfetter-Gummel fitted electron face current;
- dense analytical Jacobian;
- independent face-current conservation metrics.

It contains no holes, traps, recombination, illumination, stochastic operators, dynamic contacts, external circuit state, or material-specific HgCdTe parameter set.

## Accepted equations

The dimensionless electron current is

\[
j_n=d_n(\partial_xN-N\partial_x\psi).
\]

The face current is

\[
j_{i+1/2}
=
\frac{d_n}{h}
\left[
B(\psi_{i+1}-\psi_i)N_{i+1}
-
B(\psi_i-\psi_{i+1})N_i
\right].
\]

The interior residuals are

\[
R_{\psi,i}
=
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{h^2}
-
\Lambda^2(N_i-N_B),
\]

\[
R_{n,i}
=
\frac{j_{i+1/2}-j_{i-1/2}}{h}.
\]

## Validation completed

Local isolated testing of the statistics and finite-volume prototype package reports 46 passed tests.

Finite-volume evidence includes:

- stable Bernoulli evaluation and symmetry;
- analytical Bernoulli derivative agreement;
- positive density reconstruction;
- exact equilibrium residual;
- exact biased uniform-resistor residual and current;
- correct zero-field diffusion limit;
- exact telescoping continuity balance;
- analytical Jacobian agreement with finite differences;
- invalid configuration rejection.

GitHub Actions remains the repository-level authority for the committed head.

## Scientific interpretation

This increment validates numerical signs and conservation architecture only. It does not establish that the selected one-carrier equations are quantitatively adequate for HgCdTe.

The fitted flux is accepted because it is exact for the local constant-current problem under piecewise-linear potential. The logarithmic density variable is accepted as a positivity device. The dense Jacobian is accepted only as a transparent Phase 1 verification implementation; sparse assembly is required later.

## Authorization

Authorized next:

1. export the prototype through the package API;
2. add a damped Newton solver limited to exact and manufactured benchmarks;
3. add mesh-refinement and continuation tests;
4. specify the bipolar block structure;
5. connect equilibrium density and susceptibility through the statistics interface;
6. continue mobility and permittivity source audits;
7. prepare the final Phase 1 gate.

Still unauthorized:

- material-accurate HgCdTe detector simulation;
- broad parameter sweeps;
- trap or optical production models;
- stochastic linearization and PSD production code;
- predictive terminal noise, responsivity, or detectivity claims;
- manuscript drafting;
- novelty claims.

## Failure and rollback conditions

Revise the prototype if:

- current conservation is lost under mesh refinement;
- the analytical Jacobian fails an independent derivative check;
- fitted flux signs conflict with the project terminal convention;
- sparse implementation changes the residual semantics;
- equilibrium FDT later requires a deterministic state convention incompatible with this residual.

## Next gate

The next numerical gate is a damped Newton and manufactured-solution package. The next material gate remains the exact Kane/intrinsic-density equation audit plus low-temperature mobility and static permittivity provenance.