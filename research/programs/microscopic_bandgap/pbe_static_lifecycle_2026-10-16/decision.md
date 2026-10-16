# Gate A NO-GO — actual launcher/startup owner refusal

**2026-10-16 14:33 UTC; baseline9f59814. One live attempt, zero retries,
zero negative attempts, zero QE/PW/HSE/SCF/saved-density actions. STOP.**

The new, separately frozen NON_SCIENCE lifecycle owner entered a real transient
systemd user service at14:31:01 UTC. It **did not qualify two-rank execution**.
The first observed failure was a disappearing per-FD path
`/proc/1978386/fd/9` during Account.sample. Protocol.inventory_failure refused
`incomplete/unknown live final pair`. Neither rank had authenticated begin or
final; no MPI collective completion or native packet was observed. The
conditional missing-final experiment was correctly withheld, not retried.

| Condition | Measured outcome |
|---|---|
| Source/compiler/import/read-only preflight | PASS for this harness. Actual MPI-linked C ELF compiled; distinct R07L/scope1601; old R07S/scope16 science release remains NOT_GRANTED. |
| Actual systemd startup/kernel controls | PASS for observed startup:12GiB memory.max, swap.max0, pids.max12, memory.oom.group1,600s, no restart/delegation, outside holder. |
| Full live FD accounting | **REFUSED** during launcher startup, before any authenticated world rank. No partial inventory accepted. |
| Both-rank live begin/final / collective/readback / wait0 | **NOT DEMONSTRATED**. Launcher command specifies two local ranks; command intent is not evidence that MPI_Init completed. |
| Failure and cleanup | Actual owner preserved REFUSED_ABSORBING; stopped only the bound same-invocation unit. Known actor pidfd exit, foreground wait1, managerfailed/exit1/MainPID0 and empty/absent original cgroup were checked. Independently checked afterwards. |
| Deliberate negative; crash/cancel | Negative NOT RUN because positive failed. Crash/cancel/retirement predicates only modeled offline, not live systemd qualification. |
| Gate B / physics | NOT RELEASED. No scientific peak bound,2meV certificate, Hamiltonian observation, material gap or x_c. |

## Actual measurements and evidence

Unit `r07-owned-dff45c7befde403e9f4c977891cb0bb6.service`, invocation
`81277654cf2748f1995afe1cfb7c90c0`. Refusal after **0.202116s** in owner
monotonic timing; shell command including cleanup took0.506933s. Final manager
MemoryPeak **2,789,376B**; sampled kernel peak1,835,008B. Sampled family RSS
9,039,872B includes shared pages and is NOT the same accounting as cgroup
memory. Sampled outside-holder RSS **24,408,064B**, not a certified peak of all
possible owner/readback work. Minimum sampled host available29,910,380,544B;
disk49,559,183,360B. Two resource-check samples occurred before refusal.

Independent post-cleanup two-root retained output is **67,252,224B**, including
64MiB escrow and per-observed-inode metadata allowance. This is sampled block
accounting, not a continuous quota or proof against between-sample bursts or
external writers. No scientific memory/performance comparison follows.

Exact [RESULT](evidence/RESULT.json), [startup](evidence/STARTED.json),
[cleanup](evidence/CLEANUP.json), [argv/properties](evidence/COMMAND.json),
[preregistration](preregistration.md), [frozen pins](frozen_execution.json),
[preflight](preflight.json), [build](build.json), [offline checks](offline_results.json)
and [independent verification](verification.json) are retained. The executable
and empty private outputs remain off-repository with hashes; no public raw
scientific data was acquired. Native fixture ELF SHA256:
`2d3b4a44db796e541b937e4f14e5b54e3cbc328cc9be732e356795d130714c57`.

## Precise obstruction and evidence limitations

The reported PID is the manager's actual mpirun MainPID. A finite `/proc/PID/fd`
enumeration followed by readlink/stat encountered ENOENT. The traceback does
not distinguish readlink from stat on that Python line, nor prove whether
individual FD close or whole-task exit caused disappearance. **No teardown
race or still-live exit-mask claim is inferred.** There was no prior final pair,
so the source correctly refuses either way. This is independent of the old
unshared scientific diagnostic's live-EACCES failure; that old failure stays
unchanged and unqualified.

The failure's pw.out is empty. The code drains stdout in the normal loop,
but does not drain a last producer message in its exception path; no missing
MPI diagnostic is invented. Managerexit1 does not establish why mpirun exited.
The owner cleanup schema contains `rank_pidfds_exited:true`, but **no ranks
were registered**; that conjunction is vacuous and is NOT rank-exit evidence.
Cleanup rests on known actor pidfds, manager/wait and cgroup checks. These
reporting limitations and the actual failure remain immutable.

Minimum next lifecycle input, outside this completed authorization: a reviewed
source/process-lifetime account for mpirun bootstrap FD churn that can meet
the complete-owned-inventory condition, independently tested before another
separately authorized live attempt. Merely skipping ENOENT, waiting for JOBDONE,
or calling a missing PID retired would weaken the gate and is rejected. No
such remedy, new service or Gate B authorization is issued here.

## Scope relative to9f59814

The production-derived `owner.run`, actual systemd creation and FD-accounting
path are now **measured**, exposing a real startup refusal. `protocol.py` keeps
fresh socket/process pidfds, typed identity, strict absorbing refusal and3s
terminal-pending rules. The C ABI changes only magic/scope/environment namespace
and comment; `mpi_fixture.c` uses real MPI world rank, collectives, checked close
and live final. The dedicated reader cannot accept science packets. No mock
manager/cgroup was used in the live attempt. Positive terminal/readback/final
logic nevertheless remains unqualified because it was never reached.

Original implementation/build/refusals,126 profile pins,14 refused raw pins,
protected DFT dirty status/diff/files, stock QE and historical ledger independently
match. No host-wide inventory, private-netns proof, unrelated unit modification,
DFT write, original HSE16 change, historical-goal update or new session occurred.
Failed **transient metadata** is retained; it has no active process or restart.
R07 scientific/registry status remains gated and physical x_c OPEN.
