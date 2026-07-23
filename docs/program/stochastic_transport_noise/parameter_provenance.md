# R06 material-parameter and uncertainty schema

**Program:** stochastic transport and finite-size noise  
**Controlling issue:** #339  
**Status:** Phase 1 schema; no numerical baseline authorized

## Purpose

R06 requires material and device parameters sufficient to evaluate both the nonlinear mean state and the stochastic linear response. A single convenient parameter set is not acceptable evidence. Each quantity must be associated with a physical definition, source, validity range, uncertainty class, and sensitivity role.

## Parameter classes

### Class A — established public relation

Use only when the relation is directly verified from an authoritative source and its independent variables, units, specimen conditions, and validity range match the intended calculation.

Examples may include:

- composition- and temperature-dependent band-gap relations;
- dielectric constant relations;
- equilibrium density-of-states or intrinsic-density relations;
- measured mobility parameterizations within documented ranges;
- absorption-coefficient relations for specified polarization, temperature, and composition.

Class A does not imply negligible uncertainty.

### Class B — uncertain literature parameter

Use when public sources report broad scatter, strong process dependence, incomplete metadata, or conflicting definitions.

Likely Class B quantities include:

- SRH lifetimes;
- trap density and trap energy;
- surface or contact recombination velocity;
- compensation and ionization fractions;
- low-temperature mobility in processed material;
- contact-equilibrium carrier densities;
- minority-carrier parameters in heavily compensated material.

Class B quantities require a documented range or probability model and sensitivity analysis.

### Class C — exploratory control parameter

Use for deliberate theory sweeps not intended to represent one specific specimen.

Examples:

- independent dimensionless groups used to construct regime diagrams;
- idealized blocking or infinite-recombination limits;
- hypothetical mobility ratios;
- controlled Debye-length or optical-depth sweeps.

Class C values must be labeled as exploratory and must not be presented as measured HgCdTe properties.

## Required fields

Each parameter record must contain:

| Field | Requirement |
|---|---|
| Symbol | Unique mathematical symbol |
| Code name | Stable machine-readable name |
| Definition | Physical quantity and sign convention |
| SI unit | Canonical internal unit |
| Dependency | Composition, temperature, density, field, frequency, or geometry dependence |
| Source | DOI, report ID, or derivation path |
| Verified location | Equation, page, table, figure, or section |
| Specimen context | Bulk, epitaxial, processed detector, surface, contact, or inferred |
| Validity range | Numerical and physical range supported by the source |
| Class | A, B, or C |
| Central value | Optional; never substitutes for range |
| Uncertainty representation | Bounds, distribution, covariance, or unresolved |
| Correlations | Known shared-source or physical correlations |
| Sensitivity role | Observable or regime boundary affected |
| Status | verified, provisional, conflicting, inaccessible, or rejected |

## Initial parameter inventory

The following inventory is required before Phase 2:

### Geometry and circuit

- detector length `L`;
- cross-sectional area `A`;
- applied voltage `V_b`;
- external source and load impedance;
- contact area and one-dimensional reduction assumptions.

### Composition and thermodynamics

- Cd fraction `x`;
- temperature `T`;
- band gap `E_g(x,T)`;
- electron affinity or band alignment where contact models require it;
- effective masses or nonparabolic density-of-states parameters;
- intrinsic carrier concentration `n_i`;
- degeneracy criterion and Fermi-Dirac integral implementation.

### Electrostatics

- dielectric permittivity `epsilon`;
- donor and acceptor concentrations;
- ionization fractions;
- fixed charge;
- trap charge and occupancy model;
- reference Debye length definition.

### Transport

- electron mobility `mu_n`;
- hole mobility `mu_p`;
- generalized diffusion coefficients `D_n`, `D_p`;
- field dependence and velocity-saturation model if needed;
- temperature and carrier-density dependence;
- validity of local transport at the selected length scale.

### Recombination and traps

- electron and hole SRH lifetime parameters;
- trap energy;
- trap density;
- capture cross sections or microscopic transition rates if stochastic trap dynamics are retained;
- radiative coefficient, deferred;
- Auger coefficients, deferred.

### Optical generation

- absorption coefficient `alpha(lambda,x,T)`;
- internal quantum efficiency or pair-generation yield;
- incident photon flux;
- reflection and transmission assumptions;
- optical depth `alpha L`.

### Contacts

- electron and hole surface recombination/injection velocities;
- contact-equilibrium carrier populations or electrochemical potentials;
- contact resistance or barrier parameters;
- contact capacitance if required for the terminal observable;
- temperature and bias dependence;
- contact stochastic transition rates.

### Noise and spectrum

- one-sided versus two-sided convention;
- hertz versus angular-frequency covariance normalization;
- external resistor temperature;
- primitive source covariance parameters;
- measurement loading and transfer function.

## Correlation policy

Parameters obtained from the same fitted material model must not automatically be sampled independently. Examples include:

- band gap, intrinsic density, and absorption edge;
- mobility and diffusion coefficient;
- trap lifetime, capture cross section, and trap density;
- contact recombination velocity and equilibrium injection population.

Where covariance is unavailable, compare at least:

1. independent-range sampling;
2. physically coupled sampling;
3. worst-case aligned perturbations.

The difference is part of the uncertainty result.

## Sensitivity hierarchy

Before broad stochastic simulations, classify each uncertain quantity by its expected effect on:

- steady terminal current;
- responsivity;
- dominant pole frequency;
- low-frequency PSD amplitude;
- Johnson-Nyquist recovery;
- modal separation;
- regime-map boundaries.

Use local derivatives, adjoint sensitivity, or structured finite differences only after the deterministic and linearized operators are verified. A parameter with large sensitivity and weak source support is a program risk, not an adjustable fit knob.

## Acceptance rule

Phase 2 may use a numerical parameter only when:

1. its definition and unit are unambiguous;
2. its source or exploratory status is explicit;
3. its validity range covers the calculation or the extrapolation is labeled;
4. its uncertainty representation is documented;
5. material and numerical conclusions are not conditioned silently on a single uncertain value.

## Initial table

| Symbol | Code name | Quantity | SI unit | Dependency | Class | Status | Source | Range or uncertainty | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `x` | `cd_fraction` | Cd mole fraction | 1 | specimen | A/C | unresolved | — | program range not yet fixed | Distinguish measured composition from sweep coordinate |
| `T` | `temperature` | lattice temperature | K | operating point | A/C | provisional | — | near 77 K baseline | Non-isothermal effects deferred |
| `epsilon` | `permittivity` | static dielectric permittivity | F/m | `x,T` | A/B | unresolved | — | source audit required | Frequency dependence may matter for displacement current |
| `mu_n` | `electron_mobility` | electron mobility | m^2/(V s) | `x,T,n,E` | B | unresolved | — | range required | Do not assume field independence without criterion |
| `mu_p` | `hole_mobility` | hole mobility | m^2/(V s) | `x,T,p,E` | B | unresolved | — | range required | Mobility ratio is a dimensionless control |
| `tau_n` | `srh_tau_n` | electron SRH lifetime parameter | s | trap/specimen state | B | unresolved | — | range required | Not automatically equal to measured noise lifetime |
| `tau_p` | `srh_tau_p` | hole SRH lifetime parameter | s | trap/specimen state | B | unresolved | — | range required | Requires microscopic interpretation for covariance |
| `E_t` | `trap_energy` | trap energy | J | trap family | B/C | unresolved | — | range required | Reference energy must be explicit |
| `N_t` | `trap_density` | active trap density | 1/m^3 | specimen/process | B/C | unresolved | — | range required | May require dynamic occupancy state |
| `S_n` | `contact_velocity_n` | electron contact velocity | m/s | contact,bias,T | B/C | unresolved | — | include blocking to large-velocity limits | Deterministic Robin coefficient is not full stochastic model |
| `S_p` | `contact_velocity_p` | hole contact velocity | m/s | contact,bias,T | B/C | unresolved | — | include blocking to large-velocity limits | Treat left and right contacts separately if asymmetric |
| `alpha` | `absorption_coefficient` | optical absorption coefficient | 1/m | `lambda,x,T` | A/B | unresolved | — | source audit required | Needed only for nonuniform optical generation |

This table is intentionally incomplete. Values must not be inserted without source or exploratory classification.