# Finite engineering decision — 2026-10-13

**PASS SOFTWARE; NATIVE EXECUTION HARD_BLOCKED.** Starting clean `9a58846`,
three distinct useful workstreams advanced; no global inventory fishing or
native QE/HSE/MPI execution occurred. Old sources, binaries, dirty DFT files,
supervisors, sessions, physical inputs and the historical goal are preserved.

1. **TESTED COUNTEREXAMPLE / FIX:** an authenticated malformed unsigned wire
   status >=2^31 becomes negative in the old C cast. Old `MPI_MAX` reduction
   can mask that error with another rank's zero. Live **serial** kernel ABI
   tests reproduce negative results for 0x80000000 and 0xffffffff. Patched C
   refuses as EPROTO; native Fortran reduces `MERGE(1,0,code/=0)`, preserving
   all nonzero failures including INT_MIN without ABS overflow. Normal zero,
   errno and native-scope refusal semantics pass. Eight serial decision traces
   plus the wire tests pass (three focused methods). The counterexample is
   malformed protocol data, not evidence of any previously executed MPI job.
2. **PASS COMPILE / SERIAL REAL-TYPE CODEC:** a versioned, labelled rank FFT
   observer captures dense/smooth/Fock dimensions, process coordinates, local
   workspace/partition and directional G maps. The hook is after real FFT
   construction and before large EXX gather/exxbuff allocation. Local I/O
   errors take the same normalized world collective; no partial packet passes.
   Both native modes compile. Six serial codec/refusal tests use the real QE
   descriptor type, including unequal local extents and equal-volume/different
   G-map counterexample. They grant no authority. Actual MPI behavior/descriptor
   remains UNKNOWN; a valid file alone is not an authenticated rank receipt.
3. **SOURCE-CONDITIONED RESOURCE CORRECTIONS:** complete required-term ledger
   and checked expressions include Miller HDF5 data, compact-map/gather
   lifetimes, RAM-versus-disk mixing histories and explicit backend/log/cache
   terms. Four expression/refusal tests and four tiny pristine-qeh5 schema
   checks pass with MPI-init trapped. No unproved HDF5/backend overhead is
   inserted. The **whole** output/RSS envelope remains unqualified; see
   `resource_ledger.md` for exact closed and UNKNOWN terms.
   The omitted `disk_io` selects **RAM** buffering for SCF. Mix history remains
   in RAM alongside df/dv, and `close_buffer(keep)` dumps it to disk before
   freeing it. This source finding changes both RSS and stop-path accounting;
   no input setting was changed to avoid the cost.

Both new private candidates link the status fix and observer, with exactly one
definition of each intended symbol and the same retained FFT/MPI/backend
fingerprints. They preserve the common-wave/readback and EXX/ACE diagnostics
already built at `9a58846`. They are **unexecuted/unadmitted**:

- stock/control: `625cae4eba225d9615b3403868fbff9ac2a4a72b35e5e0aa45352c3af5b67b35`
- streamed: `64f1a8e9030200fd15c8858262b181cacc864e5d7199b38340671c43ab1a9784`

Private artifacts: DFT `.local/qe75_lowram_20261011/native_envelope_20261013/`.
No DFT commit, stock overwrite, full run, altered HSE/SOC/352-band target,
native restart claim or physical x_c claim.

**STOP this bounded phase at the remaining evidence boundary.** The independently
useful source/codec/transport/producer fixes requested here are implemented.
Remaining admission needs the host-wide live inventory-and-exclusion certificate,
complete producer/generation/backend resource certification, and admitted native
common-state/MPI/SCF readback observations. The new observer is ready to acquire
one of those observations later; it cannot certify its own absent output. More
synthetic cases or familiar process names would not retire these gates.
`ownership_alternatives.md` identifies viable conditional ownership designs
without pretending any of them satisfies missing host-wide evidence.
