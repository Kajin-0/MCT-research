# Program state: correlated random-mass Kane regime

**Portfolio contribution:** R05  
**State:** Phase 0 PR 1 gate passed for a restricted minimal oracle; HgCdTe physics activation blocked  
**Controlling issue:** #390

## Objective

Investigate whether finite-correlation-length composition disorder near the HgCdTe normal/inverted transition requires a random-mass Kane or Dirac treatment beyond scalar distributional and measurement-kernel models.

## Current status

This program is recognized as a distinct potential work, not as an automatic second stage of the spatial-disorder program.

Issue #390 controls a bounded Phase 0 activation study. The governing protocol is:

```text
research/programs/correlated_random_mass_kane/phase0_specification.md
```

PR 1 completed the repository dependency audit, claim-level prior-art boundary, model conventions, source-quality-ranked parameter envelope, analytical limits, experimental-addressability screen, and full-Kane necessity gate.

The controlling PR 1 decision is:

```text
GO_MINIMAL_ORACLE_RESTRICTED
```

recorded in:

```text
research/decision_records/2026-07-31-r05-phase0-pr1-gate.md
```

This authorizes only a low-cost one-dimensional two-component random-mass Dirac mechanism and threshold benchmark. It does not authorize a quantitative bulk HgCdTe prediction, full 8-band spatial disorder, production SCBA, manuscript drafting, or a large parameter sweep.

## Available foundations

- homogeneous bulk 8-band Kane Hamiltonians;
- symmetry and matrix-projection infrastructure;
- distributional signed-gap diagnostics;
- spatial covariance and measurement-kernel models;
- exact scalar-null and homogeneous analytical references defined for PR 2.

These foundations do not establish that a random-mass regime occurs in a real specimen.

## PR 1 gate results

### Prior art

```text
correlation-dependent random-mass Dirac DOS: ESTABLISHED
HgCdTe disorder-renormalized Kane DOS under uncorrelated SCBA: ESTABLISHED
finite-range HgCdTe matched scalar-null comparison: POTENTIALLY_DISTINCT
broad novelty claim: NOT SUPPORTED
```

### Parameter envelope

```text
v_K = (1.07 +/- 0.05)e6 m/s
hbar v_K = 0.7043 eV nm nominal
```

At `77 K`, the repository Hansen model gives:

```text
critical composition x_c = 0.1494464216
dEg/dx at x_c = 1.661253 eV per Cd fraction
```

Under the exploratory mapping `sigma_x = 0.002`:

```text
sigma_M = 1.661 meV
xi required for g = 1: 424 nm
```

No qualifying near-critical HgCdTe continuum mass-correlation length was identified.

```text
velocity gate: PASS
mean-mass tunability gate: PASS
mass-variance gate: UNRESOLVED
correlation-length gate: FAIL_NO_QUALIFYING_SOURCE
nontrivial g regime: EXPLORATORY_ONLY
HgCdTe physics activation: BLOCKED
```

### Experimental addressability

Tunneling DOS is potentially discriminating because the smooth scalar null vanishes linearly at zero energy. Magneto-optics is the most established HgCdTe platform but requires magnetic full-Kane response. No public near-critical dataset was identified with both a calibrated spatial covariance length and a low-energy spectral observable.

The experimental-addressability gate remains:

```text
FAIL_NOT_YET_QUANTIFIED
```

## Candidate control parameters

The Phase 0 convention uses

```text
Eg = 2 M,
sigma_E = 2 sigma_M.
```

Define

```text
m = Mbar xi / (hbar v_K),
g = sigma_M xi / (hbar v_K).
```

The earlier diagnostic is

```text
kappa = xi / ell_K,
ell_K = 2 hbar v_K / sigma_E.
```

Under the declared factor-of-two convention,

```text
kappa = g.
```

The fixed-integrated-disorder short-correlation limit also requires

```text
w = W / (hbar v_K)^2,
W = integral dr <delta M(0) delta M(r)>.
```

This is a regime diagnostic, not a material measurement or proof of topology. The effective `v_K` for a later multiband reduction must be derived from an explicit low-energy Kane block, including basis coefficients, rather than assumed silently from `P/hbar`.

## Restricted PR 2 authorization

The authorized oracle is:

```text
one spatial dimension
two-component symmetric Dirac Hamiltonian
Fourier pseudospectral regularization
Gaussian primary marginal and covariance
matched analytic and finite-box scalar nulls
periodic and antiperiodic boundaries
explicit convergence and experimental convolution
```

Frozen primary parameter grid:

```text
m = [0.0, 0.5, 1.0, 2.0, 3.0]
g = [0.1, 0.3, 0.6, 1.0, 1.5, 2.0]
L/xi = [32, 64, 128]
a/xi = [1/8, 1/12, 1/16]
```

Frozen primary energy window:

```text
|epsilon| <= 1
epsilon = E xi / (hbar v_K)
```

The numerical effect passes only if the minimum converged integrated effect across accepted variants exceeds `0.10` after dimensionless experimental Gaussian convolution width `0.25`.

## Full-Kane gate

```text
minimal random-mass Dirac oracle: AUTHORIZED
full 8-band spatial disorder: NOT AUTHORIZED
quantitative optical or magneto-optical prediction: REQUIRES FULL KANE OR A VALIDATED REDUCTION
```

Full Kane may be reconsidered only if the minimal effect, material-overlap, and experimental-addressability gates pass.

## Unsupported claims

This program does not currently support:

- a specimen-specific random-mass field;
- a measured HgCdTe alloy correlation length;
- a topological Anderson phase in HgCdTe;
- domain-wall transport or percolation claims;
- interpreting local gap-sign probability as a bulk invariant;
- production SCBA, tight-binding, or large-scale Kane calculations;
- a manuscript claim based only on generic random-mass literature;
- material validation from synthetic numerical recovery.

## Shared dependencies

The program uses Kane, symmetry, distributional-gap, spatial-covariance, measurement-kernel, literature, and immutable-validation infrastructure shared with R02, R03, and R04.

The current dependency map identifies at minimum:

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

Shared modules must not be modified merely to simplify R05. Any shared-foundation change requires explicit cross-program impact and preservation tests.

## Authorized next work

1. implement the restricted minimal oracle and matched scalar null;
2. validate homogeneous, exact scalar-null, domain-wall, short-correlation, and LDA limits;
3. run the predeclared convergence and covariance-family tests;
4. produce immutable synthetic references and a PR 2 decision;
5. proceed to physical screening only if the convolved numerical effect exceeds the frozen threshold.

## Stop rule

Do not activate the program if:

- plausible correlation lengths remain unsupported or far outside the regime where finite-`xi` physics changes a measurable prediction;
- the proposed observable is already captured by scalar portfolio models;
- prior art leaves no meaningful HgCdTe or matched-null distinction;
- the correlated model converges to the scalar mixture within uncertainty;
- an apparent effect is explained by finite size, discretization, ultraviolet cutoff, numerical broadening, covariance-family choice, field normalization, or measurement convolution;
- no experimentally discriminating observable remains.

A useful analytical or numerical framework without a defensible HgCdTe physics claim should be returned as `REFRAME_AS_METHOD_BENCHMARK`, not promoted to an R05 material claim.