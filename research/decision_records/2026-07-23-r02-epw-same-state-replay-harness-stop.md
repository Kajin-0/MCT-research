# R02 decision record: same-state EPW replay stops in the serial restart harness

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #332  
**Closed executable PR:** #333  
**Decision:** terminate the pinned serial same-state `epwread` protocol as `STOP_HARNESS`.

## Objective

Prepare one upstream diamond EPW state, freeze its complete directory tree, create three byte-identical copies, and replay only the final EPW self-energy stage as disabled A, disabled B, and exporter-enabled treatment.

The experiment was intended to separate intrinsic same-state replay variability from exporter I/O effects. It did not reach that comparison.

## Execution identity

```text
workflow run      30020494017
job               89251617785
head              6b7cee7aa043789a273e1b12d2738522992385a6
artifact          8569280948
artifact digest   sha256:1d80fb575a5d736dbd3211edb7dad4c694c151a7209dffed954489924e65dcd8
artifact size     241,357 bytes
```

## Fixed source and binaries

```text
QE / EPW              7.6 / 6.1
source commit         9f93ddec427d2b9a45bb72d828c6d324f62fcabd
source-tree SHA-256   34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849
patch SHA-256         b1cb083f4ff859a33d3f990dce3a0389b37372b251f037c4b479bc7e9832dee1
```

Executable SHA-256 values:

```text
pw.x   572e97aca36d6841d31add2ad803b1ebaf234af9f006c847afdc146aa02a2d73
ph.x   e1717cb27c1b9227947331dce0ea1b1d50db580a8bdd2a16fe15c2864eacd51a
epw.x  9692de1f980314548a7df455d679340d45a028a4768cf14bd42b06fe7800855f
```

## Completed preparation

One build and the complete six-command preparation succeeded:

```text
pinned builds                 1
preparation commands          6 / 6 exit code 0
material calculations         0
prepared-state regular files  168
```

The complete prepared tree was preserved without deleting preparation outputs. Its manifest identity was:

```text
manifest payload SHA-256  6478b7db2839930e8edfdf9350b5f530255a7356305c1da9f89d77be22123289
manifest file SHA-256     646df1e09b0bd986ca980fa5a7193721c8bdbeb05a727b3fc5dd16cfd4a7148c
pre-replay gate SHA-256   dbf1e4bacbd11a63dc2677aed22e55cf8658a9cc7537c853dbba22d57e5b0eda
```

All required preparation paths were present. The disabled-A, disabled-B, and enabled pre-replay manifests were byte-identical.

## Terminal failure

The first replay was exporter-disabled. It exited with code 139 before electron self-energy evaluation:

```text
replay             disabled_a
exporter enabled   false
exit code          139
signal             SIGSEGV
routine            wigner_divide_ndegen_epmat
source             EPW/src/wigner.f90:1009
caller             build_wannier
caller source      EPW/src/wannier.f90:452
```

Evidence identities:

```text
disabled-A stdout  da3421f9bae60fc2cef344756e67d32818de4d17990fe812c237615560654a46
disabled-A stderr  24c2562bb9088f776b78fee404e1369ada4a3dbd7a937cd3001515181874b3bd
exit-code file     690e07064753123c967bbac0180f32da6a753a5bd8b79a47644cef58e776d9f0
```

Disabled B and the enabled treatment were not launched. The exporter was never enabled, no raw-vertex evidence was generated, and no post-replay state manifest was created.

## Source-supported inference

The pinned source provides a plausible explanation for the serial restart failure:

1. `epw_read` explicitly allocates `epmatwp` inside the MPI conditional branch.
2. The non-MPI branch reads records into `epmatwp(:,:,:,:,irg)` without a visible allocation in that branch.
3. `build_wannier` later passes `epmatwp` to `wigner_divide_ndegen_epmat`.
4. The observed serial replay fails in that routine at its first array division.

This supports a likely serial `epwread` allocation defect. It does not prove the diagnosis, validate a patch, or establish that MPI execution would succeed.

## Unevaluated gates

The following were not measured:

```text
post-replay state mutation       not evaluated
disabled A/B reproducibility     not evaluated
enabled exporter attribution     not evaluated
raw normalization                not evaluated
matrix reconstruction            not evaluated
```

No scientific failure or exporter effect was established.

## Decision

Terminate the current serial same-state `epwread` execution protocol.

The historical issue-313 result remains `STOP_NONPERTURBATION_GATE`. This result neither strengthens nor weakens that scientific stop.

Closed:

- another build, preparation, or replay;
- an MPI substitution run;
- a patched-source rerun;
- alternate compiler or build options;
- threshold changes;
- SOC and all material calculations.

Open only for design and source analysis:

- trace the serial allocation and ownership of `epmatwp`;
- identify the smallest source-level correction consistent with MPI and non-MPI layouts;
- design synthetic/static regression coverage;
- decide whether an upstream report is warranted.

No execution is authorized by this decision record.
