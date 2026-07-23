# R06 Phase 1C acceptance matrix

| Gate | Required evidence | Current status | Pass condition | Failure action |
|---|---|---|---|---|
| Carrier statistics | Boltzmann versus Fermi-Dirac/Kane comparison over intended `x,T,n,p` domain | Architecture accepted; exact Madarasz/Lowney equations pending | Maximum declared observable error below selected tolerance, or generalized statistics adopted | Narrow domain or adopt higher-fidelity closure |
| Generalized Einstein relation | `D/mu` derived from carrier compressibility | Accepted at architecture level; parabolic prototype verified | Positive diffusion coefficient and source-consistent equilibrium FDT | Reject transport closure |
| Permittivity and screening | Verified `epsilon(x,T)` range and screening sensitivity | Open | Screening regime remains classifiable under uncertainty | Reframe regime map as exploratory |
| Mobility | Electron/hole ranges with field and specimen context | Open | At least bounded low-field reference and mobility-ratio sweep | Do not make quantitative HgCdTe claims |
| Trap kinetics | Energy, density, capture rates, detailed-balance emissions | Kinetic structure accepted; material ranges exploratory | Four positive propensities and equilibrium occupancy recover SRH mean limit | Retain exploratory trap parameters only |
| Optical generation | Uniform reference plus sourced or exploratory absorption depth | Uniform generation allowed; absorption relation open | Pair-generation normalization and units verified | Defer Beer-Lambert calculations |
| Contacts | Ideal exchange, interface-state, blocking, and reduced-`S` hierarchy | Architecture accepted | Mean and fluctuation models separated; electrochemical potentials defined | Restrict to ideal reservoir benchmarks |
| External circuit | Fixed-voltage, fixed-current, and finite-load formulations | Architecture specified; executable circuit state pending | Terminal observable and equilibrium ensemble unambiguous | Defer stochastic terminal claims |
| Discretization | Conservative finite volume with fitted fluxes | **Prototype passed**: exact equilibrium, uniform resistor, diffusion limit, telescoping balance | Exact discrete source-flux balance and mesh convergence | Revise flux formulation |
| Residual Jacobian | Independent derivative verification | **Prototype passed locally** against centered finite differences | Cross-check below declared absolute/relative tolerance | Revise analytical derivatives |
| Nonlinear solution | Scaling and continuation strategy | Open | Reproducible convergence from equilibrium to target controls | Restrict operating domain |
| Independent verification | Analytical or second discretization | Exact benchmark checks present; second implementation pending | Cross-method error below declared tolerance | No Phase 2 authorization |
| Research viability | Candidate reduction observable stable under parameter uncertainty | Open | At least one falsifiable error boundary remains | Reframe as benchmark/synthesis or terminate paper objective |

## Required final report

The final Phase 1 gate must list for each row:

- evidence completed;
- quantitative metric;
- pass/fail decision;
- unresolved uncertainty;
- effect on authorized Phase 2 scope.