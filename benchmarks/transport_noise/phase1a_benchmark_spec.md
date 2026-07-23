# R06 Phase 1A benchmark specification

**Program:** stochastic transport and finite-size noise  
**Contribution:** R06  
**Controlling issue:** #341  
**Status:** benchmark design only; implementation remains unauthorized until the Phase 2 gate

## 1. Purpose

R06 requires a benchmark ladder in which each additional physical mechanism is activated only after a simpler limit is recovered. The solver must not be validated solely by nonlinear convergence or by reproducing its own synthetic data.

The proposed sequence separates:

- conservation and spectral normalization;
- finite-size diffusion and screening;
- dynamic traps;
- bipolar source correlations;
- terminal transfer methods;
- finite-contact exchange;
- HgCdTe-specific material specialization.

## 2. Common numerical metrics

The following preliminary tolerances apply after mesh and frequency convergence. They are acceptance targets, not claims that every numerical method can reach them at every singular limit.

| Metric | Symbol | Preliminary target |
|---|---:|---:|
| Nonlinear residual, normalized infinity norm | `epsilon_F` | `< 1e-10` |
| Integrated electron continuity imbalance | `epsilon_n` | `< 1e-9` |
| Integrated hole continuity imbalance | `epsilon_p` | `< 1e-9` |
| Spatial terminal-current variation | `epsilon_I` | `< 1e-8` |
| Equilibrium FDT relative error | `epsilon_FDT` | `< 1e-4` after convergence |
| Direct-versus-adjoint terminal PSD discrepancy | `epsilon_adj` | `< 1e-5` |
| Mesh refinement change in terminal DC observables | `epsilon_mesh,DC` | `< 1e-4` |
| Mesh refinement change in terminal PSD | `epsilon_mesh,PSD` | `< 5e-3` over accepted band |
| Frequency-grid interpolation error near poles | `epsilon_omega` | `< 1e-3` |
| Bulk-GR limiting-spectrum discrepancy | `epsilon_GR` | `< 1e-3` |

Each reported tolerance must include the normalization used and the frequency range over which it is evaluated.

## 3. B0 — algebraic and convention tests

### Objective

Verify sign conventions, Fourier transforms, one-/two-sided PSD conversion, and dimensional reconstruction without solving a semiconductor device.

### Tests

1. Exponential mode `u(t)=exp(-t/tau)` maps to the pole `1/(1+i omega tau)` under the selected transform.
2. A real stationary process has Hermitian two-sided spectral covariance.
3. One-sided per-hertz variance equals the integrated two-sided angular-frequency variance after the declared factor-of-two and `2 pi` conversions.
4. Dimensional reconstruction of every nondimensional equation recovers the SI equation.

### Failure implication

No field solver work proceeds if B0 fails.

## 4. B1 — equilibrium homogeneous resistor

### Objective

Recover zero mean current and terminal Johnson-Nyquist noise in a spatially uniform equilibrium conductor.

### Physics

- zero applied bias;
- uniform equilibrium carrier densities;
- no optical generation;
- thermodynamically balanced bulk and contact processes;
- finite external circuit selected so the terminal observable is not identically constrained.

### Required outputs

\[
S_V^{(1)}(f)=4k_BT\operatorname{Re}Z(f),
\]

or

\[
S_I^{(1)}(f)=4k_BT\operatorname{Re}Y(f).
\]

### Diagnostic decomposition

Report separate contributions from:

- bulk transport events;
- bulk reaction events;
- contact exchange;
- external resistor/source;
- cross correlations.

The sum, not each component separately, must satisfy FDT.

## 5. B2 — Gomila-Reggiani finite-size unipolar benchmark

### Source

G. Gomila and L. Reggiani, 2002, DOI `10.1063/1.1526915`.

### Objective

Recover the established finite-size correction caused by diffusion and Coulomb correlation in a one-dimensional uniformly doped resistor.

### Reduction

- unipolar electron transport;
- nondegenerate statistics;
- one trap level;
- ideal ohmic carrier boundary conditions;
- voltage-driven terminal current;
- constant coefficients;
- no optical generation.

### Sweep

- length relative to diffusion length;
- length relative to Debye length;
- normalized applied voltage;
- normalized frequency.

### Acceptance

Reproduce published limiting trends and selected analytical formulas before adding bipolar or HgCdTe-specific physics.

## 6. B3 — Iverson-Smith strong-screening dynamic-trap benchmark

### Source

A. Evan Iverson and D. L. Smith, 1985, DOI `10.1063/1.335666`.

### Objective

Recover the structural modal content of a quasineutral HgCdTe photoconductor with explicit deep-level population dynamics.

### Reduction

- strong-screening/quasineutral limit;
- low-level n-type excitation;
- one two-state deep level;
- ohmic contacts;
- ambipolar drift and diffusion;
- field-dependent sweepout;
- direct band-to-band and trap exchange source families.

### Required comparison

- number and position of dominant poles;
- separate band-to-band, photon-generation, and trap-exchange contributions;
- trend of mobility/diffusion reduction with trap population;
- trend of corner frequency with sweepout and trap density.

### Novelty protection

R06 may not claim dynamic traps or trap-generated HgCdTe noise as new after this benchmark is established.

## 7. B4 — Bonani-Ghione source-reduction benchmark

### Source

F. Bonani and G. Ghione, 1999, DOI `10.1016/S0038-1101(98)00253-6`.

### Objective

Quantify error introduced by replacing fundamental bipolar population sources with equivalent-current or monopolar sources.

### Compared models

1. full electron-hole-trap population sources;
2. bipolar equivalent-current representation;
3. monopolar equivalent-current representation.

### Independent variables

- length relative to minority diffusion length;
- normalized electric field;
- contact proximity;
- frequency;
- majority/minority density ratio.

### Output

Define

\[
\epsilon_{\mathrm{red}}(f)
=
\frac{|S_{\mathrm{reduced}}(f)-S_{\mathrm{population}}(f)|}
{S_{\mathrm{population}}(f)}.
\]

A later regime map may use a threshold such as `epsilon_red = 0.1`, but that threshold must be declared as an engineering tolerance rather than a physical singularity.

## 8. B5 — Bulashenko direct-versus-adjoint benchmark

### Source

O. M. Bulashenko et al., 1998, DOI `10.1063/1.367023`.

### Objective

Verify that direct stochastic resolvent propagation and an adjoint/impedance-field method produce the same terminal spectrum in an inhomogeneous drift-diffusion structure.

### Required methods

1. Direct covariance propagation:

\[
S_y=C(i\omega M-J)^{-1}Q(-i\omega M^T-J^T)^{-1}C^T.
\]

2. Adjoint propagation using the terminal weighting field.

### Acceptance

The two methods must agree within `epsilon_adj` after discretization and solver tolerances are separated.

### Local-noise interpretation

Report primitive source intensity, adjoint weighting, weighted diagonal contribution, and cross-correlation contribution separately.

## 9. B6 — finite stochastic contact benchmark

### Sources

- C. H. Park, 2022, DOI `10.1063/5.0111954`;
- D. L. Smith, 1984, DOI `10.1063/1.334155`.

### Status

Exact equations remain pending full-text acquisition.

### Objective

Construct a contact model with forward and reverse exchange propensities that:

1. gives the desired mean finite-recombination boundary;
2. satisfies equilibrium detailed balance;
3. recovers finite equilibrium contact fluctuations;
4. tends continuously to blocking and reservoir limits;
5. does not double count bulk transport noise.

### Required limits

- `Bi -> 0`: blocking flux and vanishing exchange-event rate when physically appropriate;
- `Bi -> infinity`: reservoir-pinned population with the correct fluctuation ensemble;
- equilibrium: zero mean contact flux but nonzero forward-plus-reverse event intensity;
- asymmetric contacts: spatially conserved terminal current remains exact.

### Gate

No final contact covariance is accepted until Park and Smith are audited at equation level.

## 10. B7 — conventional bulk Lorentzian

### Objective

Recover the conventional lumped GR model only after spatial and contact limits are taken explicitly.

A single-mode benchmark has the form

\[
S_I(f)=\frac{S_I(0)}{1+(2\pi f\tau)^2}.
\]

### Required limiting procedure

Document which assumptions suppress higher modes:

- uniform steady state;
- quasi-neutrality or fast dielectric relaxation;
- device dimensions large or small relative to relevant diffusion lengths as appropriate;
- negligible contact influence in the terminal transfer function;
- one dominant reaction eigenvalue;
- weak external-circuit distortion.

### Output

The benchmark must identify the computed modal eigenvalue that becomes `1/tau`; it cannot infer `tau` only by fitting a Lorentzian.

## 11. B8 — finite-mode apparent spectral slope

### Objective

Test whether a finite number of transport-recombination modes can produce an apparent power-law interval.

For

\[
S(f)=\sum_{m=1}^{M}\frac{A_m}{1+(f/f_m)^2},
\]

define the local slope

\[
\alpha_{\mathrm{eff}}(f)
=-\frac{d\log S}{d\log f}.
\]

### Acceptance rule

An apparent `1/f^alpha` interval is reported only if:

- `alpha_eff` stays within a declared tolerance over at least one full decade;
- the result is stable to mesh and modal truncation;
- no broad trap-time distribution, surface shunt, or external-circuit pole was inserted implicitly;
- the finite-mode construction and its bandwidth are stated.

This benchmark can produce a proof or counterexample without claiming universal `1/f` noise.

## 12. B9 — HgCdTe parameter sensitivity benchmark

### Objective

Determine whether uncertain public HgCdTe parameters permit falsifiable regime boundaries.

### Inputs

- mobility ratio and generalized Einstein factors;
- dielectric constant;
- equilibrium density and compensation;
- trap density, energy, and capture rates;
- passivated-surface versus metal-contact exchange velocities;
- absorption depth;
- external circuit.

### Outputs

For every proposed regime boundary, report:

- local sensitivity;
- uncertainty interval;
- parameter correlation assumptions;
- whether classification changes within the plausible range.

A regime boundary that moves across the full plot under plausible parameter uncertainty is not quantitatively predictive.

## 13. Phase 2 authorization criterion

A positive Phase 2 gate requires:

1. B0 fully specified;
2. full-text equations for B2 through B6 sufficient to implement independent benchmarks;
3. primitive source covariance fixed without double counting;
4. finite-contact equilibrium closure accepted;
5. reduced dimensionless set accepted;
6. numerical methods selected for direct and adjoint solutions;
7. uncertainty ranges adequate to define at least one falsifiable HgCdTe regime boundary.

Until then, this file is a design specification, not evidence that any benchmark has passed.