# Finite native collective validation: preregistration

2026-10-13; starts clean MCT `ba48c97`, original research branch/session.
This is a **new LOCAL-OWNED-EXECUTION claim**, not passage of the original
strict host-wide exclusion gate. No QE/HSE, material spectrum, timing benchmark
or physical x_c is admissible. No permission or host configuration changes.

## Ordered, fail-closed experiment

1. One fixed **non-MPI** isolation prerequisite: private user/network namespace
   under existing UID1001 manager. Verify a new network namespace with loopback
   only, actual kernel 64-MiB/swap0/tasks4 controls, fixed executable fingerprint,
   8-second manager bound, 16-KiB file/output bound, independent foreground
   MemAvailable >=4GiB / disk >=10GiB and exact cleanup. No network connect or
   data is sent. Failure prohibits native MPI; do not retry with host networking.
   **11:30 UTC diagnostic amendment:** first preflight had a dependency-type
   error before launching any unit, then the first actual non-MPI unit exited91
   before observations. The probe combined four error sites and omitted errno.
   Preserve both negatives. Permit one diagnostic-only source correction/run
   to distinguish the failed site; unchanged restrictions, no MPI or fallback.
   A second failure ends this prerequisite workstream.
2. Only after isolation and all owner/admission integration gates pass: at most
   **one** pinned standalone two-rank MPI harness under a distinct typed scope
   `LOCAL_MPI_COLLECTIVE_ONLY`. Exact manager cap <=512MiB, swap0, tasks<=32,
   45-second manager/monotonic bound. This scope must never issue QE NATIVE or
   ABI_NO_MPI receipts. Existing cgroup controller/guard remain unchanged.
3. Required observations from that one run: real MPI_Init, size=2/ranks0,1,
   live kernel-authenticated all-rank registration; same verified unit cgroup,
   network namespace and node; barrier and exact integer sum/max/allgather;
   normalization of negative/positive/INT_MIN application status before max;
   bounded outputs and complete family/lease cleanup. Application-status
   injection is **not** an actual MPI library failure. MPI_Init or transport
   failures abort/refuse rather than fabricate collective error normalization.
4. Any first unmet gate or unexpected mismatch stops this native experiment.
   No second MPI attempt, runtime/environment workaround, new job queue or QE
   fixture follows. Independent build/serial/source work may finish afterwards.

## Network meaning and decision gate

Installed Open MPI 5.0.10 supports `btl=self,sm` for same-node MPI **data**.
Installed PRRTE 3.0.8 advertises only `oob=tcp` for runtime bootstrap/control.
Those facts do not establish a TCP-free launch. We require no external/host
network or remote ranks, with loopback runtime control confined to a separately
verified network namespace; we expressly do **not** call that “no TCP sockets”.
If “no network” requires forbidding even private loopback, the current runtime
has no qualified launch path and MPI remains NO-GO. No such fallback is run.

The previous owner uses an **abstract** Unix lifeline, which is also scoped to
the network namespace. A future isolated owner must first implement and test
a short pathname Unix lifeline across namespaces, retain SCM_RIGHTS flock
escrow/durable closed-family recovery and independently verify each rank. The
already-tested owner cannot simply be invoked with PrivateNetwork and assumed
to work. No native launch until this bridge is qualified.

## Predicted scientific outcome and disconfirmation

Nonmalicious unrelated CPU/MPI activity need not change the exact integer
result of an isolated communicator. It can change scheduling, pressure and
completion. This permits a conditional local correctness claim after all
gates, not a host exclusivity or guaranteed continuous resource-floor claim.
Any observed pressure, task/memory limit event, membership change, missing
receipt, timeout, file-cap breach, state/pin change or incorrect result
invalidates PASS. Original strict host exclusion remains UNPASSED in every
outcome. EXX/QE initial state, backend/layout, full envelope and readback are
separate gates and no collective-only result retires them.
