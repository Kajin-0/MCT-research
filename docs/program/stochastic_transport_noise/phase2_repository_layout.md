# R06 provisional Phase 2 repository layout

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Status:** planning only; limited Phase 1C prototypes exist, but Phase 2 production implementation is not yet authorized

```text
src/mct_research/transport_noise/
    __init__.py
    statistics_prototype.py          # implemented Phase 1C verification kernel
    finite_volume_prototype.py       # implemented Phase 1C unipolar residual/Jacobian
    constants.py
    scaling.py
    parameter_sets.py
    statistics.py
    material_hgcdte.py
    traps.py
    optics.py
    contacts.py
    circuit.py
    mesh_1d.py
    fluxes.py
    deterministic_residual.py
    deterministic_solver.py
    conservation.py

benchmarks/transport_noise/
    equilibrium/
    uniform_resistor/
    manufactured_solution/
    drift_diffusion/
    smith_1982/
    smith_1984/
    interface_exchange/
    schottky_contact/

 tests/transport_noise/
    test_scaling.py
    test_statistics.py
    test_trap_detailed_balance.py
    test_contact_detailed_balance.py
    test_uniform_equilibrium.py
    test_current_conservation.py
    test_diffusion_limit.py
    test_drift_limit.py
    test_manufactured_solution.py
    test_smith_1982_limit.py
    test_smith_1984_limit.py
    test_mesh_convergence.py

configs/transport_noise/
    dimensionless_unipolar_reference.toml  # implemented Phase 1C config
    equilibrium_reference.toml
    smith_1982_reference.toml
    smith_1984_reference.toml
    dimensionless_reference.toml

results/transport_noise/
    README.md
```

## Architecture rules

1. `statistics.py` owns density, chemical-potential, compressibility, and generalized Einstein calculations.
2. `material_hgcdte.py` contains only source-controlled HgCdTe relations and validity metadata.
3. `contacts.py` exposes primitive interface processes and reduced deterministic boundaries through distinct APIs.
4. `fluxes.py` contains conservative face fluxes and no global solver state.
5. `deterministic_residual.py` assembles equation blocks but does not select continuation or linear solvers.
6. `deterministic_solver.py` owns damping, continuation, convergence history, and linear-solver selection.
7. `conservation.py` computes independent balances from the converged state rather than reusing solver residuals.
8. Benchmark configurations contain source citations and convention translations.
9. Generated numerical results are not committed unless repository policy explicitly authorizes a compact benchmark artifact.
10. Prototype files remain explicitly named until their equations, sparse structure, and source interfaces pass the Phase 2 gate.

## Initial dependency boundary

The current Phase 1C prototypes require only:

- NumPy;
- pytest for tests.

The first nonlinear Phase 2 implementation may add SciPy as an optional transport-solver dependency for sparse matrices and linear solves.

Plotting, tabulation, HDF5, PETSc, and FEniCSx remain analysis or independent-verification extras.

## Current executable Phase 1C scope

Implemented:

1. normalized parabolic Fermi-integral verification;
2. Hansen-Schmit abstract-fit benchmark;
3. dimensionless steady unipolar Poisson-continuity residual;
4. Scharfetter-Gummel electron face current;
5. dense analytical Jacobian;
6. independent current-conservation metrics;
7. exact equilibrium and uniform-resistor tests.

Not implemented:

- nonlinear solver;
- sparse Jacobian;
- bipolar transport;
- source-controlled HgCdTe material model;
- traps or optics;
- circuit unknowns;
- stochastic operators.

## Next executable increment

The next code increment is limited to:

1. damped Newton iteration for the existing dimensionless unipolar kernel;
2. equilibrium and uniform-resistor convergence from perturbed initial states;
3. a manufactured nonuniform solution;
4. mesh-refinement tests;
5. sparse Jacobian representation after dense/sparse equality is verified.

Biased illumination, bipolar traps, material-accurate HgCdTe parameters, and stochastic operators remain downstream.