# R02 decision record: non-mutating serial EPW replay passes

**Date:** 2026-07-24  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #371  
**Closed executable PR:** #372  
**Decision:** validate the patched non-mutating serial restart harness for the pinned upstream non-SOC diamond fixture.

## Objective

Validate exactly one exporter-disabled serial `epwread` replay after:

- applying the previously diagnosed `epmatwp` allocation correction;
- preparing one pinned upstream diamond state;
- projecting a clean immutable replay seed;
- disabling optional `.epb` serialization with `epbwrite=.false.`;
- preserving source-grounded completion and filesystem-integrity gates.

This run was a software-fixture validation. It was not a material calculation.

## Fixed state

```text
QE / EPW                  7.6 / 6.1
source commit             9f93ddec427d2b9a45bb72d828c6d324f62fcabd
source-tree SHA-256       34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849
allocation patch SHA-256  ce24ab3ce90f8fa0d0d098f8e8761511204a99bf96589b9ff37eaff79a330e70
replay input SHA-256      e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda
boundary design commit    4cb0b9fef65a67e56a794fd3676ef2e687d0e1c3
```

Replay controls:

```text
epbwrite   = .false.
epbread    = .false.
epwwrite   = .false.
epwread    = .true.
wannierize = .false.
elecselfen = .true.
nest_fn    = .false.
```

No physical, temperature, broadening, mesh, band-window, pseudopotential, or self-energy parameter changed.

## Preflight history

An initial workflow attempt stopped during focused tests:

```text
workflow run             30107570717
artifact                 8602243538
builds                   0
preparations             0
replays                  0
focused tests            53 / 54 passed
```

The failure was one structural string assertion that searched for a nonexistent shell literal rather than the actual Python status-path expression. Only that assertion changed. No source, patch, input, contract, threshold, driver behavior, or scientific setting changed. The one scientific authorization therefore remained unconsumed.

## Controlling execution

```text
workflow run             30107733166
job                      89529197616
head                     a50739354b767545acb44c9be98f0d48acf2acf8
artifact                 8602492899
artifact digest          sha256:c3aeb035173b582f33a65ca1688048257ea8c10c092fa6f6d987d0c328f0d032
artifact archive size    305,174 bytes
evidence tree size       3,605,225 bytes
```

Execution counts:

```text
pinned builds            1
preparations             1
preparation commands     6 / 6 exit code 0
serial replays           1
replay exit code         0
analyzer exit code       0
material calculations    0
```

## Immutable seed

The complete successful preparation tree contained 168 regular files. The prospective projection removed six files before replay cloning:

```text
forbidden serialization
  diam.epb1

declared outputs
  EPW.bib
  diam.kgmap
  diam_0.kmap
  linewidth.elself.300.000K
  selecq.fmt
```

The projected seed contained 162 files. Its manifest was identical before replay:

```text
seed manifest SHA-256        9c1cc2151461b25a4f41468268cdce9444efbda11bbb3075de9a64d0e450d1ca
replay-pre manifest SHA-256  9c1cc2151461b25a4f41468268cdce9444efbda11bbb3075de9a64d0e450d1ca
```

After replay:

```text
immutable mutations          0
immutable deletions          0
forbidden files created      0
unknown files created        0
transient files retained     0
```

The replay created only the declared outputs:

```text
EPW.bib
linewidth.elself.300.000K
selecq.fmt
```

No `.epb` or raw-vertex file was created.

## Completion evidence

All prospectively defined completion gates passed:

```text
process exit code zero                 pass
fatal or signal markers absent        pass
Total program execution present       pass
selfen_elec_ timer positive            216 calls
new linewidth.elself.* output         pass
linewidth numeric rows                5,184
linewidth size                        414,841 bytes
```

## Classification

```text
PASS_NONMUTATING_SERIAL_REPLAY
```

This establishes that the pinned serial restart harness can:

1. read the projected immutable Wannier-state seed;
2. pass the corrected `epmatwp` restart path;
3. execute the electron self-energy interpolation;
4. create only declared result outputs;
5. preserve every immutable seed byte.

## Claim boundary

The pass validates only one patched, exporter-disabled, non-mutating serial `epwread` replay of the pinned upstream non-SOC diamond fixture.

It does not establish:

- exporter noninterference;
- enabled/disabled attribution;
- matrix-export normalization in this run;
- SOC-spinor behavior;
- CdTe, HgTe, or HgCdTe validity;
- generalized-Fröhlich material inputs;
- A1, A2, or A3 readiness.

The historical issue-350 stop remains unchanged. The present pass validates the corrected protocol rather than reclassifying the earlier run.

## Decision

- Close issue #371 as completed after this record merges.
- Keep executable PR #372 closed and unmerged.
- Prohibit additional issue-371 builds, preparations, or replays.
- Permit a separately reviewed same-state exporter-attribution successor.
- Do not authorize that successor automatically.
- Keep SOC and all material calculations closed.
