# Shared scientific and computational foundations

This document identifies portfolio-level infrastructure that may support multiple research works. It is a dependency map, not a claim of scientific novelty.

## Ownership rule

Shared foundations are maintained for the repository portfolio. No program or manuscript acquires exclusive ownership merely by using a module first.

Changes to a shared foundation must declare which programs are affected and must preserve existing validated behavior unless the PR explicitly documents a breaking scientific correction.

## Foundation map

### Empirical and analytical gap laws

Representative assets:

- Hansen, Laurenti, and provisional composition/temperature gap models;
- provenance-controlled historical datasets and digitizations;
- weighted fitting, cross-validation, uncertainty, and conditioning tools;
- signed-gap evaluation near the normal/inverted transition.

Primary users:

- empirical bandgap reconstruction;
- distributional band-edge observables;
- spatial-disorder propagation;
- finite-temperature Kane benchmarking.

### Distributional and observation operators

Representative modules:

```text
src/mct_research/distributional_gap.py
src/mct_research/distributional_quadrature.py
src/mct_research/spectral_convolution.py
src/mct_research/detector_cutoff.py
src/mct_research/unified_spectrum.py
```

Primary users:

- distributional band-edge observables;
- spatial-disorder measurement theory;
- future detector- and modality-specific manuscripts.

These modules do not by themselves establish a specimen distribution, a universal optical edge, or a material correlation length.

### Spatial covariance and measurement kernels

Representative modules:

```text
src/mct_research/spatial_disorder.py
src/mct_research/spatial_disorder_depth.py
src/mct_research/spatial_disorder_inference.py
src/mct_research/spatial_disorder_theorems.py
src/mct_research/spatial_disorder_optics.py
src/mct_research/spatial_disorder_cutoff.py
src/mct_research/spatial_disorder_design.py
src/mct_research/spatial_disorder_calibration.py
src/mct_research/spatial_disorder_covariance_families.py
src/mct_research/spatial_disorder_posterior.py
```

Primary users:

- measurement-kernel-aware spatial disorder;
- distributional band-edge observables;
- future mapped-detector and multiscale experimental-design studies.

The general filtering, Fisher/Schur, Matérn, reciprocal-linearity, posterior-convolution, and cumulant mathematics are established. Application-specific claims require explicit HgCdTe observables, kernels, calibration assumptions, prior support, operation order, and validation.

The calibration layer quantifies common, independent, and correlated probe-log nuisance modes without changing the existing Gaussian prediction or Fisher definitions.

The covariance-family layer adds half-integer Matérn alternatives and tests the exact Gaussian reciprocal-linearity condition. It does not identify a specimen covariance family or convert a low lack-of-fit residual into proof of Gaussian covariance.

The posterior layer propagates an independent common scale calibration through the full nonlinear relative-length posterior. Its exact factorization requires scale dependence through the ratio `s/xi` and translation-invariant or effectively broad absolute log-length support. The direct bounded-prior diagnostic must be used when that support assumption is questionable.

### Kane, symmetry, and matrix projection

Representative capabilities:

- homogeneous bulk 8-band Kane Hamiltonians;
- one-`P` and two-`P` parameter projection;
- zone-centre symmetry restoration and gauge alignment;
- matrix-valued covariance propagation and generalized least squares;
- finite-temperature matrix and reconstruction oracles.

Primary users:

- finite-temperature Kane and electronic structure;
- distributional band-edge observables;
- correlated random-mass Kane, if activated.

A validated matrix transformation is not equivalent to a converged material calculation.

### First-principles adapters and provenance

Representative capabilities:

- strict `8x8` selected-band export contracts;
- immutable `MatrixDataset` storage;
- static CdTe selected-band post-processing;
- calculation readiness and provenance ledgers.

Primary users:

- finite-temperature Kane and electronic structure;
- future parameter-validation studies.

Production AHC, SQS, CPA, SCBA, or alloy calculations require program-specific authorization.

### Literature, validation, and research workflow

Shared directories:

```text
literature/
data/validation/
docs/derivations/
benchmarks/
tools/
tests/
```

These directories support claim provenance, immutable references, analytical checks, and clean-environment validation across the entire portfolio.

## Change-impact categories

A PR touching shared foundations should classify itself as one of:

- `additive`: new API or result without changing established behavior;
- `corrective`: fixes an identified scientific or numerical defect;
- `refactor`: behavior-preserving structural change;
- `breaking`: changes definitions, conventions, or numerical outputs;
- `validation-only`: adds tests or independent reproduction;
- `documentation-only`: changes interpretation or navigation without code behavior changes.

Breaking changes require an explicit migration note for every affected program.
