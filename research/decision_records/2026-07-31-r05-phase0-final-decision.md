# R05 Phase 0 final decision

**Date:** 2026-07-31  
**Program:** R05 — Correlated random-mass Kane regime  
**Controlling issue:** #390  
**Final decision:** `REFRAME_AS_METHOD_BENCHMARK`

## What was tested

The complete Phase 0 sequence tested:

1. repository and claim boundaries across R02, R03, R04, and R05;
2. claim-level prior art for random-mass Dirac and HgCdTe disorder physics;
3. signed-gap, mass, velocity, covariance, unit, and DOS conventions;
4. a source-quality-ranked HgCdTe parameter envelope;
5. exact homogeneous and scalar-null references;
6. a deterministic one-dimensional finite-range random-mass Dirac oracle;
7. finite-size, discretization, boundary, seed, broadening, covariance, and field-conditioning robustness;
8. a dimensionless `m,g` physical-screening sweep;
9. experimental-resolution and full-Kane necessity gates.

## Why it was tested

The central question was whether coherent finite-correlation-length signed mass produces a stable prediction beyond independent local-gap averaging and whether that prediction is sufficiently grounded to justify an HgCdTe research program.

## Assumptions

The successful numerical result is conditioned on:

```text
one spatial dimension
two-component symmetric Dirac Hamiltonian
M = Eg/2
constant v_K
Gaussian primary marginal
finite-range Gaussian/Matérn covariance
DOS observable
frozen dimensionless resolution width 0.25
```

## Evidence

The primary numerical point passed:

```text
m = 0
g = 0.3
Delta_1 = 0.140930
batch SE = 0.005064
minimum converged Delta_1 = 0.124598
minimum covariance-family Delta_1 = 0.117198
```

A higher-sampling screen bracketed the near-massless 10% threshold:

```text
g = 0.25 -> Delta_1 = 0.098739
g = 0.30 -> Delta_1 = 0.137232
```

The effect weakened with mean-mass detuning and required stronger disorder.

## Failed activation gates

```text
source-supported HgCdTe parameter regime: FAIL
source-grounded experimental convolution: FAIL
discriminating experiment: FAIL
decision-changing full-Kane calculation: FAIL
```

No source-qualified near-critical HgCdTe continuum mass-correlation length was identified. The local mass variance is also unresolved. The synthetic convolution cannot be relabeled as an instrument model for an unspecified specimen.

## Remaining uncertainty

The numerical mechanism is credible within the declared model. The dominant uncertainty is the model-to-material mapping:

- three-dimensional geometry;
- heavy-hole and multiband structure;
- correlated variation of parameters beyond the gap;
- specimen-specific mass distribution and covariance;
- experimental linewidth and confounders.

## Claims supported

```text
A controlled finite-range 1D signed-mass model can differ from a matched scalar mixture.
The difference survives the declared numerical tests near the massless mean.
The repository now contains a reusable matched-null threshold benchmark.
```

## Claims not supported

```text
A real HgCdTe specimen reaches the required regime.
The predicted low-energy DOS has been measured.
The effect is a topological phase or universal law.
A full Kane production calculation is currently justified.
```

## Final decision

```text
REFRAME_AS_METHOD_BENCHMARK
```

The R05 HgCdTe physics claim is not activated. The code and analytical framework are retained to screen future source-qualified spatial and spectroscopic data.