# Stochastic transport and finite-size noise

**Last updated:** 2026-07-23  
**Program ID:** `stochastic_transport_noise`  
**Contribution:** R06  
**Controlling issues:** #341 and #343  
**Current phase:** Phase 1C — HgCdTe statistics, parameter provenance, and solver architecture

## Objective

Develop a verified one-dimensional stochastic drift-diffusion-Poisson framework for a finite HgCdTe photoconductor and quantify the error incurred when the full model is reduced to conventional quasineutral, deterministic-contact, or single-lifetime interpretations.

Target observables:

1. nonlinear steady-state carrier, field, potential, recombination, and current profiles;
2. terminal current, differential resistance, and conductance;
3. photoconductive responsivity;
4. terminal current and voltage power spectral densities;
5. dominant modal frequencies and fitted noise corners;
6. error in lifetime inferred from a terminal corner;
7. responsivity-noise-bandwidth and detectivity trade space;
8. dimensionless regime boundaries for valid reduced models.

The final observable is the terminal response under a declared external circuit. Local carrier-number and interface fluctuations are intermediate state variables.

## Revised core scientific question

Under what dimensionless conditions can a finite bipolar HgCdTe photoconductor with self-consistent electrostatics, dynamic traps, stochastic interfaces, optical generation, and a loaded terminal circuit be reduced to:

- a quasineutral ambipolar model;
- a deterministic finite surface-recombination velocity;
- a one-carrier model;
- a single-Lorentzian GR spectrum;
- a corner-frequency lifetime estimate;

without exceeding a declared error tolerance?

## Current decision

R06 remains a gated active research program.

The broad novelty premise has been rejected. Prior work already establishes finite spatial GR noise, diffusion and drift effects, Poisson correlations, dynamic traps, stochastic semiconductor interfaces, thermionic-emission contact noise, impedance-field transfer, contact-controlled HgCdTe noise, and non-Lorentzian spectra.

The program proceeds as a **controlled reduction and error-bound study**. Novelty is not claimed.

Production parameter sweeps and manuscript drafting remain unauthorized until the final Phase 1 gate is passed.

## Baseline geometry

A one-dimensional HgCdTe slab occupies

\[
0\le x\le L
\]

with uniform cross-sectional area `A` and uniform composition in the baseline model.

Initial operating scope:

- temperature near 77 K;
- applied terminal voltage or current through an explicit external circuit;
- uniform or Beer-Lambert optical generation;
- electron and hole drift-diffusion;
- Poisson electrostatics;
- one explicit two-state SRH trap family;
- stochastic bulk reactions and transport;
- stochastic ideal, interface-state, finite-exchange, or blocking-contact limits;
- small-signal frequency-domain analysis around the nonlinear steady state.

Radiative and Auger recombination remain deferred until the SRH baseline passes equilibrium and bulk-limit tests.

## Accepted sign and terminal conventions

The program uses:

\[
E=-\frac{\partial\phi}{\partial x},
\qquad q>0,
\]

with conventional current positive in `+x`.

Electron and hole current densities are

\[
J_n=q\mu_n nE+qD_n\frac{\partial n}{\partial x},
\]

\[
J_p=q\mu_p pE-qD_p\frac{\partial p}{\partial x}.
\]

Continuity equations are

\[
\frac{\partial n}{\partial t}
=\frac{1}{q}\frac{\partial J_n}{\partial x}+G-R,
\]

\[
\frac{\partial p}{\partial t}
=-\frac{1}{q}\frac{\partial J_p}{\partial x}+G-R.
\]

The conserved total current density is

\[
J_{tot}=J_n+J_p+\frac{\partial(\varepsilon E)}{\partial t}.
\]

At fixed voltage and constant area, the terminal current is the spatial average of conduction current plus any nonzero voltage-derivative displacement term. It is not generally the conduction current evaluated at an arbitrary interior point.

Internal stochastic derivations use a two-sided angular-frequency covariance. Reported detector spectra use one-sided PSD per hertz with explicit conversion.

## Deterministic baseline equations

Poisson electrostatics is

\[
\frac{\partial}{\partial x}
\left(\varepsilon\frac{\partial\phi}{\partial x}\right)
=-q\left(p-n+N_D^+-N_A^-+\frac{\rho_t}{q}\right).
\]

The reference trap model retains explicit occupancy. The algebraic SRH law is a steady reduction of four positive channels:

1. electron capture;
2. electron emission;
3. hole capture;
4. hole emission.

The net SRH residual is not a noise intensity.

## Stochastic operator architecture

The discretized linearized system will have the form

\[
(i\omega M-J)\delta u=B\xi,
\]

\[
\delta I=C\delta u+D\xi,
\]

with primitive-event covariance

\[
Q_\xi=\sum_r \nu_r\nu_r^T a_r.
\]

The terminal PSD is

\[
S_I=H_IQ_\xi H_I^\dagger.
\]

A second implementation based on an adjoint or impedance field is mandatory for selected benchmarks.

## Accepted stochastic-interface hierarchy

### Ideal exchange

For forward and reverse event activities,

\[
\bar\Gamma=a_+-a_-,
\qquad
Q_\Gamma=\frac{a_++a_-}{A_c}.
\]

This structure is source-established by Gomila and Rubí (1998).

### Nonideal interface

Interface states are represented by explicit primitive processes. Composite interface currents have cross covariance whenever they share a primitive event.

### Schottky specialization

Thermionic-emission contact noise and its thermal-to-shot crossover are established. The contact source must enter as a stochastic boundary condition.

### Deterministic finite velocity

A boundary such as

\[
\Gamma=S(c-c_{eq})
\]

is a reduced mean law. It is not a complete stochastic contact model.

The reference implementation will compare:

1. explicit ideal interface exchange;
2. explicit dynamic interface-state exchange;
3. stochastic reduced boundary after state elimination;
4. deterministic Robin boundary without interface covariance.

## Dimensionless baseline

For nondegenerate isothermal transport, define

\[
\Pi_D=\frac{L}{\sqrt{D_r\tau_r}},
\qquad
\Lambda=\frac{L}{L_{D,r}},
\qquad
U=\frac{qV_b}{k_BT}.
\]

Derived ratios include

\[
\frac{\tau_r}{t_{tr}}=\frac{U}{\Pi_D^2},
\]

and, for the unipolar reference conductivity,

\[
\frac{\tau_r}{\tau_{dr}}=\frac{\Lambda^2}{\Pi_D^2}.
\]

Additional independent controls include:

- electron/hole mobility and equilibrium-density ratios;
- left/right, electron/hole contact Biot numbers;
- thermionic-to-diffusion contact ratio;
- optical depth and injection level;
- trap density, trap energy, and nonredundant transition-rate ratios;
- generalized Einstein factors when degenerate;
- normalized external impedance.

## Completed Phase 1 work

### Literature and prior art

- full equation-level audits of Smith 1982, Smith 1984, Iverson-Smith 1985, Shockley-Read 1952, Bulashenko et al. 1998, Zocchi 2006, Gomila-Rubí 1997, Gomila-Rubí 1998, and Gomila-Bulashenko-Rubí 1998;
- literature matrix with explicit verification depth;
- source acquisition and substitution records;
- broad novelty hypothesis rejected;
- stochastic-interface novelty hypothesis rejected.

### Conventions and derivations

- sign, voltage, Fourier, PSD, and terminal-current conventions;
- event-level bulk reaction covariance;
- explicit trap-state requirement;
- contact detailed balance;
- contact Onsager-FDT relation;
- blocking and fast-reservoir singular-limit analysis;
- reduced dimensionless parameter set.

### Benchmark design

- B0-B9 benchmark ladder;
- source-derived HgCdTe and finite-size targets;
- stochastic-interface benchmarks;
- direct-versus-adjoint comparison requirement;
- equilibrium FDT and current-conservation tolerances.

## Established prior art exclusions

R06 will not claim novelty for:

- finite one-dimensional drift-diffusion noise;
- Poisson and dielectric-relaxation effects;
- dynamic trap populations;
- stochastic semiconductor-interface boundary conditions;
- thermionic-emission contact noise;
- interface-state cross covariance;
- Green-function or impedance-field transfer;
- deterministic finite contact recombination velocity;
- contact-controlled HgCdTe responsivity and GR noise;
- non-Lorentzian spatial spectra;
- apparent lifetime changes caused by transport and contacts in principle.

## Candidate contribution

A paper-level contribution remains possible only if R06 establishes a new quantitative result such as:

1. a controlled asymptotic error for eliminating dynamic interface states;
2. a dimensionless validity boundary for deterministic `S`;
3. a quantitative error boundary for quasineutral ambipolar reduction;
4. an uncertainty-robust criterion for when a terminal corner misestimates microscopic lifetime;
5. a falsifiable HgCdTe regime map separating contact, trap, screening, diffusion, drift, and circuit modes.

## Required limiting cases

The model must recover:

1. zero-bias thermal equilibrium;
2. detailed balance and zero mean terminal current;
3. Johnson-Nyquist terminal noise;
4. strong-screening quasineutrality;
5. uniform-field drift transport;
6. diffusion-dominated transport;
7. ideal reservoir and absorbing-contact limits;
8. blocking-contact behavior;
9. Smith 1982 and Smith 1984 HgCdTe limits;
10. Iverson-Smith dynamic-trap limit;
11. Gomila-Rubí ideal and interface-state stochastic boundaries;
12. Gomila-Bulashenko-Rubí Schottky thermal-shot and Nyquist limits;
13. Zocchi finite Poisson-trap spectra;
14. conventional bulk Lorentzian;
15. spatial conservation of conduction plus displacement current;
16. agreement between direct and adjoint terminal-noise methods.

## Preliminary numerical acceptance targets

| Metric | Target after convergence |
|---|---:|
| Normalized nonlinear residual | `< 1e-10` |
| Integrated carrier-continuity imbalance | `< 1e-9` |
| Spatial terminal-current variation | `< 1e-8` |
| Equilibrium FDT relative error | `< 1e-4` |
| Direct-versus-adjoint PSD discrepancy | `< 1e-5` |
| Mesh change in terminal DC observables | `< 1e-4` |
| Mesh change in terminal PSD | `< 5e-3` |
| Frequency-grid interpolation error near poles | `< 1e-3` |

These are design requirements, not completed results.

## Remaining Phase 1C work

1. Build the HgCdTe parameter and uncertainty table.
2. Classify each relation as source-established, uncertain literature input, or exploratory.
3. Decide the baseline carrier-statistics closure near 77 K.
4. Quantify the error of the nondegenerate Einstein relation over the intended composition and density range.
5. Finalize deterministic contact and external-circuit boundary hierarchy.
6. Select numerical dependencies and solver architecture.
7. Specify Phase 2 executable tests and file layout.
8. Record the final Phase 1 proceed, reframe, or terminate decision.

## Authorized next work

Authorized:

- material/statistics source audit;
- parameter uncertainty table;
- generalized Einstein validity analysis;
- deterministic solver architecture;
- small analytical prototypes that do not constitute production sweeps;
- preparation of a final Phase 1 gate.

Not authorized:

- production HgCdTe sweeps;
- predictive detector claims;
- manuscript drafting;
- claims that contact noise or dynamic traps are new;
- arbitrary fitted source terms;
- three-dimensional simulation.

## Termination criteria

Reframe R06 as a benchmark/synthesis package or terminate the paper objective if:

- reduction errors are negligible across all plausible HgCdTe regimes;
- equivalent quantitative boundaries are found in prior work;
- material uncertainty prevents a stable regime boundary;
- the one-dimensional terminal observable is structurally non-identifiable;
- equilibrium FDT cannot be recovered from one consistent event model;
- modal conclusions are not robust to discretization or parameter uncertainty.

## Manuscript status

No manuscript is authorized. The project remains a candidate theoretical work pending completion of Phase 1C and a positive Phase 2 gate.