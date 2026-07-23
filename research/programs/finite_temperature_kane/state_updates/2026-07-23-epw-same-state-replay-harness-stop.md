# R02 state update: same-state serial EPW replay stops in the harness

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
same-immutable-state exporter attribution
  SERIAL EPWREAD EXECUTION
  -> STOP_HARNESS

serial epwread source diagnosis
  -> DESIGN ONLY
```

## Established

- The pinned QE 7.6 / EPW 6.1 source and observational patch were verified.
- One build completed.
- All six preparation commands completed with zero exit status.
- The complete 168-file prepared tree was hashed without output removal.
- Three byte-identical pre-replay clones were established.
- Required preparation outputs were present.
- The first exporter-disabled replay entered the restart path and failed with SIGSEGV.

## Failure identity

```text
workflow run       30020494017
artifact           8569280948
classification     STOP_HARNESS
replay             disabled_a
exit code          139
routine            wigner_divide_ndegen_epmat
source             EPW/src/wigner.f90:1009
caller             build_wannier
caller source      EPW/src/wannier.f90:452
```

The exporter was not enabled. Disabled B and the enabled treatment did not run.

## Interpretation

The source and backtrace support a likely serial restart-path allocation defect involving `epmatwp`:

- allocation is explicit in the MPI `epw_read` branch;
- the non-MPI branch reads the same array without a visible branch-local allocation;
- the replay fails when the array is processed by `wigner_divide_ndegen_epmat`.

This is an inference requiring source-level confirmation. No correction has been validated.

## Not established

- post-replay state immutability;
- disabled replay reproducibility;
- enabled exporter attribution;
- raw complex-vertex normalization;
- SOC compatibility;
- any material self-energy result.

The historical issue-313 `STOP_NONPERTURBATION_GATE` remains unchanged.

## Authorization

Closed:

- additional build, preparation, or replay;
- MPI substitution;
- patched-source execution;
- alternate build or compiler;
- threshold fitting;
- SOC and material work.

Open only for design:

- audit serial versus MPI `epmatwp` allocation and dimensions;
- define a minimal source correction without executing it;
- add static and synthetic regression logic;
- prepare an upstream-quality diagnosis if the source defect is confirmed.

## Controlling records

```text
first_principles/b0/r02_epw_same_state_terminal_result.json
research/decision_records/2026-07-23-r02-epw-same-state-replay-harness-stop.md
```
