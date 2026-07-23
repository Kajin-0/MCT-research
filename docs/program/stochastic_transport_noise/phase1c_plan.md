# R06 Phase 1C plan: HgCdTe statistics, parameters, and solver architecture

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Status:** authorized Phase 1 planning; production simulation remains gated

## Objective

Complete the remaining work required for a defensible Phase 2 deterministic implementation:

1. select and justify the HgCdTe carrier-statistics closure;
2. populate the material and uncertainty table;
3. define deterministic bulk and contact boundary hierarchies;
4. specify the numerical discretization and nonlinear-solver architecture;
5. define executable conservation, convergence, and analytical-limit tests;
6. issue the final Phase 1 proceed, reframe, or terminate decision.

## Workstream A — composition and thermodynamics

Required relations:

- `E_g(x,T)`;
- electron and hole density of states;
- effective-mass or Kane nonparabolicity closure;
- intrinsic carrier density;
- charge neutrality and ionization;
- dielectric permittivity;
- reduced chemical potentials.

Decision required:

- Boltzmann baseline with quantified degeneracy error; or
- Fermi-Dirac/Kane baseline from the start.

The decision metric is the maximum relative error in carrier density, compressibility `partial n/partial mu`, generalized Einstein factor, Debye length, and terminal current over the intended parameter range.

## Workstream B — transport

Required inputs:

- electron and hole mobility ranges;
- field-dependence criterion;
- generalized diffusion coefficients;
- velocity-saturation or hot-carrier exclusion criterion;
- local-transport validity versus mean free path and mesh scale.

The baseline may use constant low-field mobility only if the resulting error is bounded for all benchmark fields.

## Workstream C — traps and recombination

Required inputs:

- trap density and energy ranges;
- electron and hole capture cross sections or rate coefficients;
- detailed-balance emission rates;
- equilibrium trap occupancy and charge convention;
- direct band-to-band generation/recombination baseline if retained.

The explicit four-channel trap model remains the stochastic reference.

## Workstream D — optics

Required inputs:

- absorption coefficient or controlled optical-depth sweep;
- reflection and quantum-yield assumptions;
- uniform versus Beer-Lambert generation hierarchy;
- incident photon-flux normalization.

Uniform generation is the first deterministic benchmark. Beer-Lambert generation follows only after the uniform case converges and conserves charge.

## Workstream E — contacts and external circuit

Deterministic hierarchy:

1. ideal equilibrium reservoir;
2. finite direct exchange;
3. explicit dynamic interface state;
4. blocking particle flux with electrostatic coupling;
5. Smith-type effective pair-recombination boundary;
6. asymmetric left/right contacts.

External-circuit hierarchy:

1. fixed voltage;
2. fixed current/open-circuit voltage response;
3. finite source and load impedance;
4. optional contact and parasitic capacitance.

## Workstream F — discretization

Reference deterministic method:

- conservative finite volume on a one-dimensional nonuniform mesh;
- Scharfetter-Gummel or generalized exponential fitting for carrier fluxes;
- cell-centered carrier and trap variables;
- face electric field or potential-difference formulation;
- exact event-compatible boundary fluxes;
- sparse Newton solve with continuation in bias and generation.

Independent verification method:

- second-order finite differences or a one-dimensional finite-element formulation;
- analytical eigenfunction solutions for reduced linear limits.

## Workstream G — nonlinear solver

Required features:

- equilibrium initialization;
- continuation in terminal voltage;
- continuation in optical generation;
- variable scaling and nondimensional residuals;
- damped Newton or trust-region fallback;
- sparse direct solve for initial development;
- iterative PETSc option only after the small problem is verified;
- explicit reporting of block residuals and conditioning.

## Workstream H — Phase 2 acceptance suite

Minimum deterministic tests:

1. equilibrium detailed balance;
2. zero terminal current at equal contact electrochemical potentials;
3. Poisson charge consistency;
4. spatially conserved steady conduction current;
5. uniform resistor analytical solution;
6. diffusion-only analytical solution;
7. drift-only uniform-field solution;
8. blocking and reservoir contact limits;
9. Smith 1982 absorbing-contact profile;
10. Smith 1984 finite-`S` profile;
11. mesh refinement over bulk and Debye boundary layers;
12. agreement with the independent discretization.

## Dependency strategy

Keep the base package lightweight.

Provisional optional dependencies:

- SciPy for sparse nonlinear and linear algebra;
- matplotlib and pandas for analysis only;
- h5py or NetCDF for reproducible result storage;
- PETSc/SLEPc in a separate optional environment after baseline verification.

FEniCSx is not the initial reference method because a conservative one-dimensional finite-volume implementation provides more transparent flux and stochastic-event bookkeeping. It may be used later as an independent method.

## Deliverables

1. populated parameter table with source locations and uncertainty classes;
2. statistics and generalized Einstein decision record;
3. deterministic boundary-condition specification;
4. solver architecture document;
5. Phase 2 issue and file layout;
6. final Phase 1 gate decision.

## Stop criteria

Pause before implementation if:

- no defensible low-temperature carrier-statistics closure is available;
- mobility or trap uncertainty prevents even dimensionless benchmark construction;
- one-dimensional contact parameters cannot be mapped to any falsifiable observable;
- the numerical hierarchy cannot recover the required analytical limits without incompatible assumptions.