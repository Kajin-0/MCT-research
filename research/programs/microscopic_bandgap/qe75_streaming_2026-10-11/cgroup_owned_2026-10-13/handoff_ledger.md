# Reset handoff — cgroup owned-family phase

Read `../EXECUTION_PLAN.md`, this `decision.md`, `design_and_boundaries.md`,
`policy_decision.md`, `validation.json`, then DFT AGENTS. Starting clean
`de000d4`, existing research branch; historical goal unchanged.

- Private root: DFT `.local/qe75_lowram_20261011/cgroup_owned_20261013/`.
  Compiled C workers v1 and v2 both retained. Source uses only `rank_worker.v2`.
  No MPI/PW link, launcher, native fixture, queue or new supervisor/session.
- UID1001 user bus `/run/user/1001/bus`; systemd257.9; actual cgroup-v2 memory/
  swap/pids controls verified. Normal 128MiB, controlled OOM64MiB, TasksMax16,
  per-file128KiB, log32KiB, 3/8s runtime and 1s stop. **These are small tests.**
- Full13-method suite passes; three final focused checks pass on fd escrow and
  crash recovery. Kernel task EAGAIN and OOM/cleanup measured. Real MPI/NATIVE
  scope remains unissued. Corrected sampling/collection and actor-release
  failures retained in `negative_findings.json` / private source-condition
  reports. The OOM kill counter was initially missed, not interpreted as zero.
- Guard is user-service MainPID, not controller child. Kernel peer credentials,
  actual manager invocation, cgroup inode/limits, interpreter/source whitelist,
  pidfds and an abstract Unix lifeline establish binding.
- Guard obtains legacy flock and sends duplicate via SCM_RIGHTS. Controller
  holds it until verified unit closure; independent post-guard-exit lock attempt
  proves exclusion. A temporary durable `CGROUP_RUNNING` compatibility marker
  prevents legacy restart after a double crash; no legacy source changed.
  Original `CURRENT_FAMILY.json` bytes escrowed and restored **exactly** after
  verified closure. Owner-crash recovery captures/resets only that owned failed
  unit. All recorded transient units are now unloaded, both ledgers FINISHED,
  no lease held. Never overwrite an unknown live marker.
- New adapter executes only hashed tiny C cases. No arbitrary command parameter
  or flag can issue native execution. Missing manager, source/profile/limits,
  invocation, resources or scope refuses. No global inventory scan occurs.
- Kernel memory accounting is not summed RSS; external controller/run-client,
  shared mappings, host MemAvailable and disk remain separate. File size and
  log caps do not enforce an aggregate filesystem quota or host-wide reserve.
- The previous no-accessible-control **availability observation** is superseded
  by this measured capability. Foreign-MPI non-identifiability theorem remains.
  `policy_decision.md` proposes adding this control, never silently replacing
  host-wide exclusion. Native state/common-wave/readback/full-resource gates
  remain unpassed; physical x_c remains absent.

## Permitted reproduction

DFT `source scripts/env.sh`; absolute path to this package's
`preservation.py` is read-only. `test_owned.py` runs the finite tiny systemd
fixtures; named test methods may select focused checks. Do not repeat complete
suites without a changed gate/failure. `build.py` is one-shot and preserves
existing binaries. No installation, sudo, Docker or manager configuration is
needed. Version/dependency/command/property/source hashes are in evidence.

Do not call native binaries or MPI, modify any preexisting supervisor/session,
change target physics, merge main, make a DFT commit, create agents/sessions,
resume the old goal, or waive foreign inventory/readback/resource gates.
This bounded phase stops after validated commit/push; any next scope must
retire a new acceptance gate or supply indispensable independent evidence.
