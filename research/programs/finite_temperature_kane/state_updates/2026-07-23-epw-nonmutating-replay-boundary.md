# R02 state update: non-mutating EPW replay boundary supported

**Date:** 2026-07-23  
**Parent state:** `research/programs/finite_temperature_kane/state.md`

## Transition

```text
strict issue-350 replay harness
  -> SERIAL_EPWREAD_PATCH_VALIDATION_STOP remains binding

replay state/output ownership
  -> REPLAY_BOUNDARY_SUPPORTED at design level

runtime validation
  -> NOT AUTHORIZED
```

## Established

- `.epb` files are optional coarse Bloch-representation serialization files.
- `epwread=true, epbread=false` does not consume `.epb` files.
- `epbwrite=true` independently rewrote `diam.epb1` in issue #350.
- `epbwrite=false` suppresses that serialization without changing the declared self-energy, mesh, temperature, broadening or restart-read controls.
- Upstream `epw2.in` supports restart with `epbwrite` left at its false default.
- A future replay seed can exclude all outputs, transients and `.epb` files while retaining every consumed and unknown regular file as immutable state.
- Graceful completion can be established prospectively through exit status, fatal-marker exclusion, the source-grounded total timer, a positive `selfen_elec_` call count and a parseable `linewidth.elself.*` result.

## Replay seed policy

```text
complete preparation tree
  -> remove declared outputs
  -> remove transient files
  -> remove .epb and raw-vertex files
  -> hash all remaining regular files
  -> create byte-identical replay clones
```

Every retained byte remains immutable. Declared outputs must be created from absence. Unknown new files and `.epb` recreation are terminal.

## Input design

```text
first_principles/b0/r02_epw_nonmutating_replay.in
SHA-256 e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda
```

Only the `.epb` output control changes relative to issue #350:

```text
epbwrite  true  -> false
epbread   false -> false, explicit
```

## Completion design

Required together:

```text
exit code zero
no fatal or signal markers
Total program execution
selfen_elec_ timer with N > 0 calls
new nonempty parseable linewidth.elself.* file
```

Rejected as required markers:

```text
JOB DONE.
Electron Self-Energy
```

## Authorization

Open:

- source/design review;
- inert contracts and replay input;
- synthetic filesystem and parser tests.

Closed:

- build, patch application, preparation or replay;
- exporter execution;
- MPI or SOC;
- CdTe, HgTe, HgCdTe, A1, A2 or A3;
- automatic executable successor.

## Controlling records

```text
first_principles/b0/r02_epw_replay_output_boundary_source_audit.json
first_principles/b0/r02_epw_replay_output_boundary_contract.json
research/capability_audits/qe76_epw61_nonmutating_replay_boundary.md
research/decision_records/2026-07-23-r02-epw-nonmutating-replay-boundary.md
```
