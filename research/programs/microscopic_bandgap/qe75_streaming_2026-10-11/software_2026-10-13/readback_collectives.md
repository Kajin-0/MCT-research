# Source-level initial readback and collective failure boundary

The new read-only 48-band observation codec now has a native-encoded reader.
It opens old data read-only; compares exact extent, version/endianness, common input ID,
rank/k, caller-provided shapes, physical Miller labels, FFT layout and k bits
before reading arrays. It refuses nonfinite fields and noncanonical padding.
Only the expected layout/Miller metadata is temporarily copied. Wave and
density data are read by columns into existing arrays, with no q-store copy.

**Critical failure semantics:** metadata rejection precedes payload mutation.
A later I/O/nonfinite failure returns a nonzero status; partially read arrays
are unusable. This is not an atomic in-place SCF restoration transaction.
The reader is a serial readback/check component, not a replacement for retained
M3b's full state/import proof or native-file transaction. It is not wired into
SCF to make a failed read resumable. A future caller must jointly refuse every
nonzero status and cannot take a successful rank as authority for all peers.

Independent tests use one mode's writer and both modes' reader. They check all
constructed 48-band wave/density/et/wg fields and reject corrupted fingerprint,
Miller/FFT maps, extent, NaN and padding. Both real-QE initial-capture objects compile and link into new private
unexecuted/unadmitted candidates with matching retained FFT/MPI backends; pristine RNG/default and common-state tests are repeated after
the codec change. No native initial state or material number is generated.

## Actual-source collective decision checks, without MPI

The unchanged `m5_readiness/native_lease.f90` is compiled separately against
explicit **serial decision stubs**, whose binary does not link MPI. Ten traces
cover both world-rank identities: success, a remote registration refusal, a
remote all-rank-check refusal, a local lease refusal and incompatible world size.
They confirm that positive failures reduce before the corresponding barrier
and error path, and that both ranks take the prescribed refusal. Stub results
are explicitly printed as NO_AUTHORITY; they never impersonate a live kernel
lease, launch job, native receipt or real communicator.

This retires a **source/decision-model** test gap, not the real collective gate.
For actual `mp_max` semantics, every participant must reach the same collective
on the same communicator and in the same order. The capture hook's per-k loop
requires the scoped one pool/group and identical local k counts. An absent,
crashed or stuck rank breaks the participation premise; serial maximum algebra
does not supply MPI liveness. Retained foreground timeout/pidfd cleanup is the
separate recovery mechanism. Actual distributed scatter, both native SCF stop
paths, old/current ACE distinction and native restart remain NOT RUN.

## Remaining boundary after independent software progression

The safe queue has produced three testable software checkpoints, rather than
stopping at unreadable maps. The unresolved acceptance observations now require
native execution or independent external admission evidence: common native
48-band packets and true maps, real collectives/SCF restore, complete native
HDF5/file lifetime/backend peak and EXX/ACE equivalence. Strict foreign inventory
remains HARD_BLOCKED. None of these can be established by relabelling the
44-band save, serial stubs, a guessed output allowance or source compilation.

No native scope, native fixture retry, full-size job, empirical gap fit,
supervisor/session change or historical-goal resume is issued. Another source
description of these same missing observations would not pass a new native
gate. Stop at this cross-workstream observation boundary, with these bounded
source/serial results retained. This does not prove all possible future software
development exhausted. The next necessary input is an
authoritative permission-compatible admission domain, followed by genuine
matched native observations under every original guard; not a Boolean waiver.
