# R05 Phase 0 specification: correlated random-mass Kane activation gate

**Program:** R05 — Correlated random-mass Kane regime  
**Controlling issue:** #390  
**Branch:** `agent/r05-random-mass-activation-gate`  
**Document status:** Phase 0 protocol; no physics claim or production calculation authorized  
**Permitted final decisions:** `ACTIVATE_R05`, `TERMINATE_R05_PHYSICS_CLAIM`, `REFRAME_AS_METHOD_BENCHMARK`

## 1. Decision-changing question

Determine whether finite-correlation-length signed-mass disorder near the HgCdTe normal-to-inverted transition produces an experimentally distinguishable low-energy observable beyond independent local-gap averaging.

The first candidate observable is the disorder-averaged density of states (DOS),

\[
\rho_{\mathrm{corr}}(E;\overline M,\sigma_M,\xi),
\]

for a spatially correlated mass field

\[
M(\mathbf r)=\overline M+\delta M(\mathbf r),
\qquad
\langle\delta M\rangle=0,
\]

\[
\langle\delta M(\mathbf r)\delta M(\mathbf r')\rangle
=\sigma_M^2 C(|\mathbf r-\mathbf r'|/\xi).
\]

The controlling null is an incoherent scalar mixture with the same one-point mass distribution,

\[
\rho_{\mathrm{scalar}}(E)
=\int dM\,P(M)\rho_{\mathrm{hom}}(E;M).
\]

A broadened edge, nonzero subgap DOS, or apparent gap distribution is not sufficient. The Phase 0 claim can advance only if the matched correlated model and scalar null differ after numerical convergence and plausible measurement convolution.

## 2. Authority and claim boundary

The controlling scientific authority is `research/programs/correlated_random_mass_kane/state.md`. R05 is a distinct gated program, not an automatic continuation of R03 or R04.

Phase 0 must maintain separate evidence classes:

1. source-established facts;
2. exact mathematical consequences of the declared model;
3. synthetic numerical validation;
4. HgCdTe-specific inference from source-bounded parameters;
5. experimentally established behavior;
6. speculative extensions.

The following are explicitly unsupported during Phase 0:

- a specimen-specific random-mass field or correlation length;
- topology inferred from local mass sign;
- topological Anderson phases;
- domain-wall transport or percolation;
- a mobility edge;
- a universal covariance law;
- production SCBA, 3D 8-band disorder, or large-scale phase diagrams;
- material validation from synthetic recovery.

## 3. Repository dependency map

### 3.1 R02: Kane and symmetry foundation

Primary reusable implementation:

```text
src/mct_research/kane8.py
```

Established repository conventions:

- basis order is Novik-style `Gamma6`, `Gamma8`, `Gamma7`;
- wave vector is in inverse angstrom;
- energies are in electron volts;
- Kane couplings are in electron-volt angstrom;
- the homogeneous model contains no position ordering, strain, magnetic field, or bulk-inversion-asymmetry terms;
- both one-`P` and two-`P` homogeneous Hamiltonians exist;
- time-reversal and Hermiticity checks exist.

R05 may reuse these conventions and homogeneous reference spectra. It must not insert spatially varying parameters directly into the 8-band implementation without deriving and validating operator ordering.

Relevant provenance and validation assets include the R02 state, symmetry-intertwiner tests, matrix projection tools, and material-source records. R05 must derive the minimal velocity convention from an explicit low-energy block rather than silently identifying `v_K=P/hbar` when basis factors may apply.

### 3.2 R03: signed-gap and scalar-null foundation

Primary reusable implementation:

```text
src/mct_research/gap_models.py
src/mct_research/distributional_gap.py
src/mct_research/distributional_quadrature.py
src/mct_research/spectral_convolution.py
```

Established repository conventions:

- `Eg(x,T)` is the signed zone-centre gap in eV;
- `x` is Cd mole fraction and `T` is kelvin;
- exact or controlled quadrature exists for declared scalar distributions;
- local sign probability is explicitly not a topological invariant;
- numerical or experimental resolution is represented by an observation operator, not silently absorbed into material disorder.

R05 should reuse the signed-gap functions for parameter mapping and reuse or adapt the quadrature infrastructure for the scalar null. The null must be matched to the correlated model's one-point distribution.

### 3.3 R04: covariance and measurement-kernel foundation

Primary reusable implementation:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_covariance_families.py
src/mct_research/spatial_disorder_instrument.py
src/mct_research/spatial_disorder_map_sampling.py
src/mct_research/spatial_disorder_multiscale_map.py
src/mct_research/spatial_disorder_posterior.py
```

Established reusable content:

- normalized Gaussian covariance conventions;
- half-integer Matérn families `nu = 1/2, 3/2, 5/2`;
- explicit scale and covariance-family falsification logic;
- finite measurement kernels and calibration covariance;
- strict distinction between synthetic covariance parameters and specimen measurements.

R05 may reuse covariance definitions and measurement convolution logic. Field realization code should be R05-specific only where coherent Hamiltonian propagation requires a spatial raster rather than filtered scalar moments.

### 3.4 Shared validation and provenance

Use existing repository patterns under:

```text
literature/
data/validation/
docs/derivations/
benchmarks/
tests/
tools/
research/decision_records/
```

Every immutable R05 output must include schema version, code commit, parameter convention, random seeds, units or dimensionless normalization, estimator settings, and hashes of inputs where applicable.

## 4. Governing conventions

### 4.1 Signed gap and minimal mass

The repository's homogeneous Kane convention gives the signed zone-centre gap

\[
E_g=E_{\Gamma_6}-E_{\Gamma_8}.
\]

The default minimal symmetric Dirac reduction is

\[
H=-i\hbar v_K\alpha\cdot\nabla+M(\mathbf r)\beta,
\]

with homogeneous eigenvalues

\[
E_\pm(\mathbf k)=\pm\sqrt{(\hbar v_K |\mathbf k|)^2+M^2}.
\]

Therefore the Phase 0 mapping is

\[
E_g=2M,
\qquad
M=E_g/2,
\qquad
\sigma_E=2\sigma_M.
\]

This factor-of-two convention is mandatory for the minimal model unless a later derivation explicitly replaces it. The sign of `M` follows the repository signed-gap convention.

### 4.2 Dimensionless parameters

Define

\[
m=\frac{\overline M\xi}{\hbar v_K},
\qquad
g=\frac{\sigma_M\xi}{\hbar v_K},
\qquad
\varepsilon=\frac{E\xi}{\hbar v_K}.
\]

The existing R05 diagnostic is

\[
\kappa=\frac{\xi}{\ell_K},
\qquad
\ell_K=\frac{2\hbar v_K}{\sigma_E}.
\]

Under `sigma_E = 2 sigma_M`,

\[
\ell_K=\frac{\hbar v_K}{\sigma_M},
\qquad
\kappa=g.
\]

Thus `kappa` and `g` are redundant under the declared convention. `m` remains independent and controls the mean displacement from the massless point.

### 4.3 DOS normalization

The minimal DOS is reported:

- per unit physical length in 1D;
- per two-component Dirac species;
- without spin, valley, or Kane-band degeneracy multipliers;
- in units of states per energy per length;
- with a separate dimensionless DOS where useful.

Any mapping to HgCdTe observables must add physical degeneracy only after the low-energy block is derived.

### 4.4 Numerical broadening versus measurement resolution

Two kernels must remain separate:

1. `eta_num`: numerical spectral-estimator broadening;
2. `delta_E_exp`: experimental resolution convolution.

Numerical broadening must be decreased in a convergence ladder. Experimental convolution is applied only after the underlying model comparison is numerically stable.

## 5. Phase 0 model hierarchy

### 5.1 Mandatory first oracle: 1D two-component random-mass Dirac model

Use

\[
H=-i\hbar v_K\sigma_x\partial_x+M(x)\sigma_z
\]

on a periodic interval of length `L`.

Purpose:

- validate conventions and matched-null construction;
- expose coherent effects that scalar averaging cannot represent;
- establish limiting cases and convergence behavior at low cost;
- avoid premature full-Kane implementation.

The 1D result is a benchmark, not by itself an HgCdTe material claim.

### 5.2 Preferred regularization

Use a Fourier pseudospectral derivative for the first oracle:

- periodic real-space grid of `N` points;
- spacing `a=L/N`;
- explicit ultraviolet cutoff `k_max=pi/a`;
- Hermitian kinetic operator constructed from the Fourier wave numbers;
- diagonal real mass field in position space.

This choice avoids the unacknowledged fermion doubling of a naive central-difference Dirac discretization. A local Wilson or staggered discretization may be added only as an independent regularization check.

Required checks:

- Hermiticity residual;
- particle-hole spectral symmetry for the declared model;
- exact homogeneous finite-box spectrum;
- convergence versus `a/xi`, `L/xi`, and ultraviolet cutoff;
- periodic versus antiperiodic boundary sensitivity.

### 5.3 Conditional second oracle: 2D minimal Dirac model

A 2D extension is authorized only if all are true:

- prior art leaves a plausible claim-level distinction;
- the HgCdTe parameter envelope includes a nontrivial `m,g` region;
- the 1D oracle identifies a robust non-scalar mechanism;
- the mechanism is not known to be one-dimensional only;
- the 2D calculation has a predeclared decision-changing target.

No 3D or full 8-band disorder model is authorized in Phase 0 without a separate gate.

## 6. Disorder construction

### 6.1 Primary marginal distribution

The primary comparison uses a Gaussian mass marginal,

\[
M\sim\mathcal N(\overline M,\sigma_M^2),
\]

because R03 already supports Gaussian distributional propagation and the covariance is fully specified by its two-point function for a Gaussian field.

### 6.2 Primary covariance

Use the R04-compatible normalized Gaussian covariance

\[
C_G(r/\xi)=\exp[-r^2/(2\xi^2)],
\qquad C_G(0)=1.
\]

The field generator must:

- sample the nonnegative discrete power spectrum on the periodic grid;
- enforce a real field;
- remove residual finite-box mean before adding `Mbar`;
- renormalize the realized variance only when explicitly declared;
- record both target and realized covariance statistics;
- use deterministic seeded tests.

Finite-box mean removal and per-realization variance normalization can alter long-wavelength statistics. Production comparisons must report results with and without per-realization normalization.

### 6.3 Covariance-family robustness

After the Gaussian reference passes, test R04-supported Matérn families:

```text
nu = 1/2, 3/2, 5/2
```

using a declared correlation-length parameterization. The one-point marginal must remain matched to the scalar null.

### 6.4 Additional distribution family

A non-Gaussian mass marginal is optional and only follows the primary result. It must be generated with a method that distinguishes marginal-distribution effects from covariance effects, for example a Gaussian-copula transform with documented changes to the Pearson covariance.

## 7. Scalar null model

For the 1D homogeneous Dirac model, the infinite-volume DOS per length per two-component species is

\[
\rho_{\mathrm{hom}}(E;M)
=
\frac{|E|}{\pi\hbar v_K\sqrt{E^2-M^2}}
\Theta(|E|-|M|).
\]

The massless limit is

\[
\rho_{\mathrm{hom}}(E;0)=\frac{1}{\pi\hbar v_K}
\]

away from the finite-box zero-mode convention.

The scalar mixture is evaluated using the same `P(M)` as the correlated field. Two independent implementations are required:

1. adaptive or exact-quadrature integration of the analytic homogeneous DOS followed by the declared numerical kernel;
2. Monte Carlo averaging of finite-box homogeneous spectra using the same mass samples and estimator as the correlated calculation.

The two scalar-null implementations must agree within the predeclared tolerance before the correlated comparison is accepted.

## 8. Controlled analytical limits

At minimum, derive and test the following.

### 8.1 Homogeneous limit

\[
\sigma_M\rightarrow0
\]

must recover the finite-box and infinite-volume homogeneous spectra.

### 8.2 Long-correlation semiclassical limit

For

\[
\xi\gg \ell_E,
\qquad
\ell_E=\hbar v_K/\max(|E|,\eta_{\mathrm{num}}),
\]

and away from coherent interfaces, the local-density approximation should approach the scalar mixture. Deviations must be associated with gradients, sign-changing interfaces, finite-box effects, or estimator error.

### 8.3 Short-correlation limit

The limit `xi -> 0` must declare which quantity is fixed:

- point variance `sigma_M^2`; or
- integrated disorder strength
  \(W=\int dr\,\langle\delta M(0)\delta M(r)\rangle\).

These are different limits. Both should be tested if computationally cheap.

### 8.4 Large mean mass

For

\[
|m|\gg \max(1,g),
\]

opposite-sign domains are exponentially rare for a Gaussian marginal. The correlated and scalar models should converge within uncertainty after matched broadening unless gradient corrections remain measurable.

### 8.5 Mean-massless limit

For

\[
\overline M=0,
\]

check particle-hole symmetry, finite-size zero-mode sensitivity, and whether the inferred DOS difference survives boundary-condition averaging.

### 8.6 Isolated sign-changing wall

Test one deterministic profile, such as

\[
M(x)=M_0\tanh(x/w),
\]

only as a mechanism benchmark. A localized near-zero mode in this constructed profile does not establish random-domain transport or topology in HgCdTe.

## 9. HgCdTe parameter envelope

Create `parameter_envelope.md` and a machine-readable JSON record with fields:

```text
symbol
physical_definition
lower_bound
nominal_value
upper_bound
units
temperature
composition
source
source_quality
conversion_assumptions
uncertainty_type
evidence_class
```

Required parameters:

```text
v_K
Mbar
sigma_M
xi
T
```

### 9.1 Velocity mapping

The repository homogeneous Kane coupling `P` is stored in eV angstrom. Existing source records include historical HgCdTe `P` evidence, but R05 must derive the effective `v_K` of the chosen two-band block including all basis coefficients. Do not silently use `v_K=P/hbar`.

The envelope should report both:

- source-level `P` bounds;
- derived `v_K` bounds under the declared block mapping.

### 9.2 Mean mass

Compute

\[
\overline M=E_g(x,T)/2
\]

from repository-approved signed-gap laws. Model spread among source-supported gap laws is a systematic uncertainty, not a statistical standard error.

### 9.3 Mass disorder

Where a composition fluctuation `sigma_x` is independently supported,

\[
\sigma_M\approx\frac12\left|\frac{\partial E_g}{\partial x}\right|\sigma_x
\]

is a local linearization. Curvature and non-Gaussian corrections must be quantified when `sigma_x` is not small.

### 9.4 Correlation length

No HgCdTe `xi` value is accepted without a direct source defining the measured field, specimen, temperature, spatial kernel, and covariance convention.

If no defensible range is found, use an explicitly exploratory sweep and classify the physical-regime gate as unresolved or failed. A synthetic `xi` is not evidence of a material correlation length.

### 9.5 Regime gate

Map the source-bounded envelope into

\[
(m,g)=
\left(
\frac{\overline M\xi}{\hbar v_K},
\frac{\sigma_M\xi}{\hbar v_K}
\right).
\]

The expensive-computation gate fails if all credible values lie in a trivial regime where analytical bounds already force the correlated model to the scalar null within the measurement threshold.

## 10. Prior-art gate

Create `prior_art_matrix.md` with one structured record per claim:

```text
Claim:
Closest prior result:
Hamiltonian used:
Spatial dimension:
Disorder type:
Finite correlation length included:
HgCdTe-specific:
Observable:
Analytical or numerical:
Experimental comparison:
What remains distinct:
Novelty status:
```

Allowed classifications:

```text
ESTABLISHED
INCREMENTAL_EXTENSION
POTENTIALLY_DISTINCT
UNRESOLVED
NOT_SUPPORTED
```

Search domains must include random-mass Dirac theory, correlated mass disorder, SCBA, rare regions, Lifshitz tails, domain walls, correlated-disorder mobility phenomena, HgCdTe alloy fluctuations, massless Kane fermions, DOS, tunneling, transport, and magneto-optical observables.

No numerical oracle beyond limiting-case tests proceeds unless the audit identifies a plausible distinction in at least one of:

- HgCdTe material specificity;
- finite correlation length;
- full Kane structure;
- matched comparison against scalar local-gap averaging;
- a previously untested observable or scaling regime.

## 11. Numerical estimator and convergence protocol

### 11.1 Spectral estimator

The initial oracle may use exact diagonalization for small `N` and a sparse interior eigensolver for larger `N`. If a kernel polynomial method is introduced, it requires an independent exact-diagonalization reference at overlapping sizes.

The saved output must contain raw eigenvalues or sufficient spectral moments to reproduce every plot.

### 11.2 Minimum convergence axes

Test:

- `a/xi`;
- `L/xi`;
- boundary condition;
- number of disorder realizations;
- independent seed batches;
- numerical broadening;
- energy-bin or polynomial order;
- covariance family;
- field-generation method;
- ultraviolet cutoff;
- fixed point variance versus fixed integrated disorder;
- per-realization normalization choice;
- scalar-null quadrature versus Monte Carlo implementation.

### 11.3 Error decomposition

Report separately:

- disorder-sampling standard error;
- seed-batch variation;
- finite-size drift;
- discretization and cutoff drift;
- broadening drift;
- covariance-family spread;
- scalar-null integration error.

A total uncertainty band must not conceal the separate failure modes.

## 12. Predeclared effect-size test

Before the production sweep, freeze an energy window in dimensionless units and two statistics.

Primary integrated effect:

\[
\Delta_1=
\frac{
\int_{\mathcal E}dE\,
|\rho_{\mathrm{corr}}(E)-\rho_{\mathrm{scalar}}(E)|
}{
\int_{\mathcal E}dE\,\rho_{\mathrm{scalar}}(E)+\epsilon_1
}.
\]

Secondary maximum effect:

\[
\Delta_\infty=
\max_{E\in\mathcal E}
\frac{
|\rho_{\mathrm{corr}}(E)-\rho_{\mathrm{scalar}}(E)|
}{
\rho_{\mathrm{scalar}}(E)+\epsilon_\infty
}.
\]

Provisional regularization:

```text
epsilon_1 = 1e-12 times the integrated reference weight
epsilon_infinity = 0.05 times max_E rho_scalar(E)
```

Provisional activation threshold:

```text
Delta_1 > 0.10 after experimental convolution
```

with all of:

- disorder-sampling standard error below `0.02` absolute;
- discretization and finite-size drift below `0.03` absolute;
- the sign of the effect stable across independent seed batches;
- the effect present for at least two reasonable covariance families or physically explained when family-specific;
- no scalar-null implementation discrepancy large enough to explain the effect.

The exact dimensionless energy window and experimental resolution kernel must be locked in PR 1 after the parameter and observability audits, before the production sweep.

## 13. Experimental addressability gate

Assess at least:

- tunneling DOS;
- low-energy optical conductivity or absorption-edge shape;
- Landau-level or magneto-optical broadening;
- low-temperature transport;
- spatially resolved spectroscopy where realistic.

For each candidate, record:

```text
required specimen regime
required temperature
required energy resolution
required spatial resolution
predicted correlated signal
matched scalar-null prediction
confounding mechanisms
public data availability
```

The resolution estimate must be quantitative. A feature erased by every plausible kernel does not support activation.

## 14. Full-Kane necessity gate

The 8-band model is not the default next step.

It becomes necessary only if a decision-changing prediction depends on one or more of:

- heavy-hole flat-band participation;
- split-off-band coupling;
- anisotropic or multiple Kane velocities;
- electron-hole asymmetry;
- noncommuting spatial variations of several Kane parameters;
- optical matrix elements;
- magnetic-field response;
- physical degeneracy structure.

The decision memo must state exactly which observable changes between the two-band and full-Kane descriptions. If the central non-scalar distinction is already captured by the minimal model, the full-Kane calculation remains unauthorized.

## 15. Required Phase 0 artifacts

PR 1 should create or update:

```text
research/programs/correlated_random_mass_kane/
    state.md
    phase0_specification.md
    prior_art_matrix.md
    parameter_envelope.md
    model_conventions.md
    analytical_limits.md
    experimental_observability.md
    full_kane_necessity.md
```

PR 2, only after the PR 1 gate, may add:

```text
src/mct_research/
    random_mass_dirac.py
    random_mass_covariance.py
    random_mass_dos.py
    random_mass_scalar_null.py

tests/
    test_random_mass_dirac_limits.py
    test_random_mass_covariance.py
    test_random_mass_scalar_null.py
    test_random_mass_dos_reference.py
    test_random_mass_convergence.py

data/validation/
    r05_phase0_reference.json
    r05_convergence_summary.json
```

PR 3 may add:

```text
research/programs/correlated_random_mass_kane/
    numerical_validation.md
    activation_decision.md

data/validation/
    r05_parameter_envelope.json
    r05_activation_decision.json
```

Paths may be adjusted only to follow a demonstrably cleaner existing repository convention.

## 16. Pull-request sequence and stopping rules

### PR 1 — Specification and novelty gate

Permitted:

- repository audit;
- prior-art audit;
- model and convention specification;
- parameter envelope;
- analytical derivations;
- predeclared numerical and experimental tests.

Prohibited:

- production disorder sweeps;
- full-Kane spatial implementation;
- manuscript drafting.

Stop after PR 1 if prior art leaves no meaningful distinction or the parameter envelope cannot plausibly reach a nontrivial regime.

### PR 2 — Minimal numerical oracle

Proceed only after PR 1 records a `GO_MINIMAL_ORACLE` decision. Stop if the correlated model reduces to the scalar null within uncertainty or the apparent effect is a numerical artifact.

### PR 3 — Physical screening and final decision

Proceed only after PR 2 passes analytical and convergence gates. Apply source-bounded parameters and measurement convolution, then return exactly one final decision.

## 17. Activation criteria

Return `ACTIVATE_R05` only if every condition is satisfied:

1. a claim-level distinction from prior work exists;
2. a physically plausible HgCdTe parameter regime exists;
3. the correlated model differs from a matched scalar mixture;
4. the effect exceeds the frozen threshold;
5. the effect survives numerical convergence;
6. the effect survives reasonable covariance variation;
7. the effect survives plausible measurement convolution;
8. at least one experiment can distinguish the models;
9. the next calculation has a decision-changing purpose;
10. full Kane structure is justified or explicitly unnecessary.

Return `TERMINATE_R05_PHYSICS_CLAIM` when the physical distinction, regime, robustness, or addressability gate fails.

Return `REFRAME_AS_METHOD_BENCHMARK` when the numerical or analytical machinery is useful but no new HgCdTe physical claim is supported.

## 18. Immediate next work authorized by this specification

1. complete the claim-level primary-source prior-art matrix;
2. audit the exact R02 low-energy velocity and basis-factor mapping;
3. construct the source-quality-ranked HgCdTe parameter envelope, especially `xi`;
4. derive the homogeneous, long-correlation, short-correlation, massless, and domain-wall limits;
5. freeze the effect-size window and resolution test;
6. issue a PR 1 gate decision before writing the numerical oracle.

No numerical production implementation is authorized by this document alone.