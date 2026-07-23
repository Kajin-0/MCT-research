# R06 Phase 1C acceptance matrix

| Gate | Required evidence | Pass condition | Failure action |
|---|---|---|---|
| Carrier statistics | Boltzmann versus Fermi-Dirac/Kane comparison over intended `x,T,n,p` domain | Maximum declared observable error below selected tolerance, or generalized statistics adopted | Narrow domain or adopt higher-fidelity closure |
| Generalized Einstein relation | `D/mu` derived from carrier compressibility | Positive diffusion coefficient and source-consistent equilibrium FDT | Reject transport closure |
| Permittivity and screening | Verified `epsilon(x,T)` range and Debye-length sensitivity | Screening regime remains classifiable under uncertainty | Reframe regime map as exploratory |
| Mobility | Electron/hole ranges with field and specimen context | At least bounded low-field reference and mobility-ratio sweep | Do not make quantitative HgCdTe claims |
| Trap kinetics | Energy, density, capture rates, detailed-balance emissions | Four positive propensities and equilibrium occupancy recover SRH mean limit | Retain exploratory trap parameters only |
| Optical generation | Uniform reference plus sourced or exploratory absorption depth | Pair-generation normalization and units verified | Defer Beer-Lambert calculations |
| Contacts | Ideal exchange, interface-state, blocking, and reduced-`S` hierarchy | Mean and fluctuation models separated; electrochemical potentials defined | Restrict to ideal reservoir benchmarks |
| External circuit | Fixed-voltage, fixed-current, and finite-load formulations | Terminal observable and equilibrium ensemble unambiguous | Defer stochastic terminal claims |
| Discretization | Conservative finite volume with fitted fluxes | Exact discrete source-flux balance to solver tolerance | Revise flux formulation |
| Nonlinear solution | Scaling and continuation strategy | Reproducible convergence from equilibrium to target controls | Restrict operating domain |
| Independent verification | Analytical or second discretization | Cross-method error below declared tolerance | No Phase 2 authorization |
| Research viability | Candidate reduction observable stable under parameter uncertainty | At least one falsifiable error boundary remains | Reframe as benchmark/synthesis or terminate paper objective |

## Required final report

The final Phase 1 gate must list for each row:

- evidence completed;
- quantitative metric;
- pass/fail decision;
- unresolved uncertainty;
- effect on authorized Phase 2 scope.