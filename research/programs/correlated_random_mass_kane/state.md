# Program state: correlated random-mass Kane regime

**Portfolio contribution:** R05  
**State:** Phase 0 complete; material-physics activation denied; method benchmark retained  
**Final decision:** `REFRAME_AS_METHOD_BENCHMARK`  
**Controlling issue:** #390

## Objective

Determine whether finite-correlation-length signed mass near the HgCdTe normal/inverted transition produces an experimentally distinguishable observable beyond scalar distributional and finite-measurement-kernel models.

## Final Phase 0 sequence

```text
PR 1: GO_MINIMAL_ORACLE_RESTRICTED
PR 2: GO_PHYSICAL_SCREENING
PR 3: REFRAME_AS_METHOD_BENCHMARK
```

Governing records:

```text
research/programs/correlated_random_mass_kane/phase0_specification.md
research/programs/correlated_random_mass_kane/prior_art_matrix.md
research/programs/correlated_random_mass_kane/parameter_envelope.md
research/programs/correlated_random_mass_kane/model_conventions.md
research/programs/correlated_random_mass_kane/analytical_limits.md
research/programs/correlated_random_mass_kane/numerical_validation.md
research/programs/correlated_random_mass_kane/physical_screening.md
research/programs/correlated_random_mass_kane/experimental_observability.md
research/programs/correlated_random_mass_kane/full_kane_necessity.md
research/programs/correlated_random_mass_kane/activation_decision.md
```

Decision records:

```text
research/decision_records/2026-07-31-r05-phase0-pr1-gate.md
research/decision_records/2026-07-31-r05-phase0-pr2-gate.md
research/decision_records/2026-07-31-r05-phase0-final-decision.md
```

## Scientific boundary

The broad claim that correlation changes random-mass Dirac density of states is established prior art. R05 tested the narrower matched-null question:

\[
\rho_{\rm corr}(E)
\stackrel{?}{=}
\int dM\,P(M)\rho_{\rm hom}(E;M),
\]

with the same one-point mass distribution.

The numerical answer is no in the declared one-dimensional model. The HgCdTe material and experimental answers remain unestablished.

## Conventions

```text
Eg = 2 M
sigma_E = 2 sigma_M
m = Mbar xi/(hbar v_K)
g = sigma_M xi/(hbar v_K)
kappa = g
```

The fixed-integrated-disorder short-correlation limit additionally uses

```text
w = W/(hbar v_K)^2.
```

## Repository implementation

R05-specific code:

```text
src/mct_research/random_mass_covariance.py
src/mct_research/random_mass_dirac.py
src/mct_research/random_mass_scalar_null.py
src/mct_research/random_mass_dos.py
tools/run_r05_phase0_oracle.py
tools/run_r05_phase0_physical_screening.py
```

Immutable records:

```text
data/validation/r05_parameter_envelope.json
data/validation/r05_phase0_reference.json
data/validation/r05_convergence_summary.json
data/validation/r05_activation_decision.json
```

Shared R02, R03, and R04 scientific modules were reused but not modified.

## Numerical result

Primary converged point:

```text
m = 0
g = 0.3
L/xi = 32
a/xi = 0.125
eta_num = 0.08
Delta_1 = 0.140930 at delta_epsilon_exp = 0.25
batch standard error = 0.005064
minimum accepted converged Delta_1 = 0.124598
minimum covariance-family Delta_1 = 0.117198
```

The matched scalar null and correlated DOS differ most strongly near zero energy.

The dimensionless threshold screen gave:

```text
m = 0, g = 0.25 -> Delta_1 = 0.098739
m = 0, g = 0.30 -> Delta_1 = 0.137232
```

Thus the declared 10% threshold is bracketed by

```text
0.25 < g_threshold < 0.30
```

for this finite-box one-dimensional screen. This is not a universal critical coupling.

Mean-mass detuning suppresses the feature and requires stronger disorder.

## Numerical quality

```text
Hermiticity residual                         0.0
homogeneous maximum eigenvalue error         3.91e-14
paired-spectrum residual                     4.38e-15
exact Gaussian scalar-null error             4.44e-16
finite-box scalar-null discrepancy           0.003488
finite-size drift                            0.019715
discretization drift                         0.010908
numerical-broadening drift                   0.022034
field-conditioning drift                     0.008424
```

All predeclared numerical and covariance-family gates pass.

## HgCdTe parameter screen

Source-ranked nominal value:

```text
hbar v_K = 0.7042868 eV nm.
```

At `77 K`, the repository Hansen law gives:

```text
x_c = 0.1494464216
dEg/dx = 1.661253 eV per Cd fraction.
```

An illustrative, nonvalidated `sigma_x=0.002` linearization gives

```text
sigma_M = 1.661 meV
g = 0.25 -> xi = 106 nm
g = 0.30 -> xi = 127 nm
```

The corresponding decision-resolution scales are

```text
g = 0.25 -> delta_E = 1.661 meV
g = 0.30 -> delta_E = 1.384 meV.
```

No source establishes that `sigma_x=0.002` is a local standard deviation in the required specimen regime. No qualifying near-critical continuum electronic-mass correlation length was identified.

```text
velocity gate: PASS
mean-mass tunability gate: PASS
mass-variance gate: UNRESOLVED
correlation-length gate: FAIL_NO_QUALIFYING_SOURCE
material-overlap gate: FAIL
```

## Experimental gate

Tunneling DOS remains the cleanest conceptual discriminator, but no identified specimen or public dataset combines:

```text
independently measured local mass distribution
source-qualified xi
matched low-energy spectroscopy
sufficient energy resolution
controlled surface/contact electrostatics
```

Magneto-optics is an established HgCdTe platform, but a prediction requires full-Kane Landau levels, heavy-hole physics, optical matrix elements, filling, and magnetic disorder treatment.

```text
source-grounded experimental convolution: FAIL
discriminating experiment: FAIL
```

## Full-Kane decision

```text
DEFER_NOT_DECISION_CHANGING_WITHOUT_MATERIAL_OVERLAP
```

Full Kane is necessary for a later quantitative optical or magneto-optical prediction, but it cannot supply missing specimen covariance evidence. It is therefore not authorized now.

## Final activation gates

```text
claim-level distinction from prior work: PASS, narrowly framed
source-supported HgCdTe parameter regime: FAIL
matched correlated model differs: PASS in 1D
predeclared numerical effect threshold: PASS
numerical convergence: PASS
covariance variation: PASS
source-grounded measurement convolution: FAIL
discriminating experiment: FAIL
next full-Kane calculation decision changing: FAIL
full-Kane status explicit: PASS
```

## Final decision

```text
REFRAME_AS_METHOD_BENCHMARK
```

The R05 HgCdTe material-physics claim is not activated. The validated solver, scalar null, convergence suite, threshold screen, and physical mapping are retained to evaluate future source-qualified spatial and spectroscopic data.

## Unsupported claims

This program does not support:

- a measured HgCdTe mass correlation length;
- a specimen-specific random-mass field;
- an experimentally observed correlated-mass DOS signature;
- a topological Anderson phase;
- topology inferred from local mass sign;
- domain-wall transport or percolation;
- a mobility edge;
- a universal threshold or covariance law;
- a production full-Kane disorder calculation;
- manuscript novelty language.

## Reopening condition

R05 may be reconsidered only when new evidence provides a source-qualified near-critical spatial mass/gap covariance and a matched spectroscopic observable. Reopening must begin with the new evidence, not with a larger simulation.