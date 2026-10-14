# Prospective terminal FD ownership rule

**2026-10-14.** This is a new software scope following local checkpoint
`89922a7`. It changes no frozen historical file, scientific threshold, exchange
arithmetic or physical input. The old native FD refusal has no pidfd-poll sample
at its failing syscall. Its cause remains OPEN.

## Identity acquisition

A fresh connected Unix peer must pass the existing typed JOB/PROFILE, nonce,
kernel UID/cgroup, registered world rank, ELF/argv, lineage and live lease checks.
The new owner additionally obtains its socket-bound `SO_PEERPIDFD`, checks that
it is live, opens a process pidfd with flags zero, checks the proc start identity,
and checks the socket-bound pidfd remains live after the numeric acquisition.
Unsupported socket pidfd, permission denial or any uncertainty refuses.

**PROVEN UNDER KERNEL/TRANSPORT ASSUMPTIONS:** termination of the pinned socket
peer is irreversible. If its pidfd is still live at the end of this interval,
the original task lived throughout acquisition; its numeric PID was unavailable
for reuse during the numeric `pidfd_open`. Later authority follows that retained
descriptor, not a new lookup of a missing PID. Fresh rank sockets are required:
an inherited socket is not its child's identity. The fixed native lease client
creates and connects its own socket on each call; no ABI change is needed.
Descriptor reuse, foreign kernel identity and mismatched registration refuse.

Process pidfds without `PIDFD_THREAD` become readable only after the last thread
exits; the retained descriptor reports hangup after reaping. These semantics are
documented by the [Linux pidfd manual](https://man7.org/linux/man-pages/man2/pidfd_open.2.html).
This is established Linux behavior, not a research novelty claim.

## Active → pending → accepted terminal transition

1. Normal active FD/inode/block accounting and all existing resource guards
   remain mandatory. Whole-task FD disappearance, EACCES or ENODEV cannot be
   excused by `Z`, exit status, logged success or a now-missing PID.
2. If FD enumeration fails, BOTH final phase-10 records must have been received
   from the actual live registered tasks in this invocation, after numerical
   post-punch/readback validation. No deserialized historical JSON or Boolean
   can create a final receipt. The particular denied task's pinned pidfd must
   prove exit. A still-live task always refuses, even after both final records.
3. The only permitted response at this point is **TERMINAL_PENDING**, not a
   successful sample or FD omission. The owner ceases numerical grants and has
   at most three seconds, also bounded by the original 600-second deadline, to
   obtain the complete terminal conjunction. Kernel hard caps, host RAM/disk,
   retained-tree/output, log and sampled RSS checks continue. Tree-only samples
   during pending are explicitly incomplete FD inventories; they grant no
   acceptance. Cancellation and any resource failure refuse.
4. BOTH pinned process pidfds must prove exit; the foreground manager wait must
   return zero. A retained manager query must match the original unit and
   invocation, loaded/inactive/dead, `Result=success`, `ExecMainCode=CLD_EXITED`,
   `ExecMainStatus=0`, `MainPID=0`, no restart/delegation. The original cgroup
   must be absent or have its original inode, populated zero, and no members
   including descendants. Absent group alone is insufficient. A final complete
   retained-tree account must still satisfy the original aggregate budget.
5. Only this conjunction permits omission of the retired task's FD inventory.
   A dead task cannot produce new writes. Under the fixed closed-family source
   assumption, an empty group contains no surviving family writer retaining
   shared file descriptions. Retained generations remain counted by their
   paths/inodes; the accepted sampled-domain external-writer/burst risks remain.
   This proves neither a continuous disk quota nor absence of foreign MPI.

The owner retains a connection-local `RefUnit` before releasing the launcher,
preventing manager metadata collection until terminal evidence is recorded.
Closing that connection releases the reference. No unit property/global changes
are needed. See the [systemd manager API](https://www.man7.org/linux/man-pages/man5/org.freedesktop.systemd1.5.html).
`RemainAfterExit` was considered and rejected: its documented incompatibility
with the existing `--pipe/--wait` path would change the runner's semantics.
See [systemd-run](https://man7.org/linux/man-pages/man1/systemd-run.1.html).

## Integration status and remaining gates

`retirement.py` implements the identity/receipt/terminal predicates. The new
`sampled_output.py` and `owned_pair.py` are **prospective source copies**, with
reviewable patches against the frozen rooted owner. They wire authenticated
receipts before reply, strict FD failure delegation, bounded pending wait and
mandatory terminal proof for every native acceptance path. Whole-task missing
or denied FD inventories of unregistered actors still refuse. Individual file
close/unlink races retain the previous sampled-domain limits, not a continuous
inventory theorem.

The candidate CLI explicitly refuses native release. Package assembly, fresh
JOB/PROFILE/seed/deck pins, final production integration and its prospective
freeze are not issued by these tests. No build or native execution occurred in
this phase. Original numerical tolerances are independently checked identical.
Any future policy must keep 12 GiB/swap-zero/tasks-12/600 seconds per member,
4 GiB host RAM, 10 GiB disk and 14 GiB sampled aggregate output, fresh states,
two local ranks, one family, complete actual FFT/readback and cleanup gates.
No old refused control is automatically adopted as a new accepted member.

Publication of the prior scientific checkpoint is presently blocked by ordinary
Git authentication. This phase therefore stops at tested non-MPI owner mechanics
and prospective integration, without creating a fresh native work queue.
