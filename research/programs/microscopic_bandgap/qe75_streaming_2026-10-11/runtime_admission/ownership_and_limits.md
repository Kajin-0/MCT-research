# Process identity, lease and resource contract

## Authority and lifetime

The runner is a dedicated foreground Python owner with no inherited unrelated
children. Its child monitor holds `.local/qe75_lowram_20261011/runtime_admission/
MPI_FAMILY.lock` using nonblocking exclusive flock. Workers do not inherit the
lock descriptor. The owner and monitor both install child-subreaper semantics;
the monitor also watches a socket lifeline and receives a parent-death signal.
The launcher exec stub gets a parent-death signal. No persistent detached
supervisor, tmux session or Codex process is created.

Discovery starts from actual `/proc` parent links. A candidate descendant is
bound to a pidfd, and the complete observed ancestry is checked against start
ticks and parent links before it becomes signal authority. A racing snapshot
remains unresolved, is retried and cannot count as verified cleanup. Reused PID
identities retire instead of retargeting. TERM/KILL always use
`pidfd_send_signal`, never a numeric PID, PGID, argv match or environment token.
No unrelated process may be signalled based on the MPI inventory.

An abstract local SOCK_SEQPACKET endpoint supplies a live receipt. Client and
monitor verify kernel SO_PEERCRED, UID, process start ticks, current kernel flock
owner, source/interpreter fingerprints, canonical JOB digest and fresh random
challenge. Both registered ranks must still be alive. Fake rank indices must
match the fixed hashed launch arguments. A native rank index must instead come
from compiled MPI communicator state; that adapter is missing. A JSON file or
Boolean is never sufficient authority. The endpoint file locates the server;
it does not grant a lease. The native bridge's former file-receipt path is fenced
behind the live API; no native receipt is currently issuable.

Normal cancellation closes the owner lifeline; the monitor sends TERM, then
pidfd KILL after 0.2 s, and checks/reaps for at most 3 s. Owner SIGKILL leaves the
monitor holding the lease until cleanup. Monitor SIGKILL causes owner-sub-reaper
fallback. Session-detaching/double-fork descendants are still owned through
subreaper adoption; parent-death signalling alone is not the proof.

Before any worker is spawned, a fsynced/atomic global INITIALIZING ledger is
written. Unexpected dual owner/monitor death releases the kernel lock but leaves
this or RUNNING evidence; the next owner refuses it. FINISHED is published only
after no live or unresolved owned descendants remain. Unkillable processes,
unreadable process state, kernel/system failure, or concurrent hostile same-UID
tampering are not solved by these tests. This is a cooperative scientific-job
ownership protocol, not a security boundary against a privileged adversary.

The kernel identities/locking/subreaper semantics are established Linux APIs:
[pidfd signals](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/pidfd_send_signal.2),
[flock](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/flock.2),
[prctl](https://raw.githubusercontent.com/mkerrisk/man-pages/master/man2/prctl.2).
The project-specific composition and failure handling are what the tests assess.

## Resource guard and reservations

Retained native policy is 12 GiB summed family RSS maximum, 4 GiB minimum
MemAvailable, 10 GiB minimum physical free disk and stop at monotonic elapsed
>=600 s. The guard includes the owner, monitor and witnessed workers. RSS is a
conservative sum with shared-page duplication; PSS is diagnostic and never
substituted to loosen admission. Fake tests enforce stricter 256-MiB / short-wall
caps and independently check exact 600-s and memory/disk predicate boundaries.
They do not run for 600 s or approach 12 GiB.

The nominal sampling delay is 20 ms; IPC handling and real I/O add latency. This
is a sampled abort policy, not a cgroup hard ceiling or proof that no transient
overshoot can occur. Cleanup time is reported separately through the total
elapsed result. Disk/RAM changes by other jobs, blocked kernel I/O and abrupt
system failure can defeat instantaneous guarantees; failure remains a refusal,
not a successful run. Native admission is absent, so this limit is not promoted
to a full-HSE resource certificate.

Rank complex-DP extents are `16*R*band*q`, with every multiplication checked in
signed 64 bits and every extent block-rounded independently. Existing M3 guard
code requires local ext4, complete user/group/project quota status and sufficient
soft/hard headroom without grace. Unknown quota or tmpfs refuses. Each owned new
O_EXCL/O_NOFOLLOW inode gets actual 64-bit fallocate, fdatasync and allocated-block
verification. Rollback touches only matching newly created, still-open inodes;
colliding/foreign files survive. No whole stream is copied or hashed in memory.

For tiny workers the two 192-byte files and 32768-byte escrow allocate 40960
physical bytes. Admission additionally charges 32768 future-output bytes, for
73728 bytes plus the 10-GiB reserve. Escrow is not permission to spend those bytes
twice. All files under the owned job, including logs and metadata, are counted
against the output envelope except the already reserved matching inodes. The
global lease/ledger has small control metadata outside this job budget. Real
native stream/state/output extents and rank layouts are still missing. Fake
reservation inodes are removed only with their unique test directories; no
existing scientific scratch or supervisory file is cleaned.

## Qualification boundary and falsification

The strict native input whitelist accepts only exact preregistered text and
hashes. Changes to bands, functional, cutoffs, k/q, atom count, solver accuracy,
ambiguous duplicate controls and even unregistered extra text refuse. Native
control and stream sources/backends are pinned; passive ELF dependency tracing
does not run PW or initialize MPI. Native FFT/rank layout and common waves cannot
be inferred from those pins.

Readable process inventory detects known MPI/PW executable names and renamed
processes with readable MPI-library mappings. Some pre-existing mappings are
unreadable. Fake-only tests explicitly permit this limited inventory because
their command cannot invoke MPI. Strict native inventory returns UNKNOWN/refuses;
renaming an unreadable foreign MPI process cannot be ruled out. No global lease
can compel unrelated launchers that do not participate in this protocol.

Native admission requires compiled per-rank registration, bridge PROFILE/JOB
binding, exact layout/output bounds, common initial state, direct EXX/ACE/energy
and restart readback instruments, complete ownership evidence and all retained
guards. Fake receipts, source compilation and identical dynamic libraries do not
meet these conditions. A mismatch, resource stop or unreadable prerequisite
stops before any speculative native launch or retry.
