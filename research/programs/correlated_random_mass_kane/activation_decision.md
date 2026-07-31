# R05 Phase 0 activation decision

**Controlling issue:** #390  
**Decision date:** 2026-07-31  
**Final decision:** `REFRAME_AS_METHOD_BENCHMARK`

## Decision statement

Finite-correlation-length signed-mass disorder produces a reproducible non-scalar low-energy DOS signature in the declared one-dimensional random-mass Dirac benchmark. The result survives the predeclared numerical, covariance-family, boundary, sampling, and synthetic-resolution tests near the mean-massless regime.

The work does not establish an HgCdTe physical claim because no source-qualified near-critical electronic-mass correlation length or local mass-variance distribution was identified, no experiment-specific matched scalar null and resolution kernel is available, and a full-Kane calculation would not currently change that evidentiary failure.

The solver, analytical references, immutable outputs, and threshold mapping are therefore retained as a method benchmark rather than activated as a material-physics program.

## Direct answer to the Phase 0 question

> Does finite-correlation-length signed-mass disorder produce an HgCdTe-relevant, experimentally distinguishable physical prediction beyond independent local-gap averaging?

```text
Model-level answer: yes, in the controlled one-dimensional benchmark.
HgCdTe material answer: not established.
Experimental answer: not established.
Program decision: REFRAME_AS_METHOD_BENCHMARK.
```

## Evidence supporting the model-level answer

Primary converged point:

```text
m = 0
g = 0.3
Delta_1 = 0.140930 at delta_epsilon_exp = 0.25
batch standard error = 0.005064
minimum accepted converged Delta_1 = 0.124598
minimum covariance-family Delta_1 = 0.117198
```

The physical-screening sweep brackets the 10% synthetic threshold near the massless mean:

```text
g = 0.25 -> Delta_1 = 0.098739
g = 0.30 -> Delta_1 = 0.137232
```

Detuning the mean mass suppresses the result:

```text
m = 0.5, g = 0.3 -> Delta_1 = 0.078991
m = 0.5, g = 0.6 -> Delta_1 = 0.216752
m = 1.0, g = 0.3 -> Delta_1 = 0.081781
m = 1.0, g = 0.6 -> Delta_1 = 0.100829 with SE = 0.030411
m = 1.0, g = 1.0 -> Delta_1 = 0.358560
```

The signature is therefore concentrated near the mean-massless regime unless disorder is strong.

## Numerical evidence quality

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

All declared PR 2 numerical gates passed.

## Negative results controlling the final decision

### 1. HgCdTe parameter overlap is unsupported

Using the source-ranked nominal

```text
hbar v_K = 0.7042868 eV nm,
```

the threshold bracket requires

\[
\xi=\frac{g\hbar v_K}{\sigma_M}.
\]

For an illustrative, nonvalidated `sigma_x=0.002` linearization at `77 K`:

```text
sigma_M = 1.661 meV
g = 0.25 -> xi = 106 nm
g = 0.30 -> xi = 127 nm
```

No source establishes that this `sigma_x` is a local standard deviation or that near-critical HgCdTe has an electronic-mass correlation length in this range.

The historical approximately `+/-0.002` composition-homogeneity statement is not a probability distribution, not a local covariance measurement, and not from the required near-critical specimen regime.

### 2. Experimental-resolution overlap is unsupported

For the same illustrative row, the frozen decision convolution maps to

```text
g = 0.25 -> delta_E = 1.661 meV
g = 0.30 -> delta_E = 1.384 meV
```

A tunneling thermal width of order `3.5 k_B T` would require temperatures below approximately `5.5 K` and `4.6 K`, respectively, before accounting for modulation, contact, lifetime, electrostatic, and background broadening.

No identified dataset combines that resolution with an independently measured mass marginal and correlation length in the same near-critical HgCdTe specimen.

### 3. The minimal oracle is not a bulk Kane prediction

The one-dimensional model omits:

```text
heavy-hole flat-band DOS
split-off-band coupling
electron-hole asymmetry
three-dimensional domain geometry
multiple Kane velocities and disorder vertices
optical matrix elements
Landau quantization
carrier filling
```

The successful mechanism benchmark cannot be interpreted as the bulk HgCdTe DOS without additional work.

### 4. Full Kane is not presently decision changing

A full-Kane disorder calculation could change a quantitative optical or magneto-optical prediction, but it cannot supply missing specimen covariance evidence. Starting it now would add substantial operator-ordering, multiband-disorder, cutoff, and validation complexity without changing the activation decision.

Decision:

```text
DEFER_NOT_DECISION_CHANGING_WITHOUT_MATERIAL_OVERLAP
```

## Activation-gate disposition

| Gate | Result | Consequence |
|---|---|---|
| claim-level distinction from prior work | pass, narrow | retain method question |
| physically plausible source-supported HgCdTe regime | fail | blocks physics activation |
| correlated versus matched scalar difference | pass in 1D | retain benchmark |
| predeclared numerical effect threshold | pass | permits physical screening only |
| numerical convergence | pass | numerical result accepted |
| covariance variation | pass | not covariance-family artifact |
| plausible source-grounded measurement convolution | fail | blocks experimental claim |
| discriminating experimental observable | fail | blocks activation |
| decision-changing next calculation | fail | full Kane deferred |
| full-Kane necessity status | explicit | governance gate satisfied |

## Why this is not `ACTIVATE_R05`

Activation requires every gate to pass. Four decisive gates fail:

```text
source_supported_hgcdte_parameter_regime
survives_source_grounded_experimental_convolution
experiment_can_distinguish_models
next_full_kane_calculation_is_decision_changing
```

## Why this is not `TERMINATE_R05_PHYSICS_CLAIM`

The broad HgCdTe physics claim is not supported, but the work produced a useful and validated framework:

- exact matched scalar-null references;
- deterministic finite-range covariance generators;
- a Fourier random-mass Dirac oracle;
- domain-wall and limiting-case validation;
- a predeclared effect metric and resolution test;
- a dimensionless threshold bracket;
- a transparent map from future measured `(sigma_M, xi)` values to experimental requirements.

This framework can evaluate future data without presuming the effect exists.

## Authorized future use

R05 remains inactive as a material-physics claim. The benchmark may be reopened only when new evidence supplies at least one of:

1. a near-critical HgCdTe composition or band-edge map with calibrated spatial kernel and identifiable `xi`;
2. an independently measured local mass/gap distribution in the same specimen;
3. low-temperature tunneling or spatial spectroscopy with a matched scalar null and sufficient energy resolution;
4. a magneto-optical dataset for which a multiband correlated-disorder calculation has a specific decision-changing prediction.

A reopening must begin with the new evidence, not with a larger simulation.

## Final standard

```text
REFRAME_AS_METHOD_BENCHMARK
```

The defensible result is a validated method and a negative HgCdTe activation decision, not a new material law.