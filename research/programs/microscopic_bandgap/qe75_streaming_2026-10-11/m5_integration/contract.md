# Finite production-transport integration contract

Starting revision `6b5fc5e`, existing research branch. This package implements
one new gate and ends at the first unpassed native admission prerequisite.
It never launches a QE executable, MPI launcher or communicator.

## What changed

The existing M4 foreground owner/guardian now dispatches the native C client's
180-byte `R07L` packets on its actual leased socket. Version-2 JOBs bind a
separate PROFILE digest; the ticket and C environment carry both. The original
version-1 fake-worker JSON path, pidfd cleanup, subreaper, lifeline, crash fence,
flock, 64-bit extents, quota/block reservations and sampled limits are retained.

The production adapter uses the previously tested `RankRegistry`, not a second
independent rank registry. Kernel SO_PEERCRED, executable hash and observed
pidfd lineage establish a unique process for each rank. CHECK succeeds only
with both registered identities live. A child-hook RPC requires both digests,
the exact script/interpreter and a currently pinned lineage ending at an actual
registered C process. Merely being another child of the owned launcher fails.
The receipt includes guardian and launcher PID/start-ticks, rank ancestor,
owner, both digests and fresh measured resources. The client rechecks the live
kernel lock/guardian and nonce before returning it.

The native bridge now consumes this typed live-RPC interface and requires scope
2 plus agreement between its independently found executable ancestor and the
receipt's registered native PID. **The only issued scope remains 1, ABI_NO_MPI.**
The production guardian admits only the exact small serial transport fixture;
native JOB validation still calls the explicit unissued native-admission gate.
No native scope, native Python-hook allowlist, real MPI collective or checkpoint
publication is qualified by this package. The serial hook tests the transport
and ancestry path; it does not call native publication under fabricated scope.

## Independent tests and resource interpretation

The retained C lease client is compiled unchanged with a tiny serial worker.
Its dynamic dependencies are libc and the loader, not MPI/QE/FFT. Two real
workers use the production guardian, which makes actual 192-byte per-rank
extents and a 262,144-byte output escrow under the existing ext4/quota policy.
All other job files, output and logs are charged to the separate envelope.
No nominal 22-GiB file is allocated or copied.

Failures include changed JOB/PROFILE digests, wrong guardian start-ticks,
duplicate ranks, dead registered ranks, native-scope demand, an unregistered
launcher child, an outside-family requester, malformed wire input, timeout,
owner kill and guardian kill. Successful cleanup is verified with live identity
checks and the released kernel lease. Old M4 lifecycle/resource tests and the
affected bridge/client refusal tests are rerun sequentially. Tests do not
certify MPI barriers or native HSE state/action equivalence.

The 12-GiB RSS ceiling, 4-GiB MemAvailable floor, 10-GiB disk floor and >=600-s
deadline refusal remain sampled stop predicates, not continuous cgroup bounds.
Summed RSS includes shared-page overcount; PSS and RSS-minus-PSS indicators are
retained. Test-specific limits are tighter (256-MiB RSS, seconds of wall time).
The unchanged parent-death/crash fence is cooperative owned-family control,
not authority to kill or inspect arbitrary foreign processes.

## First native blocker and negative inference

The first retained inventory snapshot has 32 unreadable live mappings, versus
36 in the preceding phase. They include PID 1, system/service UIDs and three
same-UID processes. The current process has no effective capabilities and
`ptrace_scope=1`; mapping and executable-link reads return EACCES. These are
permission observations, not a proof of a single cause for each denial. No
permission, system setting, session or unrelated process is changed.

`comm`, UID and readable process statistics can bind an identity but cannot
exclude an unseen MPI library. Two processes with identical exposed metadata
can differ in their unreadable mappings; a renamed program or a process that
loads MPI later defeats inference from a harmless name. The guardian's exclusive
flock proves exclusion of cooperating owners only. Its sound control over its
own descendants does not prove host-wide exclusion. Hence the strict inventory
check correctly returns UNKNOWN_REFUSE at PID 1. A readable snapshot alone
would also not prove continuous exclusion without an enforced admission domain.

**Stop:** no native fixture is admitted. The next necessary input is a
permission-compatible, authoritative foreign-family inventory/admission-domain
certificate covering these unreadable live identities. A list of familiar
service names or an `all_clear=true` file is insufficient. This package does
not acquire that certificate, change permissions or substitute a weaker policy.

Actual two-rank MPI/FFT layout, native output/peak envelope, both stop/readback
paths and a common 48-band/k2/Fock120Ry initial-wave certificate remain unpassed.
The 44-band/k4/Fock180Ry save is still incompatible. No seed is relabelled,
no original 352-band setting changes, and no direct-versus-ACE equality outside
the interpolation span is asserted. Existing diagnostic and serial readback
evidence stays conditional; there are no new EXX/energy/Gram/material numbers.

## Reproduction

From `/home/User/opencode_workspace/DFT`, after `source scripts/env.sh`:

```bash
python /home/User/repos/MCT-research/research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/m5_integration/validate.py
```

This rebuilds only the tiny libc worker and runs finite serial production-path
tests. It retains the original first inventory evidence, checks protected DFT
pins/status/stock/private candidates/sessions and never executes native QE.
Private binary and fresh preservation snapshot are retained under
`.local/qe75_lowram_20261011/m5_integration/`; repository evidence contains their
hashes and commands, not ignored binaries. Do not reset unknown leases, create
a queue, launch a fixture or resume the historical blocked goal from this file.
