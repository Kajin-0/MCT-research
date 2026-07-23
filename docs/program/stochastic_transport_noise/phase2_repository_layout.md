# R06 provisional Phase 2 repository layout

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Status:** planning only; Phase 2 implementation is not yet authorized

```text
src/mct_research/transport_noise/
    __init__.py
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
    test_smith_1982_limit.py
    test_smith_1984_limit.py
    test_mesh_convergence.py

configs/transport_noise/
    equilibrium_reference.toml
    smith_1982_reference.toml
    smith_1984_reference.toml
    dimensionless_reference.toml

results/transport_noise/
    README.md
```

## Architecture rules

1. `statistics.py` owns density, chemical-potential, compressibility, and generalized Einstein calculations.
2. `material_hgcdte.py` contains only source-controlled HgCdTe relations and their validity metadata.
3. `contacts.py` exposes primitive interface processes and reduced deterministic boundaries through distinct APIs.
4. `fluxes.py` contains conservative face fluxes and no global solver state.
5. `deterministic_residual.py` assembles equation blocks but does not select continuation or linear solvers.
6. `conservation.py` computes independent balances from the converged state rather than reusing solver residuals.
7. Benchmark configurations contain source citations and convention translations.
8. Generated numerical results are not committed unless repository policy explicitly authorizes a compact benchmark artifact.

## Initial dependency boundary

The first implementation should require only:

- NumPy;
- SciPy as an optional transport-solver dependency;
- pytest.

Plotting, tabulation, HDF5, PETSc, and FEniCSx remain analysis or independent-verification extras.

## Phase 2 first increment

The first executable increment should implement only:

1. nondimensional equilibrium statistics;
2. a uniform one-carrier resistor;
3. conservative Poisson and continuity residuals;
4. ideal equilibrium reservoir contacts;
5. current and charge conservation metrics;
6. mesh-refinement tests.

Biased illumination, bipolar traps, and stochastic operators follow only after this minimal deterministic kernel passes.