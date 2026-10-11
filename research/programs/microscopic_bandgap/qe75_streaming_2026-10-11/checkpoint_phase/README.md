# Bounded checkpoint and resource-engineering phase

Base: MCT `ea8823e`; separate new user scope, historical BLOCKED goal unchanged.

**Decision: STOP_NO_NATIVE_STATE_BRIDGE.** Durable no-copy **storage ownership**,
read-only Fortran storage import and resource primitives pass small tests. The
complete native QE checkpoint capture/import bridge is **not implemented or
qualified**. Task 1 therefore has not passed its native-state gate; the sequential
MPI/FFT/EXX comparison is **NOT ADMITTED / NOT RUN**. No statement of successful
native SCF restart, MPI equivalence, full-run memory or material x_c.

| Requested stage | Actual result |
|---|---|
| Versioned atomic EXX stream checkpoint | Hard-link ownership/commit/checksum/layout/provenance backend implemented and tested; Fortran open-store deletion and storage restoration tested. Full old-ACE/occupation and native-SCF-state bridge remains OPEN |
| Disk/quota/reservation/RAM guards | 64-bit block/quota admission and ext4 reservation APIs tested; read-only quota status resolved. Runtime predicates implemented, but no native launch monitor/source callback integration is claimed |
| Small stock/private native comparison | Protocol retained; prerequisite source/state gate fails, so no native process is launched |

- [Checkpoint contract and precise native obstruction](checkpoint_contract.md)
- [Resource contract and measurements](resource_contract.md)
- [Conditional single-fixture protocol](native_fixture_protocol.md)
- [Decision](decision.md), [persistent handoff](handoff_ledger.md)
- [Test evidence](tests_final.json), [24 storage regressions](store_regression.json)
- [Measured outcomes and preservation](phase_outcomes.json)

Implementation: `checkpoint_capsule.py`, `exx_qstream_v2.f90`, `storage_guard.c`,
`resource_guard.py`. Reproduction: `build_and_check.py`; tests never invoke QE or
MPI. All compiled artifacts and tiny fixtures stay under DFT
`.local/qe75_lowram_20261011/checkpoint_phase`. The original QE installation,
previous private PW binary, numerical inputs and detached supervisors are untouched.

**Correction to the dated first-package claim:** the initial refusal patch missed
QE's **between-EXX-iterations** stop/export path. That path can write `restart_e`
without the new stream protocol. The private-source correction in
`outer_stop_guard.patch` compiles and closes that path with an explicit refusal.
It is a refusal fix, **not** a completed native checkpoint exporter. The patch is
retained as zero-context review evidence; use the guarded script to reproduce it
in a private source copy. Prior compiled PW candidate remains unexecuted and
unqualified; this phase does not silently deploy a changed executable.
