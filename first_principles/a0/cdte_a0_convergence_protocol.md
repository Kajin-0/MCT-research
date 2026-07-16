# CdTe A0 convergence protocol

## Status

This document declares the smallest sequential convergence plan for the authorized
CdTe A0 static, coarse-phonon, dielectric and Born-charge sanity stage.

No calculation has been run. The ladder values are candidate test points, not
converged settings and not scientific results.

## Release-specific basis

The protocol is tied to the pinned Quantum ESPRESSO source:

```text
QEF/q-e qe-7.4.1
commit 500de340b820e1cb8c05f2d8bb8fced102f377c1
```

In `PW/Doc/INPUT_PW.def`, this release states that:

- `ecutrho` defaults to `4 * ecutwfc`;
- for norm-conserving pseudopotentials the default should generally be retained,
  because reducing it introduces noise especially in forces and stress;
- testing remains mandatory;
- in a noncollinear calculation, the number of conduction states is
  `nbnd - number of electrons`.

The byte-verified PseudoDojo pair contains 20 Cd and 16 Te valence electrons, so
the primitive CdTe cell contains 36 electrons in the noncollinear SOC accounting
used here.

## Principle

Change one numerical control at a time, lock the first setting that passes two
successive refinements, then perform one cross-factor recheck using the selected
settings and the next denser available combination.

Do not infer convergence from a single adjacent comparison. Do not extend any
ladder automatically if its largest point fails.

## Declared sequence

### 1. Charge-density cutoff

Hold:

```text
ecutwfc = 114 Ry
```

and test:

| ecutrho / ecutwfc | ecutrho (Ry) |
|---:|---:|
| 4 | 456 |
| 5 | 570 |
| 6 | 684 |

This starts at the QE norm-conserving default but does not assume it is adequate
for stress, phonons or response quantities.

### 2. Wavefunction cutoff

After selecting the charge-density ratio, test:

```text
ecutwfc = 94, 102, 114 Ry
```

with `ecutrho = selected_ratio * ecutwfc`.

These are PseudoDojo starting hints converted from Hartree to Rydberg. They are
not convergence evidence.

### 3. Electronic k grid

Use unshifted cubic automatic grids:

```text
4x4x4 -> 6x6x6 -> 8x8x8 -> 10x10x10 -> 12x12x12
shift = 0 0 0
```

The even, zero-shift ladder samples Gamma directly and preserves a consistent
cubic grid convention. Stop at the first point with two successive passing
refinements. A 12-cube failure requires a new decision memo.

### 4. SOC band count

For 36 valence electrons in the noncollinear accounting, test:

| nbnd | explicit empty spinor states |
|---:|---:|
| 40 | 4 |
| 48 | 12 |
| 56 | 20 |
| 64 | 28 |

The purpose is to stabilize the Gamma conduction edge and response quantities.
This A0 ladder does not establish the empty-state requirement of a future AHC
backend; A1 must record whether it uses explicit sums or a Sternheimer method.

### 5. Iterative thresholds

Electronic SCF:

```text
1e-8 -> 1e-10 -> 1e-12 Ry
```

Phonon response:

```text
tr2_ph = 1e-12 -> 1e-14
```

### 6. Cross-factor recheck

After selecting each independent control, rerun:

1. the complete selected setting;
2. the next denser available combination.

If any required observable moves beyond its threshold, the independent
one-factor selections are not accepted. Reopen the coupled controls; do not
average discrepant values.

## Observable thresholds

The thresholds allocate at most 0.25 meV to each Gamma edge from A0 controls,
leaving numerical budget for the later q-grid, denominator, polar and
Fan/Debye--Waller uncertainties required by the A1 decision memo.

| Observable change between refinements | Maximum |
|---|---:|
| total energy | 0.2 meV/atom |
| hydrostatic or largest stress component | 0.02 GPa |
| Gamma conduction edge | 0.25 meV |
| Gamma valence edge | 0.25 meV |
| Gamma gap | 0.5 meV |
| spin-orbit splitting | 0.5 meV |
| optical phonon frequency | 0.2 cm^-1 |
| acoustic-sum-rule residual | 0.1 cm^-1 |
| dielectric-tensor component | 0.2% relative |
| Born effective-charge component | 0.005 e |

Use the maximum absolute change over symmetry-equivalent components and over all
reported volume points. Record raw values and differences; do not retain only a
pass/fail flag.

## Execution order and stopping rules

1. Resolve and hash the physical lattice source first.
2. Verify exact runtime pseudopotential hashes and installed code binaries.
3. Render and syntax-check the complete ladder against the pinned releases.
4. Execute only A0 points, smallest first.
5. Stop a ladder once two successive refinements pass all applicable criteria.
6. Stop the branch if the largest point fails or if convergence is nonmonotonic.
7. Do not run the A1 `4x4x4` electron-phonon pilot until A0 results are reviewed.

## Validation command

```bash
python tools/check_cdte_a0_convergence_protocol.py \
  --require-valid \
  --report-json runs/cdte_a0/convergence-protocol-report.json
```

This command validates the declared protocol only. It does not execute QE or
ABINIT and cannot certify numerical convergence.

## What this protocol does not establish

- no lattice constant is selected;
- no cutoff, k grid, band count or threshold is converged;
- no static band ordering, gap, phonon, dielectric tensor or Born charge is known;
- no AHC, EPW, HgTe or alloy calculation is authorized;
- no analytical HgCdTe equation or novelty claim changes.
