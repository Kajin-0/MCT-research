# Program state: correlated random-mass Kane regime

**Portfolio contribution:** R05  
**State:** gated future program

## Objective

Investigate whether finite-correlation-length composition disorder near the HgCdTe normal/inverted transition requires a random-mass Kane or Dirac treatment beyond scalar distributional and measurement-kernel models.

## Current status

This program is recognized as a distinct potential work, not as an automatic second stage of the spatial-disorder program.

No controlling implementation issue, manuscript, or production calculation is currently authorized.

## Available foundations

- homogeneous bulk 8-band Kane Hamiltonians;
- symmetry and matrix-projection infrastructure;
- distributional signed-gap diagnostics;
- spatial covariance and measurement-kernel models;
- preliminary dimensionless comparison between correlation length and a Kane mass length.

These foundations do not establish that a random-mass regime occurs in a real specimen.

## Activation gates

Before implementation, require:

1. an independently supported correlation-length range near the relevant composition and temperature;
2. a clearly defined observable not already explained by scalar distributional or finite-kernel theory;
3. a claim-level prior-art audit of HgCdTe disorder, SCBA, and correlated random-mass Dirac/Kane literature;
4. a dimensionless regime showing finite correlation length can materially change the observable;
5. a minimal analytical or low-cost numerical benchmark with a falsification criterion;
6. a decision memo explaining why full Kane structure is necessary.

## Candidate control parameter

A useful screening quantity is

```text
kappa = xi / ell_K,
ell_K = 2 hbar v_K / sigma_E,
```

under a declared convention. This is a regime diagnostic, not a material measurement or proof of topology.

## Unsupported claims

This program does not currently support:

- a specimen-specific random-mass field;
- a topological Anderson phase in HgCdTe;
- domain-wall transport or percolation claims;
- interpreting local gap-sign probability as a bulk invariant;
- production SCBA, tight-binding, or large-scale Kane calculations;
- a manuscript claim based only on generic random-mass literature.

## Shared dependencies

The program would use Kane, symmetry, distributional-gap, and spatial-covariance infrastructure shared with R02, R03, and R04.

## Stop rule

Do not activate the program if plausible correlation lengths remain far outside the regime where finite-`xi` physics changes a measurable prediction, or if the proposed observable is already captured by the scalar portfolio models.