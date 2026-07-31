# Program state: correlated random-mass Kane regime

**Portfolio contribution:** R05  
**State:** Phase 0 minimal numerical oracle passed; physical screening authorized; HgCdTe physics activation blocked  
**Controlling issue:** #390

## Objective

Determine whether finite-correlation-length signed mass near the HgCdTe normal/inverted transition produces an experimentally distinguishable observable beyond scalar distributional and finite-measurement-kernel models.

## Current gate sequence

```text
PR 1: GO_MINIMAL_ORACLE_RESTRICTED
PR 2: GO_PHYSICAL_SCREENING
Final Phase 0 decision: pending PR 3
```

Governing records:

```text
research/programs/correlated_random_mass_kane/phase0_specification.md
research/decision_records/2026-07-31-r05-phase0-pr1-gate.md
research/decision_records/2026-07-31-r05-phase0-pr2-gate.md
research/programs/correlated_random_mass_kane/numerical_validation.md
```

## Scientific boundary

The broad claim that correlated random mass changes Dirac density of states is established prior art. The only potentially distinct R05 question is whether a finite-range HgCdTe/Kane mass field produces a measurable prediction that cannot be reproduced by a matched scalar local-gap mixture.

No novelty, topology, material validation, or experimental detection claim is currently authorized.

## Conventions

The minimal symmetric mapping is

```text
Eg = 2 M
sigma_E = 2 sigma_M
m = Mbar xi/(hbar v_K)
g = sigma_M xi/(hbar v_K)
kappa = g
```

The fixed-integrated-disorder short-correlation limit also uses

```text
w = W/(hbar v_K)^2
W = integral dr <delta M(0) delta M(r)>.
```

## Repository dependencies

R05 reuses, without modifying:

```text
src/mct_research/kane8.py
src/mct_research/gap_models.py
src/mct_research/distributional_gap.py
src/mct_research/distributional_quadrature.py
src/mct_research/spectral_convolution.py
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_covariance_families.py
src/mct_research/spatial_disorder_instrument.py
```

The R05-specific numerical implementation is:

```text
src/mct_research/random_mass_covariance.py
src/mct_research/random_mass_dirac.py
src/mct_research/random_mass_scalar_null.py
src/mct_research/random_mass_dos.py
tools/run_r05_phase0_oracle.py
```

## PR 1 evidence gate

Source-bounded near-transition velocity:

```text
v_K = (1.07 +/- 0.05)e6 m/s
hbar v_K = 0.7043 eV nm nominal
```

At `77 K`, the repository Hansen model gives:

```text
critical composition x_c = 0.1494464216
dEg/dx at x_c = 1.661253 eV per Cd fraction
```

Exploratory mapping at `sigma_x=0.002`:

```text
sigma_M = 1.661 meV
xi required for g=1 = 424 nm
xi required for g=0.3 = 127 nm
```

The composition-width and correlation-length values are not accepted material measurements. No qualifying near-critical HgCdTe continuum mass-correlation length has been identified.

```text
velocity gate: PASS
mean-mass tunability gate: PASS
mass-variance gate: UNRESOLVED
correlation-length gate: FAIL_NO_QUALIFYING_SOURCE
nontrivial g regime: EXPLORATORY_ONLY
```

## PR 2 minimal numerical oracle

The model is

\[
H=-i\hbar v_K\sigma_x\partial_x+M(x)\sigma_z
\]

in one dimension with Fourier-pseudospectral regularization and a scalar null using the identical one-point Gaussian mass distribution.

Primary point:

```text
m = 0
g = 0.3
L/xi = 32
a/xi = 0.125
eta_num = 0.08
32 boundary-averaged realizations
```

At the frozen experimental convolution width `delta_epsilon_exp=0.25`:

```text
Delta_1 = 0.140930
Delta_infinity = 0.419586
batch standard error = 0.005064
```

Selected zero-energy result before experimental convolution but after common numerical broadening:

```text
correlated DOS = 0.383550 +/- 0.009416
matched scalar DOS = 0.081573
```

The feature is resolution sensitive:

```text
delta_epsilon_exp    Delta_1
0.10                 0.23687
0.25                 0.14093
0.50                 0.03977
1.00                 0.004845
```

## Numerical validation status

```text
Hermiticity residual                         0.0
homogeneous eigenvalue error                 3.91e-14
paired-spectrum residual                     4.38e-15
exact scalar-null error                      4.44e-16
finite-box scalar-null discrepancy           0.003488
minimum accepted converged Delta_1            0.124598
finite-size drift                            0.019715
discretization drift                         0.010908
numerical-broadening drift                   0.022034
minimum covariance-family Delta_1            0.117198
field-conditioning drift                     0.008424
```

All predeclared PR 2 numerical gates pass.

Immutable records:

```text
data/validation/r05_phase0_reference.json
data/validation/r05_convergence_summary.json
```

## Interpretation

The synthetic oracle supports only:

1. a finite-range correlated signed mass can differ from a matched scalar mixture;
2. the declared 1D effect survives the declared numerical and covariance-family checks at `g=0.3`;
3. coherent sign-changing-wall physics is a consistent mechanism for the low-energy excess.

It does not establish:

- a bulk three-dimensional HgCdTe DOS feature;
- that a real specimen reaches `g=0.3`;
- a measured mass correlation length;
- an optical, tunneling, transport, or magneto-optical signal;
- topology, a mobility edge, percolation, or a domain-wall transport network.

## Experimental addressability

Tunneling DOS remains the cleanest conceptual scalar-null discriminator, but no qualifying near-critical HgCdTe dataset or specimen protocol has been identified.

Magneto-optics is experimentally established for massless Kane HgCdTe, but a prediction requires multiband Landau levels, optical matrix elements, heavy-hole physics, filling, and a magnetic disorder calculation. The 1D DOS oracle is insufficient.

The addressability gate remains:

```text
FAIL_NOT_YET_QUANTIFIED
```

## Full-Kane gate

```text
minimal 1D random-mass oracle: COMPLETE
full 8-band spatial disorder: NOT AUTHORIZED
quantitative optical or magneto-optical prediction: REQUIRES FULL KANE OR A VALIDATED REDUCTION
```

Full Kane is not justified merely because the synthetic effect passes. It may be reconsidered only if source-supported HgCdTe parameters overlap the effect regime and a concrete experiment can change the final decision.

## Authorized PR 3 work

PR 3 is limited to:

1. mapping the observed `g=0.3` threshold to the source-ranked HgCdTe parameter envelope;
2. calculating the associated physical energy-resolution and temperature requirements;
3. determining whether any existing or realistically specifiable experiment can distinguish the models;
4. reassessing whether full Kane has a decision-changing purpose;
5. returning exactly one final Phase 0 decision.

No additional production solver, large parameter sweep, full-Kane model, or manuscript is authorized.

## Final stop rule

Return `ACTIVATE_R05` only if a source-supported HgCdTe parameter regime, experimental-resolution path, and decision-changing next calculation all exist.

Return `TERMINATE_R05_PHYSICS_CLAIM` if the numerical distinction cannot map to a credible material regime or experiment and the method has no independent value.

Return `REFRAME_AS_METHOD_BENCHMARK` if the matched-null framework and numerical threshold are useful but no HgCdTe physical claim is supported.