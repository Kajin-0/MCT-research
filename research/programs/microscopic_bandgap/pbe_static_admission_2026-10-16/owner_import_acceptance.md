# Narrow owner/import acceptance — components PASS, production NO-GO

The original unshared guard failed on unbound/incomplete FD inventory at4.0203s,
with BOTH registered rank pidfds reported false for exit. Affected PID, syscall
errno and instantaneous identity were not retained, so a teardown explanation
is UNPROVEN. JOBDONE and readback numbers do not repair that refusal. Shared
was withheld; the new scope must acquire BOTH members afresh if later released.

Exact old call path: static_environment/owner.py constructs Account inherited
from terminal_owner/SingleMemberAccount, but supplies NO retirement object.
sample(active_pids) raises OutputRefusal on whole-task /proc/FD denial. The
owner's catch retries only after some pinned task exits; it does not establish
the required complete terminal conjunction. It records no native final-live
receipt. The diagnostic run driver has no native lease/completion hook. Do not
simply skip unreadable tasks, wait for a live-denied task to die and retropass,
accept a Z flag, or infer rank completion from a file/JOBDONE.

Minimum PROSPECTIVE fix, keeping the old experiment immutable:

1. Fresh scope/root/unit/invocation and typed PROFILE/JOB/nonce. Retain manager
   RefUnit. Bind actual rank kernel UID/cgroup/process identity through fresh
   socket-bound SO_PEERPIDFD, then a process pidfd(flags0), with live bracketing,
   start identity and descriptor identity. An inherited socket is not self ID.
   Observe the pinned native ELF/argv after exec; a claimed hash alone is not
   observation. Pin the owned launcher as a direct child BEFORE any poll/reap;
   all other cgroup actors need their own identity/complete live FD inventory.
2. Add the smallest diagnostic native final hook after both completed packet
   writes/close and collective completion, before rank exit. It must send live
   typed completion from the SAME registered native PID/start/cgroup/ELF and
   invocation, with packet extent/provenance/readback gating; BOTH ranks are
   required. Reuse established live-lease machinery only through a NEW scoped
   profile, not a transplanted HSE/48band authorization. The currently pinned
   PBE binary does NOT contain this hook. A separately built/tested private
   diagnostic is required; exchange/SCF arithmetic need not change.
3. Denied FD inventory of a still-live pinned rank ALWAYS refuses, even after
   both final receipts. Unknown tasks, output paths, inode/overflow errors or
   missing identities refuse. ONLY the PARTICULAR denied task's kernel-proved
   death plus both prior live final receipts permits TERMINAL_PENDING, never
   a successful incomplete FD sample. Log PID/start/pidfd mask, errno and path.
   Refusal is absorbing for that acquisition: later exit cannot resurrect it.
4. Pending is bounded by3s AND remaining600s; no new work grants. Keep hard
   caps, host pressure, live remaining actors' FDs and retained-block/inode/tree
   accounting active. Numeric/PID disappearance or zombie text alone is not
   retirement. Require both rank pidfds exited, foreground wait0, same retained
   unit/invocation loaded/inactive/dead/exit0/no restart/no delegation, original
   cgroup absent OR same inode/populated0/no descendants. A failed manager or
   live/missing writer prevents acceptance; final complete aggregate accounting
   must still pass. An outside foreground holder verifies after guardian exit.
5. The new reader is imported in a CLEAN subprocess BEFORE any launch; import
   paths/dependencies are pinned explicitly. No AST-only or warm sys.modules
   check. Old refused roots are rejected. All native source/PP/save/deck/ELF
   and cgroup/lease/resource gates remain mandatory for every member.

**What actually passed here:** bounded scratch-only NON-MPI Python children
created their own sockets. Kernel-bound registration/final pairs, real live
EACCES via only the disposable child's dumpability, actual pidfd exits and
descriptor reuse were tested. Live denial refused. Fake success, bool wire
tags, wrong job, duplicate/different actor, PID-start injection, unknown output,
single-live-rank, failed/mismatched manager, unknown/reused/populated cgroup
and resource-boundary models refused. No service or real new manager/empty
cgroup was created. Model conjunction success is explicitly NOT native
authority. Complete production caller/native hook wiring is NOT qualified.
The modeled Attempt latch remains refused after a live-denied child actually
exits. Other positive/negative predicate branches are independent tests, not
continued eligibility of that failed attempt. Production must wire that latch
through every active gate; testing predicates alone does not supply the caller.

**Importer PASS, limited precisely:** the original missing `packets` import
reproduces in an isolated interpreter. Prospective readback loads an explicitly
pinned minimal Reader module, AST-identical to the existing bounded Reader
class, avoiding unrelated DFT/HSE imports. Missing/corrupt dependency injections
fail before execution. The old packet is decoded ONLY as an unqualified format
fixture; no old validate/science/owner result is rerun or accepted. Proposed
validate refuses old roots. No native profile/readback acceptance is issued.

Kernel exit semantics are established
[pidfd behavior](https://man7.org/linux/man-pages/man2/pidfd_open.2.html), not a
new result. Without PIDFD_THREAD, readiness means the last thread exited;
retained descriptors avoid retargeting a recycled numeric PID. That proves
retirement of THAT process, not absence of descendants or foreign MPI.
No global process inventory/private-network proof is claimed. Original sampled
output limits retain between-sample burst/external-writer and metadata-allowance
limitations; RLIMIT_FSIZE remains per file, never an aggregate quota.

**STOP source/owner qualification here:** the exact production final hook and
caller are absent from the pinned PBE executable/owner. Offline component
tests cannot substitute for that integration. No new native/service/build
was attempted; no HSE infrastructure was continued.
