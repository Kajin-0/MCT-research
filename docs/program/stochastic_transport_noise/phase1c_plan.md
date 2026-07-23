# R06 Phase 1C plan: HgCdTe statistics, parameters, and deterministic kernel architecture

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #346  
**Status:** active Phase 1C; production simulation remains gated

## Objective

Complete the remaining material, nonlinear-solver, uncertainty, and verification gates required before a limited Phase 2 deterministic implementation can be authorized.

## Completed Phase 1C gates

### Carrier-statistics architecture

- Fermi-Dirac statistics with a source-controlled nonparabolic density of states selected as the reference architecture;
- generalized Einstein relation tied to carrier susceptibility;
- susceptibility-based screening selected;
- Boltzmann statistics retained only as a quantified reduction;
- parabolic Fermi-integral prototype and immutable reference data implemented;
- Hansen-Schmit abstract fit implemented as a benchmark only.

### Boundary and circuit architecture

- carrier-contact physics separated from terminal electrical ensemble;
- blocking, reservoir, finite exchange, dynamic interface-state, pair-recombination, Smith finite-`S`, and asymmetric contact classes defined;
- fixed-voltage, fixed-current, open-circuit, finite-load, and capacitive terminal ensembles defined.

### Deterministic numerical kernel

- dimensionless steady unipolar Poisson-continuity prototype implemented;
- logarithmic density state used for positivity;
- Scharfetter-Gummel fitted electron face current implemented;
- conservative residual implemented;
- dense analytical Jacobian implemented;
- residual-independent current-conservation metrics implemented;
- exact equilibrium, uniform-resistor, zero-field diffusion, telescoping balance, and Jacobian checks passed locally.

## Active workstream A — exact HgCdTe statistics source audit

Required:

1. Madarasz-Szmulowicz 1985 equation-quality source;
2. Lowney et al. 1992 equation-quality source;
3. exact dispersion, density-of-states, degeneracy, mass, gap, and neutrality definitions;
4. source validity and parameter provenance;
5. intrinsic-density model comparison over one declared `x,T` grid.

Fallback: retain a dimensionless nonparabolic statistics family without material-accuracy claims.

## Active workstream B — transport and electrostatic parameters

Required:

- low-field electron mobility near 77 K with specimen, doping, and compensation context;
- heavy-hole mobility range with comparable context;
- field-dependence criterion;
- generalized diffusion coefficients;
- static electrostatic permittivity relation and uncertainty;
- local-transport validity versus mean free path and mesh scale.

The baseline may use constant low-field mobility only if the resulting error is bounded for all benchmark fields.

## Active workstream C — traps and recombination

Required inputs:

- trap density and energy ranges;
- electron and hole capture cross sections or rate coefficients;
- detailed-balance emission rates;
- equilibrium trap occupancy and charge convention;
- direct band-to-band generation/recombination baseline if retained.

The explicit four-channel trap model remains the stochastic reference. No trap code enters before the deterministic bipolar block passes equilibrium and conservation tests.

## Active workstream D — optics

Required inputs:

- absorption coefficient or controlled optical-depth sweep;
- reflection and quantum-yield assumptions;
- uniform versus Beer-Lambert generation hierarchy;
- incident photon-flux normalization.

Uniform generation is the first deterministic benchmark. Beer-Lambert generation follows only after the uniform case converges and conserves charge.

## Active workstream E — contacts and external circuit

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

## Active workstream F — nonlinear deterministic solve

Next implementation steps:

1. damped Newton iteration;
2. residual and variable scaling;
3. continuation in normalized voltage and screening strength;
4. exact equilibrium and uniform-resistor convergence;
5. manufactured nonuniform solution;
6. mesh-refinement study;
7. sparse Jacobian representation preserving the verified dense derivatives.

Independent verification remains:

- second-order finite differences or a one-dimensional finite-element formulation;
- analytical solutions for reduced limits.

## Active workstream G — bipolar deterministic block specification

Before coding, fix:

- electron and hole log-density variables;
- current signs and fitted fluxes;
- Poisson charge derivatives;
- generation-recombination source placement;
- ideal-reservoir and blocking limits;
- terminal current reconstruction;
- block Jacobian sparsity.

No stochastic operator enters before this block passes equilibrium, conservation, and mesh tests.

## Active workstream H — Phase 2 acceptance suite

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
11. mesh refinement over bulk and screening boundary layers;
12. agreement with the independent discretization.

## Active workstream I — uncertainty and research viability

Demonstrate at least one reduction-error boundary that remains stable under credible uncertainty in:

- carrier statistics;
- gap and intrinsic density;
- mobility ratio;
- permittivity and screening;
- contact controls;
- trap parameters where used.

Failure to obtain a stable boundary triggers reframe to a benchmark/synthesis package or termination of the paper objective.

## Dependency strategy

Keep the base package lightweight.

Current prototype dependencies:

- NumPy;
- pytest for tests.

Potential Phase 2 optional dependencies:

- SciPy for sparse nonlinear and linear algebra;
- matplotlib and pandas for analysis only;
- h5py or NetCDF for compact reproducible result storage;
- PETSc/SLEPc in a separate optional environment after baseline verification.

FEniCSx is not the initial reference method because a conservative one-dimensional finite-volume implementation provides more transparent flux and stochastic-event bookkeeping. It may be used later as an independent method.

## Next executable increment

The next code increment is limited to a damped Newton solver and manufactured-solution tests for the existing dimensionless unipolar kernel.

It must not add:

- source-unsupported HgCdTe material parameters;
- holes or traps before the block specification is approved;
- stochastic operators;
- production parameter sweeps.

## Phase 1 completion criteria

A final proceed/reframe/terminate record requires:

1. statistics model decision with source and error evidence;
2. mobility and permittivity bounds or explicit exploratory classification;
3. nonlinear deterministic convergence and mesh evidence;
4. bipolar block specification;
5. executable Phase 2 test plan;
6. at least one uncertainty-robust candidate reduction observable;
7. explicit authorized and prohibited Phase 2 scope.

## Stop criteria

Pause or reframe if:

- no defensible low-temperature carrier-statistics closure is available;
- mobility or trap uncertainty prevents even dimensionless benchmark construction;
- one-dimensional contact parameters cannot be mapped to any falsifiable observable;
- the numerical hierarchy cannot recover the required analytical limits without incompatible assumptions;
- no candidate reduction boundary survives credible material uncertainty.