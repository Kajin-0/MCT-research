# Bounded NON-MPI namespace-cookie investigation

2026-10-13, starts clean `9fdfdaa`; original branch/session/blocked goal retained.
First read EXECUTION_PLAN, prior local protocol/decision, cgroup decision and
DFT AGENTS. No MPI, QE, HSE, queues, new sessions, permissions/global changes.

One fixed compiled C service, no arbitrary command. PrivateUsers/PrivateNetwork,
64MiB memory.max, swap0, tasks4, no restart, whole-group OOM/kill, 8s manager
runtime plus 1s stop, bounded foreground controller, 32KiB pipe capture, 16KiB
per-file/core0/nofile64. Independent host MemAvailable>=4GiB/disk>=10GiB;
actual ext4/quota admission and one synced byte/block-checked 4096-byte extent.
All protected states/pins and the old lease ledger must remain exact.

Probe creates sockets **inside** the running service and never connects any
IP socket. Reject any inherited socket before measuring self. Three newly
created AF_INET sockets must yield the same nonzero 64-bit SO_NETNS_COOKIE;
independent fresh host sockets before/during/after must agree with each other
and differ from service cookies. Enumerate real interfaces/addresses/flags,
requiring only lo, UP+LOOPBACK and only loopback addresses. No stat-inode
fallback or unsupported getter interpreted as success.

A short private pathname Unix endpoint connects across namespaces. Bind the
exchange to JOB/PROFILE digests, live kernel peer credentials/pidfds/start
ticks, manager InvocationID/MainPID, actual cgroup and limits, a fresh challenge,
exact non-MPI receipt type, and the original exclusive cooperating-owner flock.
Transferred regular lease fd is not network identity. Record fresh client vs
accepted host socket cookies separately; the accepted endpoint must never be
used as the peer's self-namespace cookie.

At most one healthy unit plus two predetermined non-MPI negative units
(corrupted nonce and owner-channel EOF) if the healthy observation passes.
Stop a failed/unsafe positive attempt; only a concrete source defect may receive
one bounded correction. Unit/owner/PID/receipt/resource unknowns refuse admission.
Negative tests must really refuse and clean up, not count nonzero exit alone.
No native MPI attempt is scheduled by this package.

Assess remaining full-runtime bounds independently. Namespace/IPC component
success must not retire untested MPI rank/descendant registration, exact
producer/output budgets, production live issuer, state/FFT/readback or original
strict host-wide exclusion. Explicitly retain continuous-host-floor limitations.
