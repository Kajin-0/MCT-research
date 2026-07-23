# R02 decision record: serial `epwread` patch removes crash but strict harness stops

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #350  
**Closed executable PR:** #352  
**Decision:** retain `SERIAL_EPWREAD_PATCH_VALIDATION_STOP`; record runtime support for the allocation diagnosis without promoting the replay harness.

## Objective

Validate whether the minimal QE 7.6 serial `epwread` correction removes the exporter-disabled restart crash while preserving every preexisting prepared-state byte and satisfying predeclared completion markers.

## Fixed execution

```text
QE / EPW                  7.6 / 6.1
source commit             9f93ddec427d2b9a45bb72d828c6d324f62fcabd
source-tree SHA-256       34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849
io.f90 Git blob           73fb24ecbf4b690c460006ec354d0b9a7772a044
patch SHA-256             ce24ab3ce90f8fa0d0d098f8e8761511204a99bf96589b9ff37eaff79a330e70
replay-input SHA-256      6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73
fixture                   upstream nonpolar diamond
```

The patch moved the existing `epmatwp` allocation and zero initialization above the MPI/non-MPI split. Static verification found exactly one allocation in `epw_read`, located before that split.

## Execution identity

```text
workflow run              30046644183
job                       89339231302
head                      33939fbaaee71ad1952e14534675e55396460d85
artifact                  8579603653
artifact digest           sha256:17c155f502ecc36cfd88940035ff3c84166d23ac483e09f70ed04dd4a7eb7a67
```

Execution completed:

```text
builds                    1
preparation sequences     1
preparation commands      6 / 6 exit code 0
serial replays            1
replay exit code          0
focused tests             39 / 39 passed
material calculations     0
```

## Positive runtime result

The patched replay did not reproduce the prior failure.

Absent:

```text
SIGSEGV
Segmentation fault
wigner_divide_ndegen_epmat crash marker
```

Present:

```text
Reading Hamiltonian, Dynamical matrix and EP vertex in Wann rep from file
Unfolding on the coarse grid
Electron-Phonon interpolation
selfen_elec_ : ... (216 calls)
Total program execution
EPW          : 1.60s CPU 1.67s WALL
```

Therefore, for this pinned serial fixture:

```text
allocation diagnosis       runtime supported
previous restart crash     removed
self-energy stage          completed
```

This is a meaningful engineering result, but it does not satisfy every issue-350 gate.

## Binding harness failures

### Preexisting state mutation

The prepared state and replay clone were byte-identical before execution:

```text
file count                 168
prepared manifest          431ab24f64e76bb1d57627b8019b69eb3e65fd5007226f5b4b6cf69645d9836a
replay pre-manifest        431ab24f64e76bb1d57627b8019b69eb3e65fd5007226f5b4b6cf69645d9836a
```

After replay, one existing file changed:

```text
path                       diam.epb1
before size                1,137,036 bytes
before SHA-256             cae2607e190fbf4ef25ad27f49231bbfff011d5d42f234d86beccefdd9654b55
after size                 660 bytes
after SHA-256              834e3e9735f346b065f8ec270c4cdce672d72a901f684e5afba1e08eac3d29c1
```

No file was deleted and no new path appeared. Nevertheless, the contract prohibited mutation of any preexisting file, so state integrity failed.

### Literal completion markers

The contract required the exact strings:

```text
Electron Self-Energy
JOB DONE.
```

They were absent. EPW reported completion using different text, including `selfen_elec_` and `Total program execution`.

The observed text is strong evidence that the calculation completed, but the literal marker contract cannot be changed after the run.

## Other gates

```text
exporter variables         unset
raw exporter files         none
forbidden crash markers    none
replay exit code           0
prepared files before/after 168 / 168
```

## Interpretation

The minimal allocation patch is runtime-supported as a correction for the observed serial restart crash.

The stronger claim—an immutable, fully validated serial replay harness—does not pass. Two distinct design questions remain:

1. Is `diam.epb1` an intended replay output that must be isolated or disabled, or an unintended mutation of consumed state?
2. Which stable EPW observables should define self-energy completion without relying on output strings absent from this release?

Neither question may be resolved retrospectively inside issue #350.

## Decision

```text
issue result                         SERIAL_EPWREAD_PATCH_VALIDATION_STOP
allocation source diagnosis          runtime supported
serial restart crash                 removed in patched fixture
strict immutable replay harness      failed
patch merge                          not authorized
additional issue-350 execution       not authorized
```

The executable PR remains unmerged.

Only a design-only successor may inspect:

- source ownership and write semantics of `diam.epb1`;
- whether `epbwrite=.false.` is scientifically and restart-semantically appropriate for replay;
- stable completion observables available in QE 7.6 / EPW 6.1;
- a future immutable-state boundary that separates consumed state from declared replay outputs.

No future run is authorized by this decision record.

## Scientific boundary

Still closed:

- exporter attribution;
- matrix-normalization promotion;
- MPI validation;
- SOC;
- CdTe, HgTe, HgCdTe;
- A1, A2, A3 and dense interpolation.
