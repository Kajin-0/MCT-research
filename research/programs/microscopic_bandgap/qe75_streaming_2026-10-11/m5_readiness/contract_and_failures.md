# Readiness contract, exact bounds and retained failures

## Typed identity and native adapter

JOB version 2 / binding version 1 carries the SHA256 of the canonical PROFILE;
JOB's own canonical SHA256 is separate. Both are sent in a fixed 180-byte,
network-endian request with version, operation, world rank/size and a 32-byte
random challenge. The 48-byte response echoes that challenge, status and explicit
authority scope. The compiled client verifies kernel peer UID/PID/start ticks,
live pidfd and actual flock owner before and after the response. It does not
trust a Boolean or stale JSON receipt. Socket waits and retries are bounded.

The native Fortran adapter takes `mpime,nproc,world_comm` from pinned QE
`mp_world`, not argv or rank environment variables. Register, mp_max error
propagation, barrier and all-rank recheck occur before `iosys` or native checkpoint
read. The source is compiled against the real installed QE modules in both
private modes. Its collective semantics have not been executed; a missing peer
must still fail/abort under the M4 owner if MPI collective progress stalls.

Serial component peers use explicit `ABI_NO_MPI` scope. Native QE requires
`NATIVE` scope; the component server cannot supply it. The production M4
guardian currently understands its old fake-worker JSON protocol, not these
native binary packets. A future native dispatcher, live per-rank executable
pinning, bridge-child-to-registered-rank ancestry and JOB/PROFILE receipt binding
remain necessary. `native_admission()` deliberately refuses until those and all
other retained gates are evidenced. There is no native launch path in this package.

This protocol assumes cooperative owned code/files and kernel identity semantics;
it is not protection against arbitrary privileged or same-UID malicious code.
Unreadable maps are enumerated as UNKNOWN. No UID exemption, privilege change,
inferred harmless process or fabricated exclusivity certificate is introduced.

## First-ACE capture and observability

The two private modes have identical diagnostic hooks. Each local k point is
captured only on its first `aceinit_k` call. The adapter records actual reciprocal
index/FFT/G maps, current Phi, raw direct V-Phi, Gram and native weighted energy,
old source occupations, a globally normalized deterministic G-index/spin/k probe
and its direct action. After native `aceupdate_k` it records factor/xi and the
native ACE action on that same probe, restoring the prior `domat` flag afterward.
New arrays are bounded to the separately approved 48-band small fixture. The
original 16-atom/352-band decks and previous binaries remain untouched.

Full-band probe/direct scratch is retained because `vexx_k` declares an explicit
`max_ibands` dummy extent even for `m=1`; a compact one-column actual could violate
that array contract. The native probe uses only column one. Serialization writes
existing columns instead of copying the q store or whole Phi/xi arrays.

Direct exchange, exchange-energy, ACE-update and ACE-application bodies remain
byte-identical to M3b. The extra probe calls touch normal exchange scratch/cache
and timing state; source equality alone does not establish run-time
noninterference or quantitative agreement. That remains an actual matched-fixture
gate. Direct and ACE action comparisons must be kept separate; ACE's subspace
exactness does not imply arbitrary-probe equality. No native diagnostic number
appears in the synthetic codec tests.

## Exact conditional component extents

Let `R=npwx*npol`, `B=nbnd`, `K=nks`, `Nt=nkstot`, `L=layout integers`,
`n=npw`, `F=actual padded local FFT rows including spin`, `Q=stored q count`.
All arithmetic below is signed-64 checked and refuses nonpositive/incompatible
shapes or overflow. Native interpretation requires an independently certified
actual descriptor, not a synthetic dimension substituted for it.

- Stream: `16 F B Q` bytes.
- Retained M3 rank state packet: `240 + 8L + 8B Nt + 16B K + 16R B K`.
- Each before/after diagnostic common header: `H=96+8L+8n`.
- Before per k: `H+16+8B Nt+32R B+16B²+32R`.
- After per k: `H+16R B+16B²+16R`.
- First-ACE diagnostic output per rank: `K*(before+after)`.
- Probe/direct/ACE scratch: `32R B+16R`, plus the actual layout/global-index arrays.

The two serial test captures are exactly 800 and 480 bytes, matching these
formulas. They do not bound the real fixture's `npwx`, local FFT padding, q-map
size, native HDF5 waves/ACE/density, mix history, XML/log output, checkpoint
generation lifetimes or allocator/FFT/MPI work buffers. Consequently the complete
output envelope and native peak RAM remain uncertified. An arbitrary 1-GiB or
similar envelope is not promoted to a proof. M4 ext4/quota reservation and
12/4/10-GiB/600-s guards remain mandatory, with their previously documented
sampling/cleanup limitations.

## Actual saved-data readback and incompatibility

The pristine pinned QE `Modules/qeh5_module.f90` is compiled separately as a
serial component. The driver uses QE's `initialize_hdf5/finalize_hdf5` and the same
complex-column hyperslabs used in `io_base`. An independent h5py path compares
every output payload byte for the inspected wave, ACE and density files, and
rechecks original file hashes afterward. This verifies 1,208,137 complex values
(19,330,192 payload bytes); it does not run `io_base`'s MPI scatter or resume SCF.

The inspected XML/save belongs to the existing 44-band k4/Fock180Ry calculation.
The small approved fixture is 48-band k2/Fock120Ry. Its wave basis, k selection,
empty-state coverage and prior SCF state cannot be inferred identical from these
files. No extra bands are fabricated and no existing seed is relabelled. The
readback result is I/O evidence, not material convergence or common-wave evidence.

Parallel-HDF5 transitively loads an MPI library. The serial decoder links explicit
exported refusal definitions for MPI/PMPI Init/Init_thread; their four stub paths
exit 97 in independent no-MPI self-tests. Successful decoding with these traps,
plus the serial default file-access path, provides bounded evidence of no MPI
initialization through these public entry points. It is not a universal assertion
about every hidden MPI API or a reason to ignore MPI-linked processes in the
inventory. No MPI launcher or real communicator is used.

## Retained software failures

1. Initial serial-component link lacked `infomsg`; a local driver stub resolves
   it. No stock source or library was patched.
2. The first driver omitted HDF5 initialization and incorrectly made native
   `errore(...,0)` fatal. Corrected to native status-zero semantics.
3. Calling only HDF5's generic initializer left QE's private REALDP/SP datatype
   handles unset; qeh5 could report read errors while the process exited zero
   and produced zero payloads. The exact-byte check rejected this. The driver
   now calls QE's proper initializer, and all three actual readbacks pass with
   stderr-empty and exact-byte checks. This was a harness defect, not evidence of
   defective stock QE or saved scientific data.
4. Compile warnings in the C client and refusal stub were corrected under
   `-Wall -Wextra -Werror`; final compiled wire/guard checks pass.

The initial private build failure is retained at
`DFT/.local/qe75_lowram_20261011/m5_readiness/build.first_failed.json`.
Final test/build/readback evidence is committed separately. These corrections
do not retire the actual MPI collective, common-state, full-output or inventory
no-go gates. No restart or quantitative storage equivalence is claimed.
