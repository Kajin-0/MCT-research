# ZG selected-band matrix reconstruction decision

**Date:** 2026-07-18  
**Status:** synthetic supercell reconstruction oracle passed

## Question

Can a special-displacement route preserve the full finite-temperature eight-band matrix, rather than only temperature-dependent eigenvalues, when distorted supercells introduce band folding, remote-state mixing, arbitrary phases, rotations inside degenerate manifolds, odd displacement terms and broken primitive-cell symmetry?

## Synthetic construction

The oracle begins with exact temperature-dependent extended-Kane matrices at:

```text
Gamma
+/-[001]
+/-[111]
+/-[110] holdout
```

For each temperature and configuration it embeds the eight primitive states into a 16-state synthetic supercell, mixes them weakly with a remote complement, randomizes eigenvector phases, rotates exactly degenerate eigenspaces, shuffles the band order and adds:

- odd-in-displacement matrix terms;
- zero-mean configuration terms;
- Gamma-irrep and finite-k time-reversal breaking artifacts.

No primitive band index survives by assumption.

## Reconstruction

1. Select eight supercell states by total projection weight onto the primitive reference manifold.
2. Form the primitive-reference overlap matrix.
3. Use its unitary polar factor to transport the selected eigenspace into the fixed primitive reference gauge.
4. Pair positive and negative displacements.
5. Average three configuration pairs.
6. Restore Gamma block covariance and time reversal between opposite k points.
7. Fit the extended-Kane matrix on Gamma, [001] and [111].
8. Predict the unused [110] direction.

## Result

Evidence:

```text
workflow run: 29651328986
artifact:     8431551243
digest:       sha256:df61798f1cf4eac0ed08d1fcfb9fa23a38230dd3015519b10ee60a8e13253f49
```

Metrics:

```text
minimum selected overlap singular value          = 0.9600132263
maximum per-configuration reconstruction error   = 7.22785e-15
minimum unpaired-configuration error              = 0.53537%
maximum first-pair error                          = 0.30032%
minimum pre-restoration symmetry residual         = 0.28991%
maximum post-restoration symmetry residual        = 0
maximum final primitive-matrix error              = 7.18248e-16
maximum extended-parameter absolute error         = 1.07176e-11
maximum training fit residual                     = 1.74378e-15
maximum unused-[110] prediction error             = 1.91304e-15
minimum eigenvalue-only matrix error               = 180.005%
```

The primitive matrix is therefore recoverable under the declared overlap assumptions, despite arbitrary eigenvector gauge and remote-state leakage.

## Required operations

The oracle makes four requirements non-optional:

- selected-subspace overlap and polar alignment;
- positive/negative displacement pairing;
- multiple configuration averaging;
- explicit primitive symmetry restoration.

A temperature-dependent eigenvalue list is not an acceptable substitute for the matrix. In this oracle, placing the selected eigenvalues on a diagonal in the primitive basis gives at least `180%` relative matrix error.

## Decision

- The selected-band supercell reconstruction architecture is ready.
- A real ZG export contract may now be designed.
- Real ZG or supercell DFT execution remains unauthorized.
- The next contract must specify primitive/supercell overlaps, selected-state weights, supercell-size convergence, configuration-count convergence, symmetry restoration, and polar finite-size correction.

## Remaining physical blockers

1. A real supercell may not retain a well-conditioned eight-state overlap manifold.
2. Configuration-pair and configuration-count convergence are unknown.
3. Polar long-range interactions converge slowly with supercell size and need a controlled finite-size correction.
4. Distorted-cell band folding and state crossings may require more than eight selected states before downfolding.
5. Single-mode or frequency-resolved reconstruction remains separate from the total special-displacement matrix.
6. The current CdTe PBE polar response is not an acceptable long-range reference.

## Claim boundary

This result establishes method feasibility on known synthetic truth. It does not establish a real supercell size, configuration count, overlap threshold, polar correction, material accuracy or computational authorization.
