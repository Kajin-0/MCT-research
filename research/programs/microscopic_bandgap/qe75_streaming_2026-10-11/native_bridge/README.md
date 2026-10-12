# Native checkpoint bridge candidate — finite phase from b1a4772

**Decision: STOP_NATIVE_READBACK_AND_RUNTIME_OWNERSHIP_BOUNDARY.** A substantive
private bridge candidate is implemented and compiled. It is **not a qualified QE
restart**, and its private executable has never been executed. No PW, MPI, HSE,
16-atom calculation, supervisor operation or historical goal API is invoked.

Work began on 2026-10-11 and concluded on 2026-10-12 UTC. This is the separately
authorized engineering task, on `research/hgcdte-impurity-tmatrix-20261010`.
All earlier material rejection gates remain in force.

## Implemented and checked

- Exact version-2 native rank packet: **old xi**, old source occupations, current
  `wg/et`, outer counter/stop mode, `tr2`, `dexx`, `exxen`, `fock0..3`,
  `tr2_final`, and **current `ethr`**. Byte order, shapes, actual valid G/q/FFT
  maps, profile fingerprint, extent and I/O failures have explicit refusals.
- Native source hooks at the inner and outer EXX stops; publication occurs only
  after native `punch('all')`. A natural inner iteration-limit exit now writes
  its previously missing `restart_scf` record. Partial-k counter semantics remain
  unchanged. Wavefunction import refuses atomic/random fallback.
- An import branch performs the existing basis/kernel setup, then restores old
  occupations/xi and a read-only stream. It bypasses source-orbital production
  and ACE rebuilding. All source/ACE bands remain present; no HSE, SOC, cutoff,
  mesh or target-deck setting is edited.
- Full native-file transaction: closed density/schema/current waves/old ACE,
  copied native PPs, SCF/k counters and mixing history are bound to every rank's
  operator packet. SHA-256, same-inode hard links, file/directory fsync, an atomic
  global pointer, import retirement and ownership-checked orphan cleanup are
  implemented. This is single-checkpoint consumption, **not rolling retention**.
- An exact 64-bit reservation request connects the native producer to checked
  ext4/quota `fallocate`. A new reserved-inode storage API resolves the previous
  incompatibility between preallocated files and `qs_begin(STATUS='new')`.
- Runtime dispatch refuses absent admission, synthetic provenance, an unowned or
  stale monitor, wrong input/binary/backend fingerprints and invalid resources.
  **No monitor/whole-job lease implementation or admitted native profile is
  supplied by this phase.** These refusals are not a substitute for testing that
  complete runtime handshake.

## Evidence and limits

[Validation](validation.json): **21 serial test methods**, including O0/O2 exact
roundtrips, independent Python decoding of actual Fortran bytes, both stop modes,
five publication failure points, retirement failure, corrupt native density and
packet payload, cross-rank mismatch, stale mixing history, symlinks, foreign-file
cleanup refusal, tiny real reservations and collision rollback. A boolean cannot
promote synthetic provenance into native runtime. All **24 inherited storage
regression cases** also pass against the extended store.

[Build](build_results.json): **14 native-unit compiles** (seven units with and
without the streaming macro), serial codec/reservation/zero-counter fixtures,
six byte-identical exchange-reader/ACE body checks, and a private mixed-object
PW link with resolved dynamic libraries. Maximum observed child compile/link RSS
was **183,488 KiB**; it is not a PW or aggregate-MPI memory bound.

The native-like files in transaction tests are expressly **synthetic stand-ins**.
They do not validate QE XML/HDF5 parsing, actual MPI rank failure, native EXX
action/energy/ACE identity, whole SCF continuation or physical material accuracy.
Native qualification stays false. See [closure and boundaries](closure_and_boundaries.md)
and [decision](decision.md).

Final measured free disk: **30.259 GiB**; available physical RAM: **29.658 GiB**.
The nominal 22-GiB stream plus 10-GiB reserve already exceeds free disk, before
state/native output. No such file is allocated. Stock QE, previous private PW,
dirty DFT status and all 17 protected source/supervisor/PP pins remain identical.

## Reproduction

Use the existing private toolchain and pinned source specified in
`patch_native_bridge.py`. From MCT:

```bash
python3 research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/native_bridge/build_checks.py
python3 research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/native_bridge/final_checks.py
```

These commands compile/link and execute tiny serial tests only. Neither launches
PW/MPI. Generated sources and binaries stay under DFT
`.local/qe75_lowram_20261011/native_bridge`; the old private source/tree and binary
are preserved. The build report records the exact generated source directory.

The review diff is encoded in `native_hooks.patch.json` to preserve upstream
whitespace exactly. Use the patch generator for reproducible private copies;
do not replace the installed stock executable. [Handoff](handoff_ledger.md).
