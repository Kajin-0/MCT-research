# Cgroup owned-family engineering — finite decision

**PASS: kernel/user-manager and cooperating-owner integration on tiny non-MPI
workers. NATIVE QE/HSE/MPI ADMISSION REMAINS HARD_BLOCKED.** Starting clean
`de000d4`, no new session/agent/goal, global inventory scan, permissions or
global service configuration changes were made.

- Real systemd user unit verifies actual memory.max, swap.max, pids.max,
  memory.oom.group, per-file/core rlimits and invocation/cgroup identity.
- Live typed two-rank lease includes real peer creds/pidfds/ancestry, dual
  JOB/PROFILE, cgroup/invocation and exact source/executable whitelist.
- Kernel fork refusal, controlled group OOM, log/file caps, timeout,
  cancellation, guard/owner crashes, detached child cleanup, strict restart
  recovery and native-scope refusals tested. Full **13-method suite PASS**;
  **three final focused fd-escrow/crash checks PASS** after the independent
  post-guard-exit flock probe was added. Source conditions are labelled in
  `validation.json`; no real MPI collective is claimed.
- Controller retains the same flock description past guard death; double
  crash leaves a durable refusal marker. The original legacy launcher rejects
  it before inventory. Verified cleanup restores the original ledger bytes
  exactly. No old runtime/native source or stock binary is overwritten.
- Final full-suite controlled OOM reaches 67,108,864-byte cgroup peak and
  manager `oom-kill`; group counter 1 witnessed in that run. Task fixture
  witnesses pids.events.max=1 / EAGAIN. Sampled successful task-fixture family
  RSS=65,740,800 bytes (includes outside controller/client; shared overcount).
  Native peak RAM is **not measured**. Timeout fixture ends in ~3.20 seconds.

Preservation audits cover protected 17 pins, dirty DFT HEAD/status, stock/all
prior candidates including `de000d4`, sessions, original ledger byte identity,
closed cgroup ledger, no flock holders and **only our recorded** transient units
unloaded. Detailed measurement artifacts remain project-local and evidence is
committed on the MCT research branch only; no DFT commit/main merge.

**Qualified next step:** adopt this as a tested owned-family backend component
while retaining every original native gate. `policy_decision.md` rejects using
the cap as a foreign-MPI exclusion certificate. Aggregate disk/host headroom,
native initial state/readback/collectives and full envelope remain unqualified.
No expensive/native job or physical x_c prediction follows from this PASS.
