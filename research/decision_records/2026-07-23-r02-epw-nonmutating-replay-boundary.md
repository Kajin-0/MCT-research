# R02 decision record: non-mutating EPW replay boundary supported

**Date:** 2026-07-23  
**Program:** R02 — finite-temperature Kane and electronic structure  
**Issue:** #355  
**Decision:** `REPLAY_BOUNDARY_SUPPORTED` at design level; runtime execution remains closed.

## Context

Issue #350 established two facts simultaneously:

1. the minimal serial `epmatwp` allocation correction removed the observed restart crash and allowed electron-self-energy execution;
2. the strict replay harness still stopped because `diam.epb1` changed and the predeclared completion literals were absent.

The historical classification remains:

```text
SERIAL_EPWREAD_PATCH_VALIDATION_STOP
```

This record does not weaken or reinterpret that result.

## Source decision

Pinned QE 7.6 / EPW 6.1 source separates coarse Bloch serialization from Wannier-state restart:

```text
epbread   read prefix.epb pool files
epbwrite  write prefix.epb pool files
epwread   read Wannier-representation restart state
epwwrite  write Wannier-representation restart state
```

In the tested restart mode:

```text
epwread = true
epbread = false
```

EPW explicitly skips `.epb` input and reports that formatted/Wannier files are used. A separate `epbread OR epbwrite` block controls `.epb` serialization. Therefore `diam.epb1` was not consumed by the replay; it was overwritten only because the issue-350 input retained `epbwrite=true`.

The source supports:

```text
epbwrite = false
epbread  = false
```

as an output-control change that leaves interpolation and electron-self-energy settings unchanged.

## Replay-state boundary

A future preparation tree must be projected into a clean replay seed.

### Immutable seed

Retain and hash:

- every source-audited consumed restart file;
- every otherwise-unclassified regular file, conservatively.

### Remove before seed creation

- all declared result outputs;
- all transient runtime files;
- all `.epb` files;
- all raw-vertex files.

### Replay requirements

- every immutable seed path remains byte-identical;
- declared outputs are created from absence;
- `.epb` and raw-vertex files remain absent;
- unknown new paths terminate the gate.

A path may not be both immutable input and mutable output.

## Completion boundary

The future gate must use independent, source-grounded evidence:

1. process exit code zero;
2. no fatal or signal markers;
3. `Total program execution` from the `stop_epw -> print_clock_epw` path;
4. `selfen_elec_` timer with positive call count;
5. at least one newly created, nonempty, numerically parseable `linewidth.elself.*` file.

The following are rejected as required markers:

```text
JOB DONE.
Electron Self-Energy
```

No one completion condition is sufficient by itself.

## Design result

```text
epb ownership                        resolved
issue-350 mutation cause             resolved
non-mutating state/output split       defined
completion observables                source-grounded
synthetic policy/parser coverage      required
runtime validation                    not performed
classification                        REPLAY_BOUNDARY_SUPPORTED
```

## Authorization

Open:

- source and design review;
- inert replay-input review;
- pure Python filesystem and completion-parser tests.

Closed:

- configure or compilation;
- allocation-patch application;
- preparation or replay;
- exporter-enabled execution;
- MPI or SOC;
- CdTe, HgTe, HgCdTe, A1, A2 or A3;
- automatic executable successor.

A future runtime gate requires a new bounded issue and may not be inferred from this decision.
