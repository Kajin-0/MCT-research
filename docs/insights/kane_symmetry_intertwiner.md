# Symmetry-defined Kane basis at Gamma

## Problem

The CdTe runtime smoke supplies an eight-state Gamma manifold and direct finite-k overlaps, but each exactly degenerate Gamma eigenspace has an arbitrary unitary gauge. Irrep labels or characters identify `Gamma6`, `Gamma8`, and `Gamma7`; they do not identify the conventional basis vectors inside those spaces.

Fitting conventional Kane matrix elements before resolving this gauge can rotate physical couplings into different matrix entries without changing any eigenvalue or character.

## Target representation

Use the conventional cubic axes and generate target double-group matrices from:

- `Gamma6`: an `s` orbital times spin one-half;
- `Gamma8`: the `j=3/2` subspace of Cartesian `p` orbitals times spin;
- `Gamma7`: the `j=1/2` subspace of Cartesian `p` orbitals times spin.

The two declared generators are proper `C3` about `[111]` and improper `S4` about `z`. Spin transforms axially under an improper polar operation `R`, through the proper rotation `det(R) R`.

Their target characters are:

| irrep | `C3[111]` | `S4z` |
|---|---:|---:|
| Gamma6 | `+1` | `+sqrt(2)` |
| Gamma8 | `-1` | `0` |
| Gamma7 | `+1` | `-sqrt(2)` |

The improper generator is essential for distinguishing the two spinor doublets.

## Intertwiner theorem

Let `Dcalc(g)` be a symmetry matrix in the arbitrary DFT eigenbasis and `DKane(g)` the target matrix. Solve

```text
Dcalc(g) W = W DKane(g)
```

for both generators by taking the nullspace of

```text
I kron Dcalc(g) - DKane(g)^T kron I.
```

For one copy of an irreducible representation, Schur's lemma gives one complex null vector. Polar decomposition maps it to the nearest unitary matrix.

The synthetic certificate shows:

- one generator leaves a multidimensional gauge freedom;
- `C3` plus `S4` gives nullity exactly one for Gamma6, Gamma8, and Gamma7;
- randomly rotated 2D, 4D, and 2D subspaces are recovered to approximately machine precision;
- characters remain exactly unchanged under the random rotations and therefore cannot perform this task.

## Time reversal and signs

For antiunitary time reversal represented by `A K`, require

```text
W^dagger Acalc W* = AKane.
```

This fixes the continuous complex phase of each intertwiner. One discrete sign per inequivalent irrep remains. Those relative signs are conventional and must be fixed by a declared linear-k Kane matrix-element convention, for example requiring one selected `P8` element to be real and positive and then applying the published Gamma7 phase convention.

## Physical implementation route

IrRep provides a Quantum ESPRESSO parser and a `symm_matrix` routine that returns full symmetry matrices in the Bloch-eigenstate basis, not only traces. Its `BandStructure` object also exposes symmetry matrices by degenerate band block. Primary reference: M. Iraola et al., *Computer Physics Communications* **272**, 108226 (2022), DOI `10.1016/j.cpc.2021.108226`.

Do not use Quantum ESPRESSO `pw2wannier90.x write_dmn` for this SOC gate. The interface documents `write_dmn`, but the maintained developer guidance states that noncollinear support is not implemented. The direct IrRep/QE wavefunction route is therefore the narrower auditable path.

## Next runtime gate

At the existing planning geometry:

1. Pin an exact IrRep source revision and dependency set.
2. Read the completed QE `.save` directory before the runner is destroyed.
3. Identify bands 31-32, 33-36, and 37-38 as the three energy-degenerate blocks, then verify their Gamma7, Gamma8, and Gamma6 characters.
4. Export full `C3[111]`, `S4z`, and time-reversal matrices for each block.
5. Solve the intertwiners and report nullspace singular values, unitarity, all-generator residuals, and phase-fixing residuals.
6. Rotate the already reconstructed finite-k Hamiltonians into the canonical basis.
7. Only then fit `P8`, `P7`, `F`, and `gamma1-3`.

No phonon, AHC, HgTe, alloy, or physical-parameter claim is authorized by this analytical result.
