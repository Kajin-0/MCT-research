# Independent-Hermitian matrix covariance schema

**Date:** 2026-07-18  
**Status:** implementation and deterministic method validation  
**Decision:** replace redundant 128-real-component covariance for Hermitian `8 x 8` matrices with 64 independent Frobenius-isometric coordinates.

## Problem

The former matrix pipeline represented every complex `8 x 8` matrix as

```text
vec128(H) = [Re H(:), Im H(:)].
```

That representation has 128 real entries. A Hermitian `8 x 8` Hamiltonian has only

```text
8 diagonal real entries + 2 * C(8,2) off-diagonal real entries = 64
```

independent real degrees of freedom.

For Hermitian observations, the former representation therefore duplicated the lower and upper triangles and retained zero imaginary diagonal directions. A covariance in that space is singular on the physical Hermitian manifold. Eigenvalue flooring can make a numerical whitener executable, but it does not make chi-square, likelihood, degrees-of-freedom, or parameter-standard-error claims statistically valid.

## Coordinate definition

The replacement coordinate map is

```text
hvec(H) = [
  H_00, ..., H_77,
  sqrt(2) Re H_01, sqrt(2) Im H_01,
  ...,
  sqrt(2) Re H_67, sqrt(2) Im H_67
].
```

The `sqrt(2)` scaling makes the map an isometry:

```text
hvec(A)^T hvec(B) = Re Tr(A^dagger B)
||hvec(A)||_2      = ||A||_F.
```

A unitary basis transformation

```text
H -> U^dagger H U
```

therefore induces an orthogonal `64 x 64` real map. Total covariance trace is preserved under unitary gauge rotation without duplicating matrix entries.

## Schema decision

- current matrix dataset schema: `2.0`;
- covariance coordinate system: `hermitian_frobenius_64`;
- covariance shape per matrix: `64 x 64`;
- new JSONL, NetCDF, and array exports reject legacy `128 x 128` covariance;
- schema `1.0` files remain readable through an explicit migration path.

Legacy migration applies

```text
L_legacy = hvec o Hermitize o unvec128
C64      = L_legacy C128 L_legacy^T.
```

The returned dataset is schema `2.0`. Global provenance and per-record metadata record that the covariance was projected from `complex_cartesian_128` to `hermitian_frobenius_64`.

## Statistical consequence

For `N` matrices and `p` fitted parameters, the matrix-regression residual degrees of freedom are now based on

```text
64 N - p
```

rather than the former redundant

```text
128 N - p.
```

Previously reported parameter covariance or chi-square values obtained from the redundant coordinate representation must not be interpreted as calibrated statistical quantities. Deterministic parameter estimates and unweighted Frobenius residuals are not invalidated by this correction.

## Deterministic validation

The committed validation oracle reports:

```text
roundtrip maximum error                 2.22e-16
Frobenius inner-product error           1.11e-15
unitary-map orthogonality residual      6.39e-15
legacy identity-covariance error        2.22e-16
|det(unitary coordinate map)|           1.0000000000000009
```

All declared gates pass.

## Scope boundary

This correction validates matrix coordinates, covariance transport, and schema migration. It does not:

- estimate physical covariance from electronic-structure convergence ensembles;
- propagate uncertainty in the numerical gauge or selected subspace;
- define covariance for a general non-Hermitian, frequency-dependent self-energy;
- convert a diagonal-only self-energy export into a full matrix;
- authorize new material or finite-temperature claims.

A general complex self-energy may still be stored without covariance. Covariance on a record is accepted only when the matrix is Hermitian. A separate explicit coordinate system is required before non-Hermitian self-energy covariance can be supported.

## Files

- `src/mct_research/hermitian.py`
- `src/mct_research/dataio.py`
- `src/mct_research/projection.py`
- `src/mct_research/pipeline.py`
- `src/mct_research/code_exports.py`
- `tools/validate_hermitian_covariance_schema.py`
- `validation/hermitian_covariance_schema_reference_result.json`
- `tests/test_hermitian_coordinates.py`

## Next statistical work

1. Preserve 64D covariance as the only Hermitian matrix uncertainty representation.
2. Estimate covariance from declared convergence ensembles rather than synthetic diagonal matrices.
3. Add gauge/subspace uncertainty only after a physically meaningful stochastic model is specified.
4. Keep non-Hermitian self-energy covariance fail-closed until an explicit full-complex schema and observable use case are justified.
