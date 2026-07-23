# R06 Phase 1C bipolar deterministic block gate

**Date:** 2026-07-23  
**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Decision:** provisionally accept the restricted source-free bipolar finite-volume block; retain Phase 1C; material and stochastic production work remain unauthorized

## Implemented scope

The branch adds:

- fixed-potential, fixed-electron-density, and fixed-hole-density reservoirs;
- logarithmic electron and hole density unknowns;
- bipolar Poisson charge `N-P-C`;
- the merged fitted electron face current;
- an independently derived fitted hole face current;
- conservative electron and hole continuity residuals;
- a dense analytical three-block Jacobian;
- independent current-conservation metrics for each carrier;
- a linear reservoir-state constructor;
- an explicit B0-B11 benchmark contract.

The state ordering is

\[
u=(\psi,\log N,\log P)^T,
\]

and the residual ordering is

\[
R=(R_\psi,R_n,R_p)^T.
\]

## Accepted sign structure

The conventional currents are

\[
j_n=d_n(\partial_xN-N\partial_x\psi),
\]

\[
j_p=-d_p(\partial_xP+P\partial_x\psi).
\]

The accepted hole face flux is

\[
j_{p,i+1/2}
=
\frac{d_p}{h}
\left[
B(\Delta\psi_i)P_i
-
B(-\Delta\psi_i)P_{i+1}
\right].
\]

The Poisson residual is

\[
R_{\psi,i}
=
\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{h^2}
-
\Lambda^2(N_i-P_i-C).
\]

## Local verification evidence

A focused local harness reports **13 passed tests**.

Verified properties include:

- zero-residual uniform neutral equilibrium;
- exact biased neutral-resistor currents for both carriers;
- opposite electron and hole diffusion signs at zero field;
- exact telescoping of both continuity blocks;
- full analytical Jacobian agreement with centered finite differences;
- absence of direct electron-to-hole and hole-to-electron continuity Jacobian blocks;
- electron-hole symmetry under potential, charge, density, and diffusion exchange;
- exact recovery of the merged unipolar Poisson and electron blocks when the hole population is held constant;
- positive density reconstruction;
- invalid configuration rejection.

GitHub Actions remains authoritative for the committed branch head.

## Scientific interpretation

This increment validates the deterministic bipolar sign and block architecture. It does not validate a quantitative HgCdTe carrier model.

The direct cross-carrier continuity blocks are zero only because recombination, traps, and pair generation are absent from this restricted benchmark. Those blocks must become nonzero when physically shared carrier events are introduced.

## Authorization

Authorized next after current-head CI:

1. apply the verified damped-Newton globalization to the bipolar residual;
2. add bipolar manufactured-solution and mesh-refinement tests;
3. connect equilibrium densities and susceptibilities through the accepted statistics interface;
4. specify one explicit two-state trap block and four event channels;
5. continue low-temperature mobility and static-permittivity audits;
6. evaluate the final Phase 1 proceed/reframe/terminate gate.

Still unauthorized:

- material-accurate HgCdTe production simulation;
- broad composition, temperature, bias, or trap sweeps;
- predictive responsivity, detectivity, contact, or noise claims;
- stochastic PSD production code;
- manuscript drafting;
- novelty claims;
- three-dimensional simulation.

## Failure and rollback conditions

Revise or reject the block if:

- the hole flux sign fails an independent analytical limit;
- the Jacobian fails current-head finite-difference tests;
- electron-hole symmetry is broken without an explicitly asymmetric parameter;
- the unipolar reduction no longer reproduces the merged one-carrier kernel;
- either continuity block loses exact telescoping;
- later event-level detailed balance requires incompatible deterministic state conventions.

## Merge condition

This gate becomes accepted rather than provisional only when all current-head GitHub Actions checks pass and the branch remains limited to the declared bipolar deterministic architecture.
