# Deterministic Weiler quadratic classes for static CdTe

## Status

The complete ten-dimensional quadratic projector has been separated into deterministic classes carrying the established Weiler labels

```text
F, N2, G, G',
gamma1, gamma2, gamma3,
gamma2', gamma3', gamma1'.
```

The labels identify symmetry classes and matrix sectors. The fitted numbers in this note use an explicit **repository orthonormal class normalization**. They are not yet conventional Weiler parameter values.

## Class construction

The six quadratic tensors decompose under `Td` as

```text
Sym^2(Gamma15) = A1 + E + T2.
```

In tensor coefficient order

```text
xx, yy, zz, yz, zx, xy,
```

the repository uses

```text
A1: (xx + yy + zz) / sqrt(3)
E:  (-xx - yy + 2zz) / sqrt(6), (xx - yy) / sqrt(2)
T2: yz, zx, xy
```

with the off-diagonal tensor matrices themselves normalized by `1/sqrt(2)`.

Each tensor-irrep subspace is combined with one declared matrix sector and projected through the complete `Td` plus time-reversal Reynolds projector. Every declared pair produces exactly one invariant:

| Class | Matrix sector | Tensor irrep |
|---|---|---|
| `F` | `Gamma6-Gamma6` | `A1` |
| `N2` | `Gamma6-Gamma8` | `E` |
| `G` | `Gamma6-Gamma8` | `T2` |
| `G'` | `Gamma6-Gamma7` | `T2` |
| `gamma1` | `Gamma8-Gamma8` | `A1` |
| `gamma2` | `Gamma8-Gamma8` | `E` |
| `gamma3` | `Gamma8-Gamma8` | `T2` |
| `gamma2'` | `Gamma8-Gamma7` | `E` |
| `gamma3'` | `Gamma8-Gamma7` | `T2` |
| `gamma1'` | `Gamma7-Gamma7` | `A1` |

The ten class vectors are orthonormal to `5.88e-16` and reproduce the complete quadratic projector to `9.30e-15`.

## Exact conventional ties

The executable conventional homogeneous Kane model contains the four templates

```text
f, gamma1, gamma2, gamma3.
```

In repository class normalization, their normalized directions are

```text
f      = +F

gamma1 = -sqrt(2/3) gamma1
         -1/sqrt(3) gamma1'

gamma2 = -1/sqrt(3) gamma2
         -sqrt(2/3) gamma2'

gamma3 = +1/sqrt(3) gamma3
         -sqrt(2/3) gamma3'.
```

The executable templates agree with these relations to `4.01e-16`.

This proves directly that the conventional model:

1. omits the `N2`, `G`, and `G'` sectors;
2. retains only one fixed direction in each unprimed/primed gamma pair;
3. removes the three orthogonal gamma-departure directions.

The signs above belong to the deterministic repository basis. They are not a claim about universal textbook parameter signs.

## Static CdTe coordinates

Fit on `[001]` and `[111]`; retain `[110]` as unused holdout.

| Repository class | Coordinate, eV A^2 |
|---|---:|
| `F` | 7.20115 |
| `N2` | 6.11465 |
| `G` | 7.01960 |
| `G'` | 9.42491 |
| `gamma1` | -15.26615 |
| `gamma2` | -8.75565 |
| `gamma3` | -1.59802 |
| `gamma2'` | 4.58769 |
| `gamma3'` | -18.50707 |
| `gamma1'` | -17.12300 |

Closure remains

| Quantity | Result |
|---|---:|
| Design rank | 10 |
| Condition number | 1.73205 |
| Training residual | `1.3748e-5` |
| `[110]` residual | `8.6242e-6` |

These are coordinates of unit-norm invariant functions, not conventional dimensionless Luttinger parameters or standard Weiler `N2/G/G'` coefficients.

## Departures from the conventional subspace

The three omitted conduction-valence coordinates are

```text
N2 = 6.11465 eV A^2
G  = 7.01960 eV A^2
G' = 9.42491 eV A^2.
```

Projecting each primed/unprimed gamma pair onto the direction orthogonal to the conventional tie gives

```text
gamma1 departure =  +5.16695 eV A^2
gamma2 departure =  -9.79766 eV A^2
gamma3 departure = -11.98984 eV A^2.
```

All six established departures are therefore nonzero at the static smoke point. This explains why adding only one channel group did not close the matrix Hamiltonian.

## Scientific interpretation

The result now supports a precise statement:

> The conventional homogeneous Novik/Kane quadratic reduction is exactly a four-dimensional tied subspace of the established ten-dimensional Weiler double-group space. The projected static CdTe matrices require components in all six directions removed by that reduction.

The result does not yet support:

- standard numerical values of `N2`, `G`, `G'`, or primed gamma parameters;
- converged CdTe material parameters;
- six new invariants;
- a novel Hamiltonian form;
- finite-temperature or HgCdTe conclusions.

## Next authorized gate

Derive the exact standard Weiler matrix normalization in the fixed Novik basis from primary formulas. The gate must:

1. construct conventional-scale matrices for all ten named parameters;
2. prove a full-rank transformation to the repository class basis;
3. document all basis, phase, unit, and sign conversions;
4. reproduce the current matrix closure;
5. only then report named parameter values in standard normalization.

No new electronic-structure, denser-`k`, additional-band, phonon, AHC, HgTe, or alloy calculation is authorized.
