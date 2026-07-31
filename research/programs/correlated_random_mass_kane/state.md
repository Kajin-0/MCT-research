# Program state: correlated random-mass Kane regime

**Portfolio contribution:** R05  
**State:** gated Phase 0 specification and novelty audit; numerical oracle not yet authorized  
**Controlling issue:** #390

## Objective

Investigate whether finite-correlation-length composition disorder near the HgCdTe normal/inverted transition requires a random-mass Kane or Dirac treatment beyond scalar distributional and measurement-kernel models.

## Current status

This program is recognized as a distinct potential work, not as an automatic second stage of the spatial-disorder program.

Issue #390 now controls a bounded Phase 0 activation study. The governing protocol is:

```text
research/programs/correlated_random_mass_kane/phase0_specification.md
```

The specification authorizes only:

- repository dependency and convention audit;
- claim-level prior-art review;
- uncertainty-bounded HgCdTe parameter screening;
- controlled analytical limits;
- predeclared minimal-oracle, convergence, effect-size, experimental-resolution, and stop criteria.

No production random-mass solver, manuscript, full 8-band spatial calculation, or expensive parameter sweep is currently authorized.

## Available foundations

- homogeneous bulk 8-band Kane Hamiltonians;
- symmetry and matrix-projection infrastructure;
- distributional signed-gap diagnostics;
- spatial covariance and measurement-kernel models;
- preliminary dimensionless comparison between correlation length and a Kane mass length.

These foundations do not establish that a random-mass regime occurs in a real specimen.

## Activation gates

Before numerical implementation, require:

1. an independently supported correlation-length range near the relevant composition and temperature;
2. a clearly defined observable not already explained by scalar distributional or finite-kernel theory;
3. a claim-level prior-art audit of HgCdTe disorder, SCBA, and correlated random-mass Dirac/Kane literature;
4. a dimensionless regime showing finite correlation length can materially change the observable;
5. controlled analytical limits and a minimal numerical benchmark with a falsification criterion;
6. a predeclared matched scalar-null comparison and effect-size threshold;
7. a decision memo explaining why full Kane structure is necessary or explicitly unnecessary.

The minimal numerical oracle may proceed only after PR 1 records a `GO_MINIMAL_ORACLE` decision.

## Candidate control parameters

The Phase 0 convention uses the symmetric Dirac mapping

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

This is a regime diagnostic, not a material measurement or proof of topology. The effective `v_K` must be derived from an explicit low-energy Kane block, including basis coefficients, rather than assumed silently from `P/hbar`.

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

Under issue #390 and the Phase 0 specification, the next authorized tasks are:

1. complete the claim-level primary-source prior-art matrix;
2. audit the exact R02 low-energy velocity, basis, sign, and degeneracy mapping;
3. construct the source-quality-ranked HgCdTe parameter envelope, especially the correlation-length evidence boundary;
4. derive homogeneous, short-correlation, long-correlation, massless, large-mass, and isolated-wall limits;
5. freeze the matched scalar-null implementation, energy window, effect-size statistic, uncertainty budget, and experimental-resolution kernel;
6. issue a PR 1 decision before implementing the numerical oracle.

## Stop rule

Do not activate the program if:

- plausible correlation lengths remain unsupported or far outside the regime where finite-`xi` physics changes a measurable prediction;
- the proposed observable is already captured by scalar portfolio models;
- prior art leaves no meaningful HgCdTe or matched-null distinction;
- the correlated model converges to the scalar mixture within uncertainty;
- an apparent effect is explained by finite size, discretization, ultraviolet cutoff, numerical broadening, covariance-family choice, field normalization, or measurement convolution;
- no experimentally discriminating observable remains.

A useful analytical or numerical framework without a defensible HgCdTe physics claim should be returned as `REFRAME_AS_METHOD_BENCHMARK`, not promoted to an R05 material claim.