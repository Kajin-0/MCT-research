# LOCAL-OWNED-EXECUTION: separate, conditional validation claim

## What host exclusion can and cannot establish

**PROVEN UNDER ASSUMPTIONS.** Fix a finite local communicator, executable,
inputs, algorithm and private writable state. Suppose message/collective
semantics are correct, arithmetic is defined, all ranks execute the same
prescribed collective sequence, and no external actor changes their state or
communication objects. Adding an unrelated MPI process changes neither the
communicator membership nor those mathematical operations. In particular,
the harness computes the exact integer sum 1+2=3 and Boolean maximum of
normalized application statuses. A foreign process can delay or prevent
completion; it need not change a completed correct result. Therefore absence
of all foreign MPI is **not logically necessary** for this conditional local
correctness claim. This is not a new MPI theorem or a host exclusion certificate.

For floating-point EXX, additional conditions include fixed rank/FFT/reduction
layout, component selection, compiler/arithmetic modes, identical actual wave
and density/occupation state, no writable file aliasing and valid completion.
A standalone collective result cannot establish any of these QE conditions or
streamed EXX equivalence. Host-wide exclusion alone would not establish them
either. Unrelated resource contention disqualifies timing claims and may cause
an abort; accepting numerical data after a failed monitor is forbidden.

**Counterexample to owned=>exclusive:** two hosts have identical owned unit
identity, kernel caps and rank receipts; one has a foreign MPI process outside
the unit. Owned evidence cannot distinguish them. This retains the previous
negative theorem and the original strict acceptance gate unchanged.

**Counterexample to continuously guaranteed host floors:** let independent
monitors sample at t_i and t_i+delta. An unrelated allocator/writer can reduce
available memory/free disk between samples and release/delete before the next
sample. Both observations pass although the continuous floor failed. If a
separately justified drift bound |H(t)-H(t_i)|<=L_H delta existed, a margin
H(t_i)>=H_min+L_H delta would suffice. No such bound on all foreign actors is
known here. Kernel limits on our family and actual disk extents do not supply
it. Thus this pilot claims sampled, fail-closed pressure admission with short
exposure and hard owned caps; it does not claim reserved host RAM or a proven
continuous global 4/10-GiB floor. An original acceptance claim requiring those
unconditionally remains unpassed.

## Admission contract, not an executable authorization switch

| Required gate | New local collective-only requirement | Current result |
|---|---|---|
| Payload | Exact standalone C harness and argv; no arbitrary command, QE or HSE | Source/compile pins retained; runtime issuer absent |
| Typed binding | Distinct JOB/PROFILE; magic R07C, scope3 LOCAL_MPI_COLLECTIVE_ONLY; kernel live grant | Compiled codec tests PASS; production rank registry NOT RUN |
| Unit ownership | User manager UID1001, fixed unit name/InvocationID/MainPID/cgroup inode; pidfds, SCM_RIGHTS lock escrow, durable legacy marker | Original non-MPI backend tested; isolated adapter bridge not qualified |
| Network/ranks | Fresh private network namespace, loopback only, no inherited network fds, no remote ranks; all rank/daemon membership checked | **First local launch blocker: self netns identity EACCES** |
| Limits | memory.max<=536870912; swap.max=0; pids.max<=32; oom.group=1; manager+monotonic runtime<=45s, kill whole group | Required, not measured on an MPI family |
| Host pressure | Independent outside controller and inside guard sample <=100ms; MemAvailable>=4GiB, ext4 free>=10GiB; abort on read failure/pressure/events | Contract only; no continuous-floor theorem |
| Disk/output | Exact quota/block admission and actual 64-bit rank extents; isolated temp/shm/session paths, bounded log sink, inode/file/block envelope | Backend guards retained; complete MPI producer envelope still unqualified |
| All-rank receipts | True MPI_Init rank/size=0,1/2; two unique live executable identities in the same unit and namespace; CHECK after both REGISTER | Harness calls added; actual MPI registration NOT TESTED |
| Completion | Exact sum/allgather/status results, no MPI error/timeout/OOM/task/file instability; pinned run state unchanged | NOT RUN |
| Cleanup | Verified empty exact cgroup, all witnessed identities retired, capture terminal result, restore legacy bytes, release flock last | Probe cleanup measured; full MPI descendant cleanup NOT TESTED |

The original scope1/2 launchers, `hostwide_gate`, strict inventory and all QE
gates remain unchanged. No local production launch function has been installed.
Passing a serial R07C codec test does not issue authority; a submitted Boolean,
environment variable or file cannot replace the live owner/cgroup evidence.

## Exact future local-only sequence and refusal points

1. Use a single-use, durably recorded attempt ID. Pin C source/binary,
   installed mpirun/prterun, MPI/PMIx components, compiler and all dependencies;
   check the closed old/new ledgers and exclusive cooperating-owner flock.
   No host-wide `/proc/maps` scan or foreign process changes.
2. Build the unit with <=512MiB/swap0/tasks32/45s, no restart, group OOM/kill,
   no privilege acquisition, bounded per-file/core/output limits. Reject any
   actual manager/kernel mismatch. The foreground owner independently monitors
   host pressure, cgroup events, monotonic wall time and bounded pipes. Unit
   runtime is the independent fallback if the owner dies.
3. Certify a **fresh** network namespace and only loopback, and verify it for
   each actual rank. Installed `btl=self,sm` selects local MPI data, while the
   advertised PRRTE `oob=tcp` still uses runtime TCP. Loopback control must be
   confined to the new namespace; it is not called TCP-free. Socket inheritance,
   other network devices, service-spawned/migrated ranks or unreadable owned
   identity cause refusal. If zero TCP is mandatory, this stack has no
   qualified solution. No namespace/global permission change is permitted.
4. The old abstract owner lifeline is not cross-namespace transport. First
   qualify a short pathname AF_UNIX lifeline with kernel peer/pidfd identity,
   SCM_RIGHTS fd escrow and durable interruption/recovery behavior. The server
   must inspect only verified owned cgroup members, not global process tables.
   The current self-netns EACCES cannot be treated as a passing observation.
5. Use a clean allowlisted runtime environment, not inherited OMPI/PMIX/PRTE,
   scheduler, hostfile, SSH or preload settings. A fixed launcher must request
   exactly two localhost ranks, no remote launch path, no recovery/respawn,
   OB1 with `self,sm`, pinned components and private PRRTE/PMIx/TMPDIR/shm
   backing paths. Runtime selection and actual descendants require evidence;
   CLI flags alone are insufficient. Installed sm default is a 16-MiB segment,
   with `/dev/shm` backing: both defaults must enter the disk/resource design,
   not disappear from a “bounded files” claim.
6. Reserve checked, quota-admitted extents and a complete output envelope before
   ranks execute. Initial host margin should exceed the 4GiB floor by the whole
   512MiB owned budget plus independently bounded outside-control costs; disk
   must exceed 10GiB by all admitted allocations/output. Keep host/shared-service
   costs and RSS shared overcount separate from cgroup accounting. No numeric
   whole-runtime envelope is invented from a payload-only expression.
7. After MPI_Init, register each actual rank through R07C. Verify SO_PEERCRED,
   pidfds/start ticks, binary/argv, actual cgroup/namespace, common node and
   distinct identities. Hold CHECK until both are live. A peer outside the
   isolated unit or with the old scope/magic refuses. Before Init, the v2
   harness requires a live PREINIT action3 receipt with (-1,0) sentinel; this
   permits only family runtime setup and makes no claim of MPI world identity.
   The production server must reject ordinary rank values at this phase and
   bind that kernel process to the fully admitted owner/unit/profile. A source
   review found/fixed v1's missing pre-Init call. Receipt codec/source order is
   tested; no production issuer or runtime validation is claimed.
8. Perform barrier, exact integer sum/allgather and application-status phases
   once. Normalize s to (s!=0) before MPI_MAX; signed raw statuses can otherwise
   disappear. MPI_ERRORS_RETURN is not fault tolerance: a real Init/transport
   failure does not imply another allreduce is safe. Abort via the verified
   owner/group, and do not claim distributed normalization across failed ranks.
9. Any instability invalidates the run. Capture bounded logs, counters and
   source/component fingerprints; prove exact unit empty/identities retired
   before restoring the old closed ledger/releasing escrow. Failure consumes
   the attempt; no retry/campaign. The one presently authorized MPI attempt
   has **not** been used because prerequisite admission failed.

## Primary references and novelty boundary

- [systemd v257 execution semantics](https://raw.githubusercontent.com/systemd/systemd/v257/man/systemd.exec.xml):
  private network namespace and abstract/pathname Unix distinction; user-manager
  user namespaces and socket-family restriction limitations. Configured
  properties are not substitutes for observations.
- [Open MPI 5.0.10 shared-memory transport](https://docs.open-mpi.org/en/v5.0.10/tuning-apps/networking/shared-memory.html):
  same-node sm BTL. Local data transport does not prove runtime isolation.
- [Open MPI error-handler contract](https://docs.open-mpi.org/en/v5.0.10/man-openmpi/man3/MPI_Comm_set_errhandler.3.html):
  returned errors do not guarantee continued execution.
- [Open MPI initialization/thread contract](https://docs.open-mpi.org/en/v5.0.10/man-openmpi/man3/MPI_Init_thread.3.html):
  initialization/thread-level checks and environment overrides.

Established MPI/cgroup semantics and conditional mathematical reasoning;
no scientific novelty, physical HgCdTe validation or new gap claim is made.
