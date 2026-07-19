# Hermitian covariance coordinate correction

**Date:** 2026-07-19  
**Status:** validated schema and statistical correction

## Problem

An `8x8` Hermitian Hamiltonian has 64 independent real coordinates, but the repository stored and fitted its covariance using 128 stacked real and imaginary matrix entries. The duplicated conjugate entries created redundant observations, singular covariance directions, and inflated statistical degrees of freedom.

A general complex dynamical self-energy is different: damping may make it non-Hermitian, so it can require all 128 real coordinates.

## Decision

Use two explicit coordinate systems:

- **64D orthonormal Hermitian coordinates** for Hamiltonian and quasiparticle-Hamiltonian statistics;
- **128D real/imaginary coordinates** for general complex operators.

The Hermitian basis contains eight real diagonal entries and the real and imaginary upper-triangle entries scaled by `sqrt(2)`. Its Euclidean norm equals the matrix Frobenius norm.

## Consequences

- Kane projection uses 64 observations per matrix.
- Unweighted Frobenius least-squares point estimates are unchanged by the coordinate correction.
- Hamiltonian chi-square, reduced chi-square, standard errors, and covariance diagnostics previously computed in redundant 128D coordinates are superseded.
- General complex self-energy covariance remains 128D.

## Dataset schema

Schema `2.0` stores a padded covariance container and one dimension value per record: `0`, `64`, or `128`.

Schema `1.0` remains readable:

- Hamiltonian covariance is projected into the 64D Hermitian subspace;
- complex self-energy covariance remains 128D;
- migration provenance is recorded.

## Validation

The focused suite verifies:

1. matrix-coordinate round trip;
2. Frobenius norm equality;
3. orthonormal embedding;
4. covariance embed/project round trip;
5. unitary rotation;
6. positive-semidefinite symmetry projection;
7. corrected observation count and degrees of freedom;
8. schema-v1 migration;
9. schema-v2 mixed 64D/128D round trip;
10. legacy export conversion and rejection of 64D covariance for non-Hermitian operators.

Evidence:

- validated head: `b3c3eaac9e11a1e13e4bc2840d9e481103c7a485`
- workflow run: `29667041548`
- artifact: `8436037457`
- digest: `sha256:2953a3a5a00efb34ec29191efad1acfd3c7112aa8f459ff25bd04971826ffc36`

Machine-readable record: `validation/hermitian_covariance_64d_reference_result.json`.
