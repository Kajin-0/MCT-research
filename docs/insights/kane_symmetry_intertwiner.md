# Symmetry-defined Kane basis at Gamma

## Problem

The CdTe runtime smoke supplies an eight-state Gamma manifold and direct finite-k overlaps, but each exactly degenerate Gamma eigenspace has an arbitrary unitary gauge. Irrep labels or characters identify `Gamma6`, `Gamma8`, and `Gamma7`; they do not identify the conventional basis vectors inside those spaces.

Fitting conventional Kane matrix elements before resolving this gauge can rotate physical couplings into different matrix entries without changing any eigenvalue or character.

A second requirement is equally important: the target irrep basis must use the exact phase convention of the executable Kane Hamiltonian. Two bases can have identical characters and symmetry content while assigning a different sign or phase to `P7` or `P8`.

## Target representation

Use the explicit eight-band states of Novik et al. Eq. (4), in the repository order

```text
Gamma6(+1/2), Gamma6(-1/2),
Gamma8(+3/2), Gamma8(+1/2), Gamma8(-1/2), Gamma8(-3/2),
Gamma7(+1/2), Gamma7(-1/2).
```

The implementation constructs these states directly from Cartesian `(X,Y,Z)` orbitals and spin. The generated symmetry matrices must satisfy

```text
D(g) H_Kane(k) D(g)^dagger = H_Kane(g k)
```

for the complete executable one- and two-`P` Hamiltonians. This covariance test is the phase-convention gate that characters alone cannot provide.

The two declared generators are proper `C3` about `[111]` and improper `S4` about `z`. Spin transforms axially under an improper polar operation `R`, through the proper rotation `det(R) R`.

Their target characters are:

| irrep | `C3[111]` | `S4z` |
|---|---:|---:|
| Gamma6 | `+1` | `+sqrt(2)` |
| Gamma8 | `-1` | `0` |
| Gamma7 | `+1` | `-sqrt(2)` |

The improper generator distinguishes the two spinor doublets.

## Intertwiner theorem

Let `Dcalc(g)` be a symmetry matrix in the arbitrary DFT eigenbasis and `DKane(g)` the Novik-convention target matrix. Solve

```text
Dcalc(g) W = W DKane(g)
```

for both generators by taking the nullspace of

```text
I kron Dcalc(g) - DKane(g)^T kron I.
```

For one copy of an irreducible representation, Schur's lemma gives one complex null vector. Polar decomposition maps it to the nearest unitary matrix.

The synthetic certificate shows:

- one generator leaves multidimensional gauge freedom;
- `C3` plus `S4` gives nullity exactly one for Gamma6, Gamma8, and Gamma7;
- randomly rotated 2D, 4D, and 2D subspaces are recovered to machine precision;
- characters remain unchanged under those rotations and cannot determine the internal basis;
- a character-preserving phase error is rejected by the Hamiltonian covariance test.

## Time reversal and signs

For antiunitary time reversal represented by `A K`, require

```text
W^dagger Acalc W* = AKane.
```

`AKane` must be the same phase convention used by `mct_research.kane8.time_reversal_unitary()`. In particular, the p-like Bloch sector carries the conventional relative phase required by the published Novik matrix.

Time reversal fixes the continuous complex phase of each intertwiner. One discrete sign per inequivalent irrep remains. Those relative signs are fixed only from finite-k Kane matrix elements, for example by requiring declared `P8` and `P7` elements to be real and positive.

## Complete double-group section

A spatial operation has two spinor lifts differing by the central minus sign. Independent principal SU(2) choices do not necessarily form one global multiplication table.

The physical runtime therefore:

1. matches the `C3[111]` and `S4z` lifts;
2. generates all 48 double-group elements by multiplication;
3. maps every IrRep operation using both its spatial rotation and recorded spinor lift;
4. forms antiunitary targets by composition with matched time reversal;
5. validates all 24 unitary and 24 antiunitary matrices.

The corrected Novik-convention CdTe result passes with maximum canonical residual approximately `6.2e-12`.

## Physical implementation route

IrRep provides a Quantum ESPRESSO parser and a `symm_matrix` routine returning full matrices in the Bloch-eigenstate basis. The direct IrRep/QE wavefunction route is used because characters are insufficient and the relevant Wannier90 double-group export route is not used for this SOC gate.

## Next runtime gate

At the existing planning geometry:

1. reconstruct exact finite-k fixed-reference Hamiltonians from the Gamma-star overlaps and exact QE eigenvalues;
2. rotate them with the committed Novik-convention intertwiners;
3. fix relative irrep signs using declared real-positive `P8` and `P7` elements;
4. use paired `+/-k` points at `h` and `h/2` to remove leading finite-radius contamination;
5. fit on `[001]` and `[111]`;
6. hold out `[110]`;
7. compare one-`P` and two-`P` closure and propagate the available numerical covariance.

Only after that gate passes may the smoke report finite-k Kane parameters. No phonon, AHC, HgTe, alloy, or converged physical-parameter claim is authorized here.
