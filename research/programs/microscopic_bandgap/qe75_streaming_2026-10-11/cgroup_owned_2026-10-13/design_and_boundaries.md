# User-manager cgroup adapter: contract and boundaries

Starting clean `de000d4`, the new host evidence retires **one availability
obstruction**: UID1001's existing systemd user manager can create a bounded
cgroup-v2 family. It does not retire the independent host-wide exclusion
obstruction. Only tiny compiled non-MPI workers are executable in this package.

## Actual kernel/service binding

The foreground controller uses the existing `/run/user/1001/bus`, a unique
128-bit unit name, `Type=exec`, `Restart=no`, `Delegate=no`,
`KillMode=control-group`, `OOMPolicy=kill`, `MemorySwapMax=0`,
`NoNewPrivileges=yes`, `LimitCORE=0`, one-second stop timeout and an explicit
3/8-second manager runtime bound. Normal tests use MemoryMax=128 MiB;
one controlled allocation tests a 64-MiB group. TasksMax=16, file limit=128 KiB,
aggregate captured worker log cap=32 KiB. These are cheap engineering fixtures,
not the native 12-GiB/600-second profile or a downgrade of target physics.

Before releasing workers, **both** controller and guard match actual manager
MainPID, InvocationID, ControlGroup, transient properties and configured limits
against the JOB/PROFILE. The guard reports its kernel cgroup path/inode,
memory.max, memory.swap.max, pids.max and memory.oom.group; it checks actual
RLIMIT_FSIZE/CORE and NoNewPrivs. The owner uses kernel SO_PEERCRED and pidfds,
not a submitted Boolean. The kernel peer's interpreter, command and source/
executable allowlist are checked. A changed/missing field, source, digest,
limit, manager, invocation, cgroup or live owner refuses release.

The service connects to an abstract Unix lifeline (the project path exceeds
the pathname socket limit). MainPID has systemd as parent rather than the
foreground controller; the authenticated lifeline and actual unit identity
replace a false parent-lineage assumption. Only verified cgroup members are
read from /proc. No foreign mapping/process inventory is performed.

## Lease lifetime and compatibility with the existing owner

1. The guard obtains the existing `MPI_FAMILY.lock` before creating workers.
2. It sends a duplicate of that **same open file description** to the
   controller using SCM_RIGHTS. Controller checks fd device/inode and kernel
   flock holder against the authenticated guard pidfd identity.
3. Before a second live release, the controller durably records the previous
   closed legacy ledger bytes and a `CGROUP_RUNNING` marker. The existing
   legacy `stale_refusal` rejects that marker **before** its inventory call.
   No legacy source is changed. New-unit metadata is also durable.
4. Typed REGISTER/CHECK receipts bind JOB, PROFILE, two distinct compiled
   processes, guardian ancestry, kernel cgroup and invocation/inode. Scope is
   strictly ABI_NO_MPI. A native-scope client rejects those receipts.
5. On guard death the controller-held duplicate retains flock exclusion until
   the unit is verified empty/absent and all witnessed identities are retired.
   A separate flock attempt **after guard exit** independently confirms this.
6. On owner death, the guard's fd remains until its exit. The durable marker
   protects the gap after both fds close but before manager cleanup/recovery.
   Recovery requires the exact old invocation/cgroup inode, closure and retired
   identities, never just a dead client or released lock. The original legacy
   ledger is restored **byte-for-byte**, then the lease released.

Manager `control-group` cleanup covers detached setsid/fork descendants when
the main guard exits. A crashed owner leaves a failed transient unit until
verified recovery captures its result and resets **only that owned unit**.
No unit files, manager defaults, permissions, other units or supervisors are
changed. Native payload cannot be selected by an arbitrary command or flag.

Fork/exec descendants inherit cgroup membership; this is the required mechanism
for a future *local* MPI family. Remote/service-spawned/migrated ranks do not
inherit it and would need explicit refusal or a separate scope. **Actual MPI
descendants and distributed native collectives are NOT TESTED.** A same-UID
adversary can use the manager or writable delegation to migrate work; this is
a cooperative workload admission contract, not a hostile-user sandbox.
Unexpected identity/membership changes refuse. Name-to-invocation manager stop
checks do not constitute an atomic defense against malicious same-UID unit
replacement. None of these limits proves foreign MPI absence.

## Resource semantics

**memory.max is kernel-enforced cgroup accounting, not summed RSS.** It includes
anonymous/file/kernel charges and can temporarily exceed the configured limit
under documented kernel conditions. Reclaim or group OOM can terminate work;
it neither reserves that RAM nor guarantees numerical completion. Shared-RSS
overcount, foreground controller/systemd-run outside the cgroup, and system
MemAvailable remain separate. The original 12-GiB summed-RSS and 4-GiB
MemAvailable predicates are retained; tests independently report their sampled
RSS. The existing user manager/journal are shared services, not charged as
owned rank work. Original full native backend/output bounds remain unqualified.

TasksMax counts **tasks/threads** and enforces fork/clone refusal. External
migration can defeat a claim that observed pids.current always stays <=max;
the adapter does not perform migration and rejects unexpected membership.

RLIMIT_FSIZE is a hard **per-file** limit; captured stdout/stderr has an exact
aggregate sink cap. This is not an aggregate filesystem quota: many small
files, manager journal and unrelated writers remain outside that theorem.
The guard samples allocated owned inode blocks, one-MiB fixture envelope,
10-GiB free-disk floor and 4-GiB MemAvailable. Checked 64-bit per-rank extents
are actually fallocated, synced and byte/block verified using the retained
ext4/quota guard (two 4096-byte files). No large disk reservation is made.
No claim of continuously guaranteed host free disk is justified without
additional quota/reservation control and the complete native producer bound.

## Preserved negative discoveries

- Immediate `--collect` can remove the kernel group/event record before a
  sampler witnesses oom_group_kill. The first test correctly **failed** that
  evidence requirement; it observed memory peak=64 MiB and oom=1, but group
  kill count was not captured. Nonzero exit was insufficient.
- Failed-unit collection is now deferred until durable, invocation-specific
  manager Result/ExecMainStatus capture; then only our failed unit is reset.
  Controlled OOM yields `Result=oom-kill`, status 9, and complete cleanup. In
  the final full suite, oom_group_kill=1 was also sampled. Absence of a sampled
  counter is still labelled absence, not zero events.
- A cgroup can disappear between exists/read during legitimate collection.
  Losing that sample is allowed only if the entire group disappears; final
  closure/identity checks still decide success. A partially missing live
  interface remains a refusal.
- A tiny rank can exit before its partner's live CHECK. v1 fixture failure
  remains recorded and its compiled binary preserved. v2 adds explicit serial
  two-sided actor release after both CHECKs/readiness identities. This is
  **not MPI_Barrier**, and no native collective is inferred from it.
- A guard-only flock can release before group cleanup. SCM_RIGHTS fd escrow
  plus a durable legacy refusal marker closes that cooperating-owner gap.

## Primary references and dependency boundary

The tested manager is systemd **257.9-0ubuntu2.5**; UID1001, cgroup v2, active
user bus, delegated memory/pids controls, readable owned membership, pidfds,
SCM_RIGHTS/flock and local ext4/quota primitives are required. Bus/controller
failure refuses. New units remain foreground-observed, have kernel/manager
timeouts, and are collected; no detached long-lived supervisor is installed.

Primary references: [systemd v257 resource controls](https://raw.githubusercontent.com/systemd/systemd/v257/man/systemd.resource-control.xml),
[systemd v257 service/OOM policy](https://raw.githubusercontent.com/systemd/systemd/v257/man/systemd.service.xml),
[systemd v257 group cleanup](https://raw.githubusercontent.com/systemd/systemd/v257/man/systemd.kill.xml),
[Linux cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html).
These established mechanisms are not a scientific novelty or material result.
