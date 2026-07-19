# Hamiltonian statistics regeneration after the 64D correction

**Date:** 2026-07-19  
**Status:** validated statistical audit

## Question

Which committed results change when Hermitian `8x8` Hamiltonians move from the redundant 128-entry real/imaginary representation to 64 independent orthonormal real coordinates?

## Repository inventory

Eleven current analysis paths were classified.

Regenerated:

- `src/mct_research/projection.py`;
- `tests/test_hermitian_covariance_coordinates.py`.

Unaffected:

- the synthetic covariance-aware `[110]` holdout, which uses a `9x8` scalar design and `9x9` covariance;
- deterministic quadratic-invariant, Weiler-class, corrected-static, and spectral-closure analyses;
- the controlling corrected static reference record.

Out of scope:

- scalar HgCdTe temperature and composition regressions.

No committed physical static record contains calibrated Hamiltonian covariance, parameter standard errors, or reduced chi-square. No physical coefficient or residual value therefore requires replacement.

## Unweighted regeneration

Six noisy Hermitian matrices were fit with eight Kane parameters in both coordinate systems.

```text
legacy observations = 768
current observations = 384
rank                = 8
legacy dof          = 760
current dof         = 376
```

Results:

- maximum fitted-parameter difference: `1.24523e-12`;
- numeric SSE difference: `4.23516e-21`;
- current/legacy reduced-chi-square ratio: `2.0212765957`;
- current/legacy variance-scaled standard-error ratio: `1.4217160742`.

The point estimates and Frobenius residuals are unchanged because both coordinate systems are isometric on the Hermitian subspace. The statistical denominator changes because the former lower-triangle and imaginary-diagonal entries were not independent observations.

## Absolute covariance equivalence

A physical isotropic `64x64` covariance was embedded into the legacy `128x128` space. The embedded covariance has rank 64.

Using its Moore-Penrose pseudoinverse reproduces the current 64D result:

- maximum parameter difference: `6.26582e-13`;
- chi-square difference: `2.13731e-11`;
- parameter-covariance Frobenius difference: `1.62089e-11`.

Thus the physical Hermitian subspace is equivalent when handled correctly. The former practice of flooring 64 null directions was not a calibrated probability model.

## Decision

Retain:

- all deterministic static Kane coefficients;
- all deterministic matrix and spectral residuals;
- the scalar covariance-aware `[110]` protocol;
- scalar empirical-gap statistical analyses.

Supersede:

- Hamiltonian residual degrees of freedom based on `128N-p`;
- unweighted variance-scaled Hamiltonian standard errors based on that denominator;
- interpretations of regularized 128D Hamiltonian covariance as full-rank measurement covariance.

## Reproducibility

- validated head: `469f45c3bff877a8b5e943e48a37a213a11c8fa1`
- workflow run: `29667599043`
- artifact: `8436220417`
- digest: `sha256:835039da2d2bc8b7afa356315ef91e25b0a0e44d5c73a8ff6013953578429fc0`
- reference: `validation/hamiltonian_statistics_64d_reference_result.json`
- inventory: `data/evidence/hamiltonian_statistics_64d_inventory.csv`
